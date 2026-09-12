# Cartridges, BIOS and persistent data

## Before the technical details

A ROM image is a sequence of bytes representing cartridge program/data storage. BIOS is separate firmware; cartridge save data is separate persistent storage. Reading a file into memory is a host operation. Making the guest see the correct cartridge behavior is an emulation task. Start with bytes and read-only views.

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

### Inspect bytes without interpreting them as text

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] sample = { 0x41, 0x00, 0xFE };
Console.WriteLine(sample.Length);
Console.WriteLine(sample[2].ToString("X2"));
```

Expected output:

```text
3
FE
```

`Length` counts bytes in this array. `ToString("X2")` displays a hexadecimal value with at least two digits. Binary contents can include zero and values that do not form text; formatting a byte for inspection does not change it.

### A read-only view is not a frozen snapshot

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] source = { 7, 8 };
ReadOnlySpan<byte> view = source;
source[0] = 9;
Console.WriteLine(view[0]);
```

Expected output:

```text
9
```

`ReadOnlySpan<byte>` prevents writing through this view. The array owner can still change the same storage. “Read-only to this caller” and “immutable forever” are different promises.

### Try it before implementing

Change the sample bytes and predict their hex display. Draw separate boxes for ROM, BIOS, RAM and cartridge save data, and mark which survive closing the app. Keep file paths out of your Core design.

Continue with the detailed lesson below after you can explain your prediction.


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

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/CartridgeTests.cs` with a **public class named `CartridgeTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test the implemented cartridge reads and save-device protocol using synthetic bytes. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~CartridgeTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `CartridgeTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

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
