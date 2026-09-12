# Debugging and reproducible state

## Before the technical details

Debugging means finding the earliest point where actual state differs from expected state. A trace records a sequence of observations. A snapshot preserves values at a chosen moment. Inspecting a live reference later is different from capturing what it contained earlier. Practice that distinction before building a debugger UI or save-state format.

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

### Capture data instead of another reference

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int[] live = { 2, 4 };
int[] alias = live;
int[] snapshot = (int[])live.Clone();
live[0] = 9;
Console.WriteLine(alias[0]);
Console.WriteLine(snapshot[0]);
```

Expected output:

```text
9
2
```

`Clone()` creates another array; the cast states the array type of the returned object. For integer elements, copied values form an independent snapshot. Arrays of mutable objects need deeper ownership reasoning because cloning their array still copies references.

### Print a compact observation

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int step = 3;
uint value = 42u;
Console.WriteLine($"step={step} value=0x{value:X8}");
```

Expected output:

```text
step=3 value=0x0000002A
```

Inside an interpolated string, `:X8` displays at least eight hexadecimal digits. Labeling both the moment and value makes a trace easier to compare. Formatting a value does not freeze an entire mutable machine.

### Try it before implementing

Make a three-step paper trace and deliberately change the second result. Identify the first divergence, not only the final wrong answer. List which arrays in a future snapshot must be copied and which host resources must be recreated.

Continue with the detailed lesson below after you can explain your prediction.


## Why this exists

An emulator bug is often an incorrect state transition many instructions before the visible symptom. Start with a compact trace and breakpoints; build elaborate UI only after those help solve real failures. Debugging tools observe Core state; they are not emulated hardware registers.

Useful observations include instruction address/bits, ARM/Thumb state, selected registers/CPSR, memory access address/width/value, guest timestamp and peripheral event. A read-only debugger memory view should not accidentally trigger a side-effecting emulated register read. Define “peek for inspection” separately if needed.

```text
known initial state → recorded input/events → first divergent transition
                                                 ↓
                                       smallest regression test
```

## Save states are a later milestone

User-facing Save State/Load State slots and their interaction with cartridge saves are described in [saving and resuming](../12-cartridges-and-roms/saving-and-resuming.md). Normal in-game saving is a required earlier feature; a save state supplements it.

A state must preserve everything needed to reproduce future execution: CPU banks/status, RAM, peripheral registers and hidden latches, timer remainders, DMA active state, audio phase/FIFOs, pending events and cartridge protocol state. ROM identity and a format version protect against restoring into the wrong environment. Store explicit data, not raw object layouts or host pointers. Flush/recreate host output resources separately after restore.

A cartridge save file contains persistent game data; a save state captures a moment of emulation. Neither should serialize Vulkan handles or live .NET references. Test save → run N cycles → restore → run N cycles with identical input and compare resulting state/pixels/samples.

## In C#

Control trace allocations and preserve values, not references to mutable live objects. Start with textual output behind an explicit enable flag. A bounded ring buffer can be added if profiling shows logs are too expensive; it need not be a framework.


## C#/.NET concepts used here

- [Ref and value semantics](../csharp-and-dotnet/ref-and-value-semantics.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters): Pass by value, ref, in and out.
- [Allocations and garbage collection](../csharp-and-dotnet/allocations-and-gc.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Reachability, collection and generations.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] Useful traces capture transitions with guest timestamps.
- [ ] Save-state completeness includes hidden state.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Add a bounded trace of the smallest state transition needed to diagnose your current failure. Later implement versioned save/restore after timing state stabilizes.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/DebugStateTests.cs` with a **public class named `DebugStateTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test captured values, tracing on/off equivalence and later deterministic save/restore replay. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~DebugStateTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `DebugStateTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- A trace identifies the first divergence in a failing case.
- Tracing disabled does not change emulated results.
- Later save/restore replay yields identical future state for identical inputs.

## Common mistakes

- Taking shallow copies of arrays for snapshots.
- Serializing native pointers.
- Observing I/O through normal reads that mutate the machine.

## Further reading

- [GBATEK](https://mgba-emu.github.io/gbatek/) — resolve the behavior at the first divergent transition.
- [Microsoft diagnostics](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/) — separate host performance problems from guest correctness.

## Next chapter

[Return to your next milestone](../../ROADMAP.md)
