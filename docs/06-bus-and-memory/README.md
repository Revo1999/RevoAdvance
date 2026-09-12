# The bus: behavior beyond storage

## Before the technical details

A bus is the route used to communicate with memory and devices. Reading ordinary storage can simply return a value; reading a device can have special rules. A side effect is any additional change caused by an operation. Start by noticing the difference between a stored value and a method that changes state.

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

### A method can have a side effect

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
TicketDesk desk = new TicketDesk();
Console.WriteLine(desk.Take());
Console.WriteLine(desk.Take());

class TicketDesk
{
    private int next = 4;
    public int Take()
    {
        int result = next;
        next++;
        return result;
    }
}
```

Expected output:

```text
4
5
```

`private` keeps the counter inside the object. `next++` adds one after the result has been saved. Two identical calls produce different results because the object remembers a change. A device access needs its own documented contract.

### Check a range before using a position

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int position = 4;
int length = 4;
bool inside = position >= 0 && position < length;
Console.WriteLine(inside);
```

Expected output:

```text
False
```

`>=` includes the lower boundary; `<` excludes the upper boundary. `&&` combines Boolean questions, while bitwise `&` is used for integer bit patterns. Bounds are one concern; device width and timing rules are additional concerns.

### Try it before implementing

Try positions -1, 0, 3 and 4. Then list the state before and after each ticket call. In the bus lesson, ask separately what is stored, what an access changes, and how long that access takes.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

The bus connects CPU and DMA accesses to memory and devices. An access has an address, width, read/write direction and timing context. Different physical bus widths and cartridge wait states affect how long it occupies the machine. I/O writes can change future hardware behavior rather than simply store a number.

Important registers include WAITCNT at 0x04000204 and the full peripheral I/O range. Distinguish sequential and nonsequential accesses; prefetch and bus ownership complicate cartridge timing later. BIOS read protection and open-bus behavior depend on prior execution/access state.

```text
guest address + width + direction + access context
                         ↓
                  select region/device
                         ↓
      storage or register side effect + elapsed guest time
```

## In our emulator

Keep RAM storage simple but centralize access rules. A read of a timer counter is different from reading the reload value last written. Palette byte writes duplicate into both bytes of a halfword; OAM byte writes are ignored. VRAM has mode-dependent byte-write rules. Therefore “Read32 is always four Read8 calls” and “Write16 is always two Write8 calls” are unsafe generalizations for devices.

For ARM7TDMI, an unaligned word load has rotation behavior relative to an aligned word; stores and halfword/signed loads have their own rules. Decide which layer handles instruction-specific alignment and which layer handles physical region access. Test that contract rather than aligning every guest access indiscriminately.

## Version 1 and later

First: EWRAM/IWRAM and ROM reads with explicit widths, little endian and deterministic unsupported-access reporting. Then: mirroring, register masks/side effects and wait-state accounting. Later: open bus, BIOS restrictions, prefetch and exact access ordering. Track temporary simplifications in the progress log so they cannot masquerade as accurate hardware.

## In C#

Guest addresses use uint; validated offsets lead to bounded arrays/spans. A numeric overflow policy should be intentional. Avoid catching IndexOutOfRangeException as ordinary bus control flow; it hides routing mistakes and does not model open bus.


## C#/.NET concepts used here

- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Host exceptions and guest exceptions](../csharp-and-dotnet/exceptions.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/): Throw, try, catch and finally.

## What you should understand now

- [ ] Memory bytes and bus behavior are separate.
- [ ] Access width and timing belong in your design.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Extend your RAM exercise to explicit widths, one documented mirror and one side-effecting register. Keep storage tests separate from device-access tests.

## Run and check your own implementation

Use the PowerShell terminal prepared at the top of this page, in the repository root. Write your tests in `tests/Gba.Core.Tests/BusTests.cs` with a **public class named `BusTests`** and public methods marked `[Fact]` or `[Theory]`. Add `using Xunit;` at the top. The [complete xUnit examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only) show the file structure; write the actual test bodies yourself. Test read/write widths, boundaries and the specific device side effects you implemented. Emulator logic belongs in `src/Gba.Core`; the first low-byte practice needs no emulator component.

Save all edited files. Run each command separately, stopping if a command fails:

```powershell
dotnet build GbaEmulator.sln
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --list-tests
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj --filter "FullyQualifiedName~BusTests" --logger "console;verbosity=normal"
dotnet test tests/Gba.Core.Tests/Gba.Core.Tests.csproj
```

The build should succeed. The list must include your new test methods. The filtered run must execute your `BusTests` cases and report zero failures; the last command runs **all** Core tests to catch regressions. The count depends on the cases you wrote. “No tests available” or “No test matches” is not a pass: check the saved file, public class/method, attribute and filter spelling. If you choose a different class name, change the filter to match it.

After each code or test edit, save and rerun the filtered command. When it passes, run the full test command again. For your first test, deliberately change one expected value, rerun to see a failed assertion, restore the correct value and rerun to see a pass. Do not leave the deliberately wrong expectation in your work. A compiler error must be fixed before you can evaluate assertions. These commands build automatically; do not use `--no-build` while learning because it can execute stale code.

## Definition of done

- Tests cover a mirror alias and a region boundary.
- One register read/write pair demonstrates why I/O is not RAM.
- Unsupported guest access reports its address, width and CPU context.

## Common mistakes

- Using host endianness implicitly.
- Assuming every byte access is legal.
- Counting each multi-byte access as the same number of cycles.

## Further reading

- [GBATEK memory control](https://mgba-emu.github.io/gbatek/#4000204h---waitcnt---waitstate-control-rw) — WAITCNT and bus behavior.
- [ARM7TDMI manual](https://documentation-service.arm.com/static/5f4786a179ff4c392c0ff819) — alignment and memory interface.

## Next chapter

[PPU: turning video data into a picture](../07-ppu/README.md)
