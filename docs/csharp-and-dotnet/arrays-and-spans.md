# Arrays, spans and byte order


An array has a fixed length and numbered elements starting at zero. `new byte[1024]` creates 1,024 zero-initialized bytes; valid indexes are 0 through 1,023. Arrays are reference types even when their elements are value types.

```csharp
byte[] data = new byte[1024];
data[3] = 42;
Span<byte> window = data.AsSpan(2, 4);
window[1] = 7; // modifies data[3]; no new backing array
```

`Span<T>` is a temporary bounded view of contiguous elements of type `T`. The angle brackets supply a type argument. `ReadOnlySpan<T>` prevents writing through that view, but another owner can still change the underlying array. Neither owns the storage. A span cannot be stored as an ordinary class field or retained freely across asynchronous suspension. `Memory<T>` can be retained in such contexts; lifetime and ownership remain your responsibility.

Ranges use an exclusive end: `data[2..6]` on an **array copies** four elements into a new array; `data.AsSpan()[2..6]` slices a span without copying. Prefer explicit `AsSpan(start, length)` until this distinction is comfortable.

```text
offset       0      1
byte        0x34   0x12
little-endian 16-bit interpretation: 0x1234
```

Use explicit little-endian conversion at the guest memory boundary. [BinaryPrimitives](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.binary.binaryprimitives) provides named endian operations; read the little-endian methods after understanding the two-byte example. Host-native reinterpretation is not an endian contract.

A framebuffer can be a one-dimensional array even though you reason in rows and columns. Work out row stride and the last valid position on paper. A guest address is not an array index: first resolve the region, then calculate its offset, then enforce that access's rules.

Advanced later: [Span<T>](https://learn.microsoft.com/en-us/dotnet/api/system.span-1) explains restrictions and slicing; [Memory<T>](https://learn.microsoft.com/en-us/dotnet/api/system.memory-1) explains a storable memory view. Ordinary arrays are enough for the first exercise.


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [PPU](../07-ppu/README.md)
- [Audio](../13-audio/README.md)

## What you should understand now

- [ ] I can explain zero-based indexing and array reference semantics in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Arrays, spans and byte order](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays); look specifically for **Zero-based indexing and array reference semantics**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Create a tiny generic byte array. Verify first/last indexes, aliasing through a span and a two-byte little-endian interpretation in tests. Leave GBA address routing for the memory milestone.

## Definition of done

- You distinguish copying an array slice from sharing a span.
- Byte order can be demonstrated with two unequal bytes.

## Common mistakes

- Indexing an array with 0x06000000.
- Keeping a span after its storage lifetime ends.
- Assuming every range operation is allocation-free.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays) — Zero-based indexing and array reference semantics. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
