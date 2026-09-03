from typing import Dict, Any
from.ai_model_interface import AIModel

class AIActionRouter:
    """
    Routes deterministic decisions into the correct AI action.
    This layer NEVER decides, it only communicates the deterministic outcome.
    """

    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def route(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Accepts deterministic engine output and returns an AI-generated message.
        """

        outcome = decision.get("outcome")
        escalation = decision.get("escalation")
        trace = decision.get("trace", [])
        matched_rule = decision.get("matched_rule")

        if outcome == "APPROVE":
            message = self._generate_approval_message(matched_rule, trace)

        elif outcome == "REVIEW":
            message = self._generate_review_message(matched_rule, trace, escalation)

        elif outcome == "ESCALATE":
            message = self._generate_escalation_message(matched_rule, trace, escalation)

        else:
            message = self._generate_fallback_message(matched_rule, trace)

        return {
            "outcome": outcome,
            "escalation": escalation,
            "matched_rule": matched_rule,
            "trace": trace,
            "ai_message": message
        }

    # -------------------------------------------------------------------------
    # AI Prompt Generators
    # -------------------------------------------------------------------------

    def _generate_approval_message(self, matched_rule: str, trace: Any) -> str:
        prompt = (
            "You are an assistant generating a clear, concise approval message.\n\n"
            f"Decision outcome: APPROVE\n"
            f"Matched rule: {matched_rule}\n"
            f"Evaluation trace: {trace}\n\n"
            "Write a short message explaining that the request was approved and why."
        )
        return self.ai_model.generate(prompt)

    def _generate_review_message(self, matched_rule: str, trace: Any, escalation: str) -> str:
        prompt = (
            "You are an assistant generating a message for a request under review.\n\n"
            f"Decision outcome: REVIEW\n"
            f"Matched rule: {matched_rule}\n"
            f"Escalation path: {escalation}\n"
            f"Evaluation trace: {trace}\n\n"
            "Write a short message explaining that the request is being reviewed "
            "and what happens next."
        )
        return self.ai_model.generate(prompt)

    def _generate_escalation_message(self, matched_rule: str, trace: Any, escalation: str) -> str:
        prompt = (
            "You are an assistant generating a message for a request requiring escalation.\n\n"
            f"Decision outcome: ESCALATE\n"
            f"Matched rule: {matched_rule}\n"
            f"Escalation path: {escalation}\n"
            f"Evaluation trace: {trace}\n\n"
            "Write a short message explaining that additional verification is required "
            "without promising an outcome."
        )
        return self.ai_model.generate(prompt)

    def _generate_fallback_message(self, matched_rule: str, trace: Any, escalation: str) -> str:
        prompt = (
            "You are an assistant generating a message for a request requiring escalation.\n\n"
            f"Decision outcome: ESCALATE\n"
            f"Matched rule: {matched_rule}\n"
            f"Escalation path: {escalation}\n"
            f"Evaluation trace: {trace}\n\n"
            "Write a short message explaining that additional verification is required "
            "without promising an outcome."
        )
        return self.ai_model.generate(prompt)
    