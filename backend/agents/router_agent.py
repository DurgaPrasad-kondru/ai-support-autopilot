def router_agent(state):

    question = state["question"]

    if "refund" in question.lower():

        route = "billing"

    elif "payment" in question.lower():

        route = "billing"

    elif "error" in question.lower():

        route = "technical"

    else:

        route = "general"

    return {

        "route": route,
        "question": state["question"],
        "email": state["email"],
        "name": state["name"]

    }