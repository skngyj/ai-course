"""calc.py가 스펙 4절 규칙대로 동작하는지 검사한다. flet은 필요 없다.

실행: python test_calc.py
"""

from calc import Calculator

NO_KEY = "(아무것도 안 누름)"

# (누른 키 순서, 그 뒤에 보여야 하는 display) - 스펙 6절 표 그대로
CASES = [
    ("", "0"),
    ("1 2 + 3 =", "15"),
    ("2 + 3 * 4 =", "20"),
    ("5 + - 3 =", "2"),
    ("0 . 1 + 0 . 2 =", "0.3"),
    ("6 / 3 =", "2"),
    ("7 / 2 =", "3.5"),
    ("5 / 0 =", "0으로 나눌 수 없습니다"),
    ("5 / 0 = 7", "0으로 나눌 수 없습니다"),
    ("5 / 0 = C", "0"),
    ("1 . . 5", "1.5"),
    (".", "0."),
    ("0 0 7", "7"),
    ("1 2 3 BS", "12"),
    ("5 BS", "0"),
    ("9 +/-", "-9"),
    ("5 0 %", "0.5"),
    ("2 + 3 = 4", "4"),
    ("2 + 3 = + 4 =", "9"),
    ("2 + 3 = =", "5"),
]


def press(keys):
    """키 순서를 계산기에 넣고 마지막 display를 돌려준다."""
    calc = Calculator()
    for key in keys.split():
        calc.press(key)
    return calc.display


def main():
    failures = []
    for keys, expected in CASES:
        actual = press(keys)
        if actual != expected:
            failures.append((keys or NO_KEY, expected, actual))

    if failures:
        for keys, expected, actual in failures:
            print(f"실패: {keys} -> 기대 {expected!r}, 실제 {actual!r}")
        print(f"{len(failures)}개 실패 ({len(CASES)}개 중)")
        return 1

    print(f"모든 테스트 통과 ({len(CASES)}개)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
