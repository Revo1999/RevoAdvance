# Structs versus classes


A struct is a value type: ordinary assignment copies its fields. A class is a reference type: assignment copies a reference to the same object. Choose based on identity and mutation, not a slogan that structs are always faster.

```csharp
struct Pair { public int X; public int Y; }
class Box { public int Value; }
```

If you assign one `Pair` variable to another, changing the second's X leaves the first alone. If you assign one `Box` reference to another, both see changes to its Value. A struct containing an array copies the **array reference**, not every array element: copying CPU state that way is not a deep save state.

```text
value assignment:      a [X,Y]       b [copied X,Y]
reference assignment:  a ──┐
                          ├──> one Box
                       b ──┘
```

One concrete class for mutable CPU state is a reasonable first design. Small immutable descriptions may fit structs. `readonly struct` means its instance fields cannot be reassigned after construction; it does not deeply freeze referenced arrays. A `record` adds generated equality and printing behavior; a `record class` has reference semantics and a `record struct` has value semantics. Neither is needed initially.

[Classes](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/class) covers shared objects; [records](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record) is optional reading when comparing snapshots.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [PPU](../07-ppu/README.md)

## What you should understand now

- [ ] I can explain value copying versus shared identity in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Structs versus classes](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct); look specifically for **Value copying versus shared identity**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Predict then test assignment of one Pair and one Box. Add an array field to a toy struct and explain why its elements remain shared after copying.

## Definition of done

- You can choose an initial CPU state representation and justify who owns mutations.

## Common mistakes

- Assuming struct means stack allocation.
- Accidentally updating a copied timer value.
- Treating shallow copies as independent save states.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct) — Value copying versus shared identity. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
