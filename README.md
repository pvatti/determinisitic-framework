# determinisitic-framework
A lightweight deterministic decision engine for rule‑based, traceable outcomes in enterprise workflows.

This repository contains a tiny, beginner‑friendly example of deterministic decision logic using Python, JSON inputs, and YAML rules. It’s designed so anyone — even without Python experience — can run it, modify it, and understand how deterministic systems work.

## What this framework does

This example shows how to:
    * evaluate decisions withot probability or guessing
    * enforces explicit rules instead of model improvisation
    * produce traceable, auditable outcomes
    * escalate safely when no rule matches
    * help readers understand deterministic AI governance

It is intentionally simple, readable, and sage for beginners.

## Repository Structure

```text
deterministic-framework/
│
├── src/
│   ├── deterministic/
│   │   ├── rules.yaml
│   │   ├── inputs.json
│   │   ├── engine.py
│   │   ├── router.py
│   │   └── __init__.py
│   │
│   ├── ai/
│   │   ├── ai_model_interface.py
│   │   ├── ollama_model.py
│   │   ├── ai_action_layer.py
│   │   └── __init__.py
│
├── docs/
│   ├── architecture.md
│   ├── governance.md
│   └── extending.md
│
├── requirements.txt
├── LICENSE
└── README.md
```

## Create a Python environment

A deterministic framework only works if everyone runs the same environment.
So before running the example, create a clean Python environment

1. Install Python (if you don't have it)

Download Python 3.10+ from python.org

2. Create a virtual environment

This keeps your deterministic framework isolated and reproducible
Run this in your terminal:

```python
python -m venv env
```

3. Activate the environment

Windows:

```python
env\Scripts\activate
```

macOS/Linux:

```python
source env/bin/activate
```

You'll know it worked when your terminal shows at the beginning:

```bash
(env)
```

## Install dependencies

```python
pip install -r requirements.txt
```

This ensures everyone runs the same version, a core principle of deterministic behavior.

Once this is complete you'll be ready to run the example:
You will see
    * which rule matched
    * the final outcome
    * the escalation path
    * a full evaluation trace

## How it works

1. Inputs(input.json)

your engine evaluates these values:

```json
{
  "risk_score": 12,
  "requested_amount": 15000,
  "existing_customer": true
}
```

2. Rules(rules.yaml)

Rules are expected to be deterministic

```yaml
rules:
  - name: escalate_medium_risk
    priority: 3
    conditions:
      risk_score:
        min: 11
        max: 20
    outcome: REVIEW
    escalation: ESCALATE_TO_MANAGER
```

Supported condition types:
* Equality
* Range(min/max)

Engine Logic

1. Load inputs
2. Load Rules
3. Evaluate rules in priority order
4. Log every step
5. Return the first matching rule
6. If none match -> deterministic escalation

## Output example

```text
=== Deterministic Framework Example ===
Matched rule : escalate_medium_risk
Outcome      : REVIEW
Escalation   : ESCALATE_TO_MANAGER

Evaluation Trace:
 - approve_low_risk: SKIP
 - approve_existing_customer: SKIP
 - escalate_medium_risk: MATCH
 - reject_high_risk: SKIP
 - reject_high_amount: SKIP
```

Rule Matching Logic

Range conditions:

```python
if isinstance(expected, dict):
    min_val = expected.get("min")
    max_val = expected.get("max")

    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
```

Equality

```python
if value != expected:
    return False
```

Full Example Runner (examples.py)

```python
from framework import DeterministicFramework

def run_example():
    engine = DeterministicFramework(
        inputs_path="src/inputs.json",
        rules_path="src/rules.yaml"
    )

    result = engine.evaluate()

    print("=== Deterministic Framework Example ===")
    print(f"Matched rule : {result['matched_rule']}")
    print(f"Outcome      : {result['outcome']}")
    print(f"Escalation   : {result['escalation']}\n")

    print("Evaluation Trace:")
    for step in result["trace"]:
        status = "MATCH" if step["matched"] else "SKIP"
        print(f" - {step['rule']}: {status}")

if __name__ == "__main__":
    run_example()
```

## Why This Framework Matters
* Deterministic
* Explainable
* Auditable
* Beginner-friendly
* Zero AI "magic"
* Perfect for governance, compliance, and rule-based workflows

# Local AI Setup (Ollama) + Running Deterministic & AI Modes

## 1. Install Ollama

Ollama is a local LLM runtime that allows yyou to rrun models entire on yyour machine: no API keys, no cloud dependency

### macOS

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

or Install via Homebrew:

```bash
brew install ollama
```

### Windows

1. Download the installer: https://ollama.com/download
2. Run OllamaSetup.exe
3. Verify installation:

```Powershell
ollama --version
```
### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation:

```bash
ollama --version
```

## 2. Download a Model

Your AI layer requires a mode.
You can choose any model supported by Ollama.

### Recommended model for low-memory machines (4-8 GB RAM)

1. phi3 (best overall forr low memory)
2. phi3.5 (slightly better, still lightweight)
3. gemma:2B (good alternative)
4. mistral-tiny (fasted, siimplest)
5. llama3.1:3b (higher quality, still safe)

### 3. How to pull these models for Ollama

```bash
ollama pull model
```

example:

```bash
ollama pull phi3
```

If you want to see which models you have already installed run:

```bash
ollama list
```

### 4. Configure the AI Model in Code

Inside of the examply.py file set the model name to match what you installed:

for example:

```Python
ai_model = OllamaModel(model_name="phi3")
```

### 5. Running the Deterministic Framework (Article 1)

```python
python src/examples.py
```

You will see

* matched rule
* deterministic outome
* escalation
* evaluation trace (if enabled)

No AI is used in this mode.

### 6. Running Deterministic + AI Mode (Article 2)

This runs the deterministic engine plus the AI explanation layer.

```bash
python src/examples.py --ai
```

You will see:

* deterministic output
* AI explanation
* AI outcome
* matched rule
* escalation

This mode requires:

* Ollama installed
* a model downloaded
* correct model name adjusted in the examples.py
