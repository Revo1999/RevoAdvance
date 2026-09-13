# Locally supplied ROMs and BIOS

Your `.gba` files are intended inputs to the finished emulator. Follow [loading and playing](../docs/12-cartridges-and-roms/loading-and-playing.md) and [saving and resuming](../docs/12-cartridges-and-roms/saving-and-resuming.md). The loader should accept files from any selected location; copying them here is optional. Save data lives separately and never modifies the original ROM.

The local BIOS location is **`roms/gba_bios.bin`**. The desktop build copies it into its run folder automatically when present. `BiosFile.Load()` reads and checks its 16,384-byte size; this supplies firmware bytes without asking you to write a BIOS. The CPU and bus will execute/map those bytes during the boot lesson. No firmware or game binaries are included in Git.

The folder contents are ignored by Git except this README. Your BIOS stays local, and the build does not bundle it into publish output. On another computer, place your own BIOS at the same path.

[mGBA suite](https://github.com/mgba-emu/suite) and [gba-tests](https://github.com/jsmolka/gba-tests) are useful diagnostic starting points. They may require a separate homebrew toolchain to build. Reading their tests to understand expected hardware behavior is different from copying an emulator implementation.

Before running a diagnostic, record its source/revision/hash, initial CPU/stack/entry state, BIOS requirements and expected report in [progress](../progress/README.md). See the [testing strategy](../docs/16-testing/README.md).
