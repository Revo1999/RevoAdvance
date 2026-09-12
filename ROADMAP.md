# Roadmap: one understandable problem at a time

Check a box only after you can explain and verify it. Project files already exist; their learning boxes remain unchecked until you understand them. Folder numbers organize reference subjects; this roadmap chooses implementation order. Each phase links to hardware and local C# lessons, which provide authoritative external references.

For every phase, open its linked lesson and follow the local **Run and check** instructions after saving your work. They name the project, test file/class, command and expected result. [Exactly how to run and test](docs/00-getting-started/running-and-testing.md) supplies terminal setup and troubleshooting. A paper-only exercise is labeled explicitly; a no-tests result never counts as passing an implementation milestone.

## Phase 0 — C# and low-level refresher

New to emulation or the tools? Work through [Before you code](docs/00-getting-started/before-you-code.md) first. Set up the scratchpad, run one tiny console example, then follow the first-session test. The list below is a set of skills to revisit as needed, not a requirement to master every topic before beginning. Each hardware lesson has a syntax warm-up before its technical details.

Hardware / exercise: [Start here: one small experiment](docs/00-getting-started/README.md).
C#/.NET: [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md), [Bitwise operations: a mini-course](docs/csharp-and-dotnet/bitwise-operations.md), [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Structs versus classes](docs/csharp-and-dotnet/structs-vs-classes.md), [Enums and named states](docs/csharp-and-dotnet/enums.md), [Switch statements and pattern matching](docs/csharp-and-dotnet/switch-and-pattern-matching.md), [Projects, assemblies and the .NET CLI](docs/csharp-and-dotnet/project-structure.md).

- [ ] Refresh hexadecimal and binary; explain one hex digit as four bits.
- [ ] Refresh byte / sbyte / ushort / short / uint / int / ulong / long, widening and truncation.
- [ ] Practice AND / OR / XOR / complement, shifts, masks and sign extension.
- [ ] Refresh arrays and understand Span conceptually; defer optimizations.
- [ ] Compare structs/classes, enums and switch statements/expressions.
- [ ] Understand projects, references and the test runner; write your low-byte exercise.

**Exit evidence:** your own discovered tests and written predictions.

## Phase 1 — Understand the machine

Hardware / exercise: [The GBA as an interconnected machine](docs/01-system-overview/README.md).
C#/.NET: [Types and memory](docs/csharp-and-dotnet/types-and-memory.md), [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md).

- [ ] Draw the complete GBA ownership/data-flow map.
- [ ] Explain addresses, little endian, memory-mapped I/O and shared guest time.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 2 — Understand the supplied shell

Hardware / exercise: [Start here: one small experiment](docs/00-getting-started/README.md).
C#/.NET: [Projects, assemblies and the .NET CLI](docs/csharp-and-dotnet/project-structure.md), [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md).

- [ ] Build and inspect the supplied Core, Desktop and test projects (already scaffolded).
- [ ] Explain the one-way dependency boundary; run your first discovered test.
- [ ] Later in this shell phase, follow [loading lesson 1](docs/12-cartridges-and-roms/loading-and-playing.md) and the [file I/O refresher](docs/csharp-and-dotnet/file-io.md): accept a `.gba` path and inspect bytes/metadata without executing the game yet.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 3 — Memory · 🏁 FIRST MEMORY READ

Hardware / exercise: [Memory map: addresses are routes](docs/02-memory-map/README.md).
C#/.NET: [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md).

- [ ] Represent EWRAM; verify byte reads/writes and boundaries.
- [ ] Represent BIOS, IWRAM, VRAM, palette RAM, OAM and ROM storage in small steps.
- [ ] Implement your own Read8, Read16 and Read32 with an explicit endian/width contract.
- [ ] Understand alignment and unsupported-address behavior; add mirrors and I/O through the bus chapter.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 4 — CPU foundation · 🏁 FIRST ARM INSTRUCTION

Hardware / exercise: [ARM7TDMI before opcodes](docs/03-arm7tdmi/README.md).
C#/.NET: [Structs versus classes](docs/csharp-and-dotnet/structs-vs-classes.md), [Enums and named states](docs/csharp-and-dotnet/enums.md), [Bitwise operations: a mini-course](docs/csharp-and-dotnet/bitwise-operations.md), [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md).

- [ ] Represent registers, SP/LR/PC, banked modes and CPSR/SPSRs.
- [ ] Document pipeline/visible-PC convention and test bank switching.
- [ ] Test conditions, then decode/execute one simple ARM operation.
- [ ] Track an initial guest cycle count from the beginning.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 5 — Early graphics · 🏁 FIRST PIXEL

Hardware / exercise: [PPU: turning video data into a picture](docs/07-ppu/README.md).
C#/.NET: [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md).

- [ ] Read the bitmap-modes subchapter; create a synthetic Mode 3 VRAM fixture.
- [ ] Produce a 240 × 160 buffer with verified corner colours and save/view an image.
- [ ] Label this as isolated PPU progress; it does not require a working ROM or Vulkan.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 6 — A narrow CPU program · 🏁 FIRST TEST ROM EXECUTES

