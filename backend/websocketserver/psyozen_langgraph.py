from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from psyozen_agent import process_input, should_continue, generate_recommendation

# Define the state schema
class ChatState(TypedDict):
    summary: str
    last_response: str
    conversation: list

workflow = StateGraph(state_schema=ChatState)

workflow.add_node("process_input", process_input)
workflow.add_node("should_continue", should_continue)
workflow.add_node("generate_recommendation", generate_recommendation)


#Use add_edge_with_condition for branching
workflow.set_entry_point("process_input")
workflow.add_edge("process_input", "should_continue")
workflow.add_conditional_edges(
    "should_continue",
    {
        "process_input": process_input,
        "generate_recommendation": generate_recommendation
    }
)

workflow.set_finish_point("generate_recommendation")
#workflow.add_edge("process_input", "should_continue")
#workflow.add_edge("should_continue", "process_input")
#workflow.add_edge("should_continue", "generate_recommendation")

#llm agent
#Compile langgraph config

# Compile the graph
app2 = workflow.compile()