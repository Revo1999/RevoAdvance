# 29. Loading a program and choosing a boot state

**Read this page → edit `src/Gba.Core/Cartridge/BootSession.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

Your local firmware goes in **`roms/gba_bios.bin`**. The desktop build copies it automatically, and **`BiosFile.Load()`** returns its validated bytes. This host helper is already supplied. You do not write or recreate the BIOS. It stays local rather than being included in Git.

## The GBA behavior

A ROM image does not run until the CPU has a deliberate starting state and can fetch it through the bus. Map cartridge reads at 08000000 and the other wait-state windows as appropriate. BIOS code normally provides initialization and services; starting directly at ROM requires an explicit alternative boot contract. Begin with a synthetic instruction sequence in RAM or ROM, then a diagnostic, and only then a chosen game. Do not pretend that setting PC alone reproduces BIOS startup.

## C# you need now

```csharp
byte[] image = File.ReadAllBytes(path);
// In the desktop host: read the file, then pass bytes into Core.
```

A host path is a string; guest addresses are uint values. Catch file errors around host loading and show them before replacing the current session. Constructor arguments or a configuration record can describe BIOS-present versus explicit diagnostic boot modes without scattering special cases through CPU instructions.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Connect a byte image to RomImage and guest ROM address windows; preserve ROM as read-only input.
2. Define a synthetic boot fixture with explicit PC, SP, mode, instruction state, RAM, and expected final signature.
3. Load the local BIOS through the supplied desktop BiosFile.Load() helper, pass its bytes into Core, and map its 16 KiB at guest addresses 00000000–00003FFF. Execute it with your CPU, then diagnose the first divergence for a selected diagnostic or game.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A tiny MOV/ADD/STR fixture writes the hand-computed signature into EWRAM.
- The same image runs identically twice from the same reset state.
- A missing/unreadable ROM leaves the existing session intact and shows a useful message.
- Unsupported instructions/BIOS behavior report an address and operation rather than silently advancing.
- A selected game boot screen is an observed milestone; record its remaining feature requirements.

<details>
<summary>A hint if you get stuck</summary>

If a real game fails, return to the first wrong instruction or device event. Adding unrelated opcodes is less useful than following one reproducible divergence.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/loading-and-playing.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Run, pause, reset, and buttons](../30-play-controls/README.md). Press **N** in the launcher when this step is checked.
