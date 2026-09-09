# Integer types, binary and hexadecimal


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
