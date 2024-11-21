import aiohttp
from loguru import logger

class RestClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_insightful_data(self, token: str, limit: int = 50):
        url = f"{self.base_url}/v1/twitter-fraud-detection/{token}/fetch-insightful-data?limit={limit}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch data: {response.status} - {await response.text()}")
                        return None
                    data = await response.json()
                    logger.info(f"Successfully fetched data: {data}")
                    return data
            except Exception as e:
                logger.error(f"Error during REST API call: {e}")
                return None
