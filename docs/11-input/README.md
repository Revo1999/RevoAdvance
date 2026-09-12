# Keypad: host buttons become guest bits

## Before the technical details

Your keyboard is a host input device. The GBA sees logical buttons, represented by register bits. Active-low means a zero bit indicates the active condition. Keep the physical key mapping separate from the guest meaning, so tests can describe button presses without a window.

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

### Interpret an active-low toy signal

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int wireLevel = 0;
bool active = wireLevel == 0;
Console.WriteLine(active);
```

Expected output:

```text
True
```

The numeric level and its meaning differ. A zero can mean “active” when that is the convention. Do not assume every hardware flag uses one for true.

### Turn a host-style choice into a label

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
string key = "Space";
string action = key switch
{
    "Space" => "Jump",
    "Escape" => "Pause",
    _ => "None"
};
Console.WriteLine(action);
```

Expected output:

```text
Jump
```

A mapping chooses meaning from an input. These are invented actions, not a completed GBA button map. Later, emulator controls such as pause belong to the host and must be kept distinct from guest buttons.

### Try it before implementing

Predict the first example for wire level one. Write a paper sequence of press, hold, release and focus loss, and state which logical buttons remain down at each step. No keyboard library is needed for this reasoning.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

KEYINPUT at 0x04000130 reports ten active-low button bits: 0 means pressed. KEYCNT at 0x04000132 selects keys and configures an optional keypad interrupt with OR/AND matching. Button order is A, B, Select, Start, Right, Left, Up, Down, R, L in bits 0–9.

## In our emulator

Desktop samples physical keyboard/gamepad state and supplies a logical button snapshot to Core. Core models KEYINPUT and keypad IRQ behavior. Input is an external stimulus; tests inject it deterministically instead of requiring a real keyboard. Document at which guest boundary a new host snapshot becomes visible and clear host-held keys on focus loss.

```text
keyboard / gamepad → Desktop mapping → logical buttons
                                           ↓
                         Core KEYINPUT / KEYCNT → IRQ request
```

Timing initially samples at a known frame or scheduler boundary; later record guest timestamps for replay. Host key repeat is not repeated hardware button presses.

## In C#

Enums can name independent button bits. Bitwise operations invert or combine the specified field width. Keep reserved read bits consistent with the hardware documentation, rather than blindly complementing an entire int.


## C#/.NET concepts used here

- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Enums and named states](../csharp-and-dotnet/enums.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum): Named constants and underlying integral types.

## What you should understand now

- [ ] Host mapping and emulated keypad logic have different owners.
- [ ] Active-low bits need an explicit width.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Implement input-state injection and test no buttons, one button, two buttons and KEYCNT matching. Then map one host key after the host milestone exists.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/InputTests.cs` with a **public class named `InputTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test logical press/release, active-low bits and implemented keypad IRQ conditions. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~InputTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `InputTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Unpressed/pressed states use the correct polarity.
- AND and OR matching differ in tests.
- A deterministic input sequence can be replayed.

## Common mistakes

- Using 1 for pressed directly in KEYINPUT.
- Leaking desktop key codes into Core.
- Forgetting C# complement operates over the promoted width.

## Further reading

- [Tonc keypad](https://gbadev.net/tonc/keys.html) — active-low input and combinations.
- [GBATEK keypad](https://mgba-emu.github.io/gbatek/#gbakeypadinput) — KEYCNT and interrupt details.

## Next chapter

[Cartridges, BIOS and persistent data](../12-cartridges-and-roms/README.md)
