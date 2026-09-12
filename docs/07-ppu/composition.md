# Affine sampling, priorities, windows and effects

## Before the technical details

Composition chooses a final pixel from multiple candidates, then applies the permitted effects. Priority is an ordering rule; transparency says a candidate may contribute nothing. Blending combines permitted candidates numerically. Learn explicit choices before trying to make all these rules interact.

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

### Choose between two candidates

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
bool firstAvailable = false;
string chosen = firstAvailable ? "first" : "second";
Console.WriteLine(chosen);
```

Expected output:

```text
second
```

`condition ? valueIfTrue : valueIfFalse` is the conditional operator. It chooses one value. This illustrates syntax, not the actual GBA priority or transparency decision.

### Make a numeric limit explicit

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int requested = 14;
int bounded = Math.Clamp(requested, 0, 10);
Console.WriteLine(bounded);
```

Expected output:

```text
10
```

`Math.Clamp(value, minimum, maximum)` keeps a value inside the specified inclusive range. A hardware effect has its own documented ranges and rounding rules; the toy range zero through ten is not one of those rules.

### Try it before implementing

Make a paper table of two candidates with different visibility and priority. Include a tie so you must ask for a tie-break rule. Then read the actual composition order and effects rules; do not infer them from host draw-call order.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

The final pixel is chosen from eligible background, object and backdrop candidates. Lower numeric priority is generally in front; ties need hardware-specific layer/OAM ordering. Transparent index zero removes a candidate, rather than producing black. Window masks can disable layers or effects at a screen location before the final composition decision.

Affine rendering maps a destination coordinate to a source coordinate using a matrix and reference point. The signed fixed-point registers encode fractional steps; this is sampling, not physically rotating bytes in VRAM. Background and object affine behavior have distinct bounds and reference rules. BG reference-point registers and per-line internal state matter when software writes them mid-frame.

```text
destination (x,y) → fixed-point affine mapping → source sample
                                                     ↓
candidate layers → window eligibility → priority → effects → final pixel
```

WIN0/WIN1 rectangles and OBJ-window pixels select masks via WININ/WINOUT. BLDCNT chooses effects/eligible targets; BLDALPHA chooses blend coefficients; BLDY controls brighten/darken. Coefficients have documented effective limits and output clamps. A semitransparent OBJ has special blending behavior; it is not general modern per-pixel alpha. MOSAIC groups sample positions and is another later independent feature.

## In our emulator

Keep enough candidate metadata to explain why a pixel wins. First solve opaque priority and transparency; add windows, then alpha/brightness effects, then affine edge cases and mosaic. Inputs include register state and per-layer samples; outputs are final colours. Scanline latching is an initial timing approximation, particularly visible with affine reference and window writes.

## In C#

Use signed integer reasoning for affine coefficients and wide enough intermediates. Fixed point stores an integer scaled by a power of two; fractional position is preserved until deliberately reduced. Generic floating-point transforms may obscure the exact rounding rules the GBA uses.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Create tiny overlap fixtures: transparent/opaque BG, equal priorities, a masked window and one blend. Implement identity affine sampling before rotations.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/CompositionTests.cs` with a **public class named `CompositionTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test known candidate pixels, priorities, ties and the effects you implemented. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~CompositionTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `CompositionTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- A single pixel trace names the winning layers and applied effect.
- Identity affine output matches untransformed output.
- Boundary/clamping cases use independently calculated expectations.

## Common mistakes

- Using float rounding without comparing hardware fixed-point rules.
- Treating every transparent pixel as black.
- Applying blend effects before window eligibility.

## Further reading

[Tonc effects](https://gbadev.net/tonc/gfx.html) — windows and colour effects. [Tonc affine](https://gbadev.net/tonc/affine.html) — transform interpretation. [GBATEK](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — exact registers and composition rules.

## Next chapter

[Continue](../08-interrupts/README.md).
