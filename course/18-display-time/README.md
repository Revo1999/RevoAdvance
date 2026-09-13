# 18. Counting scanlines

**Read this page → edit `src/Gba.Core/Ppu/DisplayTiming.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The GBA display advances through 228 lines per frame, with 1232 system cycles per line. Lines 0–159 are visible. For the DISPSTAT VBlank flag, lines 160–226 are set and line 227 clears it. The nominal drawing budget is 960 cycles, but the DISPSTAT HBlank flag starts at line-cycle 1006 and lasts to the next line. Today IsHBlank models that status flag, not every PPU/DMA access edge. Today track line and line-cycle, starting at zero in your fixture. Advance must retain leftover cycles across calls; a large advance can cross several lines. Rendering and interrupts are later consumers of these boundaries.

## C# you need now

```csharp
int whole = total / 12;
int remainder = total % 12;
// Integer division counts full groups; % retains what remains.
```

A property such as `public int Line { get; private set; }` exposes state for reading while only this component changes it. Accumulate in long if a public cycle count can be large, then reduce to bounded line/frame values. Do not discard remainder cycles after an event.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Store the current line and cycle within the line.
2. Implement Advance for a nonnegative cycle count and wrap after 228 lines.
3. Implement HBlank and VBlank properties using the precise boundaries above.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- At line-cycle 1005 the HBlank status flag is clear; one more cycle sets it.
- 1232 cycles advances one line and resets line-cycle to zero.
- Line 160 enters VBlank; line 227 clears the status flag.
- A whole frame plus 5 cycles ends at line 0, cycle 5.

<details>
<summary>A hint if you get stuck</summary>

A frame is 280,896 cycles. Distinguish the line-160 event from a Boolean flag that is true across multiple lines.

</details>

Optional detail: [the existing hardware reference](../../docs/07-ppu/display-timing.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Remembering interrupt requests](../19-interrupts/README.md). Press **N** in the launcher when this step is checked.
