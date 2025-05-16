import  requests


class OllamaCustomSummarizerClient:
    def __init__(self):
        """
        Initialize the OllamaCustomSummarizerClient class.
        """
        url = "http://localhost:8000/llm/ollama/custom-summarization/"

        text = """
        By using a pre-made container image it's very easy to combine and use different tools. For example, to try out a new database. In most cases, you can use the official images, and just configure them with environment variables.

That way, in many cases you can learn about containers and Docker and reuse that knowledge with many different tools and components.

So, you would run multiple containers with different things, like a database, a Python application, a web server with a React frontend application, and connect them together via their internal network.

All the container management systems (like Docker or Kubernetes) have these networking features integrated into them
        """
        llama_model = "Mistral"

        res = requests.post(url, params={"text": text})

        if res.status_code == 200:
            summary = res.json()

            print("Summary:", summary)
        else:
            raise Exception(f"Error: {res.status_code} - {res.text}")


if __name__ == "__main__":
    # Initialize the client
    OllamaCustomSummarizerClient()
