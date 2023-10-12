import os
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

import os


def load_configurations():
    load_dotenv()

    config_mapping = {
        "user": "username",
        "pswd": "password",
        "user_posts": "user_posts",
        "new_user_posts": "new_user_posts",
        "profiles": "profiles",
        "save_method": "save_method"
    }

    missing_variables = [env_var for key, env_var in config_mapping.items() if os.getenv(env_var) is None]
    if missing_variables:
        raise ValueError(f"One or more required environment variables are missing: {', '.join(missing_variables)}")

    config = {}
    for key, env_var in config_mapping.items():
        config[key] = os.getenv(env_var)

    config.setdefault("user_posts", str(5))
    config.setdefault("new_user_posts", str(10))
    config.setdefault("save_method", "new")

    config["profiles"] = set(config["profiles"].split(","))

    return config


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


def get_posts(client: Client, profile: str, posts: int, new_user_posts: int, save_method: str):
    history = get_profile_history(profile)

    user_id = client.user_id_from_username(profile)
    if not history:
        medias = client.user_medias(user_id, new_user_posts)
    else:
        medias = client.user_medias(user_id, posts)

    new_posts = []
    for media in medias:
        if media.code in history:
            continue

        new_posts.append(media.code)
        history.append(media.code)

        if save_method == "new":
            path = Path.cwd() / "new" / media.code
        else:
            path = Path.cwd() / "profiles" / profile / media.code

        path.mkdir(parents=True, exist_ok=True)

        with open(path / "description.txt", "w", encoding="utf-8") as file:
            file.write(media.caption_text)

        download_media(client, media, path)
        generate_html(media.caption_text, media.code, path)
        update_profile_history(profile, history)

    if save_method == "profile":
        print(f"{profile} {'has' if len(new_posts) > 0 else 'has no'} new posts")

    return


if __name__ == "__main__":
    configurations = load_configurations()
    client = connect(configurations)

    profiles = configurations["profiles"]
    if not profiles:
        print(f"Profiles list is empty, exiting")
        exit(0)

    save_method = configurations["save_method"]
    user_posts = int(configurations["user_posts"])
    new_user_posts = int(configurations["new_user_posts"])

    progress_bar = tqdm(desc="Processing Profiles", total=len(profiles), position=0, leave=True)

    for idx, profile in enumerate(profiles):
        get_posts(client, profile, user_posts, new_user_posts, save_method)
        progress_bar.update()

    progress_bar.close()
