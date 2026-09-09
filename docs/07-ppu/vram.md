# VRAM is a mode-dependent workspace


## In the real GBA

VRAM has 96 KiB of physical storage. Its layout changes with video mode. In tiled modes, the first 64 KiB serves backgrounds and the final 32 KiB serves objects. In bitmap modes, bitmap pages occupy background storage and object tile data is restricted to the final 16 KiB starting at 0x06014000.

```text
Tiled:   06000000 [ BG tiles / maps: 64 KiB ] 06010000 [ OBJ:32 KiB ] 06018000
Bitmap:  06000000 [ bitmap area:    80 KiB ] 06014000 [ OBJ:16 KiB ] 06018000
```

Tiled backgrounds choose character blocks (tile data) and screen blocks (maps) through BGCNT. These are interpretations of the same storage, so careless placement can overlap them. Palette RAM is separate: 512 bytes for BG palettes and 512 bytes for OBJ palettes. OAM is also separate.

Address mirroring is not a simple modulo-96-KiB rule. The upper part of the 128-KiB VRAM window aliases part of the physical storage. Byte-write behavior also depends on whether the destination lies in the current mode's BG/OBJ area. Read the bus rules before implementing writes.

## In our emulator

Maintain one physical VRAM backing store and interpret it through display state. Inputs are bus accesses and mode configuration; output is the data sampled by BG/OBJ rendering. Do not move bytes when changing modes. Display-time access restrictions and exact mid-frame changes can be later refinements with documented limits.

## In C#

Bounded spans can describe views into an array without copying. A view does not enforce hardware layout or prevent overlap; your configuration decoding does that.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Draw memory placement for one BG tile set and one map without overlap. Implement the relevant addressing yourself, then test one documented VRAM mirror.

## Definition of done

- Changing mode changes interpretation without copying VRAM.
- A mirror test accesses the intended physical byte.

## Common mistakes

- Allocating independent arrays for overlapping character and screen blocks.
- Mirroring with modulo physical size.
- Assuming a span owns independent bytes.

## Further reading

[GBATEK memory/video](https://mgba-emu.github.io/gbatek/#gbamemorymap) — mirroring and write rules. [Tonc tiles](https://gbadev.net/tonc/objbg.html) — shared video storage.

## Next chapter

[Continue](tile-modes.md).
