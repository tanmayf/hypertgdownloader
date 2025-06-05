# HyperTGDownloader

A blazing-fast Telegram file downloader using Pyrogram and multiple bot tokens.

## Usage

```python
from hypertgdownloader import HyperTGDownloader

downloader = HyperTGDownloader()
file_path = await downloader.download_media(message)
print("Downloaded to:", file_path)
```

Make sure you have set up your helper bots, config, and client before using.---
