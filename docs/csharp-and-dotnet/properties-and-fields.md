# Properties and fields


A field stores data. A property exposes access through `get` and/or `set`; access can execute code. An auto-property has compiler-generated storage.

```csharp
class Counter
{
    private int count;
    public int Count { get { return count; } }
}
```

The compact equivalent getter is `public int Count => count;`. Here `=>` means an expression-bodied member returning that expression. In a lambda it separates arguments from the function body; context matters. Prefer the longer form until both are readable.

`public` exposes a member to other projects. `internal` limits it to this assembly, and `private` to its containing type. An I/O register is not necessarily a simple settable property: reads can expose current counters, and writes can acknowledge flags or latch a reload value. Keep side-effecting bus operations explicit when that makes intent clearer.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Timers](../09-timers/README.md)

## What you should understand now

- [ ] I can explain accessors and encapsulation in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Properties and fields](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties); look specifically for **Accessors and encapsulation**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Create a toy object with a field and a read-only public property. Explain which caller can modify state and how this would differ from a write-one-to-clear hardware register.

## Definition of done

- You distinguish storage from the operation exposed to callers.

## Common mistakes

- Assuming every I/O write is assignment.
- Hiding surprising hardware side effects behind ordinary-looking getters.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties) — Accessors and encapsulation. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
