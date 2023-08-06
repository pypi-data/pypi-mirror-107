import click
import tmdbsimple as tmdb


def get_episodes(api_key, query, season):
    tmdb.API_KEY = api_key

    search = tmdb.Search().tv(query=query)
    for i, s in enumerate(search["results"]):
        print(
            f"{i}." + " " + s["name"],
            s["original_name"],
            s["first_air_date"],
            sep=" - ",
        )

    if not search["results"]:
        exit(f"Cant find anything for your query: {query}")

    choice = click.prompt(
        "Enter number corresponding to TV show", type=click.IntRange(min=0, max=i)
    )

    id = search["results"][choice]["id"]

    seasons = tmdb.TV(id=id).info()["number_of_seasons"]
    if season > seasons:
        print(
            "You ask for a season that doesn't exist, this TV show only has",
            seasons,
            "season" if seasons == 1 else "seasons",
        )
        exit()

    tv_season = tmdb.TV_Seasons(tv_id=id, season_number=season).info()

    episodes = [episode["name"] for episode in tv_season["episodes"]]

    return episodes
