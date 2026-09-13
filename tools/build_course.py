"""Maintainer tool: rebuild lesson pages/templates, never the learner's source files."""
from pathlib import Path
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'course'
lessons = []

def clean(text):
    return textwrap.dedent(text).strip() + '\n'

def lesson(number, slug, title, file, hardware, syntax, explanation, tasks, checks, hint, reference,
           starter=None, tests=None, count=0):
    ident = f'{number:02}'
    folder = COURSE / f'{ident}-{slug}'
    folder.mkdir(parents=True, exist_ok=True)
    mode = 'automatic' if tests is not None or number == 1 else 'observed'
    item = dict(id=ident, title=title, folder=folder.relative_to(ROOT).as_posix(),
                file=file, mode=mode, count=count, checks=checks, templates=[])
    if starter:
        (folder / 'starter.cs.txt').write_text(clean(starter), encoding='utf-8')
        item['templates'].append(dict(source=f"{item['folder']}/starter.cs.txt", target=file))
    if tests:
        testfile = f'tests/Gba.Core.Tests/Course{ident}Tests.cs'
        source = f'using Gba.Core.Memory;\nusing Gba.Core.Cartridge;\nusing Gba.Core.Cpu;\nusing Gba.Core.Ppu;\nusing Gba.Core.Interrupts;\nusing Gba.Core.Timers;\nusing Gba.Core.Input;\n\n[Trait("Lesson", "{ident}")]\npublic class Course{ident}Tests\n{{\n{clean(tests)}}}\n'
        # Only import namespaces that actually occur in these checks. Avoid future dependencies.
        imports = []
        for ns, names in {
            'Memory': ['Ewram', 'RamWords', 'MemoryBus'], 'Cartridge': ['RomImage'],
            'Cpu': ['CpuRegisters', 'Conditions', 'ArmFields', 'ArmImmediate', 'Arithmetic', 'ThumbImmediate'],
            'Ppu': ['GbaColor', 'DisplayTiming'], 'Interrupts': ['InterruptController'],
            'Timers': ['GbaTimer'], 'Input': ['Keypad'],
        }.items():
            if any(name in tests for name in names): imports.append(f'using Gba.Core.{ns};')
        source = '\n'.join(imports) + f'\n\n[Trait("Lesson", "{ident}")]\npublic class Course{ident}Tests\n{{\n{clean(tests)}}}\n'
        (folder / 'checks.cs.txt').write_text(source, encoding='utf-8')
        item['templates'].append(dict(source=f"{item['folder']}/checks.cs.txt", target=testfile))
    if mode == 'observed' and starter is None:
        typename = Path(file).stem
        namespace = 'Gba.Desktop' if file.startswith('src/Gba.Desktop/') else 'Gba.Core.' + file.split('/')[2]
        todo = '\n'.join('    // TODO: ' + task for task in tasks)
        content = f'namespace {namespace};\n\n// Read course/{ident}-{slug}/README.md. Choose small methods for the steps below.\npublic class {typename}\n{{\n{todo}\n}}\n'
        (folder / 'starter.cs.txt').write_text(content, encoding='utf-8')
        item['templates'].append(dict(source=f"{item['folder']}/starter.cs.txt", target=file))
    steps = '\n'.join(f'{i}. {task}' for i, task in enumerate(tasks, 1))
    evidence = '\n'.join(f'- {check}' for check in checks)
    checking = (f'The launcher runs **{count} supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.'
                if mode == 'automatic' else
                'The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.')
    (folder / 'README.md').write_text(clean(f'''
# {ident}. {title}

**Read this page → edit `{file}` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

{hardware}

## C# you need now

```csharp
{clean(syntax).strip()}
```

{explanation}

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

{steps}

## Check it

{checking}

{evidence}

<details>
<summary>A hint if you get stuck</summary>

{hint}

</details>

Optional detail: [the existing hardware reference](../../{reference}). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.
'''), encoding='utf-8')
    (folder / 'learn.cmd').write_text(f'@echo off\ncall "%~dp0..\\..\\learn.cmd" -Lesson {ident}\n', encoding='utf-8')
    lessons.append(item)

lesson(1, 'ewram', 'Memory that remembers bytes', 'src/Gba.Core/Memory/Ewram.cs',
    'Games keep changing data in RAM. The GBA has 262,144 bytes of external work RAM (EWRAM). Each byte holds 0–255. Today use offsets into that storage: first 0, last 262143. Write 42 at offset 7, then read 7: you should get 42. Writing 99 there replaces 42. This is physical storage only; guest addresses and timing come later. Callers supply valid offsets.',
    'byte[] boxes = new byte[10];\nboxes[3] = 42;\nbyte answer = boxes[3];',
    '`byte[]` is similar to JavaScript Uint8Array: fixed size, one byte per element. Keep it in a field so calls use the same storage. `public byte Read8(int offset)` returns a byte using `return expression;`. `public void Write8(int offset, byte value)` changes storage and returns nothing. `private` keeps a field inside the object; `public` allows calls from other code. Leave the class/namespace structure in place.',
    ['Give the existing array 262,144 elements.', 'Replace the Read8 placeholder with a read at the given offset.', 'Replace the Write8 placeholder with a write to that same array.'],
    ['A written value can be read.', 'A second write replaces the first.', 'Adjacent offsets stay independent.', 'The first and last offsets work, including values 255 and 0.', 'Two Ewram objects do not share storage.'],
    'Create the array once per object, not inside Read8 or Write8. The NotImplementedException lines are markers to replace.',
    'docs/02-memory-map/README.md', count=6)

lesson(2, 'memory-widths', 'Reading two or four bytes together', 'src/Gba.Core/Memory/RamWords.cs',
    'The GBA is little endian: the byte at the lowest address supplies the lowest eight bits of a larger value. Bytes 34 12 (hex) represent 0x1234. Bytes 78 56 34 12 represent 0x12345678. A halfword is two bytes; a word is four. This helper is only for valid, naturally aligned offsets in ordinary EWRAM, not I/O devices or CPU unaligned-load behavior.',
    'uint value = 0xABCD;\nbyte low = (byte)(value & 0xFF);\nuint moved = value << 4;',
    '`0x` writes a hexadecimal number. `&` keeps bits selected by a mask. `<<` moves bits left; `>>` moves them right. `|` combines bit fields. `(byte)` converts a value to a byte after you select the desired bits. `ushort` holds 16 bits; `uint` holds 32. Cast a byte to uint before placing it in the top eight bits of a word.',
    ['Implement Read16 and Write16 through the supplied Ewram object.', 'Implement Read32 and Write32 through the same storage.', 'Keep each byte in increasing address order; do not make a second memory array.'],
    ['Bytes 34 12 read as 0x1234.', 'Writing 0xBEEF stores EF then BE.', 'Bytes 78 56 34 12 read as 0x12345678.', 'Writing 0xFEDCBA98 stores 98 BA DC FE.'],
    'Number the bytes 0, 1, 2, 3. Work out how many bits each is above the lowest byte before combining them.', 'docs/csharp-and-dotnet/arrays-and-spans.md',
    starter='''namespace Gba.Core.Memory;
public class RamWords(Ewram ram)
{
    public ushort Read16(int offset) => throw new NotImplementedException();
    public uint Read32(int offset) => throw new NotImplementedException();
    public void Write16(int offset, ushort value) => throw new NotImplementedException();
    public void Write32(int offset, uint value) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Reads_a_little_endian_halfword() { var r=new Ewram(); r.Write8(0,0x34); r.Write8(1,0x12); Assert.Equal((ushort)0x1234,new RamWords(r).Read16(0)); }
    [Fact] public void Writes_low_byte_first() { var r=new Ewram(); new RamWords(r).Write16(2,0xBEEF); Assert.Equal((byte)0xEF,r.Read8(2)); Assert.Equal((byte)0xBE,r.Read8(3)); }
    [Fact] public void Reads_a_little_endian_word() { var r=new Ewram(); r.Write8(0,0x78); r.Write8(1,0x56); r.Write8(2,0x34); r.Write8(3,0x12); Assert.Equal(0x12345678u,new RamWords(r).Read32(0)); }
    [Fact] public void Writes_all_four_bytes() { var r=new Ewram(); new RamWords(r).Write32(4,0xFEDCBA98); Assert.Equal(new byte[]{0x98,0xBA,0xDC,0xFE},new[]{r.Read8(4),r.Read8(5),r.Read8(6),r.Read8(7)}); }
''', count=4)

lesson(3, 'bus', 'Turning a GBA address into a memory access', 'src/Gba.Core/Memory/MemoryBus.cs',
    'A guest address identifies a place in the GBA, not an index in your PC memory. EWRAM begins at 0x02000000 and is mirrored throughout 0x02000000–0x02FFFFFF. Its 0x40000 physical bytes repeat: addresses 0x02000007 and 0x02040007 name the same byte. First route only this region. Throw ArgumentOutOfRangeException for other addresses; that is a temporary diagnostic policy, not the GBA open-bus rule.',
    'uint address = 0x12000005;\nbool inside = address >= 0x12000000 && address < 0x13000000;\nint smallIndex = (int)(address & 0xFF);',
    '`uint` is an unsigned 32-bit integer, suitable for guest addresses. `&&` combines comparisons. `if (!inside)` handles a rejected range. A cast to int is safe after you have reduced an address to a small bounded offset. The starter uses a primary constructor: `MemoryBus(Ewram ram)` receives the already-created RAM object, which its methods can use.',
    ['Implement Read8 by checking the EWRAM address region and translating to a physical offset.', 'Implement Write8 with the same address translation and the supplied Ewram.', 'Reject unsupported regions before computing an array offset.'],
    ['A write to 0x02000007 reaches offset 7 in the original RAM.', 'The mirror at 0x02040007 sees the same byte.', '0x02FFFFFF maps to the last physical byte.', 'Addresses outside the EWRAM region report an unsupported access.'],
    'The region selects the device. The low 18 address bits select a byte inside EWRAM. Keep those two decisions separate.', 'docs/06-bus-and-memory/README.md',
    starter='''namespace Gba.Core.Memory;
public class MemoryBus(Ewram ram)
{
    public byte Read8(uint address) => throw new NotImplementedException();
    public void Write8(uint address, byte value) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Routes_to_the_original_RAM() { var r=new Ewram(); var b=new MemoryBus(r); b.Write8(0x02000007,42); Assert.Equal((byte)42,r.Read8(7)); Assert.Equal((byte)42,b.Read8(0x02000007)); }
    [Fact] public void Mirrors_share_storage() { var b=new MemoryBus(new Ewram()); b.Write8(0x02000007,93); Assert.Equal((byte)93,b.Read8(0x02040007)); }
    [Fact] public void Region_end_maps_to_last_byte() { var r=new Ewram(); var b=new MemoryBus(r); b.Write8(0x02FFFFFF,81); Assert.Equal((byte)81,r.Read8(262143)); }
    [Fact] public void Unsupported_regions_are_reported() { var b=new MemoryBus(new Ewram()); Assert.Throws<ArgumentOutOfRangeException>(()=>b.Read8(0x01FFFFFF)); Assert.Throws<ArgumentOutOfRangeException>(()=>b.Write8(0x03000000,1)); }
''', count=4)

