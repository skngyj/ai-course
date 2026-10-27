import sqlite3
import ollama
import numpy as np

con = sqlite3.connect("campus.db")
rows = con.execute("SELECT id, name, embedding FROM facility").fetchall()
names = [r[1] for r in rows]
V = np.stack([np.frombuffer(r[2], dtype=np.float32) for r in rows])
V = V / np.linalg.norm(V, axis=1, keepdims=True)

# (질문, 정답 가게 이름)
TESTS = [
    ("커피 제일 싼 데 어디야?", "컴포즈커피"),
    ("노트북 들고 과제할 카페 있어?", "투썸플레이스"),
    ("새벽까지 술 마실 수 있는 데?", "역전할머니맥주"),
    ("밤새고 아침에 밥 먹을 데?", "순대국밥집"),
    ("고기 무한리필 되는 데 있어?", "명륜진사갈비"),
    ("기숙사에서 제일 가까운 밥집?", "돈까스집"),
    ("매운 거 먹고 싶은데 어디 가?", "신전떡볶이"),
    ("부모님 오셨는데 모시고 갈 데?", "원할머니보쌈"),
    ("다이어트 중인데 가벼운 거 먹을 데?", "샐러디"),
    ("한 끼 제일 싸게 해결하려면?", "구내식당"),
]

hit1 = hit3 = 0
for q, want in TESTS:
    qv = np.array(ollama.embed(model="bge-m3", input=q).embeddings[0])
    qv = qv / np.linalg.norm(qv)
    top = [names[i] for i in np.argsort(-(V @ qv))[:3]]
    ok1, ok3 = top[0] == want, want in top
    hit1 += ok1
    hit3 += ok3
    print("O" if ok1 else ("△" if ok3 else "X"), q, "->", top[0], "" if ok1 else f"(정답 {want}, 3위 안 {ok3})")
print(f"\n1위 적중 {hit1}/{len(TESTS)}, 3위 안 적중 {hit3}/{len(TESTS)}")
