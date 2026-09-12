# Tiles and backgrounds: patterns plus placement

## Before the technical details

A tile is a reusable small picture block. A tile map chooses which block appears at each map position. The map is like a pattern of numbered stamps; it is different from the collection of stamp images. First practice lookup and splitting a position into a group and a position within that group.

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

### Look up a reusable pattern

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
string[] patterns = { "grass", "stone", "water" };
int[] arrangement = { 0, 1, 0 };
Console.WriteLine(patterns[arrangement[2]]);
```

Expected output:

```text
grass
```

Read the inner brackets first: arrangement position two contains zero. Then patterns position zero yields grass. The map stores choices; the pattern array stores the corresponding content.

### Split a position into a group and local position

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int position = 11;
int groupSize = 4;
Console.WriteLine(position / groupSize);
Console.WriteLine(position % groupSize);
```

Expected output:

```text
2
3
```

Zero-based groups start at positions zero, four and eight. Position eleven belongs to group two, local position three. Four is an invented group size; use the real tile dimensions from the lesson when doing hardware calculations.

### Try it before implementing

Draw three pattern choices and a four-cell map that reuses one pattern. Change one map entry, then change a shared pattern, and explain why their effects differ. Read about flips and palette selection after that distinction is clear.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

A tile is an 8 × 8 pattern. At 4 bits per pixel it occupies 32 bytes and chooses from a 16-colour bank. At 8 bits per pixel it occupies 64 bytes and indexes a 256-colour palette. Index zero is transparent for tiled layers. A map selects which tile appears at each location; a regular BG map entry also carries flip and palette-bank bits.

```text
screen coordinate
    ↓ apply scroll / wrap
map cell + position within 8×8 cell
    ↓ map entry selects tile, flips and palette bank
tile pixel index → palette colour → candidate pixel with priority
```

Modes 0–2 choose combinations of regular and affine backgrounds: Mode 0 has four regular BGs; Mode 1 has BG0/1 regular and BG2 affine; Mode 2 has BG2/3 affine. Regular maps use 16-bit entries and screen-block organization. Affine maps have different entry formats and sizes; do not reuse regular-map decoding unchanged.

Registers include BGCNT, horizontal/vertical offsets for regular BGs, and affine matrix/reference registers. VRAM contains both maps and tiles, palette RAM contains colours. Rendering follows display time; a first fixture freezes these inputs and samples an unscrolled scene.

## In our emulator

Start with one 8 × 8 tile and one palette, then a small repeated map. Separate map coordinates, local tile coordinates and final screen coordinates on paper. Add scrolling, flips, map block boundaries and mode combinations incrementally. A candidate pixel needs transparency and priority as well as colour.

## In C#

Nibble extraction uses masks/shifts and explicit byte indexing. Remainders and divisions can explain coordinates clearly before optimizing them. Avoid a new heap object per sampled pixel.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Render one 4-bpp tile from synthetic data, then repeat it through a regular background map. Add asymmetric patterns so flips and nibble order are observable.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/TileTests.cs` with a **public class named `TileTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test a tiny known map and tile fixture, then supported flip/palette cases. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~TileTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `TileTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- A hand-drawn 8 × 8 expected result matches pixel values.
- Horizontal/vertical flips and palette banks work.
- A map block boundary test catches incorrect row layout.

## Common mistakes

- Swapping high/low nibbles.
- Treating every map as one flat linear layout.
- Forgetting index-zero transparency.

## Further reading

[Tonc regular backgrounds](https://gbadev.net/tonc/regbg.html) — maps and tiles. [GBATEK BG controls](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — formats and modes.

## Next chapter

[Continue](sprites.md).