lesson(4, 'rom', 'Keeping cartridge program bytes', 'src/Gba.Core/Cartridge/RomImage.cs',
    'A .gba file contains cartridge ROM bytes. Reading those bytes is different from executing them. Start with a RomImage object that owns a copy of supplied bytes and exposes their length and byte reads. It has no write operation. This first helper uses file offsets, not guest addresses. For now an out-of-file read throws ArgumentOutOfRangeException; cartridge bus behavior is a later integration concern.',
    'byte[] original = { 10, 20, 30 };\nbyte[] copy = (byte[])original.Clone();\nint size = copy.Length;',
    'Arrays are reference types: assigning `copy = original` would share one array. Clone creates separate storage; the cast tells C# it is a byte array. A constructor has the class name and no return type. A read-only property can be written `public int Length => expression;`. Later the desktop can supply bytes with File.ReadAllBytes(path); the memory object itself does not need file dialogs.',
    ['In the constructor, retain an independent copy of the supplied bytes.', 'Implement Length and Read8; check the offset against the actual length.', 'Keep the original input independent and expose no ROM write method.'],
    ['The length matches the supplied image.', 'The first and final bytes can be read.', 'Changing the input array after construction does not change ROM data.', 'Negative and past-the-end offsets throw ArgumentOutOfRangeException.'],
    'This is an immutable input snapshot, not RAM. A path, an array, and a guest address are three different things.', 'docs/12-cartridges-and-roms/loading-and-playing.md',
    starter='''namespace Gba.Core.Cartridge;
public class RomImage
{
    public RomImage(byte[] source) { throw new NotImplementedException(); }
    public int Length => throw new NotImplementedException();
    public byte Read8(int offset) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Keeps_the_image_length_and_bytes() { var r=new RomImage(new byte[]{12,34,56}); Assert.Equal(3,r.Length); Assert.Equal((byte)12,r.Read8(0)); Assert.Equal((byte)56,r.Read8(2)); }
    [Fact] public void Input_changes_do_not_modify_ROM() { var data=new byte[]{12}; var r=new RomImage(data); data[0]=99; Assert.Equal((byte)12,r.Read8(0)); }
    [Fact] public void Invalid_file_offsets_are_reported() { var r=new RomImage(new byte[]{12}); Assert.Throws<ArgumentOutOfRangeException>(()=>r.Read8(-1)); Assert.Throws<ArgumentOutOfRangeException>(()=>r.Read8(1)); }
''', count=3)

lesson(5, 'registers', 'The CPU working registers', 'src/Gba.Core/Cpu/CpuRegisters.cs',
    'The GBA ARM7TDMI CPU holds values in registers while it works. R0–R15 each store 32 bits. R13 is normally the stack pointer, R14 the link register, and R15 the program counter. Today store sixteen raw values. Later lessons add mode banking and the special meaning of reading PC; this helper alone is not an accurate PC model. Our learning constructor starts storage at zero as a convenience, not a claim about power-on hardware.',
    'uint[] values = new uint[4];\nvalues[1] = 0xFFFFFFFFu;\nuint result = values[1];',
    '`uint` holds 0 through 4,294,967,295. A trailing `u` marks an unsigned literal. An array of uint holds separate 32-bit elements. Reuse the field/method pattern from EWRAM. A register number is an index; a register value can be a number, bits, or a guest address.',
    ['Create sixteen uint storage slots per CpuRegisters object.', 'Implement Read and Write for register numbers 0–15.', 'Keep objects independent; do not make the backing array static.'],
    ['R0 can hold a full 32-bit value.', 'R15 is an available storage slot.', 'Updating R1 preserves R0.', 'Separate CPU objects retain separate values.'],
    'This task resembles RAM, but the element width and number of elements differ. Do not truncate a register to byte.', 'docs/03-arm7tdmi/README.md',
    starter='''namespace Gba.Core.Cpu;
public class CpuRegisters
{
    // TODO: add per-object storage for sixteen 32-bit values.
    public uint Read(int register) => throw new NotImplementedException();
    public void Write(int register, uint value) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Registers_keep_32_bits() { var r=new CpuRegisters(); r.Write(0,0xFEDCBA98); Assert.Equal(0xFEDCBA98u,r.Read(0)); }
    [Fact] public void R15_has_storage() { var r=new CpuRegisters(); r.Write(15,0x08000000); Assert.Equal(0x08000000u,r.Read(15)); }
    [Fact] public void Register_slots_are_independent() { var r=new CpuRegisters(); r.Write(0,12); r.Write(1,34); Assert.Equal(12u,r.Read(0)); Assert.Equal(34u,r.Read(1)); }
    [Fact] public void CPU_objects_are_independent() { var a=new CpuRegisters(); var b=new CpuRegisters(); a.Write(0,12); b.Write(0,34); Assert.Equal(12u,a.Read(0)); }
''', count=4)

lesson(6, 'conditions', 'Deciding whether an ARM instruction runs', 'src/Gba.Core/Cpu/Conditions.cs',
    '''ARM instructions normally carry a four-bit condition. Test it against CPSR flags N/Z/C/V in bits 31/30/29/28. A failed condition leaves architectural results unchanged (timing is still consumed later).

| Code | Passes when | Code | Passes when |
| --- | --- | --- | --- |
| 0 EQ | Z | 1 NE | !Z |
| 2 CS | C | 3 CC | !C |
| 4 MI | N | 5 PL | !N |
| 6 VS | V | 7 VC | !V |
| 8 HI | C && !Z | 9 LS | !C || Z |
| A GE | N == V | B LT | N != V |
| C GT | !Z && N == V | D LE | Z || N != V |
| E AL | always | F NV | never in this ARMv4T learning contract |''',
    'bool enabled = (settings & 0x10u) != 0;\nbool ready = enabled && !busy;\n// settings is a uint and busy is a bool supplied by your caller.',
    'This is a syntax fragment, not a separate program. `!= 0` converts selected bits into a Boolean. `!`, `&&`, and `||` mean not, and, and or. A switch can choose one result for each condition code. Parentheses make grouped Boolean rules explicit. Implement a pure method: it returns a decision without changing CPSR.',
    ['Extract N, Z, C, and V as Booleans.', 'Translate the table into Matches(condition, cpsr).', 'Evaluate all codes 0–15; return false for F rather than importing newer ARM extensions.'],
    ['Every condition is checked against all sixteen flag combinations.', 'AL always passes and NV never passes.', 'Unrelated CPSR mode/control bits do not affect condition results.'],
    'Signed comparisons use N and V together. N alone does not tell you whether a signed subtraction was less than zero after overflow.', 'docs/04-arm-instruction-set/README.md',
    starter='''namespace Gba.Core.Cpu;
public static class Conditions
{
    public static bool Matches(int condition, uint cpsr) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void All_condition_truth_tables_match()
    {
        // Expected masks: bit k is the answer for flag nibble k (NZCV).
        ushort[] masks={0xF0F0,0x0F0F,0xCCCC,0x3333,0xFF00,0x00FF,0xAAAA,0x5555,0x0C0C,0xF3F3,0xAA55,0x55AA,0x0A05,0xF5FA,0xFFFF,0};
        for(int c=0;c<16;c++) for(int f=0;f<16;f++) Assert.Equal((masks[c]&(1<<f))!=0,Conditions.Matches(c,(uint)f<<28));
    }
    [Fact] public void Always_and_never_are_explicit() { Assert.True(Conditions.Matches(14,0)); Assert.False(Conditions.Matches(15,0xFFFFFFFF)); }
    [Fact] public void Mode_bits_do_not_change_conditions() { for(int c=0;c<16;c++) Assert.Equal(Conditions.Matches(c,0xA0000000),Conditions.Matches(c,0xA00000D3)); }
''', count=3)

lesson(7, 'arm-fields', 'Reading fields from an ARM instruction', 'src/Gba.Core/Cpu/ArmFields.cs',
    'An instruction is a number containing smaller fields. For an already-identified ARM data-processing instruction: opcode is bits 24–21, Rn bits 19–16, Rd bits 15–12, and bit 20 requests flag updates. Today extract only those fields. Identifying instruction families is a separate decision: multiply and other special encodings overlap broad data-processing patterns.',
    'uint packed = 0x00000AB0;\nint field = (int)((packed >> 4) & 0xFF);',
    'Move the field down until its lowest bit is at position zero, then mask away everything above its width. Eight bits use mask 0xFF; four bits use 0xF. Return a bool for a single flag. These static methods need no object because their output depends only on the supplied word.',
    ['Extract opcode, Rn, and Rd with shifts and masks.', 'Extract the S bit as a Boolean.', 'Keep decoding separate from changing register values.'],
    ['0xE2813005 identifies ADD (opcode 4), Rn=1, Rd=3, S=false.', '0xE3B02007 identifies MOV (opcode 13), Rd=2, S=true.', 'Different condition bits do not contaminate operand fields.'],
    'Write the bit positions above the word on paper. Use one mask per field rather than comparing the whole instruction.', 'docs/04-arm-instruction-set/README.md',
    starter='''namespace Gba.Core.Cpu;
public static class ArmFields
{
    public static int Opcode(uint word) => throw new NotImplementedException();
    public static int Rn(uint word) => throw new NotImplementedException();
    public static int Rd(uint word) => throw new NotImplementedException();
    public static bool SetsFlags(uint word) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Extracts_ADD_fields() { const uint w=0xE2813005; Assert.Equal(4,ArmFields.Opcode(w)); Assert.Equal(1,ArmFields.Rn(w)); Assert.Equal(3,ArmFields.Rd(w)); Assert.False(ArmFields.SetsFlags(w)); }
    [Fact] public void Extracts_MOV_and_S_bit() { const uint w=0xE3B02007; Assert.Equal(13,ArmFields.Opcode(w)); Assert.Equal(2,ArmFields.Rd(w)); Assert.True(ArmFields.SetsFlags(w)); }
    [Fact] public void Condition_bits_are_separate() { Assert.Equal(ArmFields.Opcode(0xE2813005),ArmFields.Opcode(0x12813005)); Assert.Equal(3,ArmFields.Rd(0x12813005)); }
''', count=3)

lesson(8, 'first-arm', 'Executing MOV, ADD, and SUB', 'src/Gba.Core/Cpu/ArmImmediate.cs',
    'MOV copies a value, ADD adds to a source register, and SUB subtracts from it. Begin with valid ARM immediate data-processing words whose rotation is zero, S=0, and operands are R0–R14. Evaluate the condition first. Opcode 13 is MOV, 4 is ADD, and 2 is SUB. The immediate value here is bits 7–0. Full rotated immediates, PC writes, flag updates, and timing are deliberately later work.',
    'uint total = unchecked(0xFFFFFFFFu + 1u);\n// total is 0: only the low 32 bits are retained.',
    '`unchecked` states that overflow wraps to the width of the integer. Reuse the field extractor and register object you already wrote. A switch statement can choose the arithmetic operation. Method calls such as `registers.Read(index)` retrieve existing component state; do not create a new register bank during execution.',
    ['Use Conditions.Matches to decide whether the instruction executes.', 'Decode fields and implement MOV, ADD, and SUB using the existing registers.', 'For a passing condition, throw NotSupportedException on any other opcode in this limited helper. Leave unrelated registers unchanged.'],
    ['MOV r0,#7 stores 7.', 'MOV, ADD, SUB sequence produces r0=7, r1=12, r2=10.', 'A failing EQ condition makes no register change.', 'Unsupported opcode 0 is reported, not silently treated as MOV.'],
    'The first argument to Execute is the encoded word, not an opcode number. Read Rn before writing Rd because they may name the same register.', 'docs/04-arm-instruction-set/README.md',
    starter='''namespace Gba.Core.Cpu;
public static class ArmImmediate
{
    public static void Execute(uint instruction, CpuRegisters registers, uint cpsr) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void MOV_stores_an_immediate() { var r=new CpuRegisters(); ArmImmediate.Execute(0xE3A00007,r,0); Assert.Equal(7u,r.Read(0)); }
    [Fact] public void Three_instructions_share_registers() { var r=new CpuRegisters(); ArmImmediate.Execute(0xE3A00007,r,0); ArmImmediate.Execute(0xE2801005,r,0); ArmImmediate.Execute(0xE2412002,r,0); Assert.Equal(7u,r.Read(0)); Assert.Equal(12u,r.Read(1)); Assert.Equal(10u,r.Read(2)); }
    [Fact] public void Failed_condition_preserves_state() { var r=new CpuRegisters(); r.Write(0,91); ArmImmediate.Execute(0x03A00007,r,0); Assert.Equal(91u,r.Read(0)); }
    [Fact] public void Unsupported_opcode_is_reported() { Assert.Throws<NotSupportedException>(()=>ArmImmediate.Execute(0xE2000001,new CpuRegisters(),0)); }
''', count=4)

