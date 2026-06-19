import logging
import typing as t
from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from ragas.prompt import PydanticPrompt
from ragas.testset.graph import KnowledgeGraph, Node
from ragas.testset.graph_queries import get_parent_nodes
from ragas.testset.transforms.base import LLMBasedNodeFilter

logger = logging.getLogger(__name__)


DEFAULT_RUBRICS = {
    "score1_description": "Nội dung trang hoàn toàn không liên quan hoặc không phù hợp với các chủ đề chính hoặc nội dung của bản tóm tắt tài liệu.",
    "score2_description": "Nội dung trang chỉ phù hợp một phần với bản tóm tắt tài liệu, chứa các chi tiết không liên quan hoặc thiếu thông tin quan trọng liên quan đến các chủ đề chính của tài liệu.",
    "score3_description": "Nội dung trang phản ánh khá khái quát bản tóm tắt tài liệu nhưng có thể bỏ sót các chi tiết cốt lõi hoặc thiếu chiều sâu khi giải quyết các chủ đề chính.",
    "score4_description": "Nội dung trang khớp tốt với bản tóm tắt tài liệu, bao quát được các chủ đề chính với những lỗ hổng không đáng kể hoặc rất ít thông tin ngoài lề.",
    "score5_description": "Nội dung trang có tính liên quan cao, chính xác và phản ánh trực tiếp các chủ đề cốt lõi của bản tóm tắt tài liệu, bao hàm tất cả các chi tiết quan trọng và giúp hiểu sâu hơn về các chủ đề của tài liệu.",
}


class QuestionPotentialInput(BaseModel):
    document_summary: str = Field(
        ...,
        description="Bản tóm tắt của tài liệu nhằm cung cấp ngữ cảnh để đánh giá node.",
    )
    node_content: str = Field(
        ...,
        description="Nội dung của node cần đánh giá về tiềm năng tạo câu hỏi.",
    )
    rubrics: t.Dict[str, str] = Field(..., description="Bộ tiêu chí chấm điểm (rubric).")


class QuestionPotentialOutput(BaseModel):
    score: int = Field(
        ...,
        description="Điểm số đánh giá trong khoảng từ 1 đến 5",
    )


class QuestionPotentialPrompt(
    PydanticPrompt[QuestionPotentialInput, QuestionPotentialOutput]
):
    instruction = (
        "Dựa trên bản tóm tắt tài liệu và nội dung của node được cung cấp, hãy chấm điểm nội dung của node theo thang điểm từ 1 đến 5 dựa trên bộ tiêu chí (rubrics) đi kèm."
        ""
    )
    input_model = QuestionPotentialInput
    output_model = QuestionPotentialOutput


@dataclass
class CustomNodeFilter(LLMBasedNodeFilter):
    """
    Trả về True nếu điểm số đánh giá nhỏ hơn hoặc bằng min_score (để lọc bỏ node yếu).
    """

    scoring_prompt: PydanticPrompt = field(default_factory=QuestionPotentialPrompt)
    min_score: int = 2
    rubrics: t.Dict[str, str] = field(default_factory=lambda: DEFAULT_RUBRICS)

    async def custom_filter(self, node: Node, kg: KnowledgeGraph) -> bool:
        if node.type.name == "CHUNK":
            parent_nodes = get_parent_nodes(node, kg)
            if len(parent_nodes) > 0:
                summary = parent_nodes[0].properties.get("summary", "")
            else:
                summary = ""
        else:
            summary = node.properties.get("summary", "")

        if summary == "":
            logger.warning(
                f"Node {node.id} không có summary (bản tóm tắt). Bỏ qua bước lọc."
            )
            return False

        prompt_input = QuestionPotentialInput(
            document_summary=summary,
            node_content=node.properties.get("page_content", ""),
            rubrics=self.rubrics,
        )
        response = await self.scoring_prompt.generate(data=prompt_input, llm=self.llm)
        
        # Giữ nguyên logic lọc node dựa trên min_score
        return response.score <= self.min_score