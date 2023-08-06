from abc import ABC, abstractmethod
from typing import Optional


class StateHandler(ABC):
    __slots__ = ()

    @abstractmethod
    def get(self, user_id: Optional[int]) -> str:
        pass

    @abstractmethod
    def set(self, user_id: Optional[int], new_state: str) -> None:
        pass

    @abstractmethod
    def create(self, user_id: Optional[int]) -> bool:
        pass

    @abstractmethod
    def go_back(self, user_id: Optional[int], count: Optional[int] = 1) -> None:
        pass


class MemoryStateHandler(StateHandler):
    __slots__ = 'default_state', 'state', 'history'

    def __init__(self, default_state: str) -> None:
        self.default_state = default_state

        self.state = {}
        self.history = {}

    def __repr__(self) -> str:
        return f'MemoryStateHandler({self.default_state})'

    def get(self, user_id: Optional[int]) -> str:
        if user_id not in self.state:
            return self.default_state

        return self.state[user_id]

    def set(self, user_id: Optional[int], new_state: str) -> None:
        if user_id not in self.history:
            self.history[user_id] = []

        self.history[user_id].append(self.state[user_id] if user_id in self.state else self.default_state)
        self.state[user_id] = new_state

    def create(self, user_id: Optional[int]) -> bool:
        if user_id not in self.state:
            self.state[user_id] = self.default_state
            self.history[user_id] = []

            return True

    def go_back(self, user_id: Optional[int], count: Optional[int] = 1) -> None:
        if count < 1:
            raise ValueError('Count must be at least 1')

        elif count == -1:
            count = 1000

        if user_id not in self.history:
            return

        for i in range(count):
            if len(self.history[user_id]) <= i + 1:
                new_state = self.default_state
                break

            else:
                new_state = self.history[user_id][-(i + 1)]

        self.state[user_id] = new_state
        self.history[user_id] = self.history[user_id][:-count]