lesson(9, 'arithmetic-flags', 'Carry and signed overflow', 'src/Gba.Core/Cpu/Arithmetic.cs',
    'The low 32 result bits do not tell the whole story. N is result bit 31; Z means the result is zero; C means an addition carried beyond bit 31, or a subtraction needed no borrow. V means the mathematical signed result does not fit in a signed 32-bit integer. Add and subtract should return result and NZCV together. Here Flags contains only bits 31–28; later the CPU merges them into CPSR while preserving other bits.',
    'ulong wide = (ulong)left + right;\nuint low = unchecked((uint)wide);\n// left and right are uint values supplied by the caller.',
    '`ulong` is a 64-bit unsigned integer, so an intermediate can retain carry. Casting an unsigned bit pattern to int inside unchecked interprets it as signed; a long intermediate can measure signed overflow. The supplied record struct groups two return values. Construct one with `new ArithmeticResult(value, flags)`; it is data, not a second CPU.',
    ['Implement Add returning the wrapped value plus N/Z/C/V.', 'Implement Subtract with C meaning no borrow.', 'Keep flags outside NZCV clear in this helper. Later extend the same reasoning to ADC, SBC, RSB, and RSC.'],
    ['FFFFFFFF + 1 → value 0, flags Z+C.', '7FFFFFFF + 1 → 80000000, flags N+V.', '0 − 1 → FFFFFFFF, N set and C clear.', '80000000 − 1 → 7FFFFFFF, C+V set.'],
    'Carry answers an unsigned question. Overflow answers a signed question. Test them separately instead of assuming they always match.', 'docs/03-arm7tdmi/README.md',
    starter='''namespace Gba.Core.Cpu;
public readonly record struct ArithmeticResult(uint Value, uint Flags);
public static class Arithmetic
{
    public static ArithmeticResult Add(uint left, uint right) => throw new NotImplementedException();
    public static ArithmeticResult Subtract(uint left, uint right) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Unsigned_addition_carries() { Assert.Equal(new ArithmeticResult(0,0x60000000),Arithmetic.Add(0xFFFFFFFF,1)); }
    [Fact] public void Signed_addition_overflows() { Assert.Equal(new ArithmeticResult(0x80000000,0x90000000),Arithmetic.Add(0x7FFFFFFF,1)); }
    [Fact] public void Subtraction_can_borrow() { Assert.Equal(new ArithmeticResult(0xFFFFFFFF,0x80000000),Arithmetic.Subtract(0,1)); }
    [Fact] public void Signed_subtraction_overflows() { Assert.Equal(new ArithmeticResult(0x7FFFFFFF,0x30000000),Arithmetic.Subtract(0x80000000,1)); }
''', count=4)

lesson(10, 'shifter', 'Shifts, rotations, and ARM operands', 'src/Gba.Core/Cpu/BarrelShifter.cs',
    '''ARM can shift operand 2 before the main operation. LSL inserts zeros on the right, LSR inserts zeros on the left, ASR repeats the sign bit, and ROR rotates bits around. Also return the last bit shifted out as carry. For register-specified shifts use the low eight bits of the amount; zero preserves value and carry. Handle amounts 32 and above explicitly: C# masks shift counts and does not implement ARM boundary rules for you.

For immediate shifts, encoded zero means LSL #0, LSR #32, ASR #32, or RRX (for ROR). RRX moves old carry into bit 31 and bit 0 into carry. A rotated immediate takes an 8-bit literal and rotates right by twice its 4-bit rotation field; zero rotation preserves carry.''',
    'int signed = unchecked((int)bits);\nint shifted = signed >> 3;\n// bits is a uint. Signed right shift extends the sign bit.',
    'Return both value and carry in a small record struct, like ArithmeticResult. An enum can name Lsl/Lsr/Asr/Ror. Use distinct methods or an explicit parameter for immediate versus register amounts: encoded zero has different meanings.',
    ['Start with LSL/LSR for amounts 1–31 and return the carry-out bit.', 'Add ASR/ROR and explicit 0/32/>32 cases for register shifts. Add immediate zero special cases and RRX.', 'Extend ARM execution to rotated immediates and register operand 2; use shifter carry for logical flag-setting operations.'],
    ['LSL(0x80000001,1) gives 2 and carry=true.', 'LSR #32 of 0x80000000 gives 0 and carry=true; a register amount of 0 preserves old carry.', 'ASR(0x80000000,32) gives FFFFFFFF and carry=true.', 'RRX of 2 with carry=true gives 80000001 and carry=false.', 'Rotating 0x80 right by 8 gives 80000000; rotating by zero preserves carry.'],
    'For LSL #32, carry is original bit 0; for LSR #32 it is bit 31. Beyond 32 both give zero value and zero carry. ASR at 32 or more repeats the sign. Nonzero ROR multiples of 32 preserve value but report bit 31 as carry.', 'docs/04-arm-instruction-set/README.md')

lesson(11, 'branches', 'Program flow and the visible PC', 'src/Gba.Core/Cpu/BranchUnit.cs',
    'Keep the address being executed separate from the PC value a guest instruction reads. In ordinary ARM operand reads, visible PC is instruction address +8; in Thumb it is +4. ARM B/BL uses a signed 24-bit displacement shifted left two, added to visible PC. BL also saves the following instruction address in LR. BX chooses Thumb when target bit 0 is one, ARM when zero, and aligns the fetch address accordingly. A branch replaces sequential fetch and refills the conceptual pipeline.',
    'int signedField = unchecked((int)(field << 8)) >> 8;\n// field contains 24 bits. Shifting through the sign bit extends its sign.',
    'Signed and unsigned arithmetic can represent the same bit pattern differently. Use int for a signed displacement and unchecked arithmetic for 32-bit address wrapping. A result record can hold Target, Link, and Thumb. This prevents hidden PC increments in several different helpers.',
    ['Add an instruction-address field to your CPU integration and one consistent visible-PC helper.', 'Implement ARM B/BL: decode displacement, optionally write LR, and replace the next fetch address.', 'Implement BX with state exchange and correct target alignment. Keep a sequential path for a failed condition.'],
    ['At ARM address 08000000, EA000000 branches to 08000008.', 'At the same address, EAFFFFFE branches back to 08000000.', 'EB000000 also writes LR=08000004.', 'BX to 08000005 selects Thumb and fetches at 08000004; an even target selects ARM and is word-aligned.', 'A failed conditional branch continues at instruction address +4.'],
    'A branch target is based on the visible PC, not simply the next instruction. Do not increment PC again after replacing the fetch address.', 'docs/03-arm7tdmi/README.md')

lesson(12, 'loads-stores', 'Moving values between registers and memory', 'src/Gba.Core/Cpu/SingleTransfer.cs',
    'ARM LDR/STR move words; LDRB/STRB move bytes. First implement immediate offsets, pre-indexed addressing, no writeback, with ordinary EWRAM. Compute the effective address from Rn, then access the bus. Extend MemoryBus with Read16/32 and Write16/32 for RAM, reusing your byte-order helper. Later add post-indexing, writeback, register offsets, halfwords and signed loads. On ARM7TDMI, an unaligned word load reads an aligned word then rotates it; this CPU rule is not the same as four arbitrary byte reads.',
    'uint address = add ? unchecked(baseAddress + offset) : unchecked(baseAddress - offset);',
    '`condition ? first : second` chooses one expression. Keep effective-address calculation separate from the bus access and base-register update, so a writeback cannot accidentally change the source address. Sign-extending a byte uses `unchecked((uint)(int)(sbyte)value)`; an ordinary byte load zero-extends.',
    ['Add RAM width access to MemoryBus, then implement immediate pre-indexed LDR/STR and byte variants.', 'Connect decoding to the CPU and preserve the condition check before any memory side effect.', 'Add post-index/writeback and unaligned word-load rotation. Expand halfword/signed transfers as separate small cases, using their distinct encodings.'],
    ['With r0=02000000 and r1=12345678, E5801000 stores r1; E5902000 reads it into r2.', 'A byte store changes exactly one byte; a byte load returns 0–255.', 'A failing condition neither writes memory nor updates Rn.', 'With aligned word 12345678 at A, a word load from A+1 returns 78123456.', 'Record separate cases for positive/negative offsets and pre/post indexing before expanding instruction families.'],
    'Byte writes are valid for EWRAM; do not later reuse this implementation blindly for VRAM, palette RAM, or OAM. Handle an unsupported encoding explicitly until implemented.', 'docs/06-bus-and-memory/README.md')

lesson(13, 'thumb', 'The first Thumb instructions', 'src/Gba.Core/Cpu/ThumbImmediate.cs',
    'Thumb instructions are 16 bits wide, but registers still hold 32 bits. Start with immediate MOV (top five bits 00100), CMP (00101), ADD (00110), and SUB (00111). Bits 10–8 select R0–R7 and bits 7–0 hold the immediate. MOV updates N/Z while preserving C/V. ADD, SUB, and CMP update NZCV; CMP does not write the result. Execute returns the updated CPSR while preserving all bits outside the flags it changes.',
    'ushort instruction = 0x2509;\nint index = (instruction >> 8) & 7;\n// index is 5. ushort stores one 16-bit Thumb encoding.',
    'Shifts on ushort are promoted to int. Convert the extracted immediate to uint when doing register arithmetic. Reuse Arithmetic for flags, instead of inventing a second rule for Thumb. A returned uint can replace the caller\'s CPSR; the supplied register object retains register changes.',
    ['Decode MOV/CMP/ADD/SUB immediate and the low register index.', 'Reuse Arithmetic for arithmetic flags; merge changed flag bits with old CPSR.', 'Return updated CPSR, leaving registers unchanged for CMP.'],
    ['MOV r5,#9 writes R5 and preserves C/V and control bits.', 'MOV 7, ADD 5, SUB 2 leaves R0=10 and C set after subtraction.', 'CMP equal values sets Z+C and leaves its source unchanged.'],
    'Thumb is another decoder feeding the same CPU state, not another CPU. Later add shifts, ALU/register forms, loads/stores, high registers, stack operations, and branches one family at a time.', 'docs/05-thumb-instruction-set/README.md',
    starter='''namespace Gba.Core.Cpu;
public static class ThumbImmediate
{
    public static uint Execute(ushort instruction, CpuRegisters registers, uint cpsr) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void MOV_preserves_carry_overflow_and_control() { var r=new CpuRegisters(); uint s=ThumbImmediate.Execute(0x2509,r,0xF000003F); Assert.Equal(9u,r.Read(5)); Assert.Equal(0x3000003Fu,s); }
    [Fact] public void Immediate_sequence_updates_shared_state() { var r=new CpuRegisters(); uint s=ThumbImmediate.Execute(0x2007,r,0x3F); s=ThumbImmediate.Execute(0x3005,r,s); s=ThumbImmediate.Execute(0x3802,r,s); Assert.Equal(10u,r.Read(0)); Assert.Equal(0x2000003Fu,s); }
    [Fact] public void CMP_sets_flags_without_writing() { var r=new CpuRegisters(); r.Write(2,9); uint s=ThumbImmediate.Execute(0x2A09,r,0x3F); Assert.Equal(9u,r.Read(2)); Assert.Equal(0x6000003Fu,s); }
''', count=3)

