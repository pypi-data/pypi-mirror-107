from abc import ABC, abstractmethod
from typing import Any

from navmenu.menu_manager import MenuManager


class BaseIO(ABC):
    __slots__ = 'menu_manager',

    def __init__(self, menu_manager: MenuManager) -> None:
        self.menu_manager = menu_manager

    @abstractmethod
    def process(self, *args: Any, **kwargs: Any) -> Any:
        pass
