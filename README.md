
# Bielemetrics Kinexon API Wrapper

This package provides a wrapper for the Kinexon API, including functions for authentication and data retrieval. It simplifies interacting with the Kinexon REST API, making it easier to authenticate and retrieve data.

## Table of Contents
- [Bielemetrics Kinexon API Wrapper](#bielemetrics-kinexon-api-wrapper)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
- [Bielemetrics Kinexon API Wrapper](#bielemetrics-kinexon-api-wrapper-1)
  - [Table of Contents](#table-of-contents-1)
  - [Installation](#installation-1)
  - [Usage](#usage)
    - [Authentication](#authentication)
    - [Fetching Data](#fetching-data)
- [Kinexon REST API Authentication and Usage Example](#kinexon-rest-api-authentication-and-usage-example)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Credentials \& Environment Variables](#credentials--environment-variables)
    - [Usage](#usage-1)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

## Installation

You can install the package using pip:

```bash
pip install bielemetrics-kinexon-api-wrapper
```

## Usage
### Authentication
First, load your credentials and authenticate with the Kinexon API.

```python
import requests
from bielemetrics_kinexon_api_wrapper import login

# Load credentials from environment variables
credentials = load_credentials()

# Create a session by logging in
session_kinexon = login(credentials)
```

    
### Fetching Data
You can fetch different types of data using the provided functions.

Fetch Team IDs
```python
from bielemetrics_kinexon_api_wrapper import fetch_team_ids

team_ids = fetch_team_ids(session)
print(team_ids)
```

# Kinexon REST API Authentication and Usage Example

![API Status](./badge.svg)

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
export USERNAME_KINEXON_SESSION='your_session_username' # Username for the popup on the website
export PASSWORD_KINEXON_SESSION='your_session_password' # Password for the popup on the website
export ENDPOINT_KINEXON_SESSION='https://your_session_endpoint' # Endpoint for the session login

export USERNAME_KINEXON_MAIN='your_main_username' # Username for the main login site
export PASSWORD_KINEXON_MAIN='your_main_password' # Password for the main login site
export ENDPOINT_KINEXON_MAIN='https://your_main_endpoint' # Endpoint for the main login

export API_KEY_KINEXON='your_api_key' # API key created in profile settings
export ENDPOINT_KINEXON_API='https://your_api_endpoint' # Base URL for the Kinexon API


```
Explanation:

- **USERNAME_KINEXON_SESSION** and **PASSWORD_KINEXON_SESSION**: Credentials for initial authentication using HTTP Basic Authentication. **ENDPOINT_KINEXON_SESSION** is usually `https://hbl-cloud.kinexon.com/`
- **USERNAME_KINEXON_MAIN** and **PASSWORD_KINEXON_MAIN**: Credentials for the main site authentication using a POST request payload. **ENDPOINT_KINEXON_MAIN** is usually `https://hbl-cloud.kinexon.com/checklogin/`
- **KINEXON_API_KEY**: API key created in the user profile under the Teams tab. Ensure to confirm your password again to save your profile and store the API_KEY. **ENDPOINT_KINEXON_API**  is usually `https://hbl-cloud.kinexon.com/public/v1/`

Hack for faster auth:
- Create a `.env` file in the repo with credentials (will be ignored by .gitignore):
```
USERNAME_KINEXON_SESSION='your_session_username'
PASSWORD_KINEXON_SESSION='your_session_password'
...
```
`python-dotenv` package will detect `.env` file and use it. No need for cumbersome environment entries. 
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