# 02. Reading two or four bytes together

**Read this page → edit `src/Gba.Core/Memory/RamWords.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The GBA is little endian: the byte at the lowest address supplies the lowest eight bits of a larger value. Bytes 34 12 (hex) represent 0x1234. Bytes 78 56 34 12 represent 0x12345678. A halfword is two bytes; a word is four. This helper is only for valid, naturally aligned offsets in ordinary EWRAM, not I/O devices or CPU unaligned-load behavior.

## C# you need now

```csharp
uint value = 0xABCD;
byte low = (byte)(value & 0xFF);
uint moved = value << 4;
```

`0x` writes a hexadecimal number. `&` keeps bits selected by a mask. `<<` moves bits left; `>>` moves them right. `|` combines bit fields. `(byte)` converts a value to a byte after you select the desired bits. `ushort` holds 16 bits; `uint` holds 32. Cast a byte to uint before placing it in the top eight bits of a word. The supplied `RamWords(Ewram ram)` is a primary constructor: it receives your existing RAM object, available as `ram` inside these methods. The `=> throw ...` syntax is an unfinished expression body; replace it with `{ ... }` when writing several statements.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement Read16 and Write16 through the supplied Ewram object.
2. Implement Read32 and Write32 through the same storage.
3. Keep each byte in increasing address order; do not make a second memory array.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- Bytes 34 12 read as 0x1234.
- Writing 0xBEEF stores EF then BE.
- Bytes 78 56 34 12 read as 0x12345678.
- Writing 0xFEDCBA98 stores 98 BA DC FE.

<details>
<summary>A hint if you get stuck</summary>

Number the bytes 0, 1, 2, 3. Work out how many bits each is above the lowest byte before combining them.

</details>

Optional detail: [the existing hardware reference](../../docs/csharp-and-dotnet/arrays-and-spans.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Turning a GBA address into a memory access](../03-bus/README.md). Press **N** in the launcher when this step is checked.
