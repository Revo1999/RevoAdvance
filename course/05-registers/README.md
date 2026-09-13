# 05. The CPU working registers

**Read this page → edit `src/Gba.Core/Cpu/CpuRegisters.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The GBA ARM7TDMI CPU holds values in registers while it works. R0–R15 each store 32 bits. R13 is normally the stack pointer, R14 the link register, and R15 the program counter. Today store sixteen raw values. Later lessons add mode banking and the special meaning of reading PC; this helper alone is not an accurate PC model. Our learning constructor starts storage at zero as a convenience, not a claim about power-on hardware.

## C# you need now

```csharp
uint[] values = new uint[4];
values[1] = 0xFFFFFFFFu;
uint result = values[1];
```

`uint` holds 0 through 4,294,967,295. A trailing `u` marks an unsigned literal. An array of uint holds separate 32-bit elements. Reuse the field/method pattern from EWRAM. A register number is an index; a register value can be a number, bits, or a guest address.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Create sixteen uint storage slots per CpuRegisters object.
2. Implement Read and Write for register numbers 0–15.
3. Keep objects independent; do not make the backing array static.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- R0 can hold a full 32-bit value.
- R15 is an available storage slot.
- Updating R1 preserves R0.
- Separate CPU objects retain separate values.

<details>
<summary>A hint if you get stuck</summary>

This task resembles RAM, but the element width and number of elements differ. Do not truncate a register to byte.

</details>

Optional detail: [the existing hardware reference](../../docs/03-arm7tdmi/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Deciding whether an ARM instruction runs](../06-conditions/README.md). Press **N** in the launcher when this step is checked.
