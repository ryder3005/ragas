"""Answer Correctness prompts for classification.

Note: statement_generator_prompt has been moved to ragas.prompt.metrics.common
"""

import json
import typing as t


def correctness_classifier_prompt(
    question: str, answer_statements: t.List[str], ground_truth_statements: t.List[str]
) -> str:
    """
    V1-identical correctness classifier - matches PydanticPrompt.to_string() exactly.

    Args:
        question: The original question
        answer_statements: List of statements from the answer to evaluate
        ground_truth_statements: List of ground truth reference statements

    Returns:
        V1-identical prompt string for the LLM
    """
    # Format inputs exactly like V1's model_dump_json(indent=4, exclude_none=True)
    safe_question = json.dumps(question)
    safe_answer_statements = json.dumps(answer_statements, indent=4).replace(
        "\n", "\n    "
    )
    safe_ground_truth = json.dumps(ground_truth_statements, indent=4).replace(
        "\n", "\n    "
    )

    return f"""Dựa trên các luận điểm của câu trả lời tham chiếu (ground truth) và câu trả lời của người dùng (answer), hãy phân tích từng luận điểm và phân loại chúng vào một trong các danh mục sau: 
TP (True Positive): các luận điểm xuất hiện trong câu trả lời của người dùng và đồng thời được hỗ trợ trực tiếp bởi một hoặc nhiều luận điểm trong câu trả lời tham chiếu.
FP (False Positive): các luận điểm xuất hiện trong câu trả lời của người dùng nhưng không được hỗ trợ trực tiếp bởi bất kỳ luận điểm nào trong câu trả lời tham chiếu.
FN (False Negative): các luận điểm có trong câu trả lời tham chiếu nhưng lại thiếu vắng trong câu trả lời của người dùng.
Mỗi luận điểm chỉ được thuộc về duy nhất một danh mục. Hãy cung cấp lý do (reason) cho mỗi lượt phân loại.

Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"$defs": {{"StatementsWithReason": {{"properties": {{"statement": {{"title": "Statement", "type": "string"}}, "reason": {{"title": "Reason", "type": "string"}}}}, "required": ["statement", "reason"], "title": "StatementsWithReason", "type": "object"}}}}, "properties": {{"TP": {{"items": {{"$ref": "#/$defs/StatementsWithReason"}}, "title": "Tp", "type": "array"}}, "FP": {{"items": {{"$ref": "#/$defs/StatementsWithReason"}}, "title": "Fp", "type": "array"}}, "FN": {{"items": {{"$ref": "#/$defs/StatementsWithReason"}}, "title": "Fn", "type": "array"}}}}, "required": ["TP", "FP", "FN"], "title": "ClassificationWithReason", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "question": "Năng lượng nào cung cấp cho mặt trời và chức năng chính của nó là gì?",
    "answer": [
        "Mặt trời được cung cấp năng lượng bởi phản ứng phân hạch hạt nhân, tương tự như các lò phản ứng hạt nhân trên Trái đất.",
        "Chức năng chính của mặt trời là cung cấp ánh sáng cho hệ mặt trời."
    ],
    "ground_truth": [
        "Mặt trời được cung cấp năng lượng bởi phản ứng hợp hạch hạt nhân, nơi các nguyên tử hydro hợp nhất để tạo thành helium.",
        "Quá trình hợp hạch này trong lõi mặt trời giải phóng một lượng năng lượng khổng lồ.",
        "Năng lượng từ mặt trời cung cấp nhiệt và ánh sáng, những yếu tố thiết yếu cho sự sống trên Trái đất.",
        "Ánh sáng của mặt trời đóng một vai trò quan trọng trong hệ thống khí hậu của Trái đất.",
        "Ánh sáng mặt trời giúp thúc đẩy thời tiết và các dòng hải lưu."
    ]
}}
Output: {{
    "TP": [
        {{
            "statement": "Chức năng chính của mặt trời là cung cấp ánh sáng cho hệ mặt trời.",
            "reason": "Luận điểm này phần nào được hỗ trợ bởi câu trả lời tham chiếu có đề cập đến việc mặt trời cung cấp ánh sáng và các vai trò của nó, mặc dù câu trả lời tham chiếu tập trung rộng hơn vào năng lượng của mặt trời."
        }}
    ],
    "FP": [
        {{
            "statement": "Mặt trời được cung cấp năng lượng bởi phản ứng phân hạch hạt nhân, tương tự như các lò phản ứng hạt nhân trên Trái đất.",
            "reason": "Luận điểm này sai và mâu thuẫn với câu trả lời tham chiếu, nơi khẳng định rằng mặt trời được cung cấp năng lượng bởi phản ứng hợp hạch hạt nhân."
        }}
    ],
    "FN": [
        {{
            "statement": "Mặt trời được cung cấp năng lượng bởi phản ứng hợp hạch hạt nhân, nơi các nguyên tử hydro hợp nhất để tạo thành helium.",
            "reason": "Mô tả chính xác này về nguồn năng lượng của mặt trời không được bao hàm trong câu trả lời của người dùng."
        }}
    ],
        {{
            "statement": "Quá trình hợp hạch này trong lõi mặt trời giải phóng một lượng năng lượng khổng lồ.",
            "reason": "Quá trình này và tầm quan trọng của nó không được nhắc đến trong câu trả lời của người dùng."
        }},
        {{
            "statement": "Năng lượng từ mặt trời cung cấp nhiệt và ánh sáng, những yếu tố thiết yếu cho sự sống trên Trái đất.",
            "reason": "Câu trả lời của người dùng chỉ đề cập đến ánh sáng, bỏ qua khía cạnh thiết yếu về nhiệt và sự cần thiết của nó đối với sự sống mà câu trả lời tham chiếu có bao quát."
        }},
        {{
            "statement": "Ánh sáng của mặt trời đóng một vai trò quan trọng trong hệ thống khí hậu của Trái đất.",
            "reason": "Tác động rộng lớn này của ánh sáng mặt trời đối với hệ thống khí hậu Trái đất không được giải quyết trong câu trả lời của người dùng."
        }},
        {{
            "statement": "Ánh sáng mặt trời giúp thúc đẩy thời tiết và các dòng hải lưu.",
            "reason": "Ảnh hưởng của ánh sáng mặt trời đối với các kiểu thời tiết và dòng hải lưu đã bị bỏ sót trong câu trả lời của người dùng."
        }}
    ]
}}

Ví dụ 2
Input: {{
    "question": "Nhiệt độ sôi của nước là bao nhiêu?",
    "answer": [
        "Nhiệt độ sôi của nước là 100 độ Celsius ở mực nước biển"
    ],
    "ground_truth": [
        "Nhiệt độ sôi của nước là 100 độ Celsius (212 độ Fahrenheit) ở mực nước biển.",
        "Nhiệt độ sôi của nước có thể thay đổi theo độ cao."
    ]
}}
Output: {{
    "TP": [
        {{
            "statement": "Nhiệt độ sôi của nước là 100 độ Celsius ở mực nước biển",
            "reason": "Luận điểm này được hỗ trợ trực tiếp bởi câu trả lời tham chiếu, trong đó xác định rõ nhiệt độ sôi của nước là 100 độ Celsius ở mực nước biển."
        }}
    ],
    "FP": [],
    "FN": [
        {{
            "statement": "Nhiệt độ sôi của nước có thể thay đổi theo độ cao.",
            "reason": "Thông tin bổ sung này về việc nhiệt độ sôi của nước có thể thay đổi tùy theo độ cao không được đề cập trong câu trả lời của người dùng."
        }}
    ]
}}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "question": {safe_question},
    "answer": {safe_answer_statements},
    "ground_truth": {safe_ground_truth}
}}
Output: """


__all__ = ["correctness_classifier_prompt"]