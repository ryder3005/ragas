"""Answer Relevance prompt for generating questions and detecting noncommittal responses."""

import json


def answer_relevancy_prompt(response: str) -> str:
    """
    Generate the prompt for answer relevance evaluation.

    Args:
        response: The response text to evaluate

    Returns:
        Formatted prompt string for the LLM
    """
    # Use json.dumps() to safely escape the response string
    safe_response = json.dumps(response)

    return f"""Hãy tạo một câu hỏi phù hợp cho câu trả lời được cung cấp và Xác định xem câu trả lời đó có phải là dạng 'không cam kết' (noncommittal) hay không. Gán giá trị 'noncommittal' là 1 nếu câu trả lời thuộc dạng không cam kết, và 0 nếu câu trả lời có tính cam kết (rõ ràng). Một câu trả lời không cam kết là câu trả lời mang tính lảng tránh, mơ hồ hoặc không rõ ràng. Ví dụ, các câu như "Tôi không biết" hoặc "Tôi không chắc chắn" là những câu trả lời không cam kết.

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "response": "Albert Einstein sinh ra tại Đức."
}}
Output: {{
    "question": "Albert Einstein sinh ra ở đâu?",
    "noncommittal": 0
}}

Ví dụ 2
Input: {{
    "response": "Tôi không biết về tính năng đột phá của chiếc điện thoại thông minh được phát minh vào năm 2023 vì tôi không có thông tin sau năm 2022."
}}
Output: {{
    "question": "Tính năng đột phá của chiếc điện thoại thông minh được phát minh vào năm 2023 là gì?",
    "noncommittal": 1
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "response": {safe_response}
}}
Output: """