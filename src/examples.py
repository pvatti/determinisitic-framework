"""
examples.py

A simple runner script that demonstrates how to use the deterministic framework.
This file is intentionally beginner-friendly and heavily commented so that
non-technical users can run the example without touching the core engine.
"""

from deterministic.framework import DeterministicFramework


def run_example():
    """
    Loads the deterministic framework using the example inputs.json and rules.yaml,
    evaluates the decision, and prints the result in a readable format.
    """

    # Initialize the deterministic engine
    framework = DeterministicFramework(
        inputs_path="src/inputs.json",
        rules_path="src/rules.yaml",
    )

    # Evaluate the decision
    result = framework.evaluate()

    # Print results
    print("=== Deterministic Framework Example ===")
    print(f"Matched rule : {result['matched_rule']}")
    print(f"Outcome      : {result['outcome']}")
    print(f"Escalation   : {result['escalation']}")
    print("\nEvaluation Trace:")
    for step in result["trace"]:
        status = "MATCH" if step["matched"] else "SKIP"
        print(f" - {step['rule']}: {status}")


if __name__ == "__main__":
    run_example()
