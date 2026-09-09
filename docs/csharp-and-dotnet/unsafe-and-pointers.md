# Unsafe code and pointers


This is a host-interop chapter for later. Ordinary managed C# can represent addresses as numbers and memory as arrays; guest addresses are not host pointers.

```csharp
// Language demonstration only; requires AllowUnsafeBlocks to compile.
unsafe
{
    int number = 7;
    int* pointer = &number;
    int copy = *pointer;
}
```

`unsafe` permits pointer operations; it does not disable the GC. `int*` is a pointer to an integer, `&` takes an address here, and unary `*` dereferences a pointer. Those meanings differ from bitwise AND and multiplication because of syntax context.

`fixed` pins movable managed storage for a limited scope so the GC cannot move it while a native call uses its address. A pointer must not escape that scope if the storage can later move. If an API retains the pointer, a short fixed block is insufficient: establish an explicit longer lifetime. [The fixed statement](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/fixed) explains this scope.

Neither project enables unsafe initially. Vulkan bindings may later require it because native functions receive pointers to structures and buffers. Enable it only in Desktop when you reach that milestone, after understanding [native interop](native-interop.md).


## Where this meets the GBA

- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain unsafe contexts, pointers and fixed in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Unsafe code and pointers](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code); look specifically for **Unsafe contexts, pointers and fixed**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Draw the lifetime of a managed array pinned for one native call. Explain what would go wrong if that API retained the pointer. No unsafe code is needed in your emulator yet.

## Definition of done

- You distinguish guest address, managed reference and native pointer.

## Common mistakes

- Casting a GBA address to a host pointer.
- Assuming fixed makes a buffer live forever.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code) — Unsafe contexts, pointers and fixed. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
