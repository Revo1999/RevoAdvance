# 23. Connecting components to one guest clock

**Read this page → edit `src/Gba.Core/Common/GbaMachine.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A GBA instruction, DMA transfer, timer, and scanline share guest time. Your PC running faster must not make timers count differently. Build one owner for CPU, bus, PPU timing, timers, DMA, and IRQ state. First run a deterministic instruction or fixed-cycle fixture; later use bus sequential/nonsequential wait states and instruction internal cycles. HALT stops CPU execution but relevant devices continue. Pause, unlike HALT, stops advancing the whole guest.

## C# you need now

```csharp
public readonly record struct StepResult(int Cycles);
// Return work consumed instead of reading DateTime inside emulated hardware.
```

Composition means one object holds references to the pieces you already made. Constructor parameters supply those references. Use long for cumulative cycle counts. Process events at their boundaries rather than advancing every component by a whole frame and hoping their order matches.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Connect CPU fetch/decode/execute to the bus and define what one Step returns. Add IWRAM, ROM, BIOS storage, and required I/O routing as separate regions.
2. Advance timing and timers by consumed cycles; deliver HBlank/VBlank/timer events to DMA and IRQ in a documented order.
3. Expand to all four timers with cascade; add HALT and distinguish it from host pause. Keep hardware state changes in one controlled thread initially.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Running the same fixture as one cycle batch or many small batches reaches the same counter/line state.
- A timer overflow feeds its cascade successor and IRQ once per event.
- HALT allows a display/timer event to become pending; pause changes no guest state.
- A memory-mapped IF write acknowledges rather than replacing the latch.
- Record event order for coincident timer/display/DMA activity; rerunning produces the same trace.

<details>
<summary>A hint if you get stuck</summary>

Start by returning a deliberately limited cycle cost and label it approximate. Replace that cost at one boundary as timing accuracy grows; do not scatter host clocks through components.

</details>

Optional detail: [the existing hardware reference](../../docs/14-timing-and-scheduling/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

The runner now retires the early “all non-EWRAM regions are unsupported” rejection check so you can map IWRAM and other devices. Existing EWRAM routing/mirroring checks still run.

Next: [Drawing a tiled background](../24-tiles/README.md). Press **N** in the launcher when this step is checked.
