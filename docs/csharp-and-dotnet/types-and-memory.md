# Types and memory


A type determines which values and operations a variable permits. C# is statically typed: the compiler checks those operations before execution. `var count = 3;` infers `int`; it does not mean dynamically typed.

```csharp
int count = 3;
var sameKind = 3; // also int
string? label = null;
```

`string?` marks a reference that may be null, meaning it currently refers to no object. Nullable analysis helps find missing initialization; it is not a runtime substitute for ownership rules. A value type holds a value; a reference variable identifies an object. Where bytes physically live depends on context and runtime optimization, not just the keyword `struct`.

Managed memory is tracked by .NET. Native memory belongs to an external allocator or API and needs its own lifetime rules. [Runtime](runtime.md) explains the execution model; [structs versus classes](structs-vs-classes.md) explains assignment in more detail.


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)

## What you should understand now

- [ ] I can explain value types, reference types and type safety in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Types and memory](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/); look specifically for **Value types, reference types and type safety**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Explain the type and initial value of three toy variables. Draw which variables refer to shared data before choosing how to represent hardware state.

## Definition of done

- You distinguish a type, a variable, an object and a reference.

## Common mistakes

- Confusing `var` with dynamic typing.
- Assuming a managed object models every hardware rule automatically.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/) — Value types, reference types and type safety. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
