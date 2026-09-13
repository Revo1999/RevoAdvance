# Your emulator course

**One lesson at a time: read → write → save → check.**

Double-click `learn.cmd` in the repository root. It remembers your current lesson. **O** opens its README. **N** moves on after checks; **P** revisits the previous lesson. You can also double-click `learn.cmd` inside a lesson folder to select it directly.

The launcher prepares missing starter files and supplied tests without overwriting your work. You write the emulator behavior. Early checks run automatically on save. Later lessons include small observable fixtures and app checks; the launcher distinguishes those self-checks from automatic test results.

The whole course uses the same page structure: the GBA rule, a short C# example, specific implementation steps, and an observable finish. Larger components are split into several lessons. Work on one numbered implementation step per sitting if needed. You can ask for an explanation, signature, fixture, test, or host/setup assistance at any point; emulator method bodies remain yours.

Start with [01: memory that remembers bytes](01-ewram/README.md). The table is navigation, not a reading assignment.

| Lesson | Component or behavior | How you check |
| --- | --- | --- |
| 01 | [Memory that remembers bytes](01-ewram/README.md) | Supplied tests |
| 02 | [Reading two or four bytes together](02-memory-widths/README.md) | Supplied tests |
| 03 | [Turning a GBA address into a memory access](03-bus/README.md) | Supplied tests |
| 04 | [Keeping cartridge program bytes](04-rom/README.md) | Supplied tests |
| 05 | [The CPU working registers](05-registers/README.md) | Supplied tests |
| 06 | [Deciding whether an ARM instruction runs](06-conditions/README.md) | Supplied tests |
| 07 | [Reading fields from an ARM instruction](07-arm-fields/README.md) | Supplied tests |
| 08 | [Executing MOV, ADD, and SUB](08-first-arm/README.md) | Supplied tests |
| 09 | [Carry and signed overflow](09-arithmetic-flags/README.md) | Supplied tests |
| 10 | [Shifts, rotations, and ARM operands](10-shifter/README.md) | Observe the listed behavior |
| 11 | [Program flow and the visible PC](11-branches/README.md) | Observe the listed behavior |
| 12 | [Moving values between registers and memory](12-loads-stores/README.md) | Observe the listed behavior |
| 13 | [The first Thumb instructions](13-thumb/README.md) | Supplied tests |
| 14 | [Stacks and transferring several registers](14-stack-transfers/README.md) | Observe the listed behavior |
| 15 | [Completing CPU families one at a time](15-more-cpu/README.md) | Observe the listed behavior |
| 16 | [Banked registers and entering an exception](16-exceptions/README.md) | Observe the listed behavior |
| 17 | [Turning a GBA color into a pixel](17-first-pixel/README.md) | Supplied tests |
| 18 | [Counting scanlines](18-display-time/README.md) | Supplied tests |
| 19 | [Remembering interrupt requests](19-interrupts/README.md) | Supplied tests |
| 20 | [One timer that reloads on overflow](20-timers/README.md) | Supplied tests |
| 21 | [Copying through the bus with DMA](21-dma/README.md) | Observe the listed behavior |
| 22 | [Pressed buttons become zero bits](22-keypad/README.md) | Supplied tests |
| 23 | [Connecting components to one guest clock](23-machine-time/README.md) | Observe the listed behavior |
| 24 | [Drawing a tiled background](24-tiles/README.md) | Observe the listed behavior |
| 25 | [Objects on top of backgrounds](25-sprites/README.md) | Observe the listed behavior |
| 26 | [Affine sampling and the other bitmap modes](26-affine-bitmaps/README.md) | Observe the listed behavior |
| 27 | [Choosing the final visible pixel](27-composition/README.md) | Observe the listed behavior |
| 28 | [Showing your framebuffer in a window](28-desktop-display/README.md) | Observe the listed behavior |
| 29 | [Loading a program and choosing a boot state](29-boot/README.md) | Observe the listed behavior |
| 30 | [Run, pause, reset, and buttons](30-play-controls/README.md) | Observe the listed behavior |
| 31 | [Keeping a game save after the app closes](31-sram/README.md) | Observe the listed behavior |
| 32 | [Flash saves are a command-driven device](32-flash/README.md) | Observe the listed behavior |
| 33 | [A save protocol sent one bit at a time](33-eeprom/README.md) | Observe the listed behavior |
| 34 | [A sound channel as changing numeric output](34-square-audio/README.md) | Observe the listed behavior |
| 35 | [The other legacy sound sources](35-wave-noise/README.md) | Observe the listed behavior |
| 36 | [Timer-driven audio FIFOs and DMA refill](36-direct-sound/README.md) | Observe the listed behavior |
| 37 | [Mixing and playing the sound](37-host-audio/README.md) | Observe the listed behavior |
| 38 | [Restoring an exact emulated moment](38-save-states/README.md) | Observe the listed behavior |
| 39 | [Finding the first wrong step](39-debugger/README.md) | Observe the listed behavior |
| 40 | [Making one game reliably playable](40-compatibility/README.md) | Observe the listed behavior |

All 40 lesson pages are written. Automatic checks are supplied for the lessons labeled above; the observed lessons have starter files and concrete acceptance cases, not a hidden claim of automated coverage. The course grows a supported emulator in stages. Completion of a small helper does not claim complete ARM7TDMI, GBA hardware accuracy, or universal game support.
