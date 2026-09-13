# 38. Restoring an exact emulated moment

**Read this page → edit `src/Gba.Core/Common/SaveState.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

An emulator save state captures the machine, unlike a game’s cartridge save. Include CPU banks/status/pipeline convention, every memory device, timer remainders, DMA latches, interrupt requests, PPU internal state, audio phases/FIFOs, scheduler time, and in-progress Flash/EEPROM commands. Include a format version and ROM identity. Host window/GPU/audio handles are not guest state and must be reconstructed or rebound.

## C# you need now

```csharp
public sealed record SnapshotHeader(int Version, string RomId);
// A record can describe data; mutable arrays inside it still need copies.
```

A shallow object copy shares arrays and can silently change your saved snapshot. Copy mutable guest data deliberately. Parse/validate a state into temporary data before replacing the running machine. Use an explicit versioned representation rather than serializing arbitrary host objects.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Capture an owned snapshot of all guest state and restore it into a compatible machine.
2. Add version/ROM validation and host file slots; reject malformed/incompatible files before changing the current session.
3. Decide and show how loading an older state affects later cartridge-save persistence. Refill host output buffers from restored guest state.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Run N steps, snapshot, run M, restore, run the same M: registers, memory, frame, and audio sequence agree.
- Taking a snapshot then changing RAM does not change the snapshot.
- Restoring midway through a timer divisor, DMA transfer, or EEPROM command resumes the same behavior.
- A wrong-ROM or corrupt state leaves the running machine intact.
- The normal Save State/Load State UI works after fully closing and reopening the app.

<details>
<summary>A hint if you get stuck</summary>

Deterministic replay is a stronger check than seeing the same picture immediately after loading.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/saving-and-resuming.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Finding the first wrong step](../39-debugger/README.md). Press **N** in the launcher when this step is checked.
