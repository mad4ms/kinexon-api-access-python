from typing import Dict
import requests


from bielemetrics_kinexon_api_wrapper import (
    login,
    load_credentials,
)
from bielemetrics_kinexon_api_wrapper import (
    fetch_team_ids,
    fetch_event_ids,
    fetch_game_csv_data,
)

DO_DOWNLOAD = False


def main() -> None:
    """
    Main function to authenticate and fetch metrics and events.
    """
    # Create a session (connection to the server, not game related)
    # session_request = requests.Session()
    # Load credentials from environment variables
    credentials = load_credentials()
    # Authenticate with the session and main login URLs
    session_request = login(credentials)

    endpoint_kinexon_api = credentials["endpoint_kinexon_api"]

    # Fetch team IDs (currently hardcoded)
    team_data = fetch_team_ids(session_request)

    # Example ID for TBV Lemgo Lippe
    team_id = team_data[0]["id"]
    team_name = team_data[0]["name"]
    # Example time range (one month in December 2023), there should be two games
    min_time = "2023-12-01 00:00:00"
    max_time = "2023-12-31 23:59:59"
    # Fetch session IDs
    list_game_ids = fetch_event_ids(
        session_request,
        endpoint_kinexon_api,
        team_id,
        min_time,
        max_time,
    )

    # Print the list of game IDs
    for game in list_game_ids:
        if team_name in game["description"].split("vs.")[0]:
            print(
                f"Time: {game['start_session']}, game: {game['description']}"
            )

    # Example "session_id" (Kinexon calls events "session")
    # not to be confused with the HTTP session ID
    example_game_id = list_game_ids[0]["session_id"]
    example_game_time = (
        list_game_ids[0]["start_session"].replace(" ", "_").replace(":", "-")
    )
    print(f"Example game ID: {example_game_id}, time: {example_game_time}")

    # Download example game
    if DO_DOWNLOAD:
        # Fetch game data
        csv_data = fetch_game_csv_data(
            session_request,
            endpoint_kinexon_api,
            example_game_id,
        )

        if isinstance(csv_data, bytes):
            with open(
                f"{example_game_time}_game_positions_{example_game_id}.csv",
                "wb",
            ) as file:
                file.write(csv_data)
            print("CSV data saved successfully.")
        else:
            print(f"Failed to fetch data: {csv_data}")

    # Close the session
    session_request.close()


if __name__ == "__main__":
    main()
