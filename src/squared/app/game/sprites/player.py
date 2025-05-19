"""Contains player related classes."""

# Copyright (C) 2025  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from abc import ABC, abstractmethod
from typing import TypedDict, Optional, Union
from uuid import UUID

from pygame import Surface, Rect

from . import BaseSprite


type PlayerBounds = tuple[int, int, int, int]
type PlayerColor = tuple[int, int, int]
type PlayerPosition = tuple[int, int]
type PlayerSize = tuple[int, int]
type PlayerVelocity = tuple[float, float]


PLAYERS: dict[UUID, Union['MainPlayer', 'RemotePlayer']] = {}
PLAYER_SIZE: PlayerSize = (32, 32)


class PlayerAttributes(TypedDict):
    color: PlayerColor
    position: PlayerPosition
    size: PlayerSize


class BasePlayer(ABC, BaseSprite):
    """"""

    def __init__(self, bounds: PlayerBounds):
        """"""

        super().__init__()

        self._surface = Surface((0, 0))
        self._surface.fill((0, 0, 0))
        self._rect = self._surface.get_rect()
        
        self._bounds = Rect(*bounds)
        
        self.__blit__ = [self._surface, self._rect]

    @abstractmethod
    def update(self) -> None:
        ...

    @property
    def surface(self) -> Surface:
        """"""

        return self._surface

    @property
    def rect(self) -> Rect:
        """"""

        return self._rect

    @property
    def x(self) -> int:
        """"""

        return self._rect.x

    @property
    def y(self) -> int:
        """"""

        return self._rect.y


class RemotePlayer(BasePlayer):
    """"""

    def __init__(self, bounds: PlayerBounds, color: PlayerColor, position: PlayerPosition, size: PlayerSize):
        """"""

        super().__init__(bounds)

        self._position: PlayerPosition = position

        self._surface = Surface(size)
        self._surface.fill(color)
        self._rect = self._surface.get_rect()

        self.__blit__ = [self._surface, self._rect]

    def update(self) -> None:
        """"""

        self._rect.move_ip(self._position[0] - self.x, self._position[1] - self.y)

    def set_position(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """"""

        if x is not None and y is not None:
            new_position = (x, y)
        elif x is not None:
            new_position = (x, self._position[1])
        elif y is not None:
            new_position = (self._position[0], y)
        else:
            new_position = self._position

        if self._bounds.contains(Rect(*new_position, *self._surface.get_size())):
            self._position = new_position


class MainPlayer(BasePlayer):
    """"""

    def __init__(self, bounds: PlayerBounds, client):
        """"""

        super().__init__(bounds)

        self._client = client

        self._prev_position = (0, 0)
        self._velocity: PlayerVelocity = (0 ,0)

    def update(self) -> None:
        """"""

        if self._bounds.contains(Rect(self.x + self._velocity[0], self.y + self._velocity[1], *self._surface.get_size())):

            self._rect.move_ip(*self._velocity)

            if self._prev_position != (self.x, self.y):
                self._client.update_position(self.x, self.y)

                self._prev_position = (self.x, self.y)
    
    def set_attributes(self, attributes: PlayerAttributes) -> None:
        """"""

        self._surface = Surface(attributes['size'])
        self._surface.fill(attributes['color'])

        self._rect = self._surface.get_rect()
        self._rect.move(*attributes['position'])

        self.__blit__ = [self._surface, self._rect]

    def set_velocity(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """"""

        if x is not None and y is not None:
            new_velocity = (x, y)
        elif x is not None:
            new_velocity = (x, self._velocity[1])
        elif y is not None:
            new_velocity = (self._velocity[0], y)
        else:
            new_velocity = self._velocity

        if self._bounds.contains(Rect(self.x + new_velocity[0], self.y + new_velocity[1], *self._surface.get_size())):
            self._velocity = new_velocity
