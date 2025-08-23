# Ready Tensor Agentic AI Certification – Week 5

This repository contains lesson materials, code examples, reference scripts for **Week 5** of the [Agentic AI Developer Certification Program](https://app.readytensor.ai/publications/HrJ0xWtLzLNt) by Ready Tensor. This week marks the transition from traditional prompt pipelines to building **agent-based AI systems** using tools like **LangGraph**, **LangChain**, and **LangSmith**.

---

## What You'll Learn

- When to use workflows vs. agents
- How to build and run LangGraph projects
- How to trace and debug agentic flows with LangSmith
- How to integrate tools — both built-in and custom — into agent loops
- How to manage shared state and node-level behavior in LangGraph

---

## Lessons in This Repository

### 1. From Workflows to Agents: When Predictable Paths Aren’t Enough

Learn when and why to move beyond static LLM workflows toward more flexible, adaptive agentic systems.

### 2a. Building Agentic Systems at Scale: An Introduction to LangGraph

Get introduced to LangGraph — a framework for designing agentic flows as graphs of nodes, edges, and state — built for scalability and control.

### 2b. Your First LangGraph Project: Building a Joke Bot

Build a simple, non-LLM LangGraph joke bot to learn about graph structure, state objects, and routing logic.

### 2c. Agentic AI With LangGraph: Building a Writer–Critic Loop

Enhance your joke bot with LLMs and a writer–critic architecture. The agent generates, evaluates, and refines its output before sharing it with the user.

### 3. Inside the Mind of an Agent: Observability with LangSmith

Use LangSmith to trace every step of your agent's process — from LLM calls to tool usage — with full visibility into the graph’s state transitions.

### 4a. Beyond Conversation: Giving Your AI Agent the Power of Tools

Integrate built-in tools into your LangGraph workflow and design a **Think–Act–Think** loop. Let your agent retrieve real data and make decisions dynamically.

### 4b. Custom Tools, Custom Powers: Extending Your Agent’s Capabilities

Build your own tools from scratch and register them with your agent. Extend functionality in ways that suit your own domain or product use case.

---

## Repository Structure

```txt
rt-agentic-ai-cert-week5/
├── code/
│   ├── custom_tools.py                         # Custom tool implementations for Lesson 3b
│   ├── llm.py                                  # LLM utility wrapper
│   ├── paths.py                                # Standardized file path management
│   ├── prompt_builder.py                       # Modular prompt construction functions
│   ├── run_wk5_l2b_pyjokes_joke_bot.py         # Lesson 2b: Run joke-bot using pyjokes
│   ├── run_wk5_l2c_llm_joke_bot.py             # Lesson 2c: Run joke-bot using ai agents
│   ├── run_wk5_l4b_custom_tools.py             # Lesson 4b: Run agent with custom tools
│   └── utils.py                                # Common utilities
├── config/
│   ├── config.yaml                             # Configuration file for tool registration or agent setup
│   └── prompt_config.yaml                      # Prompt configurations for agents
├── lessons/                                    # Lesson content and images
├── outputs/
│   └── graph.png                               # Example LangGraph visualization
├── .env.example                                # Sample environment variable file (e.g., Groq API key)
├── .gitignore
├── LICENSE
├── README.md                                   # You are here
└── requirements.txt                            # Required Python dependencies
```

---

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/readytensor/rt-agentic-ai-cert-week5.git
   cd rt-agentic-ai-cert-week5
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**

   Copy the `.env.example` to `.env` and update the values (e.g., Groq API key):

   ```bash
   cp .env.example .env
   ```

   You can get your API key from [Groq](https://console.groq.com/).

---

## License

This project is licensed under the CC BY-NC-SA 4.0 License – see the [LICENSE](LICENSE) file for details.

---

## Contact

**Ready Tensor, Inc.**

- Email: contact at readytensor dot com
- Issues & Contributions: Open an issue or PR on this repo
- Website: [https://readytensor.ai](https://readytensor.ai)
