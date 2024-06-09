import json
import time
from functools import partial

from config import URL_JSON
import pywebio.input as inp
from handler.parser import get_info
from pywebio.output import clear, put_button, put_table, toast, use_scope
from pywebio.session import run_js


class TaskHandler:
    @staticmethod
    def read_task_file() -> dict| None:
        """
        Reads a JSON file "tasks.json" and returns its content as a Python dictionary.
        If the file does not exist, it creates an empty file and returns an empty dictionary.
        If there is an error decoding the JSON, it returns None.

        Returns:
            dict or None: A Python dictionary containing the data from the "tasks.json" file,
            or None in case of an error.
        """
        try:
            with open(URL_JSON, encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("File 'tasks.json' not found. Creating an empty file.")
            with open(URL_JSON, "w", encoding="utf-8") as file:
                json.dump({}, file)
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in 'tasks.json': {e}")
            return None

    @staticmethod
    def delete_task_in_file(link, update=True):
        """
        Deletes a task entry from the "tasks.json" file and optionally updates the task list.

        Args:
            link (str): The key (link) of the task to be deleted.
            update (bool, optional): Whether to update the task list. Default is True.

        If the specified link does not exist in the task list, a message is printed indicating
        that the key is not found. If update is True, a toast message is displayed to indicate
        the successful deletion, and the task list is refreshed.

        Returns:
            None
        """
        last_changes = (
            TaskHandler.read_task_file()
        )  # Read the current task list from "tasks.json"
        try:
            del last_changes[link]  # Remove the task with the specified link
            with open(URL_JSON, "w", encoding="utf-8") as file:
                json.dump(
                    last_changes, file, indent=4
                )  # Write the updated task list back to the file

        except KeyError:
            print(
                "Key not found in the task list"
            )  # Print a message if the specified key is not found

        if update:
            toast(
                "Task successfully deleted"
            )  # Display a toast message indicating successful deletion
            time.sleep(1)
            TaskHandler.get_task_list()  # Optionally update the task list

    @staticmethod
    def add_task_to_file(date: dict):
        """
        Adds a task to the "tasks.json" file.

        Args:
            date (dict): A dictionary representing the task to be added.

        The function reads the current task list from "tasks.json," merges it with the provided
        dictionary, and writes the updated task list back to the file. The resulting dictionary
        should have a unique key for each task.

        Returns:
            None
        """
        last_changes = (
            TaskHandler.read_task_file()
        )  # Read the current task list from "tasks.json"
        result = (
            last_changes | date
        )  # Merge the existing task list with the provided dictionary

        with open(URL_JSON, "w", encoding="utf-8") as file:
            json.dump(
                result, file, indent=4
            )  # Write the updated task list back to the file

    @staticmethod
    def get_task_list():
        """
        Displays a task list, including a button to delete tasks, in a PyWebIO scope.

        The function clears the previous content, reads the task list from "tasks.json,"
        and displays the tasks in a table format. Each task includes a "Delete" button that
        allows users to remove the task. There is also a "Back" button to return to the previous page.

        Returns:
            None
        """
        clear()  # Clear the previous content

        result = []
        tasks = TaskHandler.read_task_file()  # Read the task list from "tasks.json"

        for link, values in tasks.items():
            result.append(
                [
                    *list(values.values()),  # Extract task values from the dictionary
                    put_button(
                        "Удалить",
                        color="danger",
                        onclick=partial(TaskHandler.delete_task_in_file, link),
                    ),  # Create a delete button for each task
                ]
            )

        with use_scope("table", clear=True):
            put_button(
                "Back", color="dark", onclick=lambda: run_js("location.reload()")
            ).style("margin-top: 60px; text-align: right")
            put_table(
                result, header=["Name", "Total Episodes", "Episodes Released", "Delete"]
            ).style("margin-top: 30px; display: table")

    @staticmethod
    async def add_task_in_list():
        """
        This function allows the user to add a new task to the list by providing a link to an anime.
        The function validates the input URL, retrieves information about the anime, and adds it to the task list.

        Returns:
            None
        """
        input_url = await inp.input(
            "Enter the link to the anime to get notifications",
            required=True,
            placeholder="https://animego.org/anime/doktor-stoun-novyy-mir-chast-2-2388",
            type=inp.URL,
        )

        response_info = get_info(input_url)
        if response_info.get("name") == "N/A":
            toast(
                "Failed to retrieve anime information. Please make sure the link is correct.",
                position="center",
                color="error",
            )
        else:
            TaskHandler.add_task_to_file({input_url: response_info})
            toast("Task successfully created", position="center", color="success")
