# Affine sampling, priorities, windows and effects


## In the real GBA

The final pixel is chosen from eligible background, object and backdrop candidates. Lower numeric priority is generally in front; ties need hardware-specific layer/OAM ordering. Transparent index zero removes a candidate, rather than producing black. Window masks can disable layers or effects at a screen location before the final composition decision.

Affine rendering maps a destination coordinate to a source coordinate using a matrix and reference point. The signed fixed-point registers encode fractional steps; this is sampling, not physically rotating bytes in VRAM. Background and object affine behavior have distinct bounds and reference rules. BG reference-point registers and per-line internal state matter when software writes them mid-frame.

```text
destination (x,y) → fixed-point affine mapping → source sample
                                                     ↓
candidate layers → window eligibility → priority → effects → final pixel
```

WIN0/WIN1 rectangles and OBJ-window pixels select masks via WININ/WINOUT. BLDCNT chooses effects/eligible targets; BLDALPHA chooses blend coefficients; BLDY controls brighten/darken. Coefficients have documented effective limits and output clamps. A semitransparent OBJ has special blending behavior; it is not general modern per-pixel alpha. MOSAIC groups sample positions and is another later independent feature.

## In our emulator

Keep enough candidate metadata to explain why a pixel wins. First solve opaque priority and transparency; add windows, then alpha/brightness effects, then affine edge cases and mosaic. Inputs include register state and per-layer samples; outputs are final colours. Scanline latching is an initial timing approximation, particularly visible with affine reference and window writes.

## In C#

Use signed integer reasoning for affine coefficients and wide enough intermediates. Fixed point stores an integer scaled by a power of two; fractional position is preserved until deliberately reduced. Generic floating-point transforms may obscure the exact rounding rules the GBA uses.


## C#/.NET concepts used here

- [Integer types, binary and hexadecimal](../csharp-and-dotnet/integer-types.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types): Ranges, literals and signedness.
- [Bitwise operations: a mini-course](../csharp-and-dotnet/bitwise-operations.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/bitwise-and-shift-operators): AND, OR, XOR, complement and shift behavior.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.

## What you should understand now

- [ ] I can trace the inputs to the outputs described above.
- [ ] I can state the relevant memory/register and timing rules before coding.

## C#/.NET refresher

Use the local and official links above together: read the local explanation first, then the named part of the official page.

## Your implementation task

Create tiny overlap fixtures: transparent/opaque BG, equal priorities, a masked window and one blend. Implement identity affine sampling before rotations.

## Definition of done

- A single pixel trace names the winning layers and applied effect.
- Identity affine output matches untransformed output.
- Boundary/clamping cases use independently calculated expectations.

## Common mistakes

- Using float rounding without comparing hardware fixed-point rules.
- Treating every transparent pixel as black.
- Applying blend effects before window eligibility.

## Further reading

[Tonc effects](https://gbadev.net/tonc/gfx.html) — windows and colour effects. [Tonc affine](https://gbadev.net/tonc/affine.html) — transform interpretation. [GBATEK](https://mgba-emu.github.io/gbatek/#gbalcdvideocontroller) — exact registers and composition rules.

## Next chapter

[Continue](../08-interrupts/README.md).
