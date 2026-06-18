"""Summary Score prompts - V1-identical using exact PydanticPrompt.to_string() output."""

import json
import typing as t


def extract_keyphrases_prompt(text: str) -> str:
    """
    V1-identical keyphrase extraction - matches PydanticPrompt.to_string() exactly.

    Args:
        text: The text to extract keyphrases from

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format input exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_text = json.dumps(text)

    return f"""Trích xuất các cụm từ khóa (keyphrases) thuộc các loại sau: Con người (Person), Tổ chức (Organization), Địa điểm (Location), Ngày/Giờ (Date/Time), Giá trị tiền tệ (Monetary Values), và Tỷ lệ phần trăm (Percentages).
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"keyphrases": {{"items": {{"type": "string"}}, "title": "Keyphrases", "type": "array"}}}}, "required": ["keyphrases"], "title": "ExtractedKeyphrases", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "text": "Apple Inc. là một công ty công nghệ có trụ sở tại Cupertino, California. Được thành lập bởi Steve Jobs vào năm 1976, công ty đã đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la vào năm 2023."
}}
Output: {{
    "keyphrases": [
        "Apple Inc.",
        "Cupertino, California",
        "Steve Jobs",
        "năm 1976",
        "3 nghìn tỷ đô la",
        "năm 2023"
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "text": {safe_text}
}}
Output: """


def generate_questions_prompt(text: str, keyphrases: t.List[str]) -> str:
    """
    V1-identical question generation - matches PydanticPrompt.to_string() exactly.

    Args:
        text: The text to generate questions about
        keyphrases: The keyphrases extracted from the text

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format inputs exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_text = json.dumps(text)
    safe_keyphrases = json.dumps(keyphrases, indent=4, ensure_ascii=False).replace("\n", "\n    ")

    return f"""Dựa trên văn bản và các cụm từ khóa (keyphrases) được cung cấp, hãy tạo ra các câu hỏi đóng (closed-ended questions) mà kết quả có thể trả lời bằng '1' nếu câu hỏi đó có thể được trả lời bằng cách sử dụng văn bản, hoặc '0' nếu không thể. Các câu hỏi được tạo ra phải LUÔN LUÔN có kết quả là '1' dựa trên văn bản đã cho.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"questions": {{"items": {{"type": "string"}}, "title": "Questions", "type": "array"}}}}, "required": ["questions"], "title": "QuestionsGenerated", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "text": "Apple Inc. là một công ty công nghệ có trụ sở tại Cupertino, California. Được thành lập bởi Steve Jobs vào năm 1976, công ty đã đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la vào năm 2023.",
    "keyphrases": [
        "Apple Inc.",
        "Cupertino, California",
        "Steve Jobs",
        "năm 1976",
        "3 nghìn tỷ đô la",
        "năm 2023"
    ]
}}
Output: {{
    "questions": [
        "Apple Inc. có phải là một công ty công nghệ không?",
        "Apple Inc. có trụ sở tại Cupertino, California không?",
        "Apple Inc. có phải được thành lập bởi Steve Jobs không?",
        "Apple Inc. có phải được thành lập vào năm 1976 không?",
        "Apple Inc. có đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la không?",
        "Apple Inc. có đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la vào năm 2023 không?"
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "text": {safe_text},
    "keyphrases": {safe_keyphrases}
}}
Output: """


def generate_answers_prompt(summary: str, questions: t.List[str]) -> str:
    """
    V1-identical answer generation - matches PydanticPrompt.to_string() exactly.

    Args:
        summary: The summary to evaluate
        questions: The questions to check against the summary

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format inputs exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_summary = json.dumps(summary)
    safe_questions = json.dumps(questions, indent=4, ensure_ascii=False).replace("\n", "\n    ")

    return f"""Dựa trên danh sách các câu hỏi đóng có câu trả lời '1' hoặc '0', hãy tạo một chuỗi JSON với khóa 'answers' là một danh sách các chuỗi (strings) để xác định xem bản tóm tắt (summary) được cung cấp có chứa đủ thông tin để trả lời cho MỖI câu hỏi hay không. Câu trả lời BẮT BUỘC phải là '1' hoặc '0'. Trả về '0' nếu bản tóm tắt được cung cấp không chứa đủ thông tin để trả lời câu hỏi và trả về '1' nếu bản tóm tắt được cung cấp có thể trả lời được câu hỏi.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"answers": {{"items": {{"type": "string"}}, "title": "Answers", "type": "array"}}}}, "required": ["answers"], "title": "AnswersGenerated", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "summary": "Apple Inc. là một công ty công nghệ có trụ sở tại Cupertino, California. Được thành lập bởi Steve Jobs vào năm 1976, công ty đã đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la vào năm 2023.",
    "questions": [
        "Apple Inc. có phải là một công ty công nghệ không?",
        "Apple Inc. có trụ sở tại Cupertino, California không?",
        "Apple Inc. có phải được thành lập bởi Steve Jobs không?",
        "Apple Inc. có phải được thành lập vào năm 1976 không?",
        "Apple Inc. có đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la không?",
        "Apple Inc. có đạt giá trị vốn hóa thị trường là 3 nghìn tỷ đô la vào năm 2023 không?",
        "Apple Inc. có phải là một công ty phần mềm lớn không?",
        "Apple Inc. có nổi tiếng với iPhone không?",
        "Steve Jobs có phải là người đồng sáng lập Apple Inc. không?"
    ]
}}
Output: {{
    "answers": [
        "1",
        "1",
        "1",
        "1",
        "1",
        "1",
        "0",
        "0",
        "1"
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "summary": {safe_summary},
    "questions": {safe_questions}
}}
Output: """