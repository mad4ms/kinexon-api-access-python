""" This module contains functions for making REST API requests. """

import requests
from typing import Union, Dict, Any, Tuple, List
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


def make_api_request(
    session: requests.Session,
    url: str,
    method: str = "GET",
    headers: Dict[str, str] = None,
    params: Dict[str, Any] = None,
    data: Dict[str, Any] = None,
    json_data: Dict[str, Any] = None,
    stream: bool = False,
) -> Union[Dict[str, Any], Tuple[int, str]]:
    """
    Make a REST API request.

    Args:
        session (requests.Session): The session object to use.
        url (str): The endpoint URL.
        method (str): The HTTP method (GET, POST, PUT, DELETE).
        headers (dict): The headers for the request.
        params (dict): The query parameters for the request.
        data (dict): The form data for POST/PUT requests.
        json_data (dict): The JSON data for POST/PUT requests.
        stream (bool): Whether to stream the response (useful for large files).

    Returns:
        dict: The JSON response if successful.
        tuple: A tuple containing the status code and error message if failed.
    """
    try:
        response = session.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            json=json_data,
            stream=stream,
            verify=False,
        )
        response.raise_for_status()

        if response.status_code == 200:
            if response.headers.get("Content-Type") == "application/json":
                return response.json()
            else:
                return response.content
        else:
            return response.status_code, response.text
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return response.status_code, str(e)
