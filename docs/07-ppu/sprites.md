# Objects and OAM


## In the real GBA

Sprites are movable objects whose attributes reside in OAM. There are 128 entries, each spanning eight bytes. Three halfwords contain object attributes; the fourth participates in the interleaved affine-parameter layout rather than being a general fourth attribute. Shape and size together choose dimensions; affine and regular objects interpret some bits differently.

```text
one OAM entry (8 bytes)
+-------------+-------------+-------------+------------------+
| attr0       | attr1       | attr2       | affine parameter |
| Y, modes... | X, size...  | tile/prio...| interleaved      |
+-------------+-------------+-------------+------------------+
          ↓ tile data in VRAM + OBJ palette
       candidate pixel at current scanline X
```

Coordinates wrap within their encoded widths; an object can straddle the screen edge. DISPCNT selects 1D/2D object tile mapping. Objects have priority, colour-depth, mosaic and window/semitransparent modes. Affine objects select matrices distributed across OAM entries, with optional doubled bounding boxes; doubling bounds does not double the source texture.

## In our emulator

Inputs are OAM, OBJ VRAM, OBJ palette, display mode and scanline. Output is object candidates, including transparency and priority metadata. Begin with one regular object, then overlap, flips, wrapping and mapping modes. Hardware has per-line processing limits; unlimited objects per scanline is an early approximation to record, not the final specification.

## In C#

Decode fields into small values for reasoning. Do not reinterpret an arbitrary C# struct as eight hardware bytes without explicit layout/endian reasoning. OAM byte-write rules remain the bus's responsibility.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Render one asymmetric regular object, then two overlapping objects with equal and unequal priorities. Add edge wrapping before affine objects.

## Definition of done

- Position, shape/size and tile selection match a known fixture.
- Transparent pixels reveal the lower layer.
- Overlap tie behavior is verified against the reference.

## Common mistakes

- Treating the fourth halfword as unused padding.
- Decoding affine and normal bits identically.
- Assuming a copied struct containing array references is independent.

## Further reading

[Tonc regular sprites](https://gbadev.net/tonc/regobj.html) — object representation. [GBATEK OBJ](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — OAM modes, priorities and limits.

## Next chapter

[Continue](composition.md).
