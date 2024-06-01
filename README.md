# Kinexon REST API Authentication and Usage Example

Welcome to the Kinexon REST API Authentication and Usage Example for Python.

Due to the lack of available documentation on the Kinexon API (i'm not mad, just disappointed), I am providing this open source script to assist you.


Currently a **WIP**. If you find this repo useful, consider leaving a star, or not. Your choice. Not affiliated with Kinexon.

Used in the soon-to-be-opensource™ framework **BieLeMetrics**, which is a Python project for automated multimodal data processing applied in the paper [Expected Goals Prediction in Professional Handball using Synchronized Event and Positional Data](https://www.researchgate.net/publication/375086950_Expected_Goals_Prediction_in_Professional_Handball_using_Synchronized_Event_and_Positional_Data).

## Overview
This example demonstrates a comprehensive approach for interacting with the Kinexon REST API. It includes a two-step authentication process, session management with HTTP cookies, and API key handling for secure data access from the Kinexon Cloud.

## Key Features
- **Two-Step Authentication**: First, authenticate using HTTP Basic Authentication, followed by a session-based login.
- **Session Management**: Utilizes HTTP cookies to maintain session state across multiple API requests.
- **API Key Handling**: Demonstrates secure usage of API keys for accessing protected endpoints.
- **Retrieval Examples**: Shows how to fetch and download positional information and further data.

## Getting Started

### Prerequisites
- Python 3.6+
- `requests` library (`pip install requests`)


Clone this repository:
```
git clone https://github.com/mad4ms/kinexon-api-access-python
```



### Credentials & Environment Variables
Set the following environment variables with your credentials and API information:

```sh
export SESSION_USERNAME='your_session_username' # username for the popup on the website
export SESSION_PASSWORD='your_session_password' # password for the popup on the website
export MAIN_USERNAME='your_main_username' # username for the login site
export MAIN_PASSWORD='your_main_password' # password for the login site
export KINEXON_API_KEY='your_api_key' # create API key in profile settings
```
Explanation:

- **SESSION_USERNAME** and **SESSION_PASSWORD**: Credentials for initial authentication using HTTP Basic Authentication.
- **MAIN_USERNAME** and **MAIN_PASSWORD**: Credentials for the main site authentication using a POST request payload.
- **KINEXON_API_KEY**: API key created in the user profile under the Teams tab. Ensure to confirm your password again to save your profile and store the API_KEY.

### Usage
Change into project directory:
```sh
cd kinexon-api-access-python
```
Test authentication with:
```sh
python src/auth.py
```
On success, explore and run the script:

```sh
python main.py
```
Watch as the script performs the two-step login and fetches a game.

## Troubleshooting
- Failed to Login: Double-check your credentials. Ensure they match those provided by the Kinexon Cloud and are correctly set to the environment.
- Connection Errors: Ensure you have an active internet connection.
- API Changes: Be aware that the Kinexon API is young and prone to changes.
## Contributing
Feel free to contribute to this project. You're welcome to fork, submit PRs, or open issues.

## License
This project is licensed under the MIT License.