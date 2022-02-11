import os
import random
import pygame as pg

from typing import Union
from collections import namedtuple


Point = namedtuple('Point', ['x', 'y'], defaults=[0, 0])


def get_font_renderer(font_path: str, size: int):
    # TODO: Turn this into a proper try/catch and throw an appropriate error for both conditions
    if os.path.exists(font_path) and pg.get_init():
        return pg.font.Font(font_path, size)


def random_location(width: int, height: int, block_size: int) -> Point:
    x = random.randint(0, (width - block_size) // block_size) * block_size
    y = random.randint(0, (height - block_size) // block_size) * block_size
    return Point(x, y)


def blit(source: pg.Surface, dest: pg.Surface, p: Point, centered: bool = True):
    if not centered:
        dest.blit(source, (p.x, p.y))
    else:
        size = Point(*source.get_size())
        cx = p.x - size.x / 2
        cy = p.y - size.y / 2
        dest.blit(source, (cx, cy))


class CallbackManager:
    def __init__(self):
        self.callbacks: {str: callable} = {}

    def __getitem__(self, name):
        return self.callbacks[name]

    def __contains__(self, name: str):
        return self.callbacks.keys().__contains__(name)

    @property
    def count(self) -> int:
        return len(self.callbacks)

    def add(self, name: str, func: callable) -> None:
        if not self.__contains__(name):
            self.callbacks.update({name: func})

    def update(self, name: str, func: callable) -> None:
        self.callbacks.update({name: func})

    def remove(self, name: str) -> None:
        if self.__contains__(name):
            self.callbacks.pop(name)

    def clear(self) -> None:
        self.callbacks.clear()

    def execute(self, name: str) -> bool:
        if self.__contains__(name):
            self.callbacks[name]()
            return True
        return False

    def execute_all(self):
        if len(self.callbacks) > 0:
            for _, func in self.callbacks.items():
                func()
            return True
        return False


class KeypressCallbackManager:
    def __init__(self):
        self.key_callbacks: {int, CallbackManager} = {}
        pass

    def __contains__(self, key: int):
        return self.key_callbacks.keys().__contains__(key)

    def _register(self, key, name, function):
        if not self.__contains__(key):
            self.key_callbacks.update({key: CallbackManager()})
        self.key_callbacks[key].add(name, function)

    def unregister(self):
        pass

    def clear(self):
        pass

    def execute_callbacks(self, key):
        pass
