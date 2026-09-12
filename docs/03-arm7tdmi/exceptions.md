# Exception entry and return

## Before the technical details

A guest exception changes where the guest CPU executes and preserves information for its eventual return. Banking means a register name can select different stored values in different modes. Neither is a .NET throw/catch operation. Before reading the entry rules, practice saving values and selecting between separate storage locations.

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

### Store independent notebook positions

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int[] bookmarks = { 8, 21 };
int selectedNotebook = 0;
Console.WriteLine(bookmarks[selectedNotebook]);
selectedNotebook = 1;
Console.WriteLine(bookmarks[selectedNotebook]);
```

Expected output:

```text
8
21
```

Changing the selected index changes which stored value you see; it does not erase the other value. This is an analogy for bank selection, not the GBA register-bank layout.

### A local copy remembers an earlier choice

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
string activity = "reading";
string previous = activity;
activity = "answering the door";
Console.WriteLine(previous);
Console.WriteLine(activity);
```

Expected output:

```text
reading
answering the door
```

Assigning a new string to `activity` leaves `previous` referring to the old string. Strings are immutable; this would not freeze the contents of a shared mutable object. Architectural saved status consists of specified values, not arbitrary object references.

### Try it before implementing

Draw a table with prior state, saved state, new state and return information as separate columns. Fill the real SWI/IRQ rows from the manual below. Leave return-address formulas unimplemented until you can explain them.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

An exception changes control flow through a fixed vector and processor mode. It preserves return information and status in banked state. The architectural vectors are Reset 0x00, Undefined 0x04, SWI 0x08, Prefetch Abort 0x0C, Data Abort 0x10, IRQ 0x18 and FIQ 0x1C. GBA normal operation does not exercise all external exception inputs; use the ARM manual to understand architecture and GBATEK for what the GBA exposes.

| Entry | Destination mode | Status/return concern |
| --- | --- | --- |
| SWI | Supervisor | saved CPSR and banked LR; return after request |
| Undefined | Undefined | saved state and appropriate next instruction |
| IRQ | IRQ | return offset reflects interrupt/pipeline convention |

Do not use one guessed LR formula for every exception. ARM versus Thumb entry and exception type affect return calculations. Exceptions enter ARM state; exception return must restore saved status using the architectural instruction behavior, not just branch to LR. Reset has its own initialization contract.

## In our emulator

Inputs are an exception cause, execution state and masks. Outputs include bank selection, saved status, LR, PC/vector and refill timing. CPU state owns these changes; a host-language throw is unrelated. Test the transition without a BIOS handler first, then integrate a handler through real guest execution. IRQ pending bits remain the interrupt controller's responsibility.

## In C#

Enums can name exception causes; explicit state transitions are clearer than indirect callbacks. Tests should compare saved values, active bank and current status separately.


## C#/.NET concepts used here

- [Enums and named states](../csharp-and-dotnet/enums.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum): Named constants and underlying integral types.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Host exceptions and guest exceptions](../csharp-and-dotnet/exceptions.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/): Throw, try, catch and finally.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Write an entry/return state table for SWI and IRQ in ARM and Thumb, consulting the manual for return offsets. Implement one pair yourself after bank-switch tests pass.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/CpuExceptionTests.cs` with a **public class named `CpuExceptionTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test saved status, bank selection and one implemented entry/return pair. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~CpuExceptionTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `CpuExceptionTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Tests verify saved CPSR, active mode, LR, T/I bits and returned state.

## Common mistakes

- Treating LR as a universal current-PC value.
- Returning without restoring CPSR.
- Using a shallow CPU copy as saved architectural state.

## Further reading

[ARM programmer model](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — exception entry/return details. [GBATEK](https://mgba-emu.github.io/gbatek/#armcpureference) — GBA CPU behavior.

## Next chapter

[Continue](../04-arm-instruction-set/README.md).
