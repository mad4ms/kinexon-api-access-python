"""
Authenticate with the Kinexon API using requests.
"""

import os
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

# Endpoints
SESSION_LOGIN_URL: str = "https://hbl-cloud.kinexon.com/"
LOGIN_URL: str = "https://hbl-cloud.kinexon.com/checklogin"


def load_credentials() -> dict[str, str]:
    """
    Load credentials from environment variables.

    Returns:
        dict[str, str]: The credentials as a dictionary.
    """
    return {
        "session_username": os.getenv("SESSION_USERNAME", ""),
        "session_password": os.getenv("SESSION_PASSWORD", ""),
        "main_username": os.getenv("MAIN_USERNAME", ""),
        "main_password": os.getenv("MAIN_PASSWORD", ""),
        "API_KEY": os.getenv("KINEXON_API_KEY", ""),
    }


def authenticate_basic_auth(
    session: Session, session_username: str, session_password: str
) -> None:
    """
    Authenticate with the popup login URL using Basic HTTP Authentication.

    Args:
        session (requests.Session): The session object to use.
        session_username (str): The username for the popup authentication.
        session_password (str): The password for the popup authentication.

    Raises:
        requests.exceptions.HTTPError: If authentication fails.
    """
    session.auth = HTTPBasicAuth(session_username, session_password)
    response = session.get(SESSION_LOGIN_URL)
    if response.status_code != 200:
        raise HTTPError(f"Failed to login to {SESSION_LOGIN_URL}")
    print(f"Successfully logged in to {SESSION_LOGIN_URL}")


def authenticate_main(
    session: Session, main_username: str, main_password: str
) -> None:
    """
    Authenticate with the main login URL.

    Args:
        session (requests.Session): The session object to use.
        main_username (str): The username for the main authentication.
        main_password (str): The password for the main authentication.

    Raises:
        requests.exceptions.HTTPError: If authentication fails.
    """
    login_payload = {
        "login": {"username": main_username, "password": main_password}
    }
    response = session.post(LOGIN_URL, json=login_payload)
    if response.status_code != 200:
        raise HTTPError(f"Failed to login to {LOGIN_URL}")
    print(f"Successfully logged in to {LOGIN_URL}")


if __name__ == "__main__":
    # Example usage
    with Session() as my_session:
        # load credentials from environment variables
        credentials = load_credentials()

        authenticate_basic_auth(
            my_session,
            credentials["session_username"],
            credentials["session_password"],
        )
        authenticate_main(
            my_session,
            credentials["main_username"],
            credentials["main_password"],
        )

        print(">> Login successful! 🥳 🥳 🥳")
        print(
            "\t>>You can now make requests to the Kinexon API."
            " See data_retrieval.py for an example."
        )
