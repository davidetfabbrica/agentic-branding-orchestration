import os
import warnings
from typing import TypedDict
from dotenv import load_dotenv
from google import genai
from langgraph.graph import StateGraph, END
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Silence warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Configuration
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-flash-latest"

# 1. State Schema
class BrandState(TypedDict):
    description: str
    brand_identity: str
    critique: str
    iteration_count: int
    is_approved: bool
    marketing_copy: str

# 2. Agent Definitions with Retry Logic
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def strategist_agent(state: BrandState):
    print(f"\n🎨 [STRATEGIST]: Processing round {state.get('iteration_count', 0) + 1}...")
    prompt = f"Role: Brand Strategist. Create a name, hex colors, and typography for: {state['description']}. Feedback to address: {state.get('critique', 'None')}"
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return {"brand_identity": response.text, "iteration_count": state.get("iteration_count", 0) + 1}

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def critic_agent(state: BrandState):
    print("🔍 [CRITIC]: Reviewing branding...")
    prompt = f"Role: Design Critic. Review this: {state['brand_identity']}. Start response with 'APPROVED' if ready, otherwise give Change Orders."
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    feedback = response.text
    return {"critique": feedback, "is_approved": feedback.strip().upper().startswith("APPROVED")}

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def copywriter_agent(state: BrandState):
    print("✍️ [COPYWRITER]: Writing launch copy...")
    prompt = f"Role: Luxury Copywriter. Write a 3-sentence welcome email and tagline for: {state['brand_identity']}."
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    return {"marketing_copy": response.text}

# 3. Workflow
workflow = StateGraph(BrandState)
workflow.add_node("strategist", strategist_agent)
workflow.add_node("critic", critic_agent)
workflow.add_node("copywriter", copywriter_agent)

workflow.set_entry_point("strategist")
workflow.add_edge("strategist", "critic")

def router(state: BrandState):
    return "proceed" if state["is_approved"] or state["iteration_count"] >= 3 else "refine"

workflow.add_conditional_edges("critic", router, {"proceed": "copywriter", "refine": "strategist"})
workflow.add_edge("copywriter", END)
app = workflow.compile()

# 4. Execution
if __name__ == "__main__":
    print("🚀 BrandTuna Agency Online...")
    state = {"description": "Luxury watch marketplace", "iteration_count": 0, "is_approved": False, "brand_identity": "", "critique": "", "marketing_copy": ""}
    
    final_state = state
    for event in app.stream(state):
        for node, data in event.items():
            final_state.update(data)
            
    if final_state.get("marketing_copy"):
        with open("brand_brief.md", "w") as f:
            f.write(f"# Brand Brief: {final_state['description']}\n\n{final_state['brand_identity']}\n\n## Launch Copy\n{final_state['marketing_copy']}")
        print("\n✨ SUCCESS! Saved to brand_brief.md")
