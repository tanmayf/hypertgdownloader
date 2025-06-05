import pytest
import asyncio
from pyrogram import Client
from hypertgdownloader.downloader import HyperTGDownloader
from hypertgdownloader.clients import ClientManager

@pytest.mark.asyncio
async def test_downloader_initialization():
    clients = {
        "bot1": Client("bot1", api_id=123, api_hash="abc", bot_token="token1"),
    }
    downloader = HyperTGDownloader(
        helper_bots=clients,
        helper_loads={"bot1": 0},
        num_parts=4,
        chunk_size=1024,
        download_dir="downloads/",
    )
    assert downloader.num_parts == 4
    assert downloader.chunk_size == 1024
    assert downloader.download_dir == "downloads/"

@pytest.mark.asyncio
async def test_get_media_type():
    # Mock a message with a document
    class MockMessage:
        document = type("Document", (), {"file_id": "mock_file_id", "file_size": 1024})

    message = MockMessage()
    media = await HyperTGDownloader.get_media_type(message)
    assert media == message.document

    # Test with no media
    class EmptyMessage:
        pass

    with pytest.raises(ValueError, match="This message doesn't contain any downloadable media"):
        await HyperTGDownloader.get_media_type(EmptyMessage())
