import os
import warnings
# Suppress the Python 3.14 / Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from google import genai
from typing import TypedDict, Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# --- 1. CONFIGURATION ---
load_dotenv()

# Initialize without the http_options override to let the SDK choose the best path
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Using the specific versioned ID from your list
MODEL_ID = "gemini-flash-latest"

# --- 2. THE STATE DEFINITION ---
class BrandState(TypedDict):
    description: str
    brand_identity: str
    critique: str
    iteration_count: int
    is_approved: bool

# --- 3. AGENT: THE STRATEGIST ---
def strategist_agent(state: BrandState):
    print(f"\n🎨 [STRATEGIST]: Processing iteration {state.get('iteration_count', 0) + 1}...")
    
    critique_context = ""
    if state.get("critique"):
        critique_context = f"\nREFINEMENT NEEDED: {state['critique']}"

    prompt = f"""
    You are a Lead Brand Strategist. 
    Topic: {state['description']}
    {critique_context}
    
    Provide a Brand Name, a 3-color Hex Palette, and a Typography recommendation.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    
    return {
        "brand_identity": response.text,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

# --- 4. AGENT: THE CRITIC ---
def critic_agent(state: BrandState):
    print("🔍 [CRITIC]: Reviewing branding against UI/UX standards...")
    
    prompt = f"""
    You are a Senior Design Critic. Review this branding:
    {state['brand_identity']}
    
    If it fits the luxury/professional vibe and is UI-ready, you MUST start your response with the single word 'APPROVED'.
    Otherwise, give specific 'Change Orders'.
    """
    
    response = client.models.generate_content(model=MODEL_ID, contents=prompt)
    feedback = response.text
    
    # We use .strip() to remove any hidden spaces or newlines before checking
    is_approved = feedback.strip().upper().startswith("APPROVED")
    
    return {"critique": feedback, "is_approved": is_approved}

# --- 5. THE GRAPH ORCHESTRATION ---
workflow = StateGraph(BrandState)

workflow.add_node("strategist", strategist_agent)
workflow.add_node("critic", critic_agent)

workflow.set_entry_point("strategist")
workflow.add_edge("strategist", "critic")

def router_logic(state: BrandState):
    # Stop if approved or if we've tried 3 times
    if state["is_approved"] or state["iteration_count"] >= 3:
        return "end"
    return "refine"

workflow.add_conditional_edges(
    "critic", 
    router_logic, 
    {"end": END, "refine": "strategist"}
)

brand_tuna_app = workflow.compile()

# --- 6. RUN THE CANNING LINE ---
if __name__ == "__main__":
    print(f"🚀 BrandTuna is online using {MODEL_ID}...")
    
    initial_input = {
        "description": "A luxury watch marketplace for high-end collectors.",
        "iteration_count": 0,
        "is_approved": False
    }
    
    # This dictionary will hold the "Full Picture" as it evolves
    full_state = initial_input.copy()

    for event in brand_tuna_app.stream(initial_input):
        for node, data in event.items():
            # Update our full_state with whatever the latest node just produced
            full_state.update(data)
            
            if node == "critic":
                status = "✅ APPROVED" if data.get('is_approved') else "❌ REJECTED"
                print(f"Result: {status}")
                print(f"Feedback: {data.get('critique', '')[:100]}...")

    # --- 7. EXPORT TO PORTFOLIO ---
    # Now we check our accumulated 'full_state'
    if full_state.get("is_approved"):
        filename = "brand_brief.md"
        with open(filename, "w") as f:
            f.write(f"# BrandTuna Brief: {full_state['description']}\n\n")
            f.write("## Final Identity\n")
            f.write(full_state.get("brand_identity", "No identity generated."))
            f.write("\n\n---\n")
            f.write("## Critic's Final Review\n")
            f.write(full_state.get("critique", "No critique provided."))
        
        print(f"\n✨ SUCCESS! Your brand brief has been saved to: {filename}")