lesson(14, 'stack-transfers', 'Stacks and transferring several registers', 'src/Gba.Core/Cpu/BlockTransfer.cs',
    'A stack is RAM used through R13/SP. ARM LDM/STM transfer a register list in ascending register-number order to ascending memory addresses; IA/IB/DA/DB select the starting address and final base update. Thumb PUSH uses a descending full stack and POP restores from it. Thumb PUSH/POP has low-register bits 0–7 and an optional LR/PC bit. Start with ordinary registers and nonempty lists; user-bank transfers, PC effects, and empty-list quirks are explicit later cases.',
    'for (int i = 0; i < 8; i++)\n{\n    bool selected = (mask & (1 << i)) != 0;\n    // Process one selected item.\n}',
    'A bitmask represents a set without a List allocation. Count selected registers before choosing a starting address. Keep temporary transfer addresses separate from the visible base register so writes cannot disturb later transfers. You can reuse bus width methods and register access.',
    ['Implement STMIA/LDMIA for nonempty lists with base outside the list.', 'Add the other address modes and explicit writeback; route transfers through the bus in order.', 'Connect Thumb PUSH/POP to this behavior, including LR saving and PC restoration, then extend low-register Thumb loads/stores.'],
    ['STMIA r0!,{r1,r2} writes r1 at old R0 and r2 at old R0+4, then advances R0 by 8.', 'PUSH {r0,r1} with SP=02000100 writes r0 at 020000F8 and r1 at 020000FC; SP becomes 020000F8.', 'POP restores both values and the old SP.', 'No transfer happens when an ARM condition fails.', 'Give base-in-list, empty-list, and PC cases their own fixtures before calling those forms supported.'],
    'Stack order is not the same as repeatedly pushing registers in ascending order. Compute the final layout first.', 'docs/05-thumb-instruction-set/README.md')

lesson(15, 'more-cpu', 'Completing CPU families one at a time', 'src/Gba.Core/Cpu/CpuDispatch.cs',
    '''Your decoder now needs precise family matching. Check special patterns before broad data-processing patterns. For ARM, complete logical operations AND/EOR/ORR/BIC/MVN and tests TST/TEQ/CMP/CMN, then ADC/SBC/RSB/RSC, multiply/long multiply, swap, and status transfers. For Thumb, reuse the same arithmetic and bus behavior for ALU, high-register, SP/PC-relative, conditional branch, and two-halfword BL forms. This lesson is a repeated small loop: choose ONE row below, implement it, check it, then take the next. It is not a request to finish the CPU in one sitting.

| Next family | Observable change |
| --- | --- |
| Logical/test | Result or flags; test operations do not write Rd |
| Carry arithmetic | Includes carry-in or inverted borrow-in |
| Multiply | Low or long product, optionally accumulated |
| Swap | Exchange register value with bus memory |
| Status | Masked CPSR/SPSR reads/writes respecting privilege |
| Thumb remaining forms | Same registers/bus, narrower encodings |''',
    'bool matches = (word & fixedBitsMask) == expectedPattern;\n// Only fixed encoding bits belong in fixedBitsMask.',
    'Give each family its own small method instead of one enormous switch body. Use ulong for unsigned long products and long for signed long products. A delegate such as Action<uint> can name a handler, but a simple ordered if/switch dispatcher is enough. Unsupported encodings should report the word and PC.',
    ['For the next family, write its fixed-bit mask, operands, changed state, and one hand-computed before/after example beside its handler. Use the linked instruction reference for exact encodings.', 'Implement and check that family only. For test operations preserve Rd; for status writes preserve unselected fields.', 'Repeat the table, then add collision fixtures proving multiply/swap/status words cannot enter ordinary data-processing handlers.'],
    ['AND of F0 and 3C gives 30; TST changes flags without replacing a register.', 'ADC(FFFFFFFF,0,C=1) gives 0 with carry; SBC(5,2,C=0) gives 2.', 'Unsigned long multiplication FFFFFFFF × 2 gives high=1, low=FFFFFFFE.', 'A swap writes the old register value and returns the old memory value.', 'Thumb BL keeps the first-half intermediate state until the second half and returns a Thumb-state link address.', 'Each implemented family has a passing example and boundary case; unsupported families remain named diagnostics, never silent no-ops.'],
    'This is the point where an exact opcode table is useful. Ask for a single family’s mask, starter signature, and checks if stuck; the handler logic is still yours.', 'docs/04-arm-instruction-set/README.md')

lesson(16, 'exceptions', 'Banked registers and entering an exception', 'src/Gba.Core/Cpu/ExceptionUnit.cs',
    'CPU modes select different physical register banks. User/System share R0–R14; IRQ, Supervisor, Abort, and Undefined bank R13/R14; FIQ banks R8–R14. Each exception mode has an SPSR. Exception entry saves CPSR, selects the mode, stores an exception-specific LR, clears T for ARM state, applies interrupt masks, and fetches from a vector. SWI uses vector 08, IRQ 18, undefined instruction 04. For SWI, LR is the following instruction address. IRQ LR must support the architectural return sequence, not simply copy the visible PC.',
    'public enum CpuMode { User = 0x10, Irq = 0x12, Supervisor = 0x13 }\n// This example names three modes; your complete model adds the others.',
    'An enum gives names to numeric mode bits. Store banks in separate arrays/fields; selecting a bank changes which storage is visible. Save a uint status value by value. Do not alias current CPSR with a mutable saved-status object. Keep host NotImplementedException diagnostics separate from guest CPU exceptions.',
    ['Extend CpuRegisters with mode selection and banked storage without changing the existing raw-register API for ordinary access.', 'Implement SWI entry first, then IRQ and undefined entry with a deliberate internal instruction-address convention.', 'Implement exception-return status restoration and bank selection. Add Thumb SWI and test both ARM/Thumb return state.'],
    ['Switch User → IRQ → User: shared R0 survives, each mode retains its own SP/LR.', 'FIQ has a different R8; User/System share theirs.', 'ARM SWI at address A saves return A+4; Thumb SWI saves A+2, and both enter ARM Supervisor at 08.', 'Saved status restores Thumb state and the prior mode on return.', 'For IRQ, verify the return target using the intended SUBS PC,LR,#4 sequence.'],
    'Banking does not clear registers. Model entry as a sequence and record old state before changing modes.', 'docs/03-arm7tdmi/exceptions.md')

lesson(17, 'first-pixel', 'Turning a GBA color into a pixel', 'src/Gba.Core/Ppu/GbaColor.cs',
    'A direct GBA color uses five red bits (0–4), five green bits (5–9), and five blue bits (10–14). Bit 15 is unused, not alpha. Mode 3 stores one halfword per pixel for a 240×160 image. Start with color conversion only. Our host format is explicitly the integer 0xFFRRGGBB. Expand a five-bit channel to eight using bit replication: (channel << 3) | (channel >> 2). This chooses a deterministic conversion; actual LCD color response is a separate topic.',
    'uint packed = (0xFFu << 24) | (red << 16) | (green << 8) | blue;\n// red, green, blue are uint channel values from 0 through 255.',
    'Integer channel packing is a format contract, not an assumption about in-memory byte order. Mask each source channel before expanding it. A pure static Convert method can be checked without a window or GPU.',
    ['Extract the three five-bit channels.', 'Expand each channel with bit replication.', 'Pack an opaque 0xFFRRGGBB value and ignore source bit 15.'],
    ['001F becomes FFFF0000 (red).', '03E0 becomes FF00FF00 (green).', '7C00 becomes FF0000FF (blue).', 'FFFF becomes FFFFFFFF; channel value 16 expands to 132.'],
    'Red is in the low GBA bits but the high color byte of this host format. Write down both layouts before moving bits.', 'docs/07-ppu/bitmap-modes.md',
    starter='''namespace Gba.Core.Ppu;
public static class GbaColor
{
    public static uint Convert(ushort color) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Red_channel_is_placed_correctly() { Assert.Equal(0xFFFF0000u,GbaColor.Convert(0x001F)); }
    [Fact] public void Green_channel_is_placed_correctly() { Assert.Equal(0xFF00FF00u,GbaColor.Convert(0x03E0)); }
    [Fact] public void Blue_channel_is_placed_correctly() { Assert.Equal(0xFF0000FFu,GbaColor.Convert(0x7C00)); }
    [Fact] public void High_bit_is_not_alpha_and_midtones_expand() { Assert.Equal(0xFFFFFFFFu,GbaColor.Convert(0xFFFF)); Assert.Equal(0xFF840000u,GbaColor.Convert(0x0010)); }
''', count=4)

lesson(18, 'display-time', 'Counting scanlines', 'src/Gba.Core/Ppu/DisplayTiming.cs',
    'The GBA display advances through 228 lines per frame, with 1232 system cycles per line. Lines 0–159 are visible. For the DISPSTAT VBlank flag, lines 160–226 are set and line 227 clears it. The nominal drawing budget is 960 cycles, but the DISPSTAT HBlank flag starts at line-cycle 1006 and lasts to the next line. Today IsHBlank models that status flag, not every PPU/DMA access edge. Today track line and line-cycle, starting at zero in your fixture. Advance must retain leftover cycles across calls; a large advance can cross several lines. Rendering and interrupts are later consumers of these boundaries.',
    'int whole = total / 12;\nint remainder = total % 12;\n// Integer division counts full groups; % retains what remains.',
    'A property such as `public int Line { get; private set; }` exposes state for reading while only this component changes it. Accumulate in long if a public cycle count can be large, then reduce to bounded line/frame values. Do not discard remainder cycles after an event.',
    ['Store the current line and cycle within the line.', 'Implement Advance for a nonnegative cycle count and wrap after 228 lines.', 'Implement HBlank and VBlank properties using the precise boundaries above.'],
    ['At line-cycle 1005 the HBlank status flag is clear; one more cycle sets it.', '1232 cycles advances one line and resets line-cycle to zero.', 'Line 160 enters VBlank; line 227 clears the status flag.', 'A whole frame plus 5 cycles ends at line 0, cycle 5.'],
    'A frame is 280,896 cycles. Distinguish the line-160 event from a Boolean flag that is true across multiple lines.', 'docs/07-ppu/display-timing.md',
    starter='''namespace Gba.Core.Ppu;
public class DisplayTiming
{
    public int Line => throw new NotImplementedException();
    public int LineCycle => throw new NotImplementedException();
    public bool IsHBlank => throw new NotImplementedException();
    public bool IsVBlank => throw new NotImplementedException();
    public void Advance(int cycles) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void HBlank_status_begins_at_cycle_1006() { var d=new DisplayTiming(); d.Advance(1005); Assert.False(d.IsHBlank); d.Advance(1); Assert.True(d.IsHBlank); }
    [Fact] public void A_line_preserves_remainder_cycles() { var d=new DisplayTiming(); d.Advance(1200); d.Advance(39); Assert.Equal(1,d.Line); Assert.Equal(7,d.LineCycle); Assert.False(d.IsHBlank); }
    [Fact] public void VBlank_flag_has_both_boundaries() { var d=new DisplayTiming(); d.Advance(1232*160); Assert.True(d.IsVBlank); d.Advance(1232*67); Assert.Equal(227,d.Line); Assert.False(d.IsVBlank); }
    [Fact] public void A_frame_wraps_without_losing_cycles() { var d=new DisplayTiming(); d.Advance(1232*228+5); Assert.Equal(0,d.Line); Assert.Equal(5,d.LineCycle); }
''', count=4)

