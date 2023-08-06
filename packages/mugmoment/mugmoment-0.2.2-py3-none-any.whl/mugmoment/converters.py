import html

_srcset_sizes = ["1x", "2x", "4x"]


def ttv_raw_to_simple_format(raw_comments):
    comments = []
    include_hours = raw_comments[-1]["content_offset_seconds"] >= 3600
    for comment in raw_comments:
        simple_data = {
            "author": comment["commenter"]["display_name"],
            "body": comment["message"]["body"],
            "offset": comment["content_offset_seconds"],
            "fancy_offset": _offset_to_fancy_timestamp(
                comment["content_offset_seconds"], include_hours
            ),
        }
        comments.append(simple_data)
    return comments


def ttv_raw_to_txt(raw_comments):
    simple_comments = ttv_raw_to_simple_format(raw_comments)
    comments = []
    for comment in simple_comments:
        text_data = f"{comment['fancy_offset']} <{comment['author']}> {comment['body']}"
        comments.append(text_data)
    return "\r\n".join(comments)


def _offset_to_fancy_timestamp(
    offset, include_hours=True, only_include_hours_above_1h=True
):
    # Convert offset to int to drop the msecs
    offset = int(offset)

    if only_include_hours_above_1h and include_hours and offset < 3600:
        include_hours = False

    # Derive hours, minutes and seconds
    hours = int(offset / 3600) if include_hours else 0
    minutes = int((offset - (hours * 3600)) / 60)
    seconds = offset - ((hours * 3600) + (minutes * 60))

    fancy_timestamp = f"{minutes:02d}:{seconds:02d}"
    if include_hours:
        fancy_timestamp = f"{hours:02d}:" + fancy_timestamp

    return fancy_timestamp


def _process_badges(badges):
    new_badges = {}

    for badge in badges:
        set_id = badge["setID"]
        version = badge["version"]

        if set_id not in new_badges:
            new_badges[set_id] = {}

        new_badges[set_id][version] = badge

    return new_badges


def _html_handle_badges(badges, comment):
    html_data = ""
    for user_badge in comment["message"]["user_badges"]:
        set_id = user_badge["_id"]
        version = user_badge["version"]
        if set_id not in badges or version not in badges[set_id]:
            continue

        badge_data = badges[set_id][version]
        src = ""
        srcset = []
        for key, value in badge_data.items():
            if key.startswith("image"):
                size = key.replace("image", "")
                if size == "1x":
                    src = value
                srcset.append(f"{value} {size}")
        html_data += f'<img alt="{badge_data["title"]}" class="badge badge-{set_id} badge-{set_id}-{version}" src="{src}" srcset="{",".join(srcset)}">'
    return html_data


def _derive_emote_img(emote):
    return f'<img alt="{emote["alt"]}" class="emote emote-{emote["source"]} emote-{emote["id"]}" src="{emote["src"]}" srcset="{emote["srcset"]}">'


def _html_handle_emotes(emotes, text):
    # This impl is mostly based on BTTV
    # https://github.com/night/betterttv/blob/8f699b4665aa476d70f5fb9e7946042deda77134/src/modules/chat/index.js#L164-L197
    words = []
    for word in text.split(" "):
        if word in emotes:
            emote = emotes[word]
            words.append(_derive_emote_img(emote))
        else:
            words.append(html.escape(word))
    return " ".join(words)


def _ttv_emote_url(emote_id: str, size: str) -> str:
    if size == "4x":
        size = "3x"
    size = size.replace("x", ".0")
    return f"https://static-cdn.jtvnw.net/emoticons/v2/{emote_id}/default/dark/{size}"


def _ttv_emote_srcset(emote_id: str):
    srcset = []
    for size in _srcset_sizes:
        srcset.append(f"{_ttv_emote_url(emote_id, size)} {size}")
    return ",".join(srcset)


def _ttv_emote_to_emote(emote_id, emote_name):
    return {
        "source": "twitch",
        "id": emote_id,
        "global": None,
        "alt": f"{emote_name} | Twitch emote",
        "src": _ttv_emote_url(emote_id, "1x"),
        "srcset": _ttv_emote_srcset(emote_id),
    }


def _html_derive_twitch_emote(emote_id, emote_name):
    emote = _ttv_emote_to_emote(emote_id, emote_name)
    return _derive_emote_img(emote)


def ttv_raw_to_html(raw_comments, badges_in=None, ext_emotes=None):
    comments = []
    badges = _process_badges(badges_in)
    include_hours = raw_comments[-1]["content_offset_seconds"] >= 3600
    for comment in raw_comments:
        timestamp = _offset_to_fancy_timestamp(
            comment["content_offset_seconds"], include_hours
        )
        color = comment["message"].get("user_color", "#000000")
        name = comment["commenter"]["display_name"]

        html_data = f'<span class="timeoffset">{timestamp}</span>'

        # Append badges if we have them available
        if badges and "user_badges" in comment["message"]:
            html_data += _html_handle_badges(badges, comment)

        html_data += f'<span class="author" style="color: {color}">{name}</span>'
        html_data += '<span class="message">'

        if "fragments" in comment["message"]:
            for fragment in comment["message"]["fragments"]:
                if "emoticon" in fragment:
                    emote_id = fragment["emoticon"]["emoticon_id"]
                    html_data += _html_derive_twitch_emote(emote_id, fragment["text"])
                else:
                    fragment_text = fragment["text"]

                    # Append third party emotes if we have them available
                    if ext_emotes:
                        fragment_text = _html_handle_emotes(ext_emotes, fragment_text)
                    else:
                        fragment_text = html.escape(fragment_text)
                    html_data += fragment_text
        else:
            message_text = comment["message"]["body"]
            emotes = {}
            for emote in comment["message"]["emoticons"]:
                emote_name = message_text[emote["begin"] - 1 : emote["end"]]
                emotes[emote_name] = _ttv_emote_to_emote(emote["_id"], emote_name)

            if ext_emotes:
                emotes = {**emotes, **ext_emotes}

            if emotes:
                message_text = _html_handle_emotes(emotes, message_text)
            else:
                message_text = html.escape(message_text)

            html_data += message_text

        html_data += "</span>"

        comments.append(html_data)
    return "<br>\r\n".join(comments)
