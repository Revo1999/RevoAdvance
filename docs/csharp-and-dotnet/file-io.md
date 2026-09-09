# Files, paths and persistence

Read this when implementing [ROM loading](../12-cartridges-and-roms/loading-and-playing.md) or [game saves](../12-cartridges-and-roms/saving-and-resuming.md). File I/O belongs in Desktop; Core models the bytes and hardware behavior.

A path names a file location. Relative paths depend on the current working directory, which may differ between an IDE and a packaged app. Use `Path` operations to construct paths rather than concatenating separator characters. Constructing a path does not create a directory or establish that a file exists.

```csharp
using System.IO;

string folder = "practice";
string location = Path.Combine(folder, "sample.dat");
```

`using System.IO;` imports names. A static method such as `Path.Combine` is called on the type without constructing an instance. This generic example only builds a path; it reads or writes nothing.

ROM and save files are binary, not text. `File` offers operations that read or write whole byte arrays, while streams support incremental access. Prefer the simplest bounded operation suited to your first exercise. Inspect file size before allocating for untrusted/incorrect input, and still handle failure during the actual operation.

A stream is a resource: dispose it when finished using the lifetime rules in [native interop](native-interop.md), which also explains the resource form of `using`. Disk I/O can fail because a path is missing, permissions deny access or storage is unavailable. Catch appropriate failures at the host boundary; do not report success when data was not persisted.

For a save snapshot, decide who owns the buffer while it is being written. Assignment of `byte[]` copies a reference, not the bytes. Start with controlled synchronous I/O; introduce background operations only after learning their lifetime and synchronization requirements. Keep disk work outside the CPU's instruction loop.

## What you should understand now

- [ ] Paths, in-memory bytes and persistent files are different objects/concepts.
- [ ] Binary data should not pass through text encoding operations.
- [ ] A filesystem operation can fail even after an earlier existence check.

## C#/.NET refresher

- [Arrays and spans](arrays-and-spans.md) — byte storage and copying.
- [Exceptions](exceptions.md) — host failure handling.
- [Microsoft File](https://learn.microsoft.com/en-us/dotnet/api/system.io.file) — look for byte-array reads/writes, overwrite behavior and documented exceptions.
- [Microsoft Path](https://learn.microsoft.com/en-us/dotnet/api/system.io.path) — look for Combine and full versus relative paths.

## Your implementation task

Write a few synthetic bytes to a new file in a disposable practice directory, then read them back in a separate run and compare with expectations chosen on paper. Never use your real game saves for this exercise. Choose the methods yourself.

## Definition of done

The same bytes survive a fresh process; a path containing spaces works; a deliberately invalid destination produces a clear failure rather than a false success message.

## Common mistakes

- Assuming the working directory is always the executable directory.
- Overwriting a real save while practicing file operations.
- Assuming a reference copy freezes a save snapshot.

## Further reading

[Microsoft file and stream I/O](https://learn.microsoft.com/en-us/dotnet/standard/io/) — read the file/stream distinction and binary versus text sections; the older platform-specific sections are not needed here.

## Next chapter

[Load a .gba file](../12-cartridges-and-roms/loading-and-playing.md), then [save and resume](../12-cartridges-and-roms/saving-and-resuming.md).