lesson(19, 'interrupts', 'Remembering interrupt requests', 'src/Gba.Core/Interrupts/InterruptController.cs',
    'Devices request attention by setting bits in IF. IE selects which requests are enabled; IME is the master switch; CPSR.I masks CPU IRQ acceptance. A masked request stays pending. Writing ones to IF acknowledges only those bits; zeros leave other requests alone. Today implement the latch and decision, not exception entry. Connect the decision to ExceptionUnit only after these checks pass.',
    'bits |= selected;\nbits &= ~selected;\n// First set selected bits; then clear only those selected bits.',
    '`|=` and `&=` update a variable with bitwise operations. `~` complements all bits of an integer, so mask to the register width where needed. Public auto-properties can hold IE and IME; IF should be changed only through Request/Acknowledge. The starter uses descriptive property names instead of abbreviations.',
    ['Implement Request and Acknowledge for source bits 0–13.', 'Implement ShouldTakeIrq from pending & enabled sources, master enable, and the CPU mask.', 'Keep a request pending when any gate is closed.'],
    ['Requesting bits 0 and 3 retains both.', 'Acknowledging bit 0 leaves bit 3 pending.', 'All gates must allow a request before IRQ is accepted.', 'Masking does not erase pending requests.'],
    'IF is not an ordinary assignment register. A write value of zero must not clear everything.', 'docs/08-interrupts/README.md',
    starter='''namespace Gba.Core.Interrupts;
public class InterruptController
{
    public ushort Enabled { get; set; }
    public bool MasterEnabled { get; set; }
    public ushort Pending => throw new NotImplementedException();
    public void Request(ushort sources) => throw new NotImplementedException();
    public void Acknowledge(ushort sources) => throw new NotImplementedException();
    public bool ShouldTakeIrq(bool cpuMasked) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Requests_accumulate() { var i=new InterruptController(); i.Request(1); i.Request(8); Assert.Equal((ushort)9,i.Pending); }
    [Fact] public void Acknowledgement_clears_only_written_ones() { var i=new InterruptController(); i.Request(9); i.Acknowledge(1); i.Acknowledge(0); Assert.Equal((ushort)8,i.Pending); }
    [Fact] public void IRQ_requires_all_gates() { var i=new InterruptController(); i.Request(1); i.Enabled=1; Assert.False(i.ShouldTakeIrq(false)); i.MasterEnabled=true; Assert.True(i.ShouldTakeIrq(false)); Assert.False(i.ShouldTakeIrq(true)); i.Enabled=2; Assert.False(i.ShouldTakeIrq(false)); }
    [Fact] public void Masked_requests_remain_pending() { var i=new InterruptController(); i.Request(2); Assert.False(i.ShouldTakeIrq(true)); Assert.Equal((ushort)2,i.Pending); }
''', count=4)

lesson(20, 'timers', 'One timer that reloads on overflow', 'src/Gba.Core/Timers/GbaTimer.cs',
    'A GBA timer has a 16-bit live counter and a separate reload value. Writing reload while running does not immediately replace the live counter. A disabled→enabled transition loads reload; overflow loads it again. The divisors are 1, 64, 256, 1024. First implement one non-cascade timer with divisor fixed for each enable period. Advance returns the number of overflows so other hardware can react later. Preserve a partial divisor across calls.',
    'public ushort Reload { get; set; }\n// An auto-property stores a value. More complex transitions belong in a method.',
    '`ushort` wraps at 16 bits, but use a wider intermediate to count overflows rather than losing them through a cast. A while loop can process repeated overflow events in a first implementation. Separate host method calls from emulated elapsed cycles.',
    ['Implement SetEnabled so only a rising enable edge loads Reload. Do not tick while disabled.', 'Accumulate cycles, consume full divisor ticks, and retain the remainder.', 'On each overflow reload the counter and count an event. Later connect four timers, cascade inputs, and IRQ requests.'],
    ['Enabling loads Reload.', 'With divisor 64, calls of 63 then 1 advance exactly one tick.', 'Reload FFFE and five ticks produce two overflows and counter FFFF.', 'A reload write while enabled waits until overflow; disabling stops advancement.'],
    'Avoid resetting the prescaler remainder every time Advance returns. Multiple timer overflows may happen in one call.', 'docs/09-timers/README.md',
    starter='''namespace Gba.Core.Timers;
public class GbaTimer
{
    public ushort Reload { get; set; }
    public int Divisor { get; set; } = 1;
    public ushort Counter => throw new NotImplementedException();
    public void SetEnabled(bool enabled) => throw new NotImplementedException();
    public int Advance(int cycles) => throw new NotImplementedException();
}''', tests='''
    [Fact] public void Enabling_loads_reload() { var t=new GbaTimer{Reload=123}; t.SetEnabled(true); Assert.Equal((ushort)123,t.Counter); }
    [Fact] public void Prescaler_remainder_is_retained() { var t=new GbaTimer{Reload=4,Divisor=64}; t.SetEnabled(true); t.Advance(63); Assert.Equal((ushort)4,t.Counter); t.Advance(1); Assert.Equal((ushort)5,t.Counter); }
    [Fact] public void Multiple_overflows_reload_each_time() { var t=new GbaTimer{Reload=0xFFFE}; t.SetEnabled(true); Assert.Equal(2,t.Advance(5)); Assert.Equal((ushort)0xFFFF,t.Counter); }
    [Fact] public void Reload_write_waits_and_disabled_timer_stops() { var t=new GbaTimer{Reload=0xFFFE}; t.SetEnabled(true); t.Reload=7; t.Advance(1); Assert.Equal((ushort)0xFFFF,t.Counter); t.Advance(1); Assert.Equal((ushort)7,t.Counter); t.SetEnabled(false); Assert.Equal(0,t.Advance(20)); Assert.Equal((ushort)7,t.Counter); }
''', count=4)

lesson(21, 'dma', 'Copying through the bus with DMA', 'src/Gba.Core/Dma/DmaChannel.cs',
    'DMA moves halfwords or words without the CPU executing each load/store. A channel latches source, destination, and count when enabled; bus reads/writes then consume guest time. Start with one immediate incrementing channel and a nonzero count. Count is transfers, not bytes. Four channels later add priority (0 highest), triggers, address control, repeat/reload, and completion IRQ. A zero count means the channel-specific maximum, not no work: 0x4000 units on channels 0–2, 0x10000 on channel 3.',
    'public enum AddressMode { Increment, Decrement, Fixed, Reload }\n// Named values make configuration easier to read than unexplained numbers.',
    'Use fields for latched running state separate from writable register values. A small Step method can perform one transfer and report consumed cycles; an immediate loop can call it until finished. Route through bus methods so device side effects are preserved.',
    ['Implement one nonzero immediate halfword copy through MemoryBus; add word width next.', 'Advance latched addresses according to transfer width, then add decrement/fixed/destination-reload behavior.', 'Connect four channels to scheduler triggers and completion IRQ; add repeat and zero-count decoding as separate cases.'],
    ['Copy three halfwords 1111,2222,3333: destination bytes and final addresses match six transferred bytes.', 'Word transfers advance incrementing addresses by four.', 'A fixed destination receives each successive source value at the same address.', 'HBlank-triggered DMA waits for its trigger; simultaneous eligible channels run in priority order.', 'A completion IRQ occurs once per completed transfer sequence, not once per unit.'],
    'Do not use Array.Copy: it bypasses the bus and its device behavior. Start with RAM fixtures before special FIFO DMA.', 'docs/10-dma/README.md')

lesson(22, 'keypad', 'Pressed buttons become zero bits', 'src/Gba.Core/Input/Keypad.cs',
    'KEYINPUT has ten active-low bits: zero means pressed. Bit order is A, B, Select, Start, Right, Left, Up, Down, R, L. Thus no buttons is 03FF; A alone is 03FE. Your input method accepts an active-high mask for convenience: one means the host says pressed. Convert it to the guest register without touching unrelated bits. KEYCNT interrupt matching and physical keyboard mapping come after this helper.',
    'ushort masked = (ushort)(value & 0x03FF);\n// The cast returns the masked result to a 16-bit type.',
    'Bitwise complement `~` acts on the promoted integer width, so retain only the ten keypad bits afterward. A stateful object can remember the latest pressed mask. Do not query a real keyboard in Core: pass logical button state in from the host.',
    ['Store a logical pressed mask through SetPressed.', 'Implement ReadInput to expose only the ten active-low bits.', 'Keep each Keypad object independent; later add KEYCNT OR/AND match and an injected IRQ request.'],
    ['No buttons reads 03FF.', 'A pressed reads 03FE.', 'A+Start reads 03F6; releasing A leaves 03F7.', 'Bits above bit 9 in the host mask are ignored.'],
    'For the guest, pressing clears a bit. For your host-facing input, pressing sets a bit. Name the two representations clearly.', 'docs/11-input/README.md',
    starter='''namespace Gba.Core.Input;
public class Keypad
{
    public void SetPressed(ushort mask) => throw new NotImplementedException();
    public ushort ReadInput() => throw new NotImplementedException();
}''', tests='''
    [Fact] public void No_buttons_are_all_ones() { var k=new Keypad(); k.SetPressed(0); Assert.Equal((ushort)0x03FF,k.ReadInput()); }
    [Fact] public void A_press_clears_bit_zero() { var k=new Keypad(); k.SetPressed(1); Assert.Equal((ushort)0x03FE,k.ReadInput()); }
    [Fact] public void Releasing_one_button_preserves_the_other() { var k=new Keypad(); k.SetPressed(9); Assert.Equal((ushort)0x03F6,k.ReadInput()); k.SetPressed(8); Assert.Equal((ushort)0x03F7,k.ReadInput()); }
    [Fact] public void Only_ten_button_bits_are_exposed() { var k=new Keypad(); k.SetPressed(0xFC00); Assert.Equal((ushort)0x03FF,k.ReadInput()); }
''', count=4)

