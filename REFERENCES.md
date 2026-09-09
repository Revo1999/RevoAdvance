# Curated references

External URLs were checked during repository creation; see [the verification record](docs/VALIDATION.md). Hardware rules in local chapters are simplified explanations with scope limits, not replacements for the full references.

# GBA / hardware references

## ARM7TDMI technical reference manual

**PRIMARY / HARDWARE REFERENCE** — [ARM7TDMI technical reference manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819). The CPU designer’s reference for the programmer model, exceptions, pipeline and instruction cycle timing. Use before CPU state and instruction implementation. This manual covers a specific core revision; combine it with GBA-specific evidence.
Relevant chapter: [ARM7TDMI before opcodes](docs/03-arm7tdmi/README.md).

## GBATEK (mGBA-hosted mirror)

**HARDWARE REFERENCE / COMMUNITY RECONSTRUCTION** — [GBATEK (mGBA-hosted mirror)](https://mgba-emu.github.io/gbatek/). Detailed community hardware register and behavior reference, not an official Nintendo specification. Use as a lookup at every subsystem milestone. Read GBA and ARMv4T sections, not DS/3DS sections.
Relevant chapter: [Memory map: addresses are routes](docs/02-memory-map/README.md).

## Tonc

**TUTORIAL / EXPLANATION** — [Tonc](https://gbadev.net/tonc/). A GBA programming tutorial explaining how software uses the hardware. Use for memory, graphics and peripheral mental models; its C/assembly examples are reference material, not code to port wholesale.
Relevant chapter: [PPU: turning video data into a picture](docs/07-ppu/README.md).

## mGBA test suite

**TEST RESOURCE** — [mGBA test suite](https://github.com/mgba-emu/suite). Focused GBA diagnostics. Use after documenting the selected test’s CPU, BIOS and output prerequisites; record revision/build details.
Relevant chapter: [Evidence before game compatibility](docs/16-testing/README.md).

## gba-tests

**TEST RESOURCE** — [gba-tests](https://github.com/jsmolka/gba-tests). Additional diagnostic programs for cross-checking hardware behavior. Use after isolated subsystem tests; read each test’s requirements and license.
Relevant chapter: [Evidence before game compatibility](docs/16-testing/README.md).

# C# / .NET / host references

## Official reference entry points

- [C# documentation](https://learn.microsoft.com/en-us/dotnet/csharp/) — language guide; use when a local explanation needs more context.
- [C# language reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/) — precise syntax/semantics; use for a particular operator or construct.
- [.NET documentation](https://learn.microsoft.com/en-us/dotnet/) — runtime and library map; use when locating a platform API.
- [.NET CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/) — command arguments; use while working with projects.

## Contextual Microsoft references

### Integer types, binary and hexadecimal

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types). Look for ranges, literals and signedness.
Use when working on [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md), [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md). Read [the local explanation](docs/csharp-and-dotnet/integer-types.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Bitwise operations: a mini-course

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators). Look for and, or, xor, complement and shift behavior.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md). Read [the local explanation](docs/csharp-and-dotnet/bitwise-operations.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Arrays, spans and byte order

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays). Look for zero-based indexing and array reference semantics.
Use when working on [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md), [PPU](docs/07-ppu/README.md), [Audio](docs/13-audio/README.md). Read [the local explanation](docs/csharp-and-dotnet/arrays-and-spans.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Structs versus classes

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct). Look for value copying versus shared identity.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [PPU](docs/07-ppu/README.md). Read [the local explanation](docs/csharp-and-dotnet/structs-vs-classes.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Types and memory

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/). Look for value types, reference types and type safety.
Use when working on [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md), [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md). Read [the local explanation](docs/csharp-and-dotnet/types-and-memory.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Enums and named states

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum). Look for named constants and underlying integral types.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [Keypad](docs/11-input/README.md). Read [the local explanation](docs/csharp-and-dotnet/enums.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Properties and fields

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties). Look for accessors and encapsulation.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [Timers](docs/09-timers/README.md). Read [the local explanation](docs/csharp-and-dotnet/properties-and-fields.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Switch statements and pattern matching

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression). Look for arms, ordering and exhaustive handling.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md). Read [the local explanation](docs/csharp-and-dotnet/switch-and-pattern-matching.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Ref and value semantics

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters). Look for pass by value, ref, in and out.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [Timing](docs/14-timing-and-scheduling/README.md). Read [the local explanation](docs/csharp-and-dotnet/ref-and-value-semantics.md) first.
Optional advanced reading: wait for a measured need or host interoperability.

### Unsafe code and pointers

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code). Look for unsafe contexts, pointers and fixed.
Use when working on [Vulkan output](docs/15-vulkan-output/README.md). Read [the local explanation](docs/csharp-and-dotnet/unsafe-and-pointers.md) first.
Optional advanced reading: wait for a measured need or host interoperability.

### MemoryMarshal: optional advanced views

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.memorymarshal). Look for casts, layout and reference restrictions.
Use when working on [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md), [Vulkan output](docs/15-vulkan-output/README.md). Read [the local explanation](docs/csharp-and-dotnet/memorymarshal.md) first.
Optional advanced reading: wait for a measured need or host interoperability.

### Allocations and garbage collection

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals). Look for reachability, collection and generations.
Use when working on [Timing](docs/14-timing-and-scheduling/README.md), [Audio](docs/13-audio/README.md). Read [the local explanation](docs/csharp-and-dotnet/allocations-and-gc.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Host exceptions and guest exceptions

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/). Look for throw, try, catch and finally.
Use when working on [CPU state](docs/03-arm7tdmi/README.md), [ARM decoding](docs/04-arm-instruction-set/README.md), [Cartridges](docs/12-cartridges-and-roms/README.md). Read [the local explanation](docs/csharp-and-dotnet/exceptions.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Testing with xUnit v2

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test). Look for test projects, assertions and parameterized tests.
Use when working on [Testing](docs/16-testing/README.md), [Memory map](docs/02-memory-map/README.md), [Bus and memory](docs/06-bus-and-memory/README.md). Read [the local explanation](docs/csharp-and-dotnet/testing.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Performance without premature optimization

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/). Look for profiling cpu use and allocation.
Use when working on [Timing](docs/14-timing-and-scheduling/README.md), [Vulkan output](docs/15-vulkan-output/README.md). Read [the local explanation](docs/csharp-and-dotnet/performance.md) first.
Optional advanced reading: wait for a measured need or host interoperability.

### Native interop and resource lifetime

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/). Look for marshalling, abi and native ownership.
Use when working on [Vulkan output](docs/15-vulkan-output/README.md). Read [the local explanation](docs/csharp-and-dotnet/native-interop.md) first.
Optional advanced reading: wait for a measured need or host interoperability.

