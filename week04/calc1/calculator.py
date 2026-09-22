"""터미널에서 쓰는 계산기.

식을 한 줄로 입력하면 값을 계산해 준다. 사칙연산, 괄호, 소수, 단항 부호를 지원한다.

실행:
    python calculator.py              # 계속 입력 (끝내려면 q)
    python calculator.py "2 + 3 * 4"  # 한 번만 계산하고 끝
"""

import math
import sys

DIGITS = "0123456789"
OPERATORS = "+-*/"
BRACKETS = "()"


class CalcError(ValueError):
    """식이 잘못되었거나 0으로 나누었을 때 낸다."""


# ------------------------------------------------------------------ 글자 나누기


def tokenize(text):
    """식을 (종류, 값) 목록으로 나눈다. 종류는 "number" 아니면 "op"이다."""
    tokens = []
    i = 0
    while i < len(text):
        ch = text[i]

        if ch.isspace():
            i += 1
        elif ch in DIGITS or ch == ".":
            start = i
            dots = 0
            while i < len(text) and (text[i] in DIGITS or text[i] == "."):
                if text[i] == ".":
                    dots += 1
                i += 1
            number = text[start:i]
            if dots > 1 or number == ".":
                raise CalcError(f"숫자가 잘못되었습니다: {number}")
            tokens.append(("number", float(number)))
        elif ch in OPERATORS or ch in BRACKETS:
            tokens.append(("op", ch))
            i += 1
        else:
            raise CalcError(f"알 수 없는 글자입니다: {ch}")

    if not tokens:
        raise CalcError("식이 비어 있습니다")
    return tokens


# ------------------------------------------------------------------ 계산하기


class Parser:
    """토큰 목록을 읽어 값을 계산한다. 곱셈·나눗셈을 덧셈·뺄셈보다 먼저 한다.

    expression = term (("+" | "-") term)*
    term       = factor (("*" | "/") factor)*
    factor     = ("+" | "-") factor | "(" expression ")" | number
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ------------------------------------------------------------ 토큰 다루기

    def _peek(self):
        """지금 볼 차례인 토큰. 다 읽었으면 (None, None)."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None, None

    def _take(self):
        kind, value = self._peek()
        self.pos += 1
        return kind, value

    def _take_op(self, op):
        """다음 토큰이 op이면 먹고 True, 아니면 False."""
        kind, value = self._peek()
        if kind == "op" and value == op:
            self.pos += 1
            return True
        return False

    # -------------------------------------------------------------- 계산 규칙

    def parse(self):
        value = self.expression()
        if self.pos != len(self.tokens):
            kind, token = self._peek()
            raise CalcError(f"식을 읽을 수 없습니다: {token} 앞이 이상합니다")
        return value

    def expression(self):
        value = self.term()
        while True:
            if self._take_op("+"):
                value = self._check(value + self.term())
            elif self._take_op("-"):
                value = self._check(value - self.term())
            else:
                return value

    def term(self):
        value = self.factor()
        while True:
            if self._take_op("*"):
                value = self._check(value * self.factor())
            elif self._take_op("/"):
                divisor = self.factor()
                if divisor == 0:
                    raise CalcError("0으로 나눌 수 없습니다")
                value = self._check(value / divisor)
            else:
                return value

    def factor(self):
        kind, value = self._peek()

        if kind == "op" and value in "+-":     # 단항 부호 (예: -3, --5)
            self._take()
            item = self.factor()
            return item if value == "+" else -item

        if kind == "op" and value == "(":      # 괄호
            self._take()
            item = self.expression()
            if not self._take_op(")"):
                raise CalcError("닫는 괄호가 없습니다")
            return item

        if kind == "number":
            self._take()
            return value

        if kind is None:
            raise CalcError("식이 끝나지 않았습니다")
        raise CalcError(f"숫자가 와야 할 자리에 {value}가 있습니다")

    @staticmethod
    def _check(value):
        if math.isinf(value) or math.isnan(value):
            raise CalcError("계산 결과가 너무 큽니다")
        return value


def calculate(text):
    """식 문자열을 계산해서 값을 돌려준다. 잘못된 식이면 CalcError."""
    cleaned = text.strip()
    if cleaned.endswith("="):                  # "2+3=" 처럼 끝에 =를 붙여도 받아 준다
        cleaned = cleaned[:-1]
    return Parser(tokenize(cleaned)).parse()


def format_number(value):
    """값을 보기 좋은 문자열로 바꾼다. 7.0 -> "7", 0.30000000000000004 -> "0.3"."""
    if value == int(value):
        return str(int(value))
    return f"{value:.10f}".rstrip("0").rstrip(".")


def calculate_text(text):
    """식을 계산해서 보여 줄 문자열을 돌려준다."""
    return format_number(calculate(text))


# ------------------------------------------------------------------ 터미널


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)

    if args:                                   # 인자로 받은 식을 한 번만 계산
        try:
            print(calculate_text(" ".join(args)))
        except CalcError as error:
            print(f"오류: {error}")
            return 1
        return 0

    print("계산기입니다. 식을 입력하세요. 끝내려면 q를 누르세요.")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if line.strip().lower() in ("q", "quit", "exit"):
            break
        if not line.strip():
            continue

        try:
            print(f"= {calculate_text(line)}")
        except CalcError as error:
            print(f"오류: {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

