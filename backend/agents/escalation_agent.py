
def escalation_agent(state):
    question = state["question"]
    answer = state["answer"]

    escalation_keywords = [
        "angry",
        "lawsuit",
        "legal",
        "court",
        "fraud",
        "refund immediately",
        "complaint",
        "worst service",
        "cancel subscription",
        "frustrated",
    ]

    escalate = any(
        keyword in question.lower()
        for keyword in escalation_keywords
    )

    if escalate:
        answer = (
            "Thank you for contacting support. Your message has been "
            "flagged for human review because it may require additional "
            "attention. This demonstration does not confirm that a support "
            "agent has been assigned or provide a guaranteed response time. "
            "Please use your organization's verified support channels "
            "for further assistance."
        )

    return {
        "question": question,
        "context": state.get("context", ""),
        "tool_context": state.get("tool_context", ""),
        "answer": answer,
        "route": "escalation" if escalate else state.get("route", "general"),
        "escalated": escalate,
        "email": state["email"],
        "name": state["name"],
    }