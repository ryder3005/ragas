"""Context Entity Recall prompts - V1-identical using exact PydanticPrompt.to_string() output."""

import json


def extract_entities_prompt(text: str) -> str:
    """
    V1-identical entity extraction prompt using exact PydanticPrompt.to_string() output.
    Args:
        text: The text to extract entities from
    Returns:
        V1-identical prompt string for the LLM
    """

    safe_text = json.dumps(text)

    return f"""Cho một đoạn văn bản, hãy trích xuất các thực thể duy nhất (unique entities) mà không trùng lặp. Đảm bảo rằng bạn coi các dạng thức khác nhau hoặc các cách nhắc đến khác nhau của cùng một thực thể là một thực thể duy nhất.
Vui lòng trả về kết quả dưới dạng định dạng JSON tuân thủ chính xác theo cấu trúc (schema) được chỉ định trong JSON Schema sau:
{{"properties": {{"entities": {{"items": {{"type": "string"}}, "title": "Entities", "type": "array"}}}}, "required": ["entities"], "title": "EntitiesList", "type": "object"}}Không sử dụng dấu nháy đơn trong phản hồi của bạn, thay vào đó hãy sử dụng dấu nháy kép và được escape đúng cách bằng dấu gạch chéo ngược (\\").
--------VÍ DỤ-----------
Ví dụ 1
Input: {{
    "text": "Tháp Eiffel, tọa lạc tại Paris, Pháp, là một trong những địa danh mang tính biểu tượng nhất trên toàn cầu. Hàng triệu du khách bị thu hút đến đây mỗi năm vì tầm nhìn ngoạn mục ra thành phố. Hoàn thành vào năm 1889, công trình được xây dựng kịp thời cho Hội chợ Thế giới năm 1889."
}}
Output: {{
    "entities": [
        "Tháp Eiffel",
        "Paris",
        "Pháp",
        "1889",
        "Hội chợ Thế giới"
    ]
}}
Ví dụ 2
Input: {{
    "text": "Đấu trường La Mã ở Rome, còn được gọi là Nhà hát lớn Flavian, là một đài tượng niệm cho thành tựu kỹ thuật và kiến trúc của La Mã. Việc xây dựng bắt đầu dưới thời Hoàng đế Vespasian vào năm 70 sau Công nguyên và được hoàn thành bởi con trai ông là Titus vào năm 80 sau Công nguyên. Nơi đây có thể chứa từ 50.000 đến 80.000 khán giả đến xem các trận đấu sĩ và các buổi trình diễn công cộng."
}}
Output: {{
    "entities": [
        "Đấu trường La Mã",
        "Rome",
        "Nhà hát lớn Flavian",
        "Vespasian",
        "năm 70 sau Công nguyên",
        "Titus",
        "năm 80 sau Công nguyên"
    ]
}}
Ví dụ 3
Input: {{
    "text": "Vạn Lý Trường Thành của Trung Quốc, trải dài hơn 21.196 km từ đông sang tây, là một kỳ quan của kiến trúc phòng thủ cổ đại. Được xây dựng để bảo vệ chống lại các cuộc xâm lược từ phương bắc, việc xây dựng công trình đã bắt đầu từ thế kỷ thứ 7 trước Công nguyên. Ngày nay, nơi đây là Di sản Thế giới được UNESCO công nhận và là một điểm thu hút khách du lịch lớn."
}}
Output: {{
    "entities": [
        "Vạn Lý Trường Thành",
        "21.196 km",
        "thế kỷ thứ 7 trước Công nguyên",
        "Di sản Thế giới được UNESCO công nhận"
    ]
}}
Ví dụ 4
Input: {{
    "text": "Sứ mệnh Apollo 11, được phóng vào ngày 16 tháng 7 năm 1969, đã đánh dấu lần đầu tiên con người đặt chân lên Mặt Trăng. Các phi hành gia Neil Armstrong, Buzz Aldrin và Michael Collins đã làm nên lịch sử, trong đó Armstrong là người đầu tiên bước đi trên bề mặt mặt trăng. Sự kiện này là một cột mốc quan trọng trong quá trình khám phá không gian."
}}
Output: {{
    "entities": [
        "Sứ mệnh Apollo 11",
        "ngày 16 tháng 7 năm 1969",
        "Mặt Trăng",
        "Neil Armstrong",
        "Buzz Aldrin",
        "Michael Collins"
    ]
}}
-----------------------------
Bây giờ hãy thực hiện công việc tương tự với đầu vào sau đây
input: {{
    "text": {safe_text}
}}
Output: """