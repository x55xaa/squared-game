"""Contains server-side packet filters."""


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


from collections.abc import Callable

from .packet import Packet, PacketType


type PacketFilter = Callable[[Packet], bool]


def whitelist_packets(*args: PacketType) -> PacketFilter:
    """Returns a packet filter that allows only certain packets to go through.

    Args:
        *args:
            a list of allowed packets.
    """

    def packet_filter(pkt: Packet) -> bool:
        if pkt.type not in args:
            return False

        return True

    return packet_filter

