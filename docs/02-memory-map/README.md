# Memory map: addresses are routes


## In the real GBA

An address identifies where a bus access goes. `0x06000000` is hexadecimal (base 16), with each digit standing for four bits. It is the start address of VRAM, not its size or an index into a giant array. Hardware manuals use hex because boundaries and bit fields align naturally with powers of two. The decimal spelling 100,663,296 describes the same address, but hides those boundaries.

![Address regions, not to scale](../assets/memory-map.svg)

The table gives base physical storage extents. Address windows and mirrors are larger than storage; do not allocate every address in a window.

| Region | Base physical extent (inclusive) | Storage | Users / purpose | Access quirks to investigate |
| --- | --- | ---: | --- | --- |
| BIOS | 0x00000000–0x00003FFF | 16 KiB | CPU firmware | read-only; protected reads outside BIOS execution |
| EWRAM | 0x02000000–0x0203FFFF | 256 KiB | CPU/DMA working data | mirrored; 16-bit external bus affects timing |
| IWRAM | 0x03000000–0x03007FFF | 32 KiB | CPU/DMA fast data | mirrored; 32-bit internal bus |
| I/O | 0x04000000–0x040003FE | sparse register area | CPU/DMA configure hardware | holes, widths, read masks and write side effects; not plain RAM |
| Palette | 0x05000000–0x050003FF | 1 KiB | PPU BG/OBJ colours | mirrored; byte writes duplicate into a halfword |
| VRAM | 0x06000000–0x06017FFF | 96 KiB | PPU pixel/tile storage | non-power-of-two mirror; byte writes depend on BG/OBJ area and mode |
| OAM | 0x07000000–0x070003FF | 1 KiB | PPU object attributes | mirrored; byte writes ignored |
| ROM WS0 | 0x08000000–0x09FFFFFF | up to 32 MiB | CPU/DMA cartridge reads | writes generally not ROM writes; cartridge devices can respond |
| ROM WS1 | 0x0A000000–0x0BFFFFFF | same ROM | alternate wait-state window | same data with different timing configuration |
| ROM WS2 | 0x0C000000–0x0DFFFFFF | same ROM | alternate wait-state window | EEPROM may respond in part of this space |
| SRAM / Flash | begins 0x0E000000 | device-dependent | persistent saves | 8-bit bus; Flash commands/banking differ from RAM |

KiB means 1,024 bytes. The save address window does not state the physical device capacity: common SRAM is 32 KiB and Flash can be 64 or 128 KiB with banking. Serial EEPROM is a different protocol, not an array in the SRAM range.

## In our emulator

Give physical regions storage and route reads/writes by address. A physical offset is the position inside the selected region. For an ordinary unmirrored access near VRAM's base, ask how far the address is from `0x06000000`; only then consider indexing. Do not apply modulo to every region: I/O, VRAM mirroring and cartridge devices need specific rules.

Start with EWRAM and a clear development diagnostic for unsupported addresses. Unknown access should produce a deliberate report or documented temporary fallback, not an accidental index exception. This fallback is not the final hardware open-bus model.

## In C#

Separate `uint` guest addresses from validated host indexes. Byte arrays are enough initially. Two adjacent unequal bytes reveal byte order: lower address `0x78`, next address `0x56` represent little-endian halfword `0x5678`. Wider accesses can cross boundaries, require alignment handling or have I/O semantics different from several byte accesses. The next bus chapter explains why storage and access behavior are separate concerns.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.

## What you should understand now

- [ ] Address versus size versus offset.
- [ ] Why a memory map includes behavior as well as bytes.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Represent EWRAM yourself, then implement the first byte read/write for that region. After that, add little-endian halfword and word tests with distinct bytes. Delay complete mirroring and side-effecting I/O until the bus chapter.

## Definition of done

- First and last EWRAM bytes round-trip.
- Your unsupported-address policy is documented and deterministic.
- 16/32-bit tests demonstrate little endian and define boundary behavior.

## Common mistakes

- Allocating a 4 GiB byte array as the bus.
- Treating mirrored windows as separate storage.
- Assuming casts make an out-of-range host index valid.

## Further reading

- [GBATEK memory map](https://mgba-emu.github.io/gbatek/#gbamemorymap) — check physical sizes, windows and mirrors.
- [Tonc hardware](https://gbadev.net/tonc/hardware.html) — understand why RAM types and access costs differ.

## Next chapter

[ARM7TDMI before opcodes](../03-arm7tdmi/README.md)
