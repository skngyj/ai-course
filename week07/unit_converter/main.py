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

# 창 안쪽 여백과 조작 칸의 너비 (360 - 여백 16 × 2 = 328 안에 맞춘다)
PADDING = 16
FIELD_WIDTH = 328


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 360
    page.window.height = 480
    page.window.resizable = False

    value_field = ft.TextField(label="값", width=FIELD_WIDTH)
    from_dropdown = ft.Dropdown(label="출발 단위", width=FIELD_WIDTH, value="m",
                                options=[ft.DropdownOption(key=unit, text=unit) for unit in UNITS])
    to_dropdown = ft.Dropdown(label="도착 단위", width=FIELD_WIDTH, value="cm",
                              options=[ft.DropdownOption(key=unit, text=unit) for unit in UNITS])
    result = ft.Text(value="", size=32, width=FIELD_WIDTH)
    error = ft.Text(value="", size=14, color=ft.Colors.RED, width=FIELD_WIDTH)

    def refresh():
        text = convert(value_field.value, from_dropdown.value, to_dropdown.value)
        if text in ERRORS:               # 오류면 결과를 비우고 문구만 보여 준다
            result.value = ""
            error.value = text
        else:
            result.value = text
            error.value = ""
        page.update()

    value_field.on_change = lambda e: refresh()
    from_dropdown.on_select = lambda e: refresh()
    to_dropdown.on_select = lambda e: refresh()

    page.add(
        ft.Container(
            padding=PADDING,
            content=ft.Column(
                controls=[value_field, from_dropdown, to_dropdown, result, error],
                spacing=14,
            ),
        ),
    )
    refresh()    # 처음 창을 열면 값이 비어 있으므로 안내 문구가 보인다


ft.run(main)
