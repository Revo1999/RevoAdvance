# Ref and value semantics

## Before the technical details

A method normally receives a copy of the argument value. `ref` instead makes a parameter refer to the caller’s storage. For a reference type, the value normally copied is already an object reference; distinguish those two uses of the word reference. Begin with an integer so only one distinction is involved.

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

### Compare an ordinary parameter with ref

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int number = 4;
ChangeCopy(number);
Console.WriteLine(number);
ChangeOriginal(ref number);
Console.WriteLine(number);

void ChangeCopy(int value) { value++; }
void ChangeOriginal(ref int value) { value++; }
```

Expected output:

```text
4
5
```

The first method increments its local copy and discards it on return. The second aliases `number` itself. `ref` appears at both declaration and call so the effect is visible. These are local functions in a top-level program.

### Try it before implementing

Trace each variable on paper. Then remove `ref` at the call and observe the compiler error before restoring it. Use this understanding to identify accidental state copies, not as a reason to add ref everywhere.

Continue with the detailed lesson below after you can explain your prediction.


Parameters normally receive a copy of their argument's value. For a class, that copied value is a reference: the method can mutate the object but rebinding its local reference does not rebind the caller's variable.

```csharp
static void Increment(ref int number)
{
    number++;
}
```

`ref` aliases caller storage, so this toy method changes the original variable. `in` passes a readonly reference; `out` requires the callee to assign a result before return. Both declaration and call syntax communicate intent where required. A `ref` local aliases existing storage instead of copying it.

Use ordinary parameters first. Passing large structs by `in` can avoid a copy, but non-readonly members can cause defensive copies. Measure before changing signatures. Saving a reference to mutable CPU state is not saving its historical contents.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Timing](../14-timing-and-scheduling/README.md)

## What you should understand now

- [ ] I can explain pass by value, ref, in and out in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Ref and value semantics](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters); look specifically for **Pass by value, ref, in and out**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Compare passing a toy integer by value and by ref. Draw the difference between copying a class reference and passing that variable by ref.

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

- You can predict which caller values change.

## Common mistakes

- Using ref everywhere as an assumed speed improvement.
- Recording references to live state as trace snapshots.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters) — Pass by value, ref, in and out. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
