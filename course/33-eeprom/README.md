# 33. A save protocol sent one bit at a time

**Read this page → edit `src/Gba.Core/Cartridge/EepromSave.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

EEPROM save access is serial: bus transfers carry protocol bits rather than ordinary addressed bytes. Common GBA EEPROM capacities use six or fourteen address bits, transferring a 64-bit data block per command. The large addressing form has unused address bits that must be handled as specified. Command framing, stop bits, read dummy bits, and routing depend on the cartridge mapping. Start with a configured size so detection does not obscure the protocol.

## C# you need now

```csharp
int collected = 0;
ulong block = 0;
// A counter tracks how many bits of a command or block have arrived.
```

A state machine plus a bit counter is enough. ulong holds 64 data bits; avoid shifting by 64 because C# masks shift counts. Collect or emit one bit at a time in an explicit order. Keep command state separate from persistent storage.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Decode read/write command framing for one configured EEPROM size using the reference’s bit sequence.
2. Collect address/data bits and implement block write plus dummy/read-data output.
3. Add the second capacity, bus/DMA routing, and persistence without confusing EEPROM commands with ROM reads.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- A complete serial write followed by read returns the same asymmetric 64-bit pattern.
- Two neighboring block addresses remain independent.
- Read output begins with the documented dummy bits before data.
- A partial command does not accidentally become a completed write.
- The same EEPROM data survives a full close/reopen, while save states also preserve partial protocol state.

<details>
<summary>A hint if you get stuck</summary>

Use a pattern such as 0123456789ABCDEF rather than all-zero/all-one data: it exposes reversed bit order.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [A sound channel as changing numeric output](../34-square-audio/README.md). Press **N** in the launcher when this step is checked.
