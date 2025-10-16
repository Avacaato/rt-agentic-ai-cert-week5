from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from run_wk5_l2b_pyjokes_joke_bot import (
    Joke,
    JokeState,
    show_menu,
    exit_bot,
    route_choice,
    reset_jokes,
    update_language,
    print_joke,
)
from prompt_builder import build_prompt_from_config
from utils import load_config
from difflib import SequenceMatcher
from llm import get_llm
from paths import PROMPT_CONFIG_FILE_PATH

# ========== Extended State ==========


class AgenticJokeState(JokeState):
    latest_joke: str = ""
    approved: bool = False
    retry_count: int = 0
    critic_type: str = "llm"


# ========== Prompt Config ==========

prompt_cfg = load_config(PROMPT_CONFIG_FILE_PATH)

# ========== Writer–Critic Node Factories ==========

def update_critic_type(state: AgenticJokeState) -> dict:
    print("select critic type:")
    print("    0. LLM Critic")
    print("    1. Human Critic")
    selection = input("Enter choice (0 or 1): ").strip()
    if selection == "1":
        print("    ✅ Critic type set to Human Critic")
        return {"critic_type": "human"}
    else:
        print("    ✅ Critic type set to LLM Critic")
        return {"critic_type": "llm"}


def is_similar(joke1, joke2, threshold=0.7):
    """Check if two jokes are similar based on a similarity threshold."""
    return SequenceMatcher(None, joke1, joke2).ratio() > threshold

def make_writer_node(writer_llm):
    def writer_node(state: AgenticJokeState) -> dict:
        config = prompt_cfg["joke_writer_cfg"]
        prompt = build_prompt_from_config(config, input_data="", app_config=None)
        prompt += f"\n\nThe category is: {state.category}"

        max_attempts = 5
        for _ in range(max_attempts):
            response = writer_llm.invoke(prompt)
            candidate_joke = response.content

            if any(is_similar(prev_joke.text, candidate_joke) for prev_joke in state.jokes):
                print("   ⚠️ Similar joke detected. Generating a new one...")
                continue  # Try next attempt
            else:
                print("   ✅ New joke generated.")
                return {"latest_joke": candidate_joke}

        # After max retries
        return {"latest_joke": "Failed to generate a unique joke after several attempts."}

    return writer_node


def make_critic_node(critic_llm):
    def critic_node(state: AgenticJokeState) -> dict:
        if state.critic_type == "human":
            print(f"\n👉 joke for approval:\n{state.latest_joke}\n")
            user_input = input("Do you approve this joke? (y/n): ").strip().lower()
            approved = user_input == "y"
            return {"approved": approved, "retry_count": state.retry_count + 1}
        
        config = prompt_cfg["joke_critic_cfg"]
        prompt = build_prompt_from_config(config, input_data=state.latest_joke, app_config=None)
        decision = critic_llm.invoke(prompt).content.strip().lower()
        approved = "yes" in decision
        return {"approved": approved, "retry_count": state.retry_count + 1}
    
    return critic_node

def show_final_joke(state: AgenticJokeState) -> dict:
    joke = Joke(text=state.latest_joke, category=state.category)
    print_joke(joke, approved=state.approved)
    return {"jokes": [joke], "retry_count": 0, "approved": False, "latest_joke": ""}


def writer_critic_router(state: AgenticJokeState) -> str:
    if state.approved or state.retry_count >= 5:
        return "show_final_joke"
    return "writer"


def update_category(state: AgenticJokeState) -> dict:
    categories = ["dad developer", "chuck norris developer", "general"]
    emoji_map = {
        "knock-knock": "🚪",
        "dad developer": "👨‍💻",
        "chuck norris developer": "🥋",
        "general": "🎯",
    }

    print("📂" + "=" * 58 + "📂")
    print("    CATEGORY SELECTION")
    print("=" * 60)

    for i, cat in enumerate(categories):
        emoji = emoji_map.get(cat, "📂")
        print(f"    {i}. {emoji} {cat.upper()}")

    print("=" * 60)

    try:
        selection = int(input("    Enter category number: ").strip())
        if 0 <= selection < len(categories):
            selected_category = categories[selection]
            print(f"    ✅ Category changed to: {selected_category.upper()}")
            return {"category": selected_category}
        else:
            print("    ❌ Invalid choice. Keeping current category.")
            return {}
    except ValueError:
        print("    ❌ Please enter a valid number. Keeping current category.")
        return {}


# ========== Graph Assembly ==========


def build_joke_graph(
    writer_model: str = "sonar",
    critic_model: str = "sonar",
    writer_temp: float = 0.95,
    critic_temp: float = 0.1,
) -> CompiledStateGraph:

    writer_llm = get_llm(writer_model, writer_temp)
    critic_llm = get_llm(critic_model, critic_temp)

    builder = StateGraph(AgenticJokeState)

    builder.add_node("show_menu", show_menu)
    builder.add_node("update_category", update_category)
    builder.add_node("exit_bot", exit_bot)
    builder.add_node("reset_jokes", reset_jokes)
    builder.add_node("update_language", update_language)    
    builder.add_node("update_critic_type", update_critic_type)
    builder.add_node("writer", make_writer_node(writer_llm))
    builder.add_node("critic", make_critic_node(critic_llm))
    builder.add_node("show_final_joke", show_final_joke)

    builder.set_entry_point("show_menu")

    builder.add_conditional_edges(
        "show_menu",
        route_choice,
        {
            "fetch_joke": "writer",
            "update_category": "update_category",
            "update_language": "update_language",
            "update_critic_type": "update_critic_type",
            "reset_jokes": "reset_jokes",
            "exit_bot": "exit_bot",
        },
    )

    builder.add_edge("update_category", "show_menu")
    builder.add_edge("writer", "critic")
    builder.add_edge("reset_jokes", "show_menu")
    builder.add_edge("update_language", "show_menu")
    builder.add_edge("update_critic_type", "show_menu")
    builder.add_conditional_edges(
        "critic",
        writer_critic_router,
        {"writer": "writer", "show_final_joke": "show_final_joke"},
    )
    builder.add_edge("show_final_joke", "show_menu")
    builder.add_edge("exit_bot", END)

    return builder.compile()


# ========== Entry Point ==========


def main():
    print("\n🎭 Starting joke bot with writer–critic LLM loop...")
    graph = build_joke_graph(writer_temp=0.8, critic_temp=0.1)
    state = AgenticJokeState(category="dad developer")

    while not state.quit:
        new_state = graph.invoke(state, config={"recursion_limit": 200})
        state = AgenticJokeState.model_validate(new_state)

    print("\n✅ Done. Final Joke Count:", len(state.jokes))


if __name__ == "__main__":
    main()
