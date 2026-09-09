# Save your game and continue later

Persistent in-game saves are a required part of the playable emulator. Save states are an additional, later feature. Neither modifies the original `.gba` ROM.

## In the real GBA

A game with saving support talks to a cartridge save device: SRAM, Flash or EEPROM. Choosing Save in the game makes guest code perform that device's protocol. The emulator must implement the appropriate protocol before writing a host file can preserve meaningful progress. A game without its own save feature does not acquire a Continue menu merely because the emulator can write files.

## Two different features

| Feature | What it captures | How you resume |
| --- | --- | --- |
| In-game/cartridge save | Persistent bytes written by the game | Open ROM normally, then use the game's Continue/Load menu |
| Emulator save state | A snapshot of the running machine, including hidden timing/device state | Choose Load State to resume that exact captured moment |

Use a separate save-data file, for example a `.sav`, for cartridge persistence. The extension is a host convention, not a hardware protocol or a guarantee of compatibility with another emulator. Save-state files need their own format/version and must not be mistaken for raw cartridge saves.

## In our emulator — cartridge persistence first

Core owns the emulated save device, including protocol state and persistent bytes. Desktop owns the save directory and file operations. Game accesses go through the cartridge bus logic: SRAM/Flash begin in the 0x0E000000 window, while EEPROM uses its serial cartridge-space protocol. Refer to [cartridge hardware](README.md) for the exact device requirements. Device timing uses guest cycles; host disk writes happen outside instruction execution.

```text
guest chooses Save → cartridge device receives writes → save data changes
                                                           ↓
                                            Desktop persists a snapshot
                                                           ↓
next launch → read matching save file → initialize device → game reads progress
```

Work through these exercises:

1. **Choose a stable identity.** A content hash identifies the exact ROM bytes; a filename alone can collide or change. A per-ROM save directory can use that identity, with a readable title for display. Different revisions may have different identities: transferring their saves should be deliberate.
2. **Load existing data before execution.** Select the device type/capacity and validate a save file against it. Missing data means a fresh cartridge; initialize according to that device's documented erased state, not blindly to C# array zeros. A malformed or wrong-sized save should not be silently truncated or overwritten.
3. **Track pending changes.** “Dirty” means persistent data has changed since the last successful disk write. Expose a consistent snapshot at a safe boundary; do not let a host write race with a changing buffer.
4. **Persist reliably.** Begin with an explicit Flush Save action for testing and flush on orderly close, ROM change and reset when needed. Then add periodic persistence of dirty data at safe host boundaries, so a long session does not depend entirely on closing cleanly. Do not perform disk I/O for every emulated save-device write.
5. **Protect the previous good save.** Write a temporary file in the destination directory, finish and close it, then replace the destination using supported filesystem operations. Consider a backup. Replacement/error/durability guarantees vary by filesystem; do not promise immunity to power loss. If persistence fails, retain pending data, report “save failed” and allow retry. Clear dirty state only after success and only for the version actually written.
6. **Resume in a fresh process.** Close the app completely, reopen the same ROM and verify the game's own Continue option restores progress. A reset within one process is not enough evidence that disk persistence works.

Start with a toy buffer round trip, then SRAM, then Flash and EEPROM as separate hardware lessons. If your chosen game uses Flash or EEPROM, implement that device before claiming that game's save support; an SRAM-only exercise is not sufficient.

## Later — Save State and Load State

Add named slots or explicit paths after deterministic timing and snapshots work. A state includes CPU banks/status, RAM, peripheral latches, timer remainders, active DMA, sound/FIFOs, cartridge protocol state and scheduler state. Record ROM identity and format version; validate before replacing the current machine. Host window/audio/GPU resources are recreated or refreshed rather than serialized.

An older state may contain older cartridge save bytes. Define this clearly: for example, restore those bytes into the session, report that progress has rolled back, and preserve the previous disk save as a backup before later persistence. Never overwrite a newer disk save as an unexplained side effect of merely reading a state file. Follow [the save-state/debugging lesson](../17-debugging-tools/README.md) for replay verification.

## In C#

Paths are strings, save contents are bytes, and a dirty marker is ordinary state. Use explicit ownership and host exceptions for disk errors. A copied array reference is not a stable snapshot; understand copying before adding background I/O. A synchronous implementation at a controlled boundary is enough for the first exercise.

## C#/.NET concepts used here

- [File I/O](../csharp-and-dotnet/file-io.md) — [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file): writes, replacement and failures.
- [Value/reference semantics](../csharp-and-dotnet/ref-and-value-semantics.md) and [arrays](../csharp-and-dotnet/arrays-and-spans.md) — snapshots must preserve values.
- [Exceptions](../csharp-and-dotnet/exceptions.md) and [testing](../csharp-and-dotnet/testing.md) — their official references explain errors and observable assertions.

## What you should understand now

- [ ] Cartridge emulation and host persistence are both required for in-game saves.
- [ ] Cartridge saves and save states have different contents and restore behavior.
- [ ] A failed write must not destroy the last good save or discard pending data.

## C#/.NET refresher

Read [files and persistence](../csharp-and-dotnet/file-io.md) first, then arrays and reference semantics. The paired Microsoft references above explain the tools without providing a save manager implementation.

## Your implementation task

Persist and reload a tiny synthetic byte buffer in an isolated temporary directory. Then connect the same ownership/persistence decisions to your first emulated save device. Finally perform the actual game's Save → close app → reopen → Continue workflow yourself.

## Definition of done

- A game with an implemented save device preserves progress across a complete app restart.
- Original ROM contents remain unchanged; each ROM's save data stays separate.
- Reset and game switching preserve progress; a renamed identical ROM finds its data under your chosen identity policy.
- Missing, malformed and unwritable-save cases have explicit tested outcomes; failure preserves the prior good file.
- Later Save State/Load State resumes a known moment and passes deterministic replay, with an explicit cartridge-save rollback policy.

## Common mistakes

- Writing save bytes into the `.gba` file.
- Implementing only file writes while ignoring the game's Flash/EEPROM protocol.
- Testing only reset, leaving disk persistence untested.
- Clearing dirty state before a write succeeds or retaining a shared mutable array as a snapshot.
- Treating save-state formats as automatically portable across versions or emulators.

## Further reading

- [GBATEK cartridges](https://mgba-emu.github.io/gbatek/#gbacartridges) — choose the device and its command behavior.
- [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file) — inspect the selected read/write/replace methods and documented exceptions.
- [Save-state internals](../17-debugging-tools/README.md) — hidden state and replay.

## Next chapter

[Test the integrated game workflow](../16-testing/README.md), then return to your current [roadmap phase](../../ROADMAP.md).
