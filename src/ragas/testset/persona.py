import logging
import typing as t

import numpy as np
from langchain_core.callbacks import Callbacks
from pydantic import BaseModel

from ragas.executor import run_async_batch
from ragas.llms.base import BaseRagasLLM
from ragas.prompt import PydanticPrompt, StringIO
from ragas.testset.graph import KnowledgeGraph, Node

logger = logging.getLogger(__name__)


def default_filter(node: Node) -> bool:
    if (
        node.type.name == "DOCUMENT" or node.type.name == "CHUNK"
    ) and node.properties.get("summary_embedding") is not None:
        return True
    else:
        return False


class Persona(BaseModel):
    name: str
    role_description: str


class PersonaGenerationPrompt(PydanticPrompt[StringIO, Persona]):
    instruction: str = (
        "Dựa trên bản tóm tắt được cung cấp, hãy tạo ra một chân dung người dùng (persona) "
        "có khả năng cao sẽ tương tác hoặc hưởng lợi từ nội dung này. Bao gồm một tên gọi độc đáo "
        "và một mô tả ngắn gọn về vai trò, danh tính của họ."
    )
    input_model: t.Type[StringIO] = StringIO
    output_model: t.Type[Persona] = Persona
    examples: t.List[t.Tuple[StringIO, Persona]] = [
        (
            StringIO(
                text="Hướng dẫn Tiếp thị Kỹ thuật số giải thích các chiến lược thu hút khán giả trên nhiều nền tảng trực tuyến khác nhau."
            ),
            Persona(
                name="Chuyên viên Tiếp thị Kỹ thuật số",
                role_description="Tập trung vào việc thu hút khán giả và phát triển thương hiệu trên môi trường trực tuyến.",
            ),
        )
    ]


class PersonaList(BaseModel):
    personas: t.List[Persona]

    def __getitem__(self, key: str) -> Persona:
        for persona in self.personas:
            if persona.name == key:
                return persona
        raise KeyError(f"Không tìm thấy chân dung người dùng (persona) nào có tên '{key}'")


def generate_personas_from_kg(
    kg: KnowledgeGraph,
    llm: BaseRagasLLM,
    persona_generation_prompt: PersonaGenerationPrompt = PersonaGenerationPrompt(),
    num_personas: int = 3,
    filter_fn: t.Callable[[Node], bool] = default_filter,
    callbacks: Callbacks = [],
) -> t.List[Persona]:
    """
    Tạo các chân dung người dùng (personas) từ một đồ thị tri thức (knowledge graph)
    dựa trên việc gom cụm các bản tóm tắt tài liệu tương đồng.

    Tham số:
        kg: KnowledgeGraph
            Đồ thị tri thức dùng để tạo personas.
        llm: BaseRagasLLM
            Mô hình ngôn ngữ lớn (LLM) được sử dụng để tạo persona.
        persona_generation_prompt: PersonaGenerationPrompt
            Prompt được sử dụng để tạo persona.
        num_personas: int
            Số lượng personas tối đa cần tạo.
        filter_fn: Callable[[Node], bool]
            Hàm dùng để lọc các node trong đồ thị tri thức.
        callbacks: Callbacks
            Các hàm callback sử dụng trong quá trình tạo sinh.

    Trả về:
        t.List[Persona]
            Danh sách các chân dung người dùng (personas) đã được tạo.
    """

    nodes = [node for node in kg.nodes if filter_fn(node)]
    if len(nodes) == 0:
        raise ValueError(
            "Không có node nào thỏa mãn bộ lọc đã cho. Hãy thử thay đổi filter_fn."
        )

    summaries = [node.properties.get("summary") for node in nodes]
    summaries = [summary for summary in summaries if isinstance(summary, str)]
    num_personas = min(num_personas, len(summaries))

    embeddings = []
    for node in nodes:
        embeddings.append(node.properties.get("summary_embedding"))

    embeddings = np.array(embeddings)
    cosine_similarities = np.dot(embeddings, embeddings.T)

    groups = []
    visited = set()
    threshold = 0.75

    for i, _ in enumerate(summaries):
        if i in visited:
            continue
        group = [i]
        visited.add(i)
        for j in range(i + 1, len(summaries)):
            if cosine_similarities[i, j] > threshold:
                group.append(j)
                visited.add(j)
        groups.append(group)

    top_summaries = []
    for group in groups:
        representative_summary = max([summaries[i] for i in group], key=len)
        top_summaries.append(representative_summary)

    if len(top_summaries) <= num_personas:
        top_summaries.extend(
            np.random.choice(top_summaries, num_personas - len(top_summaries))
        )

    # Sử dụng run_async_batch để tạo sinh các persona song song
    kwargs_list = [
        {
            "llm": llm,
            "data": StringIO(text=summary),
            "callbacks": callbacks,
            "temperature": 1.0,
        }
        for summary in top_summaries[:num_personas]
    ]
    persona_list = run_async_batch(
        desc="Đang khởi tạo chân dung người dùng (personas)",
        func=persona_generation_prompt.generate,
        kwargs_list=kwargs_list,
    )

    return persona_list