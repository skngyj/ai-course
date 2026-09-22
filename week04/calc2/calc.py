"""계산기 로직. 화면은 main.py가 맡으므로 여기서는 flet을 import하지 않는다."""


class Calculator:
    """즉시 계산 방식 계산기.

    press(key) 하나로 모든 입력을 받고, display 속성으로 화면에 보일 값을 돌려준다.
    연산자 우선순위가 없고, 누른 순서대로 바로 계산한다.
    """

    ERROR = "0으로 나눌 수 없습니다"
    MAX_DIGITS = 12
    DIGITS = "0123456789"
    OPERATORS = ("+", "-", "*", "/")

    def __init__(self):
        self.display = "0"
        self._current = "0"        # 지금 만들고 있는 수 (문자열)
        self._acc = None           # 지금까지 계산해 둔 값
        self._op = None            # 아직 적용하지 않은 연산자
        self._entry_open = False   # _current에 글자를 더 넣을 수 있는 상태인가
        self._last = None          # 마지막 입력 종류: "digit" / "operator" / "equal" / "value"
        self._error = False        # 0으로 나눈 상태인가

    def press(self, key):
        """키를 하나 누른 것처럼 처리하고, 화면에 보일 문자열을 돌려준다."""
        if self._error:
            if key != "C":                 # 0으로 나눈 뒤에는 C만 받는다
                return self.display
            self._reset()
        elif key == "C":
            self._reset()
        elif key in self.DIGITS or key == ".":
            self._input_digit(key)
        elif key in self.OPERATORS:
            self._input_operator(key)
        elif key == "=":
            self._input_equals()
        elif key == "BS":
            self._input_backspace()
        elif key == "+/-":
            self._input_sign()
        elif key == "%":
            self._input_percent()

        self.display = self.ERROR if self._error else self._shown()
        return self.display

    # ------------------------------------------------------------------ 숫자

    def _input_digit(self, key):
        if self._last == "equal" or not self._entry_open:
            self._current = "0"
            if self._last == "equal":      # '=' 뒤에 숫자를 누르면 새 계산을 시작한다
                self._acc = None
                self._op = None
            self._entry_open = True

        if key == ".":
            if "." not in self._current:   # 소수점은 한 수에 한 번만
                self._current += "."
        elif self._digit_count() < self.MAX_DIGITS:
            if self._current in ("0", "-0"):    # 앞에 붙는 0은 남기지 않는다
                sign = "-" if self._current.startswith("-") else ""
                self._current = sign + key
            else:
                self._current += key

        self._last = "digit"

    def _input_sign(self):
        if self._current.startswith("-"):
            self._current = self._current[1:]
        else:
            self._current = "-" + self._current

    def _input_percent(self):
        self._current = self._format(self._value() / 100)
        self._entry_open = False
        self._last = "value"

    def _input_backspace(self):
        if not self._entry_open:           # 결과가 보이는 상태에서는 아무 일도 하지 않는다
            return
        self._current = self._current[:-1]
        if self._current in ("", "-"):
            self._current = "0"
        self._last = "digit"

    # ---------------------------------------------------------------- 연산자

    def _input_operator(self, key):
        if self._last == "operator":       # 연달아 누르면 마지막에 누른 것으로 바뀐다
            self._op = key
            return

        if self._op is None:
            self._acc = self._value()
        else:
            result = self._apply(self._acc, self._op, self._value())
            if self._error:
                return
            self._acc = result
            self._current = self._format(result)

        self._op = key
        self._entry_open = False
        self._last = "operator"

    def _input_equals(self):
        if self._last == "equal":          # '='을 연달아 눌러도 같은 연산을 반복하지 않는다
            return

        if self._op is None:
            result = self._value()
        else:
            result = self._apply(self._acc, self._op, self._value())
            if self._error:
                return

        self._current = self._format(result)
        self._acc = result
        self._op = None
        self._entry_open = False
        self._last = "equal"

    def _apply(self, a, op, b):
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                self._error = True
                return 0.0
            return a / b
        return b

    # ------------------------------------------------------------------ 도구

    def _reset(self):
        self._current = "0"
        self._acc = None
        self._op = None
        self._entry_open = False
        self._last = None
        self._error = False

    def _value(self):
        try:
            return float(self._current)
        except ValueError:
            return 0.0

    def _digit_count(self):
        return sum(1 for ch in self._current if ch.isdigit())

    def _shown(self):
        if self._current in ("", "-0"):
            return "0"
        # 값이 0이면 부호는 보여 주지 않는다 ("-0." -> "0."). 다음 숫자 입력에는 부호가 살아 있다
        if self._current.startswith("-") and self._value() == 0:
            return self._current[1:]
        return self._current

    @staticmethod
    def _format(value):
        """소수 10자리에서 반올림하고, 끝의 0과 필요 없는 소수점을 떼어 낸다."""
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        if text in ("", "-", "-0"):
            return "0"
        return text
