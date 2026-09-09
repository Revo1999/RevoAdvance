# ARM decoding one family at a time


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
