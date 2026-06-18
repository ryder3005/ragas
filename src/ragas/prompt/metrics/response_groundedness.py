"""Response groundedness prompts - V1-identical converted to functions."""


def response_groundedness_judge1_prompt(response: str, context: str) -> str:
    """
    V1-identical response groundedness judge 1 prompt - matches template_groundedness1 exactly.

    Args:
        response: The response/assertion to evaluate for groundedness
        context: The context to evaluate the response against

    Returns:
        V1-identical prompt string for the LLM
    """
    return f"""### Chỉ dẫn

Bạn là một chuyên gia đẳng cấp thế giới được thiết kế để đánh giá độ xác thực (groundedness) của một khẳng định.
Bạn sẽ được cung cấp một khẳng định (assertion) và một ngữ cảnh (context).
Nhiệm vụ của bạn là xác định xem khẳng định đó có được hỗ trợ/chứng thực bởi ngữ cảnh hay không.
Tuân thủ các chỉ dẫn dưới đây:
A. Nếu không có ngữ cảnh hoặc không có khẳng định, hoặc ngữ cảnh rỗng hoặc khẳng định rỗng, hãy trả về 0.
B. Nếu khẳng định không được hỗ trợ bởi ngữ cảnh, hãy trả về 0.
C. Nếu khẳng định được hỗ trợ một phần bởi ngữ cảnh, hãy trả về 1.
D. Nếu khẳng định được hỗ trợ hoàn toàn bởi ngữ cảnh, hãy trả về 2.
Bạn bắt buộc phải đưa ra điểm số đánh giá là 0, 1 hoặc 2, không thêm gì khác.

### Context:
<{context}>

### Assertion:
<{response}>

Phân tích Ngữ cảnh và Phản hồi, điểm số Độ xác thực (Groundedness score) là """


def response_groundedness_judge2_prompt(response: str, context: str) -> str:
    """
    V1-identical response groundedness judge 2 prompt - matches template_groundedness2 exactly.

    Args:
        response: The response/assertion to evaluate for groundedness
        context: The context to evaluate the response against

    Returns:
        V1-identical prompt string for the LLM
    """
    return f"""Với tư cách là một chuyên gia trong việc đánh giá mức độ liên kết giữa các tuyên bố và ngữ cảnh được cung cấp, tôi sẽ đánh giá mức độ mà một khẳng định nhận được sự hỗ trợ từ ngữ cảnh cho trước. Hãy tuân theo các nguyên tắc sau:

* Nếu khẳng định không được hỗ trợ, hoặc ngữ cảnh rỗng, hoặc khẳng định rỗng, hãy chấm điểm 0.
* Nếu khẳng định được hỗ trợ một phần, hãy chấm điểm 1.
* Nếu khẳng định được hỗ trợ hoàn toàn, hãy chấm điểm 2.

Tôi sẽ chỉ cung cấp điểm số đánh giá là 0, 1 hoặc 2, không có thêm bất kỳ thông tin nào khác.

---
**Context:**
[{context}]

**Assertion:**
[{response}]

Tuyệt đối không giải thích. Dựa trên ngữ cảnh và phản hồi được cung cấp, điểm số Độ xác thực (Groundedness score) là:"""