from duckduckgo_search import DDGS


def get_live_news_context(sport_name):
    """
    Searches DuckDuckGo for the latest news related to the selected sport.

    Parameters:
        sport_name (str): Name of the sport selected by the user.

    Returns:
        str: Combined text containing the top search result snippets.
    """

    search_query = (
        f"{sport_name} latest tournament results "
        f"championship winners recent matches news"
    )

    retrieved_texts = []

    print(f"Searching DuckDuckGo for: {search_query}")

    try:
        with DDGS() as ddgs:

            results = ddgs.text(
                keywords=search_query,
                max_results=3
            )

            for index, result in enumerate(results, start=1):

                title = result.get("title", "No Title")

                snippet = result.get(
                    "body",
                    "No description available."
                )

                retrieved_texts.append(
                    f"Web Source {index}\n"
                    f"Title: {title}\n"
                    f"Snippet: {snippet}"
                )

    except Exception as error:

        print(f"DuckDuckGo Search Error: {error}")

        return (
            "No live sports news could be retrieved "
            "at this moment."
        )

    return "\n\n".join(retrieved_texts)