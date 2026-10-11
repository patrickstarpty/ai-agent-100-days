"""Smoke test: confirm the environment and llm.py are wired up correctly.

Run it from the directory that holds your llm.py (your project root):
    python3 path/to/scripts/smoke.py
"""
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.getcwd())   # llm.py lives in the directory you run this from
load_dotenv()

try:
    from llm import chat
except ModuleNotFoundError as e:
    if e.name != "llm":
        raise                     # llm.py exists but one of its imports is missing
    print(
        "当前目录下没有找到 llm.py。先按 Day02 的说明在项目根目录写一个 llm.py，"
        "提供 chat(messages, **kwargs) 函数，再在该目录下运行本脚本。",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    resp = chat(
        [
            {"role": "system", "content": "你是一个简洁的技术助手，回答不超过两句话。"},
            {"role": "user", "content": "用一句话说明什么是 agent。"},
        ],
        max_tokens=200,
    )
    text = resp.choices[0].message.content or ""
    print("回复前 80 字：", text[:80])
    print("token 用量：输入", resp.usage.prompt_tokens, "输出", resp.usage.completion_tokens)


if __name__ == "__main__":
    main()
