from . import converters
from . import twitch_api
from . import bttv_api

__version__ = "0.2.2"
__all__ = ["converters", "twitch_api", "bttv_api"]


def fetch_raw(vod_id: int) -> dict:
    """Fetch raw chat log array from twitch API"""
    raw_log = twitch_api._fetch_all_comments(vod_id)
    return raw_log


def fetch_simple(vod_id: int) -> dict:
    """Fetch a simple chat log array"""
    raw_log = fetch_raw(vod_id)
    return converters.ttv_raw_to_simple_format(raw_log)


def fetch_txt(vod_id: int) -> str:
    """Fetch a simple text-only chat log"""
    raw_log = fetch_raw(vod_id)
    return converters.ttv_raw_to_txt(raw_log)


def fetch_html(
    vod_id: int, render_badges: bool = False, render_ext_emotes: bool = False
) -> str:
    """Fetch a simple HTML chat log"""
    raw_log = fetch_raw(vod_id)

    # Fetch badges if we want them
    badges = []
    if render_badges:
        badges = twitch_api._fetch_badges_by_vod_id(vod_id)

    # Fetch third party emotes if we want them
    ext_emotes = []
    if render_ext_emotes:
        channel_id = twitch_api._fetch_vod_info(vod_id)["owner"]["id"]
        ext_emotes = bttv_api._fetch_all_emotes(channel_id)

    return converters.ttv_raw_to_html(raw_log, badges_in=badges, ext_emotes=ext_emotes)


def fetch_badges_by_vod_id(vod_id: int) -> str:
    """Fetch global and channel badges by supplying a VOD ID"""
    return twitch_api._fetch_badges_by_vod_id(vod_id)


def fetch_badges_by_channel_login(channel_login: str) -> str:
    """Fetch global and channel badges by supplying a channel login"""
    return twitch_api._fetch_badges_by_channel(channel_login)


def fetch_third_party_emotes_by_channel_id(channel_id: int) -> str:
    """Fetch BTTV and FFZ emotes by supplying a channel ID (not login)"""
    return bttv_api._fetch_all_emotes(channel_id)


def fetch_third_party_emotes_by_vod_id(vod_id: int) -> str:
    """Fetch BTTV and FFZ emotes by supplying a VOD ID"""
    channel_id = twitch_api._fetch_vod_info(vod_id)["owner"]["id"]
    return bttv_api._fetch_all_emotes(channel_id)
