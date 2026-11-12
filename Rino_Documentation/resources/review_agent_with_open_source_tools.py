import subprocess
import json
from openai import OpenAI

client = OpenAI()

# 1. Define Read-Only Tools (The Harness Capabilities)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read full contents of a file in the repository for surrounding context.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep_codebase",
            "description": "Search for function definitions, callers, or patterns across the repo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search string or regex"}
                },
                "required": ["query"],
            },
        },
    },
]

def execute_tool(name: str, args: dict) -> str:
    """Sandboxed tool router with output truncation to protect context limits."""
    if name == "read_file":
        try:
            with open(args["path"], "r", encoding="utf-8") as f:
                return f.read()[:12000]  # Cap at 12k chars
        except Exception as e:
            return f"Error reading file: {e}"
            
    elif name == "grep_codebase":
        res = subprocess.run(
            ["git", "grep", "-n", args["query"]],
            capture_output=True, text=True
        )
        return res.stdout[:6000] or "No matches found."
    return "Unknown tool."

# 2. The Harness Execution Loop
def run_review_harness(git_diff: str, max_steps: int = 8) -> dict:
    system_prompt = """You are a senior staff code reviewer. 
Review the provided git diff for bugs, security flaws, and broken edge cases.
Do NOT guess how external functions work—use `read_file` or `grep_codebase` to verify callers and types.
Ignore formatting nitpicks handled by linters.
When finished, return ONLY valid JSON matching:
{"comments": [{"file": str, "line": int, "severity": "high|medium|low", "issue": str, "suggestion": str}]}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Review this PR diff:\n\n```diff\n{git_diff}\n```"}
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        msg = response.choices[0].message
        messages.append(msg)

        # If the model finishes calling tools, parse its final review
        if not msg.tool_calls:
            return json.loads(msg.content)

        # Execute every requested tool and feed results back into context
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            observation = execute_tool(fn_name, fn_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": observation
            })

    raise RuntimeError("Review agent exceeded max_steps without finishing
