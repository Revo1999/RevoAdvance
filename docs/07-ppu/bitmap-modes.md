# Bitmap modes: the shortest path to a pixel


## In the real GBA

Bitmap modes make BG2 use a pixel image instead of a tile map. They still participate in display enabling and composition. DISPCNT mode bits choose the format; its BG2 enable bit matters. BG2 affine state also affects sampling, so a first fixture should explicitly use identity transformation.

| Mode | Image dimensions | Pixel storage | Pages |
| --- | --- | --- | --- |
| 3 | 240 × 160 | 16-bit storage, 15-bit RGB colour | one at VRAM base |
| 4 | 240 × 160 | 8-bit palette index | bases 0x06000000 / 0x0600A000 |
| 5 | 160 × 128 | 16-bit storage, 15-bit RGB colour | same two page bases |

The LCD remains 240 × 160 in Mode 5. The bitmap is smaller; what appears outside it depends on sampling/bounds and composition. Page selection comes from DISPCNT's frame-select bit for Modes 4/5. Do not pack the pages immediately next to the used pixel bytes.

```text
15 14......10 9.......5 4.......0
 X    blue      green      red     direct-colour halfword
```

Colour components range from 0 to 31. Converting them to host 0–255 channels is a deliberate conversion, not a byte reinterpretation. Bit 15 is not an alpha bit. In indexed Mode 4, index zero is transparent for BG composition; direct-colour black in Modes 3/5 is a visible colour. The backdrop can make those cases look similar in a single-layer fixture.

## In our emulator

Use synthetic VRAM, palette and display state as inputs; produce a final buffer or a BG2 candidate buffer with explicitly documented scope. Start with Mode 3, identity coordinates and no effects. Work out row stride from pixel width and bytes per pixel. Render a few coloured corners, row/column markers and a centre block before arbitrary artwork.

For a first isolated test, timing is frozen. When integrating, render according to [display timing](display-timing.md), documenting the scanline approximation.

## In C#

Arrays store pixels or bytes; integer arithmetic maps coordinates to offsets. Confirm byte order and bounds before colour conversion. Host output formats such as RGBA and BGRA are different; name your choice.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Create a synthetic Mode 3 fixture and your own converter. Verify explicit corner colours and row orientation. Export an image or inspect it headlessly before adding Vulkan.

## Definition of done

- All four corners have predicted values and positions.
- Red/green/blue maxima and black are correct.
- Later Mode 4 tests distinguish transparent index zero and page selection.

## Common mistakes

- Treating Mode 5 as a smaller LCD.
- Using palette indices as direct colours.
- Reading 16-bit pixels in host-native byte order.

## Further reading

[Tonc bitmap modes](https://gbadev.net/tonc/bitmaps.html) — pixel organization. [GBATEK video](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — mode/register details.

## Next chapter

[Continue](display-timing.md).
