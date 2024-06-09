import requests
from bs4 import BeautifulSoup


def get_info(link: str):
    """
    This function takes a URL link to an anime webpage and retrieves information about the anime.

    Args:
        link (str): The URL of the anime webpage.

    Returns:
        list: A list containing information about the anime. The list includes the following elements:

            1. The anime title (if found) or "N/A" if not found.
            2. Number of episodes to
            3. The number of episodes that have already been released.(if found) or "N/A" if not found.


    If an error occurs during the request or when searching for elements on the page,
    the function returns a list with "N/A" values to indicate the absence of data.
    """
    try:
        # Perform a request to the page
        response = requests.get(link)
        response.raise_for_status()  # Check if the request was successful

        html_resp = response.text
        block = BeautifulSoup(html_resp, "lxml")

        # Find the information
        info = block.find_all("dd", class_="col-6")
        info_episodes = (
            info[1].text if len(info) > 1 else "N/A"
        )  # Check for the presence of the element
        episodes, total_episodes = info_episodes.split("/")
        episodes, total_episodes = (
            episodes.replace(" ", ""),
            total_episodes.replace(" ", ""),
        )

        anime_title = block.find("div", class_="anime-title")
        anime_title = (
            anime_title.find("h1").text if anime_title else "N/A"
        )  # Check for the presence of the element

        # Return the result as a dictionary
        result = {
            "name": anime_title,
            "all_count": total_episodes,
            "now_count": episodes,
        }
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error during request execution: {e}")
        return {
            "name": "N/A",
            "all_count": "N/A",
            "now_count": "N/A",
        }  # Return default values in case of an error
    except AttributeError as e:
        print(f"Attribute error occurred: {e}")
        return {
            "name": "N/A",
            "all_count": "N/A",
            "now_count": "N/A",
        }  # Return default values in case of an error
