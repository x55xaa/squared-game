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


from typing import TypedDict, Optional, Union
from uuid import UUID

from pygame import Surface, Rect
from pygame.sprite import Sprite


type PlayerColor = tuple[int, int, int]
type PlayerPosition = tuple[int, int]
type PlayerVelocity = tuple[float, float]


PLAYERS: dict[UUID, Union['Player', 'MainPlayer']] = {}


class PlayerAttributes(TypedDict):
    color: PlayerColor
    position: PlayerPosition


class Player(Sprite):
    """"""

    def __init__(self, color: PlayerColor, position: PlayerPosition):
        """"""

        super().__init__()

        self._image = Surface((32, 32))
        self._image.fill(color)

        self._rect = self._image.get_rect()
        self._position: PlayerPosition = position

    def update(self) -> None:
        """"""

        self._rect.move(*self._position)

    def set_position(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        """"""

        if x and y:
            self._position = (x, y)
        elif x:
            self._position = (x, self._position[1])
        elif y:
            self._position = (self._position[0], y)

    @property
    def image(self) -> Surface:
        """"""

        return self._image

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


class MainPlayer(Sprite):
    """"""

    def __init__(self, client):
        """"""

        super().__init__()

        self._client = client

        self._image = Surface((32, 32))
        self._image.fill((0, 0, 0))

        self._rect = self._image.get_rect()
        self._velocity: PlayerVelocity = (0 ,0)

    def set_attributes(self, attributes: PlayerAttributes) -> None:
        """"""

        self._image.fill(attributes['color'])
        self._rect.move(*attributes['position'])

    def update(self) -> None:
        """"""

        self._client.update_position(self.x, self.y)
        self._rect.move_ip(*self._velocity)

    def set_velocity(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        """"""

        if x and y:
            self._velocity = (x, y)
        elif x:
            self._velocity = (x, self._velocity[1])
        elif y:
            self._velocity = (self._velocity[0], y)

    @property
    def image(self) -> Surface:
        """"""

        return self._image

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


def player_join(identity: UUID, attributes: PlayerAttributes) -> None:
    """"""

    if int(identity) == 0:
        PLAYERS[identity].set_attributes(attributes)
    else:
        PLAYERS[identity] = Player(**attributes)


def player_leave(identity: UUID) -> None:
    """"""

    if int(identity) == 0:
        return

    PLAYERS.pop(identity, None)


def player_move(identity: UUID, position: PlayerPosition) -> None:
    """"""

    if int(identity) == 0:
        return

    if player := PLAYERS.get(identity):
        player.set_position(*position)