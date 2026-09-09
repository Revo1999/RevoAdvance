# Allocations and garbage collection


The garbage collector reclaims managed objects that are no longer reachable. Allocation is often cheap, but allocating temporary objects repeatedly adds collection work and can disturb steady audio or frame delivery.

```csharp
byte[] buffer = new byte[256]; // allocate once, then reuse deliberately
```

Do not create a new framebuffer or formatted trace string for every pixel or instruction. Start with clear ownership and reuse stable buffers. A reused buffer can still be wrong if the host reads it while the core overwrites it; allocation reduction does not solve synchronization.

```text
managed: reference → GC-tracked object → collected after unreachable
native:  handle    → driver resource   → explicit API destruction
```

GC manages memory, not the completion of GPU commands. A managed wrapper becoming unreachable does not guarantee prompt native resource release. See [native interop](native-interop.md).


## Where this meets the GBA

- [Timing](../14-timing-and-scheduling/README.md)
- [Audio](../13-audio/README.md)

## What you should understand now

- [ ] I can explain reachability, collection and generations in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Allocations and garbage collection](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals); look specifically for **Reachability, collection and generations**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Identify which operations in a toy loop allocate. Compare the total allocations of allocating a buffer each iteration versus reusing one, without changing outputs.

## Definition of done

- You can explain an allocation rate and a buffer owner.

## Common mistakes

- Calling GC.Collect every frame.
- Assuming native resources disappear promptly with managed wrappers.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals) — Reachability, collection and generations. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
