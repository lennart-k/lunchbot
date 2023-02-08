import requests


def send_message(
    url: str,
    message: str,
    props: dict = None,
    username: str = "Lunchbot (always hungry)",
):
    r = requests.post(
        url,
        json={
            "username": username,
            "text": message,
            "props": props,
        },
    )
    assert r.status_code == 200
    return r
