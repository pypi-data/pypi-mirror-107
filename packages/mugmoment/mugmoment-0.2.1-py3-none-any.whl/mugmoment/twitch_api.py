import logging
import httpx

# Default client ID from twitch web UI
default_headers = {
    "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
}


def _do_gql_request(gql_data: dict) -> dict:
    req = httpx.post(
        "https://gql.twitch.tv/gql#origin=twilight",
        headers=default_headers,
        json=gql_data,
    )
    reqj = req.json()
    return reqj


def _fetch_vod_info(vod_id: int) -> dict:
    vod_info_raw = _do_gql_request(
        [
            {
                "operationName": "VideoPlayerStreamInfoOverlayVOD",
                "variables": {"videoID": str(vod_id), "includePrivate": False},
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "682ddbe13e290d601bc500b961da5ea24c5d6193c9cef70bae1d9b520dca24b0",
                    }
                },
            }
        ]
    )

    vod_info = vod_info_raw[0]["data"]["video"]
    return vod_info


def _fetch_badges_by_channel(channel_login: str):
    vod_info_raw = _do_gql_request(
        [
            {
                "operationName": "SubModal",
                "variables": {
                    "giftRecipientLogin": "",
                    "withStandardGifting": False,
                    "login": channel_login,
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "f474f17a1a12f70db63ed13daae7acd072e53c09cc13e08de86ce4d992af5628",
                    }
                },
            },
        ],
    )

    vod_info = vod_info_raw[0]["data"]["badges"]
    return vod_info


def _fetch_badges_by_vod_id(vod_id: int):
    channel_login = _fetch_vod_info(vod_id)["owner"]["login"]
    return _fetch_badges_by_channel(channel_login)


def _fetch_comments(vod_id: int, cursor: str = None) -> dict:
    url = f"https://api.twitch.tv/v5/videos/{vod_id}/comments"
    if cursor:
        url += f"?cursor={cursor}"

    req = httpx.get(url, headers=default_headers)
    reqj = req.json()

    return reqj


def _fetch_all_comments(vod_id: int) -> dict:
    """Fetch raw chat log array from twitch API"""
    page_counter = 1
    raw_comments = _fetch_comments(vod_id)
    comments = raw_comments["comments"]

    while raw_comments.get("_next"):
        page_counter += 1
        cursor = raw_comments["_next"]
        logging.debug(f"Fetching {cursor}, page {page_counter}.")

        raw_comments = _fetch_comments(vod_id, cursor)

        comments += raw_comments["comments"]
        logging.debug(f"{comments[-1]['content_offset_seconds']} seconds of offset")
    return comments
