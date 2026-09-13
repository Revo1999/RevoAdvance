# 20. One timer that reloads on overflow

**Read this page → edit `src/Gba.Core/Timers/GbaTimer.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A GBA timer has a 16-bit live counter and a separate reload value. Writing reload while running does not immediately replace the live counter. A disabled→enabled transition loads reload; overflow loads it again. The divisors are 1, 64, 256, 1024. First implement one non-cascade timer with divisor fixed for each enable period. Advance returns the number of overflows so other hardware can react later. Preserve a partial divisor across calls.

## C# you need now

```csharp
public ushort Reload { get; set; }
// An auto-property stores a value. More complex transitions belong in a method.
```

`ushort` wraps at 16 bits, but use a wider intermediate to count overflows rather than losing them through a cast. A while loop can process repeated overflow events in a first implementation. Separate host method calls from emulated elapsed cycles.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Implement SetEnabled so only a rising enable edge loads Reload. Do not tick while disabled.
2. Accumulate cycles, consume full divisor ticks, and retain the remainder.
3. On each overflow reload the counter and count an event. Later connect four timers, cascade inputs, and IRQ requests.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- Enabling loads Reload.
- With divisor 64, calls of 63 then 1 advance exactly one tick.
- Reload FFFE and five ticks produce two overflows and counter FFFF.
- A reload write while enabled waits until overflow; disabling stops advancement.

<details>
<summary>A hint if you get stuck</summary>

Avoid resetting the prescaler remainder every time Advance returns. Multiple timer overflows may happen in one call.

</details>

Optional detail: [the existing hardware reference](../../docs/09-timers/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Copying through the bus with DMA](../21-dma/README.md). Press **N** in the launcher when this step is checked.
