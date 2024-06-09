import os
import threading

from handler.menu import TaskHandler
from handler.parser_check import check_info_anime
from pywebio import start_server
from pywebio.output import clear, put_buttons, put_image


async def main():
    clear()
    show_logo()
    show_buttons()


def show_logo():
    logo_path = os.path.join("aninotify/data", "logo.png")
    put_image(open(logo_path, "rb").read()).style(
        "width: 50%; margin: auto; float: left"
    )


def show_buttons():
    button_labels = {"add": "Add", "watch": "View"}
    button_colors = {"add": "success", "watch": "primary"}
    buttons = [
        dict(label=button_labels["add"], value="add", color=button_colors["add"]),
        dict(label=button_labels["watch"], value="watch", color=button_colors["watch"]),
    ]
    onclick = [TaskHandler.add_task_in_list, TaskHandler.get_task_list]
    put_buttons(buttons, onclick=onclick).style(
        "margin-top: 60px; text-align: center; float: right"
    )


if __name__ == "__main__":
    PORT = 8080
    threading.Thread(target=check_info_anime).start()
    start_server(main, port=PORT)
