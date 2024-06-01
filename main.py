from src.auth import *
from src.data_retrieval import *


DO_DOWNLOAD = True


def login(session: requests.Session, credentials: Dict[str, str]) -> None:
    authenticate_basic_auth(
        session,
        credentials["session_username"],
        credentials["session_password"],
    )
    authenticate_main(
        session, credentials["main_username"], credentials["main_password"]
    )


def main() -> None:
    """
    Main function to authenticate and fetch metrics and events.
    """
    # Create a session (connection to the server, not game related)
    session = requests.Session()
    # Load credentials from environment variables
    my_credentials = load_credentials()
    # Authenticate with the session and main login URLs
    login(session, my_credentials)

    # Fetch team IDs (currently hardcoded)
    team_data = fetch_team_ids(session)

    # Example ID for TBV Lemgo Lippe
    team_id = team_data[0]["id"]
    # Example time range
    min_time = "2023-12-01 00:00:00"
    max_time = "2023-12-31 23:59:59"
    # Fetch session IDs
    list_game_ids = fetch_event_ids(session, team_id, min_time, max_time)

    # Print the list of game IDs
    for game in list_game_ids:
        print(f"Time: {game['start_session']}, game: {game['description']}")

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
        csv_data = fetch_game_csv_data(session, example_game_id)

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
    session.close()


if __name__ == "__main__":
    main()
