import typing as t

from pydantic import BaseModel

from ragas.prompt import PydanticPrompt
from ragas.testset.persona import Persona


class QueryCondition(BaseModel):
    persona: Persona
    term: str
    query_style: str
    query_length: str
    context: str
    llm_context: t.Optional[str] = None


class GeneratedQueryAnswer(BaseModel):
    query: str
    answer: str


class QueryAnswerGenerationPrompt(PydanticPrompt[QueryCondition, GeneratedQueryAnswer]):
    instruction: str = (
        "Hãy tạo một cặp câu hỏi single-hop (câu hỏi một bước) và câu trả lời dựa trên các điều kiện được chỉ định "
        "(hình mẫu nhân vật - persona, thuật ngữ - term, phong cách - style, độ dài - length) và ngữ cảnh (context) được cung cấp. "
        "Đảm bảo câu trả lời hoàn toàn trung thực với ngữ cảnh, chỉ sử dụng thông tin trực tiếp từ ngữ cảnh được cung cấp.\n\n"
        "### Hướng dẫn chi tiết:\n"
        "1. **Tạo câu hỏi (Query)**: Dựa trên ngữ cảnh, persona, thuật ngữ, phong cách và độ dài được yêu cầu, hãy tạo một câu hỏi "
        "phù hợp với góc nhìn của nhân vật đó và có lồng ghép thuật ngữ đã cho.\n"
        "2. **Tạo câu trả lời (Answer)**: Chỉ sử dụng nội dung từ ngữ cảnh được cung cấp để xây dựng câu trả lời chi tiết cho câu hỏi trên. "
        "Tuyệt đối không thêm bất kỳ thông tin nào không có sẵn hoặc không thể suy luận trực tiếp từ ngữ cảnh.\n"
        "3. **Ngữ cảnh bổ sung (nếu có)**: Nếu có `llm_context`, hãy sử dụng nó làm định hướng cho loại câu hỏi cần tạo "
        "(ví dụ: câu hỏi so sánh, câu hỏi hướng dẫn từng bước, câu hỏi mang tính ứng dụng) và cấu trúc câu trả lời tương ứng. "
        "Tuy nhiên, vẫn phải đảm bảo toàn bộ nội dung câu trả lời chỉ lấy từ ngữ cảnh (context) gốc.\n"
    )
    input_model: t.Type[QueryCondition] = QueryCondition
    output_model: t.Type[GeneratedQueryAnswer] = GeneratedQueryAnswer
    examples: t.List[t.Tuple[QueryCondition, GeneratedQueryAnswer]] = [
        (
            QueryCondition(
                persona=Persona(
                    name="Kỹ sư phần mềm",
                    role_description="Tập trung vào các thực hành lập trình tốt nhất và thiết kế hệ thống.",
                ),
                term="microservices",
                query_style="Trang trọng",
                query_length="Vừa phải",
                context="Microservices (kiến trúc vi dịch vụ) là một phong cách kiến trúc mà trong đó các ứng dụng được cấu trúc thành một tập hợp các dịch vụ lỏng lẻo (loosely coupled). "
                "Mỗi dịch vụ được chia nhỏ một cách tinh gọn và chỉ tập trung vào một chức năng duy nhất.",
            ),
            GeneratedQueryAnswer(
                query="Mục đích của kiến trúc microservices trong thiết kế phần mềm là gì?",
                answer="Microservices được thiết kế để cấu trúc ứng dụng thành một tập hợp các dịch vụ liên kết lỏng lẻo, trong đó mỗi dịch vụ chỉ tập trung xử lý một chức năng duy nhất.",
            ),
        ),
    ]