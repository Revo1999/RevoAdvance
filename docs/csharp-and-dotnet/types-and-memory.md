# Types and memory

## Before the technical details

A type tells the compiler which values and operations are allowed. `var` still selects one fixed type at compile time. Nullable notation describes whether an absent value is allowed; it does not create an object. These are language questions you can learn with names and numbers before applying them to memory.

## Syntax warm-up

### Open PowerShell and prepare this lesson

Open a PowerShell terminal (an IDE terminal is fine). Run this block once in each new terminal. The path below is your current checkout; if you move the repository, change that first path. All later commands on this page run from this folder, not from the lesson folder.

```powershell
Set-Location "C:\Users\victo\Desktop\RevoAdvance"
if (Test-Path ".work/dotnet10/dotnet.exe") {
    $env:PATH = "$PWD\.work\dotnet10;$env:PATH"
}
dotnet --version
```

Expect a version beginning with `10.`. The conditional uses the local SDK when present and changes PATH only for this terminal. If the command is missing or shows `8.`, complete the [.NET 10 setup](../00-getting-started/before-you-code.md#set-up-and-know-what-success-looks-like) before continuing.

Create the console scratchpad only if it does not already exist:

```powershell
if (-not (Test-Path ".work/SyntaxLab/SyntaxLab.csproj")) {
    dotnet new console --framework net10.0 --output .work/SyntaxLab
}
```

If it already exists, no output from that block is expected. Keep using that project; do not create another project for each example. [Command troubleshooting](../00-getting-started/running-and-testing.md) explains errors and the difference between running and testing.

Each example below is a complete, independent console program. Run one at a time in [SyntaxLab](../00-getting-started/before-you-code.md#a-separate-place-to-try-the-examples). These toy examples teach C#; the emulator implementation remains your exercise.

### Handle an absent reference explicitly

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
string? title = null;
string displayed = title ?? "untitled";
Console.WriteLine(displayed);
var count = 3;
Console.WriteLine(count.GetType().Name);
```

Expected output:

```text
untitled
Int32
```

`string?` allows a null string reference. `null` means no object is referenced. `??` chooses the right-hand fallback when the left side is null. The compiler infers `count` as `int`; `var` does not permit assigning a string to it later.

### Try it before implementing

Set `title` to an empty string, then to `"Map"`, and predict how the fallback changes. Distinguish empty text from no reference. Revisit this distinction when reporting missing files or optional metadata.

Continue with the detailed lesson below after you can explain your prediction.


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

## Run and check your practice

Write your toy practice in `.work/SyntaxLab/Program.cs`, save, and run from the repository-root terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare your result with a prediction written before running; your own exercise values may differ from the worked example. Save and rerun this same command after each edit. This runs a console program, not xUnit.

For an exercise that asks for assertions or parameterized tests, use the [TestLab setup and complete test-file examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only). Put your own public test class in `.work/TestLab/PracticeTests.cs`; save it, then run:

```powershell
dotnet test .work/TestLab/TestLab.csproj --list-tests
dotnet test .work/TestLab/TestLab.csproj --logger "console;verbosity=normal"
```

The list must contain your methods, and the run must report actual executed cases with zero failures. If only the supplied generic Fact/Theory examples are present, expect three cases; adding your own increases that count. If no cases are discovered, check the public class/method and `[Fact]`/`[Theory]` attributes. After each edit, save and rerun the second command. For a reading-only part of the task, answer its questions on paper; no new test is needed for that part.

## Definition of done

- You distinguish a type, a variable, an object and a reference.

## Common mistakes

- Confusing `var` with dynamic typing.
- Assuming a managed object models every hardware rule automatically.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/) — Value types, reference types and type safety. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
