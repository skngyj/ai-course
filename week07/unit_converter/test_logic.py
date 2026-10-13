"""logic.py가 스펙 4절 규칙대로 동작하는지 검사한다. flet은 필요 없다.

실행: python test_logic.py
"""

from logic import convert

CELSIUS = "°C"
FAHRENHEIT = "°F"

# (value, from_unit, to_unit, 기대 반환) - 스펙 6절 표 그대로
CASES = [
    ("1000", "mm", "m", "1"),
    ("1", "m", "cm", "100"),
    ("2.5", "km", "m", "2500"),
    ("0.5", "m", "mm", "500"),
    ("1", "cm", "km", "0.00001"),
    ("3", "m", "m", "3"),
    ("6.213712345", "m", "m", "6.213712"),
    ("0", CELSIUS, FAHRENHEIT, "32"),
    ("100", CELSIUS, FAHRENHEIT, "212"),
    ("-40", CELSIUS, FAHRENHEIT, "-40"),
    ("98.6", FAHRENHEIT, CELSIUS, "37"),
    ("25", CELSIUS, CELSIUS, "25"),
    ("1", FAHRENHEIT, CELSIUS, "-17.222222"),
    ("10", FAHRENHEIT, CELSIUS, "-12.222222"),
    ("12.5", FAHRENHEIT, CELSIUS, "-10.833333"),
    ("abc", "m", "cm", "숫자를 입력하세요"),
    ("1.2.3", "m", "cm", "숫자를 입력하세요"),
    ("", "m", "cm", "입력값을 모두 채워 주세요"),
    ("1", "", "cm", "입력값을 모두 채워 주세요"),
    ("1", "mile", "m", "알 수 없는 단위입니다"),
    ("1", "m", CELSIUS, "길이와 온도는 변환할 수 없습니다"),
    ("-300", CELSIUS, FAHRENHEIT, "절대영도보다 낮은 온도입니다"),
    ("-500", FAHRENHEIT, CELSIUS, "절대영도보다 낮은 온도입니다"),
    ("-500", CELSIUS, CELSIUS, "절대영도보다 낮은 온도입니다"),
]


def main():
    failures = []
    for value, from_unit, to_unit, expected in CASES:
        actual = convert(value, from_unit, to_unit)
        if actual != expected:
            shown = value if value else "(빈 문자열)"
            failures.append((shown, from_unit, to_unit, expected, actual))

    if failures:
        for value, from_unit, to_unit, expected, actual in failures:
            print(f"실패: value={value!r} from={from_unit!r} to={to_unit!r} -> "
                  f"기대 {expected!r}, 실제 {actual!r}")
        print(f"{len(failures)}개 실패 ({len(CASES)}개 중)")
        return 1

    print(f"모든 테스트 통과 ({len(CASES)}개)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
