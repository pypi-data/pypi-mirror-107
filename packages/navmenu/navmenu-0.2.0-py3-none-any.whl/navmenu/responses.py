from typing import Optional

from navmenu.keyboard import Keyboard


class Message:
    __slots__ = 'keyboard', 'text'

    def __init__(
            self, text: Optional[str] = None, keyboard: Optional[Keyboard] = None, payload: Optional[dict] = None
    ) -> None:
        if payload is None:
            payload = {}

        self.keyboard = keyboard

        self.text = text.format(**payload) if text is not None else None

    def __repr__(self) -> str:
        return f'Message({repr(self.text)}, {self.keyboard})'


class Response:
    __slots__ = 'message', 'menu', 'go_back_count'

    def __init__(self, message: Optional[Message] = None, menu: str = None, go_back_count: int = None) -> None:
        self.message = message
        self.menu = menu
        self.go_back_count = go_back_count

    def __repr__(self) -> str:
        return f'Response({self.message}, {repr(self.menu)}, {self.go_back_count})'