lesson(23, 'machine-time', 'Connecting components to one guest clock', 'src/Gba.Core/Common/GbaMachine.cs',
    'A GBA instruction, DMA transfer, timer, and scanline share guest time. Your PC running faster must not make timers count differently. Build one owner for CPU, bus, PPU timing, timers, DMA, and IRQ state. First run a deterministic instruction or fixed-cycle fixture; later use bus sequential/nonsequential wait states and instruction internal cycles. HALT stops CPU execution but relevant devices continue. Pause, unlike HALT, stops advancing the whole guest.',
    'public readonly record struct StepResult(int Cycles);\n// Return work consumed instead of reading DateTime inside emulated hardware.',
    'Composition means one object holds references to the pieces you already made. Constructor parameters supply those references. Use long for cumulative cycle counts. Process events at their boundaries rather than advancing every component by a whole frame and hoping their order matches.',
    ['Connect CPU fetch/decode/execute to the bus and define what one Step returns. Add IWRAM, ROM, BIOS storage, and required I/O routing as separate regions.', 'Advance timing and timers by consumed cycles; deliver HBlank/VBlank/timer events to DMA and IRQ in a documented order.', 'Expand to all four timers with cascade; add HALT and distinguish it from host pause. Keep hardware state changes in one controlled thread initially.'],
    ['Running the same fixture as one cycle batch or many small batches reaches the same counter/line state.', 'A timer overflow feeds its cascade successor and IRQ once per event.', 'HALT allows a display/timer event to become pending; pause changes no guest state.', 'A memory-mapped IF write acknowledges rather than replacing the latch.', 'Record event order for coincident timer/display/DMA activity; rerunning produces the same trace.'],
    'Start by returning a deliberately limited cycle cost and label it approximate. Replace that cost at one boundary as timing accuracy grows; do not scatter host clocks through components.', 'docs/14-timing-and-scheduling/README.md')

lesson(24, 'tiles', 'Drawing a tiled background', 'src/Gba.Core/Ppu/TextBackground.cs',
    'A regular background map selects 8×8 tiles. A 16-bit map entry contains tile number in bits 0–9, horizontal/vertical flip in bits 10/11, and the 4bpp palette bank in bits 12–15. A 4bpp tile is 32 bytes; its first pixel is the low nibble. An 8bpp tile is 64 bytes. Color index zero is transparent for background composition. Begin with one 32×32-tile map, 4bpp, no scrolling; then add flips, palette banks, larger maps, and scroll wrapping.',
    'int cellX = x / 8;\nint withinCellX = x % 8;\n// Quotient selects a tile; remainder selects a pixel inside it.',
    'Use a flat array for image buffers and compute `y * width + x`. Keep coordinate selection, tile-byte lookup, palette lookup, and transparency separate. A pixel result can carry both a color and a Boolean visible flag; black and transparent are different.',
    ['Render a synthetic 8×8 4bpp tile through your palette and GbaColor converter.', 'Read map entries to select tiles and implement H/V flip plus palette bank.', 'Add scrolling, 8bpp, and 256/512-pixel map sizes one fixture at a time; connect BG control registers through the bus.'],
    ['A tile with first byte 21 (hex) draws palette index 1 then 2.', 'A distinct corner marker moves to the opposite corner under each flip.', 'Palette index zero lets the backdrop show through.', 'Scrolling across an 8-pixel boundary selects the adjacent tile without a gap.', 'For 512-pixel maps, verify screen-block selection rather than assuming one flat 64×64 map in memory.'],
    'Use an asymmetric test tile, with different colors in all corners. A symmetric checkerboard can hide a flipped-coordinate bug.', 'docs/07-ppu/tile-modes.md')

lesson(25, 'sprites', 'Objects on top of backgrounds', 'src/Gba.Core/Ppu/Objects.cs',
    'Sprites are called objects (OBJ). The GBA has 128 OAM entries, each eight bytes. Attribute 0 contains Y and mode/shape information, attribute 1 X and size/flip information, and attribute 2 tile index, priority, and palette bank. Coordinates wrap in their hardware bit widths. Start with one regular square 8×8 4bpp object; transparent index zero contributes no pixel. Bitmap modes restrict usable OBJ tile memory, so keep your first fixture in a tile display mode.',
    'public readonly record struct PixelCandidate(uint Color, int Priority, int ObjectIndex);',
    'A result record carries metadata needed later by composition. Returning only a final color too early loses tie-breaking information. Use explicit sign/wrap conversion for coordinates; a large stored coordinate may put an object partly off the left or top edge.',
    ['Read one regular square object and sample its tile pixels through OBJ palette memory.', 'Add flips and wrapped positions, then size/shape combinations and 1D/2D tile mapping.', 'Evaluate multiple OAM entries with priority and index ties; keep affine objects as the next lesson’s separate coordinate transform.'],
    ['An 8×8 object at (10,20) covers the intended eight pixels each way.', 'Transparent holes reveal a background pixel.', 'X=511 places the left edge at −1 after wrapping, showing only the visible portion.', 'Two regular objects with equal priority choose the lower OAM index at an overlap.', 'Switching 1D/2D mapping changes row tile addresses as expected for a multi-tile object.'],
    'Read one object into a small decoded state before rendering it. OAM is not an array of host-side sprite objects with independent fields.', 'docs/07-ppu/sprites.md')

lesson(26, 'affine-bitmaps', 'Affine sampling and the other bitmap modes', 'src/Gba.Core/Ppu/AffineBackground.cs',
    'Affine backgrounds transform screen coordinates into source coordinates using fixed-point coefficients. Begin with identity, then translation and scaling. Mode 3 is 240×160 direct color at VRAM base. Mode 4 is 240×160 palette indexes; Mode 5 is 160×128 direct color inside the 240×160 display. Modes 4/5 have page bases separated by 0xA000, selected by DISPCNT bit 4. BG2 must be enabled. Direct-color black is opaque, while indexed Mode 4 index zero participates as transparency.',
    'int fixedValue = 3 << 8;\nint integerPart = fixedValue >> 8;\n// Eight fractional bits represent 3.0 as 768.',
    'Fixed-point arithmetic stores fractions in integer bits. Sign-extend coefficients/reference values at their actual register widths before using them. Preserve internal reference accumulators where hardware behavior needs them; do not round to an integer after every addition.',
    ['Render a Mode 3 frame from synthetic VRAM with identity BG2 sampling and GbaColor.', 'Implement Mode 4 palette lookup/page selection, then Mode 5 dimensions/page selection.', 'Add affine BG sampling and affine OBJ matrices; test identity before scale/rotation, then add wrapping/bounds rules and per-line reference updates.'],
    ['Mode 3 corners have distinct expected colors and rows are 240 pixels wide.', 'Toggling page select in Mode 4 changes the image without moving the palette.', 'Mode 5 leaves the area outside its sampled image to composition rather than stretching it automatically.', 'Identity affine sampling matches the non-transformed fixture.', 'A translation moves a unique marker by the predicted amount; negative coordinates are handled deliberately.'],
    'Do not place the second page immediately after the used pixel data. Its base is a hardware address offset, not an image-size calculation.', 'docs/07-ppu/bitmap-modes.md')

lesson(27, 'composition', 'Choosing the final visible pixel', 'src/Gba.Core/Ppu/Compositor.cs',
    'The final pixel is selected from enabled BG/OBJ candidates and the backdrop. Lower priority numbers win; tie rules depend on layer type (OBJ is ahead of a BG at the same priority; equal-priority BGs use lower BG number). Windows control which layers and color effects apply at a position. Blending acts on selected first/second targets, not every pair of colors. Start with priority and transparency before adding effects. Mosaic repeats sampled blocks rather than simply scaling the completed image.',
    'int bounded = Math.Min(31, Math.Max(0, channel));\n// Clamp after arithmetic, not before you have computed the result.',
    'Separate candidate selection from color math. A tuple or record can retain layer identity, priority, and effect eligibility. Alpha coefficients use integer arithmetic and bounded ranges: the GBA channels are still five-bit values during these effects.',
    ['Choose a visible candidate using enable bits, transparency, priority, and ties.', 'Apply window masks before selection/effects; include OBJ-window behavior separately.', 'Add alpha, brighten/darken, and mosaic with small pixel fixtures, then connect display flags and mid-frame register writes at your chosen timing precision.'],
    ['A transparent top candidate reveals the next visible one; opaque black hides it.', 'OBJ versus BG and BG versus BG ties follow their documented order.', 'A window boundary changes exactly the intended pixel range.', 'Alpha at coefficients 8 and 8 produces the expected half-strength contribution from each selected target, clamped at 31.', 'Brighten at full coefficient produces white; darken produces black; disabled effects preserve the selected color.', 'State the remaining scanline versus per-pixel timing limits instead of treating a static image as full PPU accuracy.'],
    'First make a table of two or three candidates for one pixel and choose the winner on paper. Only then add an effect.', 'docs/07-ppu/composition.md')

lesson(28, 'desktop-display', 'Showing your framebuffer in a window', 'src/Gba.Desktop/Window/EmulatorWindow.cs',
    'The GBA produces a 240×160 image; your desktop host presents those pixels. Vulkan and GLFW belong to the host, not to emulated memory or CPU behavior. Start by showing a synthetic image using the planned Silk.NET/Vulkan/GLFW backend, then connect the PPU buffer. Window creation, package versions, device setup, swapchain plumbing, and synchronization are support work you may ask me to implement; your learning task is the framebuffer handoff and visible result.',
    'using var resource = CreateResource();\n// A resource implementing IDisposable is released when this scope ends.',
    'This syntax fragment explains lifetime. Managed arrays are collected automatically; GPU/window resources need explicit disposal in the right order. A ReadOnlySpan<uint> describes a temporary view of pixels; it must not be stored for later use after its owner changes/disappears. For asynchronous upload, copy or hand off an owned buffer.',
    ['Define the host handoff: 240×160 pixels, known channel format, and who owns the buffer during presentation.', 'Connect a synthetic asymmetric frame to the host backend. Have setup/plumbing supplied if needed; do not put Vulkan types into Core.', 'Connect completed PPU frames, preserving aspect ratio and nearest/integer scaling. Handle resize and orderly shutdown.'],
    ['Four distinct corners appear in the correct positions and channels.', 'Resize preserves aspect ratio and introduces borders where necessary.', 'Repeated open/resize/close does not leak resources or report validation errors.', 'The displayed frame is complete, not half from one guest frame and half from another.'],
    'The existing host is a placeholder, so the first build does not create a window. This is an observed integration lesson, not an automatic GPU test. Treat backend setup as assistance work, not a new prerequisite course.', 'docs/15-vulkan-output/README.md')

lesson(29, 'boot', 'Loading a program and choosing a boot state', 'src/Gba.Core/Cartridge/BootSession.cs',
    'A ROM image does not run until the CPU has a deliberate starting state and can fetch it through the bus. Map cartridge reads at 08000000 and the other wait-state windows as appropriate. BIOS code normally provides initialization and services; starting directly at ROM requires an explicit alternative boot contract. Begin with a synthetic instruction sequence in RAM or ROM, then a diagnostic, and only then a chosen game. Do not pretend that setting PC alone reproduces BIOS startup.',
    'byte[] image = File.ReadAllBytes(path);\n// In the desktop host: read the file, then pass bytes into Core.',
    'A host path is a string; guest addresses are uint values. Catch file errors around host loading and show them before replacing the current session. Constructor arguments or a configuration record can describe BIOS-present versus explicit diagnostic boot modes without scattering special cases through CPU instructions.',
    ['Connect a byte image to RomImage and guest ROM address windows; preserve ROM as read-only input.', 'Define a synthetic boot fixture with explicit PC, SP, mode, instruction state, RAM, and expected final signature.', 'Load the local BIOS through the supplied desktop BiosFile.Load() helper, pass its bytes into Core, and map its 16 KiB at guest addresses 00000000–00003FFF. Execute it with your CPU, then diagnose the first divergence for a selected diagnostic or game.'],
    ['A tiny MOV/ADD/STR fixture writes the hand-computed signature into EWRAM.', 'The same image runs identically twice from the same reset state.', 'A missing/unreadable ROM leaves the existing session intact and shows a useful message.', 'Unsupported instructions/BIOS behavior report an address and operation rather than silently advancing.', 'A selected game boot screen is an observed milestone; record its remaining feature requirements.'],
    'If a real game fails, return to the first wrong instruction or device event. Adding unrelated opcodes is less useful than following one reproducible divergence.', 'docs/12-cartridges-and-roms/loading-and-playing.md')

