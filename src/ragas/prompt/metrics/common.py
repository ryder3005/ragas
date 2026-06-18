"""Common prompts shared across multiple metrics."""

import json
import typing as t


def statement_generator_prompt(question: str, answer: str) -> str:
    """
    V1-identical statement generator - matches PydanticPrompt.to_string() exactly.

    Args:
        question: The question being answered
        answer: The answer text to break down into statements

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format inputs exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_question = json.dumps(question)
    safe_answer = json.dumps(answer)

    return f"""Cho một câu hỏi và một câu trả lời, hãy phân tích độ phức tạp của từng câu trong câu trả lời. Hãy tách nhỏ từng câu thành một hoặc nhiều luận điểm (statements) độc lập và hoàn chỉnh để ai cũng có thể hiểu được một cách trực tiếp. Đảm bảo rằng KHÔNG sử dụng đại từ thay thế (như anh ấy, cô ấy, nó, họ,...) trong bất kỳ luận điểm nào. Định dạng kết quả đầu ra bằng JSON.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"statements": {{"description": "The generated statements", "items": {{"type": "string"}}, "title": "Statements", "type": "array"}}}}, "required": ["statements"], "title": "StatementGeneratorOutput", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "question": "Albert Einstein là ai và ông nổi tiếng nhất về điều gì?",
    "answer": "Ông là một nhà vật lý lý thuyết sinh ra ở Đức, được công nhận rộng rãi là một trong những nhà vật lý vĩ đại và có ảnh hưởng nhất mọi thời đại. Ông nổi tiếng nhất với việc phát triển thuyết tương đối, ngoài ra ông cũng có những đóng góp quan chất cho sự phát triển của lý thuyết cơ học lượng tử."
}}
Output: {{
    "statements": [
        "Albert Einstein là một nhà vật lý lý thuyết sinh ra ở Đức.",
        "Albert Einstein được công nhận là một trong những nhà vật lý vĩ đại và có ảnh hưởng nhất mọi thời đại.",
        "Albert Einstein nổi tiếng nhất với việc phát triển thuyết tương đối.",
        "Albert Einstein đã có những đóng góp quan trọng cho sự phát triển của lý thuyết cơ học lượng tử."
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "question": {safe_question},
    "answer": {safe_answer}
}}
Output: """


def nli_statement_prompt(context: str, statements: t.List[str]) -> str:
    """
    V1-identical NLI statement evaluation - matches PydanticPrompt.to_string() exactly.

    Args:
        context: The context to evaluate statements against
        statements: The statements to judge for faithfulness

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format inputs exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_context = json.dumps(context)
    safe_statements = json.dumps(statements, indent=4).replace("\n", "\n    ")

    return f"""Nhiệm vụ của bạn là đánh giá tính trung thực (faithfulness) của một chuỗi các luận điểm dựa trên một ngữ cảnh (context) cho trước. Đối với mỗi luận điểm, bạn phải trả về phán quyết (verdict) là 1 nếu luận điểm đó có thể được suy ra trực tiếp từ ngữ cảnh, hoặc 0 nếu luận điểm đó không thể suy ra trực tiếp từ ngữ cảnh.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"$defs": {{"StatementFaithfulnessAnswer": {{"properties": {{"statement": {{"description": "the original statement, word-by-word", "title": "Statement", "type": "string"}}, "reason": {{"description": "the reason of the verdict", "title": "Reason", "type": "string"}}, "verdict": {{"description": "the verdict(0/1) of the faithfulness.", "title": "Verdict", "type": "integer"}}}}, "required": ["statement", "reason", "verdict"], "title": "StatementFaithfulnessAnswer", "type": "object"}}}}, "properties": {{"statements": {{"items": {{"$ref": "#/$defs/StatementFaithfulnessAnswer"}}, "title": "Statements", "type": "array"}}}}, "required": ["statements"], "title": "NLIStatementOutput", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "context": "John là sinh viên trường Đại học XYZ. Anh ấy đang theo học ngành Khoa học Máy tính. Học kỳ này anh ấy đăng ký một số môn học, bao gồm Cấu trúc dữ liệu, Giải thuật và Quản trị Cơ sở Dữ liệu. John là một sinh viên siêng năng, anh dành phần lớn thời gian để học và hoàn thành bài tập. Anh cũng thường xuyên ở lại thư viện muộn để làm các dự án của mình.",
    "statements": [
        "John đang học chuyên ngành Sinh học.",
        "John đang học một khóa học về Trí tuệ Nhân tạo.",
        "John là một sinh viên tận tụy.",
        "John có một công việc bán thời gian."
    ]
}}
Output: {{
    "statements": [
        {{
            "statement": "John đang học chuyên ngành Sinh học.",
            "reason": "Chuyên ngành của John được nêu rõ ràng trong ngữ cảnh là Khoa học Máy tính, không phải Sinh học.",
            "verdict": 0
        }},
        {{
            "statement": "John đang học một khóa học về Trí tuệ Nhân tạo.",
            "reason": "Ngữ cảnh chỉ đề cập đến các môn Cấu trúc dữ liệu, Giải thuật và Quản trị Cơ sở Dữ liệu, hoàn toàn không nhắc tới môn Trí tuệ Nhân tạo.",
            "verdict": 0
        }},
        {{
            "statement": "John là một sinh viên tận tụy.",
            "reason": "Ngữ cảnh khẳng định John là một sinh viên siêng năng, người dành một lượng lớn thời gian để học tập và hoàn thành các bài tập.",
            "verdict": 1
        }},
        {{
            "statement": "John có một công việc bán thời gian.",
            "reason": "Không có thông tin nào trong ngữ cảnh cho biết John có công việc bán thời gian.",
            "verdict": 0
        }}
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "context": {safe_context},
    "statements": {safe_statements}
}}
Output: """