from .providers import pocketoption
from collections.abc import Callable


class LoggerRegistry:
    def __init__(self):
        self.logger_ns: dict[str, Callable] = {
            "pocketoption": pocketoption.create_pocket_option_logger
        }
        self.ns_map = {"po": "pocketoption", "pocketoption": "pocketoption"}

    def resolve_name(self, provider: str) -> str | None:
        return self.ns_map.get(provider)

    def create_logger(self, provider: str, **kwargs):
        resolved_name = self.resolve_name(provider)
        if resolved_name:
            constructor: Callable | None = self.logger_ns.get(resolved_name)
            if constructor:
                return constructor(**kwargs)


logger_registry = LoggerRegistry()
