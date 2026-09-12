# Host exceptions and guest exceptions

## Before the technical details

A host exception reports that a .NET operation could not complete normally. Catch a failure where you can make a useful decision about it. A guest CPU exception is a modeled hardware transition; it is not a reason to throw a C# exception. Practice control flow using a deliberately rejected ordinary input.

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

### Trace throw, catch and finally

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
try
{
    CheckCount(-1);
    Console.WriteLine("accepted");
}
catch (ArgumentOutOfRangeException)
{
    Console.WriteLine("invalid count");
}
finally
{
    Console.WriteLine("finished check");
}

void CheckCount(int count)
{
    if (count < 0)
    {
        throw new ArgumentOutOfRangeException(nameof(count));
    }
}
```

Expected output:

```text
invalid count
finished check
```

`throw` leaves the normal path, so “accepted” is not printed. This catch handles the named exception type. `finally` executes when leaving the block in this example. `nameof(count)` produces the parameter name as text.

### Try it before implementing

Change the argument to zero and predict the output. List a missing host file, an invalid method argument and a guest IRQ, then decide which belong in this language mechanism and which belong in emulated state.

Continue with the detailed lesson below after you can explain your prediction.


A .NET exception interrupts normal host control flow. `throw` raises it; `try` encloses an operation; `catch` handles selected failures; `finally` runs cleanup when leaving the block. A missing ROM file is a host failure. A guest SWI or IRQ is modeled CPU state and control flow, not a .NET exception.

```csharp
if (count < 0)
{
    throw new ArgumentOutOfRangeException(nameof(count));
}
```

This generic snippet assumes an integer `count` parameter. `nameof(count)` produces the text "count" while staying tied to the symbol. Fail clearly for developer mistakes. Define deliberate development behavior for unimplemented guest operations; do not silently catch everything and continue with fabricated data.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)
- [Cartridges](../12-cartridges-and-roms/README.md)

## What you should understand now

- [ ] I can explain throw, try, catch and finally in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Host exceptions and guest exceptions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/); look specifically for **Throw, try, catch and finally**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

List three host failures and three guest events, deciding which should use .NET exceptions.

## Check this lesson's exercise

This implementation task is a written explanation or diagram; no new emulator code or test file is required here. Finish the paper task and compare it with the definition of done below. To repeat the **safe console warm-up**, save its code in `.work/SyntaxLab/Program.cs` and run from the prepared repository-root terminal:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the output shown above. The advanced fragments are explanatory and may need additional setup; they are not required runnable exercises. Do not treat a successful console run as evidence for a hardware implementation.

## Definition of done

- Invalid host input and emulated exception entry have separate handling.

## Common mistakes

- Implementing IRQ delivery with throw/catch.
- Swallowing an array bounds exception as a memory-bus policy.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/) — Throw, try, catch and finally. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
