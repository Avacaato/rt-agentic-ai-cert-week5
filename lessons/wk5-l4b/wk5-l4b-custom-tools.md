![AAIDC-wk5-l4b-custom-tools.jpeg](AAIDC-wk5-l4b-custom-tools.jpeg)

--DIVIDER--

---

[⬅️ Previous - Power of Tools](https://app.readytensor.ai/publications/hHwXrjkLnNaD)

---

--DIVIDER--

# TLDR

In this lesson, you’ll learn how to build and integrate custom tools into a LangGraph agent. You’ll create Python functions tailored to your own use case, wrap them with LangChain’s tool interface, and wire them into an agent that knows when to use them. By the end, your agent will be able to take real action using tools you’ve built yourself.

---

--DIVIDER--

# From Generic Tools to Custom Solutions

Most of the time, built-in tools like search, calculators, or file readers will cover what your agent needs to do.

But when your workflow requires domain-specific logic — querying internal systems, applying custom rules, or working with your own data formats — you’ll need to create your own tools.

In this lesson, we’ll show you how.

---

--DIVIDER--

# Implementing Custom Tools: A Practical Example

Imagine you're a security engineer tasked with auditing GitHub repositories for accidentally committed secrets. Developers sometimes push `.env` files containing API keys, database passwords, and other sensitive information to public repositories — a serious security risk.

Your challenge: Given a GitHub repository URL, you need to:

1.  Download the repository
2.  Search for any `.env` files
3.  Check if they contain potentially sensitive information

No existing tool can do this complete workflow. You need custom tools that understand your specific security requirements.

This is exactly the kind of problem that custom tools are designed to solve — domain-specific operations that require multiple steps and specialized logic.

--DIVIDER--

:::info{title="Video Walkthrough Below"}
🎥 Prefer to see it in action first? Jump to the video walkthrough section below ⬇
:::

--DIVIDER--

# Custom Tools for Security Auditing

Let's build two custom tools that work together to solve this problem:

- `download_and_extract_repo`: Downloads any GitHub repository locally
- `env_content`: Searches for and reads `.env` files in the downloaded repository

--DIVIDER--

## Step 1: Tool Structure and Registration

First, let's look at how our repository download tool is structured:

```python
import os
import shutil
import zipfile
import requests
from typing import Union
from langchain_core.tools import tool

@tool
def download_and_extract_repo(repo_url: str) -> Union[str, bool]:
    """Download a Git repository and extract it to a local directory.

    This tool downloads a Git repository as a ZIP file from GitHub or similar
    platforms and extracts it to a './data/repo' directory.

    Args:
        repo_url: The complete URL of the Git repository

    Returns:
        The path to the extracted repository directory if successful, or False if failed
    """
    # Implementation goes here
    pass
```

The `@tool` decorator automatically registers this function as a tool that your agent can use. Notice how the docstring provides clear instructions for the agent about what the tool does and how to use it.

--DIVIDER--

## Step 2: Implementation Logic

Here's how the repository download tool actually works:

```python
@tool
def download_and_extract_repo(repo_url: str) -> Union[str, bool]:
    """Download a Git repository and extract it to a local directory."""
    output_dir = os.path.join(DATA_DIR, "repo")

    try:
        # Remove existing repo if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

        # Convert repo URL to zip download URL
        if repo_url.endswith(".git"):
            repo_url = repo_url[:-4]

        download_url = f"{repo_url}/archive/refs/heads/main.zip"

        # Download and extract the repository
        response = requests.get(download_url, stream=True)
        if response.status_code == 404:
            # Try master branch if main doesn't exist
            download_url = f"{repo_url}/archive/refs/heads/master.zip"
            response = requests.get(download_url, stream=True)

        # Extract to local directory
        # ... extraction logic ...

        return output_dir

    except Exception as e:
        print(f"Error: {str(e)}")
        return False
```

This tool handles real-world complexities like different branch names (main vs master), error handling, and file system operations.

Now we need a tool to search for and read `.env` files in the downloaded repository:

--DIVIDER--

## Step 3: The Tool for .env File Analysis

Now we need a tool to search for and read `.env` files in the downloaded repository:

```python
@tool
def env_content(dir_path: str) -> str:
    """Read and return the content of a .env file from a specified directory.

    This tool searches through the given directory path and its subdirectories
    to find a .env file and returns its complete content.

    Args:
        dir_path: The directory path to search for .env file

    Returns:
        The complete content of the .env file as a string, or None if not found
    """
    for dir, _, files in os.walk(dir_path):
        for file in files:
            if file == ".env":
                with open(os.path.join(dir, file), "r") as f:
                    return f.read()
    return None
```

This tool demonstrates how custom tools can perform specialized file operations that generic tools can't handle.

--DIVIDER--

## Step 4: Tool Registry and Management

To keep your tools organized, create a registry system:

```python
def get_all_tools():
    """Return all available custom tools."""
    return [
        download_and_extract_repo,
        env_content,
        # Add more custom tools here
    ]

def create_tool_registry():
    """Create a mapping of tool names to tool functions."""
    tools = get_all_tools()
    return {tool.name: tool for tool in tools}
```

This makes it easy to manage multiple custom tools and add new ones.

---

--DIVIDER--

# Integrating Custom Tools into Your Agent

Once you've built your custom tools, integrating them follows the same pattern as built-in tools:

## The LLM Node

Your agent's brain that decides when to use tools:

```python
def llm_node(state: State):
    """Node that handles LLM invocation with custom tools."""
    tools = get_all_tools()
    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

## The Tools Node

Where your custom tools get executed:

```python
def tools_node(state: State):
    """Node that executes custom tools."""
    tool_registry = create_tool_registry()
    last_message = state["messages"][-1]
    tool_messages = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        if tool_name in tool_registry:
            tool_function = tool_registry[tool_name]
            result = tool_function.invoke(tool_call["args"])

            tool_messages.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            ))

    return {"messages": tool_messages}
```

The beauty is that your agent treats custom tools exactly like built-in ones — it just has more specialized capabilities.

---

--DIVIDER--

# 📹 Video Walkthrough: Building Custom Tools in Practice

:::youtube[Title]{#7Ajx1qDXcEA}

In this video walkthrough, you’ll see how to bring custom tools to life as we:

- Write two Python tools: one to download a GitHub repo, and one to scan for .env files
- Register these tools and bind them to an LLM inside a LangGraph workflow
- Test the full agent loop on real repositories — including one with pushed secrets

---

--DIVIDER--

# Custom Tools: Your Agent’s Power-Up

Across the last two lessons, you’ve added one of the most important ingredients that distinguish an agent from a chatbot: **tools**.

In the previous lesson, you saw how to plug in existing tools — like a web search function — and let the agent decide when to use them. That alone takes you beyond passive conversation and into real-world action.

In this lesson, you went one step further: building your own tools. When built-ins aren’t enough — when your use case involves custom logic, internal systems, or domain-specific tasks — writing your own tools is the way forward.

Most of the time, existing tools will cover common needs. But agents become truly powerful when you give them exactly the capabilities your context demands.

Keep exploring. Keep adding tools. The more your agent can do, the more useful — and agentic — it becomes.

--DIVIDER--

---

[⬅️ Previous - Power of Tools](https://app.readytensor.ai/publications/hHwXrjkLnNaD)

---
