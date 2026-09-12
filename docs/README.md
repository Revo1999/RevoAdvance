# Learning chapters

New to the stack or emulation? Read [Before you code](00-getting-started/before-you-code.md) first, then [Start here](00-getting-started/README.md); use [ROADMAP](../ROADMAP.md) for implementation order.

Every numbered chapter and focused subchapter begins with an introduction, two independent C# warm-ups with expected output, and a practice prompt. Run the examples in the separate [SyntaxLab scratchpad](00-getting-started/before-you-code.md#a-separate-place-to-try-the-examples), then return to the hardware rules and your implementation task. You can split any chapter over several sessions.

- [Before you code: tools, setup and how to learn](00-getting-started/before-you-code.md)
- [Exactly how to run and test: commands and troubleshooting](00-getting-started/running-and-testing.md)
- [Start here: one small experiment](00-getting-started/README.md)
- [The GBA as an interconnected machine](01-system-overview/README.md)
- [Memory map: addresses are routes](02-memory-map/README.md)
- [ARM7TDMI before opcodes](03-arm7tdmi/README.md)
- [ARM decoding one family at a time](04-arm-instruction-set/README.md)
- [Thumb: narrower instructions, shared CPU](05-thumb-instruction-set/README.md)
- [The bus: behavior beyond storage](06-bus-and-memory/README.md)
- [PPU: turning video data into a picture](07-ppu/README.md)
- [Interrupts: requests, masks and exception entry](08-interrupts/README.md)
- [Timers: counters driven by guest time](09-timers/README.md)
- [DMA: timed transfers with bus ownership](10-dma/README.md)
- [Keypad: host buttons become guest bits](11-input/README.md)
- [Cartridges, BIOS and persistent data](12-cartridges-and-roms/README.md)
- [Load your .gba files and play](12-cartridges-and-roms/loading-and-playing.md)
- [Save progress and resume later](12-cartridges-and-roms/saving-and-resuming.md)
- [Audio: guest clocks become host samples](13-audio/README.md)
- [One guest timeline](14-timing-and-scheduling/README.md)
- [Vulkan: presenting the finished framebuffer](15-vulkan-output/README.md)
- [Evidence before game compatibility](16-testing/README.md)
- [Debugging and reproducible state](17-debugging-tools/README.md)

- [C# and .NET refresher](csharp-and-dotnet/README.md)
- [Original visual assets](assets/README.md)
- [Validation record](VALIDATION.md)
