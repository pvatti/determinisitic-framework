from deterministic.framework import DeterministicFramework

class DynamicDeterminism:
    def __init__(self, inputs_path: str, rules_path:str):
        self.engine = DeterministicFramework(inputs_path, rules_path)

    def run(self):
        base_output = self.engine.run()

        dynamic_explanation = {
            "summary": "Dynamic determinism layer executed after deterministic engine.",
            "purpose": "Adds adaptive logic, meta-analysis, and contextual interpretation.",
            "base_value": base_output["result"]["value"],
            "additional_logic": "Dynamic layer counted inputs and added contextual metadata."
        }
        return {
            "dynamic_layer": "active",
            "base_result": base_output,
            "dynamic_explanation": dynamic_explanation,
            "additional_logic": self._dynamic_logic(base_output)
        }

    def _dynamic_logic(self, base_output):
        return {
            "message": "Dynamic determinism executed.",
            "input_count": len(base_output.get("inputs_used", {}))
        }
