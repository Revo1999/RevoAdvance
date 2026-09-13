# 09. Carry and signed overflow

**Read this page → edit `src/Gba.Core/Cpu/Arithmetic.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The low 32 result bits do not tell the whole story. N is result bit 31; Z means the result is zero; C means an addition carried beyond bit 31, or a subtraction needed no borrow. V means the mathematical signed result does not fit in a signed 32-bit integer. Add and subtract should return result and NZCV together. Here Flags contains only bits 31–28; later the CPU merges them into CPSR while preserving other bits.

## C# you need now

```csharp
ulong wide = (ulong)left + right;
uint low = unchecked((uint)wide);
// left and right are uint values supplied by the caller.
```

`ulong` is a 64-bit unsigned integer, so an intermediate can retain carry. Casting an unsigned bit pattern to int inside unchecked interprets it as signed; a long intermediate can measure signed overflow. The supplied record struct groups two return values. Construct one with `new ArithmeticResult(value, flags)`; it is data, not a second CPU.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement Add returning the wrapped value plus N/Z/C/V.
2. Implement Subtract with C meaning no borrow.
3. Keep flags outside NZCV clear in this helper. Later extend the same reasoning to ADC, SBC, RSB, and RSC.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- FFFFFFFF + 1 → value 0, flags Z+C.
- 7FFFFFFF + 1 → 80000000, flags N+V.
- 0 − 1 → FFFFFFFF, N set and C clear.
- 80000000 − 1 → 7FFFFFFF, C+V set.

<details>
<summary>A hint if you get stuck</summary>

Carry answers an unsigned question. Overflow answers a signed question. Test them separately instead of assuming they always match.

</details>

Optional detail: [the existing hardware reference](../../docs/03-arm7tdmi/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Shifts, rotations, and ARM operands](../10-shifter/README.md). Press **N** in the launcher when this step is checked.
