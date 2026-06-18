"""Answer Accuracy prompts - Convert NVIDIA dual-judge templates to function format."""

import json


def answer_accuracy_judge1_prompt(
    query: str, user_answer: str, reference_answer: str
) -> str:
    """
    First judge template for answer accuracy evaluation.

    Uses JSON structured output for reliable parsing.

    Args:
        query: The original question
        user_answer: The response to evaluate
        reference_answer: The ground truth reference

    Returns:
        Prompt string for structured JSON rating (0, 2, or 4)
    """
    safe_query = json.dumps(query)
    safe_user_answer = json.dumps(user_answer)
    safe_reference_answer = json.dumps(reference_answer)

    return f"""Chỉ dẫn: Bạn là một trợ lý đẳng cấp thế giới chuyên đánh giá Câu trả lời của Người dùng dựa trên một Câu hỏi cho trước. Câu hỏi này đã được trả lời hoàn chỉnh và chính xác trong Câu trả lời Tham chiếu.
Hãy cho 4 điểm, nếu Câu trả lời của Người dùng bao hàm toàn bộ và tương đương hoàn toàn với Câu trả lời Tham chiếu xét trên mọi khía cạnh, chủ đề, con số, chỉ số, ngày tháng và đơn vị.
Hãy cho 2 điểm, nếu Câu trả lời của Người dùng chỉ bao hàm một phần và gần như tương đương với Câu trả lời Tham chiếu xét trên mọi khía cạnh, chủ đề, con số, chỉ số, ngày tháng và đơn vị.
Hãy cho 0 điểm, nếu Câu trả lời của Người dùng không nằm trong Câu trả lời Tham chiếu, hoặc không chính xác xét trên mọi khía cạnh, chủ đề, con số, chỉ số, ngày tháng và đơn vị, hoặc Câu trả lời của Người dùng không trả lời đúng trọng tâm câu hỏi.
Tuyệt đối không giải thích hoặc biện minh cho mức điểm của bạn. Điểm số của bạn bắt buộc phải là 4, 2 hoặc 0 theo đúng chỉ dẫn ở trên.
Trả về phản hồi của bạn dưới dạng JSON theo định dạng sau: {{"rating": X}} với X là 0, 2, hoặc 4.

### Câu hỏi: {safe_query}
### Câu trả lời của Người dùng: {safe_user_answer}
### Câu trả lời Tham chiếu: {safe_reference_answer}
Điểm số là:"""


def answer_accuracy_judge2_prompt(
    query: str, user_answer: str, reference_answer: str
) -> str:
    """
    Second judge template for answer accuracy evaluation.

    Uses JSON structured output for reliable parsing.

    Args:
        query: The original question
        user_answer: The response to evaluate
        reference_answer: The ground truth reference

    Returns:
        Prompt string for structured JSON rating (0, 2, or 4)
    """
    safe_query = json.dumps(query)
    safe_user_answer = json.dumps(user_answer)
    safe_reference_answer = json.dumps(reference_answer)

    return f"""Tôi sẽ đánh giá Câu trả lời của Người dùng so với Câu trả lời Tham chiếu cho một Câu hỏi cụ thể.
Mức điểm 4 biểu thị rằng Câu trả lời của Người dùng hoàn toàn nhất quán với Câu trả lời Tham chiếu, bao quát toàn bộ các khía cạnh, chủ đề, con số, chỉ số, ngày tháng và đơn vị.
Mức điểm 2 biểu thị rằng Câu trả lời của Người dùng phần lớn khớp với Câu trả lời Tham chiếu, chỉ có một vài sai sót nhỏ ở một số khía cạnh.
Mức điểm 0 có nghĩa là Câu trả lời của Người dùng không chính xác, không đầy đủ, không liên quan đến Câu trả lời Tham chiếu hoặc không giải quyết được Câu hỏi.
Tôi sẽ đưa ra điểm số mà không kèm theo bất kỳ lời giải thích hay biện minh nào, tuân thủ nghiêm ngặt thang đo sau: 0 (không khớp), 2 (khớp một phần), 4 (khớp hoàn toàn).
Không giải thích hoặc biện minh cho điểm số của tôi. Điểm số của tôi bắt buộc chỉ được là 4, 2 hoặc 0.
Trả về phản hồi của bạn dưới dạng JSON theo định dạng sau: {{"rating": X}} với X là 0, 2, hoặc 4.

Câu hỏi: {safe_query}

Câu trả lời Tham chiếu: {safe_reference_answer}

Câu trả lời của Người dùng: {safe_user_answer}

Điểm số: """