from typing import Mapping

import click
from ghapi.all import GhApi

from . import __version__
from .constants import (
    DEFAULT_ENV_VARIABLE,
    TOKEN_HELP,
    TOPICS,
    URL_ERROR_MSG,
    WEB_URL_PATTERN,
)
from .utils import list2str


def validate_url(ctx, param, value):
    try:
        match = WEB_URL_PATTERN.match(value)
        matches = match.groupdict()

        return matches
    except AttributeError:
        raise click.BadParameter(URL_ERROR_MSG)


@click.command()
@click.argument("url", type=str, callback=validate_url)
@click.argument("topics", type=click.Choice(TOPICS.keys(), case_sensitive=False))
@click.option(
    "-t",
    "--token",
    type=str,
    metavar="VALUE",
    envvar=DEFAULT_ENV_VARIABLE,
    show_envvar=True,
    help=TOKEN_HELP,
)
@click.version_option(version=__version__)
def main(url: Mapping[str, str], topics: str, token: str) -> None:
    """A Python CLI for adding pre-defined topics to a GitHub repository."""
    click.echo(
        f"\nAdding {list2str(TOPICS[topics])} "
        f"to {click.style(url['repo'], bold=True)}...",
    )

    # More info:
    # - https://github.com/fastai/ghapi
    # - https://stackoverflow.com/a/4907053
    api = GhApi(
        owner=url["owner"],
        repo=url["repo"],
        token=token,  # or `os.environ[DEFAULT_ENV_VARIABLE]`
    )

    # current_topics = list(api.repos.get_all_topics(per_page=100)["names"])

    api.repos.replace_all_topics(names=TOPICS[topics])

    click.secho("\n✨ Done!", bold=True)
