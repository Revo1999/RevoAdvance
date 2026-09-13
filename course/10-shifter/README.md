# 10. Shifts, rotations, and ARM operands

**Read this page → edit `src/Gba.Core/Cpu/BarrelShifter.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

ARM can shift operand 2 before the main operation. LSL inserts zeros on the right, LSR inserts zeros on the left, ASR repeats the sign bit, and ROR rotates bits around. Also return the last bit shifted out as carry. For register-specified shifts use the low eight bits of the amount; zero preserves value and carry. Handle amounts 32 and above explicitly: C# masks shift counts and does not implement ARM boundary rules for you.

For immediate shifts, encoded zero means LSL #0, LSR #32, ASR #32, or RRX (for ROR). RRX moves old carry into bit 31 and bit 0 into carry. A rotated immediate takes an 8-bit literal and rotates right by twice its 4-bit rotation field; zero rotation preserves carry.

## C# you need now

```csharp
int signed = unchecked((int)bits);
int shifted = signed >> 3;
// bits is a uint. Signed right shift extends the sign bit.
```

Return both value and carry in a small record struct, like ArithmeticResult. An enum can name Lsl/Lsr/Asr/Ror. Use distinct methods or an explicit parameter for immediate versus register amounts: encoded zero has different meanings.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Start with LSL/LSR for amounts 1–31 and return the carry-out bit.
2. Add ASR/ROR and explicit 0/32/>32 cases for register shifts. Add immediate zero special cases and RRX.
3. Extend ARM execution to rotated immediates and register operand 2; use shifter carry for logical flag-setting operations.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- LSL(0x80000001,1) gives 2 and carry=true.
- LSR #32 of 0x80000000 gives 0 and carry=true; a register amount of 0 preserves old carry.
- ASR(0x80000000,32) gives FFFFFFFF and carry=true.
- RRX of 2 with carry=true gives 80000001 and carry=false.
- Rotating 0x80 right by 8 gives 80000000; rotating by zero preserves carry.

<details>
<summary>A hint if you get stuck</summary>

For LSL #32, carry is original bit 0; for LSR #32 it is bit 31. Beyond 32 both give zero value and zero carry. ASR at 32 or more repeats the sign. Nonzero ROR multiples of 32 preserve value but report bit 31 as carry.

</details>

Optional detail: [the existing hardware reference](../../docs/04-arm-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Program flow and the visible PC](../11-branches/README.md). Press **N** in the launcher when this step is checked.
