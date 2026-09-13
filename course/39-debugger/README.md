# 39. Finding the first wrong step

**Read this page → edit `src/Gba.Core/Common/TraceRecorder.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A debugger should explain guest execution without changing it. Start with a bounded instruction trace: address, ARM/Thumb state, instruction bits, register/flag changes, and elapsed guest cycles. Add a breakpoint before execution and a memory inspection path that does not trigger read side effects. The first divergent instruction or event is usually more useful than the final corrupted screen.

## C# you need now

```csharp
public readonly record struct TraceEntry(uint Address, uint Instruction, long Cycle);
```

A bounded ring buffer prevents an always-on trace from growing indefinitely. Capture values at a defined moment rather than retaining mutable references to registers. An inspection API may need a separate Peek operation from guest Read, because reading a device can itself have behavior.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Capture a bounded trace around CPU steps and significant device events.
2. Add address breakpoints/single-step and a side-effect-free inspection path for supported devices.
3. Compare a small deterministic fixture against a trusted trace/expected states and stop at the first mismatch.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Tracing enabled versus disabled leaves final guest state identical.
- A breakpoint stops before the target instruction changes registers.
- Inspecting a register/device does not acknowledge IRQs or consume FIFO data.
- The trace wraps within its configured capacity.
- A deliberate fault in a local test fixture is localized to the first wrong step, then removed.

<details>
<summary>A hint if you get stuck</summary>

The UI for trace tables and memory views is assistance-friendly host work. The important emulator decision is when and what guest state to capture.

</details>

Optional detail: [the existing hardware reference](../../docs/17-debugging-tools/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Making one game reliably playable](../40-compatibility/README.md). Press **N** in the launcher when this step is checked.
