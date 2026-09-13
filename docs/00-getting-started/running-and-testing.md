# Exactly how to run and test your work

**Prefer the [everyday workflow](daily-workflow.md):** `.\dev.cmd run`, `.\dev.cmd test`, `.\dev.cmd watch`, and `.\dev.cmd lab` handle the setup and project paths below. Double-click `dev.cmd` for a menu. This page documents the underlying commands for optional troubleshooting and special cases; you do not need to memorize them.

Commands go in **PowerShell**, C# goes in `.cs` files, and project XML goes in `.csproj` files. Save a file before running its command. A command uses the version on disk, not unsaved text in your editor.

## Start every new terminal here

Open your editor's terminal or Windows PowerShell. Copy this block into it:

```powershell
Set-Location "C:\Users\victo\Desktop\RevoAdvance"
if (Test-Path ".work/dotnet10/dotnet.exe") {
    $env:PATH = "$PWD\.work\dotnet10;$env:PATH"
}
dotnet --version
```

The first line selects your current repository folder. Change it if you move or clone the repository elsewhere. The conditional selects the validation SDK in this checkout when available; this affects only the current terminal. Expect `10.x.xxx`. If dotnet is missing or reports an older SDK, follow [setup](before-you-code.md#set-up-and-know-what-success-looks-like). A fresh clone does not include the ignored local SDK.

All commands below and in the lessons assume you remain in this repository-root terminal. The `--project` or project-file argument selects the project without changing folders. You do not need to enter `src`, `tests` or `docs` first.

## Run a console warm-up

Once, create the scratchpad if it is missing:

```powershell
if (-not (Test-Path ".work/SyntaxLab/SyntaxLab.csproj")) {
    dotnet new console --framework net10.0 --output .work/SyntaxLab
}
```

Open `.work/SyntaxLab/Program.cs` in your editor. Replace all its contents with **one** complete console example from a lesson and save. Run:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the lesson's “Expected output,” possibly preceded by build messages. To try the next example, replace the file contents, save and run exactly the same command again. To change an input, edit it, predict the result, save and rerun. Do not combine two complete examples in one file.

## Run the generic xUnit practice

Follow the [complete TestLab setup](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) to create `.work/TestLab/TestLab.csproj` and the practice `.cs` files. If those files already exist, edit them rather than making duplicate classes. The console project above cannot discover xUnit tests.

After saving the test file, run each command separately:

```powershell
dotnet test .work/TestLab/TestLab.csproj --list-tests
dotnet test .work/TestLab/TestLab.csproj --logger "console;verbosity=normal"
```

The first lists discovered methods/cases; the second executes them and prints results. With only `BasketExamples` expect one case; with only `ArithmeticExamples` expect two; with both expect three. Restore and build happen automatically when needed.

To run just the basket class:

```powershell
dotnet test .work/TestLab/TestLab.csproj --filter "FullyQualifiedName~BasketExamples" --logger "console;verbosity=normal"
```

The quoted filter means “test names containing BasketExamples.” Expect one executed case, not zero. Change the expected five to six in the basket assertion, save and run the filtered command: it should fail. Restore five, save and rerun: it should pass. A deliberately wrong expectation is a learning check, not a change to keep.

## Run your own emulator tests

Write your own test files under `tests/Gba.Core.Tests`, using the public class names suggested by the current lesson. Write emulator behavior under `src/Gba.Core`. The project reference already lets the test project use Core's public types; add a `using` for the namespace you choose, or use the fully qualified type name. Do not copy a Core class into the test project just to make its name visible.

After saving all files, run:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --logger "console;verbosity=normal"
```

Build should succeed and your saved test methods must appear in the list. The run should execute your cases with zero failures. The untouched scaffold contains no tests. A no-tests result does **not** satisfy a lesson's definition of done. Each hardware lesson supplies an exact filter for its suggested test class; run that while iterating, then run the full Core test command above before finishing.

For example, after writing a public `LowByteTests` class yourself:

```powershell
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~LowByteTests" --logger "console;verbosity=normal"
```

The class name is a naming instruction for your own file, not a claim that a completed test is supplied. The filter cannot create a missing test. Test counts grow as you implement cases; record the actual count rather than expecting a fixed total for the whole emulator.

## Build and run the desktop host

Run:

```powershell
dotnet build GbaEmulator.sln
dotnet run --project src/Gba.Desktop/Gba.Desktop.csproj
```

Initially expect the scaffold message followed by the terminal prompt. There is no window or emulator yet. Later, expect only the host behavior you have implemented. A running window may keep the terminal occupied until you close it; `Ctrl+C` requests termination of a console process, but use orderly app close for save-persistence checks.

After you implement argument-based ROM loading, pass your own file like this:

```powershell
dotnet run --project src/Gba.Desktop/Gba.Desktop.csproj -- "C:\Games\Your Game.gba"
```

Replace the example path and keep the quotes. The `--` passes subsequent arguments to your app. This command cannot add ROM support to the placeholder host. Follow the loading/saving lessons for their manual acceptance steps.

## Understand the result before continuing

| What you see | What to do |
| --- | --- |
| `dotnet` is not recognized or `NETSDK1045` | Run the terminal setup above and confirm a .NET 10 SDK is selected |
| Project/solution file not found | Run `Get-Location` and `Get-ChildItem`; return to the folder containing `GbaEmulator.sln` |
| NuGet/restore error | Resolve the reported network/package error, then rerun the same command; tests have not executed yet |
| C# compiler error with file and line | Fix the first relevant error in that file, save and rerun |
| `Xunit` or `Fact` cannot be found | Use the configured test project, not SyntaxLab, and include `using Xunit;` |
| Duplicate class or top-level statement error | Keep one complete console example per file; do not create duplicate test classes |
| No tests available or no matching tests | Check file location, public test class/method, attributes and filter spelling; use `--list-tests` |
| Failed assertion | Read expected versus actual, investigate the behavior, save the correction and rerun; do not change expectations just to hide a bug |
| Passed with one or more cases | Those cases passed; run the full project before finishing the lesson |
| Old-looking output | Save the file, check the selected project, and rerun without `--no-build` |

For performance experiments only, run the saved console program in Release mode:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj -c Release
```

Expect the same correct numeric result as Debug, but do not expect identical elapsed times. Ordinary correctness tests should not depend on a guessed wall-clock duration.

[Return to the first session](README.md) or [choose a lesson](../README.md).
