#!/usr/bin/env python3
from mensautils.parser.desy import get_canteen_data as get_desy
from mensautils.parser.studierendenwerk import get_canteen_data
from mensautils.parser.canteen_result import Serving
from datetime import date
from .const import CFEL_ID, DESY_ID
from .config import WEBHOOK_URL, IMAGE_FOLDER
import logging
from .mattermost import send_message
# TODO: Configurable preview provider
from lunchbot.preview.craiyon import create_menu_images

LOGGER = logging.getLogger(__name__)

MENSA_TODAY_URL = "https://mensa.mafiasi.de/api/canteens/{canteen}/today/"


def get_menu_today(canteen: str | int, english: bool = False) -> list[Serving]:
    LOGGER.info(f"Requesting the menu for {canteen}")
    if canteen == DESY_ID:
        canteen_data = get_desy(english=english)
    elif type(canteen) == int:
        canteen_data = get_canteen_data(canteen, english=english)
    else:
        raise ValueError("canteen needs to be either 'desy' or int")
    servings = canteen_data.servings
    today = date.today()
    return [
        serving
        for serving in servings
        if (
            today.year == serving.day.year
            and today.month == serving.day.month
            and today.day == serving.day.day
        )
    ]


def menu_to_table(
    label: str,
    menu: list[Serving],
    menu_de: list[Serving],
    images: list[str] = None,
    is_header: bool = True,
) -> str:
    if is_header:
        header = (
            f"| **{label}** | Dish | Price |\n"
            if not images
            else f"| **{label}** | Dish | Price | Preview |\n"
        )
        header += (
            "| --- | ---- | ----- |\n"
            if not images
            else "| --- | ---- | ----- | ------- |\n"
        )
    else:
        header = f"| **{label}** | | |\n" if not images else f"| **{label}** | | | |\n"

    table = header

    for i, (item, item_de) in enumerate(zip(menu, menu_de)):
        title = f"{item_de.title} $\\\\$ {item.title}"
        table += f"|{'vegan' if item.vegan else ''}{'vegetarian' if item.vegetarian else ''} | {title} | {item.price} |"
        if images:
            table += f"![Preview]({images[i]} =75) |"
        table += "\n"

    return table.rstrip()


async def run_message():
    menu_desy = get_menu_today(DESY_ID, True)
    menu_desy_de = get_menu_today(DESY_ID, False)
    menu_cfel = get_menu_today(CFEL_ID, True)
    menu_cfel_de = get_menu_today(CFEL_ID, False)

    images_desy = await create_menu_images(menu_desy, IMAGE_FOLDER)
    images_cfel = await create_menu_images(menu_cfel, IMAGE_FOLDER)

    message = "\n".join(
        [
            menu_to_table("DESY canteen", menu_desy, menu_desy_de, images_desy),
            menu_to_table(
                "Cafe CFEL", menu_cfel, menu_cfel_de, images_cfel, is_header=False
            ),
        ]
    )

    card = "Lunchbot looks up today's menus so you don't have to.\n"

    r = send_message(WEBHOOK_URL, message, props=dict(card=card))
    assert r.status_code == 200, (r.status_code, r.text)
