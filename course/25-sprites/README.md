# 25. Objects on top of backgrounds

**Read this page → edit `src/Gba.Core/Ppu/Objects.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Sprites are called objects (OBJ). The GBA has 128 OAM entries, each eight bytes. Attribute 0 contains Y and mode/shape information, attribute 1 X and size/flip information, and attribute 2 tile index, priority, and palette bank. Coordinates wrap in their hardware bit widths. Start with one regular square 8×8 4bpp object; transparent index zero contributes no pixel. Bitmap modes restrict usable OBJ tile memory, so keep your first fixture in a tile display mode.

## C# you need now

```csharp
public readonly record struct PixelCandidate(uint Color, int Priority, int ObjectIndex);
```

A result record carries metadata needed later by composition. Returning only a final color too early loses tie-breaking information. Use explicit sign/wrap conversion for coordinates; a large stored coordinate may put an object partly off the left or top edge.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Read one regular square object and sample its tile pixels through OBJ palette memory.
2. Add flips and wrapped positions, then size/shape combinations and 1D/2D tile mapping.
3. Evaluate multiple OAM entries with priority and index ties; keep affine objects as the next lesson’s separate coordinate transform.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- An 8×8 object at (10,20) covers the intended eight pixels each way.
- Transparent holes reveal a background pixel.
- X=511 places the left edge at −1 after wrapping, showing only the visible portion.
- Two regular objects with equal priority choose the lower OAM index at an overlap.
- Switching 1D/2D mapping changes row tile addresses as expected for a multi-tile object.

<details>
<summary>A hint if you get stuck</summary>

Read one object into a small decoded state before rendering it. OAM is not an array of host-side sprite objects with independent fields.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/sprites.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Affine sampling and the other bitmap modes](../26-affine-bitmaps/README.md). Press **N** in the launcher when this step is checked.
