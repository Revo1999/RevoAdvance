# 24. Drawing a tiled background

**Read this page → edit `src/Gba.Core/Ppu/TextBackground.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A regular background map selects 8×8 tiles. A 16-bit map entry contains tile number in bits 0–9, horizontal/vertical flip in bits 10/11, and the 4bpp palette bank in bits 12–15. A 4bpp tile is 32 bytes; its first pixel is the low nibble. An 8bpp tile is 64 bytes. Color index zero is transparent for background composition. Begin with one 32×32-tile map, 4bpp, no scrolling; then add flips, palette banks, larger maps, and scroll wrapping.

## C# you need now

```csharp
int cellX = x / 8;
int withinCellX = x % 8;
// Quotient selects a tile; remainder selects a pixel inside it.
```

Use a flat array for image buffers and compute `y * width + x`. Keep coordinate selection, tile-byte lookup, palette lookup, and transparency separate. A pixel result can carry both a color and a Boolean visible flag; black and transparent are different.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Render a synthetic 8×8 4bpp tile through your palette and GbaColor converter.
2. Read map entries to select tiles and implement H/V flip plus palette bank.
3. Add scrolling, 8bpp, and 256/512-pixel map sizes one fixture at a time; connect BG control registers through the bus.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A tile with first byte 21 (hex) draws palette index 1 then 2.
- A distinct corner marker moves to the opposite corner under each flip.
- Palette index zero lets the backdrop show through.
- Scrolling across an 8-pixel boundary selects the adjacent tile without a gap.
- For 512-pixel maps, verify screen-block selection rather than assuming one flat 64×64 map in memory.

<details>
<summary>A hint if you get stuck</summary>

Use an asymmetric test tile, with different colors in all corners. A symmetric checkerboard can hide a flipped-coordinate bug.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/tile-modes.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Objects on top of backgrounds](../25-sprites/README.md). Press **N** in the launcher when this step is checked.
