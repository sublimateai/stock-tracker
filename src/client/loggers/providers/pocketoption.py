from asyncio.tasks import Task
from typing import ContextManager
from playwright.async_api import async_playwright, Page
from playwright.async_api import BrowserContext
from playwright_stealth import Stealth
import asyncio

from ..base import BaseLogger


class PocketOptionLogger(BaseLogger):
    NAME = "pocketoption"

    def __init__(self, target_site: str, server_url: str, market_names: list[str]):
        self.target_site = target_site
        self.server_url = server_url
        self.market_names = market_names

    async def save_cookies(self, browser_context: BrowserContext):
        pass

    async def load_cookies(self, browser_context: BrowserContext):
        pass

    async def user_login(self):
        """
        User logs in and saves cookies to save the session. Will expire
        after some time so needs continual renewal.
        """
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            page = await context.new_page()
            await page.goto(self.server_url)

            # need to wait for user action
            while True:
                await asyncio.sleep(2)
                if len(browser.contexts[0].pages):
                    break

            await self.save_cookies(context)

    async def setup_page(
        self,
        context: BrowserContext,
        market_name: str,
        continue_logging_even_if_existing: bool = True,
    ):
        page = await context.new_page()
        await page.goto(self.server_url)

        # remap canvas.fill to our own function that logs what gets written to the canvas
        # connect websocket

        return page

    async def page_loop(self, page: Page):

        # select market
        # track and collect recent datapoints, and package into a candle, send to websocket

        # occasionally attempt to reconn websocket

        pass

    async def start(self):
        """
        Start logging on all market names specified
        """
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            await self.load_cookies(context)

            setup_tasks: list[Task] = []
            for market_name in self.market_names:
                setup_tasks.append(
                    asyncio.create_task(self.setup_page(context, market_name))
                )

            pages_and_websockets = await asyncio.gather(*setup_tasks)

            tasks: list[Task] = []
            for [page] in pages_and_websockets:
                tasks.append(asyncio.create_task(self.page_loop(page)))

            await asyncio.gather(*tasks)


def create_pocket_option_logger(
    market_names: list[str],
    target_site: str = "https://pocketoption.com/en/cabinet/",
    server_url: str = "",
) -> PocketOptionLogger:
    selected_server_url = server_url
    if not selected_server_url:
        from src.load_config import load_client_config

        selected_server_url: str = load_client_config().get(
            "server_url", "http://localhost:8080"
        )
    return PocketOptionLogger(
        target_site=target_site,
        server_url=selected_server_url,
        market_names=market_names,
    )
