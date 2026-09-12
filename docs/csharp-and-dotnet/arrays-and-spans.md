# Arrays, spans and byte order

## Before the technical details

Begin with arrays; spans are a later way to look at part of an array without copying it. An index identifies an element, and a length counts elements. Byte order answers a separate question: which byte contributes the lower or higher part of a multi-byte number?

## Syntax warm-up

### Open PowerShell and prepare this lesson

Open a PowerShell terminal (an IDE terminal is fine). Run this block once in each new terminal. The path below is your current checkout; if you move the repository, change that first path. All later commands on this page run from this folder, not from the lesson folder.

```powershell
Set-Location "C:\Users\victo\Desktop\RevoAdvance"
if (Test-Path ".work/dotnet10/dotnet.exe") {
    $env:PATH = "$PWD\.work\dotnet10;$env:PATH"
}
dotnet --version
```

Expect a version beginning with `10.`. The conditional uses the local SDK when present and changes PATH only for this terminal. If the command is missing or shows `8.`, complete the [.NET 10 setup](../00-getting-started/before-you-code.md#set-up-and-know-what-success-looks-like) before continuing.

Create the console scratchpad only if it does not already exist:

```powershell
if (-not (Test-Path ".work/SyntaxLab/SyntaxLab.csproj")) {
    dotnet new console --framework net10.0 --output .work/SyntaxLab
}
```

If it already exists, no output from that block is expected. Keep using that project; do not create another project for each example. [Command troubleshooting](../00-getting-started/running-and-testing.md) explains errors and the difference between running and testing.

Each example below is a complete, independent console program. Run one at a time in [SyntaxLab](../00-getting-started/before-you-code.md#a-separate-place-to-try-the-examples). These toy examples teach C#; the emulator implementation remains your exercise.

### Read an explicit byte order

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
using System.Buffers.Binary;

byte[] bytes = { 0x21, 0x43 };
ushort little = BinaryPrimitives.ReadUInt16LittleEndian(bytes);
ushort big = BinaryPrimitives.ReadUInt16BigEndian(bytes);
Console.WriteLine(little.ToString("X4"));
Console.WriteLine(big.ToString("X4"));
```

Expected output:

```text
4321
2143
```

The same bytes have two interpretations. Little-endian places the first byte in the low part; big-endian places it in the high part. `UInt16` means unsigned 16-bit, corresponding to C# `ushort`. The `using` line imports the helper type. These explicit methods make byte order visible without pointer casts.

### Try it before implementing

Swap the two array values and predict both results. Use unequal bytes: two equal bytes would hide the difference. Then work through the span examples below and state whether each operation copies or shares storage.

Continue with the detailed lesson below after you can explain your prediction.


An array has a fixed length and numbered elements starting at zero. `new byte[1024]` creates 1,024 zero-initialized bytes; valid indexes are 0 through 1,023. Arrays are reference types even when their elements are value types.

```csharp
byte[] data = new byte[1024];
data[3] = 42;
Span<byte> window = data.AsSpan(2, 4);
window[1] = 7; // modifies data[3]; no new backing array
```

`Span<T>` is a temporary bounded view of contiguous elements of type `T`. The angle brackets supply a type argument. `ReadOnlySpan<T>` prevents writing through that view, but another owner can still change the underlying array. Neither owns the storage. A span cannot be stored as an ordinary class field or retained freely across asynchronous suspension. `Memory<T>` can be retained in such contexts; lifetime and ownership remain your responsibility.

Ranges use an exclusive end: `data[2..6]` on an **array copies** four elements into a new array; `data.AsSpan()[2..6]` slices a span without copying. Prefer explicit `AsSpan(start, length)` until this distinction is comfortable.

```text
offset       0      1
byte        0x34   0x12
little-endian 16-bit interpretation: 0x1234
```

Use explicit little-endian conversion at the guest memory boundary. [BinaryPrimitives](https://learn.microsoft.com/en-us/dotnet/api/system.buffers.binary.binaryprimitives) provides named endian operations; read the little-endian methods after understanding the two-byte example. Host-native reinterpretation is not an endian contract.

A framebuffer can be a one-dimensional array even though you reason in rows and columns. Work out row stride and the last valid position on paper. A guest address is not an array index: first resolve the region, then calculate its offset, then enforce that access's rules.

Advanced later: [Span<T>](https://learn.microsoft.com/en-us/dotnet/api/system.span-1) explains restrictions and slicing; [Memory<T>](https://learn.microsoft.com/en-us/dotnet/api/system.memory-1) explains a storable memory view. Ordinary arrays are enough for the first exercise.


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [PPU](../07-ppu/README.md)
- [Audio](../13-audio/README.md)

## What you should understand now

- [ ] I can explain zero-based indexing and array reference semantics in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Arrays, spans and byte order](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays); look specifically for **Zero-based indexing and array reference semantics**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Create a tiny generic byte array. Verify first/last indexes, aliasing through a span and a two-byte little-endian interpretation in tests. Leave GBA address routing for the memory milestone.

## Run and check your practice

Write your toy practice in `.work/SyntaxLab/Program.cs`, save, and run from the repository-root terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare your result with a prediction written before running; your own exercise values may differ from the worked example. Save and rerun this same command after each edit. This runs a console program, not xUnit.

For an exercise that asks for assertions or parameterized tests, use the [TestLab setup and complete test-file examples](../csharp-and-dotnet/testing.md#a-complete-fact-example-test-project-only). Put your own public test class in `.work/TestLab/PracticeTests.cs`; save it, then run:

```powershell
dotnet test .work/TestLab/TestLab.csproj --list-tests
dotnet test .work/TestLab/TestLab.csproj --logger "console;verbosity=normal"
```

The list must contain your methods, and the run must report actual executed cases with zero failures. If only the supplied generic Fact/Theory examples are present, expect three cases; adding your own increases that count. If no cases are discovered, check the public class/method and `[Fact]`/`[Theory]` attributes. After each edit, save and rerun the second command. For a reading-only part of the task, answer its questions on paper; no new test is needed for that part.

## Definition of done

- You distinguish copying an array slice from sharing a span.
- Byte order can be demonstrated with two unequal bytes.

## Common mistakes

- Indexing an array with 0x06000000.
- Keeping a span after its storage lifetime ends.
- Assuming every range operation is allocation-free.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays) — Zero-based indexing and array reference semantics. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
