# One guest timeline


## In the real GBA

The master clock is 16,777,216 Hz. A scanline spans 1,232 cycles and a frame has 228 lines, giving 280,896 cycles per frame (about 59.73 Hz). Display, timers, sound, DMA and CPU activity interact on this shared timeline. The host monitor need not refresh at the same rate.

## In our emulator — version 1

Use a single-threaded deterministic scheduler with an explicit guest cycle counter. At first, complete one instruction, account for a documented approximation of its cycles, then process due hardware events. Preserve all elapsed cycles and handle multiple events when crossing boundaries. A scanline PPU is an acceptable early limitation, recorded as such.

```text
choose next CPU / DMA activity
advance guest time by consumed cycles
process due events in a documented order
reconsider pending IRQs and CPU sleep state
repeat until requested boundary
```

This pseudocode identifies responsibilities, not an implementation. Do not make “render a whole frame” the operation after each CPU instruction. If the CPU is halted, jump to the next relevant hardware event rather than freezing timers/PPU.

## Later — improve timing accuracy

Account for bus wait states, sequential accesses, instruction internal cycles, DMA contention, exact event edges and pipeline refill. Event-boundary stepping can split work that an instruction-boundary model handles late. Register writes near a display/timer boundary are valuable diagnostics. Define ordering for equal-timestamp events and validate it against hardware tests.

Inputs are CPU/DMA elapsed-time requests and scheduled events; outputs are component progression and new requests. The scheduler owns time, while devices own their registers. Desktop sleeps or paces presentation only after guest work is measured; wall time must not alter deterministic test behavior.

## In C#

Use an explicit sufficiently wide counter and predictable loops. A ulong can represent long sessions; conversion between signed/unsigned timestamp differences needs care. Start with a few next-event counters before a generic event framework. Profile Release execution later; unsafe and parallel tasks are unnecessary for this model.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [How C# becomes machine code](../csharp-and-dotnet/runtime.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process): IL, JIT compilation and runtime services.
- [Performance without premature optimization](../csharp-and-dotnet/performance.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/): Profiling CPU use and allocation.
- [Allocations and garbage collection](../csharp-and-dotnet/allocations-and-gc.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Reachability, collection and generations.

## What you should understand now

- [ ] Functional correctness and timing accuracy are distinct milestones.
- [ ] All devices progress when CPU execution is stalled.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Advance display and one timer from a common guest counter. Compare a run in large chunks with the same elapsed time in small chunks, recording any version-1 ordering limitations.

## Definition of done

- A frame has exactly 280,896 guest cycles.
- HALT permits peripheral progress.
- Repeated runs yield the same event log and state.

## Common mistakes

- Using monitor refresh as the GBA clock.
- Dropping remainder cycles at each frame.
- Allowing C# counter wrap or signed conversions to reorder events.

## Further reading

- [GBATEK timing](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — display boundaries and peripheral timing.
- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — instruction cycle timing and memory cycles.

## Next chapter

[Vulkan: presenting the finished framebuffer](../15-vulkan-output/README.md)
