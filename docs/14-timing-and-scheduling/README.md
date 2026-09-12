# One guest timeline

## Before the technical details

A cycle is a unit of guest time. A timestamp is a position on that timeline; a duration is a distance between two positions. A scheduler decides what work is due. Deterministic means identical initial state and inputs produce identical results. Use ordinary numbers first, with no sleeping or background threads.

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

### Compare an absolute time with a deadline

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
ulong now = 12UL;
ulong deadline = 15UL;
Console.WriteLine(now >= deadline);
now += 3UL;
Console.WriteLine(now >= deadline);
```

Expected output:

```text
False
True
```

`ulong` is an unsigned 64-bit integer and `UL` spells a literal of that type. `>=` includes the exact boundary. This checks a deadline without using the host clock; it is not a scheduler loop.

### Measure a duration after checking order

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
ulong start = 20UL;
ulong end = 27UL;
if (end >= start)
{
    Console.WriteLine(end - start);
}
```

Expected output:

```text
7
```

`if` executes its block only when the condition is true. Subtracting a later unsigned timestamp from an earlier one can underflow, so establish the ordering. The result is elapsed units, not another absolute timestamp.

### Try it before implementing

Test a deadline at one unit before, exactly at and one after. Draw two events with the same timestamp and write down that their ordering needs a rule. The hardware tests must justify that rule later.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

The master clock is 16,777,216 Hz. A scanline spans 1,232 cycles and a frame has 228 lines, giving 280,896 cycles per frame (about 59.73 Hz). Display, timers, sound, DMA and CPU activity interact on this shared timeline. The host monitor need not refresh at the same rate.

## In our emulator — version 1

Use a single-threaded deterministic scheduler with an explicit guest cycle counter. At first, complete one instruction, account for a documented approximation of its cycles, then process due hardware events. Preserve all elapsed cycles and handle multiple events when crossing boundaries. A scanline PPU is an acceptable early limitation, recorded as such.

```text
choose next CPU / DMA activity
advance guest time by consumed cycles
process due events in a documented order
reconsider pending IRQs and CPU sleep state
repeat until requested boundary
```

This pseudocode identifies responsibilities, not an implementation. Do not make “render a whole frame” the operation after each CPU instruction. If the CPU is halted, jump to the next relevant hardware event rather than freezing timers/PPU.

## Later — improve timing accuracy

Account for bus wait states, sequential accesses, instruction internal cycles, DMA contention, exact event edges and pipeline refill. Event-boundary stepping can split work that an instruction-boundary model handles late. Register writes near a display/timer boundary are valuable diagnostics. Define ordering for equal-timestamp events and validate it against hardware tests.

Inputs are CPU/DMA elapsed-time requests and scheduled events; outputs are component progression and new requests. The scheduler owns time, while devices own their registers. Desktop sleeps or paces presentation only after guest work is measured; wall time must not alter deterministic test behavior.

## In C#

Use an explicit sufficiently wide counter and predictable loops. A ulong can represent long sessions; conversion between signed/unsigned timestamp differences needs care. Start with a few next-event counters before a generic event framework. Profile Release execution later; unsafe and parallel tasks are unnecessary for this model.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [How C# becomes machine code](../csharp-and-dotnet/runtime.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process): IL, JIT compilation and runtime services.
- [Performance without premature optimization](../csharp-and-dotnet/performance.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/): Profiling CPU use and allocation.
- [Allocations and garbage collection](../csharp-and-dotnet/allocations-and-gc.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Reachability, collection and generations.

## What you should understand now

- [ ] Functional correctness and timing accuracy are distinct milestones.
- [ ] All devices progress when CPU execution is stalled.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Advance display and one timer from a common guest counter. Compare a run in large chunks with the same elapsed time in small chunks, recording any version-1 ordering limitations.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/SchedulingTests.cs` with a **public class named `SchedulingTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test guest timestamps, boundaries, batch stepping and HALT peripheral progression. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~SchedulingTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `SchedulingTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- A frame has exactly 280,896 guest cycles.
- HALT permits peripheral progress.
- Repeated runs yield the same event log and state.

## Common mistakes

- Using monitor refresh as the GBA clock.
- Dropping remainder cycles at each frame.
- Allowing C# counter wrap or signed conversions to reorder events.

## Further reading

- [GBATEK timing](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — display boundaries and peripheral timing.
- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — instruction cycle timing and memory cycles.

## Next chapter

[Vulkan: presenting the finished framebuffer](../15-vulkan-output/README.md)
