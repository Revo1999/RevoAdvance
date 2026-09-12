# Performance without premature optimization

## Before the technical details

Optimization means improving a measured cost while preserving behavior. A benchmark measures performance; a correctness test checks answers. Learn how to time ordinary work, but expect tiny timings to vary because startup, compilation, scheduling and measurement overhead all contribute. This chapter can wait until you have a correct milestone.

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

### Keep a measurable result

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
long total = 0;
for (int value = 1; value <= 100; value++)
{
    total += value;
}
Console.WriteLine(total);
```

Expected output:

```text
5050
```

`long` is a signed 64-bit integer. The sum provides an observable result you can check before comparing performance. The expected answer comes independently from 100 × 101 / 2. The loop itself is not a benchmark methodology.

### Try it before implementing

Check the sum first. Later wrap repeated work in a Stopwatch experiment and report elapsed time separately from the sum, using Release builds and repeated measurements. Never put a guessed millisecond threshold in a deterministic hardware test.

Continue with the detailed lesson below after you can explain your prediction.


The first version should be correct, deterministic and readable. Optimize only after measuring a representative workload in Release with tracing controlled. Startup/JIT compilation can distort a tiny benchmark; compare warmed runs with identical inputs and correctness checks.

| Normal first version | Optimized later, if measurements justify it |
| --- | --- |
| Owned arrays | Span / ReadOnlySpan views to avoid copies |
| Simple concrete classes | Small structs where value semantics fit |
| Value parameters | ref / in when copy cost is demonstrated |
| Reusable managed buffers | Small bounded stackalloc scratch storage |
| Explicit endian conversion | MemoryMarshal only with verified assumptions |
| Safe managed operations | unsafe only for interop or measured bottlenecks |
| Readable methods | Inlining hints only after evidence |

`stackalloc` reserves temporary stack storage for unmanaged elements. For example `Span<int> scratch = stackalloc int[8];` creates bounded scratch space; initialize elements before reading. It is not for large buffers, persistent framebuffers or repeated allocations inside long loops. `readonly` restricts mutation, not object ownership. The JIT can eliminate some bounds checks; unsafe indexing is not your default response to seeing arrays.

Allocations per instruction, GC pressure and oversized state copies are useful suspects. Measure them rather than assume C# is slow. Do not use unsafe code simply because emulator development is low-level.

Read [stackalloc](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc) only when scratch buffers become relevant; use [GC](allocations-and-gc.md), [ref](ref-and-value-semantics.md), and [MemoryMarshal](memorymarshal.md) as later branches.


## Where this meets the GBA

- [Timing](../14-timing-and-scheduling/README.md)
- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain profiling cpu use and allocation in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Performance without premature optimization](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/); look specifically for **Profiling CPU use and allocation**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Record a baseline for one implemented subsystem: elapsed time, workload, configuration and allocated bytes. Change one measured bottleneck and rerun correctness tests before comparing.

## Run your performance experiment

After writing and saving your own timing experiment in `.work/SyntaxLab/Program.cs`, run it from the prepared repository-root terminal in Release mode:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj -c Release
```

Run the same command several times. Check that the computed answer stays correct; record elapsed time and allocation observations separately. Do not expect a fixed timing value. Save and repeat this command after each experiment change.

## Run and check your practice

Write your toy practice in `.work/SyntaxLab/Program.cs`, save, and run from the repository-root terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare your result with a prediction written before running; your own exercise values may differ from the worked example. Save and rerun this same command after each edit. This runs a console program, not xUnit.

For an exercise that asks for assertions or parameterized tests, use the [TestLab setup and complete test-file examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only). Put your own public test class in `.work/TestLab/PracticeTests.cs`; save it, then run:

```powershell
dotnet test .work/TestLab/TestLab.csproj --list-tests
dotnet test .work/TestLab/TestLab.csproj --logger "console;verbosity=normal"
```

The list must contain your methods, and the run must report actual executed cases with zero failures. If only the supplied generic Fact/Theory examples are present, expect three cases; adding your own increases that count. If no cases are discovered, check the public class/method and `[Fact]`/`[Theory]` attributes. After each edit, save and rerun the second command. For a reading-only part of the task, answer its questions on paper; no new test is needed for that part.

## Definition of done

- A proposed optimization has evidence and preserves observable behavior.

## Common mistakes

- Benchmarking Debug and generalizing to Release.
- Using aggressive inlining without measurement.
- Sacrificing guest timing to achieve host frame rate.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/) — Profiling CPU use and allocation. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
