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


from typing import TypedDict, Optional

from pygame import Surface, Rect

from . import BaseSprite


type PlayerBounds = tuple[int, int, int, int]
type PlayerColor = tuple[int, int, int]
type PlayerPosition = tuple[int, int]
type PlayerSize = tuple[int, int]
type PlayerVelocity = tuple[float, float]


class PlayerAttributes(TypedDict):
    color: PlayerColor
    position: PlayerPosition
    size: PlayerSize


class BasePlayer(BaseSprite):
    """"""

    def __init__(self, bounds: PlayerBounds):
        """"""

        super().__init__()

        self._surface = Surface((0, 0))
        self._surface.fill((0, 0, 0))
        self._rect = self._surface.get_rect()
        
        self._bounds = bounds
        
        self.__blit__ = [self._surface, self._rect]

    def update(self) -> bool:
        """"""
        
        if not Rect(*self._bounds).contains(self._rect):
            return False

        return True
    
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

    def update(self) -> bool:
        """"""

        if self.update():
            self._rect.move_ip(self._position[0] - self.x, self._position[1] - self.y)

            return True

        return False

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

    def __init__(self, bounds: PlayerBounds, client):
        """"""

        super().__init__(bounds)

        self._client = client

        self._prev_position = (0, 0)
        self._velocity: PlayerVelocity = (0 ,0)

    def update(self) -> bool:
        """"""

        if self.update():
            self._rect.move_ip(*self._velocity)

            if self._prev_position != (self.x, self.y):
                self._client.update_position(self.x, self.y)

                self._prev_position = (self.x, self.y)

            return True

        return False
    
    def set_attributes(self, attributes: PlayerAttributes) -> None:
        """"""

        self._surface = Surface(attributes['size'])
        self._surface.fill(attributes['color'])

        self._rect = self._surface.get_rect()
        self._rect.move(*attributes['position'])
        
    def set_velocity(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """"""

        if x is not None and y is not None:
            self._velocity = (x, y)
        elif x is not None:
            self._velocity = (x, self._velocity[1])
        elif y is not None:
            self._velocity = (self._velocity[0], y)
