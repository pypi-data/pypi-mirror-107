from typing import Callable

from navmenu.io.base import BaseIO
from navmenu.menu_manager import MenuManager
from navmenu.responses import Message


def send_default(message):
    print(message.text)


class ConsoleIO(BaseIO):
    def __init__(self, menu_manager: MenuManager, send: Callable = send_default) -> None:
        super().__init__(menu_manager)

        self.send = send

    def process(self) -> None:
        while True:
            message = self.menu_manager.get_message()

            if message:
                actions = ''
                for line in message.keyboard.lines:
                    actions += ' | '.join(f"{i.payload}: {i.text}" for i in line) + '\n'

                separator = '-' * 20

                self.send(Message(f'{separator}\n{message.text}\n{separator}\n{actions}{separator}'))

            text = input('Command: ')

            try:
                messages = self.menu_manager.select(text)

            except ValueError:
                self.send(Message('Invalid command'))

            else:
                for message in messages:
                    self.send(message)
