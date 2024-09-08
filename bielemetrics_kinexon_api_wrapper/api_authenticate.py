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
        "ENDPOINT_KINEXON_SESSION": os.getenv("ENDPOINT_KINEXON_SESSION", ""),
        "ENDPOINT_KINEXON_MAIN": os.getenv("ENDPOINT_KINEXON_MAIN", ""),
        "ENDPOINT_KINEXON_API": os.getenv("ENDPOINT_KINEXON_API", ""),
        "USERNAME_KINEXON_SESSION": os.getenv("USERNAME_KINEXON_SESSION", ""),
        "USERNAME_KINEXON_MAIN": os.getenv("USERNAME_KINEXON_MAIN", ""),
        "PASSWORD_KINEXON_SESSION": os.getenv("PASSWORD_KINEXON_SESSION", ""),
        "PASSWORD_KINEXON_MAIN": os.getenv("PASSWORD_KINEXON_MAIN", ""),
        "API_KEY_KINEXON": os.getenv("API_KEY_KINEXON", ""),
        "API_KEY_SPORTRADAR": os.getenv("API_KEY_SPORTRADAR", ""),
        "ENDPOINT_STORAGE_NEXTCLOUD": os.getenv(
            "ENDPOINT_STORAGE_NEXTCLOUD", ""
        ),
        "USERNAME_STORAGE_NEXTCLOUD": os.getenv(
            "USERNAME_STORAGE_NEXTCLOUD", ""
        ),
        "PASSWORD_STORAGE_NEXTCLOUD": os.getenv(
            "PASSWORD_STORAGE_NEXTCLOUD", ""
        ),
        "PATH_STORAGE_IN_NEXTCLOUD": os.getenv(
            "PATH_STORAGE_IN_NEXTCLOUD", ""
        ),
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
                f"SSL certificate not verified for endpoint {endpoint}: Error: {e}"
            )
            pass
    else:
        payload = {"login": {"username": username, "password": password}}
        try:
            response = login_session.post(endpoint, json=payload)
        except Exception as e:
            response = login_session.post(endpoint, json=payload, verify=False)
            logger.warning(
                f"SSL certificate not verified for endpoint {endpoint}: Error: {e}"
            )
            pass

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
        creds["USERNAME_KINEXON_SESSION"],
        creds["PASSWORD_KINEXON_SESSION"],
        creds["ENDPOINT_KINEXON_SESSION"],
        use_basic_auth=True,
    )
    authenticate(
        session,
        creds["USERNAME_KINEXON_MAIN"],
        creds["PASSWORD_KINEXON_MAIN"],
        creds["ENDPOINT_KINEXON_MAIN"],
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
