# 07. Reading fields from an ARM instruction

**Read this page → edit `src/Gba.Core/Cpu/ArmFields.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

An instruction is a number containing smaller fields. For an already-identified ARM data-processing instruction: opcode is bits 24–21, Rn bits 19–16, Rd bits 15–12, and bit 20 requests flag updates. Today extract only those fields. Identifying instruction families is a separate decision: multiply and other special encodings overlap broad data-processing patterns.

## C# you need now

```csharp
uint packed = 0x00000AB0;
int field = (int)((packed >> 4) & 0xFF);
```

Move the field down until its lowest bit is at position zero, then mask away everything above its width. Eight bits use mask 0xFF; four bits use 0xF. Return a bool for a single flag. These static methods need no object because their output depends only on the supplied word.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Extract opcode, Rn, and Rd with shifts and masks.
2. Extract the S bit as a Boolean.
3. Keep decoding separate from changing register values.

## Check it

The launcher runs **3 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- 0xE2813005 identifies ADD (opcode 4), Rn=1, Rd=3, S=false.
- 0xE3B02007 identifies MOV (opcode 13), Rd=2, S=true.
- Different condition bits do not contaminate operand fields.

<details>
<summary>A hint if you get stuck</summary>

Write the bit positions above the word on paper. Use one mask per field rather than comparing the whole instruction.

</details>

Optional detail: [the existing hardware reference](../../docs/04-arm-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Executing MOV, ADD, and SUB](../08-first-arm/README.md). Press **N** in the launcher when this step is checked.
