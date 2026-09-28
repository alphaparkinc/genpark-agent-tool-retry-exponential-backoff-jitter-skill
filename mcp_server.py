import sys, json
from client import AgentToolRetryBackoffJitter

def handle_mcp():
    resilient = AgentToolRetryBackoffJitter()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(resilient.run_resilience_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-tool-retry-exponential-backoff-jitter-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "calculate_backoff_delay", "description": "Calculate backoff duration with full jitter.", "inputSchema": {"type": "object", "properties": {"attempt": {"type": "integer"}, "base_delay": {"type": "number"}, "max_delay": {"type": "number"}}}},
                    {"name": "is_retryable_error", "description": "Check if an error is retryable.", "inputSchema": {"type": "object", "properties": {"error": {"type": "string"}}}},
                    {"name": "run_resilience_benchmark", "description": "Run resilience and jitter backoff benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "calculate_backoff_delay":
                    res = resilient.calculate_backoff_delay(args.get("attempt", 1), args.get("base_delay", 0.2), args.get("max_delay", 10.0))
                elif tname == "is_retryable_error":
                    res = resilient.is_retryable_error(args.get("error", ""))
                else:
                    res = resilient.run_resilience_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
