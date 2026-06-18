"""Context Relevance prompts - Convert NVIDIA dual-judge templates to function format."""

import json


def context_relevance_judge1_prompt(query: str, context: str) -> str:
    """
    First judge template for context relevance evaluation.

    Args:
        query: The user's question
        context: The retrieved context to evaluate

    Returns:
        Prompt string for rating (0, 1, or 2)
    """
    safe_query = json.dumps(query)
    safe_context = json.dumps(context)

    return f"""### Chỉ dẫn

Bạn là một chuyên gia đẳng cấp thế giới được thiết kế để đánh giá điểm số mức độ liên quan của Ngữ cảnh (Context) nhằm trả lời Câu hỏi (Question).
Nhiệm vụ của bạn là xác định xem Ngữ cảnh có chứa thông tin phù hợp để trả về câu trả lời cho Câu hỏi hay không.
Không dựa vào kiến thức có sẵn trước đây của bạn về Câu hỏi.
Chỉ sử dụng những gì được viết trong Ngữ cảnh và trong Câu hỏi.
Tuân thủ các chỉ dẫn dưới đây:
0. Nếu ngữ cảnh không chứa bất kỳ thông tin liên quan nào để trả lời câu hỏi, hãy trả về 0.
1. Nếu ngữ cảnh chứa một phần thông tin liên quan để trả lời câu hỏi, hãy trả về 1.
2. Nếu ngữ cảnh chứa thông tin hoàn toàn liên quan để trả lời câu hỏi, hãy trả về 2.
Bạn bắt buộc phải đưa ra điểm số mức độ liên quan là 0, 1 hoặc 2, không thêm gì khác.
Tuyệt đối không giải thích.
Trả về phản hồi của bạn dưới dạng JSON theo định dạng sau: {{"rating": X}} với X là 0, 1, hoặc 2.

### Câu hỏi: {safe_query}

### Ngữ cảnh: {safe_context}

Không cố gắng giải thích.
Phân tích Ngữ cảnh và Câu hỏi, điểm số Mức độ liên quan là """


def context_relevance_judge2_prompt(query: str, context: str) -> str:
    """
    Second judge template for context relevance evaluation.

    Args:
        query: The user's question
        context: The retrieved context to evaluate

    Returns:
        Prompt string for rating (0, 1, or 2)
    """
    safe_query = json.dumps(query)
    safe_context = json.dumps(context)

    return f"""Với tư cách là một chuyên gia được thiết kế đặc biệt để đánh giá điểm số mức độ liên quan của một Ngữ cảnh đối với một Câu hỏi cho trước, nhiệm vụ của tôi là xác định mức độ mà Ngữ cảnh cung cấp thông tin cần thiết để trả lời Câu hỏi. Tôi sẽ chỉ dựa vào thông tin được cung cấp trong Ngữ cảnh và Câu hỏi, chứ không dựa vào bất kỳ kiến thức nào có từ trước.

Dưới đây là các chỉ dẫn tôi sẽ tuân theo:
* Nếu Ngữ cảnh không chứa bất kỳ thông tin liên quan nào để trả lời Câu hỏi, tôi sẽ phản hồi với điểm số mức độ liên quan là 0.
* Nếu Ngữ cảnh chứa một phần thông tin liên quan để trả lời Câu hỏi, tôi sẽ phản hồi với điểm số mức độ liên quan là 1.
* Nếu Ngữ cảnh chứa thông tin hoàn toàn liên quan để trả lời Câu hỏi, tôi sẽ phản hồi với điểm số mức độ liên quan là 2.
Trả về phản hồi của bạn dưới dạng JSON theo định dạng sau: {{"rating": X}} với X là 0, 1, hoặc 2.

### Câu hỏi: {safe_query}

### Ngữ cảnh: {safe_context}

Không cố gắng giải thích.
Dựa trên Câu hỏi và Ngữ cảnh được cung cấp, điểm số Mức độ liên quan là ["""