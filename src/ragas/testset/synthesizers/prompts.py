import typing as t

from pydantic import BaseModel

from ragas.prompt import PydanticPrompt
from ragas.testset.persona import Persona


class ThemesPersonasInput(BaseModel):
    themes: t.List[str]
    personas: t.List[Persona]


class PersonaThemesMapping(BaseModel):
    mapping: t.Dict[str, t.List[str]]


class ThemesPersonasMatchingPrompt(
    PydanticPrompt[ThemesPersonasInput, PersonaThemesMapping]
):
    instruction: str = (
        "Dựa trên danh sách các chủ đề (themes) và hình mẫu (personas) cùng với vai trò của họ, "
        "hãy liên kết mỗi hình mẫu với các chủ đề phù hợp dựa theo mô tả vai trò của họ."
    )
    input_model: t.Type[ThemesPersonasInput] = ThemesPersonasInput
    output_model: t.Type[PersonaThemesMapping] = PersonaThemesMapping
    examples: t.List[t.Tuple[ThemesPersonasInput, PersonaThemesMapping]] = [
        (
            ThemesPersonasInput(
                themes=["Sự thấu cảm", "Tính toàn diện", "Làm việc từ xa"],
                personas=[
                    Persona(
                        name="Quản lý Nhân sự",
                        role_description="Tập trung vào tính toàn diện và hỗ trợ nhân viên.",
                    ),
                    Persona(
                        name="Trưởng nhóm Từ xa",
                        role_description="Quản lý giao tiếp và tương tác trong đội ngũ làm việc từ xa.",
                    ),
                ],
            ),
            PersonaThemesMapping(
                mapping={
                    "Quản lý Nhân sự": ["Tính toàn diện", "Sự thấu cảm"],
                    "Trưởng nhóm Từ xa": ["Làm việc từ xa", "Sự thấu cảm"],
                }
            ),
        )
    ]