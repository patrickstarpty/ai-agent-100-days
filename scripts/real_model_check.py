"""Run the lesson code against a real model.

The code under test is extracted from the lesson files themselves, so this
checks what learners actually copy. Configure the model the same way the course
does (Day02): LLM_MODEL, the provider key litellm expects, and optionally
LLM_API_BASE. A .env in the current directory is read if present.

Usage:
    pip install -r requirements.txt
    python3 scripts/real_model_check.py            # all checks
    python3 scripts/real_model_check.py day06 day36 # only some

Each check runs in its own temporary directory and subprocess. The script makes
a few dozen model calls in total; re-run it after changing models (Day32, Day100).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = int(os.environ.get("CHECK_TIMEOUT", "180"))


def blocks(day: str) -> list[str]:
    """All ```python blocks of a lesson, by two-digit day number."""
    folder = next(p for p in ROOT.glob("Day*") if p.is_dir() and _covers(p.name, int(day)))
    path = next(folder.glob(f"{day}.*.md"))
    return re.findall(r"```python\n(.*?)```", path.read_text(encoding="utf-8"), re.S)


def _covers(folder: str, n: int) -> bool:
    lo, hi = (int(x) for x in re.findall(r"\d+", folder)[:2])
    return lo <= n <= hi


def llm_py() -> str:
    """Day02's llm.py with the optional LLM_API_BASE from the same lesson."""
    b = blocks("02")
    return b[1] + "\n" + b[2]


def agent_files() -> dict[str, str]:
    b = blocks("06")
    return {"tools.py": b[0], "agent.py": b[1]}


# Each check: files to write, the script to run, and a function judging stdout.
def checks() -> dict[str, tuple[dict[str, str], str, callable]]:
    d03, d04, d08, d09 = blocks("03"), blocks("04"), blocks("08"), blocks("09")
    agent = agent_files()
    c: dict[str, tuple[dict[str, str], str, callable]] = {}

    c["day02"] = ({}, blocks("02")[0], lambda out: bool(out.strip()))

    c["day03"] = ({"llm.py": llm_py()}, d03[0] + "\n" + d03[1] + "\nrun_cases()\n",
                  lambda out: "通过 " in out)

    c["day04"] = ({"llm.py": llm_py()}, d04[0] + "\n" + d04[1] + textwrap.dedent("""
        t = extract("我被重复扣款了两次，今天必须退回来，不然我就投诉")
        print("RESULT", t.category, t.urgent, t.summary)
        """), lambda out: "RESULT 账单" in out)

    c["day05"] = ({"llm.py": llm_py()}, blocks("05")[0],
                  lambda out: "发货" in out or "2 天" in out or "两天" in out)

    c["day06"] = ({"llm.py": llm_py(), **agent}, "import runpy; runpy.run_path('agent.py', run_name='__main__')\n",
                  lambda out: "187.5" in out)

    c["day08-stream"] = ({"llm.py": llm_py()}, d08[0] + textwrap.dedent("""
        text = stream_reply([{"role": "user", "content": "用一句话介绍你自己。"}])
        print("LEN", len(text))
        """), lambda out: "LEN " in out and "LEN 0" not in out)

    c["day08-events"] = ({"llm.py": llm_py(), **agent},
                         "from llm import chat\nfrom agent import SYSTEM, TOOLS, run_tool\n" + d08[1] + "\n" + d08[2],
                         lambda out: "187.5" in out)

    c["day09"] = ({"retry.py": d09[0], "llm.py": d09[1]},
                  "from llm import chat\nr = chat([{'role': 'user', 'content': '回答“好”。'}], max_tokens=20)\n"
                  "print('OK', (r.choices[0].message.content or '').strip()[:20])\n",
                  lambda out: "OK " in out)

    d36 = blocks("36")[0]
    c["day36"] = ({"llm.py": llm_py(), **agent}, d36, lambda out: out.startswith("completed") and "187.5" in out)
    c["day40"] = ({"llm.py": llm_py(), **agent}, d36 + "\n" + blocks("40")[0],
                  lambda out: out.strip().endswith("()"))
    c["day41"] = ({}, blocks("41")[0], lambda out: "Interrupt(" in out and out.strip().endswith("True"))

    smoke = (ROOT / "scripts" / "smoke.py").read_text(encoding="utf-8")
    c["smoke"] = ({"llm.py": llm_py()}, smoke, lambda out: "token 用量" in out)
    return c


def run(name: str, files: dict[str, str], script: str, judge) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        for fname, body in files.items():
            Path(tmp, fname).write_text(body, encoding="utf-8")
        Path(tmp, "check_main.py").write_text(script, encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, "check_main.py"], cwd=tmp, capture_output=True,
                               text=True, timeout=TIMEOUT, env=os.environ.copy())
            out, err, code = p.stdout, p.stderr, p.returncode
        except subprocess.TimeoutExpired:
            out, err, code = "", f"timeout after {TIMEOUT}s", -1
    ok = code == 0 and judge(out)
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    shown = out.strip().splitlines()[-6:]
    for line in shown:
        print(f"      {line[:160]}")
    if not ok and err.strip():
        for line in err.strip().splitlines()[-6:]:
            print(f"   !  {line[:160]}")
    return ok


def main() -> int:
    try:
        from dotenv import load_dotenv
        load_dotenv(Path.cwd() / ".env")
    except ImportError:
        pass
    if not os.environ.get("LLM_MODEL"):
        print("先设置 LLM_MODEL（以及 litellm 要求的供应商密钥），见 Day02 和 .env.example。", file=sys.stderr)
        return 2
    wanted = set(sys.argv[1:])
    results = {}
    for name, (files, script, judge) in checks().items():
        if wanted and name not in wanted:
            continue
        if name.startswith(("day36", "day40", "day41")):
            try:
                import langgraph  # noqa: F401
            except ImportError:
                print(f"SKIP  {name}（没有安装 langgraph）")
                continue
        results[name] = run(name, files, script, judge)
    failed = [n for n, ok in results.items() if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed" + (f"; failed: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
