# 31. Keeping a game save after the app closes

**Read this page → edit `src/Gba.Core/Cartridge/SramSave.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Cartridge save memory is separate from ROM and volatile work RAM. Begin with a configured SRAM cartridge: byte reads/writes change a save buffer and mark it dirty. Desktop loads a matching save before running the guest, and writes dirty bytes at controlled boundaries. The original .gba stays unchanged. Identify saves by cartridge identity, not merely a short display title that two games could share.

## C# you need now

```csharp
byte[] snapshot = (byte[])saveBytes.Clone();
// Capture a stable snapshot before handing bytes to file-writing code.
```

A dirty flag tracks changed data, not successful disk persistence. Clear it only after the corresponding snapshot is safely written, accounting for any newer changes. Use host file APIs outside the memory device. Saving through a temporary file and replacement keeps the previous good save when an update fails.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement configured SRAM byte storage and guest bus routing; keep it separate from ROM.
2. Add load/export snapshots and dirty tracking; supply host file persistence plumbing if needed.
3. Integrate save loading/flushing with Open ROM, reset, switching games, and orderly close.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Write a marker through the guest bus, persist, fully close, reopen, and read the same marker.
- Two different cartridge identities have independent saves.
- A failed disk write preserves the previous good save and keeps new data dirty.
- A supported game’s Save → close → reopen → Continue works through the normal app path.
- The ROM file’s bytes remain unchanged.

<details>
<summary>A hint if you get stuck</summary>

First verify a tiny byte marker independently of a game. Then test the in-game save protocol and host persistence together.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/saving-and-resuming.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Flash saves are a command-driven device](../32-flash/README.md). Press **N** in the launcher when this step is checked.
