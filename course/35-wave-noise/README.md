# 35. The other legacy sound sources

**Read this page → edit `src/Gba.Core/Apu/LegacyAudio.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The remaining legacy sources add channel 1 frequency sweep, wave RAM playback, and noise from a linear feedback shift register (LFSR). Wave samples are packed four-bit values. Noise is a deterministic bit sequence, not a call to Random. Sound routing and master controls determine which channels reach the left/right mix. Implement one source at a time and retain separate channel state.

## C# you need now

```csharp
int highNibble = packed >> 4;
int lowNibble = packed & 0xF;
// This extracts two four-bit samples; playback order follows the hardware format.
```

Bit fields and small state machines are reusable ideas, not new architecture. Use ushort for a bounded LFSR but explicitly apply the hardware feedback and width rules. Avoid allocations in the steady per-sample/per-cycle path once correctness is established.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Add channel 1 sweep to the existing square-channel behavior, including overflow/disable cases.
2. Implement wave RAM nibble playback and banking/volume controls.
3. Implement the noise LFSR widths and clock selection, then route all four sources through master and left/right controls.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A known wave pattern plays nibbles in the documented order and repeats at the configured period.
- Sweep changes frequency on its own clock and handles overflow disable.
- Noise from a fixed initial state produces the same bit sequence on every run.
- Changing noise width changes the sequence without using a random generator.
- Muting one route affects only that channel/side, not oscillator phase in unrelated channels.

<details>
<summary>A hint if you get stuck</summary>

Test wave/noise as numeric sequences. A deterministic wrong sound is easier to diagnose than a host-audio timing problem mixed with a wrong generator.

</details>

Optional detail: [the existing hardware reference](../../docs/13-audio/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Timer-driven audio FIFOs and DMA refill](../36-direct-sound/README.md). Press **N** in the launcher when this step is checked.
