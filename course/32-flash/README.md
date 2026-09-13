# 32. Flash saves are a command-driven device

**Read this page → edit `src/Gba.Core/Cartridge/FlashSave.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Flash is not SRAM with a larger array. Software sends command sequences to select identification, programming, erasing, or bank switching. Common unlock writes are AA to offset 5555 then 55 to 2AAA; the next command selects an operation. Device size and IDs belong to a selected cartridge/device profile. Erased bytes are FF. Start with one explicit profile and one command at a time; do not guess save type by treating every write as raw data.

## C# you need now

```csharp
public enum FlashPhase { Idle, Unlock1, Unlock2, ProgramByte }
// A phase remembers where you are in a multi-write protocol.
```

Use a state machine: each write sees current phase, address, and value, then changes phase or storage. An enum makes transitions inspectable. Persistence exports the byte storage; an emulator save state must also retain any in-progress command state.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement unlock tracking, ID read mode, and reset-to-read for one named Flash profile.
2. Add byte programming and sector/chip erase using that profile’s protocol and geometry.
3. Add 128 KiB banking as a separate profile, then connect storage persistence through the SRAM lesson’s host mechanism.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Ordinary writes without a valid command sequence do not behave like SRAM writes.
- ID mode reports the configured IDs; reset returns to array reads.
- Programming affects the selected location according to Flash bit-programming rules; erase returns its region to FF.
- An invalid/interrupted command sequence recovers predictably without corrupting unrelated bytes.
- Switching banks reveals independent data, and close/reopen preserves both banks.

<details>
<summary>A hint if you get stuck</summary>

Draw the command phases for a single byte program before writing the transition code. Use the exact command/device table in the reference for IDs and erase sizes.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [A save protocol sent one bit at a time](../33-eeprom/README.md). Press **N** in the launcher when this step is checked.
