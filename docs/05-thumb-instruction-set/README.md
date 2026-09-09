# Thumb: narrower instructions, shared CPU


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