Hardware / exercise: [ARM decoding one family at a time](docs/04-arm-instruction-set/README.md).
C#/.NET: [Bitwise operations: a mini-course](docs/csharp-and-dotnet/bitwise-operations.md), [Switch statements and pattern matching](docs/csharp-and-dotnet/switch-and-pattern-matching.md), [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md).

- [ ] Expand ARM data operations, flags, shifter, branches and memory transfers with focused tests.
- [ ] Add the instruction families actually needed by a chosen small legal diagnostic.
- [ ] Specify initial registers/entry point/stack and BIOS assumptions in the cartridge chapter.
- [ ] Execute that diagnostic and verify an explicit memory signature or report.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 7 — Thumb and CPU exceptions

Hardware / exercise: [Thumb: narrower instructions, shared CPU](docs/05-thumb-instruction-set/README.md).
C#/.NET: [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md), [Enums and named states](docs/csharp-and-dotnet/enums.md), [Host exceptions and guest exceptions](docs/csharp-and-dotnet/exceptions.md).

- [ ] Implement Thumb families incrementally; test ARM/Thumb exchange and BL halves.
- [ ] Add remaining ARM families, status operations and instruction edge cases as tested milestones.
- [ ] Implement SWI/undefined entry and architectural return behavior; distinguish host exceptions.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 8 — Guest timeline and IRQ

Hardware / exercise: [One guest timeline](docs/14-timing-and-scheduling/README.md).
C#/.NET: [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md), [How C# becomes machine code](docs/csharp-and-dotnet/runtime.md), [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md).

- [ ] Use a shared simple scheduler for CPU and display progress.
- [ ] Implement IE/IF/IME, masks, acknowledgement and CPU IRQ entry/return.
- [ ] Advance peripherals during HALT and test equal-time event ordering.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 9 — Timers

Hardware / exercise: [Timers: counters driven by guest time](docs/09-timers/README.md).
C#/.NET: [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md), [Properties and fields](docs/csharp-and-dotnet/properties-and-fields.md).

- [ ] Implement one counter, reload, prescaler and enable transitions.
- [ ] Expand to four timers, cascade, overflow IRQs and remainder preservation.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 10 — DMA

Hardware / exercise: [DMA: timed transfers with bus ownership](docs/10-dma/README.md).
C#/.NET: [Structs versus classes](docs/csharp-and-dotnet/structs-vs-classes.md), [Enums and named states](docs/csharp-and-dotnet/enums.md).

- [ ] Implement one immediate bus transfer with elapsed time.
- [ ] Add channel restrictions, zero-count semantics, priorities and address control.
- [ ] Add HBlank/VBlank triggers and repeat/reload; defer FIFO special cases until audio.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 11 — Host display

Hardware / exercise: [Vulkan: presenting the finished framebuffer](docs/15-vulkan-output/README.md).
C#/.NET: [Native interop and resource lifetime](docs/csharp-and-dotnet/native-interop.md), [Unsafe code and pointers](docs/csharp-and-dotnet/unsafe-and-pointers.md).

- [ ] Learn pointer/resource lifetime, then select Silk.NET Vulkan and GLFW packages without SDL.
- [ ] Present a synthetic texture; validate resize, synchronization and clean shutdown.
- [ ] Connect the PPU framebuffer with nearest and integer scaling.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 12 — First integrated boot · 🏁 FIRST REAL GAME BOOT SCREEN

Hardware / exercise: [Cartridges, BIOS and persistent data](docs/12-cartridges-and-roms/README.md).
C#/.NET: [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Host exceptions and guest exceptions](docs/csharp-and-dotnet/exceptions.md), [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md).

