# Evidence before game compatibility

## Before the technical details

A test is a reproducible question with an expected answer. Arrange chooses the starting state; Act performs one operation; Assert compares the outcome. An oracle is an independently known answer, often calculated on paper. A unit test narrows the question; an integration test combines several parts. Begin with a deliberate mismatch you can explain.

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

### Separate expected and actual values

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int expected = 9; // worked out independently
int actual = 4 + 5;
Console.WriteLine(actual == expected);
```

Expected output:

```text
True
```

This console comparison is a rehearsal. In xUnit you would use `Assert.Equal(expected, actual)` in a test method so disagreement fails the test run. Calculate the expected answer independently rather than calling the implementation twice.

### List useful boundary cases

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int[] positions = { -1, 0, 3, 4 };
foreach (int position in positions)
{
    bool inside = position >= 0 && position < 4;
    Console.WriteLine($"{position}: {inside}");
}
```

Expected output:

```text
-1: False
0: True
3: True
4: False
```

`foreach` visits each value in a collection. The cases straddle both ends of a four-element range. This illustrates test selection; your real tests need assertions and should catch a plausible incorrect implementation.

### Try it before implementing

Change `< 4` to `<= 4` and identify which case exposes the mistake. Restore it. Read the complete generic xUnit example in the testing refresher, then write your own subsystem test. A console message alone is not an automated test result.

Continue with the detailed lesson below after you can explain your prediction.


## Strategy

“Does a game boot?” is a useful integration observation, but a failure could originate almost anywhere. Build small independent oracles (known expected results) before relying on a game screen.

| Level | Example evidence | Why it isolates a bug |
| --- | --- | --- |
| Bits | field extraction with surrounding ones | reveals mask/shift errors |
| Memory | first/last byte, widths, mirrors, endian | isolates bus routing |
| Decode | fixed opcode with expected fields | no execution or host required |
| Execute | chosen initial/final registers and memory | checks one operation |
| Flags | zero, sign, carry, overflow boundary cases | distinguishes arithmetic interpretations |
| Timing | event before/at/after boundary | exposes off-by-one scheduling |
| PPU | exact pixels from tiny synthetic fixtures | isolates mode/address/priority behavior |
| Diagnostic ROM | reproducible report from known suite revision | integrates CPU, bus and devices |
| Game | boot/input/audio plus regression observations | broad compatibility evidence |

Keep generated fixtures small and describe what they prove. A synthetic Mode 3 image validates pixel conversion, not instruction execution. A CPU diagnostic may need stack, BIOS calls, interrupts or video before it can report failures. Inventory those prerequisites before interpreting a blank screen.

## Test projects and diagnostic ROMs

For real-game integration, use the normal [Open ROM workflow](../12-cartridges-and-roms/loading-and-playing.md), not a hardcoded test-only path. Verify loading a path with spaces, pause/resume, reset and changing games. For a game with the implemented save device, choose Save in-game, close the entire app, reopen the ROM and choose Continue. Check that another ROM cannot inherit its save data and that a failed persistence attempt preserves the previous good file. See [save/resume acceptance criteria](../12-cartridges-and-roms/saving-and-resuming.md).

Use `tests/Gba.Core.Tests` for deterministic xUnit cases. [The testing refresher](../csharp-and-dotnet/testing.md) shows Fact/Theory, assertions and Arrange/Act/Assert using generic arithmetic. No dummy passing test is shipped. Your first low-byte test is the first actual test.

Use [mGBA's test suite](https://github.com/mgba-emu/suite) and [gba-tests](https://github.com/jsmolka/gba-tests) as test resources; read their build instructions and licenses. Supply/build ROMs yourself in [roms](../../roms/README.md); pin revision/hash in the log. A reference emulator is useful for comparison but not infallible. Resolve conflicts using hardware documentation and hardware-backed tests, not majority vote between emulators.

For every failure, record test version, BIOS strategy, starting state, expected behavior, actual behavior, and the smallest instruction/event trace that distinguishes them. Avoid full-frame logs when ten events reveal the first divergence.

## In C#

Pure decoding tests need no expensive system setup. Integration fixtures should deliberately reset all state rather than share mutable objects across tests. Compute expected values independently; do not call the same helper in both expected and actual paths.


## C#/.NET concepts used here

- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.
- [Host exceptions and guest exceptions](../csharp-and-dotnet/exceptions.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/): Throw, try, catch and finally.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.

## What you should understand now

- [ ] Different tests prove different layers.
- [ ] Diagnostics themselves have hardware prerequisites.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Build a test inventory for the subsystem you just implemented. Add one boundary test and one case that would fail under a plausible incorrect implementation.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/RegressionTests.cs` with a **public class named `RegressionTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test one small reproducible boundary case for the subsystem you are currently implementing. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~RegressionTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `RegressionTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Tests run without a ROM or desktop unless explicitly integration tests.
- The latest diagnostic run has version and prerequisites recorded.
- Failures report enough state to reproduce.

## Common mistakes

- Counting a no-tests run as a correctness pass.
- Copying implementation logic into the expected calculation.
- Using a game boot to claim full hardware accuracy.

## Further reading

- [mGBA suite](https://github.com/mgba-emu/suite) — focused hardware diagnostics.
- [gba-tests](https://github.com/jsmolka/gba-tests) — additional diagnostic programs.
- [xUnit v2](https://xunit.net/docs/getting-started/v2/getting-started) — framework discovery and parameterization.

## Next chapter

[Debugging and reproducible state](../17-debugging-tools/README.md)
