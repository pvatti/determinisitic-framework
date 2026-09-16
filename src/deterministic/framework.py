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
import os
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
        Deterministic inputs from JSON
        Dynamic Determinism will wrap this
        """
        if not os.path.exists(self.inputs_path):
            return {}
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
        load deterministic rules from YAML
        If thhe files does not exist, return an emmpty list
        """
        if not os.path.exists(self.rules_path):
            return []
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

        rules: List[Dict[str, Any]] = []

        for item in raw.get("rules", []):
            rule_dict = {
                "name": item.get("name", "unnamed_rule"),
                "conditions": item.get("conditions", {}),
                "outcome": item.get("outcome", "UNSPECIFIED_OUTCOME"),
                "escalation": item.get("escalation"),
                "priority": item.get("priority", 100),
            }

            rules.append(rule_dict)
        # sort rules by priority
        rules.sort(key=lambda r: (r["priority"], r["name"]))
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
        for key, expected in rule["conditions"].items():

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
    def evaluate(self, text: str = None) -> Dict[str, Any]:
        """
        Evaluates rules in deterministic order.

        Returns:
        * matched_rule: the rule that matched (or None)
        * outcome: the deterministic decision
        * escalation: esclation path if no rule matched
        * trace: full evaluation history (for auditability)

        If no rule matches, the framework escalates instad of guessing
        """

        print("DEBUG RULE NAMES:", [rule["name"] for rule in self.rules])

        trace= []
        rule_results = {}

        for rule in self.rules:
            matched = self._matches_conditions(rule, self.inputs)

            rule_results[rule["name"]] = matched

            trace.append({
                "rule": rule["name"],
                "matched" : matched
            })

            if matched:

                intent_map = {
                    "approve_low_risk": "risk",
                    "approve_existing_customer": "deadline",
                    "escalate_medium_risk": "escalate",
                    "reject_high_risk": "risk",
                    "reject_high_amount": "risk"
                }

                # Convert deterministic rule names (e.g., "deadline_rule") into the
                # simpler intent signals the agent expects (e.g., "deadline").
                # We loop through each rule result, check if it has a corresponding
                # intent name in intent_map, and build a new dictionary with the
                # translated keys and their True/False values.
                intent_results = {
                    intent_map[name]: val
                    for name, val in rule_results.items()
                    if name in intent_map
                }

                print("DEBUG (MATCHED) intent_results:", intent_results)
                print("DEBUG (MATCHED) rule_results:", rule_results)
                print("DEBUG (MATCHED) trace:", trace)
                return{
                    "matched_rule": rule["name"],
                    "outcome": rule["outcome"],
                    "escalation": rule["escalation"],
                    "trace": trace,
                    "rules": intent_results  # required for agentic layer
                }
 
        # No rule matched -> deterministic escalation
        intent_map = {
            "approve_low_risk": "risk",
            "approve_existing_customer": "deadline",
            "escalate_medium_risk": "escalate",
            "reject_high_risk": "risk",
            "reject_high_amount": "risk"
        }

        intent_results = {
            intent_map[name]: val
            for name, val in rule_results.items()
            if name in intent_map
        }

        print("DEBUG (NO MATCH) intent_results:", intent_results)
        print("DEBUG (NO MATCH) rule_results:", rule_results)
        print("DEBUG (NO MATCH) trace:", trace)

        return {
            "matched_rule": None,
            "outcome": "NO MATCH",
            "escalation": "ESCALATE_TO_REVIEW",
            "trace": trace,
            "rules": intent_results # required for agentic layer
        }

    def _compute(self) -> Dict[str, Any]:
        """
        Deterministic logic layer.
        """
        numbers = self.inputs.get("numbers", [])
        rule_results = self.evaluate_rules()

        return {
            "message": "Deterministic framework executed.",
            "value": sum(numbers),
            "rules_triggered": rule_results["matched_rules"],
        }
    
    def evaluate_rules(self) -> Dict[str, Any]:
        """
        Evaluate deterministic rules against inputs.
        """
        matched = []

        for rule in self.rules:
            if self._conditions_match(rule["conditions"]):
                matched.append(
                    {
                        "rule": rule["name"],
                        "outcome": rule["outcome"],
                        "escalation": rule["escalation"],
                    }
                )

        return {"matched_rules": matched}

    def _conditions_match(self, conditions: Dict[str, Any]) -> bool:
        """
        Core condition-matching logic.
        Every rule uses this to decide if it fires.
        """
        for key, expected_value in conditions.items():
            actual_value = self.inputs.get(key)
            if actual_value != expected_value:
                return False
        return True
    
    def run(self) -> Dict[str, Any]:
        rule_results = self.evaluate_rules()
        compute_results = self._compute()

        explanation = {
            "summary": "The deterministic engine loaded inputs and rules, evaluated all rule conditions, "
                    "triggered any matching rules, and computed a final deterministic value.",
            "inputs_summary": f"{len(self.inputs)} inputs loaded from JSON.",
            "rules_summary": f"{len(self.rules)} rules loaded from YAML.",
            "rules_triggered": (
                f"{len(rule_results['matched_rules'])} rule(s) matched: "
                + ", ".join([r['rule'] for r in rule_results['matched_rules']])
                if rule_results["matched_rules"] else "No rules matched."
            ),
            "compute_summary": (
                f"The compute layer summed the 'numbers' input to produce value={compute_results['value']}."
            )
        }
        
        return {
            "status": "success",
            "inputs_used": self.inputs,
            "rules_loaded": len(self.rules),
            "result": self._compute(),
            "explanation": explanation
        }

