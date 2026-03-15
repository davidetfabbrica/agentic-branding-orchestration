# Technical Specification: BrandTuna Agentic Workflow
Status: Accepted

Author: DT

Date: March 2026

Stakeholders: Engineering, UI/UX Design

## 1. Problem Statement
Traditional AI branding tools often produce "generic" results because they lack a feedback loop. A single prompt to a standard LLM cannot balance market psychology, accessibility standards, and competitive differentiation simultaneously.

BrandTuna solves this by implementing an agentic workflow that mimics a professional design agency's internal critique cycle, using multi-agent collaboration to refine outputs.

## 2. Proposed Architecture
We utilize a Directed Acyclic Graph (DAG) with cyclic loops powered by LangGraph to allow for iterative refinement.

### 2.1 System Diagram (Logic Flow)
Input: User provides a business description.

Node 1: The Strategist: Generates brand values, names, color palettes, and typography.

Node 2: The Critic (Gatekeeper): Evaluates the output against professional standards.

If criteria are not met, provides specific "Change Orders" and routes back to The Strategist.

If criteria are met, routes to The Copywriter.

Node 3: The Copywriter: Once approved, drafts the final luxury-grade welcome announcement.

Output: A comprehensive brand_brief.md file.

### 2.2 The State Object
The system maintains a global BrandState to ensure context consistency:

```python
class BrandState(TypedDict):
    description: str
    brand_identity: str
    critique: str
    iteration_count: int
    is_approved: bool
    marketing_copy: str
```
## 3. Technology Stack Choice & Justification
| Component | Technology | Justification |
|-----------|------------|---------------|
| Orchestration | LangGraph | Supports cycles. Allows the "Critic" to send the "Strategist" back for refinement. |
| Reasoning Engine | Google Gemini | High reasoning performance with native integration via the 2026 Google GenAI SDK.|
| Resilience | Tenacity | Implements exponential backoff to handle 429 RESOURCE_EXHAUSTED errors in the free-tier environment. |
| Persistence | Markdown | Outputs final deliverables to a formatted brand_brief.md for professional review. |

## 4. Key Design Decisions (ADR)
### ADR 001: Use of Graph-Based Orchestration
- **Context:** We need to handle multi-turn refinements between specialized agents.

- **Decision:** Use LangGraph to define clear nodes and conditional edges.

- **Consequence:** Modular architecture where each agent can be updated or replaced independently.
  
### ADR 002: Separating Critique from Generation
- **Context:** LLMs struggle to be self-critical in a single pass (Self-Bias).

- **Decision:** Define a specific "Critic" persona with a prompt focused strictly on heuristic evaluation and negative construction.

- **Consequence:** Higher quality, more curated output compared to single-shot generation.

### ADR 003: Safety Guardrails (Iteration Cap)
- **Context:** Agents could theoretically loop indefinitely.
  
- **Decision:** Implement a hard cap of 3 iterations in the Graph state.

- **Consequence:** Ensures predictable completion times and stays within API usage constraints.

## 5. Test Plan
- **Unit Tests:** Validate that the Critic correctly triggers a retry if branding is deemed insufficient.

- **Integration Tests:** Ensure the BrandState dictionary passes data correctly between the Strategist, Critic, and Copywriter nodes.

- **Resilience Testing:** Verify that the tenacity decorator correctly retries requests upon encountering rate-limit errors.
