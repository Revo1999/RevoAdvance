# The GBA as an interconnected machine


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
