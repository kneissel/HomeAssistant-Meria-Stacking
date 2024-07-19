import aiohttp
from .const import API_BASE_URL


class MeriaAPIClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def status(self) -> bool:
        headers = {
            "API-KEY": self.api_key,
        }
        endpoint = f"{API_BASE_URL}/status"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                data = await response.json()
                return data["success"]

    async def stakings(self) -> list:
        headers = {
            "API-KEY": self.api_key,
        }
        endpoint = f"{API_BASE_URL}/stakings"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data["data"]

    async def lending(self, currencyCode: str) -> dict:
        headers = {
            "API-KEY": self.api_key,
        }
        endpoint = f"{API_BASE_URL}/stakings/{currencyCode}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data["data"]
