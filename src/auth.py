import os
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from requests import Session

# Endpoints
POPUP_LOGIN_URL: str = "https://hbl-cloud.kinexon.com/"
LOGIN_URL: str = "https://hbl-cloud.kinexon.com/checklogin"


# Read sensitive information from environment variables
POPUP_USERNAME: str = os.getenv("POPUP_USERNAME", "")
POPUP_PASSWORD: str = os.getenv("POPUP_PASSWORD", "")
MAIN_USERNAME: str = os.getenv("MAIN_USERNAME", "")
MAIN_PASSWORD: str = os.getenv("MAIN_PASSWORD", "")


# Main login payload
main_login_payload: dict = {
    "login": {"username": MAIN_USERNAME, "password": MAIN_PASSWORD}
}


def authenticate_basic_auth(session: Session) -> None:
    """
    Authenticate with the main Kinexon login URL.
    It is usually the popup that appears when you visit the Kinexon cloud.

    Args:
        session (requests.Session): The session object to use.

    Raises:
        requests.exceptions.HTTPError: If authentication fails.
    """
    session.auth = HTTPBasicAuth(POPUP_USERNAME, POPUP_PASSWORD)
    response = session.get(POPUP_LOGIN_URL)
    if response.status_code != 200:
        raise HTTPError(f"Failed to login to {POPUP_LOGIN_URL}")
    print(f"Successfully logged in to {POPUP_LOGIN_URL}")


def authenticate_main(session: Session) -> None:
    """
    Authenticate with the main login URL.
    You should have the main username and password to use this function.

    Args:
        session (requests.Session): The session object to use.

    Raises:
        Exception: If authentication fails.
    """
    response = session.post(LOGIN_URL, json=main_login_payload)
    if response.status_code != 200:
        raise HTTPError(f"Failed to login to {LOGIN_URL}")
    print(f"Successfully logged in to {LOGIN_URL}")
