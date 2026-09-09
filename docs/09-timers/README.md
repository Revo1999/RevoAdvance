# Timers: counters driven by guest time


## In the real GBA

Four 16-bit timers count prescaled system clocks or, for timers 1–3, overflows from the preceding timer. The clock divisors are 1, 64, 256 and 1024. Each timer has a reload value and control bits; overflow reloads the counter and can request an interrupt. Timer-driven Direct Sound consumes samples independently of the desktop audio callback.

Registers occupy 0x04000100–0x0400010E: each timer has a low counter/reload halfword and a control halfword. Reading the low register returns the live count; writing supplies a reload value. Enable transitions and timing of writes need explicit behavior.

```text
system cycles → prescaler → timer 0 overflow → timer 1 (cascade)
                                                  ↓ overflow
                                            timer 2 → timer 3
```

## In our emulator

Track live counters, reload values, enable/cascade state and fractional prescaler progress. Inputs are elapsed guest cycles and writes; outputs are counters and overflow events consumed by IRQ/audio/other timers. Advancing by a large batch may overflow more than once. Preserve leftover cycles and event ordering.

## In C#

ushort expresses stored counter width; a wider temporary helps reason about multiple elapsed ticks. Host arithmetic promotion and casts should not silently decide reload semantics. State-owning classes or carefully mutated structs both work if ownership is clear.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Properties and fields](../csharp-and-dotnet/properties-and-fields.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties): Accessors and encapsulation.
- [Ref and value semantics](../csharp-and-dotnet/ref-and-value-semantics.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters): Pass by value, ref, in and out.

## What you should understand now

- [ ] Reload state differs from the live counter.
- [ ] A guest clock is independent of host elapsed milliseconds.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement one timer with a prescaler and reload, then cascade a second. Test batch advancement against repeated small advances.

## Definition of done

- Divisor boundaries keep remainders.
- Overflow reload and IRQ occur at predicted guest times.
- Two timers cascade without using host wall time.

## Common mistakes

- Using System.Timers.Timer to emulate hardware ticks.
- Losing overflow events in a large cycle batch.
- Mutating a copied struct and discarding the result.

## Further reading

- [GBATEK timers](https://mgba-emu.github.io/gbatek/#gbatimers) — reload, cascade and control bits.
- [Tonc timers](https://gbadev.net/tonc/timers.html) — prescaling and overflow reasoning.

## Next chapter

[DMA: timed transfers with bus ownership](../10-dma/README.md)
