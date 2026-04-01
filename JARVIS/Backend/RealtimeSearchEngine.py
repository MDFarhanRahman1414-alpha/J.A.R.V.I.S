from tavily import TavilyClient
from groq import Groq
from rich import print

Tavily = TavilyClient(api_key="YOUR API KEY)
client = Groq(api_key="YPUR API KEY ")

def RealtimeSearchEngine(prompt):
    try:
        # Step 1 — Get fresh realtime results from Tavily
        search = Tavily.search(query=prompt, max_results=5)
        results = search.get("results", [])

        if not results:
            return "Sorry, I couldn't find any results for that."

        # Step 2 — Format results into text block 
        raw_text = ""
        for i, result in enumerate(results):
            title   = result.get("title", "")
            content = result.get("content", "")
            url     = result.get("url", "")
            raw_text += f"Result {i+1}: {title} — {content}\nURL: {url}\n\n"

        # Step 3 — Ask Groq to summarize into clean answer
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are JARVIS, an AI assistant. "
                        "Based on the search results provided, give a clean, "
                        "concise, and accurate answer to the user's question. "
                        "Do not mention that you searched the web. "
                        "Do not add notes or disclaimers. Just answer directly."
                    )
                },
                {
                    "role": "user",
                    "content": f"Question: {prompt}\n\nSearch Results:\n{raw_text}"
                }
            ],
            max_tokens=512,
            temperature=0.7,
            stream=True,
        )

        # Step 4 — Stream and return the clean answer
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        return answer.strip()

    except Exception as e:
        return f"Search error: {e}"


if __name__ == "__main__":
    print("[bold green]Realtime Search Engine — Ready[/bold green]")
    print("[dim]Type your query. Press Ctrl+C to exit.[/dim]\n")

    while True:
        try:
            user_input = input("[bold cyan]>>[/bold cyan] ").strip()
            if not user_input:
                continue
            print("\n[bold yellow]JARVIS:[/bold yellow]")
            result = RealtimeSearchEngine(user_input)
            print(f"{result}\n")
        except KeyboardInterrupt:
            print("\n[bold red]Exiting. Goodbye![/bold red]")
            break