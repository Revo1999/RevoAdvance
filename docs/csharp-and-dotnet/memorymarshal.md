# MemoryMarshal: optional advanced views

## Before the technical details

This is an optional advanced topic. Numeric conversion changes representation to preserve or deliberately narrow a number; reinterpretation views existing storage through another type. You should already understand arrays, spans and byte order. Start with a named endian read so you have a clear baseline before comparing native-layout views.

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

### Make the byte interpretation visible first

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
using System.Buffers.Binary;

byte[] raw = { 0x10, 0x20 };
ushort value = BinaryPrimitives.ReadUInt16LittleEndian(raw);
Console.WriteLine(value.ToString("X4"));
Console.WriteLine(raw.Length);
```

Expected output:

```text
2010
2
```

This reads a value with an explicit byte-order contract. It does not turn the array into a ushort array and does not mutate its bytes. MemoryMarshal.Cast below instead creates a shared view governed by native representation assumptions.

### Try it before implementing

Explain whether changing `raw[0]` after this read changes the already stored `value`. Contrast that with reading again through a shared view. Keep explicit endian reads as your starting tool until reinterpretation solves a measured, understood problem.

Continue with the detailed lesson below after you can explain your prediction.


MemoryMarshal exposes low-level operations on managed memory views. It can reinterpret bytes as another value type without per-element conversion. That power removes assumptions you would otherwise state explicitly.

```csharp
byte[] raw = new byte[4];
Span<ushort> words = System.Runtime.InteropServices.MemoryMarshal.Cast<byte, ushort>(raw.AsSpan());
```

This produces a view over the same storage. It does not decode little endian independently of the host, validate a GBA region, or implement hardware access widths. Length, alignment/platform assumptions and types containing managed references matter. For guest integers, begin with explicit endian operations from [arrays and spans](arrays-and-spans.md).


## Where this meets the GBA

- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)
- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain casts, layout and reference restrictions in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: MemoryMarshal: optional advanced views](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.memorymarshal); look specifically for **Casts, layout and reference restrictions**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Describe when reinterpretation and numeric conversion give different answers. Keep MemoryMarshal out of the first memory implementation.

## Check this lesson's exercise

This implementation task is a written explanation or diagram; no new emulator code or test file is required here. Finish the paper task and compare it with the definition of done below. To repeat the **safe console warm-up**, save its code in `.work/SyntaxLab/Program.cs` and run from the prepared repository-root terminal:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the output shown above. The advanced fragments are explanatory and may need additional setup; they are not required runnable exercises. Do not treat a successful console run as evidence for a hardware implementation.

## Definition of done

- You can state byte-order and lifetime assumptions for a reinterpretation.

## Common mistakes

- Treating a cast view as endian conversion.
- Using raw struct layout as a durable save-state format.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.memorymarshal) — Casts, layout and reference restrictions. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
