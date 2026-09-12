# Files, paths and persistence

## Before the technical details

File I/O moves data between memory and persistent storage. A path is a name; a byte array is data; a stream offers read/write operations over a source or destination. First practice stream position in memory, where you cannot overwrite a game save. Disk operations add paths and failure handling afterward.

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

### Write and reread a byte in a memory stream

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
using System.IO;

using MemoryStream stream = new MemoryStream();
stream.WriteByte(42);
Console.WriteLine(stream.Position);
stream.Position = 0;
Console.WriteLine(stream.ReadByte());
Console.WriteLine(stream.ReadByte());
```

Expected output:

```text
1
42
-1
```

Writing advances the position. Setting it to zero rewinds. `ReadByte` returns an `int` so it can represent every byte plus -1 for end of stream. `using` here is a declaration that disposes at the end of its scope. No file is created; memory contents alone do not survive process exit.

### Try it before implementing

Write two bytes in the scratch stream and predict all positions and reads. For the disk exercise below, choose a new disposable directory and binary File methods yourself; test again in a fresh process rather than only rereading the same memory.

Continue with the detailed lesson below after you can explain your prediction.

Read this when implementing [ROM loading](../12-cartridges-and-roms/loading-and-playing.md) or [game saves](../12-cartridges-and-roms/saving-and-resuming.md). File I/O belongs in Desktop; Core models the bytes and hardware behavior.

A path names a file location. Relative paths depend on the current working directory, which may differ between an IDE and a packaged app. Use `Path` operations to construct paths rather than concatenating separator characters. Constructing a path does not create a directory or establish that a file exists.

```csharp
using System.IO;

string folder = "practice";
string location = Path.Combine(folder, "sample.dat");
```

`using System.IO;` imports names. A static method such as `Path.Combine` is called on the type without constructing an instance. This generic example only builds a path; it reads or writes nothing.

ROM and save files are binary, not text. `File` offers operations that read or write whole byte arrays, while streams support incremental access. Prefer the simplest bounded operation suited to your first exercise. Inspect file size before allocating for untrusted/incorrect input, and still handle failure during the actual operation.

A stream is a resource: dispose it when finished using the lifetime rules in [native interop](native-interop.md), which also explains the resource form of `using`. Disk I/O can fail because a path is missing, permissions deny access or storage is unavailable. Catch appropriate failures at the host boundary; do not report success when data was not persisted.

For a save snapshot, decide who owns the buffer while it is being written. Assignment of `byte[]` copies a reference, not the bytes. Start with controlled synchronous I/O; introduce background operations only after learning their lifetime and synchronization requirements. Keep disk work outside the CPU's instruction loop.

## What you should understand now

- [ ] Paths, in-memory bytes and persistent files are different objects/concepts.
- [ ] Binary data should not pass through text encoding operations.
- [ ] A filesystem operation can fail even after an earlier existence check.

## C#/.NET refresher

- [Arrays and spans](arrays-and-spans.md) — byte storage and copying.
- [Exceptions](exceptions.md) — host failure handling.
- [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file) — look for byte-array reads/writes, overwrite behavior and documented exceptions.
- [Microsoft Path](https://learn.microsoft.com/en-us/dotnet/api/system.io.path) — look for Combine and full versus relative paths.

## Your implementation task

Write a few synthetic bytes to a new file in a disposable practice directory, then read them back in a separate run and compare with expectations chosen on paper. Never use your real game saves for this exercise. Choose the methods yourself.

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

The same bytes survive a fresh process; a path containing spaces works; a deliberately invalid destination produces a clear failure rather than a false success message.

## Common mistakes

- Assuming the working directory is always the executable directory.
- Overwriting a real save while practicing file operations.
- Assuming a reference copy freezes a save snapshot.

## Further reading

[Microsoft file and stream I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/) — read the file/stream distinction and binary versus text sections; the older platform-specific sections are not needed here.

## Next chapter

[Load a .gba file](../12-cartridges-and-roms/loading-and-playing.md), then [save and resume](../12-cartridges-and-roms/saving-and-resuming.md).
