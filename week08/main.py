import flet as ft
from logic import calculate_fee

class ParkingRecord:
    def __init__(self, entry: str, exit: str, duration_min: int, display_time: str, fee: int):
        self.entry = entry
        self.exit = exit
        self.duration_min = duration_min
        self.display_time = display_time
        self.fee = fee

def main(page: ft.Page):
    page.title = "주차 요금 계산기"
    records = []

    total_fee_text = ft.Text(value="오늘 받은 요금 합계: 0원", size=18, weight=ft.FontWeight.BOLD)
    history_list = ft.Column(spacing=10, expand=True)
    error_text = ft.Text("")
    entry_input = ft.TextField(label="입차 시간 (HH:MM)")
    exit_input = ft.TextField(label="출차 시간 (HH:MM)")

    def format_money(amount: int) -> str:
        return f"{amount:,}원"

    def delete_record(index: int):
        records.pop(index)
        update_ui()

    def update_ui():
        history_list.controls.clear()
        total = sum(r.fee for r in records)
        total_fee_text.value = f"오늘 받은 요금 합계: {format_money(total)}"

        for i, r in enumerate(records):
            # Create a closure for the index to avoid the late binding issue in loops
            def make_delete_callback(idx):
                return lambda e: delete_record(idx)

            history_list.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(f"{r.entry} ~ {r.exit} ({r.display_time}) | {format_money(r.fee)}", expand=True),
                        ft.Button(content=ft.Text("삭제"), on_click=make_delete_callback(i))
                    ]
                )
            )
        page.update()

    def calculate_click(e):
        res = calculate_fee(entry_input.value, exit_input.value)
        if res["status"] == "error":
            error_text.value = res["message"]
            page.update()
            return

        new_record = ParkingRecord(
            entry=entry_input.value,
            exit=exit_input.value,
            duration_min=res["duration_min"],
            display_time=res["display_time"],
            fee=res["fee"]
        )
        records.append(new_record)
        entry_input.value = ""
        exit_input.value = ""
        error_text.value = ""
        update_ui()

    calculate_button = ft.Button(content=ft.Text("계산하기"), on_click=calculate_click)

    page.add(
        ft.Column(
            controls=[
                ft.Column(controls=[entry_input, exit_input]),
                ft.Column(controls=[calculate_button]),
                ft.Container(content=error_text, height=30),
                ft.Text("----------------------------------------"),
                total_fee_text,
                ft.Text("----------------------------------------"),
                ft.Text("주차 내역 목록", size=16, weight=ft.FontWeight.W_500),
                ft.Container(content=history_list, expand=True)
            ],
            expand=True,
            spacing=15
        )
    )

if __name__ == "__main__":
    ft.run(main)
if __name__ == "__main__":
    ft.run(main)
