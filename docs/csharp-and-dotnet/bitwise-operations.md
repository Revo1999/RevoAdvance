# Bitwise operations: a mini-course

## Before the technical details

Ordinary arithmetic treats a number as a whole. Bitwise operators let you ask about selected positions in its binary representation. Number positions from zero at the right; bit three has value eight. Work in four positions on paper first, then remember that a `uint` actually has 32 bits.

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

### Trace AND, OR and XOR separately

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
uint a = 0b_1010u;
uint b = 0b_0110u;
Console.WriteLine(a & b);
Console.WriteLine(a | b);
Console.WriteLine(a ^ b);
```

Expected output:

```text
2
14
12
```

Write the operands above each other. AND keeps positions with two ones: `0010`. OR keeps positions with at least one one: `1110`. XOR keeps positions that differ: `1100`. Output is decimal because plain `WriteLine` does not display the source binary spelling. [Microsoft’s operator reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators) gives the precise integer-width rules.

### Try it before implementing

Predict all three results when both inputs are `0b_1010u`. Explain why OR and XOR then differ. Continue into shifts below only after you can explain each column without running code.

Continue with the detailed lesson below after you can explain your prediction.


Start with [integer types](integer-types.md). Bitwise operations work on individual bits. Logical `&&` and `||` work on Boolean conditions and are different tools.

```text
a        10110110
b        00001111
a & b    00000110   AND: retain bits set in both
a | b    10111111   OR: set bits present in either
a ^ b    10111001   XOR: set bits that differ
~a       01001001   complement shown in EIGHT bits only
a << 1   01101100   eight-bit illustration: left shifts lose high bits
a >> 1   01011011   unsigned illustration: zero enters from the left
```

In real C#, `~` on a `byte` promotes to `int`, producing a 32-bit result; mask or deliberately narrow if your exercise requires eight bits. The illustrations specify width so discarded bits are visible.

```csharp
uint value = 0b_1011_0110;
uint lowerNibble = value & 0x0F;
uint setBit = value | (1u << 3);
uint clearedBit = value & ~(1u << 2);
uint toggledBit = value ^ (1u << 4);
```

`0x0F` is `00001111`: AND keeps only the lowest four bits (a nibble). `value & 0xFF` retains eight low bits but **does not change the C# result type to byte**. Parentheses make evaluation order clear.

```text
ARM word: 31       28 27                                      0
          +---------+-----------------------------------------+
          |  COND   |             remaining bits              |
          +---------+-----------------------------------------+
>> 28:    00000000 00000000 00000000 0000CCCC
& 0xF:    00000000 00000000 00000000 0000CCCC
```

For a `uint instruction`, `instruction >> 28` moves bits 31–28 to bits 3–0. `(instruction >> 28) & 0xF` explicitly states the desired width; the mask is redundant for this particular unsigned top field but useful for reading the intent. This extracts a field, not an entire decoder.

```text
address = 0x06001234 = 00000110 00000000 00010010 00110100
address >> 24       = 00000000 00000000 00000000 00000110
```

This reveals the upper address byte, a first clue to a memory region. It does not resolve mirroring, access permissions or every I/O register. For `int`, `>>` preserves the sign bit; for `uint`, it inserts zeros. Do not use host shift behavior as a substitute for ARM's special shifts by zero, 32 and larger counts.

Learn in this order: trace AND → set/clear/toggle → shifts → extract a field → combine non-overlapping fields. Check your predicted bit strings after each step.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)

## What you should understand now

- [ ] I can explain and, or, xor, complement and shift behavior in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Bitwise operations: a mini-course](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators); look specifically for **AND, OR, XOR, complement and shift behavior**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Write a parameterized test that extracts the low byte from several unsigned values. Then extract a three-bit field from a generic status number. Choose inputs where surrounding bits are all ones, so an incorrect mask becomes visible.

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

- Every operator in the visual table can be explained without running code.
- A field extraction test catches missing masks and wrong shift offsets.

## Common mistakes

- Confusing XOR with OR.
- Applying a signed right shift unintentionally.
- Thinking an address prefix is a complete memory-map implementation.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators) — AND, OR, XOR, complement and shift behavior. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
