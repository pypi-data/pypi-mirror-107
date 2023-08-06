from typing import Dict, Optional, Sequence

from .menus import BaseMenu
from .state import StateHandler
from .responses import Message, Response


class MenuManager:
    __slots__ = 'menus', 'state_handler'

    def __init__(self, menus: Dict[str, BaseMenu], state_handler: StateHandler) -> None:
        self.menus = menus
        self.state_handler = state_handler

    def __repr__(self) -> str:
        return f'MenuManager({self.menus}, {self.state_handler})'

    def get_message(self, user_id: int = None, payload: Optional[dict] = None) -> Message:
        state = self.state_handler.get(user_id)

        return self.menus[state].get_message(payload)

    def select(self, action: str, user_id: int = None, payload: Optional[dict] = None) -> Optional[Sequence[Message]]:
        state = self.state_handler.get(user_id)

        actions = self.menus[state].select(action, payload)
        if actions is not None:
            messages = []
            for res in actions:
                if isinstance(res, Message):
                    messages.append(res)

                elif isinstance(res, Response):
                    if res.message:
                        messages.append(res.message)

                    if res.go_back_count:
                        self.state_handler.go_back(user_id, res.go_back_count)

                    if res.menu:
                        self.state_handler.set(user_id, res.menu)

                        enter_res = self.menus[res.menu].enter(payload)
                        if isinstance(enter_res, Message):
                            messages.append(enter_res)

            return messages

        else:
            raise ValueError('Invalid action')

    def serialize(self) -> dict:
        return {
            'menus': {menu_name: {
                'type': menu.__class__.__name__,
                **menu.serialize(),
            } for menu_name, menu in self.menus.items()},
        }
