# 08. Executing MOV, ADD, and SUB

**Read this page → edit `src/Gba.Core/Cpu/ArmImmediate.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

MOV copies a value, ADD adds to a source register, and SUB subtracts from it. Begin with valid ARM immediate data-processing words whose rotation is zero, S=0, and operands are R0–R14. Evaluate the condition first. Opcode 13 is MOV, 4 is ADD, and 2 is SUB. The immediate value here is bits 7–0. Full rotated immediates, PC writes, flag updates, and timing are deliberately later work.

## C# you need now

```csharp
uint total = unchecked(0xFFFFFFFFu + 1u);
// total is 0: only the low 32 bits are retained.
```

`unchecked` states that overflow wraps to the width of the integer. Reuse the field extractor and register object you already wrote. A switch statement can choose the arithmetic operation. Method calls such as `registers.Read(index)` retrieve existing component state; do not create a new register bank during execution.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Use Conditions.Matches to decide whether the instruction executes.
2. Decode fields and implement MOV, ADD, and SUB using the existing registers.
3. For a passing condition, throw NotSupportedException on any other opcode in this limited helper. Leave unrelated registers unchanged.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- MOV r0,#7 stores 7.
- MOV, ADD, SUB sequence produces r0=7, r1=12, r2=10.
- A failing EQ condition makes no register change.
- Unsupported opcode 0 is reported, not silently treated as MOV.

<details>
<summary>A hint if you get stuck</summary>

The first argument to Execute is the encoded word, not an opcode number. Read Rn before writing Rd because they may name the same register.

</details>

Optional detail: [the existing hardware reference](../../docs/04-arm-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Carry and signed overflow](../09-arithmetic-flags/README.md). Press **N** in the launcher when this step is checked.
