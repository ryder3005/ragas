import typing as t
from dataclasses import dataclass

from pydantic import BaseModel

from ragas.prompt import PydanticPrompt, StringIO
from ragas.testset.graph import Node
from ragas.testset.transforms.base import LLMBasedExtractor


class TextWithExtractionLimit(BaseModel):
    text: str
    max_num: int = 10


class SummaryExtractorPrompt(PydanticPrompt[StringIO, StringIO]):
    instruction: str = "Tóm tắt đoạn văn bản đã cho trong ít hơn 10 câu."
    input_model: t.Type[StringIO] = StringIO
    output_model: t.Type[StringIO] = StringIO
    examples: t.List[t.Tuple[StringIO, StringIO]] = [
        (
            StringIO(
                text="Trí tuệ nhân tạo\n\nTrí tuệ nhân tạo đang biến đổi nhiều ngành công nghiệp khác nhau bằng cách tự động hóa các nhiệm vụ trước đây đòi hỏi trí thông minh của con người. Từ y tế đến tài chính, AI đang được sử dụng để phân tích lượng dữ liệu khổng lồ một cách nhanh chóng và chính xác. Công nghệ này cũng đang thúc đẩy những đổi mới trong các lĩnh vực như xe tự lái và đề xuất cá nhân hóa."
            ),
            StringIO(
                text="AI đang cách mạng hóa các ngành công nghiệp bằng cách tự động hóa công việc, phân tích dữ liệu và thúc đẩy các đổi mới như xe tự lái và hệ thống gợi ý cá nhân hóa."
            ),
        )
    ]


class Keyphrases(BaseModel):
    keyphrases: t.List[str]


class KeyphrasesExtractorPrompt(PydanticPrompt[TextWithExtractionLimit, Keyphrases]):
    instruction: str = "Trích xuất tối đa max_num cụm từ khóa quan trọng từ đoạn văn bản cho trước."
    input_model: t.Type[TextWithExtractionLimit] = TextWithExtractionLimit
    output_model: t.Type[Keyphrases] = Keyphrases
    examples: t.List[t.Tuple[TextWithExtractionLimit, Keyphrases]] = [
        (
            TextWithExtractionLimit(
                text="Trí tuệ nhân tạo\n\nTrí tuệ nhân tạo đang biến đổi nhiều ngành công nghiệp khác nhau bằng cách tự động hóa các nhiệm vụ trước đây đòi hỏi trí thông minh của con người. Từ y tế đến tài chính, AI đang được sử dụng để phân tích lượng dữ liệu khổng lồ một cách nhanh chóng và chính xác. Công nghệ này cũng đang thúc đẩy những đổi mới trong các lĩnh vực như xe tự lái và đề xuất cá nhân hóa.",
                max_num=5,
            ),
            Keyphrases(
                keyphrases=[
                    "Trí tuệ nhân tạo",
                    "tự động hóa công việc",
                    "y tế",
                    "xe tự lái",
                    "đề xuất cá nhân hóa",
                ]
            ),
        )
    ]


class TitleExtractorPrompt(PydanticPrompt[StringIO, StringIO]):
    instruction: str = "Trích xuất tiêu đề của tài liệu đã cho."
    input_model: t.Type[StringIO] = StringIO
    output_model: t.Type[StringIO] = StringIO
    examples: t.List[t.Tuple[StringIO, StringIO]] = [
        (
            StringIO(
                text="Học sâu trong xử lý ngôn ngữ tự nhiên\n\nTóm tắt\n\nHọc sâu đã cách mạng hóa lĩnh vực xử lý ngôn ngữ tự nhiên (NLP). Bài báo này khám phá các mô hình học sâu khác nhau và ứng dụng của chúng trong các tác vụ NLP như dịch thuật ngôn ngữ, phân tích cảm xúc và tạo văn bản. Chúng tôi thảo luận về các ưu điểm và hạn chế của các mô hình khác nhau, đồng thời cung cấp một cái nhìn tổng quan toàn diện về trạng thái phát triển hiện tại trong NLP."
            ),
            StringIO(text="Học sâu trong xử lý ngôn ngữ tự nhiên"),
        )
    ]


class Headlines(BaseModel):
    headlines: t.List[str]


