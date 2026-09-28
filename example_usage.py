from client import AgentToolRetryBackoffJitter
import json

resilient = AgentToolRetryBackoffJitter()
print("=== AGENT TOOL RETRY & EXPONENTIAL BACKOFF BENCHMARK ===")
res = resilient.run_resilience_benchmark()
print(json.dumps(res, indent=2))
