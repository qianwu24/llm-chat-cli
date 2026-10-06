# llm-chat-cli

A small Python application for sending a prompt to either OpenAI or DeepSeek. It provides an
interactive terminal CLI and a FastAPI HTTP endpoint backed by the same chat service.

## Setup

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev
cp .env.example .env
```

Add your API keys to `.env`. The file is ignored by Git. You only need a key for the provider
you intend to use.

```dotenv
OPENAI_API_KEY=...
DEEPSEEK_API_KEY=...
```

The available model choices are configurable through `OPENAI_MODELS` and `DEEPSEEK_MODELS`.

## Interactive CLI

```bash
uv run llm-chat chat
```

The CLI asks you to select a provider and model, then accepts one message. Choices can also be
passed directly:

```bash
uv run llm-chat chat --provider deepseek --model deepseek-flash
```

## FastAPI

Start the service:

```bash
uv run llm-chat serve
```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>, or make a request:

```bash
curl http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"provider":"openai","model":"gpt-5.5","message":"Hello!"}'
```

List configured providers and model choices at `GET /providers`. The endpoint reports whether a
key is configured but never returns the key.

## Development

```bash
uv run pytest
uv run ruff check .
```
