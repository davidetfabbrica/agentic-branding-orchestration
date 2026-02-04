# 🐟 Technical Specification: BrandTuna Agentic Workflow
**Status**: Proposed

**Author:** davidetfabbrica

**Date:** Feb 2026

**Stakeholders:** Engineering, UI/UX Design

## 1. Problem Statement
Traditional AI branding tools often produce "generic" results because they lack a feedback loop. A single prompt to a standard LLM cannot balance market psychology, accessibility standards, and competitive differentiation simultaneously.

BrandBot solves this by implementing an agentic "Human-in-the-loop" workflow that mimics a professional design agency's internal critique cycle.

## 2. Proposed Architecture
We will utilize a Directed Acyclic Graph (DAG) with Cyclic Loops powered by LangGraph.

### 2.1 System Diagram (Logic Flow)
Input: User provides business description + industry (e.g., Fintech, Horology).

- **Node 1:** The Strategist: Generates brand values and naming.

- **Node 2:** The Designer: Proposes visual identity (Typography, Palette).

- **Node 3:** The Critic (The Gatekeeper): * If critique_score < 8: Route back to Designer.

If critique_score >= 8: Route to Asset Producer.

- **Output:** Final Brand Bible and Visual Assets.

### 2.2 The State Object
The system maintains a global AgentState to ensure context is never lost:

```python
#python
class AgentState(TypedDict):
    industry: str
    company_description: str
    brand_identity: dict        # Names, Colors, Fonts
    critique_history: List[str] # Logs of what was rejected
    iterations: int             # Guardrail to prevent infinite loops
    is_approved: bool
```
## 3. Technology Stack Choice & Justification
| Component | Technology | Justification |
|-----------|------------|---------------|
| Orchestration | LangGraph | Supports cycles. Standard LangChain chains are linear; LangGraph allows the "Critic" to send the "Designer" back to the drawing board. |
| Reasoning Engine | GPT-4o / Claude 3.5 |High "Reasoning" capabilities required for the Critic agent to understand UI/UX heuristics.|
| Visual Engine | DALL-E 3 / Flux.1 |State-of-the-art text-to-image with strong adherence to color hex codes and layout instructions. |
| Frontend| Streamlit | Rapid prototyping for Python. Allows us to render the "Agent Thoughts" in a clean sidebar.|

## 4. Key Design Decisions (ADR)
### ADR 001: Use of Graph-Based Orchestration
- **Context:** We need a way to handle multi-turn refinements.

- **Decision:** Use LangGraph over a simple while loop.

- **Consequence:** Better observability. Each "node" in the graph can be logged and debugged independently.

### ADR 002: Separating Critique from Generation
- **Context:** LLMs struggle to be self-critical in a single pass (Self-Bias).

- **Decision:** We define a specific "Critic" persona with a separate system prompt focused strictly on "Negative Construction" and "Heuristics."

- **Consequence:** Higher quality output and more realistic "Agentic" behavior.

### ADR 003: Safety Guardrails (Iteration Cap)
- **Context:** Agents could theoretically argue forever (Infinite Loop).

- **Decision:** Implement a hard cap of 3 iterations in the Graph state.

- **Consequence:** Ensures API cost control and predictable user experience.

## 5. Test Plan
- **Unit Tests:** Validate that the Critic correctly identifies "Poor Accessibility" in a mock colour palette (e.g., White text on Yellow).

- **Integration Tests:** Ensure the State object updates correctly when moving from Designer to Critic.

- **User Acceptance:** A "Human-in-the-loop" check where the user can override the Critic's rejection.