### Projects, assemblies and the .NET CLI

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/tools/). Look for build, run, test and project references.
Use when working on [Getting started](docs/00-getting-started/README.md), [System overview](docs/01-system-overview/README.md). Read [the local explanation](docs/csharp-and-dotnet/project-structure.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### How C# becomes machine code

**C# / .NET REFERENCE** — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process). Look for il, jit compilation and runtime services.
Use when working on [Timing](docs/14-timing-and-scheduling/README.md), [Vulkan output](docs/15-vulkan-output/README.md). Read [the local explanation](docs/csharp-and-dotnet/runtime.md) first.
This is a foundation topic; use the small local exercise before returning to hardware.

### Span<T>

**C# / .NET REFERENCE** — [Span<T>](https://learn.microsoft.com/en-us/dotnet/api/system.span-1). Bounded temporary contiguous views. Read after ordinary arrays, for memory/PPU/audio buffers.

### Memory<T>

**C# / .NET REFERENCE** — [Memory<T>](https://learn.microsoft.com/en-us/dotnet/api/system.memory-1). Storable memory views and lifetime distinctions. Read if data must outlive a local span.

### BinaryPrimitives

**C# / .NET REFERENCE** — [BinaryPrimitives](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.binary.binaryprimitives). Explicit endian reads/writes. Read during memory-width tests.

### Classes

**C# / .NET REFERENCE** — [Classes](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/class). Reference-type declaration and inheritance semantics. Read alongside state ownership; no hierarchy is required.

### Patterns

**C# / .NET REFERENCE** — [Patterns](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/patterns). Pattern syntax and ordering. Read only as needed for small decoding mappings.

### fixed

**C# / .NET REFERENCE** — [fixed](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/fixed). Pinning scope and movable managed data. Read before native calls requiring pointers.

### Dispose

**C# / .NET REFERENCE** — [Dispose](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose). Deterministic cleanup. Read before owning native host resources.

### NativeAOT

**C# / .NET REFERENCE** — [NativeAOT](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/). Ahead-of-time deployment and restrictions. Optional after the normal runtime is correct and measured.

## Host technologies

- **C# / .NET REFERENCE** — [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file), [Path](https://learn.microsoft.com/en-us/dotnet/api/system.io.path), and [file/stream I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/): use for binary ROM loading and save persistence, after the [local file I/O refresher](docs/csharp-and-dotnet/file-io.md). Read the chosen methods' overwrite behavior and exceptions before writing saves.

- **HOST TECHNOLOGY / PRIMARY** — [Khronos Vulkan documentation](https://docs.vulkan.org/): API and guide index. Read at the host milestone for resource/synchronization contracts.
- **HOST TECHNOLOGY / TUTORIAL** — [Khronos tutorial](https://docs.vulkan.org/tutorial/latest/00_Introduction.html): window-to-swapchain learning path. Its C++ examples explain native concepts; this project’s code remains C#.
- **HOST TECHNOLOGY** — [Silk.NET documentation](https://dotnet.github.io/Silk.NET/docs/): managed bindings and package guidance. Use after the local interop refresher, before selecting stable packages.
- **HOST TECHNOLOGY** — [Silk.NET backend notes](https://dotnet.github.io/Silk.NET/docs/hlu/troubleshooting/): GLFW versus SDL backend distinctions. Use to preserve the no-SDL constraint.
- **TEST FRAMEWORK** — [xUnit v2 getting started](https://xunit.net/docs/getting-started/v2/getting-started): Fact/Theory, discovery and runner setup for this scaffold. Use during your first test.

Return to [the roadmap](ROADMAP.md) after answering your current question.
