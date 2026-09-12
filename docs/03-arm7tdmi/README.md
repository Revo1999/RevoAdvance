# ARM7TDMI before opcodes

## Before the technical details

The CPU is the worker that repeatedly reads a command and changes state. Its registers are small, fast scratch locations. An instruction encoding is a pattern of bits that describes a command; a CPU mode controls which architectural state is visible. These terms do not refer to C# methods or .NET execution modes. Before decoding anything, practice naming and remembering state.

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

### Give a choice a name

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Activity current = Activity.Reading;
Console.WriteLine(current);
Console.WriteLine((int)current);

enum Activity
{
    Resting = 0,
    Reading = 1
}
```

Expected output:

```text
Reading
1
```

An `enum` supplies names for numeric values. `(int)` is an explicit conversion to show the underlying number. Names improve clarity, but you must still choose values from the hardware specification when you later describe real modes.

### Preserve a value before changing it

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int currentPage = 12;
int bookmark = currentPage;
currentPage = 30;
Console.WriteLine(bookmark);
Console.WriteLine(currentPage);
```

Expected output:

```text
12
30
```

The bookmark is a value captured at a moment in time. Saving architectural status likewise requires knowing exactly which values are preserved. This example has no CPU entry or return behavior.

### Try it before implementing

Write a glossary for register, instruction, mode, ARM/Thumb state and program counter. Read the detailed section to distinguish them. Sketch stored values before and after switching away from a notebook; do not implement an instruction yet.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

The CPU reads instructions and transforms register/memory state. It implements ARMv4T, with 32-bit ARM encodings and 16-bit Thumb encodings. Thumb is a second instruction encoding state, not a second processor or a CPU privilege mode. Do not import Thumb-2 or newer ARM instructions.

At any instant software sees R0–R15 and CPSR. R0–R12 are ordinary working registers; R13 is conventionally SP (stack pointer), R14 LR (link/return address), R15 PC (program counter) with special behavior. “16 general registers” includes these special uses; PC is not just another array slot.

![Visible registers](../assets/registers.svg)

| Processor mode | Value | Banked state |
| --- | --- | --- |
| User | 0x10 | ordinary R0–R14; no SPSR |
| FIQ | 0x11 | R8–R14 and SPSR |
| IRQ | 0x12 | R13–R14 and SPSR |
| Supervisor | 0x13 | R13–R14 and SPSR |
| Abort | 0x17 | R13–R14 and SPSR |
| Undefined | 0x1B | R13–R14 and SPSR |
| System | 0x1F | shares User register bank; privileged, no SPSR |

Banking means switching which physical register storage a name refers to; it is not clearing registers. The architecture defines modes even when the GBA does not normally drive every corresponding external exception source.

```text
CPSR bit   31 30 29 28   27........8   7   6   5   4.....0
           N  Z  C  V     reserved    I   F   T     mode
           sign/zero/carry/overflow   IRQ FIQ Thumb
                                      masks
```

CPSR is current status. An exception mode's SPSR stores saved status for return. N is the result's sign bit; Z indicates zero; C records carry (subtraction uses no-borrow interpretation); V records signed overflow. These are not interchangeable. T selects Thumb; I/F mask exception acceptance. Preserve reserved bits as required by the architectural rules rather than inventing meanings.

The conceptual pipeline is fetch → decode → execute, with overlapping work. Reading PC usually observes current instruction address +8 in ARM or +4 in Thumb; operand role and instruction family introduce details, including alignment and stored-PC cases. A branch or state change refills the pipeline. Model the architectural visible PC separately from your internal fetch position instead of sprinkling increments everywhere.

```text
time →     slot 1     slot 2     slot 3     slot 4
instr A    fetch      decode    execute
instr B              fetch     decode     execute
instr C                        fetch      decode
```

## In our emulator

State includes visible/banked registers, CPSR/SPSRs, current instruction state, and a documented pipeline/fetch convention. CPU inputs are instruction bits, bus results and pending exception signals; outputs are state changes, accesses and consumed time. Memory byte order on the GBA is little endian. Word/halfword alignment rules belong to specific access instructions and the bus, not a blanket host alignment assumption.

Exception entry preserves return information and status, chooses a mode/vector, masks as specified and refills execution. SWI and undefined instructions are CPU exceptions too; peripheral IRQ delivery is only one case. See [exceptions and banking](exceptions.md) before implementing return paths.

## In C#

A concrete state class avoids accidental copies of mutable CPU state. Arrays may represent banks, but names and ownership must stay clear. `uint` preserves bit patterns; enums name modes; explicit operations clarify mode changes. Design on paper before writing handlers.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Enums and named states](../csharp-and-dotnet/enums.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum): Named constants and underlying integral types.
- [Properties and fields](../csharp-and-dotnet/properties-and-fields.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties): Accessors and encapsulation.

## What you should understand now

- [ ] Registers, modes and ARM/Thumb state are different concepts.
- [ ] CPSR and SPSR have different ownership.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Represent CPU state and test mode switching independently of instruction execution. Document what your stored PC means. Then follow the first ARM instruction milestone.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/CpuStateTests.cs` with a **public class named `CpuStateTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test bank preservation, mode switching and your documented PC convention. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~CpuStateTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `CpuStateTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Switching away from and back to a bank preserves its values.
- User/System share the intended bank.
- Tests distinguish C and V and verify CPSR field extraction.

## Common mistakes

- Copying a struct and changing only the copy.
- Giving User mode an SPSR.
- Incrementing PC both in fetch and in handlers.

## Further reading

- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — programmer model, pipeline and cycle timing; distinguish core revision details.
- [GBATEK CPU reference](https://mgba-emu.github.io/gbatek/#armcpureference) — ARMv4T instruction and GBA-specific behavior.

## Next chapter

[ARM decoding one family at a time](../04-arm-instruction-set/README.md)
