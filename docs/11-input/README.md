# Keypad: host buttons become guest bits


## In the real GBA

KEYINPUT at 0x04000130 reports ten active-low button bits: 0 means pressed. KEYCNT at 0x04000132 selects keys and configures an optional keypad interrupt with OR/AND matching. Button order is A, B, Select, Start, Right, Left, Up, Down, R, L in bits 0–9.

## In our emulator

Desktop samples physical keyboard/gamepad state and supplies a logical button snapshot to Core. Core models KEYINPUT and keypad IRQ behavior. Input is an external stimulus; tests inject it deterministically instead of requiring a real keyboard. Document at which guest boundary a new host snapshot becomes visible and clear host-held keys on focus loss.

```text
keyboard / gamepad → Desktop mapping → logical buttons
                                           ↓
                         Core KEYINPUT / KEYCNT → IRQ request
```

Timing initially samples at a known frame or scheduler boundary; later record guest timestamps for replay. Host key repeat is not repeated hardware button presses.

## In C#

Enums can name independent button bits. Bitwise operations invert or combine the specified field width. Keep reserved read bits consistent with the hardware documentation, rather than blindly complementing an entire int.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Enums and named states](../csharp-and-dotnet/enums.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum): Named constants and underlying integral types.

## What you should understand now

- [ ] Host mapping and emulated keypad logic have different owners.
- [ ] Active-low bits need an explicit width.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement input-state injection and test no buttons, one button, two buttons and KEYCNT matching. Then map one host key after the host milestone exists.

## Definition of done

- Unpressed/pressed states use the correct polarity.
- AND and OR matching differ in tests.
- A deterministic input sequence can be replayed.

## Common mistakes

- Using 1 for pressed directly in KEYINPUT.
- Leaking desktop key codes into Core.
- Forgetting C# complement operates over the promoted width.

## Further reading

- [Tonc keypad](https://gbadev.net/tonc/keys.html) — active-low input and combinations.
- [GBATEK keypad](https://mgba-emu.github.io/gbatek/#gbakeypadinput) — KEYCNT and interrupt details.

## Next chapter

[Cartridges, BIOS and persistent data](../12-cartridges-and-roms/README.md)
