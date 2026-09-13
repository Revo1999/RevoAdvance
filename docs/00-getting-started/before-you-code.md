# Before you code: a friendly starting point

**You can leave tool setup to the launcher.** Double-click `dev.cmd` in the repository root, or use the [everyday workflow](daily-workflow.md). The explanations and manual setup below are optional background; you do not need to learn project management tools before writing emulator code.

Some C# experience is enough to begin. You do not need to know electronics, assembly, graphics programming or native libraries first. Learn one piece of hardware and one small piece of syntax at a time. The first goal is to understand a number in a test, not to boot a game.

## What are we actually building?

An emulator is a program that reproduces another machine's observable behavior. Your C# program runs on your PC (the **host**). The machine it represents is the GBA (the **guest**). A guest instruction is a number stored in a ROM; your eventual interpreter will inspect that number and update guest state. The PC does not directly run GBA instructions as C#.

**State** means everything you need to remember between steps: numbers, bytes, settings and pending work. **Behavior** means how that state changes in response to something. Start by writing “before → action → after” on paper. Timing later adds “when.”

## The stack, in ordinary language

| Name | What it does here | When you need it |
| --- | --- | --- |
| C# | The language you write; begin with variables, methods and arrays | Now |
| .NET SDK | Tools that compile, run and test C#; includes a runtime | Now; this repository targets .NET 10 |
| Terminal / PowerShell | A place to type commands; these commands are not C# | Now |
| Git / GitHub | Local change history / a remote place to share the repository | To review and synchronize work |
| Solution (`.sln`) | Groups the projects | To build everything together |
| Project (`.csproj`) | Lists the target and dependencies of one build unit | To understand Core, Desktop and Tests |
| NuGet | Downloads libraries named by a project | Restore uses it for the test tools |
| xUnit | Runs small methods that check expected results | Your first exercise |
| ARM / Thumb | Instruction encodings understood by the guest CPU | CPU lessons; not new languages you must write the app in |
| Vulkan | Sends completed images to the host GPU | Much later, after a synthetic image makes sense |
| Silk.NET | C# bindings that expose native APIs such as Vulkan | With the host graphics lesson |
| GLFW | A native window/input library used by the planned host | With the host graphics lesson |

**API** means the operations a library exposes. **Binding** means a bridge from those operations to C# declarations. “Native” means code/resources outside the ordinary managed .NET object world. None of those later tools is required for your first integer experiment.

## Set up and know what success looks like

Keep [Exactly how to run and test](running-and-testing.md) open while working. It gives copyable PowerShell setup for this checkout (including the local .NET 10 SDK), the exact command after each kind of edit, expected results and troubleshooting. Each lesson repeats the commands you need there.

Open a terminal in the folder containing `GbaEmulator.sln`. In PowerShell, `Get-Location` shows the current folder and `Get-ChildItem` lists its contents. Run `dotnet --list-sdks`. This repository needs a stable .NET 10 SDK; a listed 8.x SDK alone cannot build `net10.0`. Install the SDK, not only the runtime, from the [official .NET 10 download page](https://dotnet.microsoft.com/en-us/download/dotnet/10.0), then reopen your terminal.

Run these commands one at a time:

```text
dotnet restore GbaEmulator.sln
dotnet build GbaEmulator.sln
dotnet run --project src/Gba.Desktop
dotnet test GbaEmulator.sln
```

Restore obtains the project's packages; build checks compilation. Run prints a scaffold message and exits. No window is expected. Test initially finds no tests; once you write your first test it should report an actual result. A build error is different from a failing assertion: the former means the program could not compile, the latter means it ran and disagreed with your expectation.

If you see `NETSDK1045`, check the SDK version before changing code. If restore cannot reach NuGet, resolve that download error before interpreting any later errors. Read the first useful error with its filename and line number; later errors may be consequences.

## A separate place to try the examples

Create a console sandbox from the repository root, once:

First use the [new-terminal setup](running-and-testing.md#start-every-new-terminal-here). If SyntaxLab already exists, skip `dotnet new` and use the run command only; do not overwrite a practice project you are already using.

```text
dotnet new console --framework net10.0 --output .work/SyntaxLab
dotnet run --project .work/SyntaxLab
```

Open `.work/SyntaxLab/Program.cs`. Replace its contents with **one** complete warm-up example at a time, save, and run the second command again. `.work` is ignored by Git and this project is outside the solution. It is a scratchpad, not an emulator component. No package installation is needed for console examples. The command options are documented by [Microsoft's dotnet new reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new).

```csharp
int pencils = 4;
int more = 3;
int total = pencils + more;
Console.WriteLine($"Total: {total}");
```

Expected output:

```text
Total: 7
```

Read it aloud: “Create an integer named pencils with value four. Create another integer. Add their values into a third. Print the result.” `=` assigns; it is not an equality question. `;` ends a statement. The `$` string prefix lets `{total}` insert the variable's value. `Console.WriteLine(...)` is a method call; the parentheses enclose what you pass to it.

These are **top-level statements**: the compiler supplies the entry method. Do not paste them inside a second `Main` as well. Examples declaring a class, struct or enum put those declarations after the top-level statements. `using System.IO;` at the top imports names; it does not execute file access. Template projects enable common implicit imports, including `System`.

Warm-ups are deliberately ordinary C# experiments, with invented data and no emulator subsystem. They prepare you for the unsolved “Your implementation task” later on the page. The existing reference sections also contain small fragments that illustrate a concept; only examples explicitly labeled as complete warm-ups promise to work as an entire `Program.cs`. xUnit examples belong in a test project instead and are labeled that way.

## How to approach each lesson

1. Read its beginner introduction. Explain the new nouns without looking.
2. Predict a warm-up's output, then run it in SyntaxLab. Change one value and predict again.
3. Read the hardware section. Write down input, remembered state, output and timing as separate questions.
4. Do the paper/practice step before the implementation task. You can split a chapter over many sessions.
5. Implement one tiny behavior yourself and test it. Record what worked and the next unanswered question in the [progress log](../../progress/README.md).

If a line is confusing, identify its type, operator and method call separately. You do not need to memorize the entire language reference. The [C# lookup](../csharp-and-dotnet/README.md) is there to answer one question at a time.

## Your first few sessions

| Session | Small target | Evidence you can stop with |
| --- | --- | --- |
| Setup | Build the scaffold and run the pencil example | You can change its output deliberately |
| Numbers | Read integers and bitwise operations | You can trace four low bits on paper |
| Testing | Read the generic xUnit example, then write your own low-byte cases | A wrong expectation fails; fixing it passes |
| Machine overview | Draw who owns memory, time, pixels and files | Explain host versus guest without code |
| First memory step | Follow the roadmap's initial memory exercise | One narrow behavior and meaningful boundary tests |

Vulkan, pointers, audio mixing and complete CPU decoding can wait for their milestones. Folder order is a reading index; [ROADMAP](../../ROADMAP.md) is the implementation route. You are making progress when you can predict and explain one new behavior.

[Continue with your first experiment](README.md).
