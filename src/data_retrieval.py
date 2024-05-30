import os
from typing import Union, Tuple, Dict, Any, List
import requests
from requests import Session
from tqdm import tqdm

# Endpoint
BASE_URL: str = "https://hbl-cloud.kinexon.com/public/v1"

# Read API key from environment variables
API_KEY: str = os.getenv("KINEXON_API_KEY", "")


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
    if session is not None:
        team_data = [
            {"id": 5, "name": "TBV Lemgo Lippe"},
            {"id": 6, "name": "Rhein-Neckar Löwen"},
        ]
        return team_data
    else:
        return 400, "Session is None"


def fetch_session_ids(
    session: requests.Session, team_id: int, min_time: str, max_time: str
) -> Union[List[str], Tuple[int, str]]:
    """
    Fetch the session IDs for a given team within a specified time range.

    Args:
        session (requests.Session): The session object to use.
        team_id (int): The ID of the team.
        min_time (str): Start of the range (format yyyy-mm-dd HH:ii:ss) in UTC.
        max_time (str): End of the range (format yyyy-mm-dd HH:ii:ss) in UTC.

    Returns:
        list: The list of session IDs if successful.
        tuple: A tuple containing the status code and error message if failed.
    """
    url = f"{BASE_URL}/teams/{team_id}/sessions-and-phases"
    params = {"min": min_time, "max": max_time}
    headers = {"Accept": "application/json"}

    response = session.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            session_ids = [session for session in data]
            return session_ids
        else:
            return []
    else:
        return response.status_code, response.text


def fetch_game_csv_data(
    session: requests.Session,
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
        session_id (str): The identifier of the session.
        update_rate (int): The update rate for exported values.
        compress_output (bool): Compress the output.
        use_local_frame_imu (bool): Export accelerometer data in local frame.
        center_origin (bool): Set the origin of the position data to the center of each field.
        group_by_timestamp (bool): Group players by timestamp.
        players (str): Comma-separated player IDs.

    Returns:
        bytes: The CSV data as bytes if successful.
        tuple: A tuple containing the status code and error message if failed.
    """
    base_url = f"{BASE_URL}/export/positions/session"
    url = f"{base_url}/{session_id}"

    params = {
        "updateRate": update_rate,
        "compressOutput": str(compress_output).lower(),
        "useLocalFrameIMU": str(use_local_frame_imu).lower(),
        "centerOrigin": str(center_origin).lower(),
        "groupByTimestamp": str(group_by_timestamp).lower(),
    }

    if players:
        params["players"] = players

    headers = {
        "Accept": "text/csv",
    }

    response = session.get(url, params=params, headers=headers, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 1024
        csv_data = bytearray()

        with tqdm(
            total=total_size, unit="B", unit_scale=True, desc="Downloading CSV"
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                csv_data.extend(chunk)
                progress_bar.update(len(chunk))

        return bytes(csv_data)
    else:
        return response.status_code, response.text


def get_available_metrics_and_events(
    session: Session,
) -> Union[Dict[str, Any], Tuple[int, str]]:
    """
    Fetch the list of available metrics and events.

    Args:
        session (requests.Session): The session object to use.

    Returns:
        dict: The JSON response containing available metrics and events
        or an error message.
    """
    url: str = f"{BASE_URL}/statistics/list"
    params: dict = {"apiKey": API_KEY}
    headers: dict = {"accept": "*/*"}
    response = session.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code, response.text