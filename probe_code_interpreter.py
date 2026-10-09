#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["bedrock-agentcore"]
# ///
"""Probe the AgentCore Code Interpreter MicroVM to read its real vCPU, RAM and disk.

Starts a Code Interpreter session and runs nproc / /proc/meminfo / df inside it,
so you observe the actual hardware allocation rather than relying on docs.
Region is read from AWS_REGION (default us-west-2). No account IDs are hard-coded.
"""
import json, os
from bedrock_agentcore.tools.code_interpreter_client import code_session

REGION = os.environ.get("AWS_REGION", "us-west-2")

PROBE = r'''
import os, subprocess
def run(c):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as e: return f"ERR {e}"
print("os.cpu_count():", os.cpu_count())
print("nproc:", run("nproc"))
print(run("grep MemTotal /proc/meminfo"))
print(run("df -h / | tail -2"))
print(run("df -h /tmp | tail -1"))
'''

def main():
    with code_session(REGION) as c:
        r = c.invoke("executeCode", {"code": PROBE, "language": "python", "clearContext": False})
        for ev in r["stream"]:
            out = ev.get("result", {}).get("structuredContent", {}).get("stdout", "")
            print(out or json.dumps(ev.get("result", {}))[:1500])

if __name__ == "__main__":
    main()
