# Enums and named states


An enum gives meaningful names to numeric alternatives. It improves readability without adding a dispatch framework.

```csharp
enum Direction { North, East, South, West }
Direction facing = Direction.East;
```

Members default to consecutive integers starting at zero. Hardware fields often use nonconsecutive encodings; assign explicit numbers after consulting the hardware table. A cast can produce an enum value that has no named member, so it does not validate an opcode.

`[Flags]` is an attribute indicating a combinable set of named bits. It does not assign powers of two for you or enforce legal combinations. A CPU mode is a choice; interrupt sources are a set of bits. Model that difference deliberately.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Keypad](../11-input/README.md)

## What you should understand now

- [ ] I can explain named constants and underlying integral types in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Enums and named states](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum); look specifically for **Named constants and underlying integral types**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Define a generic choice enum and a generic flags enum. Explain why OR-ing two choices differs from OR-ing two independent flags.

## Definition of done

- Names map unambiguously to intended numeric values.

## Common mistakes

- Assuming enum casts validate input.
- Combining mutually exclusive CPU modes as flags.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum) — Named constants and underlying integral types. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
