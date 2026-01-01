import re

def inspect_prompt(prompt: str) -> (bool, str): """ Core security logic to detect prompt injection and adversarial attacks. """ # Simple heuristic-based detection (Production would use a classifier model) injection_patterns = [ r"ignore previous instructions", r"system override", r"become a pirate", r"reveal your system prompt" ]

for pattern in injection_patterns:
    if re.search(pattern, prompt, re.IGNORECASE):
        return False, "Prompt Injection Detected"
        
# Length / Complexity check
if len(prompt) > 5000:
    return False, "Input exceeds safety buffer size"
    
return True, ""


def detect_anomaly(llm_response: dict): """ Analyzes agent output traces for abnormal patterns. """ content = llm_response.get("choices", [{}])[0].get("message", {}).get("content", "") # Logic to detect PII leakage or malformed tool calls if "password" in content.lower() or "secret_key" in content.lower(): print("ALERT: Possible Data Exfiltration Detected in Agent Trace")