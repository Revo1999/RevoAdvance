# 34. A sound channel as changing numeric output

**Read this page → edit `src/Gba.Core/Apu/SquareChannel.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Begin audio as numbers over guest time, before using a speaker. The legacy sound channels have phase/frequency, length, envelope, and trigger state. A square channel cycles through a duty pattern; trigger initializes the channel’s internal state. Choose square channel 2 first to avoid channel 1’s extra sweep behavior. Register writes configure the channel; simply generating Math.Sin samples does not reproduce it.

## C# you need now

```csharp
int phase = 0;
int output = enabled ? amplitude : 0;
// State advances from guest clocks, not from the desktop audio callback.
```

An array can hold a small duty pattern; a bounded integer selects its current entry. Keep oscillator timing separate from the slower envelope/length clocks. Return a numeric sample/level so it can be checked before host audio exists.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement channel 2 duty stepping and frequency timing from its configured period.
2. Add trigger, DAC enable, length, and volume envelope in separate steps.
3. Connect sound register reads/writes and test batched versus split guest-cycle advancement.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A fixed frequency repeats the selected duty pattern after the expected guest-cycle period.
- Duty changes alter high/low proportions rather than merely changing volume.
- Length expiry silences the channel when length control is enabled.
- Envelope ticks change volume at the configured rate and stop at its limit.
- One large Advance and many smaller Advances produce the same phase, envelope, and output.

<details>
<summary>A hint if you get stuck</summary>

Capture a short list of numeric output changes and their cycle positions. Listening alone cannot reveal an off-by-one phase or envelope tick.

</details>

Optional detail: [the existing hardware reference](../../docs/13-audio/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [The other legacy sound sources](../35-wave-noise/README.md). Press **N** in the launcher when this step is checked.
