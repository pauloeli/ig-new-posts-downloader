import os
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client
from jinja2 import Environment, FileSystemLoader


def load_configurations():
    load_dotenv()

    user = os.getenv("username")
    pswd = os.getenv("password")
    post_numbers = os.getenv("posts")
    profiles_str = os.getenv("profiles")

    if None in (user, pswd, profiles_str):
        raise ValueError("One or more required environment variables are missing.")

    profiles = profiles_str.split(",")
    return {"user": user, "pswd": pswd, "profiles": profiles, "post": post_numbers}


def connect(configurations: dict):
    client = Client()
    client.login(configurations["user"], configurations["pswd"])
    return client


def download_media(client: Client, media, path: Path):
    if media.media_type == 1:
        client.photo_download(media.pk, path)
    elif media.media_type == 2:
        client.video_download(media.pk, path)
    elif media.media_type == 8:
        client.album_download(media.pk, path)
    return


def get_profile_history(profile: str):
    profile_folder = Path.cwd() / "profiles" / profile
    history_file = profile_folder / "history.dat"

    if not history_file.exists():
        profile_folder.mkdir(parents=True, exist_ok=True)
        with open(history_file, "w", encoding="utf-8") as file:
            file.write("[]")
        return []

    with open(history_file, "r") as file:
        history = file.read().strip("[]").split(", ")

    return history


def update_profile_history(profile: str, history: []):
    path = Path.cwd() / "profiles" / profile / "history.dat"
    with open(path, "w", encoding="utf-8") as file:
        file.write("[" + ", ".join(history) + "]")
    return


def generate_html(caption_text: str, code: str, path: Path):
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
    template = env.get_template('media_template.html')

    media_urls = [f"{media_file}" for media_file in os.listdir(path) if not media_file.endswith('.txt')]
    html_content = template.render(caption=caption_text, code=code, media_urls=media_urls)

    with open(path / "index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    return


def get_posts(client: Client, profile: str, post_numbers: int):
    print(f"Getting posts from {profile}")

    history = get_profile_history(profile)

    user_id = client.user_id_from_username(profile)
    medias = client.user_medias(user_id, post_numbers)

    new_posts = []
    for media in medias:
        if media.code in history:
            continue

        new_posts.append(media.code)
        history.append(media.code)

        path = Path.cwd() / "profiles" / profile / media.code
        path.mkdir(parents=True, exist_ok=True)

        with open(path / "description.txt", "w", encoding="utf-8") as file:
            file.write(media.caption_text)

        download_media(client, media, path)
        generate_html(media.caption_text, media.code, path)
        update_profile_history(profile, history)

    print(f"{profile} {'has' if len(new_posts) > 0 else 'has no'} new posts")

    return


if __name__ == "__main__":
    configurations = load_configurations()
    client = connect(configurations)

    for profile in configurations["profiles"]:
        get_posts(client, profile, int(configurations["post"]))
