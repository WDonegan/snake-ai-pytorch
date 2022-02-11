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
        self.callbacks: {int: callable} = {}
        pass

    def __getitem__(self, name):
        return self.callbacks[name]

    @property
    def count(self) -> int:
        return len(self.callbacks)

    def add(self, name: str, func: callable) -> None:
        if not self.__contains_name__(name):
            self.callbacks.update({name: func})

    def remove(self, name: str) -> None:
        if self.__contains_name__(name):
            self.callbacks.pop(name)

    def update(self, name: str, func: callable) -> None:
        self.callbacks.update({name: func})

    def remove_all(self) -> None:
        self.callbacks.clear()

    def execute(self, name: Union[str, None] = None) -> bool:
        if len(self.callbacks) > 0:
            if name is None:
                for cb in self.callbacks.values():
                    cb()
                return True
            else:
                if self.callbacks.keys().__contains__(name):
                    self.callbacks[name]()
                    return True
                else:
                    return False
        return False
    # End of Execute

    def __contains_name__(self, name: str):
        return self.callbacks.keys().__contains__(name)


class KeypressCallbackManager:
    def __init__(self):
        pass

    def _register_key(self, key):
        pass

    def _register_func(self, key, function):
        pass

    def register_callback(self, key, function):
        # if key is already registered
        self._register_func(key, function)
        # if key is not registered
        self._register_key(key)
        self._register_func(key, function)
        pass

    def execute_callbacks(self, key):
        pass
