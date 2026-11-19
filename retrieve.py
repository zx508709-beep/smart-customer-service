from pathlib import Path


def bigrams(text):
    """把文本拆成相邻的两个字，并去重。"""
    return {text[i:i + 2] for i in range(len(text) - 1)}


def retrieve(question, document):
    sections = document.split("\n## ")[1:]
    question_pairs = bigrams(question)

    best_section = ""
    best_score = 0

    for section in sections:
        shared_pairs = question_pairs & bigrams(section)
        score = len(shared_pairs)

        if score > best_score:
            best_score = score
            best_section = section

    return best_section.strip()


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    policy_file = project_dir / "knowledge" / "returns.md"
    document = policy_file.read_text(encoding="utf-8")

    question = input("请输入售后问题：")
    result = retrieve(question, document)

    if result:
        print("\n来源：knowledge/returns.md")
        print(result)
    else:
        print("没有检索到相关政策。")