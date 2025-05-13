"""Main game file."""

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


import logging
from uuid import UUID

import pygame
from colorama.ansi import clear_line
from pygame import Surface

from ...modules import metadata
from ..net.client import TCPClient
from ..net.callbacks import on_player_join, on_player_leave, on_player_move
from . import player
from .player import MainPlayer, PLAYERS, player_join, player_leave, player_move


logger = logging.getLogger(__name__)


def init(title: str, size: tuple[int, int]) -> Surface:
    """"""

    successes, failures = pygame.init()

    logger.debug(
        'initializing pygame: %d successes and %d failures.',
        successes, failures
    )

    pygame.display.set_caption(title)
    return pygame.display.set_mode(size)


def main(screen: Surface, fps: int) -> None:
    """"""

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(fps) / 1000
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    PLAYERS[UUID(int=0)].set_velocity(y=-200 * dt)
                elif event.key == pygame.K_s:
                    PLAYERS[UUID(int=0)].set_velocity(y=200 * dt)
                elif event.key == pygame.K_a:
                    PLAYERS[UUID(int=0)].set_velocity(x=-200 * dt)
                elif event.key == pygame.K_d:
                    PLAYERS[UUID(int=0)].set_velocity(x=200 * dt)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    PLAYERS[UUID(int=0)].set_velocity(y=0)
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    PLAYERS[UUID(int=0)].set_velocity(x=0)

        for p in PLAYERS.values():
            p.update()
            screen.blit(p.image, p.rect)

        pygame.display.update()  # Or pygame.display.flip()


def run(client: TCPClient) -> None:
    """"""

    PLAYERS[UUID(int=0)] = MainPlayer(client)

    client.add_callback(on_player_join(player_join))
    client.add_callback(on_player_leave(player_leave))
    client.add_callback(on_player_move(player_move))

    client.start()

    window_title: str = f'{metadata.package().capitalize()} - v{metadata.version()}'
    screen = init(window_title, (720, 480))

    main(screen, 60)
