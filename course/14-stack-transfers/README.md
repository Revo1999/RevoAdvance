# 14. Stacks and transferring several registers

**Read this page → edit `src/Gba.Core/Cpu/BlockTransfer.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A stack is RAM used through R13/SP. ARM LDM/STM transfer a register list in ascending register-number order to ascending memory addresses; IA/IB/DA/DB select the starting address and final base update. Thumb PUSH uses a descending full stack and POP restores from it. Thumb PUSH/POP has low-register bits 0–7 and an optional LR/PC bit. Start with ordinary registers and nonempty lists; user-bank transfers, PC effects, and empty-list quirks are explicit later cases.

## C# you need now

```csharp
for (int i = 0; i < 8; i++)
{
    bool selected = (mask & (1 << i)) != 0;
    // Process one selected item.
}
```

A bitmask represents a set without a List allocation. Count selected registers before choosing a starting address. Keep temporary transfer addresses separate from the visible base register so writes cannot disturb later transfers. You can reuse bus width methods and register access.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement STMIA/LDMIA for nonempty lists with base outside the list.
2. Add the other address modes and explicit writeback; route transfers through the bus in order.
3. Connect Thumb PUSH/POP to this behavior, including LR saving and PC restoration, then extend low-register Thumb loads/stores.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- STMIA r0!,{r1,r2} writes r1 at old R0 and r2 at old R0+4, then advances R0 by 8.
- PUSH {r0,r1} with SP=02000100 writes r0 at 020000F8 and r1 at 020000FC; SP becomes 020000F8.
- POP restores both values and the old SP.
- No transfer happens when an ARM condition fails.
- Give base-in-list, empty-list, and PC cases their own fixtures before calling those forms supported.

<details>
<summary>A hint if you get stuck</summary>

Stack order is not the same as repeatedly pushing registers in ascending order. Compute the final layout first.

</details>

Optional detail: [the existing hardware reference](../../docs/05-thumb-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Completing CPU families one at a time](../15-more-cpu/README.md). Press **N** in the launcher when this step is checked.