- [ ] Choose one legally obtained game and record its required CPU/video/BIOS features.
- [ ] Complete [loading and playing](docs/12-cartridges-and-roms/loading-and-playing.md): Open ROM/file selection, run, pause/resume, reset and changing games. Review [C# file I/O](docs/csharp-and-dotnet/file-io.md).
- [ ] Implement the tiled/OBJ subset it actually needs, using the PPU subchapters and focused fixtures.
- [ ] Integrate a legally obtained BIOS or explicitly documented alternative boot strategy.
- [ ] Diagnose the first divergent trace until the chosen boot screen appears; record remaining gaps.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 13 — Keypad · 🏁 FIRST INPUT

Hardware / exercise: [Keypad: host buttons become guest bits](docs/11-input/README.md).
C#/.NET: [Enums and named states](docs/csharp-and-dotnet/enums.md), [Bitwise operations: a mini-course](docs/csharp-and-dotnet/bitwise-operations.md).

- [ ] Implement active-low KEYINPUT and KEYCNT matching with injected inputs.
- [ ] Map physical buttons in Desktop; verify a game/menu response and replayable input.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 14 — Broader PPU behavior

Hardware / exercise: [PPU: turning video data into a picture](docs/07-ppu/README.md).
C#/.NET: [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Bitwise operations: a mini-course](docs/csharp-and-dotnet/bitwise-operations.md), [Structs versus classes](docs/csharp-and-dotnet/structs-vs-classes.md).

- [ ] Complete bitmap modes, regular/affine BGs, tile maps and scroll boundaries.
- [ ] Add regular/affine sprites, mapping modes, wrapping and priority ties.
- [ ] Implement transparency, windows, blending, brightness and mosaic.
- [ ] Test display flags, object limits and mid-frame writes; document scanline accuracy limits.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 15 — Cartridge persistence

Required user workflow: [save and resume](docs/12-cartridges-and-roms/saving-and-resuming.md). C#/.NET: [file I/O](docs/csharp-and-dotnet/file-io.md).

Hardware / exercise: [Cartridges, BIOS and persistent data](docs/12-cartridges-and-roms/README.md).
C#/.NET: [Arrays, spans and byte order](docs/csharp-and-dotnet/arrays-and-spans.md), [Host exceptions and guest exceptions](docs/csharp-and-dotnet/exceptions.md).

- [ ] Implement and persist SRAM first.
- [ ] Load the matching save before guest execution; keep per-ROM save data separate from the original `.gba`.
- [ ] Track dirty data, persist at controlled boundaries, and preserve the previous good save if writing fails.
- [ ] Verify a supported game's Save → close emulator completely → reopen ROM → Continue workflow, including reset and ROM switching.
- [ ] Add Flash commands/banking and EEPROM serial protocol as separate tested tasks.
- [ ] Treat unusual cartridge peripherals as later explicit scope.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 16 — Audio · 🏁 FIRST AUDIO

Hardware / exercise: [Audio: guest clocks become host samples](docs/13-audio/README.md).
C#/.NET: [Integer types, binary and hexadecimal](docs/csharp-and-dotnet/integer-types.md), [Allocations and garbage collection](docs/csharp-and-dotnet/allocations-and-gc.md), [Native interop and resource lifetime](docs/csharp-and-dotnet/native-interop.md).

- [ ] Verify one source numerically, then play a stable tone through a non-SDL host backend.
- [ ] Add legacy channels, timer-driven FIFOs, DMA refill and routing/mixing.
- [ ] Implement resampling/buffering with bounded latency and no steady underruns.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 17 — Compatibility and timing · 🏁 FIRST PLAYABLE GAME

Hardware / exercise: [Evidence before game compatibility](docs/16-testing/README.md).
C#/.NET: [Testing with xUnit v2](docs/csharp-and-dotnet/testing.md), [Performance without premature optimization](docs/csharp-and-dotnet/performance.md).

- [ ] Run versioned diagnostics and fix reproducible CPU/bus/PPU/timer/DMA failures.
- [ ] Refine wait states, sequential accesses, prefetch, pipeline and event edges.
- [ ] Play a defined section of one chosen game with graphics, input, saves and audio; log defects.
- [ ] Run the same `.gba` through the normal Open ROM path, then restart the app and continue its saved progress.
- [ ] Define supported behavior explicitly rather than claiming universal compatibility.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Phase 18 — Save states and debugger

Hardware / exercise: [Debugging and reproducible state](docs/17-debugging-tools/README.md).
C#/.NET: [Ref and value semantics](docs/csharp-and-dotnet/ref-and-value-semantics.md), [Structs versus classes](docs/csharp-and-dotnet/structs-vs-classes.md), [Allocations and garbage collection](docs/csharp-and-dotnet/allocations-and-gc.md).

- [ ] Add trace/breakpoint/memory inspection driven by actual debugging needs.
- [ ] Implement versioned save states including hidden latches and scheduler state.
- [ ] Add Save State/Load State slots using the [save-state workflow](docs/12-cartridges-and-roms/saving-and-resuming.md); validate ROM/version and explain how restoring older cartridge data affects later persistence.
- [ ] Verify restore-and-replay determinism.
- [ ] Profile before optimizing; leave NativeAOT, display shaders and serial/link peripherals optional.

**Exit evidence:** the linked chapter’s definition of done, recorded with test results or an observed artifact in [progress](progress/README.md).

## Cross-topic reading for integration

IRQ: [interrupts](docs/08-interrupts/README.md); bus accuracy: [bus](docs/06-bus-and-memory/README.md); CPU exceptions: [entry/return](docs/03-arm7tdmi/exceptions.md); initial graphics: [bitmaps](docs/07-ppu/bitmap-modes.md); game boot prerequisites: [tiles](docs/07-ppu/tile-modes.md) and [objects](docs/07-ppu/sprites.md).

A game boot date cannot be promised by a fixed opcode count. Select a target, identify its prerequisites and move only the necessary tested feature forward. A diagnostic output or a framebuffer fixture is useful visible progress even while the rest of the machine is incomplete.
