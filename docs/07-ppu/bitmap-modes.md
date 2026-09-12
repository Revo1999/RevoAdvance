# Bitmap modes: the shortest path to a pixel

## Before the technical details

A bitmap stores picture data in a direct row-and-column arrangement. Some formats store colours directly; others store indexes into a palette. A page is one separately addressed image area, not a desktop window. Learn the difference between an index and a value before working through the GBA bitmap modes.

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

### Follow an index to its value

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int[] brightness = { 10, 40, 90 };
byte selection = 1;
Console.WriteLine(selection);
Console.WriteLine(brightness[selection]);
```

Expected output:

```text
1
40
```

The stored index is one; the looked-up brightness is forty. An index cannot be displayed as if it were already the intended colour. This three-entry table is invented.

### Scale a toy numeric range

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int level = 3;
int maximum = 7;
int percent = level * 100 / maximum;
Console.WriteLine(percent);
```

Expected output:

```text
42
```

Integer operations execute with integer truncation here. Multiplying first preserves more information than dividing `3 / 7` first, which yields zero. This is a toy seven-step scale, not a GBA colour conversion formula.

### Try it before implementing

Predict the brightness for selections zero and two. Draw a tiny bitmap once with values and once with palette indexes. Read the actual channel widths and mode dimensions below before choosing conversion or addressing arithmetic.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

Bitmap modes make BG2 use a pixel image instead of a tile map. They still participate in display enabling and composition. DISPCNT mode bits choose the format; its BG2 enable bit matters. BG2 affine state also affects sampling, so a first fixture should explicitly use identity transformation.

| Mode | Image dimensions | Pixel storage | Pages |
| --- | --- | --- | --- |
| 3 | 240 × 160 | 16-bit storage, 15-bit RGB colour | one at VRAM base |
| 4 | 240 × 160 | 8-bit palette index | bases 0x06000000 / 0x0600A000 |
| 5 | 160 × 128 | 16-bit storage, 15-bit RGB colour | same two page bases |

The LCD remains 240 × 160 in Mode 5. The bitmap is smaller; what appears outside it depends on sampling/bounds and composition. Page selection comes from DISPCNT's frame-select bit for Modes 4/5. Do not pack the pages immediately next to the used pixel bytes.

```text
15 14......10 9.......5 4.......0
 X    blue      green      red     direct-colour halfword
```

Colour components range from 0 to 31. Converting them to host 0–255 channels is a deliberate conversion, not a byte reinterpretation. Bit 15 is not an alpha bit. In indexed Mode 4, index zero is transparent for BG composition; direct-colour black in Modes 3/5 is a visible colour. The backdrop can make those cases look similar in a single-layer fixture.

## In our emulator

Use synthetic VRAM, palette and display state as inputs; produce a final buffer or a BG2 candidate buffer with explicitly documented scope. Start with Mode 3, identity coordinates and no effects. Work out row stride from pixel width and bytes per pixel. Render a few coloured corners, row/column markers and a centre block before arbitrary artwork.

For a first isolated test, timing is frozen. When integrating, render according to [display timing](display-timing.md), documenting the scanline approximation.

## In C#

Arrays store pixels or bytes; integer arithmetic maps coordinates to offsets. Confirm byte order and bounds before colour conversion. Host output formats such as RGBA and BGRA are different; name your choice.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Create a synthetic Mode 3 fixture and your own converter. Verify explicit corner colours and row orientation. Export an image or inspect it headlessly before adding Vulkan.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/BitmapTests.cs` with a **public class named `BitmapTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test the first bitmap mode you implemented, including known pixel positions and colours. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~BitmapTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `BitmapTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- All four corners have predicted values and positions.
- Red/green/blue maxima and black are correct.
- Later Mode 4 tests distinguish transparent index zero and page selection.

## Common mistakes

- Treating Mode 5 as a smaller LCD.
- Using palette indices as direct colours.
- Reading 16-bit pixels in host-native byte order.

## Further reading

[Tonc bitmap modes](https://gbadev.net/tonc/bitmaps.html) — pixel organization. [GBATEK video](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — mode/register details.

## Next chapter

[Continue](display-timing.md).
