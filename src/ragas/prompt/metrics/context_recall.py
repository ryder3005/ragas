"""Context Recall prompt for classifying statement attributions."""

import json


def context_recall_prompt(question: str, context: str, answer: str) -> str:
    """
    Generate the prompt for context recall evaluation.

    Args:
        question: The original question
        context: The retrieved context to evaluate against
        answer: The reference answer containing statements to classify

    Returns:
        Formatted prompt string for the LLM
    """
    # Use json.dumps() to safely escape the strings
    safe_question = json.dumps(question)
    safe_context = json.dumps(context)
    safe_answer = json.dumps(answer)

    return f"""Dựa trên một ngữ cảnh (context) và một câu trả lời (answer) cho trước, hãy phân tích từng câu trong câu trả lời và phân loại xem câu đó có bắt nguồn hoặc được chứng thực bởi ngữ cảnh đã cho hay không. Sử dụng phân loại nhị phân bằng cách chỉ dùng 'Có' (1) hoặc 'Không' (0). Trả về kết quả đầu ra dạng JSON kèm theo lý do (reason).

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "question": "Bạn có thể cho tôi biết gì về Albert Einstein?",
    "context": "Albert Einstein (14 tháng 3 năm 1879 - 18 tháng 4 năm 1955) là một nhà vật lý lý thuyết sinh ra ở Đức, được công nhận rộng rãi là một trong những nhà khoa học vĩ đại và có ảnh hưởng nhất mọi thời đại. Nổi tiếng nhất với việc phát triển thuyết tương đối, ông cũng có những đóng góp quan trọng cho cơ học lượng tử, và do đó là một nhân vật trung tâm trong việc định hình lại mang tính cách mạng về sự hiểu biết khoa học đối với tự nhiên mà vật lý hiện đại đã đạt được trong những thập kỷ đầu của thế kỷ hai mươi. Công thức tương đương khối lượng-năng lượng E = mc2 của ông, bắt nguồn từ thuyết tương đối, đã được gọi là 'phương trình nổi tiếng nhất thế giới'. Ông đã nhận giải Nobel Vật lý năm 1921 'vì những cống hiến của ông cho vật lý lý thuyết, và đặc biệt là vì sự khám phá ra định luật hiệu ứng quang điện', một bước đi then chốt trong sự phát triển của lý thuyết lượng tử. Công trình của ông cũng được biết đến với tầm ảnh hưởng đối với triết học khoa học. Trong một cuộc khảo sát năm 1999 đối với 130 nhà vật lý hàng đầu thế giới của tạp chí Physics World thuộc Anh, Einstein được xếp hạng là nhà vật lý vĩ đại nhất mọi thời đại. Những thành tựu trí tuệ và sự độc đáo của ông đã khiến Einstein trở nên đồng nghĩa với từ thiên tài.",
    "answer": "Albert Einstein, sinh ngày 14 tháng 3 năm 1879, là một nhà vật lý lý thuyết sinh ra ở Đức, được công nhận rộng rãi là một trong những nhà khoa học vĩ đại và có ảnh hưởng nhất mọi thời đại. Ông nhận giải Nobel Vật lý năm 1921 cho những cống hiến của mình đối với vật lý lý thuyết. Ông đã xuất bản 4 bài báo vào năm 1905. Einstein chuyển đến Thụy Sĩ vào năm 1895."
}}
Output: {{
    "classifications": [
        {{
            "statement": "Albert Einstein, sinh ngày 14 tháng 3 năm 1879, là một nhà vật lý lý thuyết sinh ra ở Đức, được công nhận rộng rãi là một trong những nhà khoa học vĩ đại và có ảnh hưởng nhất mọi thời đại.",
            "reason": "Ngày sinh của Einstein được đề cập rất rõ ràng và chính xác trong ngữ cảnh.",
            "attributed": 1
        }},
        {{
            "statement": "Ông nhận giải Nobel Vật lý năm 1921 cho những cống hiến của mình đối với vật lý lý thuyết.",
            "reason": "Câu này xuất hiện chính xác và đồng nhất với nội dung trong ngữ cảnh được cung cấp.",
            "attributed": 1
        }},
        {{
            "statement": "Ông đã xuất bản 4 bài báo vào năm 1905.",
            "reason": "Hoàn toàn không có thông tin nào nhắc về các bài báo ông đã viết trong ngữ cảnh đã cho.",
            "attributed": 0
        }},
        {{
            "statement": "Einstein chuyển đến Thụy Sĩ vào năm 1895.",
            "reason": "Không có bất kỳ bằng chứng hỗ trợ nào cho thông tin này trong ngữ cảnh được cung cấp.",
            "attributed": 0
        }}
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
Input: {{
    "question": {safe_question},
    "context": {safe_context},
    "answer": {safe_answer}
}}
Output: """