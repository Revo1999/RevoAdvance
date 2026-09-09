# Exception entry and return


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
