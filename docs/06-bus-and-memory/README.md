# The bus: behavior beyond storage


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
