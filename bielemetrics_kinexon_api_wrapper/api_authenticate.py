""" This module provides functions to authenticate with the Kinexon API. """

import os
import logging
from typing import Dict
from requests import Session, HTTPError
from requests.auth import HTTPBasicAuth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_credentials() -> Dict[str, str]:
    """
    Load credentials from environment variables.

    Returns:
        dict: The credentials as a dictionary.
    """
    return {
        "username_kinexon_session": os.getenv("USERNAME_KINEXON_SESSION", ""),
        "password_kinexon_session": os.getenv("PASSWORD_KINEXON_SESSION", ""),
        "endpoint_kinexon_session": os.getenv("ENDPOINT_KINEXON_SESSION", ""),
        "username_kinexon_main": os.getenv("USERNAME_KINEXON_MAIN", ""),
        "password_kinexon_main": os.getenv("PASSWORD_KINEXON_MAIN", ""),
        "endpoint_kinexon_main": os.getenv("ENDPOINT_KINEXON_MAIN", ""),
        "api_key_kinexon": os.getenv("API_KEY_KINEXON", ""),
        "endpoint_kinexon_api": os.getenv("ENDPOINT_KINEXON_API", ""),
    }


def authenticate(
    login_session: Session,
    username: str,
    password: str,
    endpoint: str,
    use_basic_auth: bool = False,
) -> None:
    """
    Authenticate with the given endpoint.

    Args:
        login_session (Session): The session object to use.
        username (str): The username for authentication.
        password (str): The password for authentication.
        endpoint (str): The endpoint for authentication.
        use_basic_auth (bool): Whether to use basic HTTP authentication.

    Raises:
        HTTPError: If authentication fails.
    """
    if use_basic_auth:
        login_session.auth = HTTPBasicAuth(username, password)
        try:
            response = login_session.get(endpoint)
        except Exception as e:
            response = login_session.get(endpoint, verify=False)
            logger.warning(
                f"Warning. SSL certificate not verified for endpoint {endpoint}: Error: {e}"
            )
            pass
    else:
        payload = {"login": {"username": username, "password": password}}
        response = login_session.post(endpoint, json=payload)

    if response.status_code != 200:
        logger.error(
            f"Failed to login to {endpoint}: {response.status_code} "
            f"{response.text}"
        )
        response.raise_for_status()

    logger.debug(f"Successfully logged in to {endpoint}")


def login(creds: Dict[str, str]) -> Session:
    """
    Authenticate with the Kinexon API using the provided credentials.

    Args:
        creds (dict): The credentials to use for authentication.

    Returns:
        Session: The authenticated session object.
    """
    session = Session()
    authenticate(
        session,
        creds["username_kinexon_session"],
        creds["password_kinexon_session"],
        creds["endpoint_kinexon_session"],
        use_basic_auth=True,
    )
    authenticate(
        session,
        creds["username_kinexon_main"],
        creds["password_kinexon_main"],
        creds["endpoint_kinexon_main"],
    )
    return session


if __name__ == "__main__":
    # Example usage
    credentials = load_credentials()

    my_login_session = login(credentials)
    try:
        login(credentials)
        logger.info("Login successful! 🥳 🥳 🥳")
        logger.info("You can now make requests to the Kinexon API.")
    except HTTPError as e:
        logger.exception(f"An error occurred during authentication: {e}")
