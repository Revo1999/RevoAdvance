# 36. Timer-driven audio FIFOs and DMA refill

**Read this page → edit `src/Gba.Core/Apu/DirectSound.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Direct Sound A/B consume signed eight-bit samples from 32-byte FIFOs on their selected timer overflows. A 32-bit FIFO write contributes four samples in little-endian byte order. When the FIFO drops to its refill threshold (16 bytes or fewer), it can request the special sound DMA transfer. The callback from your desktop audio device must not directly consume the guest FIFO; only guest timer events do that.

## C# you need now

```csharp
sbyte signedSample = unchecked((sbyte)rawByte);
// FF represents -1, not an unsigned amplitude of 255.
```

A ring buffer uses a fixed array, read index, write index, and count. Modulo wraps positions. Keep the current output sample separate from queued data; its lifetime follows timer consumption. A refill request is a device event delivered to DMA, not a recursive arbitrary memory copy.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement each FIFO’s fixed-capacity queue and four-byte writes.
2. Connect selected timer overflows to sample consumption, reset behavior, and DMA refill requests.
3. Add special FIFO DMA semantics and route A/B sample levels into the guest mixer.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Writing 807F00FF yields signed samples −1,0,127,−128 in that order.
- No selected timer overflow means no sample is consumed.
- Crossing the refill threshold requests sound DMA; the transfer refills the queue using the required fixed destination.
- Reset clears queue state as specified without resetting unrelated audio channels.
- A fixed guest timer/input stream gives identical output regardless of desktop callback chunk size.

<details>
<summary>A hint if you get stuck</summary>

Test the ring-buffer wrap with more than one cycle through its capacity. Keep overflow/underflow behavior explicit and compare it with the hardware reference.

</details>

Optional detail: [the existing hardware reference](../../docs/13-audio/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Mixing and playing the sound](../37-host-audio/README.md). Press **N** in the launcher when this step is checked.
