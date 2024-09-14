"""This module contains functions to retrieve data from the Kinexon API."""

import os
import sys
import logging
from typing import Union, Tuple, Dict, Any, List
import requests
from requests import Session
from tqdm import tqdm
from bielemetrics_kinexon_api_wrapper import make_api_request

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_team_ids(
    session: requests.Session,
) -> Union[List[Dict[str, Any]], Tuple[int, str]]:
    """
    Fetch the list of team IDs.

    Args:
        session (requests.Session): The session object to use.

    Returns:
        list: The list of team IDs and names if successful.
        tuple: A tuple containing the status code and error message if failed.
    """

    # Assuming team_data is fetched from an endpoint, currently hardcoded
    team_data = [
        {"id": 32, "name": "VfL Gummersbach"},
        {"id": 2, "name": "TV Bittenfeld"},
        {"id": 8, "name": "TSV Hannover-Burgdorf"},
        {"id": 18, "name": "THW Kiel"},
        {"id": 33, "name": "ThSV Eisenach"},
        {"id": 5, "name": "TBV Lemgo Lippe"},
        {"id": 12, "name": "SG Flensburg-Handewitt"},
        {"id": 16, "name": "SC Magdeburg"},
        {"id": 9, "name": "SC DHfK Leipzig"},
        {"id": 7, "name": "Rhein-Neckar Löwen"},
        {"id": 6, "name": "MT Melsungen"},
        {"id": 23, "name": "HSV Hamburg"},
        {"id": 3, "name": "HSG Wetzlar"},
        {"id": 2, "name": "HC Erlangen"},
        {"id": 10, "name": "HBW Balingen-Weilstetten"},
        {"id": 13, "name": "Füchse Berlin"},
        {"id": 11, "name": "Frisch Auf Göppingen"},
        {"id": 14, "name": "Bergischer HC"},
    ]

    return team_data


def fetch_event_ids(
    session: requests.Session,
    base_url: str,
    team_id: int,
    min_time: str,
    max_time: str,
) -> Union[List[str], Tuple[int, str]]:
    """
    Fetch the event IDs for a given team within a specified time range.

    Args:
        session (requests.Session): The session object to use.
        base_url (str): The base URL for the Kinexon API.
        team_id (int): The ID of the team.
        min_time (str): Start of the range (format yyyy-mm-dd HH:ii:ss) in UTC.
        max_time (str): End of the range (format yyyy-mm-dd HH:ii:ss) in UTC.

    Returns:
        list: The list of session IDs if successful.
        tuple: A tuple containing the status code and error message if failed.
    """
    url = f"{base_url}/teams/{team_id}/sessions-and-phases"
    params = {"min": min_time, "max": max_time}
    headers = {"Accept": "application/json"}

    response = make_api_request(
        session, url, method="GET", headers=headers, params=params
    )

    if response.headers.get("Content-Type") == "application/json":
        return response.json()
    else:
        return response.status_code, response.text


def get_available_metrics_and_events(
    session: requests.Session, base_url: str, api_key: str
) -> Union[Dict[str, Any], Tuple[int, str]]:
    """
    Fetch the list of available metrics and events.

    Args:
        session (requests.Session): The session object to use.
        base_url (str): The base URL for the Kinexon API.
        api_key (str): The API key for authentication.

    Returns:
        dict: The JSON response containing available metrics
        and events or an error message.
    """
    url = f"{base_url}/statistics/list"
    params = {"apiKey": api_key}
    headers = {"Accept": "*/*"}

    response = make_api_request(
        session, url, method="GET", headers=headers, params=params
    )

    if response.status_code == 200:
        return response
    else:
        return response.status_code, response.text


def fetch_game_csv_data(
    session: requests.Session,
    base_url: str,
    session_id: str,
    update_rate: int = 20,
    compress_output: bool = False,
    use_local_frame_imu: bool = False,
    center_origin: bool = False,
    group_by_timestamp: bool = False,
    players: str = None,
) -> Union[bytes, Tuple[int, str]]:
    """
    Fetch the CSV data for the positions of a game session.

    Args:
        session (requests.Session): The session object to use.
        base_url (str): The base URL for the Kinexon API.
        session_id (str): The identifier of the session.
        update_rate (int): The update rate for exported values.
        compress_output (bool): Compress the output.
        use_local_frame_imu (bool): Export accelerometer data .
        center_origin (bool): Set the origin to the center.
        group_by_timestamp (bool): Group players by timestamp.
        players (str): Comma-separated player IDs.

    Returns:
        bytes: The CSV data as bytes if successful.
        tuple: A tuple containing the status code and error message if failed.
    """
    url = f"{base_url}/export/positions/session/{session_id}"
    params = {
        "updateRate": update_rate,
        "compressOutput": str(compress_output).lower(),
        "useLocalFrameIMU": str(use_local_frame_imu).lower(),
        "centerOrigin": str(center_origin).lower(),
        "groupByTimestamp": str(group_by_timestamp).lower(),
    }

    if players:
        params["players"] = players

    headers = {"Accept": "text/csv"}

    print(f"Fetching CSV data for session ID: {session_id} ...")

    response = make_api_request(
        session, url, method="GET", headers=headers, params=params, stream=True
    )

    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 1048576  # 1 MB
        csv_data = bytearray()

        with tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Downloading CSV"
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                csv_data.extend(chunk)
                progress_bar.update(len(chunk))

        return bytes(csv_data)
    else:
        raise Exception(f"Failed to download CSV data: {response.status_code}")


if __name__ == "__main__":

    from bielemetrics_kinexon_api_wrapper.api_authenticate import (
        login,
        load_credentials,
    )

    # Example usage
    credentials = load_credentials()

    my_login_session = login(credentials)
    try:
        logger.info("Login successful! 🥳 🥳 🥳")
        logger.info("You can now make requests to the Kinexon API.")
    except Exception as e:
        logger.error(f"Failed to authenticate: {e}")
        sys.exit(1)

    team_data = fetch_team_ids(my_login_session)

    logger.info("Team IDs:")
    for team in team_data:
        logger.info(f"ID: {team['id']}, Name: {team['name']}")

    team_id = team_data[0]["id"]
    min_time = "2021-01-01 00:00:00"
    max_time = "2021-12-31 23:59:59"

    result_event_ids = fetch_event_ids(
        my_login_session,
        credentials["endpoint_kinexon_api"],
        team_id,
        min_time,
        max_time,
    )
    if isinstance(result_event_ids, tuple):
        status_code, error = result_event_ids
    else:
        session_data = result_event_ids
        error = None

    if error:
        logger.error(f"Failed to fetch event IDs: {error}")
        sys.exit(1)

    logger.info("Event IDs:")
    for session in session_data:
        logger.info(
            f"ID: {session['session_id']}, Name: {session['description']}"
        )

    result_avail_metrics = get_available_metrics_and_events(
        my_login_session,
        credentials["endpoint_kinexon_api"],
        credentials["api_key_kinexon"],
    )
    if isinstance(result_avail_metrics, tuple):
        status_code, error = result_avail_metrics
    else:
        metrics_and_events = result_avail_metrics
        error = None
    if error:
        logger.error(f"Failed to fetch available metrics and events: {error}")
        sys.exit(1)

    logger.info("Available metrics and events:")
    for metric in metrics_and_events["metrics"]:
        logger.info(f"Metric: {metric}")
