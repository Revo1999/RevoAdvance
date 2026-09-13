# Your everyday coding workflow

**For the whole learning course, use `learn.cmd` and [the current course](../../course/README.md).** It remembers your lesson, prepares starters and checks, and reruns checks on save. The `dev.cmd` shortcuts below remain optional controls for general development.

Open the RevoAdvance folder in your editor. Double-click `dev.cmd` to choose an action, or open the editor's terminal in this folder and use the commands below. No per-terminal SDK setup is needed for the launcher.

## While writing the emulator

1. Write C# in `src/Gba.Core`, for example in its `Cpu` or `Memory` folder. Create `.cs` files directly in the editor; they are included automatically.
2. Write checks for that code in `tests/Gba.Core.Tests`. The test project already has xUnit and a reference to Core.
3. Run `.\dev.cmd watch` once. Save your edits; your tests rebuild and rerun. Read the results in the terminal. Stop with `Ctrl+C`.

To check just one class, use `.\dev.cmd watch -Filter LowByteTests`, replacing the class name with your own. To run every test once, use `.\dev.cmd test`. Check the number of executed tests: zero tests or no matching tests does not verify your code. The initial scaffold contains no tests.

To launch the app, use `.\dev.cmd run`. It builds automatically before starting. For now it prints a placeholder message and exits. As you implement the host, this same command will launch what you have written. Use `.\dev.cmd build` if you only want to check compilation across all projects.

When you implement ROM argument handling, `.\dev.cmd run -Rom "C:\Games\Your Game.gba"` passes that path to the app. The launcher does not implement loading or emulation for you.

## Trying a lesson's C# example

Run `.\dev.cmd lab`. It creates the scratchpad only if needed, preserving an existing project. Edit `.work/SyntaxLab/Program.cs`, paste one complete console example, save, and run `.\dev.cmd lab` again. Or use `.\dev.cmd lab-watch` to rerun on save. This scratchpad is ignored by Git; put emulator code in Core so it is part of your project.

## Translating commands in older lessons

You can skip their terminal PATH setup when using the launcher. Their code examples and expected results still apply.

| Lesson command | Shortcut |
| --- | --- |
| `dotnet restore ...` then `dotnet build GbaEmulator.sln` | `.\dev.cmd build` |
| `dotnet run --project src/Gba.Desktop...` | `.\dev.cmd run` |
| `dotnet test tests/Gba.Core.Tests...` | `.\dev.cmd test` |
| Same test command with `--filter "FullyQualifiedName~SomeTests"` | `.\dev.cmd test -Filter SomeTests` |
| Create/run `.work/SyntaxLab` | `.\dev.cmd lab` |

The separate optional `.work/TestLab` xUnit tutorial still uses its documented commands; `test` always targets your emulator tests. You can write your own learning tests directly in `tests/Gba.Core.Tests` to use the launcher. Test discovery lists and Release performance experiments remain available through the manual guide.

## Editor buttons and troubleshooting

In VS Code, open **Terminal → Run Task** and choose an Emulator task or **C# scratchpad: run**. **Ctrl+Shift+B** builds. Compiler errors link to your source files. In other editors, use the terminal or the double-click menu.

If compilation fails, open the first relevant filename and line in the error, fix it, save, and rerun. A failed assertion means the test ran and disagreed with its expectation. If package restore fails, resolve the reported connection/package error and rerun the same command.

`.\dev.cmd doctor` checks SDK selection. The launcher first tries `.work/dotnet10/dotnet.exe`, then an installed `dotnet` on PATH. A compatible stable .NET 10 SDK is required; if missing, the launcher shows the official download address. Install the SDK, reopen your terminal, and retry. First-time package restore needs network access.

All project paths are resolved relative to the launcher, so moving the repository does not require editing scripts. From another directory, invoke the launcher's full path. `global.json` keeps SDK selection on stable .NET 10. The launcher only changes its own process environment and its child processes. It does not install tools or edit your C# files. Command failures return a nonzero exit code to the editor.

The launcher is Windows-specific and uses built-in Windows PowerShell. All build logic lives in `tools/dev.ps1`; `dev.cmd` and the VS Code tasks invoke that same script. You do not need to maintain separate build configurations.
