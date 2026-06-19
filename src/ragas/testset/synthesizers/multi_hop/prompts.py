import typing as t

from pydantic import BaseModel, Field

from ragas.prompt import PydanticPrompt
from ragas.testset.persona import Persona


class ConceptsList(BaseModel):
    lists_of_concepts: t.List[t.List[str]] = Field(
        description="Một danh sách chứa các danh sách khái niệm từ mỗi node"
    )
    max_combinations: int = Field(
        description="Số lượng tổ hợp khái niệm tối đa cần tạo", default=5
    )


class ConceptCombinations(BaseModel):
    combinations: t.List[t.List[str]]


class ConceptCombinationPrompt(PydanticPrompt[ConceptsList, ConceptCombinations]):
    instruction: str = (
        "Tạo các tổ hợp bằng cách ghép cặp các khái niệm từ ít nhất hai danh sách khác nhau.\n"
        "**Hướng dẫn:**\n"
        "- Xem xét các khái niệm từ mỗi node.\n"
        "- Xác định các khái niệm có thể kết nối hoặc đối chiếu với nhau một cách logic.\n"
        "- Tạo các tổ hợp bao gồm các khái niệm thuộc về các node khác nhau.\n"
        "- Mỗi tổ hợp phải chứa ít nhất một khái niệm từ hai hoặc nhiều node trở lên.\n"
        "- Liệt kê các tổ hợp một cách rõ ràng và súc tích.\n"
        "- Không lặp lại cùng một tổ hợp nhiều hơn một lần."
    )
    input_model: t.Type[ConceptsList] = (
        ConceptsList  # Chứa danh sách các khái niệm từ mỗi node
    )
    output_model: t.Type[ConceptCombinations] = (
        ConceptCombinations  # Chứa danh sách các tổ hợp khái niệm được tạo ra
    )
    examples: t.List[t.Tuple[ConceptsList, ConceptCombinations]] = [
        (
            ConceptsList(
                lists_of_concepts=[
                    ["Trí tuệ nhân tạo", "Tự động hóa"],  # Khái niệm từ Node 1
                    ["Y tế", "Bảo mật dữ liệu"],  # Khái niệm từ Node 2
                ],
                max_combinations=2,
            ),
            ConceptCombinations(
                combinations=[
                    ["Trí tuệ nhân tạo", "Y tế"],
                    ["Tự động hóa", "Bảo mật dữ liệu"],
                ]
            ),
        )
    ]


class QueryConditions(BaseModel):
    persona: Persona
    themes: t.List[str]
    query_style: str
    query_length: str
    context: t.List[str]
    llm_context: t.Optional[str] = None


class GeneratedQueryAnswer(BaseModel):
    query: str
    answer: str


class QueryAnswerGenerationPrompt(
    PydanticPrompt[QueryConditions, GeneratedQueryAnswer]
):
    instruction: str = (
        "Tạo một câu hỏi suy luận đa bước (multi-hop query) và câu trả lời tương ứng dựa trên các điều kiện được chỉ định "
        "(hình mẫu/persona, chủ đề, phong cách, độ dài) và ngữ cảnh (context) được cung cấp. Các chủ đề (themes) đại diện cho "
        "một tập hợp các cụm từ được trích xuất hoặc tạo ra từ ngữ cảnh, nhằm làm nổi bật tính phù hợp của ngữ cảnh đã chọn "
        "để tạo câu hỏi đa bước. Hãy đảm bảo câu hỏi lồng ghép các chủ đề này một cách rõ ràng.\n"
        "### Hướng dẫn:\n"
        "1. **Tạo Câu Hỏi Đa Bước (Multi-Hop Query)**: Sử dụng các đoạn ngữ cảnh và chủ đề được cung cấp để tạo thành một câu hỏi "
        "đòi hỏi phải kết hợp thông tin từ nhiều đoạn ngữ cảnh khác nhau (ví dụ: `<1-hop>` và `<2-hop>`). Đảm bảo câu hỏi lồng ghép "
        "rõ ràng một hoặc nhiều chủ đề và phản ánh mối liên quan của chúng với ngữ cảnh.\n"
        "2. **Tạo Câu Trả Lời**: Chỉ sử dụng nội dung từ ngữ cảnh được cung cấp để tạo ra một câu trả lời chi tiết và trung thực "
        "cho câu hỏi. Tránh thêm thông tin không xuất hiện trực tiếp hoặc không thể suy luận ra từ ngữ cảnh đã cho.\n"
        "3. **Thẻ Ngữ Cảnh Đa Bước (Multi-Hop Context Tags)**:\n"
        "   - Mỗi đoạn ngữ cảnh được gắn thẻ là `<1-hop>`, `<2-hop>`, v.v.\n"
        "   - Đảm bảo câu hỏi sử dụng thông tin từ ít nhất hai đoạn ngữ cảnh và kết nối chúng một cách có ý nghĩa.\n"
        "4. **Ngữ Cảnh Bổ Sung** (nếu có): Nếu `llm_context` được cung cấp, hãy sử dụng nó làm định hướng cho loại câu hỏi "
        "cần tạo (ví dụ: câu hỏi so sánh, câu hỏi nguyên nhân - kết quả, câu hỏi dạng ứng dụng) và cấu trúc câu trả lời "
        "sao cho phù hợp. Tuy nhiên, vẫn phải đảm bảo nội dung câu trả lời chỉ lấy từ ngữ cảnh được cung cấp."
    )
    input_model: t.Type[QueryConditions] = QueryConditions
    output_model: t.Type[GeneratedQueryAnswer] = GeneratedQueryAnswer
    examples: t.List[t.Tuple[QueryConditions, GeneratedQueryAnswer]] = [
        (
            QueryConditions(
                persona=Persona(
                    name="Nhà sử học",
                    role_description="Tập trung vào các cột mốc khoa học lớn và tác động toàn cầu của chúng.",
                ),
                themes=["Thuyết tương đối", "Xác thực bằng thực nghiệm"],
                query_style="Trang trọng",
                query_length="Vừa phải",
                context=[
                    "<1-hop> Albert Einstein đã phát triển thuyết tương đối, giới thiệu khái niệm về không-thời gian.",
                    "<2-hop> Hiện tượng ánh sáng bị bẻ cong bởi trọng lực đã được xác nhận trong cuộc nhật thực năm 1919, ủng hộ lý thuyết của Einstein.",
                ],
            ),
            GeneratedQueryAnswer(
                query="Việc xác thực bằng thực nghiệm đối với thuyết tương đối đã được thực hiện như thế nào trong cuộc nhật thực năm 1919?",
                answer=(
                    "Việc xác thực bằng thực nghiệm đối với thuyết tương đối đã được thực hiện trong cuộc nhật thực năm 1919 bằng cách "
                    "xác nhận hiện tượng ánh sáng bị bẻ cong bởi trọng lực, từ đó ủng hộ khái niệm không-thời gian của Einstein được đề xuất trong lý thuyết."
                ),
            ),
        ),
    ]