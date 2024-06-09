import time

from handler.menu import TaskHandler
from handler.parser import get_info
from handler.telegram import send_notify
from config import TIME_REQUEST


def check_info_anime():
    """
    Periodically checks information about anime tasks.
    If changes are detected, sends a notification and updates the information in the file.

    :return: None
    """
    while True:
        time.sleep(TIME_REQUEST)

        # Read saved tasks
        anime_tasks = TaskHandler.read_task_file()

        # Iterate through tasks
        for anime_id, stored_info in anime_tasks.items():
            # Get current information for the anime
            current_info = get_info(anime_id)

            if "N/A" in current_info.values():
                print("No anime tasks found.")
                continue 

            # Compare current and stored information
            if current_info != stored_info:
                print("Changes detected!")

                # Send notification
                send_notify(
                    f"New episode released: {current_info['now_count']} out of {current_info['all_count']}. \nAnime ***{current_info['name']}***"
                )

                # Update information in the file
                TaskHandler.add_task_to_file({anime_id: current_info})
            else:
                print(f"No changes for {current_info['name']}.")
