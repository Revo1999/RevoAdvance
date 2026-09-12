# Thumb: narrower instructions, shared CPU

## Before the technical details

Thumb is another encoding understood by the same CPU. A smaller command does not imply smaller working registers. Think of an abbreviated written instruction that still refers to the same notebook. The new C# issue is separating the width used to store a value from the width used while calculating with it.

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

### Widen without changing the value

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
ushort compact = 500;
uint working = compact;
working += 20u;
Console.WriteLine(compact);
Console.WriteLine(working);
```

Expected output:

```text
500
520
```

`ushort` stores 16 bits and `uint` stores 32. Widening preserves the unsigned value. `+=` adds and assigns. The two variables remain separate values; changing the wider one does not change the original.

### Notice arithmetic promotion

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
ushort small = 12;
var result = small + 1;
Console.WriteLine(result);
Console.WriteLine(result.GetType().Name);
```

Expected output:

```text
13
Int32
```

`var` asks the compiler to infer a static type; it does not mean “any type.” This addition uses `int`, shown as `Int32`. The declared storage width of an operand does not automatically determine the result type.

### Try it before implementing

Predict the result type of adding two `ushort` values. Draw a 16-bit command beside a 32-bit working value, and explain why truncating an ARM decoding mask cannot teach you the Thumb encoding.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

Thumb packs common operations into 16-bit encodings, improving code density and often cartridge fetch efficiency. Registers remain 32 bits. Many encodings mainly address R0–R7; high-register operations and SP/PC forms have their own rules.

```text
ARM    address A: [             32-bit instruction              ]
Thumb  address A: [ 16-bit instruction ] [ next 16-bit instruction ]
data registers:  [                 32 bits                       ]
```

ARMv4T Thumb has arithmetic, loads/stores, conditional/unconditional branches, stack-oriented transfers and state exchange. The long branch-with-link sequence uses two halfwords with related effects; it is not Thumb-2. PC-relative forms may align a visible PC value. BX uses the target's low bit to select instruction state while alignment determines the actual fetch address.

## In our emulator

Reuse the same CPU registers, bus and flags; add a separate understandable decoding path. Inputs are halfword instruction bits and current state. Outputs are architectural effects and cycles. Share helper behavior only when the architectural semantics really match: flag updates and operand encodings can differ from ARM.

## In C#

Fetch a 16-bit encoding but deliberately choose a width for promoted bitwise calculations. Masks must describe Thumb fields, not truncated ARM fields. Tests should use independent small instruction examples before a mixed-state ROM.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Switch statements and pattern matching](../csharp-and-dotnet/switch-and-pattern-matching.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression): Arms, ordering and exhaustive handling.

## What you should understand now

- [ ] Instruction width differs from register width.
- [ ] State exchange affects fetch and pipeline behavior.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement one Thumb arithmetic family, then a controlled ARM ↔ Thumb exchange test. Leave the rest of the instruction table as a learning checklist you expand.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/ThumbInstructionTests.cs` with a **public class named `ThumbInstructionTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test one implemented Thumb family and shared CPU state. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~ThumbInstructionTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `ThumbInstructionTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Shared registers survive state exchange.
- PC-relative tests use documented alignment.
- A two-halfword BL case preserves correct link behavior.

## Common mistakes

- Treating Thumb registers as 16 bits.
- Adding Thumb-2 instructions.
- Assuming identical flag rules for superficially similar ARM operations.

## Further reading

- [GBATEK Thumb instruction set](https://mgba-emu.github.io/gbatek/#armcpureference) — encoding and PC rules.
- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — Thumb execution and interworking.

## Next chapter

[The bus: behavior beyond storage](../06-bus-and-memory/README.md)
