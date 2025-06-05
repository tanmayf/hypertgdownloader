# HyperTGDownloader

A high-speed, parallel Telegram file downloader using multiple helper bot tokens with Pyrogram.

## Features

- Bypasses Telegram rate/speed limits using multiple bot clients
- Splits files into chunks and downloads in parallel
- Clean, reusable API for any Pyrogram-based bot

## Installation

```bash
pip install -e .
```

## Usage

```python
from pyrogram import Client
from hypertgdownloader import HyperTGDownloader

helper_bots = {
    "bot1": Client("bot1", bot_token="..."),
    "bot2": Client("bot2", bot_token="..."),
}
main_bot = Client("main_bot", bot_token="...")

downloader = HyperTGDownloader(helper_bots=helper_bots, main_client=main_bot)

# In your handler:
file_path = await downloader.download(message)
print("Downloaded to:", file_path)
```

---