import os
import sys
import logging
from requests import Session, HTTPError

from bielemetrics_kinexon_api_wrapper import (
    load_credentials,
    login,
)
from bielemetrics_kinexon_api_wrapper import (
    get_available_metrics_and_events,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_api_status():
    credentials = load_credentials()

    try:
        # Authenticate with session and main credentials
        my_login_session = login(credentials)
        logger.info("Login successful! 🥳 🥳 🥳")

        # Use the session to check API status
        api_status = get_available_metrics_and_events(
            my_login_session,
            credentials["endpoint_kinexon_api"],
            credentials["api_key_kinexon"],
        )

        if isinstance(api_status, dict):
            logger.info("API is available and returned metrics and events.")
            print("::set-output name=api_status::available")
        else:
            logger.error("API is unavailable.")
            print("::set-output name=api_status::unavailable")

    except HTTPError as e:
        logger.exception(f"An error occurred during authentication: {e}")
        print("::set-output name=api_status::unavailable")


if __name__ == "__main__":
    check_api_status()
