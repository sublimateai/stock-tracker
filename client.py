from src.load_config import load_client_config
from src.client.loggers.registry import logger_registry
import argparse
import asyncio

client_config = load_client_config()


async def main():
    """
    Take user's command line arguments and then start running client side loggers, or what else the user
    specifies.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--login",
        default="",
        help="comma separated values for each cookie not stored, log in session manually",
    )

    args = parser.parse_args()

    requested_clients = client_config.get("clients")
    loggers_running = []

    if requested_clients and isinstance(requested_clients, list):
        if args.login:
            # log in manually sessions not functional
            providers_to_login: set[str] = set(
                [x.strip() for x in args.login.split(",")]
            )

            for provider_name in providers_to_login:
                loggers_running.append(
                    logger_registry.create_logger(
                        provider=provider_name, market_name=""
                    )
                )

            # user logs in on each thing specified,
            for logger in loggers_running:
                await logger.user_login()

        else:
            # load config, and for each client in the config start up an async logger, and start
            tasks = []

            for client_info in requested_clients:
                loggers_running.append(logger_registry.create_logger(**client_info))

            for logger in loggers_running:
                tasks.append(asyncio.create_task(logger.start()))

            # mainloop, shouldn't end
            await asyncio.gather(*tasks)
    else:
        print("Config invalid")


if __name__ == "__main__":
    asyncio.run(main())