lesson(30, 'play-controls', 'Run, pause, reset, and buttons', 'src/Gba.Desktop/Input/SessionControls.cs',
    'Your host controls a session; the guest sees logical buttons and advancing time. Pause freezes all guest state while the window still responds. Reset starts a fresh guest state for the same cartridge while preserving persistent save data. Switching ROMs creates a new guest session and loads that game’s own save. KEYINPUT is read-only guest input; KEYCNT selects optional keypad IRQ sources and OR/AND matching.',
    'public enum SessionState { Stopped, Running, Paused }\n// Named states make allowed transitions explicit.',
    'Convert host key-down/key-up events into a pressed-bit mask, then pass it to Keypad. Keep input state updates and CPU execution synchronized, initially on one thread if possible. Separate Reset from clearing every file or every object indiscriminately.',
    ['Connect physical keys to the logical keypad and clear held host inputs appropriately on focus loss.', 'Add run/pause/resume/reset through one session controller.', 'Add Open ROM and game switching with visible errors; implement KEYCNT source matching and feed its guest IRQ request into the existing controller.'],
    ['Press/release A changes KEYINPUT and a supported game/menu responds.', 'Pause freezes the cycle count; the window can still resize and resume.', 'Reset reproduces boot state but does not erase a saved game.', 'Switching games does not retain the previous CPU registers or held keys.', 'KEYCNT OR matches one selected pressed key; AND requires all selected keys, with empty-selection behavior tested from the hardware reference.'],
    'Close the old session only after the new image and save have loaded successfully. UI event handling is host plumbing; the guest input semantics are your component.', 'docs/11-input/README.md')

lesson(31, 'sram', 'Keeping a game save after the app closes', 'src/Gba.Core/Cartridge/SramSave.cs',
    'Cartridge save memory is separate from ROM and volatile work RAM. Begin with a configured SRAM cartridge: byte reads/writes change a save buffer and mark it dirty. Desktop loads a matching save before running the guest, and writes dirty bytes at controlled boundaries. The original .gba stays unchanged. Identify saves by cartridge identity, not merely a short display title that two games could share.',
    'byte[] snapshot = (byte[])saveBytes.Clone();\n// Capture a stable snapshot before handing bytes to file-writing code.',
    'A dirty flag tracks changed data, not successful disk persistence. Clear it only after the corresponding snapshot is safely written, accounting for any newer changes. Use host file APIs outside the memory device. Saving through a temporary file and replacement keeps the previous good save when an update fails.',
    ['Implement configured SRAM byte storage and guest bus routing; keep it separate from ROM.', 'Add load/export snapshots and dirty tracking; supply host file persistence plumbing if needed.', 'Integrate save loading/flushing with Open ROM, reset, switching games, and orderly close.'],
    ['Write a marker through the guest bus, persist, fully close, reopen, and read the same marker.', 'Two different cartridge identities have independent saves.', 'A failed disk write preserves the previous good save and keeps new data dirty.', 'A supported game’s Save → close → reopen → Continue works through the normal app path.', 'The ROM file’s bytes remain unchanged.'],
    'First verify a tiny byte marker independently of a game. Then test the in-game save protocol and host persistence together.', 'docs/12-cartridges-and-roms/saving-and-resuming.md')

lesson(32, 'flash', 'Flash saves are a command-driven device', 'src/Gba.Core/Cartridge/FlashSave.cs',
    'Flash is not SRAM with a larger array. Software sends command sequences to select identification, programming, erasing, or bank switching. Common unlock writes are AA to offset 5555 then 55 to 2AAA; the next command selects an operation. Device size and IDs belong to a selected cartridge/device profile. Erased bytes are FF. Start with one explicit profile and one command at a time; do not guess save type by treating every write as raw data.',
    'public enum FlashPhase { Idle, Unlock1, Unlock2, ProgramByte }\n// A phase remembers where you are in a multi-write protocol.',
    'Use a state machine: each write sees current phase, address, and value, then changes phase or storage. An enum makes transitions inspectable. Persistence exports the byte storage; an emulator save state must also retain any in-progress command state.',
    ['Implement unlock tracking, ID read mode, and reset-to-read for one named Flash profile.', 'Add byte programming and sector/chip erase using that profile’s protocol and geometry.', 'Add 128 KiB banking as a separate profile, then connect storage persistence through the SRAM lesson’s host mechanism.'],
    ['Ordinary writes without a valid command sequence do not behave like SRAM writes.', 'ID mode reports the configured IDs; reset returns to array reads.', 'Programming affects the selected location according to Flash bit-programming rules; erase returns its region to FF.', 'An invalid/interrupted command sequence recovers predictably without corrupting unrelated bytes.', 'Switching banks reveals independent data, and close/reopen preserves both banks.'],
    'Draw the command phases for a single byte program before writing the transition code. Use the exact command/device table in the reference for IDs and erase sizes.', 'docs/12-cartridges-and-roms/README.md')

lesson(33, 'eeprom', 'A save protocol sent one bit at a time', 'src/Gba.Core/Cartridge/EepromSave.cs',
    'EEPROM save access is serial: bus transfers carry protocol bits rather than ordinary addressed bytes. Common GBA EEPROM capacities use six or fourteen address bits, transferring a 64-bit data block per command. The large addressing form has unused address bits that must be handled as specified. Command framing, stop bits, read dummy bits, and routing depend on the cartridge mapping. Start with a configured size so detection does not obscure the protocol.',
    'int collected = 0;\nulong block = 0;\n// A counter tracks how many bits of a command or block have arrived.',
    'A state machine plus a bit counter is enough. ulong holds 64 data bits; avoid shifting by 64 because C# masks shift counts. Collect or emit one bit at a time in an explicit order. Keep command state separate from persistent storage.',
    ['Decode read/write command framing for one configured EEPROM size using the reference’s bit sequence.', 'Collect address/data bits and implement block write plus dummy/read-data output.', 'Add the second capacity, bus/DMA routing, and persistence without confusing EEPROM commands with ROM reads.'],
    ['A complete serial write followed by read returns the same asymmetric 64-bit pattern.', 'Two neighboring block addresses remain independent.', 'Read output begins with the documented dummy bits before data.', 'A partial command does not accidentally become a completed write.', 'The same EEPROM data survives a full close/reopen, while save states also preserve partial protocol state.'],
    'Use a pattern such as 0123456789ABCDEF rather than all-zero/all-one data: it exposes reversed bit order.', 'docs/12-cartridges-and-roms/README.md')

lesson(34, 'square-audio', 'A sound channel as changing numeric output', 'src/Gba.Core/Apu/SquareChannel.cs',
    'Begin audio as numbers over guest time, before using a speaker. The legacy sound channels have phase/frequency, length, envelope, and trigger state. A square channel cycles through a duty pattern; trigger initializes the channel’s internal state. Choose square channel 2 first to avoid channel 1’s extra sweep behavior. Register writes configure the channel; simply generating Math.Sin samples does not reproduce it.',
    'int phase = 0;\nint output = enabled ? amplitude : 0;\n// State advances from guest clocks, not from the desktop audio callback.',
    'An array can hold a small duty pattern; a bounded integer selects its current entry. Keep oscillator timing separate from the slower envelope/length clocks. Return a numeric sample/level so it can be checked before host audio exists.',
    ['Implement channel 2 duty stepping and frequency timing from its configured period.', 'Add trigger, DAC enable, length, and volume envelope in separate steps.', 'Connect sound register reads/writes and test batched versus split guest-cycle advancement.'],
    ['A fixed frequency repeats the selected duty pattern after the expected guest-cycle period.', 'Duty changes alter high/low proportions rather than merely changing volume.', 'Length expiry silences the channel when length control is enabled.', 'Envelope ticks change volume at the configured rate and stop at its limit.', 'One large Advance and many smaller Advances produce the same phase, envelope, and output.'],
    'Capture a short list of numeric output changes and their cycle positions. Listening alone cannot reveal an off-by-one phase or envelope tick.', 'docs/13-audio/README.md')

lesson(35, 'wave-noise', 'The other legacy sound sources', 'src/Gba.Core/Apu/LegacyAudio.cs',
    'The remaining legacy sources add channel 1 frequency sweep, wave RAM playback, and noise from a linear feedback shift register (LFSR). Wave samples are packed four-bit values. Noise is a deterministic bit sequence, not a call to Random. Sound routing and master controls determine which channels reach the left/right mix. Implement one source at a time and retain separate channel state.',
    'int highNibble = packed >> 4;\nint lowNibble = packed & 0xF;\n// This extracts two four-bit samples; playback order follows the hardware format.',
    'Bit fields and small state machines are reusable ideas, not new architecture. Use ushort for a bounded LFSR but explicitly apply the hardware feedback and width rules. Avoid allocations in the steady per-sample/per-cycle path once correctness is established.',
    ['Add channel 1 sweep to the existing square-channel behavior, including overflow/disable cases.', 'Implement wave RAM nibble playback and banking/volume controls.', 'Implement the noise LFSR widths and clock selection, then route all four sources through master and left/right controls.'],
    ['A known wave pattern plays nibbles in the documented order and repeats at the configured period.', 'Sweep changes frequency on its own clock and handles overflow disable.', 'Noise from a fixed initial state produces the same bit sequence on every run.', 'Changing noise width changes the sequence without using a random generator.', 'Muting one route affects only that channel/side, not oscillator phase in unrelated channels.'],
    'Test wave/noise as numeric sequences. A deterministic wrong sound is easier to diagnose than a host-audio timing problem mixed with a wrong generator.', 'docs/13-audio/README.md')

lesson(36, 'direct-sound', 'Timer-driven audio FIFOs and DMA refill', 'src/Gba.Core/Apu/DirectSound.cs',
    'Direct Sound A/B consume signed eight-bit samples from 32-byte FIFOs on their selected timer overflows. A 32-bit FIFO write contributes four samples in little-endian byte order. When the FIFO drops to its refill threshold (16 bytes or fewer), it can request the special sound DMA transfer. The callback from your desktop audio device must not directly consume the guest FIFO; only guest timer events do that.',
    'sbyte signedSample = unchecked((sbyte)rawByte);\n// FF represents -1, not an unsigned amplitude of 255.',
    'A ring buffer uses a fixed array, read index, write index, and count. Modulo wraps positions. Keep the current output sample separate from queued data; its lifetime follows timer consumption. A refill request is a device event delivered to DMA, not a recursive arbitrary memory copy.',
    ['Implement each FIFO’s fixed-capacity queue and four-byte writes.', 'Connect selected timer overflows to sample consumption, reset behavior, and DMA refill requests.', 'Add special FIFO DMA semantics and route A/B sample levels into the guest mixer.'],
    ['Writing 807F00FF yields signed samples −1,0,127,−128 in that order.', 'No selected timer overflow means no sample is consumed.', 'Crossing the refill threshold requests sound DMA; the transfer refills the queue using the required fixed destination.', 'Reset clears queue state as specified without resetting unrelated audio channels.', 'A fixed guest timer/input stream gives identical output regardless of desktop callback chunk size.'],
    'Test the ring-buffer wrap with more than one cycle through its capacity. Keep overflow/underflow behavior explicit and compare it with the hardware reference.', 'docs/13-audio/README.md')

