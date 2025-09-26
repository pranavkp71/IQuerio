import click
from optimizer import optimize_query

@click.command()
@click.argument('query')
def optimize(query):
    result = optimize_query(query)
    click.echo(f"Query: {result['original_query']}")
    click.echo(f"Optimized Query: {result['optimized_query']}")
    if result["issues"]:
        click.echo("Issues:")
        for issue in result["issues"]:
            click.echo(f"- {issue}")
    else:
        click.echo("Issues: None")
    if result["suggestions"]:
        click.echo("Suggestions:")
        for suggestion in result["suggestions"]:
            click.echo(f"- {suggestion}")
    else:
        click.echo("Suggestions: None")
    click.echo(f"EXPLAIN Plan: {result['explain_plan']}")

if __name__ == "__main__":
    optimize()