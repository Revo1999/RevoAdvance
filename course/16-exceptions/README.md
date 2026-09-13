# 16. Banked registers and entering an exception

**Read this page → edit `src/Gba.Core/Cpu/ExceptionUnit.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

CPU modes select different physical register banks. User/System share R0–R14; IRQ, Supervisor, Abort, and Undefined bank R13/R14; FIQ banks R8–R14. Each exception mode has an SPSR. Exception entry saves CPSR, selects the mode, stores an exception-specific LR, clears T for ARM state, applies interrupt masks, and fetches from a vector. SWI uses vector 08, IRQ 18, undefined instruction 04. For SWI, LR is the following instruction address. IRQ LR must support the architectural return sequence, not simply copy the visible PC.

## C# you need now

```csharp
public enum CpuMode { User = 0x10, Irq = 0x12, Supervisor = 0x13 }
// This example names three modes; your complete model adds the others.
```

An enum gives names to numeric mode bits. Store banks in separate arrays/fields; selecting a bank changes which storage is visible. Save a uint status value by value. Do not alias current CPSR with a mutable saved-status object. Keep host NotImplementedException diagnostics separate from guest CPU exceptions.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Extend CpuRegisters with mode selection and banked storage without changing the existing raw-register API for ordinary access.
2. Implement SWI entry first, then IRQ and undefined entry with a deliberate internal instruction-address convention.
3. Implement exception-return status restoration and bank selection. Add Thumb SWI and test both ARM/Thumb return state.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Switch User → IRQ → User: shared R0 survives, each mode retains its own SP/LR.
- FIQ has a different R8; User/System share theirs.
- ARM SWI at address A saves return A+4; Thumb SWI saves A+2, and both enter ARM Supervisor at 08.
- Saved status restores Thumb state and the prior mode on return.
- For IRQ, verify the return target using the intended SUBS PC,LR,#4 sequence.

<details>
<summary>A hint if you get stuck</summary>

Banking does not clear registers. Model entry as a sequence and record old state before changing modes.

</details>

Optional detail: [the existing hardware reference](../../docs/03-arm7tdmi/exceptions.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Turning a GBA color into a pixel](../17-first-pixel/README.md). Press **N** in the launcher when this step is checked.
