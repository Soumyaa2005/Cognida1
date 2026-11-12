import os
import re
import json
import subprocess
import urllib.request
import urllib.error

API_KEY = os.environ["LLM_API_KEY"]
API_URL = os.environ.get("LLM_API_URL", "https://openai.com")
MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
REPO_ROOT = os.path.abspath(".")

# 1. Native Tool Definitions (JSON Schema)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_repo",
            "description": "Search tracked repository files for a literal string.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]

# 2. Sandboxed Tool Execution (Standard Library Only)
def run_tool(name: str, args: dict) -> str:
    if name == "read_file":
        target = os.path.abspath(os.path.join(REPO_ROOT, args.get("path", "")))
        if not target.startswith(REPO_ROOT + os.sep) or not os.path.isfile(target):
            return "Error: Invalid or unauthorized file path."
        try:
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                return f.read()[:12000]
        except OSError as e:
            return f"Error: {e}"

    if name == "search_repo":
        query = args.get("query", "")
        if not query or len(query) > 100:
            return "Error: Invalid search query."
        res = subprocess.run(
            ["git", "grep", "-n", "-F", "--", query],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return res.stdout[:6000] or "No matches found."

    return "Error: Unknown tool."

# 3. Direct HTTPS Client (No SDKs)
def call_llm(messages: list) -> dict:
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto",
        "temperature": 0.1,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

# 4. Deterministic Diff Line Validator (Sensor)
def get_valid_diff_lines(diff_text: str) -> dict[str, set[int]]:
    valid_lines: dict[str, set[int]] = {}
    current_file = None
    new_line_num = 0

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            valid_lines.setdefault(current_file, set())
        elif line.startswith("@@ "):
            match = re.search(r"\+(\d+)", line)
            if match:
                new_line_num = int(match.group(1))
        elif current_file:
            if line.startswith("+") and not line.startswith("+++"):
                valid_lines[current_file].add(new_line_num)
                new_line_num += 1
            elif not line.startswith("-"):
                new_line_num += 1

    return valid_lines

# 5. Core Harness Loop
def review_pr(base_branch: str = "origin/main", max_steps: int = 8) -> list[dict]:
    diff_proc = subprocess.run(
        ["git", "diff", "-U3", f"{base_branch}...HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    diff_text = diff_proc.stdout
    if not diff_text.strip():
        return []

    valid_lines = get_valid_diff_lines(diff_text)
    system_prompt = (
        "You are a strict code reviewer. Inspect the diff for bugs, race conditions, "
        "and security flaws. Use tools to check surrounding context before commenting. "
        "Output ONLY valid JSON: "
        '{"comments": [{"file": "path", "line": 10, "severity": "high", "message": "..."}]}'
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Review this diff:\n\n{diff_text[:30000]}"},
    ]

    for _ in range(max_steps):
        data = call_llm(messages)
        msg = data["choices"][0]["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            raw_json = msg.get("content", "{}").strip()
            raw_json = re.sub(r"^```json\s*|\s*```$", "", raw_json)
            parsed = json.loads(raw_json)
            
            # Filter out comments on lines not touched in the diff
            return [
                c for c in parsed.get("comments", [])
                if c.get("line") in valid_lines.get(c.get("file"), set())
            ]

        for call in tool_calls:
            fn_name = call["function"]["name"]
            fn_args = json.loads(call["function"]["arguments"])
            result = run_tool(fn_name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": call["id"],
                "content": result,
            })

    raise TimeoutError("Harness reached max_steps without completing review.")

if __name__ == "__main__":
    findings = review_pr()
    print(json.dumps(findings, indent=2))

