import contextlib
import io
import re
import sys
from pathlib import Path
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
MODEL = "gemma4"
N = 5

TESTS = [
    ("010-1234-5678", "010-1234-5678"),
    ("01012345678", "010-1234-5678"),
    ("010 1234 5678", "010-1234-5678"),
    ("010.1234.5678", "010-1234-5678"),
    ("+82 10-1234-5678", "010-1234-5678"),
    ("011-123-4567", "011-123-4567"),
    ("02-123-4567", None),
    ("010-1234-567", None),
    ("010-abcd-5678", None),
    ("", None),
]


def generate(prompt):
    r = client.chat.completions.create(
        model=MODEL, temperature=0.7, max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def extract_code(text):
    blocks = re.findall(r"```(?:python)?\n(.*?)```", text, re.S)
    return blocks[0] if blocks else text


def score(code):
    space = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, space)
    except Exception as e:
        return 0, f"실행 오류: {e}"
    func = space.get("normalize_phone")
    if func is None:
        names = [k for k, v in space.items() if callable(v) and not k.startswith("_")]
        return 0, f"normalize_phone 없음. 있는 함수: {names}"
    passed, failed = 0, []
    for arg, want in TESTS:
        try:
            got = func(arg)
        except Exception as e:
            got = f"예외 {type(e).__name__}"
        if got == want:
            passed += 1
        else:
            failed.append(f"{arg!r} -> {got!r}")
    return passed, "; ".join(failed)


if len(sys.argv) != 2:
    script_name = Path(sys.argv[0]).name
    print(f"사용법: python {script_name} <프롬프트 파일>")
    print("예시: python evalprompt.py vague_1.txt")
    sys.exit(1)

prompt_path = Path(sys.argv[1])
if not prompt_path.is_file():
    print(f"오류: 프롬프트 파일을 찾을 수 없습니다: {prompt_path}")
    print("현재 폴더의 파일 목록을 확인하고 .txt 파일을 지정하세요.")
    sys.exit(1)

prompt = prompt_path.read_text(encoding="utf-8")
total = 0
for i in range(N):
    code = extract_code(generate(prompt))
    open(f"out_{i + 1}.py", "w", encoding="utf-8").write(code)
    passed, note = score(code)
    total += passed
    print(f"{i + 1}회: {passed}/{len(TESTS)}  {note}")
print(f"평균 {total / N:.1f}/{len(TESTS)}")
