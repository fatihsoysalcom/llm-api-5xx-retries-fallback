# LLM API 5xx Retries Fallback

This example demonstrates how to implement retry mechanisms with exponential backoff and a fallback strategy when interacting with a Large Language Model (LLM) API that might return 5xx errors. It simulates an unreliable LLM API and shows how to ensure application resilience by attempting calls multiple times before resorting to a predefined alternative response.

## Language

`python`

## How to Run

Save the code as `main.py`. Run from your terminal: `python main.py`.

## Original Article

This example accompanies the Turkish article: [LLM API 5xx Hataları: Yeniden Denemeler ve Geri Dönüş Stratejileri](https://fatihsoysal.com/blog/llm-api-5xx-hatalari-yeniden-denemeler-ve-geri-donus-stratejileri/).

## License

MIT — see [LICENSE](LICENSE).
