# VRAM is a mode-dependent workspace

## Before the technical details

VRAM is guest video memory. Its meaning depends on how display hardware is configured: the same bytes can be interpreted differently in different modes. Storage size, address window and a view into storage are different ideas. Practice using a view without allocating another backing array.

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

### Create a bounded view into storage

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] storage = { 10, 20, 30, 40, 50 };
Span<byte> middle = storage.AsSpan(1, 3);
Console.WriteLine(middle.Length);
Console.WriteLine(middle[0]);
```

Expected output:

```text
3
20
```

`AsSpan(1, 3)` uses start index one and length three, not an ending index. View index zero refers to storage index one. The view has its own bounds but shares the bytes.

### Compare a copy with a view

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] storage = { 10, 20, 30, 40 };
byte[] copy = storage[1..3];
Span<byte> view = storage.AsSpan(1, 2);
view[0] = 99;
Console.WriteLine(storage[1]);
Console.WriteLine(copy[0]);
```

Expected output:

```text
99
20
```

For an array, `[1..3]` copies indexes one and two into a new array. A span refers to existing storage. Neither operation by itself implements guest mirroring or VRAM access rules.

### Try it before implementing

Draw the shared storage and the copied array separately. Annotate the exact indexes covered by the view. When reading the real layout, label which facts describe physical storage and which describe address decoding.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

VRAM has 96 KiB of physical storage. Its layout changes with video mode. In tiled modes, the first 64 KiB serves backgrounds and the final 32 KiB serves objects. In bitmap modes, bitmap pages occupy background storage and object tile data is restricted to the final 16 KiB starting at 0x06014000.

```text
Tiled:   06000000 [ BG tiles / maps: 64 KiB ] 06010000 [ OBJ:32 KiB ] 06018000
Bitmap:  06000000 [ bitmap area:    80 KiB ] 06014000 [ OBJ:16 KiB ] 06018000
```

Tiled backgrounds choose character blocks (tile data) and screen blocks (maps) through BGCNT. These are interpretations of the same storage, so careless placement can overlap them. Palette RAM is separate: 512 bytes for BG palettes and 512 bytes for OBJ palettes. OAM is also separate.

Address mirroring is not a simple modulo-96-KiB rule. The upper part of the 128-KiB VRAM window aliases part of the physical storage. Byte-write behavior also depends on whether the destination lies in the current mode's BG/OBJ area. Read the bus rules before implementing writes.

## In our emulator

Maintain one physical VRAM backing store and interpret it through display state. Inputs are bus accesses and mode configuration; output is the data sampled by BG/OBJ rendering. Do not move bytes when changing modes. Display-time access restrictions and exact mid-frame changes can be later refinements with documented limits.

## In C#

Bounded spans can describe views into an array without copying. A view does not enforce hardware layout or prevent overlap; your configuration decoding does that.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Draw memory placement for one BG tile set and one map without overlap. Implement the relevant addressing yourself, then test one documented VRAM mirror.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/VramTests.cs` with a **public class named `VramTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test the implemented physical layout, access widths and mirroring rules. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~VramTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `VramTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Changing mode changes interpretation without copying VRAM.
- A mirror test accesses the intended physical byte.

## Common mistakes

- Allocating independent arrays for overlapping character and screen blocks.
- Mirroring with modulo physical size.
- Assuming a span owns independent bytes.

## Further reading

[GBATEK memory/video](https://mgba-emu.github.io/gbatek/#gbamemorymap) — mirroring and write rules. [Tonc tiles](https://gbadev.net/tonc/objbg.html) — shared video storage.

## Next chapter

[Continue](tile-modes.md).
