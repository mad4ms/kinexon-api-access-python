from src.auth import *
from src.data_retrieval import *


def main() -> None:
    """
    Main function to authenticate and fetch metrics and events.
    """
    session = requests.Session()

    # Authentication
    authenticate_basic_auth(session)
    authenticate_main(session)

    # Fetch team IDs (currently hardcoded)
    team_data = fetch_team_ids(session)

    if isinstance(team_data, list):
        for team in team_data:
            print(f"Team ID: {team['id']}, Team Name: {team['name']}")
    else:
        print(f"Failed to fetch team IDs: {team_data}")

    # Example ID for TBV Lemgo Lippe
    team_id = team_data[0]["id"]
    # Example time range
    min_time = "2023-12-01 00:00:00"
    max_time = "2023-12-31 23:59:59"
    # Fetch session IDs
    list_session_id_kinexon = fetch_session_ids(
        session, team_id, min_time, max_time
    )

    if isinstance(list_session_id_kinexon, list):
        print(f"Fetched session ID: {list_session_id_kinexon}")
    else:
        print(f"Failed to fetch session ID: {list_session_id_kinexon}")

    for session in list_session_id_kinexon:
        print(
            f"Time: {session['start_session']}, game: {session['description']}"
        )

    # Example session ID
    session_id_kinexon = list_session_id_kinexon[0]["session_id"]

    csv_data = fetch_game_csv_data(session, session_id_kinexon)

    if isinstance(csv_data, bytes):
        with open("game_positions.csv", "wb") as file:
            file.write(csv_data)
        print("CSV data saved successfully.")
    else:
        print(f"Failed to fetch data: {csv_data}")

    session.close()


if __name__ == "__main__":
    main()
