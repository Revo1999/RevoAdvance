# 17. Turning a GBA color into a pixel

**Read this page → edit `src/Gba.Core/Ppu/GbaColor.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A direct GBA color uses five red bits (0–4), five green bits (5–9), and five blue bits (10–14). Bit 15 is unused, not alpha. Mode 3 stores one halfword per pixel for a 240×160 image. Start with color conversion only. Our host format is explicitly the integer 0xFFRRGGBB. Expand a five-bit channel to eight using bit replication: (channel << 3) | (channel >> 2). This chooses a deterministic conversion; actual LCD color response is a separate topic.

## C# you need now

```csharp
uint packed = (0xFFu << 24) | (red << 16) | (green << 8) | blue;
// red, green, blue are uint channel values from 0 through 255.
```

Integer channel packing is a format contract, not an assumption about in-memory byte order. Mask each source channel before expanding it. A pure static Convert method can be checked without a window or GPU.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Extract the three five-bit channels.
2. Expand each channel with bit replication.
3. Pack an opaque 0xFFRRGGBB value and ignore source bit 15.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- 001F becomes FFFF0000 (red).
- 03E0 becomes FF00FF00 (green).
- 7C00 becomes FF0000FF (blue).
- FFFF becomes FFFFFFFF; channel value 16 expands to 132.

<details>
<summary>A hint if you get stuck</summary>

Red is in the low GBA bits but the high color byte of this host format. Write down both layouts before moving bits.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/bitmap-modes.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Counting scanlines](../18-display-time/README.md). Press **N** in the launcher when this step is checked.
