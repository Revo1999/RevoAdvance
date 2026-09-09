# Cartridges, BIOS and persistent data


## In the real GBA

A cartridge provides read-only game program/assets and optionally a save device. ROM appears through three wait-state windows beginning at 0x08000000, 0x0A000000 and 0x0C000000. SRAM/Flash accesses begin at 0x0E000000; serial EEPROM uses accesses in cartridge ROM space, with decoding dependent on cartridge size. Some cartridges add GPIO devices such as clocks or sensors.

The BIOS is a separate 16 KiB system ROM, not part of the game cartridge. A real BIOS boot and a deliberately initialized test-ROM entry point are different boot strategies. Firmware replacement/high-level emulation can be a later project, but skipping BIOS routines without a clear initialization contract makes failures difficult to diagnose.

## In our emulator

Opening and playing your own `.gba` games, then saving and continuing them later, are explicit goals. Work through these user-facing lessons alongside the hardware:

1. [Load a .gba file and play it](loading-and-playing.md) — file selection, validation, boot, pause/reset and game testing.
2. [Save your game and continue later](saving-and-resuming.md) — cartridge save files, restart verification and later save-state slots.
3. [C# file I/O refresher](../csharp-and-dotnet/file-io.md) — paths, binary data, ownership and disk errors.

Desktop reads files and passes bytes to Core. Core models ROM visibility, save-device protocol state, and any implemented peripheral registers. File paths and dialogs remain in Desktop. Save data persistence writes belong to the host; emulated device state belongs to Core. Device capacity and mirroring are not inferred from a large address window alone.

Start with a bounded ROM load and metadata inspection. Header strings can help identify a ROM but are not proof of every save-device type; allow an explicit configuration when detection is incomplete. Implement SRAM first, then Flash command sequences/banking and EEPROM serial transactions as separate milestones. Time-dependent device behavior should use guest time.

## In C#

Use byte arrays or read-only views for ROM contents, explicit bounds and clearly owned save buffers. Host exceptions report missing or invalid files. A save state is not just a saved SRAM file: it must capture transient machine state too.

See [roms/README](../../roms/README.md) for local files. No commercial ROM or BIOS is distributed here. Use your own legally obtained material and respect diagnostic project licenses.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Host exceptions and guest exceptions](../csharp-and-dotnet/exceptions.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/): Throw, try, catch and finally.
- [Types and memory](../csharp-and-dotnet/types-and-memory.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/): Value types, reference types and type safety.

## What you should understand now

- [ ] ROM, BIOS, cartridge saves and save states differ.
- [ ] A diagnostic needs a known initial environment.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Load and inspect a legal diagnostic ROM yourself. Document entry address, CPU state, memory assumptions, BIOS needs and the first expected observable result before running it.

## Definition of done

- Invalid/oversized input is reported clearly.
- A chosen test ROM has a reproducible boot contract.
- SRAM persistence later survives closing/reopening the host.
- A chosen game with its save device implemented passes Save → close app → reopen ROM → Continue; Flash/EEPROM games require their corresponding protocol too.

## Common mistakes

- Treating all save hardware as one writable array.
- Claiming a direct-entry test validates BIOS boot.
- Serializing object memory as a portable save format.

## Further reading

- [GBATEK cartridge](https://mgba-emu.github.io/gbatek/#gbacartridges) — save protocols and device address behavior.
- [mGBA test suite](https://github.com/mgba-emu/suite) — diagnostic source/build requirements; no suite code is copied here.

## Next chapter

[Audio: guest clocks become host samples](../13-audio/README.md)
