# Integer types, binary and hexadecimal

## Before the technical details

You probably used `int` in earlier C# programs. Here the number of bits and whether negatives are allowed matter as much as the numeric value. Binary and hexadecimal are spellings for numbers, not separate numeric types. Start by showing the same value in more than one notation.

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

### One number, several spellings

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int decimalValue = 26;
int hexValue = 0x1A;
int binaryValue = 0b_0001_1010;
Console.WriteLine(decimalValue == hexValue);
Console.WriteLine(hexValue == binaryValue);
Console.WriteLine(decimalValue.ToString("X2"));
```

Expected output:

```text
True
True
1A
```

`0x` starts a hexadecimal literal and `0b` starts a binary literal. Hexadecimal digits A–F stand for ten through fifteen. `1A` means one sixteen plus ten. `ToString("X2")` changes the display, not the stored number. Leading zeroes and separators make bit positions easier to read.

### Try it before implementing

Convert 0x2B into decimal on paper. Then display decimal 43 as hexadecimal. Before narrowing a value to `byte`, ask whether it fits in eight bits and whether your chosen checked/unchecked behavior is deliberate.

Continue with the detailed lesson below after you can explain your prediction.


A bit is a binary digit, 0 or 1. Eight bits make a byte. Unsigned values use all bits for magnitude; signed integers use two's complement. The same bit pattern can mean different numbers depending on its type.

| C# type | Bits | Minimum | Maximum |
| --- | ---: | ---: | ---: |
| `byte` | 8 | 0 | 255 |
| `sbyte` | 8 | -128 | 127 |
| `ushort` | 16 | 0 | 65,535 |
| `short` | 16 | -32,768 | 32,767 |
| `uint` | 32 | 0 | 4,294,967,295 |
| `int` | 32 | -2,147,483,648 | 2,147,483,647 |
| `ulong` | 64 | 0 | 18,446,744,073,709,551,615 |
| `long` | 64 | -9,223,372,036,854,775,808 | 9,223,372,036,854,775,807 |

`0b` introduces binary and `0x` introduces hexadecimal. Hex is base 16: digits 0–9, A–F. One hex digit represents four bits, so two hex digits describe a byte. Underscores only separate digits for readability. `0x2A`, `0b_0010_1010` and decimal `42` are the same number.

```csharp
byte small = 42;
ushort wider = small;       // widening preserves this value
uint bits = 0x8000_0000u;   // u explicitly selects unsigned
int signed = unchecked((int)bits);
```

The last two variables have the same 32-bit pattern. `bits` is 2,147,483,648; `signed` is -2,147,483,648. Comparisons, right shifts and division can therefore differ. `uint` fits a 32-bit register's bit pattern and the address space naturally. Use signed interpretation only where an instruction requires it; do not convert the entire CPU to `int`. Host array lengths and many indexing calculations use `int`; translate only after validating the guest address and region offset.

An explicit cast such as `(byte)number` asks for a conversion. Narrowing can discard upper bits. `checked` requests overflow detection for applicable integral arithmetic/conversions; `unchecked` requests wrapping/truncation. Neither computes emulated CPU flags for you. Compile-time constants and runtime expressions can behave differently if the overflow context is left implicit.

```csharp
int number = 300;
byte wrapped = unchecked((byte)number); // 44: retain eight low bits
// checked((byte)number) would throw OverflowException.
```

Addition on `byte` or `ushort` operands generally promotes them to `int`; the result does not automatically have the original width. C# masks shift counts (five low bits for 32-bit operands), so shifting a `uint` by 32 is not a hardware-style special case. Define guest rules explicitly.

Sign extension preserves a signed value while widening: 8-bit `1111_1110` represents -2; widening signed -2 fills new upper bits with ones. Zero extension instead adds zeros and yields 254. A cast through an unsigned type changes what gets preserved.

```text
zero extend:  11111110 → 00000000 11111110   (254)
sign extend:  11111110 → 11111111 11111110   (-2)
```

Endian order is a different question: it describes how multiple bytes are arranged at consecutive addresses, not whether the integer is signed. Continue with [arrays and spans](arrays-and-spans.md).


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)

## What you should understand now

- [ ] I can explain ranges, literals and signedness in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Integer types, binary and hexadecimal](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types); look specifically for **Ranges, literals and signedness**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

On paper, predict byte → ushort and ushort → uint conversions. Then write your own xUnit cases for 0, the highest unsigned value and a value with its sign bit set. Add exercises for shifting, masking, truncating 0x1234 to eight bits, and sign-extending an 8-bit negative value.

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

- You can explain why 0xFFFFFFFF is either 4,294,967,295 or -1 depending on interpretation.
- Tests distinguish widening, narrowing and sign extension.

## Common mistakes

- Treating `int` and `uint` as interchangeable.
- Expecting a C# overflow exception to implement the ARM V flag.
- Forgetting promotion and shift-count rules.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types) — Ranges, literals and signedness. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
