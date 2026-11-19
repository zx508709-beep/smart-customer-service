from pathlib import Path

from sentence_transformers import SentenceTransformer

from qwen_answer import answer_question


POLICY_FILE = Path(__file__).resolve().parent / "knowledge" / "returns.md"
SOURCE = "knowledge/returns.md"
INSTRUCTION = "为这个句子生成表示以用于检索相关文章："


def load_retriever():
    document = POLICY_FILE.read_text(encoding="utf-8")
    sections = [part.strip() for part in document.split("\n## ")[1:] if part.strip()]

    if not sections:
        raise RuntimeError("知识库里没有找到以 ## 开头的政策章节。")

    model = SentenceTransformer("BAAI/bge-small-zh-v1.5", device="cpu")
    section_vectors = model.encode(sections, normalize_embeddings=True)
    return model, sections, section_vectors


def search_policy(question, retriever):
    model, sections, section_vectors = retriever
    question_vector = model.encode(
        INSTRUCTION + question, normalize_embeddings=True
    )
    scores = section_vectors @ question_vector
    return sections[int(scores.argmax())]


def main():
    print("正在加载检索模型……")
    retriever = load_retriever()

    while True:
        question = input("\n请输入售后问题，直接回车退出：").strip()
        if not question:
            break

        policy = search_policy(question, retriever)
        print(answer_question(question, policy))
        print(f"本次检索到的资料：{SOURCE} / {policy.splitlines()[0]}")


if __name__ == "__main__":
    main()