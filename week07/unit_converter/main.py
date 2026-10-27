"""단위 변환기 화면. 계산은 logic.convert에 맡기므로 여기서는 계산하지 않는다.

실행: python main.py
"""

import flet as ft

from logic import convert
from logic import ERROR_ABSOLUTE, ERROR_CATEGORY, ERROR_EMPTY, ERROR_NUMBER, ERROR_UNIT

# 화면에 보여 줄 단위. 두 드롭다운에 똑같이 넣는다
UNITS = ("mm", "cm", "m", "km", "°C", "°F")

# logic이 오류일 때 돌려 주는 문구들
ERRORS = (ERROR_EMPTY, ERROR_NUMBER, ERROR_UNIT, ERROR_CATEGORY, ERROR_ABSOLUTE)

TITLE = "단위 변환기"

# 시작값
START_VALUE = "100"
START_FROM = "cm"
START_TO = "m"

# 창 안쪽 여백과 너비 (360 - 여백 16 × 2 = 328)
PADDING = 16
WIDTH = 328
# 두 칸으로 나눈 행의 칸 너비 (328 - 간격 10) / 2 = 159
GROUP_WIDTH = 159
SPACING = 10


def labelled(label, control):
    """라벨과 조작 칸을 위아래로 붙여 한 칸을 만든다."""
    return ft.Column(controls=[ft.Text(value=label, size=13), control], width=GROUP_WIDTH, spacing=4)


def main(page: ft.Page):
    page.title = TITLE
    page.window.width = 360
    page.window.height = 480
    page.window.resizable = False

    value_field = ft.TextField(value=START_VALUE, width=GROUP_WIDTH)
    from_dropdown = ft.Dropdown(value=START_FROM, width=GROUP_WIDTH,
                                options=[ft.DropdownOption(key=unit, text=unit) for unit in UNITS])
    to_dropdown = ft.Dropdown(value=START_TO, width=GROUP_WIDTH,
                              options=[ft.DropdownOption(key=unit, text=unit) for unit in UNITS])
    result_field = ft.TextField(value="", width=GROUP_WIDTH, read_only=True)
    error_text = ft.Text(value="", size=13, color=ft.Colors.RED, width=WIDTH,
                         text_align=ft.TextAlign.CENTER)

    def on_convert(e):
        text = convert(value_field.value, from_dropdown.value, to_dropdown.value)
        if text in ERRORS:               # 오류면 결과를 비우고 문구만 보여 준다
            result_field.value = ""
            error_text.value = text
        else:
            result_field.value = text
            error_text.value = ""
        page.update()

    convert_button = ft.Button(content="변환", on_click=on_convert, expand=1, height=44,
                               bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)

    page.add(
        ft.Container(
            padding=PADDING,
            content=ft.Column(
                controls=[
                    # 상단 둥근 테두리 제목 영역
                    ft.Container(content=ft.Text(value=TITLE, size=18),
                                 width=WIDTH, padding=10,
                                 alignment=ft.Alignment.CENTER,
                                 border=ft.Border.all(width=1, color=ft.Colors.GREY_600),
                                 border_radius=ft.BorderRadius.all(20)),
                    # 위쪽 행: 값 입력과 출발 단위
                    ft.Row(controls=[labelled("값", value_field), labelled("단위", from_dropdown)],
                           spacing=SPACING),
                    # 가운데 아래 방향 화살표
                    ft.Text(value="↓", size=28, width=WIDTH, text_align=ft.TextAlign.CENTER),
                    # 아래쪽 행: 결과와 도착 단위
                    ft.Row(controls=[labelled("결과", result_field), labelled("단위", to_dropdown)],
                           spacing=SPACING),
                    # 가로로 긴 변환 버튼
                    ft.Row(controls=[convert_button]),
                    # 버튼 아래 오류 문구
                    error_text,
                ],
                spacing=12,
            ),
        ),
    )


ft.run(main)
