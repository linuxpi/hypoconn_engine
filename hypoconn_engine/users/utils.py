from hypoconn_engine.utilities.token_scraper import TokenScraper


def scrape_api_token(username, password):
    token_scraper = TokenScraper(username, password)
    return token_scraper.login_and_get_token()
