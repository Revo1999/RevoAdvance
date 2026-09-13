# 12. Moving values between registers and memory

**Read this page → edit `src/Gba.Core/Cpu/SingleTransfer.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

ARM LDR/STR move words; LDRB/STRB move bytes. First implement immediate offsets, pre-indexed addressing, no writeback, with ordinary EWRAM. Compute the effective address from Rn, then access the bus. Extend MemoryBus with Read16/32 and Write16/32 for RAM, reusing your byte-order helper. Later add post-indexing, writeback, register offsets, halfwords and signed loads. On ARM7TDMI, an unaligned word load reads an aligned word then rotates it; this CPU rule is not the same as four arbitrary byte reads.

## C# you need now

```csharp
uint address = add ? unchecked(baseAddress + offset) : unchecked(baseAddress - offset);
```

`condition ? first : second` chooses one expression. Keep effective-address calculation separate from the bus access and base-register update, so a writeback cannot accidentally change the source address. Sign-extending a byte uses `unchecked((uint)(int)(sbyte)value)`; an ordinary byte load zero-extends.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Add RAM width access to MemoryBus, then implement immediate pre-indexed LDR/STR and byte variants.
2. Connect decoding to the CPU and preserve the condition check before any memory side effect.
3. Add post-index/writeback and unaligned word-load rotation. Expand halfword/signed transfers as separate small cases, using their distinct encodings.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- With r0=02000000 and r1=12345678, E5801000 stores r1; E5902000 reads it into r2.
- A byte store changes exactly one byte; a byte load returns 0–255.
- A failing condition neither writes memory nor updates Rn.
- With aligned word 12345678 at A, a word load from A+1 returns 78123456.
- Record separate cases for positive/negative offsets and pre/post indexing before expanding instruction families.

<details>
<summary>A hint if you get stuck</summary>

Byte writes are valid for EWRAM; do not later reuse this implementation blindly for VRAM, palette RAM, or OAM. Handle an unsupported encoding explicitly until implemented.

</details>

Optional detail: [the existing hardware reference](../../docs/06-bus-and-memory/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [The first Thumb instructions](../13-thumb/README.md). Press **N** in the launcher when this step is checked.
