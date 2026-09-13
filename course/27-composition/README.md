# 27. Choosing the final visible pixel

**Read this page → edit `src/Gba.Core/Ppu/Compositor.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The final pixel is selected from enabled BG/OBJ candidates and the backdrop. Lower priority numbers win; tie rules depend on layer type (OBJ is ahead of a BG at the same priority; equal-priority BGs use lower BG number). Windows control which layers and color effects apply at a position. Blending acts on selected first/second targets, not every pair of colors. Start with priority and transparency before adding effects. Mosaic repeats sampled blocks rather than simply scaling the completed image.

## C# you need now

```csharp
int bounded = Math.Min(31, Math.Max(0, channel));
// Clamp after arithmetic, not before you have computed the result.
```

Separate candidate selection from color math. A tuple or record can retain layer identity, priority, and effect eligibility. Alpha coefficients use integer arithmetic and bounded ranges: the GBA channels are still five-bit values during these effects.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Choose a visible candidate using enable bits, transparency, priority, and ties.
2. Apply window masks before selection/effects; include OBJ-window behavior separately.
3. Add alpha, brighten/darken, and mosaic with small pixel fixtures, then connect display flags and mid-frame register writes at your chosen timing precision.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A transparent top candidate reveals the next visible one; opaque black hides it.
- OBJ versus BG and BG versus BG ties follow their documented order.
- A window boundary changes exactly the intended pixel range.
- Alpha at coefficients 8 and 8 produces the expected half-strength contribution from each selected target, clamped at 31.
- Brighten at full coefficient produces white; darken produces black; disabled effects preserve the selected color.
- State the remaining scanline versus per-pixel timing limits instead of treating a static image as full PPU accuracy.

<details>
<summary>A hint if you get stuck</summary>

First make a table of two or three candidates for one pixel and choose the winner on paper. Only then add an effect.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/composition.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Showing your framebuffer in a window](../28-desktop-display/README.md). Press **N** in the launcher when this step is checked.
