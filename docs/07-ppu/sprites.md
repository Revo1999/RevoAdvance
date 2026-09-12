# Objects and OAM

## Before the technical details

A sprite is an object the display hardware positions and combines with backgrounds. Its attributes describe how to find and show its picture. OAM is the memory holding those attributes. Start by treating a description and the described image as separate data, and by practicing combined conditions.

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

### Group a few descriptive values

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Label label = new Label();
label.X = 2;
label.Text = "hello";
Console.WriteLine($"{label.X}: {label.Text}");

class Label
{
    public int X;
    public string Text = "";
}
```

Expected output:

```text
2: hello
```

A class groups related state. The initialized empty string gives `Text` a non-null starting value. This is an ordinary label, not a sprite class or an OAM format.

### Evaluate combined conditions explicitly

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
bool selected = true;
bool hidden = false;
if (selected && !hidden)
{
    Console.WriteLine("show label");
}
```

Expected output:

```text
show label
```

`!` negates a Boolean, so `!hidden` is true. The condition requires both selected and not hidden. Real object visibility has many more hardware rules; do not substitute this toy condition for them.

### Try it before implementing

Write a plain-language description of a movable label, separating its content from its position. Then list the OAM attributes from the lesson and identify which depend on regular versus affine mode before decoding them.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

Sprites are movable objects whose attributes reside in OAM. There are 128 entries, each spanning eight bytes. Three halfwords contain object attributes; the fourth participates in the interleaved affine-parameter layout rather than being a general fourth attribute. Shape and size together choose dimensions; affine and regular objects interpret some bits differently.

```text
one OAM entry (8 bytes)
+-------------+-------------+-------------+------------------+
| attr0       | attr1       | attr2       | affine parameter |
| Y, modes... | X, size...  | tile/prio...| interleaved      |
+-------------+-------------+-------------+------------------+
          ↓ tile data in VRAM + OBJ palette
       candidate pixel at current scanline X
```

Coordinates wrap within their encoded widths; an object can straddle the screen edge. DISPCNT selects 1D/2D object tile mapping. Objects have priority, colour-depth, mosaic and window/semitransparent modes. Affine objects select matrices distributed across OAM entries, with optional doubled bounding boxes; doubling bounds does not double the source texture.

## In our emulator

Inputs are OAM, OBJ VRAM, OBJ palette, display mode and scanline. Output is object candidates, including transparency and priority metadata. Begin with one regular object, then overlap, flips, wrapping and mapping modes. Hardware has per-line processing limits; unlimited objects per scanline is an early approximation to record, not the final specification.

## In C#

Decode fields into small values for reasoning. Do not reinterpret an arbitrary C# struct as eight hardware bytes without explicit layout/endian reasoning. OAM byte-write rules remain the bus's responsibility.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Render one asymmetric regular object, then two overlapping objects with equal and unequal priorities. Add edge wrapping before affine objects.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/SpriteTests.cs` with a **public class named `SpriteTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test a tiny object fixture with known position, visibility and supported attributes. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~SpriteTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `SpriteTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Position, shape/size and tile selection match a known fixture.
- Transparent pixels reveal the lower layer.
- Overlap tie behavior is verified against the reference.

## Common mistakes

- Treating the fourth halfword as unused padding.
- Decoding affine and normal bits identically.
- Assuming a copied struct containing array references is independent.

## Further reading

[Tonc regular sprites](https://gbadev.net/tonc/regobj.html) — object representation. [GBATEK OBJ](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — OAM modes, priorities and limits.

## Next chapter

[Continue](composition.md).
