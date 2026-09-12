# Allocations and garbage collection

## Before the technical details

Allocation creates managed storage, usually with `new`. The garbage collector eventually reclaims objects no longer reachable by the program. Keeping and reusing an array is a design decision about ownership, not just syntax. First distinguish a second reference from a second allocation.

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

### Check whether two variables share an array

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
byte[] first = new byte[4];
byte[] alias = first;
byte[] separate = new byte[4];
Console.WriteLine(ReferenceEquals(first, alias));
Console.WriteLine(ReferenceEquals(first, separate));
```

Expected output:

```text
True
False
```

`ReferenceEquals` asks whether both references point to the same object, not whether their bytes have equal values. There are two array allocations here, not three. The separate arrays start with equal zero values but different identities.

### Try it before implementing

Circle every `new` in a small loop you write and count how often each line runs. Explain who retains each array. Do not add `GC.Collect` as an experiment in frame scheduling; learning allocation ownership comes first.

Continue with the detailed lesson below after you can explain your prediction.


The garbage collector reclaims managed objects that are no longer reachable. Allocation is often cheap, but allocating temporary objects repeatedly adds collection work and can disturb steady audio or frame delivery.

```csharp
byte[] buffer = new byte[256]; // allocate once, then reuse deliberately
```

Do not create a new framebuffer or formatted trace string for every pixel or instruction. Start with clear ownership and reuse stable buffers. A reused buffer can still be wrong if the host reads it while the core overwrites it; allocation reduction does not solve synchronization.

```text
managed: reference → GC-tracked object → collected after unreachable
native:  handle    → driver resource   → explicit API destruction
```

GC manages memory, not the completion of GPU commands. A managed wrapper becoming unreachable does not guarantee prompt native resource release. See [native interop](native-interop.md).


## Where this meets the GBA

- [Timing](../14-timing-and-scheduling/README.md)
- [Audio](../13-audio/README.md)

## What you should understand now

- [ ] I can explain reachability, collection and generations in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Allocations and garbage collection](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals); look specifically for **Reachability, collection and generations**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Identify which operations in a toy loop allocate. Compare the total allocations of allocating a buffer each iteration versus reusing one, without changing outputs.

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

- You can explain an allocation rate and a buffer owner.

## Common mistakes

- Calling GC.Collect every frame.
- Assuming native resources disappear promptly with managed wrappers.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals) — Reachability, collection and generations. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
