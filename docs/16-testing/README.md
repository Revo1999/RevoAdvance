# Evidence before game compatibility


## Strategy

“Does a game boot?” is a useful integration observation, but a failure could originate almost anywhere. Build small independent oracles (known expected results) before relying on a game screen.

| Level | Example evidence | Why it isolates a bug |
| --- | --- | --- |
| Bits | field extraction with surrounding ones | reveals mask/shift errors |
| Memory | first/last byte, widths, mirrors, endian | isolates bus routing |
| Decode | fixed opcode with expected fields | no execution or host required |
| Execute | chosen initial/final registers and memory | checks one operation |
| Flags | zero, sign, carry, overflow boundary cases | distinguishes arithmetic interpretations |
| Timing | event before/at/after boundary | exposes off-by-one scheduling |
| PPU | exact pixels from tiny synthetic fixtures | isolates mode/address/priority behavior |
| Diagnostic ROM | reproducible report from known suite revision | integrates CPU, bus and devices |
| Game | boot/input/audio plus regression observations | broad compatibility evidence |

Keep generated fixtures small and describe what they prove. A synthetic Mode 3 image validates pixel conversion, not instruction execution. A CPU diagnostic may need stack, BIOS calls, interrupts or video before it can report failures. Inventory those prerequisites before interpreting a blank screen.

## Test projects and diagnostic ROMs

For real-game integration, use the normal [Open ROM workflow](../12-cartridges-and-roms/loading-and-playing.md), not a hardcoded test-only path. Verify loading a path with spaces, pause/resume, reset and changing games. For a game with the implemented save device, choose Save in-game, close the entire app, reopen the ROM and choose Continue. Check that another ROM cannot inherit its save data and that a failed persistence attempt preserves the previous good file. See [save/resume acceptance criteria](../12-cartridges-and-roms/saving-and-resuming.md).

Use `tests/Gba.Core.Tests` for deterministic xUnit cases. [The testing refresher](../csharp-and-dotnet/testing.md) shows Fact/Theory, assertions and Arrange/Act/Assert using generic arithmetic. No dummy passing test is shipped. Your first low-byte test is the first actual test.

Use [mGBA's test suite](https://github.com/mgba-emu/suite) and [gba-tests](https://github.com/jsmolka/gba-tests) as test resources; read their build instructions and licenses. Supply/build ROMs yourself in [roms](../../roms/README.md); pin revision/hash in the log. A reference emulator is useful for comparison but not infallible. Resolve conflicts using hardware documentation and hardware-backed tests, not majority vote between emulators.

For every failure, record test version, BIOS strategy, starting state, expected behavior, actual behavior, and the smallest instruction/event trace that distinguishes them. Avoid full-frame logs when ten events reveal the first divergence.

## In C#

Pure decoding tests need no expensive system setup. Integration fixtures should deliberately reset all state rather than share mutable objects across tests. Compute expected values independently; do not call the same helper in both expected and actual paths.


## C#/.NET concepts used here

- [Testing with xUnit v2](../csharp-and-dotnet/testing.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test): Test projects, assertions and parameterized tests.
- [Host exceptions and guest exceptions](../csharp-and-dotnet/exceptions.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/): Throw, try, catch and finally.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.

## What you should understand now

- [ ] Different tests prove different layers.
- [ ] Diagnostics themselves have hardware prerequisites.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Build a test inventory for the subsystem you just implemented. Add one boundary test and one case that would fail under a plausible incorrect implementation.

## Definition of done

- Tests run without a ROM or desktop unless explicitly integration tests.
- The latest diagnostic run has version and prerequisites recorded.
- Failures report enough state to reproduce.

## Common mistakes

- Counting a no-tests run as a correctness pass.
- Copying implementation logic into the expected calculation.
- Using a game boot to claim full hardware accuracy.

## Further reading

- [mGBA suite](https://github.com/mgba-emu/suite) — focused hardware diagnostics.
- [gba-tests](https://github.com/jsmolka/gba-tests) — additional diagnostic programs.
- [xUnit v2](https://xunit.net/docs/getting-started/v2/getting-started) — framework discovery and parameterization.

## Next chapter

[Debugging and reproducible state](../17-debugging-tools/README.md)
