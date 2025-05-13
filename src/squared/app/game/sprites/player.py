"""Contains player definitions."""

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
import logging
from typing import TypedDict, Optional, Union
from uuid import UUID

from pygame import Surface, Rect

from . import BaseSprite


type PlayerColor = tuple[int, int, int]
type PlayerPosition = tuple[int, int]
type PlayerVelocity = tuple[float, float]


logger = logging.getLogger(__name__)

PLAYERS: dict[UUID, Union['MainPlayer', 'RemotePlayer']] = {}


class PlayerAttributes(TypedDict):
    color: PlayerColor
    position: PlayerPosition


class BasePlayer(ABC, BaseSprite):
    """"""

    def __init__(self):
        """"""

        super().__init__()

        self._body_surface = Surface((32, 32))
        self._body_surface.fill((0, 0, 0))
        self._body_rect = self._body_surface.get_rect()
        
        self.__blit__ = [self._body_surface, self._body_rect]
    
    def grown(message: str) -> None:
        pass
        
    
    @abstractmethod
    def update(self) -> None:
        ...
    
    @property
    def surface(self) -> Surface:
        """"""

        return self._body_surface

    @property
    def rect(self) -> Rect:
        """"""

        return self._body_rect

    @property
    def x(self) -> int:
        """"""

        return self._body_rect.x

    @property
    def y(self) -> int:
        """"""

        return self._body_rect.y


class RemotePlayer(BasePlayer):
    """"""

    def __init__(self, color: PlayerColor, position: PlayerPosition):
        """"""

        super().__init__()

        self._body_surface.fill(color)
        self._position: PlayerPosition = position

    def update(self) -> None:
        """"""
        
        self._body_rect.move_ip(self._position[0] - self.x, self._position[1] - self.y)

    def set_position(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """"""

        if x is not None and y is not None:
            self._position = (x, y)
        elif x is not None:
            self._position = (x, self._position[1])
        elif y is not None:
            self._position = (self._position[0], y)


class MainPlayer(BasePlayer):
    """"""

    def __init__(self, client):
        """"""

        super().__init__()

        self._client = client
        self._prev_position = (0, 0)
        self._velocity: PlayerVelocity = (0 ,0)

    def update(self) -> None:
        """"""

        self._body_rect.move_ip(*self._velocity)
        
        if self._prev_position != (self.x, self.y):
            self._client.update_position(self.x, self.y)
        
        self._prev_position = (self.x, self.y)
    
    def set_attributes(self, attributes: PlayerAttributes) -> None:
        """"""
        
        self._body_surface.fill(attributes['color'])
        self._body_rect.move(*attributes['position'])
        
    def set_velocity(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """"""

        if x is not None and y is not None:
            self._velocity = (x, y)
        elif x is not None:
            self._velocity = (x, self._velocity[1])
        elif y is not None:
            self._velocity = (self._velocity[0], y)
