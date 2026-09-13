# Start here: one small experiment

**The simpler starting path is now [one GBA memory lesson](../../START-HERE.md).** It includes the required C# and ready-made checks. This older page is optional practice.

**Easy run controls:** use `.\dev.cmd lab` for this page's console examples and `.\dev.cmd test` for your emulator tests. `.\dev.cmd watch` reruns tests on save. These commands replace the terminal setup and long project commands below; follow the [everyday workflow](daily-workflow.md) and focus on the C# exercises.

## Before the technical details

Begin with [Before you code](before-you-code.md) for setup, the stack explained in plain language, and a separate practice project. A test is just code that compares what happened with what you expected. You can learn that skill before you know anything about the GBA. Start with ordinary integers, then investigate their individual bits.

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

### Call a method and keep its result

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int AddTickets(int current, int extra)
{
    return current + extra;
}

int result = AddTickets(3, 2);
Console.WriteLine(result);
```

Expected output:

```text
5
```

`int` before the method name is its return type. The two parameters are names for the inputs while the method runs. `return` sends one value back to the caller. Declaring a method does not call it; `AddTickets(3, 2)` does.

### Ask a true-or-false question

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int actual = 3 + 2;
bool matches = actual == 5;
Console.WriteLine(matches);
```

Expected output:

```text
True
```

`bool` holds `true` or `false`. `==` compares values; `=` stores a value. Printing `True` is a useful experiment, but an xUnit assertion will make a mismatch count as a failed test.

### Try it before implementing

Change the method inputs and update your prediction. Then deliberately compare against the wrong number. Read the testing refresher before writing the low-byte test below; its body is still yours to write.

Continue with the detailed lesson below after you can explain your prediction.


You will write this emulator yourself. This repository gives you a reading path, empty source locations and criteria for testing each step. No ROM, BIOS, memory bus, CPU interpreter or renderer is included.

## Your first session

1. Read this page, then [integer types](../csharp-and-dotnet/integer-types.md) and [bitwise operations](../csharp-and-dotnet/bitwise-operations.md).
2. Read the short [testing refresher](../csharp-and-dotnet/testing.md).
3. Run the scaffold commands below.
4. Write one test file yourself in `tests/Gba.Core.Tests`: extract the low byte of a generic `uint`, keeping the result as `uint`. Choose zero, an all-low-bits-set value, a value with only bit 8 set, and a mixed hexadecimal value. Predict each result on paper. The refresher teaches the operator; this page deliberately leaves the test and expression to you.
5. Update [your progress log](../../progress/README.md). Then move to the system overview.

## Tools and first build

Use a stable .NET 10 SDK, a text editor or IDE, and Git when you want version history. The scaffold targets `net10.0`. The [project guide](../csharp-and-dotnet/project-structure.md) explains every project setting.

```text
dotnet --info
dotnet restore GbaEmulator.sln
dotnet build GbaEmulator.sln
dotnet run --project src/Gba.Desktop
dotnet test GbaEmulator.sln
```

Run in the repository root. Restore needs access to NuGet the first time. Desktop prints a learning-scaffold message and exits; it does not open a window. Tests initially contain no methods, so a no-tests result is expected. Your first exercise is what turns discovery into an actual pass/fail check.

## Read in small loops

```text
hardware concept → relevant C# tool → your implementation
       ↑                                  ↓
next question ← progress log ← tests and observed behavior
```

Use [ROADMAP](../../ROADMAP.md) for implementation order. Folder numbers organize subjects; they do not mean you must finish all CPU instructions before drawing a pixel. When stuck, reduce the example until you can predict its result without a running emulator.


## C#/.NET concepts used here

- [Projects, assemblies and the .NET CLI](../csharp-and-dotnet/project-structure.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/tools/): Build, run, test and project references.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] Where your first test belongs.
- [ ] How the learning loop works.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Write the low-byte exercise described above. Do not begin a memory bus yet.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/LowByteTests.cs` with a **public class named `LowByteTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test the low-byte exercise; use the generic xUnit example as a syntax guide, but calculate and write your own cases. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~LowByteTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `LowByteTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Your own cases are discovered by dotnet test.
- A deliberately wrong expectation fails; restoring the right one passes.
- Your progress log names the next question.

## Common mistakes

- Copying a completed emulator instead of practicing the concept.
- Reading every advanced page before writing the first test.

## Further reading

- [Tonc numbers](https://gbadev.net/tonc/numbers.html) — use binary and hexadecimal explanations; C examples are not C#.
- [Microsoft CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/) — look up build/run/test command arguments.

## Next chapter

[The GBA as an interconnected machine](../01-system-overview/README.md)
