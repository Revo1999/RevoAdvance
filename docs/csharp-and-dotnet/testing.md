# Testing with xUnit v2

## Before the technical details

Use the console warm-up to learn comparison, then the complete xUnit example below to learn test discovery. A C# test file is not a terminal command or an executable entry point. xUnit calls methods marked with its attributes. Do not add a `Main` to a test class.

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

### Name the three parts of a check

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int items = 3; // Arrange
int costEach = 4;
int actual = items * costEach; // Act
int expected = 12; // independently calculated
Console.WriteLine(actual == expected); // rehearsal for Assert

```

Expected output:

```text
True
```

An assertion makes a mismatch fail a test; this console rehearsal only prints a Boolean. Keeping the expected value literal makes its independent origin visible. A passing check of multiplication does not prove any emulator operation.

### Try it before implementing

After reading the xUnit example below, type your own small test file in `tests/Gba.Core.Tests`, then run `dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj`. Read the discovered test count. Deliberately make one expectation wrong, observe failure, then restore it.

Continue with the detailed lesson below after you can explain your prediction.


The scaffold selects xUnit v2 with the VSTest adapter and Microsoft.NET.Test.Sdk. It deliberately starts with **zero test methods**. A successful build or empty discovery result is not emulator correctness.

## A complete Fact example (test project only)

This complete file belongs in a test project, not the console scratchpad. To practice independently, create `.work/TestLab`, copy the repository test project's package references, implicit-using and test settings into a new `.csproj` there, and omit its Core project reference. Target `net10.0`; use the same xUnit v2 versions as the repository. This avoids accidentally mixing a newer template's test framework into this lesson. Alternatively, type a practice file in `tests/Gba.Core.Tests` and replace it with your own meaningful cases afterward.

For the independent route, create a folder named `TestLab` under `.work`. Create `.work/TestLab/TestLab.csproj` with the following complete contents. These versions match the current repository scaffold:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsTestProject>true</IsTestProject>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.5.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.3" />
  </ItemGroup>
</Project>
```

XML tags enclose settings. `TargetFramework` chooses .NET 10; `PackageReference` names a dependency and its version. xUnit supplies the attributes and assertions, its adapter connects discovery to the runner, and the test SDK supplies test infrastructure. This file configures tools; it contains no C# methods. Save the next C# block as `BasketExamples.cs` in that same folder. No `Program.cs` is needed.

```csharp
using Xunit;

public class BasketExamples
{
    [Fact]
    public void TwoBasketsContainFiveApples()
    {
        int firstBasket = 2; // Arrange
        int secondBasket = 3;
        int actual = firstBasket + secondBasket; // Act
        Assert.Equal(5, actual); // Assert
    }
}
```

Run `dotnet test .work/TestLab` if you chose the independent project, or `dotnet test tests/Gba.Core.Tests` for the repository project. With only this example, expect one discovered, passing test. Change the expected five to six: expect one failed test showing the mismatch. Restore five. These are practice instructions; this repository still supplies no test source for you.

`public class` declares the container xUnit discovers. `[Fact]` marks a method as one test. `public void` makes it accessible and gives it no return value. `Assert.Equal` takes the expected value first, actual value second. You do not call the test method from `Main`: the runner calls it.

## A complete Theory example (test project only)

Save the next block as `.work/TestLab/ArithmeticExamples.cs` using the same setup. If you chose the repository test project instead, save it as `tests/Gba.Core.Tests/ArithmeticExamples.cs`. Each InlineData row runs the method with different arguments; with just this file expect two passing cases. If both example files are present, expect three cases in total. Edit an existing file instead of creating a duplicate class.

```csharp
using Xunit;

public class ArithmeticExamples
{
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(0, 4, 4)]
    public void AdditionHasExpectedResult(int left, int right, int expected)
    {
        // Arrange: the input values are supplied above.
        int actual = left + right; // Act
        Assert.Equal(expected, actual); // Assert
    }
}
```

Attributes in square brackets attach metadata. `[Fact]` marks one test without supplied data; `[Theory]` runs a parameterized test; `[InlineData]` supplies one case. A public class and method allow test discovery. An assertion compares actual behavior with an independently chosen expectation. This language example teaches the testing tool, not an emulator operation.

After saving the Theory file, run from the repository-root PowerShell terminal:

```powershell
dotnet test .work/TestLab/TestLab.csproj --filter "FullyQualifiedName~ArithmeticExamples" --logger "console;verbosity=normal"
```

Expect two executed, passing cases. If you used the repository test project, replace `.work/TestLab/TestLab.csproj` in that command with `tests/Gba.Core.Tests/Gba.Core.Tests.csproj`. After each input or expectation edit, save and rerun the same command. A filter that finds zero cases is not a pass.

Read [xUnit v2 getting started](https://xunit.net/docs/getting-started/v2/getting-started) for this scaffold's framework version. Do not mix v3 runner configuration into this project casually. Keep tests deterministic: fixed input, reproducible initial state and no real wall-clock waits.


## Where this meets the GBA

- [Testing](../16-testing/README.md)
- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)

## What you should understand now

- [ ] I can explain test projects, assertions and parameterized tests in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Testing with xUnit v2](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test); look specifically for **Test projects, assertions and parameterized tests**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Write your first test file yourself: given a uint, check the low byte as a uint. Choose 0, 0xFF, 0x100 and 0x1234ABCD; calculate expected results on paper.

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

- dotnet test discovers your cases and they pass.
- Deliberately changing one expected value makes a test fail; undo that change afterward.

## Common mistakes

- Treating a test that never runs as a pass.
- Deriving expected values using the same expression as the implementation.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test) — Test projects, assertions and parameterized tests. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
