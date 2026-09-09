# Performance without premature optimization


The first version should be correct, deterministic and readable. Optimize only after measuring a representative workload in Release with tracing controlled. Startup/JIT compilation can distort a tiny benchmark; compare warmed runs with identical inputs and correctness checks.

| Normal first version | Optimized later, if measurements justify it |
| --- | --- |
| Owned arrays | Span / ReadOnlySpan views to avoid copies |
| Simple concrete classes | Small structs where value semantics fit |
| Value parameters | ref / in when copy cost is demonstrated |
| Reusable managed buffers | Small bounded stackalloc scratch storage |
| Explicit endian conversion | MemoryMarshal only with verified assumptions |
| Safe managed operations | unsafe only for interop or measured bottlenecks |
| Readable methods | Inlining hints only after evidence |

`stackalloc` reserves temporary stack storage for unmanaged elements. For example `Span<int> scratch = stackalloc int[8];` creates bounded scratch space; initialize elements before reading. It is not for large buffers, persistent framebuffers or repeated allocations inside long loops. `readonly` restricts mutation, not object ownership. The JIT can eliminate some bounds checks; unsafe indexing is not your default response to seeing arrays.

Allocations per instruction, GC pressure and oversized state copies are useful suspects. Measure them rather than assume C# is slow. Do not use unsafe code simply because emulator development is low-level.

Read [stackalloc](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc) only when scratch buffers become relevant; use [GC](allocations-and-gc.md), [ref](ref-and-value-semantics.md), and [MemoryMarshal](memorymarshal.md) as later branches.


## Where this meets the GBA

- [Timing](../14-timing-and-scheduling/README.md)
- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain profiling cpu use and allocation in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Performance without premature optimization](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/); look specifically for **Profiling CPU use and allocation**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Record a baseline for one implemented subsystem: elapsed time, workload, configuration and allocated bytes. Change one measured bottleneck and rerun correctness tests before comparing.

## Definition of done

- A proposed optimization has evidence and preserves observable behavior.

## Common mistakes

- Benchmarking Debug and generalizing to Release.
- Using aggressive inlining without measurement.
- Sacrificing guest timing to achieve host frame rate.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/) — Profiling CPU use and allocation. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
