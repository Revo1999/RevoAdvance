# Bitwise operations: a mini-course


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
