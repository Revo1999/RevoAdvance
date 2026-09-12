# C# and .NET, only when you need them

Start with [the tools and practice-project guide](../00-getting-started/before-you-code.md), then [integer types](integer-types.md), [bitwise operations](bitwise-operations.md), [testing](testing.md) and [project structure](project-structure.md). Return to hardware after the small exercise. Each refresher now opens with a complete warm-up, its expected output, a syntax walkthrough and something to try yourself. You can revisit these pages whenever a line in a hardware lesson is unfamiliar.

## A manageable first route

For exact terminal commands and error explanations, use [Exactly how to run and test](../00-getting-started/running-and-testing.md). Every lesson repeats the console setup and tells you how to run its practice; xUnit exercises include a separate test-project command.

Read numbers → bits → a test → arrays. After that, read classes/properties/enums when you need to represent state, and switch when you need to choose behavior. Methods, top-level statements, assignments and Boolean comparisons are introduced in [Start here](../00-getting-started/README.md). You do not need pointers, MemoryMarshal, native interop or performance tuning to complete your first memory exercise.

The complete console warm-ups replace the whole scratchpad `Program.cs`. Older short snippets in the detailed explanations can be fragments, so read their surrounding context. The xUnit examples are explicitly labeled for a test project. When syntax feels unfamiliar, say what each type, operator and method call does before relating it to hardware.

## Reading map

For opening your own games and preserving progress, use [files, paths and persistence](file-io.md). It pairs with the [loading](../12-cartridges-and-roms/loading-and-playing.md) and [saving](../12-cartridges-and-roms/saving-and-resuming.md) lessons.

| Concept | Read when | Level |
| --- | --- | --- |
| [Integer types, binary and hexadecimal](integer-types.md) | Memory map, Bus and memory, CPU state, ARM decoding | Foundation |
| [Bitwise operations: a mini-course](bitwise-operations.md) | CPU state, ARM decoding, Memory map, Bus and memory | Foundation |
| [Arrays, spans and byte order](arrays-and-spans.md) | Memory map, Bus and memory, PPU, Audio | Foundation |
| [Structs versus classes](structs-vs-classes.md) | CPU state, ARM decoding, PPU | Foundation |
| [Types and memory](types-and-memory.md) | Memory map, Bus and memory, CPU state, ARM decoding | Foundation |
| [Enums and named states](enums.md) | CPU state, ARM decoding, Keypad | Foundation |
| [Properties and fields](properties-and-fields.md) | CPU state, ARM decoding, Timers | Foundation |
| [Switch statements and pattern matching](switch-and-pattern-matching.md) | CPU state, ARM decoding | Foundation |
| [Ref and value semantics](ref-and-value-semantics.md) | CPU state, ARM decoding, Timing | Later / interop or profiling |
| [Unsafe code and pointers](unsafe-and-pointers.md) | Vulkan output | Later / interop or profiling |
| [MemoryMarshal: optional advanced views](memorymarshal.md) | Memory map, Bus and memory, Vulkan output | Later / interop or profiling |
| [Allocations and garbage collection](allocations-and-gc.md) | Timing, Audio | Foundation |
| [Host exceptions and guest exceptions](exceptions.md) | CPU state, ARM decoding, Cartridges | Foundation |
| [Testing with xUnit v2](testing.md) | Testing, Memory map, Bus and memory | Foundation |
| [Performance without premature optimization](performance.md) | Timing, Vulkan output | Later / interop or profiling |
| [Native interop and resource lifetime](native-interop.md) | Vulkan output | Later / interop or profiling |
| [Projects, assemblies and the .NET CLI](project-structure.md) | Getting started, System overview | Foundation |
| [How C# becomes machine code](runtime.md) | Timing, Vulkan output | Foundation |

## Syntax lookup

| Syntax | Meaning and first explanation |
| --- | --- |
| `var`, `T?` | inferred static type / nullable reference: [types](types-and-memory.md) |
| `=>` | expression body: [properties](properties-and-fields.md); arm mapping: [switch](switch-and-pattern-matching.md) |
| `switch`, patterns, `_` | choose statements/values: [switch](switch-and-pattern-matching.md) |
| `<T>`, spans, ranges `..` | typed views and exclusive ends: [arrays](arrays-and-spans.md) |
| `ref`, `in`, `out` | parameter/storage semantics: [ref](ref-and-value-semantics.md) |
| `readonly`, `record` | mutation limits / generated value-oriented members: [structs/classes](structs-vs-classes.md) |
| `stackalloc` | temporary stack storage: [performance](performance.md) |
| `unsafe`, `fixed`, pointers | native address/lifetime operations: [unsafe](unsafe-and-pointers.md) |
| `nint`, `nuint`, `using`, IDisposable | host-width values and cleanup: [interop](native-interop.md) |
| `[Fact]`, `[Theory]`, `[InlineData]` | test metadata: [testing](testing.md) |

Generic examples teach language features only. They are not complete emulator components. Modern Microsoft pages may show features newer than this project's compiler; the explanations here avoid preview syntax.

## What you should understand now

- [ ] I know which concept my current hardware exercise needs.

## C#/.NET refresher

Each row above leads to a local explanation with a specific Microsoft reference and reading target.

## Your implementation task

Choose one refresher exercise, predict its result, then write it yourself.

## Definition of done

You can explain the result and apply the concept in the linked hardware chapter.

## Common mistakes

- Reading advanced optimization pages as prerequisites to the first memory read.
- Copying examples without predicting their behavior.

## Further reading

[Microsoft C# documentation](https://learn.microsoft.com/en-us/dotnet/csharp/) and [language reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/) are lookup tools, not required cover-to-cover reading.

## Next chapter

[Return to the roadmap](../../ROADMAP.md).
