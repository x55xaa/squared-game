
# Changelog



## [1.0.1](https://github.com/x55xaa/squared-game/releases/tag/v1.0.1) - 2025-05-19

_🌱 Initial release._

### Added

- Add the ability to use tokens to connect to a server ([a928a0e](https://github.com/x55xaa/squared-game/commit/a928a0e3b088797b1821e212392809c09a801be6)) - (Stefano Cuizza)
- Add a CLI to the package ([edc566f](https://github.com/x55xaa/squared-game/commit/edc566fa84051c73727e0c31e489ca8ae2b97b86)) - (Stefano Cuizza)
- Add online multiplayer ([2deecf6](https://github.com/x55xaa/squared-game/commit/2deecf64e662badd91225c7089b23dc8cd613786)) - (Stefano Cuizza)
- Add first game demo ([36e33c1](https://github.com/x55xaa/squared-game/commit/36e33c199501591f78ba0b9ea7c38f0fb8719e09)) - (Stefano Cuizza)
- Add position filter to the server ([e3941f4](https://github.com/x55xaa/squared-game/commit/e3941f4c8549c5d73e53d97f6d63f091158b55eb)) - (Stefano Cuizza)
- Add position filter to the server ([0a4991e](https://github.com/x55xaa/squared-game/commit/0a4991e21960437fc8cbae284642aaacbda5add4)) - (Stefano Cuizza)
- Add player collision ([a4ce8e7](https://github.com/x55xaa/squared-game/commit/a4ce8e7f9c77aa1a418b420f17a40035d0edf183)) - (Stefano Cuizza)

### Changed

- Increase the range of the square fill color ([29c4721](https://github.com/x55xaa/squared-game/commit/29c47214c038804ee22a0ea241243c05d2b25c82)) - (Stefano Cuizza)
- Cap the maximum number of players at 16 ([cceac38](https://github.com/x55xaa/squared-game/commit/cceac389b38062eeebda7366e6779ca390e5bcbd)) - (Stefano Cuizza)
- Server is now in charge of assigning the size to the player on join ([582a864](https://github.com/x55xaa/squared-game/commit/582a86450e69278215e17fa769fdbc099df8c754)) - (Stefano Cuizza)
- Check that the player is inside the perimeter of the screen ([12a8f04](https://github.com/x55xaa/squared-game/commit/12a8f04ae213b5f489fdc41d374919e7b07ccaaa)) - (Stefano Cuizza)
- Do server side check on player position ([dd2d279](https://github.com/x55xaa/squared-game/commit/dd2d279d87cc6adf9a3d8e782ff4cc4da354d3fe)) - (Stefano Cuizza)
- Pass the packet identity and server state to server filters ([5fe42dc](https://github.com/x55xaa/squared-game/commit/5fe42dce8c29b54742a746c47320b7b18d9c841c)) - (Stefano Cuizza)
- Pass the packet identity and server state to server filters ([3113021](https://github.com/x55xaa/squared-game/commit/3113021baf2d0b70bc43aab942f0995fe4a905e4)) - (Stefano Cuizza)
- Randomize player spawn point ([1d3d8a2](https://github.com/x55xaa/squared-game/commit/1d3d8a24b8c13f0692da5ec7b8f9f97cead37108)) - (Stefano Cuizza)
- When hosting, print the server token on screen ([44c5312](https://github.com/x55xaa/squared-game/commit/44c53127800ebede0dfeb97ccb52d93f8f826cfb)) - (Stefano Cuizza)
- Player position is now a pair of floats ([75817c8](https://github.com/x55xaa/squared-game/commit/75817c8ec6b133fc01b5cf2695c8b3e8622ac237)) - (Stefano Cuizza)

### Fixed

- Player can now stop moving ([d0a52a2](https://github.com/x55xaa/squared-game/commit/d0a52a260b13c54d33f3e51793452cc38c84ccfe)) - (Stefano Cuizza)
- Squares can now move in multiplayer ([2a565d4](https://github.com/x55xaa/squared-game/commit/2a565d46abbee87ed8413e0ed323eecfd10acb63)) - (Stefano Cuizza)
- Remove wrong imports ([ececdf7](https://github.com/x55xaa/squared-game/commit/ececdf762c0fe532200744f0ad5579ed155e0173)) - (Stefano Cuizza)
- Update position filter ([a871276](https://github.com/x55xaa/squared-game/commit/a871276561787c1afbf44a3c671a9f7d17568e8e)) - (Stefano Cuizza)
- Call `super().update()` instead of `self.update()` ([c4b8f40](https://github.com/x55xaa/squared-game/commit/c4b8f400e541bacad70b206af31ad3b1581b6883)) - (Stefano Cuizza)
- Refer to new `BOUNDS` constant ([2070bef](https://github.com/x55xaa/squared-game/commit/2070befac846e1e40cdda0541bf84174214ffc62)) - (Stefano Cuizza)
- Add `size` when building `JoinPacket` from attributes ([4fb8a09](https://github.com/x55xaa/squared-game/commit/4fb8a099a64a45cb9a03b3162624c687bc86b2d2)) - (Stefano Cuizza)
- Update `__blit__` variable after attributes update ([acfbffd](https://github.com/x55xaa/squared-game/commit/acfbffdde23467e105ab22f9fd1475b7a63849c8)) - (Stefano Cuizza)
- Use correct player size in position filter ([33d6328](https://github.com/x55xaa/squared-game/commit/33d63289a8f831c5e66148665b4bda412c050a3e)) - (Stefano Cuizza)
- Make sure new player spawns inside the perimeter of the screen ([aff0fe5](https://github.com/x55xaa/squared-game/commit/aff0fe5a12cba36490f23cf56ca1c67eab18e75a)) - (Stefano Cuizza)
- Remove MESSAGE packets from server whitelist ([72d2655](https://github.com/x55xaa/squared-game/commit/72d2655844eb7613577f9fa737f806255e60b802)) - (Stefano Cuizza)

