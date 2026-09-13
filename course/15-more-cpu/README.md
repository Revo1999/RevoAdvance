# 15. Completing CPU families one at a time

**Read this page → edit `src/Gba.Core/Cpu/CpuDispatch.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Your decoder now needs precise family matching. Check special patterns before broad data-processing patterns. For ARM, complete logical operations AND/EOR/ORR/BIC/MVN and tests TST/TEQ/CMP/CMN, then ADC/SBC/RSB/RSC, multiply/long multiply, swap, and status transfers. For Thumb, reuse the same arithmetic and bus behavior for ALU, high-register, SP/PC-relative, conditional branch, and two-halfword BL forms. This lesson is a repeated small loop: choose ONE row below, implement it, check it, then take the next. It is not a request to finish the CPU in one sitting.

| Next family | Observable change |
| --- | --- |
| Logical/test | Result or flags; test operations do not write Rd |
| Carry arithmetic | Includes carry-in or inverted borrow-in |
| Multiply | Low or long product, optionally accumulated |
| Swap | Exchange register value with bus memory |
| Status | Masked CPSR/SPSR reads/writes respecting privilege |
| Thumb remaining forms | Same registers/bus, narrower encodings |

## C# you need now

```csharp
bool matches = (word & fixedBitsMask) == expectedPattern;
// Only fixed encoding bits belong in fixedBitsMask.
```

Give each family its own small method instead of one enormous switch body. Use ulong for unsigned long products and long for signed long products. A delegate such as Action<uint> can name a handler, but a simple ordered if/switch dispatcher is enough. Unsupported encodings should report the word and PC.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. For the next family, write its fixed-bit mask, operands, changed state, and one hand-computed before/after example beside its handler. Use the linked instruction reference for exact encodings.
2. Implement and check that family only. For test operations preserve Rd; for status writes preserve unselected fields.
3. Repeat the table, then add collision fixtures proving multiply/swap/status words cannot enter ordinary data-processing handlers.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- AND of F0 and 3C gives 30; TST changes flags without replacing a register.
- ADC(FFFFFFFF,0,C=1) gives 0 with carry; SBC(5,2,C=0) gives 2.
- Unsigned long multiplication FFFFFFFF × 2 gives high=1, low=FFFFFFFE.
- A swap writes the old register value and returns the old memory value.
- Thumb BL keeps the first-half intermediate state until the second half and returns a Thumb-state link address.
- Each implemented family has a passing example and boundary case; unsupported families remain named diagnostics, never silent no-ops.

<details>
<summary>A hint if you get stuck</summary>

This is the point where an exact opcode table is useful. Ask for a single family’s mask, starter signature, and checks if stuck; the handler logic is still yours.

</details>

Optional detail: [the existing hardware reference](../../docs/04-arm-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

The runner now retires the early “unsupported opcode” rejection check so you can add those instructions. Existing positive arithmetic/condition checks still run.

Next: [Banked registers and entering an exception](../16-exceptions/README.md). Press **N** in the launcher when this step is checked.
