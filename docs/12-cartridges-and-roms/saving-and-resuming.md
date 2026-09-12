# Save your game and continue later

## Before the technical details

Persistence means data survives the end of a process. A cartridge save preserves the game’s saved progress; an emulator save state preserves a running machine moment. A dirty marker means data has changed since it was successfully persisted. First understand stable copies and versions before choosing disk operations.

## Syntax warm-up

### Open PowerShell and prepare this lesson

Open a PowerShell terminal (an IDE terminal is fine). Run this block once in each new terminal. The path below is your current checkout; if you move the repository, change that first path. All later commands on this page run from this folder, not from the lesson folder.

```powershell
Set-Location "C:\Users\victo\Desktop\RevoAdvance"
if (Test-Path ".work/dotnet10/dotnet.exe") {
    $env:PATH = "$PWD\.work\dotnet10;$env:PATH"
}
dotnet --version
```

Expect a version beginning with `10.`. The conditional uses the local SDK when present and changes PATH only for this terminal. If the command is missing or shows `8.`, complete the [.NET 10 setup](../00-getting-started/before-you-code.md#set-up-and-know-what-success-looks-like) before continuing.

Create the console scratchpad only if it does not already exist:

```powershell
if (-not (Test-Path ".work/SyntaxLab/SyntaxLab.csproj")) {
    dotnet new console --framework net10.0 --output .work/SyntaxLab
}
```

If it already exists, no output from that block is expected. Keep using that project; do not create another project for each example. [Command troubleshooting](../00-getting-started/running-and-testing.md) explains errors and the difference between running and testing.

Each example below is a complete, independent console program. Run one at a time in [SyntaxLab](../00-getting-started/before-you-code.md#a-separate-place-to-try-the-examples). These toy examples teach C#; the emulator implementation remains your exercise.

### Freeze a tiny byte snapshot

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] live = { 3, 5 };
byte[] saved = new byte[live.Length];
Array.Copy(live, saved, live.Length);
live[0] = 8;
Console.WriteLine(saved[0]);
Console.WriteLine(live[0]);
```

Expected output:

```text
3
8
```

`new byte[...]` allocates separate storage and `Array.Copy` copies the elements. Since elements are bytes, later writes to `live` do not change `saved`. Nothing has reached disk yet; this is an in-memory snapshot only.

### Distinguish an old version from current data

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int copiedVersion = 4;
int currentVersion = 5;
Console.WriteLine(copiedVersion == currentVersion);
```

Expected output:

```text
False
```

Version numbers can identify which data was copied. A completed write of an older copy cannot prove newer data is saved. This comparison illustrates the question, without supplying a persistence manager or save-device protocol.

### Try it before implementing

Draw live bytes, copied bytes and disk bytes as three separate boxes. Walk through a failed disk write on paper and state which data must remain available. Practice file operations only with synthetic data, then implement the real save workflow yourself.

Continue with the detailed lesson below after you can explain your prediction.

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

## Run and check your own implementation

Use the repository-root PowerShell terminal prepared above. Save your changes and run these separately before the manual host check:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

Expect a successful build and zero failures in the Core tests you have written. The untouched scaffold has no tests, so an empty test result proves no behavior. These tests do not launch or validate the desktop UI.

For the first toy disk exercise, write your own synthetic-byte program in `.work/SyntaxLab/Program.cs` and use a disposable directory such as `.work/SavePractice`. Run it once to write; change it to read, save, and run it again. Each `dotnet run` starts a fresh process. Compare exact bytes, and try an invalid destination to check that failure is reported.

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

For the later implemented game workflow, replace the example path below with your actual ROM path, then run:

```powershell
dotnet run --project src/Gba.Desktop/Gba.Desktop.csproj -- "C:\Games\Your Game.gba"
```

Use the game's Save menu, close the app completely and wait for the PowerShell prompt to return. Run the same command again and choose Continue in the game. Verify the saved progress. Reset within the same process is not this test. Use a copied disposable save fixture for failure experiments, never your only real save.

After changes, save and repeat the same commands and manual steps. Record what you actually observed, including any feature you have not implemented yet.

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
