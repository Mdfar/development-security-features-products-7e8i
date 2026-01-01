from fastapi import FastAPI, Request, HTTPException import json import httpx from security.guardrails import inspect_prompt, detect_anomaly

app = FastAPI()

LLM Endpoint Configuration

LLM_API_URL = "https://api.openai.com/v1/chat/completions" API_KEY = "your-api-key"

@app.post("/v1/agent/proxy") async def ai_gateway_proxy(request: Request): body = await request.json() prompt = body.get("messages", [{}])[-1].get("content", "")

# 1. Redteaming / Security Inspection
is_safe, reason = inspect_prompt(prompt)
if not is_safe:
    raise HTTPException(status_code=403, detail=f"Security Violation: {reason}")

# 2. Proxy request to LLM
async with httpx.AsyncClient() as client:
    response = await client.post(
        LLM_API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json=body,
        timeout=30.0
    )
    
result = response.json()

# 3. Post-processing Trace Analysis
detect_anomaly(result)

return result


if name == "main": import uvicorn uvicorn.run(app, host="0.0.0.0", port=8080)