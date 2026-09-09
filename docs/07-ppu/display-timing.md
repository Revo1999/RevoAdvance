# Scanlines, HBlank and VBlank


## In the real GBA

The display traverses lines 0–227. Lines 0–159 contain the visible image; lines 160–227 are the nonvisible vertical interval. Each line totals 1,232 master cycles: a nominal 960-cycle drawing interval and 272-cycle HBlank interval. The simple 240 × 4 calculation helps understand the nominal drawing budget, not every internal access edge.

![Nominal display timeline](../assets/scanline.svg)

DISPSTAT exposes display status and interrupt enables/compare; VCOUNT gives the current line. VBlank's status flag is cleared on line 227, even though that line is still nonvisible. Do not equate “not a visible line” with every hardware flag being set. Exact flag edges, memory access availability and DMA trigger eligibility are separate rules to verify in hardware references/tests.

## In our emulator

Track line number and position in guest cycles. Inputs are elapsed time and register writes; outputs are line/frame boundaries, status transitions, VCOUNT comparison events and requests for DMA/IRQ. Preserve overshoot when a time batch crosses multiple boundaries. A VBlank event occurs at entry, not once per host update while the flag is set.

GBATEK distinguishes the nominal drawing budget from DISPSTAT: the HBlank flag stays clear for 1,006 cycles, not just the 960 drawing cycles. Do not drive all status and trigger events from the simplified diagram without checking their specific edge rules.

First render a scanline from a defined snapshot. Later refine mid-line writes and precise event ordering. This preserves a understandable first implementation while naming exactly where accuracy is missing.

## In C#

Use integer cycle counters, not floating-point accumulation or Thread.Sleep. A host sleep controls presentation pacing only. Boundary tests should compare one cycle before, at and after a selected transition.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Model line/frame counters and verify nominal boundaries before connecting IRQ/DMA. Add a separate test for line 227 status behavior.

## Definition of done

- 228 lines consume 280,896 cycles.
- Time batches retain remainder cycles.
- Entry events occur once and VCOUNT wraps correctly.

## Common mistakes

- Treating VBlank as 68 identical flag states.
- Dropping elapsed cycles at a boundary.
- Using host frame time as guest timing.

## Further reading

[GBATEK display status](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — DISPSTAT/VCOUNT edge details. [Tonc video](https://gbadev.net/tonc/video.html) — blanking orientation.

## Next chapter

[Continue](vram.md).
