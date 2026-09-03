"""
examples.py

A simple runner script that demonstrates how to use the deterministic framework.
This file is intentionally beginner-friendly and heavily commented so that
non-technical users can run the example without touching the core engine.
"""

from deterministic.framework import DeterministicFramework
from ai.ollama_model import OllamaModel
from ai.ai_action_layer import AIActionRouter
import sys


def run_deterministic_example():
    """
    Loads the deterministic framework using the example inputs.json and rules.yaml,
    evaluates the decision, and prints the result in a readable format.
    """

    #1. Initialize the deterministic engine
    framework = DeterministicFramework(
        inputs_path="deterministic/inputs.json",
        rules_path="deterministic/rules.yaml",
    )

    #2. Evaluate the decision
    result = framework.evaluate()

    #3. Print results
    print("=== Deterministic Framework Example ===")
    print(f"Matched rule : {result['matched_rule']}")
    print(f"Outcome      : {result['outcome']}")
    print(f"Escalation   : {result['escalation']}")
    print("\nEvaluation Trace:")
    for step in result["trace"]:
        status = "MATCH" if step["matched"] else "SKIP"
        print(f" - {step['rule']}: {status}")

    return result

def run_ai_example():

    # 1. Get results from deterministic layer (article 1)
    result = run_deterministic_example()

    #2. Load AI Module(local Ollama)
    ai_model = OllamaModel(model_name="llama3.2")

    #3. Route deteministic output through AI layer
    router = AIActionRouter(ai_model)
    ai_output = router.route(result)


    #4. Print results
    print("\n=== AI Layer Output ===")
    print(f"AI Message   : {ai_output['ai_message']}")
    print(f"Outcome      : {ai_output['outcome']}")
    print(f"Matched Rule : {ai_output['matched_rule']}")
    print(f"Escalation   : {ai_output['escalation']}")

    #print("\nAI Trace:")
    #for step in ai_output["trace"]:
    #    status = "MATCH" if step["matched"] else "SKIP"
    #    print(f" - {step['rule']}: {status}")

    print("\n=== AI Explanation ===")
    print(ai_output["ai_message"])

    return ai_output


if __name__ == "__main__":

    if "--ai" in sys.argv:
        #Article 2: run ai
        run_ai_example()
    else:
        #article 1 default : run deterministic only
        run_deterministic_example()

