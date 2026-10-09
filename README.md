# AgentCore Code Interpreter: hardware verification

A tiny harness to verify the hardware an Amazon Bedrock AgentCore **Code Interpreter**
MicroVM session actually gets, by running `nproc`, `/proc/meminfo` and `df` inside a
live session.

## Why

The published spec for a Code Interpreter session is **2 vCPU / 8 GB RAM / 10 GB disk**
(plus a 900s default timeout and 100 MB max payload). Rather than trust the number,
this probe reads it from inside the running MicroVM.

Documented at the AgentCore service limits page, Code Interpreter Service Limits:
https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html#code-interpreter-service-limits

## Run it

```bash
# Requires AWS credentials for an account with AgentCore access.
AWS_REGION=us-west-2 uv run probe_code_interpreter.py
```

## Observed (desensitised)

See `sample-output.txt`. Summary:

| Spec | Documented | Observed in session |
|---|---|---|
| vCPU | 2 | `nproc` = 2 |
| RAM | 8 GB | `MemTotal` 8,209,720 kB (~8 GB) |
| Disk | 10 GB | root fs 9.7 G |
| /tmp | — | tmpfs 4.0 G |

Conclusion: the observed MicroVM matches the documented 2 vCPU / 8 GB / ~10 GB spec.

## Notes

- The `code_session` context manager starts and (on exit) terminates the session for you.
- No account IDs, role ARNs or session IDs are committed; supply your own credentials.
