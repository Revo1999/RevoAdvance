# ARM decoding one family at a time

## Before the technical details

Decoding means recognizing fields in a number. Execution means doing what those fields describe. An opcode identifies an operation; an operand supplies something the operation uses. A mask chooses bit positions. Learn to read an invented label first, then consult the real encoding table rather than guessing its patterns.

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

### Extract a field from an invented label

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
uint label = 0b_1101_0010u;
uint shifted = label >> 4;
uint group = shifted & 0b_11u;
Console.WriteLine(shifted);
Console.WriteLine(group);
```

Expected output:

```text
13
1
```

`0b` introduces binary, underscores improve readability, and `u` means unsigned. `>> 4` moves bits right by four places. `& 0b_11u` retains only the bottom two positions. The intermediate result helps you see why the mask matters. This label is not an ARM instruction.

### Choose a description with a switch

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int category = 2;
string description = category switch
{
    1 => "book",
    2 => "map",
    _ => "unknown"
};
Console.WriteLine(description);
```

Expected output:

```text
map
```

A switch expression chooses a value. Each `=>` separates a matching pattern from its result; `_` is the fallback. The final semicolon completes the assignment. Choosing a description does not execute the described action.

### Try it before implementing

Keep label bits 5–4 the same and change the surrounding bits; the extracted group should stay the same. Then change one selected bit. Make a fixed-bits/variable-bits drawing before attempting a real decoder.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

An ARM instruction is a 32-bit word whose fields describe a conditional operation. Bits 31–28 normally encode a condition evaluated against CPSR. The remaining bits identify a family, operands and modifiers. This page assumes you have completed the [bitwise mini-course](../csharp-and-dotnet/bitwise-operations.md).

```text
31      28 27                                              0
+---------+------------------------------------------------+
|condition| family-dependent fields: opcode, operands, etc. |
+---------+------------------------------------------------+
```

Do not decode solely from one broad high-bit field: multiply and special encodings overlap broad data-processing patterns. For each family, write down fixed bits (mask and expected pattern), variable fields, restrictions, state effects and timing before implementing it.

| Learning order | Focus | Independent verification |
| --- | --- | --- |
| condition evaluation | N/Z/C/V truth tables | both outcomes per condition |
| one register data operation | operands and optional flags | known before/after state |
| more data operations | carry vs signed overflow | boundary operands |
| barrel shifter | shift types, zero/32 edge rules | result plus shifter carry |
| branch / BX | PC and state exchange | target and pipeline convention |
| single transfers | width, alignment, writeback | memory and register effects |
| multiply / block transfers | special matching and sequencing | register lists, corner cases |
| status transfers / SWI | privilege and exception state | mode and return path |

A failed condition suppresses the instruction's architectural effects but does not mean zero elapsed time. Undefined encodings and an implemented-but-not-yet-supported family should be distinguishable in your diagnostics. On ARMv4T the condition 0xF is not a generic modern unconditional extension space.

## In our emulator

Decoding answers what instruction the bits describe; execution applies that meaning to state and the bus. Keep them understandable without constructing an elaborate class hierarchy. Inputs are instruction word and CPU state; outputs include registers, flags, memory effects and time. A decode test should not need a window or complete ROM boot.

## In C#

Use uint, masks and explicit shifts. A small switch is enough when choosing a family. Host arithmetic needs wider intermediates or carefully reasoned formulas for guest flags; normal C# arithmetic does not set CPSR. Write expected flags from arithmetic reasoning, not by duplicating your implementation in tests.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Switch statements and pattern matching](../csharp-and-dotnet/switch-and-pattern-matching.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression): Arms, ordering and exhaustive handling.
- [Enums and named states](../csharp-and-dotnet/enums.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum): Named constants and underlying integral types.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] A mask identifies fixed bits while extraction reads a field.
- [ ] Decoding, condition checking and execution are separate questions.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement condition checking, then one simple ARM data operation without memory effects. Decide its PC/flag contract before coding. Expand only after positive and negative tests pass.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/ArmInstructionTests.cs` with a **public class named `ArmInstructionTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test one implemented operation, condition failure and overlapping decode patterns. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~ArmInstructionTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `ArmInstructionTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- A known instruction transforms a chosen initial state as predicted.
- Failed-condition cases leave the right state untouched while advancing time.
- Decoder tests distinguish an overlapping special encoding.

## Common mistakes

- Building a giant decoder before testing one instruction.
- Using host shifts unchanged for ARM shift-by-32 cases.
- Confusing signed overflow with carry out.

## Further reading

- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — instruction behavior and cycle classes.
- [GBATEK ARM instruction set](https://mgba-emu.github.io/gbatek/#armcpureference) — encoding and edge cases.

## Next chapter

[Thumb: narrower instructions, shared CPU](../05-thumb-instruction-set/README.md)