class HeadlinesExtractorPrompt(PydanticPrompt[TextWithExtractionLimit, Headlines]):
    instruction: str = (
        "Trích xuất tối đa max_num tiêu đề quan trọng nhất từ văn bản đã cho để có thể sử dụng làm ranh giới chia nhỏ văn bản thành các phần độc lập. "
        "Tập trung vào các tiêu đề Cấp 2 (Level 2) và Cấp 3 (Level 3)."
    )

    input_model: t.Type[TextWithExtractionLimit] = TextWithExtractionLimit
    output_model: t.Type[Headlines] = Headlines
    examples: t.List[t.Tuple[TextWithExtractionLimit, Headlines]] = [
        (
            TextWithExtractionLimit(
                text="""\
                Giới thiệu
                Tổng quan về chủ đề...

                Các khái niệm chính
                Giải thích về các ý tưởng cốt lõi...

                Phân tích chi tiết
                Các kỹ thuật và phương pháp phân tích...

                Tiểu mục: Kỹ thuật chuyên sâu
                Chi tiết hơn về các kỹ thuật chuyên sâu...

                Hướng đi tương lai
                Góc nhìn về các xu hướng sắp tới...

                Tiểu mục: Các bước tiếp theo trong nghiên cứu
                Thảo luận về các lĩnh vực nghiên cứu mới...

                Kết luận
                Nhận xét cuối cùng và tóm tắt.
                """,
                max_num=6,
            ),
            Headlines(
                headlines=[
                    "Giới thiệu",
                    "Các khái niệm chính",
                    "Phân tích chi tiết",
                    "Tiểu mục: Kỹ thuật chuyên sâu",
                    "Hướng đi tương lai",
                    "Kết luận",
                ],
            ),
        ),
    ]


class NEROutput(BaseModel):
    entities: t.List[str]


class NERPrompt(PydanticPrompt[TextWithExtractionLimit, NEROutput]):
    instruction: str = (
        "Trích xuất các thực thể có tên (Named Entities) từ văn bản được cung cấp, giới hạn kết quả ở những thực thể quan trọng nhất. "
        "Đảm bảo số lượng thực thể không vượt quá mức tối đa được chỉ định."
    )
    input_model: t.Type[TextWithExtractionLimit] = TextWithExtractionLimit
    output_model: t.Type[NEROutput] = NEROutput
    examples: t.List[t.Tuple[TextWithExtractionLimit, NEROutput]] = [
        (
            TextWithExtractionLimit(
                text="""Elon Musk, CEO của Tesla và SpaceX, đã thông báo kế hoạch mở rộng hoạt động sang các địa điểm mới ở Châu Âu và Châu Á.
                Sự mở rộng này dự kiến sẽ tạo ra hàng ngàn việc làm, đặc biệt là ở các thành phố như Berlin và Thượng Hải.""",
                max_num=10,
            ),
            NEROutput(
                entities=[
                    "Elon Musk",
                    "Tesla",
                    "SpaceX",
                    "Châu Âu",
                    "Châu Á",
                    "Berlin",
                    "Thượng Hải",
                ]
            ),
        ),
    ]


@dataclass
class SummaryExtractor(LLMBasedExtractor):
    """
    Trích xuất tóm tắt từ văn bản cho trước.
    """

    property_name: str = "summary"
    prompt: SummaryExtractorPrompt = SummaryExtractorPrompt()

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, None
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        result = await self.prompt.generate(self.llm, data=StringIO(text=chunks[0]))
        return self.property_name, result.text


@dataclass
class KeyphrasesExtractor(LLMBasedExtractor):
    """
    Trích xuất các cụm từ khóa chính quan trọng từ văn bản cho trước.
    """

    property_name: str = "keyphrases"
    prompt: KeyphrasesExtractorPrompt = KeyphrasesExtractorPrompt()
    max_num: int = 5

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, None
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        keyphrases = []
        for chunk in chunks:
            result = await self.prompt.generate(
                self.llm, data=TextWithExtractionLimit(text=chunk, max_num=self.max_num)
            )
            keyphrases.extend(result.keyphrases)
        return self.property_name, keyphrases


@dataclass
class TitleExtractor(LLMBasedExtractor):
    """
    Trích xuất tiêu đề từ văn bản cho trước.
    """

    property_name: str = "title"
    prompt: TitleExtractorPrompt = TitleExtractorPrompt()

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, None
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        result = await self.prompt.generate(self.llm, data=StringIO(text=chunks[0]))
        return self.property_name, result.text


@dataclass
class HeadlinesExtractor(LLMBasedExtractor):
    """
    Trích xuất các tiêu đề từ văn bản cho trước.
    """

    property_name: str = "headlines"
    prompt: HeadlinesExtractorPrompt = HeadlinesExtractorPrompt()
    max_num: int = 5

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, None
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        headlines = []
        for chunk in chunks:
            result = await self.prompt.generate(
                self.llm, data=TextWithExtractionLimit(text=chunk, max_num=self.max_num)
            )
            if result:
                headlines.extend(result.headlines)
        return self.property_name, headlines


