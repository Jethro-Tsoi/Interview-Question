import requests
import time
import logging
import datetime
import uuid

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Todo: we can add cache-busting parameter                                                                                                                       │
def get_latest_binance_announcements(catalog_id):
    """
    Fetches the latest announcements from the unofficial Binance API,
    using HTTP headers to request fresh data and avoid caching.
    """
    # Generate a random integrity value (UUID) for each call
    integrity_value = str(uuid.uuid4())
    url = f"https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1&pageNo=1&pageSize=10&catalogId={catalog_id}"

    # Mimic browser headers to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "Referer": f"https://www.binance.com/en/support/announcement/list/{catalog_id}",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Integrity": integrity_value,
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            logger.info(f"--- Latest Announcements (Catalog ID: {catalog_id}) ---")
            # The articles are nested within the 'catalogs' list
            catalogs = data.get("data", {}).get("catalogs", [])
            if catalogs:
                articles = catalogs[0].get("articles", [])
                if not articles:
                    logger.info("No articles found for this catalog.")
                for article in articles:
                    # Convert timestamp (in ms) to a readable date string
                    release_date = datetime.datetime.fromtimestamp(article['releaseDate'] / 1000)
                    date_str = release_date.strftime('%Y-%m-%d %H:%M:%S')
                    logger.info(f"  - {article['title']} (Published: {date_str})")
            else:
                logger.info("No catalogs found in the response.")
            logger.info("----------------------------------------------------")
        else:
            logging.error(f"API request failed: {data.get('message', 'No error message')}")

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
   
if __name__ == "__main__":
    """
       * New Cryptocurrency Listing: catalogId=48
       * Latest Activities: catalogId=49
       * Latest Binance News: catalogId=161
       * New Fiat Listings: catalogId=162
       * Delisting: catalogId=164
       * API Updates: catalogId=159
       * Crypto Airdrop: catalogId=160
       * Maintenance Updates: catalogId=163
    """
    # Example: Fetch "Latest Activities" (catalogId=49)
    get_latest_binance_announcements(catalog_id=49)
