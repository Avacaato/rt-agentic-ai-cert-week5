import webbrowser
from run_wk5_l2c_llm_joke_bot import build_joke_graph


def main():
    graph = build_joke_graph()  # This is already CompiledStateGraph
    mermaid_code = graph.get_graph().draw_mermaid()
    # print(mermaid_code)
    save_and_open_mermaid(mermaid_code)

    with open("joke_bot_graph.mmd", "w") as f:
        f.write(mermaid_code)

def save_and_open_mermaid(mermaid_code: str, filename: str = "graph.html"):
    html_content = f"""
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <script>mermaid.initialize({{startOnLoad:true}});</script>
    </head>
    <body>
      <div class="mermaid">
      {mermaid_code}
      </div>
    </body>
    </html>
    """
    with open(filename, "w") as f:
        f.write(html_content)
    webbrowser.open_new_tab(filename)        

if __name__ == "__main__":
    main()