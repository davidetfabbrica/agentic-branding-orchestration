# BrandTuna Agency 🐟
**An Autonomous Multi-Agent Branding System powered by Gemini & LangGraph.**

BrandTuna is a multi-agent AI system that simulates a professional creative agency. It streamlines the branding process by orchestrating specialized AI "agents" that collaborate, critique, and refine brand identities until they meet high-end UI/UX standards.

## 🛠️ The Architecture
BrandTuna uses an **Agentic Workflow** built with **LangGraph**. Instead of a simple prompt-response chain, the system features a recursive loop where agents check each other's work:

1. **The Strategist:** Generates initial brand concepts, color palettes, and typography.
2. **The Critic:** Acts as a design gatekeeper, enforcing professional standards and providing "Change Orders."
3. **The Copywriter:** Once the Critic approves the identity, this agent generates high-end launch copy.

## 🚀 Key Engineering Features
* **Resilient Multi-Agent Loop:** Uses `LangGraph` to manage state transitions between agents.
* **Intelligent Error Handling:** Implemented `Tenacity` with exponential backoff to handle API rate limits (`429 RESOURCE_EXHAUSTED`) gracefully.
* **Automated Deliverables:** Instead of just terminal output, the system programmatically generates a formatted `brand_brief.md` file for stakeholders.
* **Cutting-Edge Stack:** Built using the 2026 Google Gemini GenAI SDK and Python 3.14.

## 📦 How to Run
1. **Clone the repo:** `git clone [your-repo-link]`
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Configure:** Create a `.env` file with your `GOOGLE_API_KEY`.
4. **Execute:** `python3 app.py`

## 📊 Example Output
Upon completion, the system generates a `brand_brief.md` file containing the final identity and the Critic's notes.
*View an example output in the [/examples](/examples) folder.*

---
*Built for the 2026 AI Developer landscape.*
