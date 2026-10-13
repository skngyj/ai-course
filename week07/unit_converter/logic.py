"""단위 변환 로직. 화면은 main.py가 맡으므로 여기서는 flet을 import하지 않는다.

SPEC.md 4절의 규칙을 그대로 따른다.
- 길이(mm, cm, m, km)는 m 기준 환산 계수로 계산한다.
- 온도(°C, °F)는 공식으로 계산한다.
- 검사 순서: 빈 입력 → 숫자 아님 → 알 수 없는 단위 → 카테고리 불일치 → 절대영도 → 계산
- 결과는 소수 6자리에서 반올림하고 뒤쪽 0과 필요 없는 소수점을 떼어 낸다.
"""

import math

# 길이: m 기준 환산 계수. 값 × 출발 계수 ÷ 도착 계수 로 계산한다
LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

# 온도: 계수가 없어 공식으로 계산한다
TEMPERATURE_UNITS = ("°C", "°F")

# 절대영도. 이보다 낮은 입력값은 받지 않는다
ABSOLUTE_ZERO = {"°C": -273.15, "°F": -459.67}

# 결과의 소수 자릿수
DECIMALS = 6

ERROR_EMPTY = "입력값을 모두 채워 주세요"
ERROR_NUMBER = "숫자를 입력하세요"
ERROR_UNIT = "알 수 없는 단위입니다"
ERROR_CATEGORY = "길이와 온도는 변환할 수 없습니다"
ERROR_ABSOLUTE = "절대영도보다 낮은 온도입니다"


def convert(value, from_unit, to_unit):
    """value(문자열)를 from_unit에서 to_unit으로 바꾼 결과 문자열을 돌려준다.

    정상이면 계산 결과 숫자 문자열, 잘못되었으면 오류 문구를 돌려준다.
    """
    value = value.strip()
    from_unit = from_unit.strip()
    to_unit = to_unit.strip()

    # 1. 빈 입력
    if not value or not from_unit or not to_unit:
        return ERROR_EMPTY

    # 2. 숫자가 아닌 값
    try:
        number = float(value)
    except ValueError:
        return ERROR_NUMBER
    # float()는 "nan"과 "inf"도 받아들이므로, 결과가 숫자가 아닌 것도 숫자 오류로 본다
    if not math.isfinite(number):
        return ERROR_NUMBER

    # 3. 알 수 없는 단위
    from_category = _category(from_unit)
    to_category = _category(to_unit)
    if from_category is None or to_category is None:
        return ERROR_UNIT

    # 4. 길이와 온도를 섞은 변환
    if from_category != to_category:
        return ERROR_CATEGORY

    # 5. 절대영도보다 낮은 온도 (입력값 기준)
    if from_unit in ABSOLUTE_ZERO and number < ABSOLUTE_ZERO[from_unit]:
        return ERROR_ABSOLUTE

    # 6. 계산. 같은 단위면 계산 없이 입력값을 그대로 쓰고, 결과 형식은 똑같이 적용한다
    if from_unit == to_unit:
        result = number
    elif from_unit in LENGTH_UNITS:
        result = number * LENGTH_UNITS[from_unit] / LENGTH_UNITS[to_unit]
    elif from_unit == "°C":
        result = number * 9 / 5 + 32
    else:
        result = (number - 32) * 5 / 9

    return _format(result)


def _category(unit):
    """단위의 카테고리를 돌려준다. 모르는 단위면 None을 돌려준다."""
    if unit in LENGTH_UNITS:
        return "length"
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    return None


def _format(value):
    """소수 6자리에서 반올림하고, 끝의 0과 필요 없는 소수점을 떼어 낸다."""
    text = f"{value:.{DECIMALS}f}".rstrip("0").rstrip(".")
    if text in ("", "-", "-0"):
        return "0"
    return text
