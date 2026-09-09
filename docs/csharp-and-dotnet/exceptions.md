# Host exceptions and guest exceptions


A .NET exception interrupts normal host control flow. `throw` raises it; `try` encloses an operation; `catch` handles selected failures; `finally` runs cleanup when leaving the block. A missing ROM file is a host failure. A guest SWI or IRQ is modeled CPU state and control flow, not a .NET exception.

```csharp
if (count < 0)
{
    throw new ArgumentOutOfRangeException(nameof(count));
}
```

This generic snippet assumes an integer `count` parameter. `nameof(count)` produces the text "count" while staying tied to the symbol. Fail clearly for developer mistakes. Define deliberate development behavior for unimplemented guest operations; do not silently catch everything and continue with fabricated data.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Cartridges](../12-cartridges-and-roms/README.md)

## What you should understand now

- [ ] I can explain throw, try, catch and finally in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Host exceptions and guest exceptions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/); look specifically for **Throw, try, catch and finally**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

List three host failures and three guest events, deciding which should use .NET exceptions.

## Definition of done

- Invalid host input and emulated exception entry have separate handling.

## Common mistakes

- Implementing IRQ delivery with throw/catch.
- Swallowing an array bounds exception as a memory-bus policy.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/) — Throw, try, catch and finally. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
