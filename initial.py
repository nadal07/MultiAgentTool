from langgraph.graph import StateGraph, END

# State keys
state = {
    "user_input": str,
    "application_area": str,
    "response": str
}

def main_agent(state):
    user_input = state["user_input"]
    print("Main Agent received:", user_input)
    # Let RAG Tool handle this
    return {"user_input": user_input}


def rag_tool(state):
    user_input = state["user_input"]
    # Simulate classification (replace with actual RAG logic)
    if "balance" in user_input or "account" in user_input:
        area = "account"
    elif "flight" in user_input or "booking" in user_input:
        area = "travel"
    else:
        area = "general"
    return {"application_area": area}

def account_agent(state):
    return {"response": f"Account Agent handling: {state['user_input']}"}

def travel_agent(state):
    return {"response": f"Travel Agent handling: {state['user_input']}"}

def fallback_agent(state):
    return {"response": f"No specific domain. General response: {state['user_input']}"}

builder = StateGraph(state)

builder.add_node("main_agent", main_agent)
builder.add_node("rag_tool", rag_tool)
builder.add_node("account_agent", account_agent)
builder.add_node("travel_agent", travel_agent)
builder.add_node("fallback_agent", fallback_agent)

# Edge definitions
builder.set_entry_point("main_agent")
builder.add_edge("main_agent", "rag_tool")

def router(state):
    area = state["application_area"]
    if area == "account":
        return "account_agent"
    elif area == "travel":
        return "travel_agent"
    else:
        return "fallback_agent"

builder.add_conditional_edges("rag_tool", router)
builder.add_edge("account_agent", END)
builder.add_edge("travel_agent", END)
builder.add_edge("fallback_agent", END)

graph = builder.compile()


input_text = "I want to check my account balance"
result = graph.invoke({"user_input": input_text})
print(result["response"])
