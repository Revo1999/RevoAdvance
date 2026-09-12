# Properties and fields

## Before the technical details

A field directly stores a value. A property offers named access through getters and setters, which can control who changes state. You may have used automatic properties already; start by reading the access rules before adding behavior to an accessor.

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

### Let the owner control a change

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Counter counter = new Counter();
counter.AddOne();
Console.WriteLine(counter.Value);

class Counter
{
    public int Value { get; private set; }
    public void AddOne()
    {
        Value++;
    }
}
```

Expected output:

```text
1
```

`get` allows reading. `private set` allows assignment only within the containing type. `void` means the method returns no value. Calling `AddOne` changes the remembered property. Trying `counter.Value = 7` outside the class should produce a compiler access error.

### Try it before implementing

Try the forbidden assignment in your scratchpad and read the first compiler error, then remove it. Explain how a setter differs from a public field before deciding how callers will modify state.

Continue with the detailed lesson below after you can explain your prediction.


A field stores data. A property exposes access through `get` and/or `set`; access can execute code. An auto-property has compiler-generated storage.

```csharp
class Counter
{
    private int count;
    public int Count { get { return count; } }
}
```

The compact equivalent getter is `public int Count => count;`. Here `=>` means an expression-bodied member returning that expression. In a lambda it separates arguments from the function body; context matters. Prefer the longer form until both are readable.

`public` exposes a member to other projects. `internal` limits it to this assembly, and `private` to its containing type. An I/O register is not necessarily a simple settable property: reads can expose current counters, and writes can acknowledge flags or latch a reload value. Keep side-effecting bus operations explicit when that makes intent clearer.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Timers](../09-timers/README.md)

## What you should understand now

- [ ] I can explain accessors and encapsulation in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Properties and fields](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties); look specifically for **Accessors and encapsulation**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Create a toy object with a field and a read-only public property. Explain which caller can modify state and how this would differ from a write-one-to-clear hardware register.

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

- You distinguish storage from the operation exposed to callers.

## Common mistakes

- Assuming every I/O write is assignment.
- Hiding surprising hardware side effects behind ordinary-looking getters.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties) — Accessors and encapsulation. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
