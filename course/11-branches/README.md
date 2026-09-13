# 11. Program flow and the visible PC

**Read this page → edit `src/Gba.Core/Cpu/BranchUnit.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Keep the address being executed separate from the PC value a guest instruction reads. In ordinary ARM operand reads, visible PC is instruction address +8; in Thumb it is +4. ARM B/BL uses a signed 24-bit displacement shifted left two, added to visible PC. BL also saves the following instruction address in LR. BX chooses Thumb when target bit 0 is one, ARM when zero, and aligns the fetch address accordingly. A branch replaces sequential fetch and refills the conceptual pipeline.

## C# you need now

```csharp
int signedField = unchecked((int)(field << 8)) >> 8;
// field contains 24 bits. Shifting through the sign bit extends its sign.
```

Signed and unsigned arithmetic can represent the same bit pattern differently. Use int for a signed displacement and unchecked arithmetic for 32-bit address wrapping. A result record can hold Target, Link, and Thumb. This prevents hidden PC increments in several different helpers.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Add an instruction-address field to your CPU integration and one consistent visible-PC helper.
2. Implement ARM B/BL: decode displacement, optionally write LR, and replace the next fetch address.
3. Implement BX with state exchange and correct target alignment. Keep a sequential path for a failed condition.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- At ARM address 08000000, EA000000 branches to 08000008.
- At the same address, EAFFFFFE branches back to 08000000.
- EB000000 also writes LR=08000004.
- BX to 08000005 selects Thumb and fetches at 08000004; an even target selects ARM and is word-aligned.
- A failed conditional branch continues at instruction address +4.

<details>
<summary>A hint if you get stuck</summary>

A branch target is based on the visible PC, not simply the next instruction. Do not increment PC again after replacing the fetch address.

</details>

Optional detail: [the existing hardware reference](../../docs/03-arm7tdmi/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Moving values between registers and memory](../12-loads-stores/README.md). Press **N** in the launcher when this step is checked.
