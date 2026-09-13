# 19. Remembering interrupt requests

**Read this page → edit `src/Gba.Core/Interrupts/InterruptController.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Devices request attention by setting bits in IF. IE selects which requests are enabled; IME is the master switch; CPSR.I masks CPU IRQ acceptance. A masked request stays pending. Writing ones to IF acknowledges only those bits; zeros leave other requests alone. Today implement the latch and decision, not exception entry. Connect the decision to ExceptionUnit only after these checks pass.

## C# you need now

```csharp
bits |= selected;
bits &= ~selected;
// First set selected bits; then clear only those selected bits.
```

`|=` and `&=` update a variable with bitwise operations. `~` complements all bits of an integer, so mask to the register width where needed. Public auto-properties can hold IE and IME; IF should be changed only through Request/Acknowledge. The starter uses descriptive property names instead of abbreviations.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement Request and Acknowledge for source bits 0–13.
2. Implement ShouldTakeIrq from pending & enabled sources, master enable, and the CPU mask.
3. Keep a request pending when any gate is closed.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- Requesting bits 0 and 3 retains both.
- Acknowledging bit 0 leaves bit 3 pending.
- All gates must allow a request before IRQ is accepted.
- Masking does not erase pending requests.

<details>
<summary>A hint if you get stuck</summary>

IF is not an ordinary assignment register. A write value of zero must not clear everything.

</details>

Optional detail: [the existing hardware reference](../../docs/08-interrupts/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [One timer that reloads on overflow](../20-timers/README.md). Press **N** in the launcher when this step is checked.
