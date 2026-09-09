# Tiles and backgrounds: patterns plus placement


## In the real GBA

A tile is an 8 × 8 pattern. At 4 bits per pixel it occupies 32 bytes and chooses from a 16-colour bank. At 8 bits per pixel it occupies 64 bytes and indexes a 256-colour palette. Index zero is transparent for tiled layers. A map selects which tile appears at each location; a regular BG map entry also carries flip and palette-bank bits.

```text
screen coordinate
    ↓ apply scroll / wrap
map cell + position within 8×8 cell
    ↓ map entry selects tile, flips and palette bank
tile pixel index → palette colour → candidate pixel with priority
```

Modes 0–2 choose combinations of regular and affine backgrounds: Mode 0 has four regular BGs; Mode 1 has BG0/1 regular and BG2 affine; Mode 2 has BG2/3 affine. Regular maps use 16-bit entries and screen-block organization. Affine maps have different entry formats and sizes; do not reuse regular-map decoding unchanged.

Registers include BGCNT, horizontal/vertical offsets for regular BGs, and affine matrix/reference registers. VRAM contains both maps and tiles, palette RAM contains colours. Rendering follows display time; a first fixture freezes these inputs and samples an unscrolled scene.

## In our emulator

Start with one 8 × 8 tile and one palette, then a small repeated map. Separate map coordinates, local tile coordinates and final screen coordinates on paper. Add scrolling, flips, map block boundaries and mode combinations incrementally. A candidate pixel needs transparency and priority as well as colour.

## In C#

Nibble extraction uses masks/shifts and explicit byte indexing. Remainders and divisions can explain coordinates clearly before optimizing them. Avoid a new heap object per sampled pixel.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Render one 4-bpp tile from synthetic data, then repeat it through a regular background map. Add asymmetric patterns so flips and nibble order are observable.

## Definition of done

- A hand-drawn 8 × 8 expected result matches pixel values.
- Horizontal/vertical flips and palette banks work.
- A map block boundary test catches incorrect row layout.

## Common mistakes

- Swapping high/low nibbles.
- Treating every map as one flat linear layout.
- Forgetting index-zero transparency.

## Further reading

[Tonc regular backgrounds](https://gbadev.net/tonc/regbg.html) — maps and tiles. [GBATEK BG controls](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — formats and modes.

## Next chapter

[Continue](sprites.md).
