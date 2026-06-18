"""Noise Sensitivity prompts - V1-identical using exact PydanticPrompt.to_string() output."""

import json
import typing as t


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
            "reason": "Chuyên ngành của John được nêu rõ ràng trong ngữ cảnh là Khoa học Máy tính. Không có thông tin nào cho thấy anh ấy đang học chuyên ngành Sinh học.",
            "verdict": 0
        }},
        {{
            "statement": "John đang học một khóa học về Trí tuệ Nhân tạo.",
            "reason": "Ngữ cảnh đề cập đến các môn học John hiện đang học, và môn Trí tuệ Nhân tạo không có tên trong đó. Do đó, không thể suy luận rằng John đang học một khóa học về AI.",
            "verdict": 0
        }},
        {{
            "statement": "John là một sinh viên tận tụy.",
            "reason": "Ngữ cảnh khẳng định anh ấy dành phần lớn thời gian để học và hoàn thành bài tập. Thêm vào đó, việc anh ấy thường xuyên ở lại thư viện muộn để làm các dự án cũng biểu thị sự tận tụy.",
            "verdict": 1
        }},
        {{
            "statement": "John có một công việc bán thời gian.",
            "reason": "Không có bất kỳ thông tin nào được đưa ra trong ngữ cảnh về việc John có một công việc bán thời gian.",
            "verdict": 0
        }}
    ]
}}

Ví dụ 2
Input: {{
    "context": "Quang hợp là một quá trình được sử dụng bởi thực vật, tảo và một số vi khuẩn để chuyển đổi năng lượng ánh sáng thành năng lượng hóa học.",
    "statements": [
        "Albert Einstein là một thiên tài."
    ]
}}
Output: {{
    "statements": [
        {{
            "statement": "Albert Einstein là một thiên tài.",
            "reason": "Ngữ cảnh và luận điểm hoàn toàn không liên quan đến nhau.",
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