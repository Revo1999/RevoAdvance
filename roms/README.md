# Locally supplied ROMs and BIOS

Your `.gba` files are intended inputs to the finished emulator. Follow [loading and playing](../docs/12-cartridges-and-roms/loading-and-playing.md) and [saving and resuming](../docs/12-cartridges-and-roms/saving-and-resuming.md). The loader should accept files from any selected location; copying them here is optional. Save data lives separately and never modifies the original ROM.

No ROM or BIOS is included. Supply legally obtained game files, your own homebrew, and diagnostic ROMs you are entitled to use. Respect each test project's license and build instructions; this repository does not download binaries automatically.

The folder contents are ignored by Git except this README. Do not commit commercial games, copyrighted BIOS files, personal save data or generated save states. Place a BIOS here under a name you document in your host configuration; no loader or naming contract exists yet.

[mGBA suite](https://github.com/mgba-emu/suite) and [gba-tests](https://github.com/jsmolka/gba-tests) are useful diagnostic starting points. They may require a separate homebrew toolchain to build. Reading their tests to understand expected hardware behavior is different from copying an emulator implementation.

Before running a diagnostic, record its source/revision/hash, initial CPU/stack/entry state, BIOS requirements and expected report in [progress](../progress/README.md). See the [testing strategy](../docs/16-testing/README.md).
