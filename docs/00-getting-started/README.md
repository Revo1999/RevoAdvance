# Start here: one small experiment


You will write this emulator yourself. This repository gives you a reading path, empty source locations and criteria for testing each step. No ROM, BIOS, memory bus, CPU interpreter or renderer is included.

## Your first session

1. Read this page, then [integer types](../csharp-and-dotnet/integer-types.md) and [bitwise operations](../csharp-and-dotnet/bitwise-operations.md).
2. Read the short [testing refresher](../csharp-and-dotnet/testing.md).
3. Run the scaffold commands below.
4. Write one test file yourself in `tests/Gba.Core.Tests`: extract the low byte of a generic `uint`, keeping the result as `uint`. Choose zero, an all-low-bits-set value, a value with only bit 8 set, and a mixed hexadecimal value. Predict each result on paper. The refresher teaches the operator; this page deliberately leaves the test and expression to you.
5. Update [your progress log](../../progress/README.md). Then move to the system overview.

## Tools and first build

Use a stable .NET 10 SDK, a text editor or IDE, and Git when you want version history. The scaffold targets `net10.0`. The [project guide](../csharp-and-dotnet/project-structure.md) explains every project setting.

```text
dotnet --info
dotnet restore GbaEmulator.sln
dotnet build GbaEmulator.sln
dotnet run --project src/Gba.Desktop
dotnet test GbaEmulator.sln
```

Run in the repository root. Restore needs access to NuGet the first time. Desktop prints a learning-scaffold message and exits; it does not open a window. Tests initially contain no methods, so a no-tests result is expected. Your first exercise is what turns discovery into an actual pass/fail check.

## Read in small loops

```text
hardware concept → relevant C# tool → your implementation
       ↑                                  ↓
next question ← progress log ← tests and observed behavior
```

Use [ROADMAP](../../ROADMAP.md) for implementation order. Folder numbers organize subjects; they do not mean you must finish all CPU instructions before drawing a pixel. When stuck, reduce the example until you can predict its result without a running emulator.


## C#/.NET concepts used here

- [Projects, assemblies and the .NET CLI](../csharp-and-dotnet/project-structure.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/tools/): Build, run, test and project references.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.

## What you should understand now

- [ ] Where your first test belongs.
- [ ] How the learning loop works.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Write the low-byte exercise described above. Do not begin a memory bus yet.

## Definition of done

- Your own cases are discovered by dotnet test.
- A deliberately wrong expectation fails; restoring the right one passes.
- Your progress log names the next question.

## Common mistakes

- Copying a completed emulator instead of practicing the concept.
- Reading every advanced page before writing the first test.

## Further reading

- [Tonc numbers](https://gbadev.net/tonc/numbers.html) — use binary and hexadecimal explanations; C examples are not C#.
- [Microsoft CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/) — look up build/run/test command arguments.

## Next chapter

[The GBA as an interconnected machine](../01-system-overview/README.md)
