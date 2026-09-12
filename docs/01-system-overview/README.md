# The GBA as an interconnected machine

## Before the technical details

Think of the machine as several workers sharing a notebook. The CPU follows instructions; memory remembers bytes; the PPU turns video data into pixels. A register is a small named storage location, while a peripheral is a device around the CPU. Host means your PC; guest means the GBA you are modeling. Your first task is an ownership drawing, not a collection of complicated classes.

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

### Two names can point to the same object

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
Notebook owner = new Notebook();
Notebook reader = owner;
owner.Pages = 6;
Console.WriteLine(reader.Pages);

class Notebook
{
    public int Pages;
}
```

Expected output:

```text
6
```

`new` creates one object. `reader = owner` copies its reference, so both variables reach the same notebook. `public` allows the example to access the field. This is why ownership matters when several parts of a program share memory.

### A copied number is independent

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
int first = 6;
int second = first;
first = 9;
Console.WriteLine(second);
```

Expected output:

```text
6
```

An `int` assignment copies the value. Updating `first` does not update `second`. Compare this result with the shared object above before choosing how to represent state.

### Try it before implementing

Predict what happens if you change `reader.Pages` instead. Draw one box for the object and two arrows for its references. Then draw separate boxes for the two integers. Use these pictures when reading the component ownership table.

Continue with the detailed lesson below after you can explain your prediction.


## In the real GBA

The Game Boy Advance is a small computer whose components share memory and time. Its ARM7TDMI CPU runs game instructions. A BIOS ROM supplies startup and firmware routines. Working memory is split into larger external work RAM (EWRAM) and smaller, faster internal work RAM (IWRAM). A cartridge supplies program/data ROM and, when present, persistent save storage using a cartridge-specific protocol.

The picture processing unit (PPU) repeatedly scans a 240 × 160 display. It interprets video RAM (VRAM), palette RAM and object attribute memory (OAM). DMA transfers data without the CPU issuing an instruction for every element. Timers count clock ticks and can trigger interrupts or audio activity. Interrupt registers collect requests; the CPU decides whether it can take an IRQ exception. Keypad hardware exposes buttons. The audio unit combines legacy tone/noise channels with FIFO-driven digital sound.

![Original system diagram](../assets/system.svg)

| Component | Receives | Produces / changes |
| --- | --- | --- |
| ARM7TDMI | instructions, memory data, IRQ line | bus accesses and architectural state |
| BIOS | instruction fetches / firmware entry | startup and software interrupt services |
| EWRAM / IWRAM | addressed reads and writes | transient program data |
| Cartridge | ROM reads / save protocol accesses | instructions, assets, persistent bytes |
| PPU | video data, control registers, elapsed cycles | pixels and display events |
| DMA | configuration and trigger | timed bus transfers, completion request |
| Timers | clocks or previous timer overflow | counters, overflows, audio/IRQ events |
| IRQ registers | peripheral requests, enable masks | pending state / CPU IRQ request |
| Keypad | button levels | active-low key bits, optional IRQ request |
| Audio | channel settings, FIFO samples, timer events | mixed signal |

## In our emulator

Represent persistent hardware state explicitly: registers, arrays, counters, latches and pending events. A bus routes guest addresses to the owner of each region. A scheduler advances the components in guest cycles. Core eventually accepts ROM data and button state, then produces framebuffer pixels, audio samples and inspectable state. Desktop loads files and presents those outputs.

```text
Conceptual frame:
CPU instruction / DMA activity consumes guest time
          ↓
advance due display, timer and audio events
          ↓
latch interrupt requests and reconsider CPU execution
          ↓
repeat until a frame boundary is reached
```

This is a teaching sequence, not literal hardware ordering. Real components operate concurrently, bus accesses occupy time, DMA can stall the CPU, and an event can occur during an instruction. A first instruction-boundary scheduler approximates that ordering; later an event model resolves the inaccuracies. A frame is a display timing boundary, not one CPU instruction or one desktop refresh.

## In C#

Begin with a few concrete state-owning classes, arrays and explicit methods. A `uint` can preserve a register's 32-bit pattern; a byte array can hold RAM bytes. Neither encodes register side effects or timing by itself. Avoid a universal device interface until actual repeated needs justify it. Keep Core independent of graphics, keyboard APIs and wall-clock pacing.

## C# concepts you will eventually use

Start with [types](../csharp-and-dotnet/types-and-memory.md), [integer widths](../csharp-and-dotnet/integer-types.md) and [arrays](../csharp-and-dotnet/arrays-and-spans.md). [State identity](../csharp-and-dotnet/structs-vs-classes.md) matters when CPU, DMA and PPU share the same memory. [Runtime](../csharp-and-dotnet/runtime.md) explains how your C# host executes.


## C#/.NET concepts used here

- [Types and memory](../csharp-and-dotnet/types-and-memory.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/): Value types, reference types and type safety.
- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.

## What you should understand now

- [ ] The role of each major component.
- [ ] Why all components share guest time.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Draw your own ownership map and annotate who writes RAM, video state and IRQ requests. No new source code is required for this overview.

## Check this lesson's exercise

This implementation task is a written explanation or diagram; no new emulator code or test file is required here. Finish the paper task and compare it with the definition of done below. To repeat the **safe console warm-up**, save its code in `.work/SyntaxLab/Program.cs` and run from the prepared repository-root terminal:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the output shown above. The advanced fragments are explanatory and may need additional setup; they are not required runnable exercises. Do not treat a successful console run as evidence for a hardware implementation.

## Definition of done

- You can trace a ROM instruction to a memory write to a visible pixel.
- You can explain why DMA and a halted CPU still require a scheduler.

## Common mistakes

- Treating Vulkan as the PPU.
- Making each component advance from a separate host thread before deterministic timing works.

## Further reading

- [Tonc hardware](https://gbadev.net/tonc/hardware.html) — orientation to the physical system.
- [GBATEK](https://mgba-emu.github.io/gbatek/) — GBA overview and hardware register index; stay in GBA sections.

## Next chapter

[Memory map: addresses are routes](../02-memory-map/README.md)
