# 40. Making one game reliably playable

**Read this page → edit `src/Gba.Core/Common/CompatibilityNotes.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A passing small lesson checks its stated behavior, not all hardware. Now use diagnostic programs and one selected game to drive accuracy: bus wait states and sequential access, CPU pipeline/alignment corner cases, I/O masks and access widths, PPU timing, DMA priority, timer edges, BIOS behavior, and cartridge protocols. Keep serial/link and unusual peripherals explicit optional extensions if outside your selected target. “Playable” means a repeatable user workflow, not just a boot picture.

## C# you need now

```csharp
var watch = System.Diagnostics.Stopwatch.StartNew();
// Measure a repeatable workload after correctness is established.
```

Stopwatch measures host performance; it must not become the guest clock. Compare the same fixture and inputs before/after an optimization. Use structured fixture results so a failure retains its diagnostic name, input, expected result, and actual result.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Choose one diagnostic failure or visible game defect, capture its earliest divergence, and fix that behavior only. Add a regression case.
2. Repeat until a defined section of one selected game has working graphics, input, audio, and persistence.
3. Exercise normal open/pause/reset/switch/save/state/close workflows, then profile any measured bottleneck. Record actual unsupported behavior instead of claiming universal compatibility.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A versioned diagnostic set produces repeatable recorded results, including remaining failures.
- Play the chosen section through the normal Open ROM path with responsive controls, graphics, and audio.
- Save in-game, close completely, reopen, and Continue with the same progress.
- Save-state replay remains deterministic after accuracy fixes.
- A measured optimization changes performance without changing fixture outputs.
- Remaining instruction/device/timing gaps are named with a next reproducible case.

<details>
<summary>A hint if you get stuck</summary>

You do not need to read every reference before fixing the next defect. Use the same loop: learn the one relevant hardware rule, learn any missing syntax, implement it, check the case.

</details>

Optional detail: [the existing hardware reference](../../docs/16-testing/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

You have reached the course’s integration milestone. Continue the same loop for each compatibility improvement.
