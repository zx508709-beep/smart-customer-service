from pathlib import Path

from sentence_transformers import SentenceTransformer


project_dir = Path(__file__).resolve().parent
policy_file = project_dir / "knowledge" / "returns.md"
document = policy_file.read_text(encoding="utf-8")
sections = [part.strip() for part in document.split("\n## ")[1:]]

model = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")

# 每一节政策转成一个向量。知识库不变，不用每次提问都重新计算。
section_vectors = model.encode(sections, normalize_embeddings=True)
print("知识库向量形状", section_vectors.shape)

while True:
    question = input("\n请输入售后问题，直接回车退出：").strip()
    if not question:
        break

    instruction = "为这个句子生成表示以用于检索相关文章："
    question_vector = model.encode(
        instruction + question,
        normalize_embeddings=True,
    )

    # 两边的向量都归一化了，点积就是余弦相似度。
    scores = section_vectors @ question_vector
    ranked_indices = scores.argsort()[::-1]

    print("相似度排名")
    for index in ranked_indices:
        title = sections[index].splitlines()[0]
        print(f"{scores[index]:.3f}  {title}")

    best_index = ranked_indices[0]
    print("\n来源：knowledge/returns.md")
    print(sections[best_index])