# 03. Turning a GBA address into a memory access

**Read this page → edit `src/Gba.Core/Memory/MemoryBus.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A guest address identifies a place in the GBA, not an index in your PC memory. EWRAM begins at 0x02000000 and is mirrored throughout 0x02000000–0x02FFFFFF. Its 0x40000 physical bytes repeat: addresses 0x02000007 and 0x02040007 name the same byte. First route only this region. Throw ArgumentOutOfRangeException for other addresses; that is a temporary diagnostic policy, not the GBA open-bus rule.

## C# you need now

```csharp
uint address = 0x12000005;
bool inside = address >= 0x12000000 && address < 0x13000000;
int smallIndex = (int)(address & 0xFF);
```

`uint` is an unsigned 32-bit integer, suitable for guest addresses. `&&` combines comparisons. `if (!inside)` handles a rejected range. A cast to int is safe after you have reduced an address to a small bounded offset. The starter uses a primary constructor: `MemoryBus(Ewram ram)` receives the already-created RAM object, which its methods can use.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement Read8 by checking the EWRAM address region and translating to a physical offset.
2. Implement Write8 with the same address translation and the supplied Ewram.
3. Reject unsupported regions before computing an array offset.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- A write to 0x02000007 reaches offset 7 in the original RAM.
- The mirror at 0x02040007 sees the same byte.
- 0x02FFFFFF maps to the last physical byte.
- Addresses outside the EWRAM region report an unsupported access.

<details>
<summary>A hint if you get stuck</summary>

The region selects the device. The low 18 address bits select a byte inside EWRAM. Keep those two decisions separate.

</details>

Optional detail: [the existing hardware reference](../../docs/06-bus-and-memory/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Keeping cartridge program bytes](../04-rom/README.md). Press **N** in the launcher when this step is checked.
