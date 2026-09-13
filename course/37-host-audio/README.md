# 37. Mixing and playing the sound

**Read this page → edit `src/Gba.Desktop/Audio/AudioOutput.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Guest channel levels must be routed/mixed with sound controls and bias, then resampled to the host device rate. The guest clock determines the signal; the host consumes buffered samples. If the host needs more data, that is a buffering concern, not permission to change a timer period. Begin with a synthetic tone and a bounded queue, then connect your guest mix. Non-SDL backend setup and device plumbing can be supplied as assistance.

## C# you need now

```csharp
Span<float> output = buffer.AsSpan();
// A span gives temporary access to existing storage without copying it.
```

A Span cannot be kept across arbitrary asynchronous work. Hand callbacks owned buffers or fill the provided span during the callback. Use a fractional resampling position so rounding each sample independently does not drift. Keep callbacks small and avoid file access or allocation in the steady path.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement guest routing, levels, saturation/bias, and a deterministic resampling boundary.
2. Have the host audio device/queue plumbing supplied or connect it to AudioOutput; verify a known synthetic tone first.
3. Feed guest mixed samples, then handle pause, resume, underrun, and close without changing guest timing.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A known synthetic tone has stable pitch and the intended left/right routing.
- A muted route produces silence on that side.
- Long playback does not steadily grow the queue or accumulate drift.
- Pause/resume does not play seconds of stale buffered audio.
- Repeated close/reopen releases the device and a supported game’s audio plays with bounded latency.

<details>
<summary>A hint if you get stuck</summary>

Compare guest sample sequences before listening to resampled output. This separates emulation mistakes from buffering and device problems.

</details>

Optional detail: [the existing hardware reference](../../docs/13-audio/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Restoring an exact emulated moment](../38-save-states/README.md). Press **N** in the launcher when this step is checked.
