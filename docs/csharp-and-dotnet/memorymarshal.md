# MemoryMarshal: optional advanced views


MemoryMarshal exposes low-level operations on managed memory views. It can reinterpret bytes as another value type without per-element conversion. That power removes assumptions you would otherwise state explicitly.

```csharp
byte[] raw = new byte[4];
Span<ushort> words = System.Runtime.InteropServices.MemoryMarshal.Cast<byte, ushort>(raw.AsSpan());
```

This produces a view over the same storage. It does not decode little endian independently of the host, validate a GBA region, or implement hardware access widths. Length, alignment/platform assumptions and types containing managed references matter. For guest integers, begin with explicit endian operations from [arrays and spans](arrays-and-spans.md).


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain casts, layout and reference restrictions in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: MemoryMarshal: optional advanced views](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.memorymarshal); look specifically for **Casts, layout and reference restrictions**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Describe when reinterpretation and numeric conversion give different answers. Keep MemoryMarshal out of the first memory implementation.

## Definition of done

- You can state byte-order and lifetime assumptions for a reinterpretation.

## Common mistakes

- Treating a cast view as endian conversion.
- Using raw struct layout as a durable save-state format.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.memorymarshal) — Casts, layout and reference restrictions. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
