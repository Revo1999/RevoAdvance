# 13. The first Thumb instructions

**Read this page → edit `src/Gba.Core/Cpu/ThumbImmediate.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Thumb instructions are 16 bits wide, but registers still hold 32 bits. Start with immediate MOV (top five bits 00100), CMP (00101), ADD (00110), and SUB (00111). Bits 10–8 select R0–R7 and bits 7–0 hold the immediate. MOV updates N/Z while preserving C/V. ADD, SUB, and CMP update NZCV; CMP does not write the result. Execute returns the updated CPSR while preserving all bits outside the flags it changes.

## C# you need now

```csharp
ushort instruction = 0x2509;
int index = (instruction >> 8) & 7;
// index is 5. ushort stores one 16-bit Thumb encoding.
```

Shifts on ushort are promoted to int. Convert the extracted immediate to uint when doing register arithmetic. Reuse Arithmetic for flags, instead of inventing a second rule for Thumb. A returned uint can replace the caller's CPSR; the supplied register object retains register changes.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Decode MOV/CMP/ADD/SUB immediate and the low register index.
2. Reuse Arithmetic for arithmetic flags; merge changed flag bits with old CPSR.
3. Return updated CPSR, leaving registers unchanged for CMP.

## Check it

The launcher runs **3 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- MOV r5,#9 writes R5 and preserves C/V and control bits.
- MOV 7, ADD 5, SUB 2 leaves R0=10 and C set after subtraction.
- CMP equal values sets Z+C and leaves its source unchanged.

<details>
<summary>A hint if you get stuck</summary>

Thumb is another decoder feeding the same CPU state, not another CPU. Later add shifts, ALU/register forms, loads/stores, high registers, stack operations, and branches one family at a time.

</details>

Optional detail: [the existing hardware reference](../../docs/05-thumb-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Stacks and transferring several registers](../14-stack-transfers/README.md). Press **N** in the launcher when this step is checked.
