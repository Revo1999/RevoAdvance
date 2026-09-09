# Original visual explanations

All figures were composed for this repository; none are copied from other emulator documentation. SVGs use opaque light panels and dark text for contrast in both GitHub themes. They are simplified learning diagrams, not timing schematics.

| Visual | Location |
| --- | --- |
| Complete system and host boundary | [system.svg](system.svg) |
| Physical memory regions | [memory-map.svg](memory-map.svg) |
| Visible CPU registers | [registers.svg](registers.svg) |
| Screen coordinates | [screen.svg](screen.svg) |
| Nominal display timing | [scanline.svg](scanline.svg) |
| Vulkan presentation | [vulkan-flow.svg](vulkan-flow.svg) |
| CPSR fields and CPU pipeline | [CPU chapter](../03-arm7tdmi/README.md) |
| ARM versus Thumb width | [Thumb chapter](../05-thumb-instruction-set/README.md) |
| VRAM layouts | [VRAM](../07-ppu/vram.md) |
| Tile → palette → pixel | [tiles](../07-ppu/tile-modes.md) and [PPU](../07-ppu/README.md) |
| OAM representation | [sprites](../07-ppu/sprites.md) |
| IRQ flow | [interrupts](../08-interrupts/README.md) |
| DMA flow | [DMA](../10-dma/README.md) |
| Timer cascade | [timers](../09-timers/README.md) |
| Audio signal | [audio](../13-audio/README.md) |
| Compilation pipeline | [runtime](../csharp-and-dotnet/runtime.md) |
| Managed versus native memory | [allocations/GC](../csharp-and-dotnet/allocations-and-gc.md) |
| Value versus reference assignment | [structs/classes](../csharp-and-dotnet/structs-vs-classes.md) |
| Masks and shifts | [bitwise mini-course](../csharp-and-dotnet/bitwise-operations.md) |

SVGs render as Markdown images; Mermaid blocks require a Mermaid-capable Markdown viewer (GitHub supports them). ASCII figures remain readable in plain text. All diagrams have adjacent prose so they are not the only explanation.
