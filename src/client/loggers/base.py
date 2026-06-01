# import asyncio
# from playwright.async_api import async_playwright
# from playwright_stealth import Stealth

# NOTE: We _should_ have a database client side, so that we can store existing cookies (to bypass captchas) and
# store candles that could not be sent to the server, for example when the server is off.


class Logger:
    def __init__(self, target_site: str, server_url: str):
        self.target_site = target_site
        self.server_url = server_url

    def login():
        pass

    def user_login():
        """
        Sometimes a human might have to log in to bypass the captchas
        """
        pass

    def save_cookies():
        pass

    def load_cookies():
        pass

    def start():
        """
        Start tracking, connect to the websocket on the server, then continually send candles as they come in to be saved on the servers database
        """
        pass
