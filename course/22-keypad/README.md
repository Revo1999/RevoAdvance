# 22. Pressed buttons become zero bits

**Read this page → edit `src/Gba.Core/Input/Keypad.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

KEYINPUT has ten active-low bits: zero means pressed. Bit order is A, B, Select, Start, Right, Left, Up, Down, R, L. Thus no buttons is 03FF; A alone is 03FE. Your input method accepts an active-high mask for convenience: one means the host says pressed. Convert it to the guest register without touching unrelated bits. KEYCNT interrupt matching and physical keyboard mapping come after this helper.

## C# you need now

```csharp
ushort masked = (ushort)(value & 0x03FF);
// The cast returns the masked result to a 16-bit type.
```

Bitwise complement `~` acts on the promoted integer width, so retain only the ten keypad bits afterward. A stateful object can remember the latest pressed mask. Do not query a real keyboard in Core: pass logical button state in from the host.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Store a logical pressed mask through SetPressed.
2. Implement ReadInput to expose only the ten active-low bits.
3. Keep each Keypad object independent; later add KEYCNT OR/AND match and an injected IRQ request.

## Check it

The launcher runs **4 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- No buttons reads 03FF.
- A pressed reads 03FE.
- A+Start reads 03F6; releasing A leaves 03F7.
- Bits above bit 9 in the host mask are ignored.

<details>
<summary>A hint if you get stuck</summary>

For the guest, pressing clears a bit. For your host-facing input, pressing sets a bit. Name the two representations clearly.

</details>

Optional detail: [the existing hardware reference](../../docs/11-input/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Connecting components to one guest clock](../23-machine-time/README.md). Press **N** in the launcher when this step is checked.
