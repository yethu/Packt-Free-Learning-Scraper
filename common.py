import re


def build_headers(referer: str, user_agent: str) -> dict:
    return {
        'Referer': referer,
        'User-Agent': user_agent
    }


def parse_title(title):
    return re.sub(r'\s?\[eBook\]', '', title.strip())