lesson(37, 'host-audio', 'Mixing and playing the sound', 'src/Gba.Desktop/Audio/AudioOutput.cs',
    'Guest channel levels must be routed/mixed with sound controls and bias, then resampled to the host device rate. The guest clock determines the signal; the host consumes buffered samples. If the host needs more data, that is a buffering concern, not permission to change a timer period. Begin with a synthetic tone and a bounded queue, then connect your guest mix. Non-SDL backend setup and device plumbing can be supplied as assistance.',
    'Span<float> output = buffer.AsSpan();\n// A span gives temporary access to existing storage without copying it.',
    'A Span cannot be kept across arbitrary asynchronous work. Hand callbacks owned buffers or fill the provided span during the callback. Use a fractional resampling position so rounding each sample independently does not drift. Keep callbacks small and avoid file access or allocation in the steady path.',
    ['Implement guest routing, levels, saturation/bias, and a deterministic resampling boundary.', 'Have the host audio device/queue plumbing supplied or connect it to AudioOutput; verify a known synthetic tone first.', 'Feed guest mixed samples, then handle pause, resume, underrun, and close without changing guest timing.'],
    ['A known synthetic tone has stable pitch and the intended left/right routing.', 'A muted route produces silence on that side.', 'Long playback does not steadily grow the queue or accumulate drift.', 'Pause/resume does not play seconds of stale buffered audio.', 'Repeated close/reopen releases the device and a supported game’s audio plays with bounded latency.'],
    'Compare guest sample sequences before listening to resampled output. This separates emulation mistakes from buffering and device problems.', 'docs/13-audio/README.md')

lesson(38, 'save-states', 'Restoring an exact emulated moment', 'src/Gba.Core/Common/SaveState.cs',
    'An emulator save state captures the machine, unlike a game’s cartridge save. Include CPU banks/status/pipeline convention, every memory device, timer remainders, DMA latches, interrupt requests, PPU internal state, audio phases/FIFOs, scheduler time, and in-progress Flash/EEPROM commands. Include a format version and ROM identity. Host window/GPU/audio handles are not guest state and must be reconstructed or rebound.',
    'public sealed record SnapshotHeader(int Version, string RomId);\n// A record can describe data; mutable arrays inside it still need copies.',
    'A shallow object copy shares arrays and can silently change your saved snapshot. Copy mutable guest data deliberately. Parse/validate a state into temporary data before replacing the running machine. Use an explicit versioned representation rather than serializing arbitrary host objects.',
    ['Capture an owned snapshot of all guest state and restore it into a compatible machine.', 'Add version/ROM validation and host file slots; reject malformed/incompatible files before changing the current session.', 'Decide and show how loading an older state affects later cartridge-save persistence. Refill host output buffers from restored guest state.'],
    ['Run N steps, snapshot, run M, restore, run the same M: registers, memory, frame, and audio sequence agree.', 'Taking a snapshot then changing RAM does not change the snapshot.', 'Restoring midway through a timer divisor, DMA transfer, or EEPROM command resumes the same behavior.', 'A wrong-ROM or corrupt state leaves the running machine intact.', 'The normal Save State/Load State UI works after fully closing and reopening the app.'],
    'Deterministic replay is a stronger check than seeing the same picture immediately after loading.', 'docs/12-cartridges-and-roms/saving-and-resuming.md')

lesson(39, 'debugger', 'Finding the first wrong step', 'src/Gba.Core/Common/TraceRecorder.cs',
    'A debugger should explain guest execution without changing it. Start with a bounded instruction trace: address, ARM/Thumb state, instruction bits, register/flag changes, and elapsed guest cycles. Add a breakpoint before execution and a memory inspection path that does not trigger read side effects. The first divergent instruction or event is usually more useful than the final corrupted screen.',
    'public readonly record struct TraceEntry(uint Address, uint Instruction, long Cycle);',
    'A bounded ring buffer prevents an always-on trace from growing indefinitely. Capture values at a defined moment rather than retaining mutable references to registers. An inspection API may need a separate Peek operation from guest Read, because reading a device can itself have behavior.',
    ['Capture a bounded trace around CPU steps and significant device events.', 'Add address breakpoints/single-step and a side-effect-free inspection path for supported devices.', 'Compare a small deterministic fixture against a trusted trace/expected states and stop at the first mismatch.'],
    ['Tracing enabled versus disabled leaves final guest state identical.', 'A breakpoint stops before the target instruction changes registers.', 'Inspecting a register/device does not acknowledge IRQs or consume FIFO data.', 'The trace wraps within its configured capacity.', 'A deliberate fault in a local test fixture is localized to the first wrong step, then removed.'],
    'The UI for trace tables and memory views is assistance-friendly host work. The important emulator decision is when and what guest state to capture.', 'docs/17-debugging-tools/README.md')

lesson(40, 'compatibility', 'Making one game reliably playable', 'src/Gba.Core/Common/CompatibilityNotes.cs',
    'A passing small lesson checks its stated behavior, not all hardware. Now use diagnostic programs and one selected game to drive accuracy: bus wait states and sequential access, CPU pipeline/alignment corner cases, I/O masks and access widths, PPU timing, DMA priority, timer edges, BIOS behavior, and cartridge protocols. Keep serial/link and unusual peripherals explicit optional extensions if outside your selected target. “Playable” means a repeatable user workflow, not just a boot picture.',
    'var watch = System.Diagnostics.Stopwatch.StartNew();\n// Measure a repeatable workload after correctness is established.',
    'Stopwatch measures host performance; it must not become the guest clock. Compare the same fixture and inputs before/after an optimization. Use structured fixture results so a failure retains its diagnostic name, input, expected result, and actual result.',
    ['Choose one diagnostic failure or visible game defect, capture its earliest divergence, and fix that behavior only. Add a regression case.', 'Repeat until a defined section of one selected game has working graphics, input, audio, and persistence.', 'Exercise normal open/pause/reset/switch/save/state/close workflows, then profile any measured bottleneck. Record actual unsupported behavior instead of claiming universal compatibility.'],
    ['A versioned diagnostic set produces repeatable recorded results, including remaining failures.', 'Play the chosen section through the normal Open ROM path with responsive controls, graphics, and audio.', 'Save in-game, close completely, reopen, and Continue with the same progress.', 'Save-state replay remains deterministic after accuracy fixes.', 'A measured optimization changes performance without changing fixture outputs.', 'Remaining instruction/device/timing gaps are named with a next reproducible case.'],
    'You do not need to read every reference before fixing the next defect. Use the same loop: learn the one relevant hardware rule, learn any missing syntax, implement it, check the case.', 'docs/16-testing/README.md')

def finish():
    # Early diagnostic restrictions must not block the later hardware expansion.
    # Keep all positive behavior checks; retire only the explicitly temporary bans.
    lessons[2]['retireChecks'] = [dict(fromLesson=23, name='Course03Tests.Unsupported_regions_are_reported')]
    lessons[7]['retireChecks'] = [dict(fromLesson=15, name='Course08Tests.Unsupported_opcode_is_reported')]
    for index, item in enumerate(lessons):
        path = ROOT / item['folder'] / 'README.md'
        if item['id'] == '02':
            text = path.read_text(encoding='utf-8')
            text = text.replace('Cast a byte to uint before placing it in the top eight bits of a word.', 'Cast a byte to uint before placing it in the top eight bits of a word. The supplied `RamWords(Ewram ram)` is a primary constructor: it receives your existing RAM object, available as `ram` inside these methods. The `=> throw ...` syntax is an unfinished expression body; replace it with `{ ... }` when writing several statements.')
            path.write_text(text, encoding='utf-8')
        if item['id'] in ('15', '23'):
            extra = ('The runner now retires the early “unsupported opcode” rejection check so you can add those instructions. Existing positive arithmetic/condition checks still run.' if item['id']=='15' else 'The runner now retires the early “all non-EWRAM regions are unsupported” rejection check so you can map IWRAM and other devices. Existing EWRAM routing/mirroring checks still run.')
            path.write_text(path.read_text(encoding='utf-8') + '\n' + extra + '\n', encoding='utf-8')
        if item['id'] == '29':
            text = path.read_text(encoding='utf-8')
            text = text.replace('## The GBA behavior', 'Your local firmware goes in **`roms/gba_bios.bin`**. The desktop build copies it automatically, and **`BiosFile.Load()`** returns its validated bytes. This host helper is already supplied. You do not write or recreate the BIOS. It stays local rather than being included in Git.\n\n## The GBA behavior')
            path.write_text(text, encoding='utf-8')
        next_link = ('\nNext: [' + lessons[index+1]['title'] + '](../' + Path(lessons[index+1]['folder']).name + '/README.md). Press **N** in the launcher when this step is checked.\n') if index+1 < len(lessons) else '\nYou have reached the course’s integration milestone. Continue the same loop for each compatibility improvement.\n'
        path.write_text(path.read_text(encoding='utf-8') + next_link, encoding='utf-8')
    (COURSE / 'lessons.json').write_text(json.dumps(lessons, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    entries = '\n'.join(f"| {i['id']} | [{i['title']}]({Path(i['folder']).name}/README.md) | {'Supplied tests' if i['mode']=='automatic' else 'Observe the listed behavior'} |" for i in lessons)
    (COURSE / 'README.md').write_text(clean(f'''
# Your emulator course

**One lesson at a time: read → write → save → check.**

Double-click `learn.cmd` in the repository root. It remembers your current lesson. **O** opens its README. **N** moves on after checks; **P** revisits the previous lesson. You can also double-click `learn.cmd` inside a lesson folder to select it directly.

The launcher prepares missing starter files and supplied tests without overwriting your work. You write the emulator behavior. Early checks run automatically on save. Later lessons include small observable fixtures and app checks; the launcher distinguishes those self-checks from automatic test results.

The whole course uses the same page structure: the GBA rule, a short C# example, specific implementation steps, and an observable finish. Larger components are split into several lessons. Work on one numbered implementation step per sitting if needed. You can ask for an explanation, signature, fixture, test, or host/setup assistance at any point; emulator method bodies remain yours.

Start with [01: memory that remembers bytes](01-ewram/README.md). The table is navigation, not a reading assignment.

| Lesson | Component or behavior | How you check |
| --- | --- | --- |
{entries}

All {len(lessons)} lesson pages are written. Automatic checks are supplied for the lessons labeled above; the observed lessons have starter files and concrete acceptance cases, not a hidden claim of automated coverage. The course grows a supported emulator in stages. Completion of a small helper does not claim complete ARM7TDMI, GBA hardware accuracy, or universal game support.
'''), encoding='utf-8')

if __name__ == '__main__':
    finish()
    print(f'Generated {len(lessons)} lesson pages and their templates; learner source files were not modified.')
