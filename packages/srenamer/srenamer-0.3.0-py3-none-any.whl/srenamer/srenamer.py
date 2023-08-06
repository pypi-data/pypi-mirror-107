import os
import click
from .param_types import ApiKeyParamType, ExtParamType
from .tmdb_api import get_episodes
from .renamer import renamer


@click.command()
@click.option(
    "--api-key",
    "-a",
    envvar="API_KEY",
    type=ApiKeyParamType(),
    prompt="Enter your API key from TMDb",
    help="Your API key for the TMDb (it can be stored in system variable under 'API_KEY' name).",
)
@click.option(
    "--query",
    "-q",
    required=True,
    type=click.STRING,
    help="Search query that should contain name of TV show.",
)
@click.option("--season", "-s", required=True, type=click.INT, help="Season number.")
@click.option(
    "--path",
    "-p",
    type=click.Path(),
    default=lambda: os.getcwd(),
    show_default="current directory",
    help="Path to the directory with files for renaming.",
)
@click.option(
    "--extension",
    "-e",
    type=ExtParamType(),
    default="",
    show_default="None, all files in a directory will be matched and renamed",
    help="Extension for files that should be renamed",
)
def cli(api_key, query, season, path, extension):
    episodes = get_episodes(api_key=api_key, query=query, season=season)
    renamer(path=path, extension=extension, episodes=episodes)
