# welp

`welp` is a CLI Yelp! client

## Features

- Utilizes the Yelp! fusion API to search Yelp without visiting the web UI. Great for devs who want to look busy but are already thinking about lunch!
- Curses menus for interactive CLI menus
- Vim bindings for navigating menus without the keyboard
- Scroll compatible on Termux and other mobile touch screen shell clients
- Emojis for easily scannable food option results

## Installation

Install using pip.

```bash
pip install welp
```

## Usage

You will need a Yelp Fusion API key in order to use this application because this is my side project and im not going to fork over an api key for it. they key is free and is more than enough for personal queries or even dev on this project.

Once you have it, export it to your environment. Stick it into your bashrc to persist it.

```bash
export YELP_API_KEY=<key>
```

If you'd like to use Google Geolocation API for automated geolocated results, provide the environment with the Google Geolocation API Key also:

```bash
export GOOGLE_API_KEY=<key>
```

Both of these keys are basically free for to use individually. The Google API will require a form of payment, but has a free credit program.

### Hotkeys

welp has general vim shotcuts.

- `j` scrolls one selection down
- `k` scrolls one selection up
- `h` scrolls one page back
- `l` scrolls one page forward
- `q` quits or goes back to previous page
- `return` opens detailed business information

## Development

To build this project, use `venv` and python3.

Install dependencies using `pip install -r requirements.txt` and place keys in `.env` of the project root.

Start venv using the following is your venv is named "venv"

```bash
source env/bin/activate && set -a; source .env; set +a
```