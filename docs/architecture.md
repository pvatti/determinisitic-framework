## Determinstic Framework Architecture

A clear, auditable, beginner-friendly rule engine built on explicit YAML rules and JSON inputs. This document explains the internal architecture, design principles, and evaluation flow of the system.

## 1. System Overview

The deterministic Framework is a lightweight rule-evaluation engine that produces predictable outcomes based on structured inputs and explicit rule definitions. It is designed for:

* **Determinism** - same inputs always produce the same outputs
* **Explainable** - every decision is logged
* **Auditability** - full evaluation trace
* **Beginner-Friendly usage** - readable YAML + simple Python

This framework does **not** use machine learning, inference, or probability. 
It is intentionlly explicit and rule-driven.

## 2. Core Principles

**Determinism**

Every evaluation follows the same ordered rule list.
No randomness, no probability, no inference.

**Explicitness**

Rules re defined in YAML using simple condition types.
Inputs are JSON.
No hidden logic.

**Tracability**

Every rule evaluation is logged in a trace list showing:

* rule name
* whether it matched

**Auditability**

The engine returls:

* matched rule
* outcome
* esclation
* full trace

This makes decisions easy to inspect and verify.

**Beginner-Friendly**

The architecture avoid complexity

* no Domain-Specific Language
* no custom syntax
* no opaque abstraction

Just YAML --> Pythin --> output

## 3. High Level Architecture Diagram

+------------------+
|   inputs.json    |
+------------------+
          |
          v
+---------------------------+
| DeterministicFramework    |
| - loads inputs            |
| - loads rules             |
| - sorts by priority       |
+---------------------------+
          |
          v
+------------------+
|   rules.yaml     |
+------------------+
          |
          v
+----------------------------------+
| Rule Evaluation Engine           |
| - condition checking             |
| - range & equality logic         |
| - trace logging                  |
| - first-match wins               |
+----------------------------------+
          |
          v
+----------------------------------+
| outcome + escalation + trace     |
+----------------------------------+

## 4. Rule Model

Each rule in rules.yaml maps directly to a Python Rule object.

### Rule Fields

* **name** - unique identifiers
* **priority** - lower numbers evaluated first
* **conditions** - equality or range checks
* **outcome** - retuned when rule matches
* **escalation** - optional escalation path

Example:

```yaml
- name: escalate_medium_risk
  priority: 3
  conditions:
    risk_score:
      min: 11
      max: 20
  outcome: REVIEW
  escalation: ESCALATE_TO_MANAGER
```

## 5. Condition Types

The framework supports two condition types:

### Equality Conditions

Used for booleans, strings, or exact matches.

```yaml
existing_customer: true
```

### Range Conditions

Used for numeric comparisons.
* min onlyy
* max only
* both min and max

## 6. The Evaluation Flow

The valuation algorithm is simple and deterministic:

### Step-by-step flow

1. Load inputs from JSON
2. Load rules from YAML
3. Short rules by priority
4. For each rule:
    * Check all conditions
    * Append trace entry
    * If matched --> return immediately
5. If no rule matches:
    * return deterministic fallback outcome
    * include full trace

### Pseudocode

```python
for rule in rules:
    matched = matches(rule, inputs)
    trace.append({rule, matched})
    if matched:
        return result
return no_match_result
```

This ensures:
* predictable behavior
* first-match-wins
* full trace logging

## 7. Condition Matching Logic

### Range Matching

```Python
if expected is a dict:
    if min exists and value < min → fail
    if max exists and value > max → fail
```

### Equality Matching

```Python
if expected is not a dict:
    if value != expected → fail
```

All conditions must pass for a rule to match

## 8. Trace Logging

Trace entries are appended for **every rule**, regardless of match outcome.

Example trace:
```json
[
  {"rule": "approve_low_risk", "matched": false},
  {"rule": "approve_existing_customer", "matched": true}
]
```

Trace is essential for:
* debugging
* auditing
* governance
* explainability

## 9. Error Handling Philosophy

The frameworks strict deterministic error handling:

### Missing Fields:

If an input field is missing --> rule fails

### Type Mismatches

If a value cannot be compate (e.g., "12" vs min: 11) --> rule fails

### Malformed YAML

Invalid rule defintion cause load-time errors.

### Invalid Condition Types

Unsupported condition structures fail last.
This ensures predictable behavior and avoids silent failures.

## 10. Extensibility

The architecture is intentionally simple so contributors can extend it easily.

### Possible extensions:

* new condition types (e.g.,in, not, contains)
* rule groups
* rule conflict detection
* rule coverage analysis
* explainability ("this rule matches because...")
* typed schemas for inputs

Each extension should preserve:

* determinism
* traceability
* explicitness

## 11. Non-Goals

This framework intentionally avoids:

* machine learning
* inference
* probability
* fuzzy matching
* NLP
* "best guess" logic
* dynamic rule generation

This is a **deterministic** engine - not an AI model.

## 12. Related Docs

* README - usage, examples, quickstart
* Rule Design Guide - how to write good rules
* Trce Guide - how trace works

