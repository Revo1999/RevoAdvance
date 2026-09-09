# Load a .gba file and play it

Loading your own `.gba` games, playing them and continuing saved progress are required goals of this emulator. Diagnostic ROMs are stepping stones toward that goal. The current repository is still a learning scaffold; these features are exercises you will implement.

## In the real GBA

A physical cartridge exposes program and graphics/audio data to the machine. A `.gba` file contains a ROM image: bytes representing that cartridge's ROM. It does not contain the emulator, and normally does not contain your current saved progress. The BIOS is separate too.

This project targets Game Boy Advance software. Original Game Boy and Game Boy Color software usually uses `.gb` and `.gbc` files and requires different emulated hardware; changing an extension does not convert it to a GBA game.

## In our emulator

The intended user experience is:

```text
Open ROM → choose a .gba file → load its existing cartridge save
    ↓
initialize the emulated GBA → run → picture + sound + controls
    ↓
save inside the game → persist save data → close emulator
    ↓
open the same ROM later → choose Continue inside the game
```

Implement one step at a time. Loading bytes successfully is an early milestone; displaying and playing the game also requires enough CPU, bus, PPU, timing and input behavior. Audio and the appropriate save device complete the intended experience. An unsupported instruction should produce a useful development report rather than making a successful file load look like a successful game boot.

## Lesson 1 — Select and inspect a ROM

Initially accept a file path through a command-line argument, so no file-dialog library is needed. Later provide an **Open ROM** action and file picker in Desktop; drag-and-drop is an optional convenience. The selected path may be anywhere on your computer: `roms/` is a development convenience, not a required library folder.

Desktop reads the file as binary bytes, validates plausible size and header availability, and passes ROM data to Core. An extension filter helps selection but is not content validation. Report missing files, unreadable files and unsupported content clearly. Cancellation should leave the current session unchanged. Do not require a commercial header signature for all homebrew/diagnostic fixtures.

Inputs: selected path and bytes. Outputs: loaded ROM identity, metadata and validation result. Core's cartridge exposes those bytes through the Game Pak memory windows; it never opens a file dialog or fetches a byte from disk for every CPU read. No guest cycles need to pass during this inspection exercise.

## Lesson 2 — Start, pause, reset and change games

Choose and document a boot strategy using the [cartridge chapter](README.md). A `.gba` file alone is not a BIOS. Do not silently invent initial CPU state when firmware is missing.

Add explicit session actions: run, pause/resume, reset, open another ROM and close. Pause stops guest advancement; the window remains responsive. Reset reinitializes volatile machine state while preserving cartridge save data. Before unloading or changing ROMs, persist outstanding saves; if writing fails, report the failure and retain the old session/save data for retry. Do not discard it because a new ROM was selected.

Keep this a small state model such as “no game”, “paused” and “running”, not an application framework. Host controls are different from the buttons sent to KEYINPUT. Flushing an audio queue on pause/reset avoids playing stale samples; release held host keys on focus loss.

## Lesson 3 — Test a game through the same path

Choose one of your `.gba` games as a compatibility target. Record ROM identity and boot assumptions, then test its title screen, menu navigation and a short repeatable gameplay sequence. Use exactly the loading path used for diagnostics; do not hide a hardcoded ROM path in the CPU or bypass its normal boot flow for a screenshot.

When a game fails, use a small diagnostic or unit test to isolate the first incorrect behavior. You can add file selection and metadata display early even though the game will not play until its hardware prerequisites are implemented.

## In C#

You will use strings for paths, byte arrays for binary contents, enums for small session states and exceptions for host I/O failures. Ordinary managed C# is sufficient. Core owns guest state; Desktop owns file access and the run/pause controls.

## C#/.NET concepts used here

- [Files and persistence](../csharp-and-dotnet/file-io.md) — [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file): binary reading and I/O operations.
- [Arrays](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft arrays](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): storage and indexing.
- [Enums](../csharp-and-dotnet/enums.md) and [exceptions](../csharp-and-dotnet/exceptions.md) — their local pages link to the relevant Microsoft references.

## What you should understand now

- [ ] Loading a ROM, executing it and making it playable are separate observable steps.
- [ ] File selection belongs in Desktop; cartridge visibility belongs in Core.
- [ ] Resetting a game should not erase its cartridge save.

## C#/.NET refresher

Begin with [file I/O](../csharp-and-dotnet/file-io.md), then revisit arrays and exceptions above. Use the official references for the particular operation you choose.

## Your implementation task

First accept a `.gba` path and show its filename, byte length and a clear load result. Leave execution disconnected until that works. Later add Open ROM, session controls and an integrated game test. Write all code yourself.

## Definition of done

- A selected `.gba` loads without editing source code; paths containing spaces work.
- A failed or cancelled selection does not destroy the previous session.
- Later, the chosen game reaches a reproducible gameplay scene with input, display and audio.
- Pause/resume and reset work, and switching games cannot mix their save data.
- The next lesson's close/reopen/Continue test passes.

## Common mistakes

- Treating successful file reading as proof that CPU emulation works.
- Reading binary ROM data as text, or putting file paths in Core.
- Requiring every user ROM to be copied into the repository.
- Clearing cartridge saves along with RAM during reset.

## Further reading

- [Cartridge hardware](README.md) — Game Pak addressing, BIOS and save protocols.
- [Testing strategy](../16-testing/README.md) — diagnose incompatibility through smaller tests.
- [Microsoft file I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/) — files versus streams.

## Next chapter

[Preserve in-game saves and add save states](saving-and-resuming.md).
