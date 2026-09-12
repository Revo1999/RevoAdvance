# Structs versus classes

## Before the technical details

Choose a struct when copying its values expresses what you mean; choose a class when several callers should share one identity. Neither choice automatically makes a program fast. Test the copying behavior first with one integer field.

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

### Compare value and reference assignment in one run

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Point a = new Point { X = 2 };
Point b = a;
b.X = 9;
Box first = new Box { Value = 2 };
Box second = first;
second.Value = 9;
Console.WriteLine(a.X);
Console.WriteLine(first.Value);

struct Point { public int X; }
class Box { public int Value; }
```

Expected output:

```text
2
9
```

`new Point { X = 2 }` uses an object initializer: it creates a value and sets a member. Copying that struct copies its integer. Copying `first` copies a reference to a shared box. Keep type declarations after the top-level statements in a complete console file.

### Try it before implementing

Draw the objects/values and arrows after each assignment. Then add an array field to a toy struct yourself and predict whether copying that struct also copies the array elements.

Continue with the detailed lesson below after you can explain your prediction.


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

- You can choose an initial CPU state representation and justify who owns mutations.

## Common mistakes

- Assuming struct means stack allocation.
- Accidentally updating a copied timer value.
- Treating shallow copies as independent save states.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct) — Value copying versus shared identity. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
