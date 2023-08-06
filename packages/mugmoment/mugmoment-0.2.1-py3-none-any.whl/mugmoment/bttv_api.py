import httpx

_urlset_sizes = ["1x", "2x", "4x"]


def _fetch_bttv_global() -> dict:
    req = httpx.get("https://api.betterttv.net/3/cached/emotes/global")
    reqj = req.json()
    return reqj


def _fetch_ffz_global() -> dict:
    req = httpx.get("https://api.betterttv.net/3/cached/frankerfacez/emotes/global")
    reqj = req.json()
    return reqj


def _fetch_bttv_channel(channel_id: int) -> dict:
    req = httpx.get(f"https://api.betterttv.net/3/cached/users/twitch/{channel_id}")
    reqj = req.json()
    return reqj


def _fetch_ffz_channel(channel_id: int) -> dict:
    req = httpx.get(
        f"https://api.betterttv.net/3/cached/frankerfacez/users/twitch/{channel_id}"
    )
    reqj = req.json()
    return reqj


def _bttv_emote_url(emote_id: str, size: str) -> str:
    if size == "4x":
        # WHY????
        size = "3x"
    return f"https://cdn.betterttv.net/emote/{emote_id}/{size}"


def _ffz_emote_url(emote_id: str, size: str) -> str:
    size = size.strip("x")
    return f"https://cdn.betterttv.net/frankerfacez_emote/{emote_id}/{size}"
    # return f"https://cdn.frankerfacez.com/emote/{emote_id}/{size}"


def _bttv_emote_srcset(emote_id: str):
    srcset = []
    for size in _urlset_sizes:
        srcset.append(f"{_bttv_emote_url(emote_id, size)} {size}")
    return ",".join(srcset)


def _ffz_emote_srcset(emote_id: str):
    srcset = []
    for size in _urlset_sizes:
        srcset.append(f"{_ffz_emote_url(emote_id, size)} {size}")
    return ",".join(srcset)


def _process_ffz(emote_set, is_global=False):
    out_set = {}
    for emote in emote_set:
        global_text = "global" if is_global else "channel"
        from_name = emote["user"]["displayName"]
        alt_text = f"{emote['code']} | FFZ {global_text} emote from {from_name}"
        url = _ffz_emote_url(emote["id"], "1x")
        srcset = _ffz_emote_srcset(emote["id"])

        out_set[emote["code"]] = {
            "id": emote["id"],
            "alt": alt_text,
            "src": url,
            "srcset": srcset,
            "global": is_global,
            "source": "ffz",
        }
    return out_set


def _process_bttv(emote_set, is_global):
    out_set = {}
    emotes_to_process = []
    if is_global:
        emotes_to_process = emote_set
    else:
        if "channelEmotes" in emote_set:
            emotes_to_process += emote_set["channelEmotes"]
        if "sharedEmotes" in emote_set:
            emotes_to_process += emote_set["sharedEmotes"]

    for emote in emotes_to_process:
        global_text = "global" if is_global else "channel"
        alt_text = f"{emote['code']} | BTTV {global_text} emote"
        if "user" in emote:
            alt_text += f" from {emote['user']['displayName']}"

        url = _bttv_emote_url(emote["id"], "1x")
        srcset = _bttv_emote_srcset(emote["id"])

        out_set[emote["code"]] = {
            "id": emote["id"],
            "alt": alt_text,
            "src": url,
            "srcset": srcset,
            "global": is_global,
            "source": "bttv",
        }
    return out_set


def _fetch_all_emotes(channel_id) -> list:
    emotes = {
        **_process_bttv(_fetch_bttv_global(), True),
        **_process_ffz(_fetch_ffz_global(), True),
        **_process_bttv(_fetch_bttv_channel(channel_id), False),
        **_process_ffz(_fetch_ffz_channel(channel_id), False),
    }
    return emotes
