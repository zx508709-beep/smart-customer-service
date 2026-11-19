from pathlib import Path

from dotenv import dotenv_values
from openai import OpenAI


def answer_question(question, policy):
    env_file = Path(__file__).resolve().with_name(".env")
    config = dotenv_values(env_file, encoding="utf-8-sig")

    api_key = config.get("DASHSCOPE_API_KEY")
    base_url = config.get("QWEN_BASE_URL")
    model_name = config.get("QWEN_MODEL")

    if not all((api_key, base_url, model_name)) or api_key == "在这里填写你的百炼Key":
        raise RuntimeError("请在项目根目录的 .env 中填写有效的 Key、接口地址和模型名。")

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0,
        max_retries=0,
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是示例店铺的售后客服。只根据提供的政策回答，不要编造。"
                    "如果客户没有提供判断所需的信息，先追问。"
                    "如果政策没有答案，就明确说明无法回答。"
                    "你没有接入订单或物流系统，不能查询实际订单状态。"
                    "请用简明的中文回答。"
                ),
            },
            {
                "role": "user",
                "content": f"【检索到的政策】\n{policy}\n\n【客户问题】\n{question}",
            },
        ],
    )

    return response.choices[0].message.content or "模型没有返回文字。"