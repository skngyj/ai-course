import flet as ft

from calc import Calculator

GREY = ft.Colors.GREY_800
ORANGE = ft.Colors.ORANGE
LIGHT_GREY = ft.Colors.GREY_600

# (화면에 보이는 글자, press에 넘길 키, 배경색) 다섯 줄
BUTTONS = [
    [("C", "C", LIGHT_GREY), ("+/-", "+/-", LIGHT_GREY), ("%", "%", LIGHT_GREY), ("÷", "/", ORANGE)],
    [("7", "7", GREY), ("8", "8", GREY), ("9", "9", GREY), ("×", "*", ORANGE)],
    [("4", "4", GREY), ("5", "5", GREY), ("6", "6", GREY), ("−", "-", ORANGE)],
    [("1", "1", GREY), ("2", "2", GREY), ("3", "3", GREY), ("+", "+", ORANGE)],
    [("0", "0", GREY), (".", ".", GREY), ("⌫", "BS", GREY), ("=", "=", ORANGE)],
]

# 키보드에서 온 키 이름 가운데 press의 키로 바꿔 줄 것들
KEY_NAMES = {"Enter": "=", "Backspace": "BS", "Escape": "C"}
TYPED_KEYS = "0123456789.+-*/"


def to_press_key(event_key):
    """KeyboardEvent.key를 press가 아는 키로 바꾼다. 모르는 키는 None."""
    if event_key in KEY_NAMES:
        return KEY_NAMES[event_key]
    if len(event_key) == 1 and event_key in TYPED_KEYS:
        return event_key
    return None


def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calc = Calculator()

    display = ft.Text(value=calc.display, size=40, text_align=ft.TextAlign.RIGHT)

    def show():
        display.value = calc.display
        page.update()

    def on_button(e):
        calc.press(e.control.data)
        show()

    def on_key(e: ft.KeyboardEvent):
        key = to_press_key(e.key)
        if key is not None:
            calc.press(key)
            show()

    page.on_keyboard_event = on_key

    def make_button(label, key, bgcolor):
        return ft.Button(content=label, data=key, on_click=on_button, expand=1, height=60,
                         bgcolor=bgcolor, color=ft.Colors.WHITE)

    page.add(
        ft.Container(content=display, alignment=ft.Alignment.CENTER_RIGHT, padding=10, height=90),
        *[ft.Row(controls=[make_button(label, key, bgcolor) for label, key, bgcolor in row])
          for row in BUTTONS],
    )


ft.run(main)
