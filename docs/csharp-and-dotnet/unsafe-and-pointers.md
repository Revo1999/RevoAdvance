# Unsafe code and pointers

## Before the technical details

This is optional until host interop requires it. A guest address is just a number in the modeled GBA address space. A managed reference identifies a .NET object; a native pointer refers to host memory. They are not interchangeable. Begin with safe storage and only then read the pointer notation below.

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

### Keep a numeric address separate from host storage

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
uint labelNumber = 100u;
byte[] contents = { 7, 8 };
Console.WriteLine(labelNumber);
Console.WriteLine(contents[0]);
```

Expected output:

```text
100
7
```

The number 100 does not point into this array. You access array contents through the managed array reference and a valid index. No unsafe setting is needed for this program. The separate pointer fragment below is labeled because it needs an explicit compiler setting.

### Try it before implementing

Draw three boxes labeled guest address, managed reference and native pointer. For the later pointer demonstration, explain what `&number` and `*pointer` mean before attempting it in a sandbox with unsafe compilation enabled. Keep unsafe disabled in Core.

Continue with the detailed lesson below after you can explain your prediction.


This is a host-interop chapter for later. Ordinary managed C# can represent addresses as numbers and memory as arrays; guest addresses are not host pointers.

```csharp
// Language demonstration only; requires AllowUnsafeBlocks to compile.
unsafe
{
    int number = 7;
    int* pointer = &number;
    int copy = *pointer;
}
```

`unsafe` permits pointer operations; it does not disable the GC. `int*` is a pointer to an integer, `&` takes an address here, and unary `*` dereferences a pointer. Those meanings differ from bitwise AND and multiplication because of syntax context.

`fixed` pins movable managed storage for a limited scope so the GC cannot move it while a native call uses its address. A pointer must not escape that scope if the storage can later move. If an API retains the pointer, a short fixed block is insufficient: establish an explicit longer lifetime. [The fixed statement](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/fixed) explains this scope.

Neither project enables unsafe initially. Vulkan bindings may later require it because native functions receive pointers to structures and buffers. Enable it only in Desktop when you reach that milestone, after understanding [native interop](native-interop.md).


## Where this meets the GBA

- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain unsafe contexts, pointers and fixed in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Unsafe code and pointers](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code); look specifically for **Unsafe contexts, pointers and fixed**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Draw the lifetime of a managed array pinned for one native call. Explain what would go wrong if that API retained the pointer. No unsafe code is needed in your emulator yet.

## Check this lesson's exercise

This implementation task is a written explanation or diagram; no new emulator code or test file is required here. Finish the paper task and compare it with the definition of done below. To repeat the **safe console warm-up**, save its code in `.work/SyntaxLab/Program.cs` and run from the prepared repository-root terminal:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the output shown above. The advanced fragments are explanatory and may need additional setup; they are not required runnable exercises. Do not treat a successful console run as evidence for a hardware implementation.

## Definition of done

- You distinguish guest address, managed reference and native pointer.

## Common mistakes

- Casting a GBA address to a host pointer.
- Assuming fixed makes a buffer live forever.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code) — Unsafe contexts, pointers and fixed. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
