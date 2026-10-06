import asyncio
from typing import Annotated

import typer

from llm_chat.config import get_settings
from llm_chat.models import ChatRequest
from llm_chat.service import ChatService

app = typer.Typer(help="Chat with an OpenAI or DeepSeek model.")


def choose(label: str, options: list[str]) -> str:
    typer.echo(f"\nSelect {label}:")
    for index, option in enumerate(options, start=1):
        typer.echo(f"  {index}. {option}")

    while True:
        raw_choice = typer.prompt("Enter number")
        try:
            return options[int(raw_choice) - 1]
        except (ValueError, IndexError):
            typer.echo(f"Please enter a number from 1 to {len(options)}.", err=True)


async def run_chat(provider_name: str | None, model_name: str | None) -> None:
    settings = get_settings()
    provider = provider_name or choose("provider", ["openai", "deepseek"])
    models = settings.models_for(provider)
    model = model_name or choose("model", models)
    message = typer.prompt("\nYou")

    try:
        response = await ChatService(settings).chat(
            ChatRequest(provider=provider, model=model, message=message)  # type: ignore[arg-type]
        )
    except Exception as error:
        typer.secho(f"Error: {error}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from error

    typer.secho("\nAssistant", bold=True)
    typer.echo(response.response)


@app.command()
def chat(
    provider: Annotated[str | None, typer.Option(help="openai or deepseek")] = None,
    model: Annotated[str | None, typer.Option(help="Model identifier")] = None,
) -> None:
    """Select a provider and model, then send one message."""
    asyncio.run(run_chat(provider, model))


@app.command()
def serve(
    host: Annotated[str, typer.Option()] = "127.0.0.1",
    port: Annotated[int, typer.Option()] = 8000,
) -> None:
    """Start the FastAPI server."""
    import uvicorn

    uvicorn.run("llm_chat.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()

