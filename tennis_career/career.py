import json
import re
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt
import pandas as pd


def _player_id(player):
    if not isinstance(player, str) or not player.strip():
        raise ValueError("Enter a player name.")
    words = player.strip().split()
    return "".join(word[0].upper() + word[1:] for word in words)


def _download(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8")
    except HTTPError as error:
        if error.code == 404:
            raise ValueError("Player not found.") from error
        raise


def _birthday(page):
    match = re.search(r"var\s+dob\s*=\s*['\"]?(\d{8})", page)
    if match is None:
        raise ValueError("Player not found.")
    return pd.to_datetime(match.group(1), format="%Y%m%d")


def _read_matches(text):
    match = re.search(r"var\s+(?:more)?matchmx\s*=\s*", text)
    if match is None:
        raise ValueError("No match data found.")
    rows, _ = json.JSONDecoder().raw_decode(text[match.end():])
    data = pd.DataFrame(rows)[[0, 1, 2, 4, 8, 9, 11, 16]]
    data.columns = ["date", "tournament", "surface", "result", "round", "score", "opponent", "opponent_age"]
    return data


def _opponent_ages(values, dates):
    birthdays = values.str.fullmatch(r"\d{8}")
    ages = pd.to_numeric(values.where(~birthdays), errors="coerce")
    dates_of_birth = pd.to_datetime(values.where(birthdays), format="%Y%m%d", errors="coerce")
    ages.loc[birthdays] = (dates - dates_of_birth).dt.days / 365.25
    return ages


def _clean_matches(text, birthday):
    data = _read_matches(text)
    data["date"] = pd.to_datetime(data["date"], format="%Y%m%d", errors="coerce")
    data = data[(data["score"] != "W/O") & data["result"].isin(["W", "L"])].copy()
    data["opponent_age"] = _opponent_ages(data["opponent_age"], data["date"])
    data["player_age"] = (data["date"] - birthday).dt.days / 365.25
    data["age_difference"] = data["player_age"] - data["opponent_age"]
    return data.dropna(subset=["player_age", "opponent_age"]).reset_index(drop=True)


def get_matches(player):
    """returns career matches + ages for a player"""
    player_id = quote(_player_id(player), safe="")
    base_url = "https://www.tennisabstract.com/jsmatches/" + player_id
    current = _download(base_url + ".js")
    birthday = _birthday(current)
    data = _clean_matches(current, birthday)
    try:
        history = _download(base_url + "Career.js")
    except ValueError:
        history = None  # Some players have only one match file.
    if history is not None:
        data = pd.concat([_clean_matches(history, birthday), data], ignore_index=True)
    data = data.drop_duplicates().sort_values("date").reset_index(drop=True)
    data.attrs["player"] = player.strip()
    return data


def plot_matches(data):
    """plots player age against age difference"""
    wins = data[data["result"] == "W"]
    losses = data[data["result"] == "L"]
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(wins["player_age"], wins["age_difference"], color="#34c5eb", s=10, label="Match won")
    ax.scatter(losses["player_age"], losses["age_difference"], color="#942a94", s=10, label="Match lost")
    ax.set_title(data.attrs.get("player", "Player") + "'s Professional Matches")
    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Player age minus opponent age (years)")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.grid(color="#e5e5e5", linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    return ax
