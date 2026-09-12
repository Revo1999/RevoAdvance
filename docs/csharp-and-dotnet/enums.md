# Enums and named states

## Before the technical details

An enum lets code use a meaningful name instead of an unexplained number. Some enums describe one choice; flags describe a combination of independent choices. Practice both, and do not assume converting a number to an enum validates it.

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

### Name independent options

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Options chosen = Options.Read | Options.Write;
Console.WriteLine((int)chosen);
Console.WriteLine((chosen & Options.Read) != Options.None);

[Flags]
enum Options
{
    None = 0,
    Read = 1,
    Write = 2
}
```

Expected output:

```text
3
True
```

`[Flags]` is metadata describing intended combinations. The values one and two select separate bits; OR combines them. AND checks whether the Read bit is present. The attribute does not pick those values for you and cannot prevent invalid combinations.

### Try it before implementing

Add an Execute option with a separate bit. Predict the numeric result of combining Read and Execute. Compare this with a mutually exclusive direction choice: north/east/south/west is a different modeling problem.

Continue with the detailed lesson below after you can explain your prediction.


An enum gives meaningful names to numeric alternatives. It improves readability without adding a dispatch framework.

```csharp
enum Direction { North, East, South, West }
Direction facing = Direction.East;
```

Members default to consecutive integers starting at zero. Hardware fields often use nonconsecutive encodings; assign explicit numbers after consulting the hardware table. A cast can produce an enum value that has no named member, so it does not validate an opcode.

`[Flags]` is an attribute indicating a combinable set of named bits. It does not assign powers of two for you or enforce legal combinations. A CPU mode is a choice; interrupt sources are a set of bits. Model that difference deliberately.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Keypad](../11-input/README.md)

## What you should understand now

- [ ] I can explain named constants and underlying integral types in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Enums and named states](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum); look specifically for **Named constants and underlying integral types**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Define a generic choice enum and a generic flags enum. Explain why OR-ing two choices differs from OR-ing two independent flags.

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

- Names map unambiguously to intended numeric values.

## Common mistakes

- Assuming enum casts validate input.
- Combining mutually exclusive CPU modes as flags.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum) — Named constants and underlying integral types. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
