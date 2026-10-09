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
        "frustrated"

    ]

    escalate = any(

        keyword in question.lower()

        for keyword in escalation_keywords

    )

    if escalate:

        escalation_message = """
Dear Customer,
Thank you for contacting Support. We've received your query and our AI system has identified this as a priority case requiring personal attention from our team.
A dedicated support executive has been assigned to your ticket and will reach out to you within 30 minutes during business hours (9 AM – 9 PM IST).
If you need immediate assistance, you can also reach us at:
📞 1800-123-4567 (Toll-Free, Mon–Sun)
💬 WhatsApp: +91-98765-43210
📧 support@rtshop.in
We sincerely apologise for any inconvenience and assure you this will be resolved on priority.
Warm regards,
ShopEase Customer Support Team

"""

        answer = escalation_message

        return {

            "question": state["question"],
            "context": state.get("context", ""),
            "tool_context": state.get("tool_context", ""),
            "answer": answer,
            "route": "escalation",
            "escalated": True,
            "email": state["email"],
            "name": state["name"]

        }

    return {

        "question": state["question"],
        "context": state.get("context", ""),
        "tool_context": state.get("tool_context", ""),
        "answer": answer,
        "route": state.get("route", "general"),
        "escalated": False,
        "email": state["email"],
        "name": state["name"]

    }