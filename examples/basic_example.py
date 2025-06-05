import asyncio
from pyrogram import Client
from hypertgdownloader import HyperTGDownloader

async def progress_callback(current, total, *args):
    """Callback to display download progress."""
    percentage = (current / total) * 100
    print(f"Downloading: {percentage:.2f}% ({current:,} / {total:,} bytes)")

async def main():
    # Replace with your Telegram API credentials and bot tokens
    helper_bots = {
        "bot1": Client("bot1", api_id="YOUR_API_ID", api_hash="YOUR_API_HASH", bot_token="YOUR_BOT_1_TOKEN"),
        "bot2": Client("bot2", api_id="YOUR_API_ID", api_hash="YOUR_API_HASH", bot_token="YOUR_BOT_2_TOKEN"),
        # Add more bots for parallel downloading if needed
    }

    # Initialize helper bot loads (required by HyperTGDownloader)
    helper_loads = {k: 0 for k in helper_bots}

    # Start all clients
    async with helper_bots["bot1"], helper_bots["bot2"]:
        # Initialize the downloader
        downloader = HyperTGDownloader(
            helper_bots=helper_bots,
            helper_loads=helper_loads,
            num_parts=8,  # Number of parts for parallel downloading
            download_dir="my_downloads/",  # Where to save files
        )

        # Start the downloader (starts cache cleanup task)
        await downloader.start()

        try:
            # Get a message with media (replace with your chat_id and message_id)
            # Example: Get a message from a specific chat
            message = await helper_bots["bot1"].get_messages(
                chat_id=123456,  # Replace with your chat ID
                message_ids=789  # Replace with your message ID
            )

            # Download the media
            file_path = await downloader.download_media(
                message=message,
                file_name="my_downloads/downloaded_file.mp4",
                progress=progress_callback,  # Optional progress callback
                dump_chat=-100123456789  # Replace with your dump chat ID (optional)
            )

            if file_path:
                print(f"Downloaded to: {file_path}")
            else:
                print("Download was cancelled or failed.")

        except Exception as e:
            print(f"Error during download: {e}")

if __name__ == "__main__":
    asyncio.run(main())
