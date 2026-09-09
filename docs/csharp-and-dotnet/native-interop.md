# Native interop and resource lifetime


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

## Definition of done

- Every native resource has an owner and a valid destruction order.

## Common mistakes

- Treating copying a handle as transferring ownership.
- Destroying a texture while GPU work still references it.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/) — Marshalling, ABI and native ownership. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
