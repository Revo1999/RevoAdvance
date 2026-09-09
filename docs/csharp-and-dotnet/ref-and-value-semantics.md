# Ref and value semantics


Parameters normally receive a copy of their argument's value. For a class, that copied value is a reference: the method can mutate the object but rebinding its local reference does not rebind the caller's variable.

```csharp
static void Increment(ref int number)
{
    number++;
}
```

`ref` aliases caller storage, so this toy method changes the original variable. `in` passes a readonly reference; `out` requires the callee to assign a result before return. Both declaration and call syntax communicate intent where required. A `ref` local aliases existing storage instead of copying it.

Use ordinary parameters first. Passing large structs by `in` can avoid a copy, but non-readonly members can cause defensive copies. Measure before changing signatures. Saving a reference to mutable CPU state is not saving its historical contents.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Timing](../14-timing-and-scheduling/README.md)

## What you should understand now

- [ ] I can explain pass by value, ref, in and out in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Ref and value semantics](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters); look specifically for **Pass by value, ref, in and out**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Compare passing a toy integer by value and by ref. Draw the difference between copying a class reference and passing that variable by ref.

## Definition of done

- You can predict which caller values change.

## Common mistakes

- Using ref everywhere as an assumed speed improvement.
- Recording references to live state as trace snapshots.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters) — Pass by value, ref, in and out. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
