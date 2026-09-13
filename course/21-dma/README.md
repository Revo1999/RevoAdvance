# 21. Copying through the bus with DMA

**Read this page → edit `src/Gba.Core/Dma/DmaChannel.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

DMA moves halfwords or words without the CPU executing each load/store. A channel latches source, destination, and count when enabled; bus reads/writes then consume guest time. Start with one immediate incrementing channel and a nonzero count. Count is transfers, not bytes. Four channels later add priority (0 highest), triggers, address control, repeat/reload, and completion IRQ. A zero count means the channel-specific maximum, not no work: 0x4000 units on channels 0–2, 0x10000 on channel 3.

## C# you need now

```csharp
public enum AddressMode { Increment, Decrement, Fixed, Reload }
// Named values make configuration easier to read than unexplained numbers.
```

Use fields for latched running state separate from writable register values. A small Step method can perform one transfer and report consumed cycles; an immediate loop can call it until finished. Route through bus methods so device side effects are preserved.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement one nonzero immediate halfword copy through MemoryBus; add word width next.
2. Advance latched addresses according to transfer width, then add decrement/fixed/destination-reload behavior.
3. Connect four channels to scheduler triggers and completion IRQ; add repeat and zero-count decoding as separate cases.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Copy three halfwords 1111,2222,3333: destination bytes and final addresses match six transferred bytes.
- Word transfers advance incrementing addresses by four.
- A fixed destination receives each successive source value at the same address.
- HBlank-triggered DMA waits for its trigger; simultaneous eligible channels run in priority order.
- A completion IRQ occurs once per completed transfer sequence, not once per unit.

<details>
<summary>A hint if you get stuck</summary>

Do not use Array.Copy: it bypasses the bus and its device behavior. Start with RAM fixtures before special FIFO DMA.

</details>

Optional detail: [the existing hardware reference](../../docs/10-dma/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Pressed buttons become zero bits](../22-keypad/README.md). Press **N** in the launcher when this step is checked.
