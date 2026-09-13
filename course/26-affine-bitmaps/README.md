# 26. Affine sampling and the other bitmap modes

**Read this page → edit `src/Gba.Core/Ppu/AffineBackground.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Affine backgrounds transform screen coordinates into source coordinates using fixed-point coefficients. Begin with identity, then translation and scaling. Mode 3 is 240×160 direct color at VRAM base. Mode 4 is 240×160 palette indexes; Mode 5 is 160×128 direct color inside the 240×160 display. Modes 4/5 have page bases separated by 0xA000, selected by DISPCNT bit 4. BG2 must be enabled. Direct-color black is opaque, while indexed Mode 4 index zero participates as transparency.

## C# you need now

```csharp
int fixedValue = 3 << 8;
int integerPart = fixedValue >> 8;
// Eight fractional bits represent 3.0 as 768.
```

Fixed-point arithmetic stores fractions in integer bits. Sign-extend coefficients/reference values at their actual register widths before using them. Preserve internal reference accumulators where hardware behavior needs them; do not round to an integer after every addition.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Render a Mode 3 frame from synthetic VRAM with identity BG2 sampling and GbaColor.
2. Implement Mode 4 palette lookup/page selection, then Mode 5 dimensions/page selection.
3. Add affine BG sampling and affine OBJ matrices; test identity before scale/rotation, then add wrapping/bounds rules and per-line reference updates.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Mode 3 corners have distinct expected colors and rows are 240 pixels wide.
- Toggling page select in Mode 4 changes the image without moving the palette.
- Mode 5 leaves the area outside its sampled image to composition rather than stretching it automatically.
- Identity affine sampling matches the non-transformed fixture.
- A translation moves a unique marker by the predicted amount; negative coordinates are handled deliberately.

<details>
<summary>A hint if you get stuck</summary>

Do not place the second page immediately after the used pixel data. Its base is a hardware address offset, not an image-size calculation.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/bitmap-modes.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Choosing the final visible pixel](../27-composition/README.md). Press **N** in the launcher when this step is checked.
