import pytest
from pyrogram import Client
from hypertgdownloader.clients import ClientManager

@pytest.fixture
def client_manager():
    # Mock clients for testing
    clients = {
        "bot1": Client("bot1", api_id=123, api_hash="abc", bot_token="token1"),
        "bot2": Client("bot2", api_id=123, api_hash="abc", bot_token="token2"),
    }
    return ClientManager(clients)

def test_client_manager_initialization(client_manager):
    assert len(client_manager.clients) == 2
    assert client_manager.loads == {"bot1": 0, "bot2": 0}

def test_get_least_loaded(client_manager):
    assert client_manager.get_least_loaded() in ["bot1", "bot2"]
    client_manager.increase_load("bot1")
    assert client_manager.loads["bot1"] == 1
    assert client_manager.get_least_loaded() == "bot2"

def test_increase_decrease_load(client_manager):
    client_manager.increase_load("bot1")
    assert client_manager.loads["bot1"] == 1
    client_manager.decrease_load("bot1")
    assert client_manager.loads["bot1"] == 0
