# Kinexon Cloud Authentication Script

Welcome to the Kinexon Cloud Authentication Script. This script performs a two-step authentication process and fetches available games from the Kinexon Cloud. 
Currently a **WIP**.
## Features
- **Popup Authentication:** Log in through a popup URL because why have one login step when you can have two?
- **Main Site Authentication:** Log in to the main site after the popup, because who doesn't love redundancy?
- **Fetch Metrics and Events:** Retrieve a list of available metrics and events. Because that's what you actually wanted, right?
- **Fetch Position files of Games:** That's what I actually wanted, so here we are.

## Getting Started

### Prerequisites
- Python 3.6+
- `requests` library

You can install the `requests` library using pip:

```
pip install requests
```

### Environment Variables
Set the following environment variables with your actual credentials and API information:

```

export POPUP_USERNAME='your_popup_username'
export POPUP_PASSWORD='your_popup_password'
export MAIN_USERNAME='your_main_username'
export MAIN_PASSWORD='your_main_password'
export KINEXON_API_KEY='your_api_key'
```

### Running the Script
Once your environment variables are set, run the script:

```
python main.py
```
And voila! Watch as the script logs you in twice (because once is never enough) and fetches your precious metrics and events.

### Troubleshooting
- Failed to Login: Double-check your credentials. Check with the webiste. We all make typos.
- Connection Errors: Ensure you have an internet connection. Yes, it’s necessary.
- Might be prone to API changes due to young age of Kinexon API
  
### Contributing
Feel free to contribute to this project. If you can handle the sarcasm, you're welcome to fork, submit PRs, or open issues.

License
This project is licensed under the MIT License.