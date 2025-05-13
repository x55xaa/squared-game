"""Contains the packet definitions used by the game alongside some helper functions."""

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


from enum import auto, IntEnum
from socket import error as socket_error, socket
import struct
from typing import Self
from uuid import UUID

from ..game.sprites.player import PlayerAttributes


class PacketType(IntEnum):
    """"""

    EMBEDDED = auto()
    JOIN = auto()
    LEAVE = auto()
    MESSAGE = auto()
    POSITION = auto()


class Packet:
    """"""

    def __init__(self, type: PacketType, length: int, data: bytes):
        """"""

        if (actual_length := len(data)) != length:
            raise ValueError(
                f'packet length mismatch ({length} != {actual_length})'
            )

        self._type: PacketType = type
        self._length: int = length
        self._data: bytes = data

    @classmethod
    def from_socket(cls, stream: socket):
        """"""

        blob: bytes = stream.recv(2)
        if not blob:
            raise socket_error

        packet_type = PacketType.from_bytes(blob, byteorder='big')

        blob: bytes = stream.recv(4)
        if not blob:
            raise socket_error

        packet_length: int = struct.unpack('>I', blob)[0]

        packet_data = stream.recv(packet_length)
        if not packet_data or len(packet_data) != packet_length:
            raise socket_error

        return cls(packet_type, packet_length, packet_data)

    @classmethod
    def from_bytes(cls, bytes: bytes):
        """"""

        if len(bytes) < 6:
            raise ValueError('packet too short')

        packet_type = PacketType.from_bytes(bytes[:2], byteorder='big')
        packet_length: int = struct.unpack('>I', bytes[2:6])[0]
        packet_data = bytes[6:]

        return cls(packet_type, packet_length, packet_data)

    def to_bytes(self) -> bytes:
        """"""

        return (
            self.type.to_bytes(2, byteorder='big') +
            self.length.to_bytes(4, byteorder='big') +
            self.data
        )

    def parse(self) -> Self:
        """"""

        match self.type:
            case PacketType.EMBEDDED:
                con = EmbeddedPacket
            case PacketType.JOIN:
                con = JoinPacket
            case PacketType.LEAVE:
                con = LeavePacket
            case PacketType.MESSAGE:
                con = MessagePacket
            case PacketType.POSITION:
                con = PositionPacket
            case _:
                con = Packet

        return con(self.type, self.length, self.data)

    @property
    def type(self) -> PacketType:
        """"""

        return self._type

    @property
    def length(self) -> int:
        """"""

        return self._length

    @property
    def data(self) -> bytes:
        """"""

        return self._data

    def __repr__(self):
        return f'Packet(type={self.type.name}, length={self.length}, data={self.data})'


class EmbeddedPacket(Packet):
    """"""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._id, self._embedded_packet = (
            UUID(int=int.from_bytes(self.data[:16], byteorder='big')),
            Packet.from_bytes(self.data[16:]),
        )

    @classmethod
    def from_packet(cls, identity: UUID, packet: Packet):
        """"""

        packet_data: bytes = (
                int(identity).to_bytes(16, byteorder='big') +
                packet.to_bytes()
        )

        return cls(PacketType.EMBEDDED, len(packet_data), packet_data)

    @property
    def identity(self) -> UUID:
        """"""

        return self._id

    @property
    def embed(self) -> Packet:
        """"""

        return self._embedded_packet


class JoinPacket(Packet):
    """"""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._attributes: PlayerAttributes = {}

        r, g, b = struct.unpack('>3B', self.data[:3])
        x, y = struct.unpack('>2H', self.data[3:7])

        self._attributes['color'] = (r, g, b)
        self._attributes['position'] = (x, y)

    @classmethod
    def from_attributes(cls, attributes: PlayerAttributes):
        """"""

        packet_data: bytes = (
            struct.pack('>3B', *attributes['color']) +
            struct.pack('>2H', *attributes['position'])
        )

        return cls(PacketType.JOIN, len(packet_data), packet_data)

    @property
    def attributes(self) -> PlayerAttributes:
        """"""

        return self._attributes


class LeavePacket(Packet):
    """"""

    @classmethod
    def new(cls):
        """"""

        return cls(PacketType.LEAVE, 0, b'')


class MessagePacket(Packet):
    """"""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._message = self.data.decode()

    @classmethod
    def from_message(cls, msg: str):
        """"""

        return cls(PacketType.MESSAGE, len(msg), msg.encode())

    @property
    def message(self) -> str:
        """"""

        return self._message


class PositionPacket(Packet):
    """"""

    def __init__(self, *args, **kwargs):
        """"""

        super().__init__(*args, **kwargs)

        self._x, self._y = struct.unpack('>2H', self.data)

    @classmethod
    def from_coordinates(cls, x: int, y: int):
        """"""

        return cls(PacketType.POSITION, 4, struct.pack('>2H', x, y))

    @property
    def x(self) -> int:
        """"""

        return self._x

    @property
    def y(self) -> int:
        """"""

        return self._y
