# Debugging and reproducible state


## Why this exists

An emulator bug is often an incorrect state transition many instructions before the visible symptom. Start with a compact trace and breakpoints; build elaborate UI only after those help solve real failures. Debugging tools observe Core state; they are not emulated hardware registers.

Useful observations include instruction address/bits, ARM/Thumb state, selected registers/CPSR, memory access address/width/value, guest timestamp and peripheral event. A read-only debugger memory view should not accidentally trigger a side-effecting emulated register read. Define “peek for inspection” separately if needed.

```text
known initial state → recorded input/events → first divergent transition
                                                 ↓
                                       smallest regression test
```

## Save states are a later milestone

User-facing Save State/Load State slots and their interaction with cartridge saves are described in [saving and resuming](../12-cartridges-and-roms/saving-and-resuming.md). Normal in-game saving is a required earlier feature; a save state supplements it.

A state must preserve everything needed to reproduce future execution: CPU banks/status, RAM, peripheral registers and hidden latches, timer remainders, DMA active state, audio phase/FIFOs, pending events and cartridge protocol state. ROM identity and a format version protect against restoring into the wrong environment. Store explicit data, not raw object layouts or host pointers. Flush/recreate host output resources separately after restore.

A cartridge save file contains persistent game data; a save state captures a moment of emulation. Neither should serialize Vulkan handles or live .NET references. Test save → run N cycles → restore → run N cycles with identical input and compare resulting state/pixels/samples.

## In C#

Control trace allocations and preserve values, not references to mutable live objects. Start with textual output behind an explicit enable flag. A bounded ring buffer can be added if profiling shows logs are too expensive; it need not be a framework.


## C#/.NET concepts used here

- [Ref and value semantics](../csharp-and-dotnet/ref-and-value-semantics.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters): Pass by value, ref, in and out.
- [Allocations and garbage collection](../csharp-and-dotnet/allocations-and-gc.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Reachability, collection and generations.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] Useful traces capture transitions with guest timestamps.
- [ ] Save-state completeness includes hidden state.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Add a bounded trace of the smallest state transition needed to diagnose your current failure. Later implement versioned save/restore after timing state stabilizes.

## Definition of done

- A trace identifies the first divergence in a failing case.
- Tracing disabled does not change emulated results.
- Later save/restore replay yields identical future state for identical inputs.

## Common mistakes

- Taking shallow copies of arrays for snapshots.
- Serializing native pointers.
- Observing I/O through normal reads that mutate the machine.

## Further reading

- [GBATEK](https://mgba-emu.github.io/gbatek/) — resolve the behavior at the first divergent transition.
- [Microsoft diagnostics](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/) — separate host performance problems from guest correctness.

## Next chapter

[Return to your next milestone](../../ROADMAP.md)
