# Switch statements and pattern matching

## Before the technical details

A switch chooses a path or value based on an input. Patterns describe what should match; they are not calls to methods named after each case. Start with the statement form you may recognize, then compare the expression form below.

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

### Follow the statement form

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int choice = 2;
switch (choice)
{
    case 1:
        Console.WriteLine("small");
        break;
    case 2:
        Console.WriteLine("large");
        break;
    default:
        Console.WriteLine("unknown");
        break;
}
```

Expected output:

```text
large
```

`case` labels the matching alternative. `break` exits this switch. `default` handles values not matched above. An expression form instead computes a value and uses `=>` between pattern and result. Neither form automatically validates an instruction encoding.

### Try it before implementing

Try inputs one, two and ninety-nine, then rewrite this toy choice as a switch expression yourself. Read ordering carefully when patterns overlap; the first matching arm matters.

Continue with the detailed lesson below after you can explain your prediction.


A traditional switch chooses statements to execute. A switch expression computes a value. Start with statements when decoding involves several checks and effects; use expressions for small pure mappings.

```csharp
int size = 2;
string label;
switch (size)
{
    case 1: label = "small"; break;
    default: label = "other"; break;
}
string compact = size switch
{
    1 => "small",
    _ => "other"
};
```

In the expression, `=>` separates a pattern from its resulting value; `_` matches anything left over. Arms are considered in order. Pattern matching tests a value's shape or condition; a guard such as `when size > 0` adds a Boolean condition. Do not use clever patterns to conceal an instruction's mask and match rule.

ARM families overlap in their broad bit patterns. A readable table of masks and required values, with specific families considered before general ones, is more useful than a giant unexplained switch. Illegal and unimplemented instructions need distinguishable outcomes in your development tools.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)

## What you should understand now

- [ ] I can explain arms, ordering and exhaustive handling in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Switch statements and pattern matching](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression); look specifically for **Arms, ordering and exhaustive handling**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Write both switch styles for a generic numeric label mapping. Decide how an unexpected input should be reported. Do not implement an opcode decoder yet.

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

- You can translate between the two forms and explain fallback ordering.

## Common mistakes

- Treating the first broad match as sufficient for every ARM encoding.
- Confusing a switch arm arrow with an assignment.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression) — Arms, ordering and exhaustive handling. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
