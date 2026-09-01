"""
framework.py

A simple determintistic framework that:
* loads inputs from JSON
* loads rules from YAML
* evaluates conditions in a predictable order
* returns a decision or escalates if no rule matches

* This file is intentionally simple and heavily commented so that non-technial people readers can understand how deterministic logic works
"""

# import statement for packes the file will be using
import json
import yaml
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# ------------------------------------------------------------
# Rule Model
# ------------------------------------------------------------
@dataclass
class Rule:
    """
    This represents a single deterministic rule.

    Each rule has:
    * name: readable identifier
    * conditions: what must be true for the rule to match
    * outcome: the deterministic decision if matched
    * escalation: optional excalation path
    * priority: lower numbers are evaluated first (deterministic ordering)
    """
    name: str
    conditions: Dict[str, Any]
    outcome: str
    escalation: Optional[str] = None
    priority: int = 100 # lower = evaluated earlier

# ------------------------------------------------------------
# Deterministic Framework Engine
# ------------------------------------------------------------
class DeterministicFramework:
    """
    Loads inputs + rules, evaluates them deterministically, and returns a preictable decision.
    """
    def __init__(self, inputs_path: str, rules_path: str):
        self.inputs_path = inputs_path
        self.rules_path = rules_path

        #load inputs and rules at initiatlization
        self.inputs = self._load_inputs()
        self.rules = self._load_rules()

    # --------------------------------------------------------
    # Load Inputs
    # --------------------------------------------------------
    def _load_inputs(self) -> Dict[str, Any]:
        """
        Loads the input data from a JSON file

        This file represents the "scenario" the user wants to evaluate
        Example:
        {
            "age":34,
            "income": 72000,
            "risk_score": 12   
        }

        This framework does NOT guess or infer anything
        It only uses what is explicitly provided
        """
        with open(self.inputs_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # --------------------------------------------------------
    # Load Rules
    # --------------------------------------------------------

    def _load_rules(self) -> List[Rule]:
        """
        Loads deterministic rules from a YAML file.

        YAML is used because:
        * it's readable for none-technial users
        * it's easy to edit
        * it supports nested structures (like min/max ranges)

        After loading, rules are sorted by priority so evaluation order is always predictable
        """
        with open(self.rules_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        rules: List[Rule] = []

        for item in raw.get("rules", []):
            rules.append(
                Rule(
                    name=item.get("name", "unnamed_rule"),
                    conditions=item.get("conditions", {}),
                    outcome=item.get("outcome", "UNSPECIFIED_OUTCOME"),
                    escalation=item.get("escalation"),
                    priority=item.get("priority", 100),
                )
            )

        rules.sort(key=lambda r: (r.priority, r.name))
        return rules


    # --------------------------------------------------------
    # Condition Matching
    # --------------------------------------------------------
    def _matches_conditions(self, rule: Rule, inputs: Dict[str, Any]) -> bool:
        """
        Checks whether the input data satisfies the rule's conditions

        Supports two types of conditions:
        1. Direct equality:
            age: 30 -> input["age"] must equal 30
        
        2. Range conditions:
            risk_score:
                min:10
                max: 20
            -> input["risk_score"] must be between 10 and 20

        No guessing. No probability. No inference.
        Everything is explicit and deterministic
        """
        for key, expected in rule.conditions.items():

            value = inputs.get(key)
            if value is None:
                return False
            
            #Range-style conditions: {min X, max Y}
            if isinstance(expected, dict):
                min_val = expected.get("min")
                max_val = expected.get("max")

                if min_val is not None and value < min_val:
                    return False
                if max_val is not None and value > max_val:
                    return False

            # Direct equality
            else:
                if value != expected:
                    return False

        return True

    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------
    def evaluate(self) -> Dict[str, Any]:
        """
        Evaluates rules in deterministic order.

        Returns:
        * matched_rule: the rule that matched (or None)
        * outcome: the deterministic decision
        * escalation: esclation path if no rule matched
        * trace: full evaluation history (for auditability)

        If no rule matches, the framework escalates instad of guessing
        """
        trace= []

        for rule in self.rules:
            matched = self._matches_conditions(rule, self.inputs)

            trace.append({
                "rule": rule.name,
                "matched" : matched
            })

            if matched:
                return{
                    "matched_rule": rule.name,
                    "outcome": rule.outcome,
                    "escalation": rule.escalation,
                    "trace": trace
                }
 
            # No rule matched -> deterministic escalation
        return {
            "matched_rule": None,
            "outcome": "NO MATCH",
            "escalation": "ESCALATE_TO_REVIEW",
            "trace": trace
        }

# ------------------------------------------------------------
# CLI Runner
# ------------------------------------------------------------
def main():
    """
    Allows users to run the deterministic framework directly
    from the commange line:

        python frame.py
    
    This loads inputs.json + rules.yaml and prints the result.
    """
    framework = DeterministicFramework(
        inputs_path="inputs.json",
        rules_path="rules.yaml"
    )
    result = framework.evaluate()

    print("=== Deterministic Decision Result ===")
    print(f"Matched rule: {result['matched_rule']}")
    print(f"Outcome     : {result['outcome']}")
    print(f"Escalation  : {result['escalation']}")
    print("\nTrace (evaluation order):")

    for step in result["trace"]:
        status = "MATCH" if step["matched"] else "SKIP"
        print(f" - {step['rule']}: {status}")

if __name__ == "__main__":
    main()






