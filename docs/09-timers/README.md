# Timers: counters driven by guest time

## Before the technical details

A hardware timer counts guest clock events. A prescaler makes it count less frequently, and a reload value is the value it resumes from after overflow. None of these is a Windows timer callback. Learn whole groups and leftover units before modeling the counter rules.

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

### Count full groups and leftovers

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int beads = 17;
int perBag = 5;
Console.WriteLine(beads / perBag);
Console.WriteLine(beads % perBag);
```

Expected output:

```text
3
2
```

Integer `/` gives whole groups here. `%` gives the remainder. Three bags use fifteen beads, leaving two. These invented units explain division; five is not a GBA prescaler setting.

### Keep configuration separate from current progress

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int startingScore = 10;
int score = startingScore;
score += 3;
Console.WriteLine(startingScore);
Console.WriteLine(score);
```

Expected output:

```text
10
13
```

The remembered starting value and current value answer different questions. Giving them separate names prevents a later update from accidentally changing both. Real timer enable and reload behavior must come from the detailed rules.

### Try it before implementing

Add four more beads to the leftover two and predict how many full bags can now be made. Explain why throwing away leftovers after each batch gives a different answer. Write a before/at/after table around a timer boundary before coding.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

Four 16-bit timers count prescaled system clocks or, for timers 1–3, overflows from the preceding timer. The clock divisors are 1, 64, 256 and 1024. Each timer has a reload value and control bits; overflow reloads the counter and can request an interrupt. Timer-driven Direct Sound consumes samples independently of the desktop audio callback.

Registers occupy 0x04000100–0x0400010E: each timer has a low counter/reload halfword and a control halfword. Reading the low register returns the live count; writing supplies a reload value. Enable transitions and timing of writes need explicit behavior.

```text
system cycles → prescaler → timer 0 overflow → timer 1 (cascade)
                                                  ↓ overflow
                                            timer 2 → timer 3
```

## In our emulator

Track live counters, reload values, enable/cascade state and fractional prescaler progress. Inputs are elapsed guest cycles and writes; outputs are counters and overflow events consumed by IRQ/audio/other timers. Advancing by a large batch may overflow more than once. Preserve leftover cycles and event ordering.

## In C#

ushort expresses stored counter width; a wider temporary helps reason about multiple elapsed ticks. Host arithmetic promotion and casts should not silently decide reload semantics. State-owning classes or carefully mutated structs both work if ownership is clear.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Properties and fields](../csharp-and-dotnet/properties-and-fields.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties): Accessors and encapsulation.
- [Ref and value semantics](../csharp-and-dotnet/ref-and-value-semantics.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters): Pass by value, ref, in and out.

## What you should understand now

- [ ] Reload state differs from the live counter.
- [ ] A guest clock is independent of host elapsed milliseconds.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement one timer with a prescaler and reload, then cascade a second. Test batch advancement against repeated small advances.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/TimerTests.cs` with a **public class named `TimerTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test prescaler remainders, reload, overflow and batch-versus-small-step advancement. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~TimerTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `TimerTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Divisor boundaries keep remainders.
- Overflow reload and IRQ occur at predicted guest times.
- Two timers cascade without using host wall time.

## Common mistakes

- Using System.Timers.Timer to emulate hardware ticks.
- Losing overflow events in a large cycle batch.
- Mutating a copied struct and discarding the result.

## Further reading

- [GBATEK timers](https://mgba-emu.github.io/gbatek/#gbatimers) — reload, cascade and control bits.
- [Tonc timers](https://gbadev.net/tonc/timers.html) — prescaling and overflow reasoning.

## Next chapter

[DMA: timed transfers with bus ownership](../10-dma/README.md)
