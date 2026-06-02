"""YUYAY Intelligence Framework — Command Line Interface."""

from __future__ import annotations

import asyncio
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from yuyay.archetypes import ALL_ARCHETYPES
from yuyay.fios import FIOS, FIOSConfig
from yuyay.questionnaire import process_responses
from yuyay.transformers import ALL_TRANSFORMERS

app = typer.Typer(
    name="yuyay",
    help="YUYAY Intelligence Framework — UN Office of the Future",
    add_completion=False,
)

console = Console()


@app.command()
def archetypes() -> None:
    """List all 12 YUYAY archetypes."""
    table = Table(title="YUYAY Archetypes", show_header=True)
    table.add_column("Name", style="gold1")
    table.add_column("Function", style="white")

    for archetype in ALL_ARCHETYPES:
        table.add_row(archetype.name, archetype.function)

    console.print(table)


@app.command()
def transformers() -> None:
    """List all transformer questions."""
    table = Table(title="Transformer Questions", show_header=True)
    table.add_column("ID", style="gold1")
    table.add_column("Question", style="white")

    for transformer in ALL_TRANSFORMERS:
        table.add_row(transformer.id, transformer.question)

    console.print(table)


@app.command()
def evaluate(
    responses: str = typer.Option(
        ...,
        "--responses",
        "-r",
        help="Comma-separated responses e.g. '1a=YES,1b=NO,2a=PO'",
    ),
) -> None:
    """Run a YUYAY evaluation with YES/NO/PO responses."""
    try:
        parsed: dict[str, str] = {}
        for item in responses.split(","):
            key, value = item.strip().split("=")
            parsed[key.strip()] = value.strip().upper()

        report = process_responses(parsed)

        console.print(
            Panel(
                f"[green]YES:[/green] {report.yes_count}  "
                f"[red]NO:[/red] {report.no_count}  "
                f"[yellow]PO:[/yellow] {report.po_count}  "
                f"[white]Total:[/white] {report.total}  "
                f"[magenta]Flagged:[/magenta] {len(report.flags)}",
                title="[gold1]YUYAY Evaluation Report[/gold1]",
            )
        )

        if report.flags:
            console.print("\n[yellow]Dimensions for deeper inquiry:[/yellow]")
            for dim in report.flags:
                console.print(f"  • {dim}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)


@app.command()
def query(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Your question"),
    provider: str = typer.Option("anthropic", "--provider", help="LLM provider"),
    model: str = typer.Option("claude-sonnet-4-6", "--model", help="Model name"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="API key"),
) -> None:
    """Query the FIOS intelligence layer."""

    async def _query() -> None:
        config = FIOSConfig(
            provider=provider,
            model=model,
            api_key=api_key or "",
        )
        fios = FIOS(config)
        with console.status(f"[gold1]Querying {provider}...[/gold1]"):
            result = await fios.query(prompt)

        console.print(
            Panel(
                result.response,
                title=f"[gold1]{result.provider}/{result.model}[/gold1]",
            )
        )
        console.print(
            f"[dim]Coherence: {result.coherence_score}/100 | "
            f"Tokens: {result.total_tokens} | "
            f"Latency: {result.latency_ms:.0f}ms | "
            f"Cost: ${result.estimated_cost_usd:.6f}[/dim]"
        )

    asyncio.run(_query())


def main() -> None:
    """Entry point for the YUYAY CLI."""
    app()
