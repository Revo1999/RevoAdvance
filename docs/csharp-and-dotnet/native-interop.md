# Native interop and resource lifetime

## Before the technical details

Interop is communication between managed C# and native APIs. A handle identifies a native resource; copying its number does not duplicate or own the resource. Disposal releases resources according to a contract. Learn scope-based cleanup with an ordinary managed example before tackling GPU synchronization or binding signatures.

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

### See when Dispose is called

**Run this example:** open `.work/SyntaxLab/Program.cs` in your editor, replace its entire contents with the C# block below, and save. Then run this in the PowerShell terminal prepared above:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Compare the program output with “Expected output” below. After changing an example, save and run the same command again. Do not paste the command into the C# file. This command compiles your saved changes automatically.

```csharp
using (PracticeResource resource = new PracticeResource())
{
    Console.WriteLine("inside scope");
}
Console.WriteLine("after scope");

class PracticeResource : IDisposable
{
    public void Dispose()
    {
        Console.WriteLine("disposed");
    }
}
```

Expected output:

```text
inside scope
disposed
after scope
```

`:` says the class implements `IDisposable`, whose contract includes `Dispose()`. The using statement arranges that call when leaving the scope. This class owns no actual native resource; Vulkan destruction must additionally respect GPU completion and ownership.

### Try it before implementing

Explain the three output lines in order. Draw a handle separately from the resource it names, with one explicit owner responsible for release. Consult the selected native API contract before deciding whether it copies or retains a pointer.

Continue with the detailed lesson below after you can explain your prediction.


Interop crosses from managed .NET into native libraries. An ABI is the agreement about calling conventions, field layout and parameter representation. Bindings such as Silk.NET describe that agreement in C#; they do not remove Vulkan's synchronization and lifetime requirements.

| Native idea | Binding representation | C# knowledge |
| --- | --- | --- |
| Vulkan handle | typed handle value | structs; not automatically an owning object |
| pointer to create-info | pointer/ref overload depending on binding | unsafe, ref, lifetime |
| pointer plus element count | pointer plus numeric count | arrays, pinning, bounds |
| flags | enum bit set | enums and bitwise OR |
| function result | result enum | explicit error checking |

`nint` and `nuint` are native-sized integers (host pointer width), not fixed 32-bit guest addresses. `using` at the top of a file imports a namespace; a `using` statement/declaration for a resource arranges `Dispose` when its scope ends. `IDisposable` is the standard cleanup contract, not a promise that the GC knows Vulkan ownership.

```csharp
using System.IO;
using (MemoryStream stream = new MemoryStream())
{
    stream.WriteByte(42);
} // Dispose runs even if control leaves through an exception.
```

For GPU resources, finish pending use before destroying dependent objects. A disposable wrapper can centralize that policy later, without adding an interface for every hardware component. Read [Dispose](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose) for deterministic cleanup and [unsafe](unsafe-and-pointers.md) before pointers.


## Where this meets the GBA

- [Vulkan output](../15-vulkan-output/README.md)

## What you should understand now

- [ ] I can explain marshalling, abi and native ownership in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Native interop and resource lifetime](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/); look specifically for **Marshalling, ABI and native ownership**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Draw who creates, uses and releases one host image and its memory. Include the point at which queued GPU work finishes.

## Check this lesson's exercise

This implementation task is a written explanation or diagram; no new emulator code or test file is required here. Finish the paper task and compare it with the definition of done below. To repeat the **safe console warm-up**, save its code in `.work/SyntaxLab/Program.cs` and run from the prepared repository-root terminal:

```powershell
dotnet run --project .work/SyntaxLab/SyntaxLab.csproj
```

Expect the output shown above. The advanced fragments are explanatory and may need additional setup; they are not required runnable exercises. Do not treat a successful console run as evidence for a hardware implementation.

## Definition of done

- Every native resource has an owner and a valid destruction order.

## Common mistakes

- Treating copying a handle as transferring ownership.
- Destroying a texture while GPU work still references it.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/) — Marshalling, ABI and native ownership. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
