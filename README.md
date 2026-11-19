\# 售后智能客服



一个面向示例电商店铺的 RAG 客服。它用中文 BGE 模型检索 Markdown 售后政策，

把检索结果交给千问生成回答，并用 Streamlit 展示聊天和检索到的资料。



\## 快速开始



需要 Python 3.11、阿里云百炼 API Key，以及首次下载 BGE 模型的网络连接。

以下命令适用于 Windows Anaconda Prompt，请在克隆后的项目根目录运行。



```bat

conda create -n smart-cs python=3.11

conda activate smart-cs

python -m pip install -r requirements.txt

copy .env.example .env

notepad .env

```



填写自己的 `DASHSCOPE\_API\_KEY`，并确认 `QWEN\_BASE\_URL` 和 `QWEN\_MODEL`

与你的百炼配置一致。不要提交 `.env`。



```bat

python -m streamlit run app.py --server.address 127.0.0.1

```



打开终端显示的 Local URL。也可以运行 `python -u vector\_retrieve.py` 使用终端版。



\## 试着问



\- 商家寄错货，退货邮费谁出？

\- 商品签收后几天内可以申请退货？

\- 帮我查一下订单 12345 到哪了。



\## 已知限制



知识库是虚构的演示政策，未接入真实订单或物流系统。

网页显示聊天记录，但每次模型调用只处理本轮问题。

页面显示的是检索到的章节，不代表该章节一定能回答问题。



如果 BGE 已在本机缓存，但程序启动时反复重试访问 Hugging Face，

可以在启动前运行 `set "HF\_HUB\_OFFLINE=1"`。这不会禁止千问 API 联网。

