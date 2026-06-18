"""Factual correctness prompts - V1-identical converted to functions."""

import json


def claim_decomposition_prompt(
    response: str, atomicity: str = "low", coverage: str = "low"
) -> str:
    """
    V1-identical claim decomposition prompt with configurable atomicity/coverage.

    Args:
        response: The response text to break down into claims
        atomicity: Level of atomicity ("low" or "high")
        coverage: Level of coverage ("low" or "high")

    Returns:
        V1-identical prompt string for the LLM
    """
    safe_response = json.dumps(response)

    # Select examples based on atomicity and coverage configuration
    if atomicity == "low" and coverage == "low":
        examples = [
            {
                "input": {
                    "response": "Charles Babbage là một nhà toán học, nhà triết học và nhà phê bình ẩm thực người Pháp."
                },
                "output": {
                    "claims": ["Charles Babbage là một nhà toán học và nhà triết học."]
                },
            },
            {
                "input": {
                    "response": "Albert Einstein là một nhà vật lý lý thuyết người Đức. Ông đã phát triển thuyết tương đối và cũng đóng góp vào sự phát triển của cơ học lượng tử."
                },
                "output": {
                    "claims": [
                        "Albert Einstein là một nhà vật lý người Đức.",
                        "Albert Einstein đã phát triển thuyết tương đối và đóng góp vào cơ học lượng tử.",
                    ]
                },
            },
        ]
    elif atomicity == "low" and coverage == "high":
        examples = [
            {
                "input": {
                    "response": "Charles Babbage là một nhà toán học, nhà triết học và nhà phê bình ẩm thực người Pháp."
                },
                "output": {
                    "claims": [
                        "Charles Babbage là một nhà toán học, nhà triết học và nhà phê bình ẩm thực người Pháp."
                    ]
                },
            },
            {
                "input": {
                    "response": "Albert Einstein là một nhà vật lý lý thuyết người Đức. Ông đã phát triển thuyết tương đối và cũng đóng góp vào sự phát triển của cơ học lượng tử."
                },
                "output": {
                    "claims": [
                        "Albert Einstein là một nhà vật lý lý thuyết người Đức.",
                        "Albert Einstein đã phát triển thuyết tương đối và cũng đóng góp vào sự phát triển của cơ học lượng tử.",
                    ]
                },
            },
        ]
    elif atomicity == "high" and coverage == "low":
        examples = [
            {
                "input": {
                    "response": "Charles Babbage là một nhà toán học, nhà triết học và nhà phê bình ẩm thực người Pháp."
                },
                "output": {
                    "claims": [
                        "Charles Babbage là một nhà toán học.",
                        "Charles Babbage là một nhà triết học.",
                    ]
                },
            },
            {
                "input": {
                    "response": "Albert Einstein là một nhà vật lý lý thuyết người Đức. Ông đã phát triển thuyết tương đối và cũng đóng góp vào sự phát triển của cơ học lượng tử."
                },
                "output": {
                    "claims": [
                        "Albert Einstein là một nhà vật lý lý thuyết người Đức.",
                        "Albert Einstein đã phát triển thuyết tương đối.",
                    ]
                },
            },
        ]
    else:  # high atomicity, high coverage
        examples = [
            {
                "input": {
                    "response": "Charles Babbage là một nhà toán học, nhà triết học và nhà phê bình ẩm thực người Pháp."
                },
                "output": {
                    "claims": [
                        "Charles Babbage là một nhà toán học.",
                        "Charles Babbage là một nhà triết học.",
                        "Charles Babbage là một nhà phê bình ẩm thực.",
                        "Charles Babbage là người Pháp.",
                    ]
                },
            },
            {
                "input": {
                    "response": "Albert Einstein là một nhà vật lý lý thuyết người Đức. Ông đã phát triển thuyết tương đối và cũng đóng góp vào sự phát triển của cơ học lượng tử."
                },
                "output": {
                    "claims": [
                        "Albert Einstein là một nhà vật lý lý thuyết người Đức.",
                        "Albert Einstein đã phát triển thuyết tương đối.",
                        "Albert Einstein đã đóng góp vào sự phát triển của cơ học lượng tử.",
                    ]
                },
            },
        ]

    # Build examples string
    examples_str = "\n".join(
        [
            f"""Ví dụ {i + 1}
Input: {json.dumps(ex["input"], indent=4, ensure_ascii=False)}
Output: {json.dumps(ex["output"], indent=4, ensure_ascii=False)}"""
            for i, ex in enumerate(examples)
        ]
    )

    return f"""Hãy phân tích và tách nhỏ từng câu đầu vào thành một hoặc nhiều tuyên bố (claims) độc lập. Mỗi tuyên bố phải là một khẳng định độc lập có thể được kiểm chứng thực tế một cách riêng biệt.
Hãy tuân thủ mức độ chia nhỏ (atomicity) và mức độ bao phủ dữ liệu (coverage) giống như các ví dụ mẫu được hiển thị dưới đây.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"claims": {{"description": "Decomposed Claims", "items": {{"type": "string"}}, "title": "Claims", "type": "array"}}}}, "required": ["claims"], "title": "ClaimDecompositionOutput", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").

--------VÍ DỤ-----------
{examples_str}
-----------------------------

Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "response": {safe_response}
}}
Output: """