"""
After adding Agentic layer, it becomes Determinic + Agentic that has the following:
* A full agent - a true agentic laye
* memory tracking - stores past decisions/outcomes
* planning - decides what to do
* action - executes an action
* learn - updates strategy based on feedback

* It is important to understand that even though it is agentic, it is still following a determistic rule set that it cannot go above
"""
class Agent:

    """
    This is the REAL agentic layer:
    - memory
    - planning
    - action
    - learning
    It consumes deterministic outputs but does not change them.
    """

    def __init__(self, framework: DeterministicFramework):
        self.framework = framework
        self.memory = [] # stores past plans, actions, feedback
        self.policy = {
            "escalate": "escalate",
            "deadline": "prioritize",
            "risk": "mitigate",
            "default": "standard"
        }

    def interpret(self, deterministic_output):
        """
        Converts deterministic rule results into agentic intent
        This keeps deterministic output unchanged
        """
        triggered_rules = deterministic_output["result"].get("rules_triggered", [])
        print("AGENT RECEIVED RULES:", triggered_rules)

        if not triggered_rules:
            return "escalate"
        
        first_rule = triggered_rules[0]

        outcome = first_rule.get("outcome")
        escalation = first_rule.get("escalation")

        if escalation:
            return "escalate"
        if outcome == "APPROVE":
            return "deadline"
        if outcome == "REJECT":
            return "reject"
        if outcome == "REVIEW":
            return "review"
        return "unknown"

    def plan(self, text):
        #Run deterministic engine (no text argument anymore)
        deterministic_output = self.framework.run()
        #Interpret deterministic output
        intent = self.interpret((deterministic_output))
        #Map intent to action
        action = self.policy[intent]

        plan= {
            "intent":intent,
            "action":action,
            "deterministic_putput": deterministic_output
        }

        self.memory.append(plan)
        return plan

    def act(self, plan):
        """
        Executes the chosen action
        In a real system, this would call APIs or workflows
        """
        outcome = f"Executed: {plan['action']}"
        self.memory.append({"outcome": outcome})
        return outcome

    def learn(self, feedback):
        """
        Updates internal policy based on feedback.
        This is true agentic adaption
        """

        if "too aggresive" in feedback.lower():
            self.policy["escalate"] = "notify"
        if "too slow" in feedback.lower():
            self.policy["deadline"] = "expedite"

        self.memory.append({"feedback": feedback, "policy": dict(self.policy)})
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






