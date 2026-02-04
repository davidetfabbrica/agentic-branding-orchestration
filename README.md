# BrandTuna: An Agentic Design & Branding Orchestrator

BrandTuna is a multi-agent system built with **LangGraph** that automates the end-to-end branding process. It transforms a simple business idea into a refined visual identity through an iterative "Creative-Critique" loop.

## 🚀 Overview
Most AI branding tools are "one-shot"—you get what you get. BrandTuna mimics a professional design agency by employing distinct agents that debate, critique, and refine concepts based on UI/UX heuristics, psychology, and market positioning.

## 🧠 The Agentic Workflow
This project utilizes a **Stateful Graph** architecture:
1.  **The Strategist:** Defines the brand persona and naming.
2.  **The Designer:** Prototypes visual styles and color palettes.
3.  **The Critic:** An autonomous evaluator that checks the work against accessibility standards (WCAG), color psychology, and competitor saturation.
4.  **The Refiner:** Adjusts the output based on the Critic’s feedback.
5.  **The Producer:** Generates the final "Brand Bible" and asset suite.

## 🛠️ Tech Stack
* **Orchestration:** [LangGraph](https://www.langchain.com/langgraph) (for stateful, cyclic multi-agent flows)
* **LLM:** GPT-4o or Claude 3.5 Sonnet (for reasoning and critique)
* **Image Generation:** DALL-E 3 / Flux (via API for prototyping)
* **Interface:** Streamlit or Next.js (for the real-time agent "thought" display)
* **Language:** Python 3.11+

## 📈 Key Portfolio Highlights
* **Cyclic Graphs:** Implementation of a "Critic-Loop" that prevents hallucinations and improves quality.
* **Domain-Specific Logic:** Encoded UI/UX heuristics and psychological principles into agent personas.
* **State Management:** Handling shared memory across multiple agents to maintain brand consistency.