@dataclass
class NERExtractor(LLMBasedExtractor):
    """
    Trích xuất các thực thể có tên (Named Entities) từ văn bản cho trước.
    """

    property_name: str = "entities"
    prompt: PydanticPrompt[TextWithExtractionLimit, NEROutput] = NERPrompt()
    max_num_entities: int = 10

    async def extract(self, node: Node) -> t.Tuple[str, t.List[str]]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, []
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        entities = []
        for chunk in chunks:
            result = await self.prompt.generate(
                self.llm,
                data=TextWithExtractionLimit(text=chunk, max_num=self.max_num_entities),
            )
            entities.extend(result.entities)
        return self.property_name, entities


class TopicDescription(BaseModel):
    description: str


class TopicDescriptionPrompt(PydanticPrompt[StringIO, TopicDescription]):
    instruction: str = "Cung cấp một mô tả ngắn gọn về (các) chủ đề chính được thảo luận trong đoạn văn bản sau."
    input_model: t.Type[StringIO] = StringIO
    output_model: t.Type[TopicDescription] = TopicDescription
    examples: t.List[t.Tuple[StringIO, TopicDescription]] = [
        (
            StringIO(
                text="Máy tính lượng tử\n\nMáy tính lượng tử tận dụng các nguyên lý của cơ học lượng tử để thực hiện các phép toán phức tạp hiệu quả hơn so với máy tính cổ điển. Nó có tiềm năng cách mạng hóa các lĩnh vực như mật mã học, khoa học vật liệu và các bài toán tối ưu hóa bằng cách giải quyết các nhiệm vụ hiện không thể xử lý được bằng các hệ thống cổ điển."
            ),
            TopicDescription(
                description="Giới thiệu về máy tính lượng tử và tiềm năng vượt trội của nó so với máy tính cổ điển trong các tính toán phức tạp, gây ảnh hưởng lớn đến các lĩnh vực như mật mã và khoa học vật liệu."
            ),
        )
    ]


@dataclass
class TopicDescriptionExtractor(LLMBasedExtractor):
    """
    Trích xuất mô tả ngắn gọn về chủ đề chính từ văn bản cho trước.
    """

    property_name: str = "topic_description"
    prompt: PydanticPrompt = TopicDescriptionPrompt()

    async def extract(self, node: Node) -> t.Tuple[str, t.Any]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, None
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        result = await self.prompt.generate(self.llm, data=StringIO(text=chunks[0]))
        return self.property_name, result.description


class ThemesAndConcepts(BaseModel):
    output: t.List[str]


class ThemesAndConceptsExtractorPrompt(
    PydanticPrompt[TextWithExtractionLimit, ThemesAndConcepts]
):
    instruction: str = "Trích xuất các chủ đề và khái niệm chính từ văn bản cho trước."
    input_model: t.Type[TextWithExtractionLimit] = TextWithExtractionLimit
    output_model: t.Type[ThemesAndConcepts] = ThemesAndConcepts
    examples: t.List[t.Tuple[TextWithExtractionLimit, ThemesAndConcepts]] = [
        (
            TextWithExtractionLimit(
                text="Trí tuệ nhân tạo đang biến đổi các ngành công nghiệp bằng cách tự động hóa các công việc đòi hỏi trí thông minh của con người. AI phân tích lượng dữ liệu khổng lồ một cách nhanh chóng và chính xác, thúc đẩy các đổi mới như xe tự lái và hệ thống gợi ý cá nhân hóa.",
                max_num=10,
            ),
            ThemesAndConcepts(
                output=[
                    "Trí tuệ nhân tạo",
                    "Tự động hóa",
                    "Phân tích dữ liệu",
                    "Đổi mới sáng tạo",
                    "Xe tự lái",
                    "Đề xuất cá nhân hóa",
                ]
            ),
        )
    ]


@dataclass
class ThemesExtractor(LLMBasedExtractor):
    """
    Trích xuất các chủ đề (themes) từ văn bản cho trước.
    """

    property_name: str = "themes"
    prompt: ThemesAndConceptsExtractorPrompt = ThemesAndConceptsExtractorPrompt()
    max_num_themes: int = 10

    async def extract(self, node: Node) -> t.Tuple[str, t.List[str]]:
        node_text = node.get_property("page_content")
        if node_text is None:
            return self.property_name, []
        chunks = self.split_text_by_token_limit(node_text, self.max_token_limit)
        themes = []
        for chunk in chunks:
            result = await self.prompt.generate(
                self.llm,
                data=TextWithExtractionLimit(text=chunk, max_num=self.max_num_themes),
            )
            themes.extend(result.output)

        return self.property_name, themes