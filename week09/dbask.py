import sys
import sqlite3
import ollama
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")
con = sqlite3.connect("campus.db")

rows = con.execute("SELECT id, name, building, floor, hours, category, description, embedding FROM facility").fetchall()
V = np.stack([np.frombuffer(r[-1], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)


def search(question, k=3):
    q = np.array(ollama.embed(model="bge-m3", input=question).embeddings[0])
    q = q / np.linalg.norm(q)
    sims = V @ q
    return [(float(sims[i]), rows[i][:-1]) for i in np.argsort(-sims)[:k]]


def answer(question):
    found = search(question)
    context = "\n".join(f"- {name} ({building} {floor}층, {hours}): {desc}"
                        for _, (id_, name, building, floor, hours, cat, desc) in found)
    prompt = f"""아래 시설 목록만 근거로 질문에 답한다. 목록에 없는 내용은 "자료에 없습니다"라고 답한다. 답은 두 문장 이내로 쓴다.

시설 목록:
{context}

질문: {question}"""
    r = client.chat.completions.create(model="gemma4", temperature=0,
                                       messages=[{"role": "user", "content": prompt}])
    return found, r.choices[0].message.content.strip()


questions = sys.argv[1:] or [
    "커피 싸게 마실 수 있는 데 어디야?",
    "밤새고 아침에 밥 먹을 데 있어?",
    "조별 과제 모여서 할 카페 추천해줘",
    "만 원으로 고기 먹을 수 있어?",
    "초밥 뷔페 있어?",
]
for q in questions:
    found, a = answer(q)
    print("Q:", q)
    for s, (id_, name, *_rest) in found:
        print(f"   {s:.3f} {name}")
    print("   답:", a)
    print()
