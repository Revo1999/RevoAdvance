# 04. Keeping cartridge program bytes

**Read this page → edit `src/Gba.Core/Cartridge/RomImage.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

A .gba file contains cartridge ROM bytes. Reading those bytes is different from executing them. Start with a RomImage object that owns a copy of supplied bytes and exposes their length and byte reads. It has no write operation. This first helper uses file offsets, not guest addresses. For now an out-of-file read throws ArgumentOutOfRangeException; cartridge bus behavior is a later integration concern.

## C# you need now

```csharp
byte[] original = { 10, 20, 30 };
byte[] copy = (byte[])original.Clone();
int size = copy.Length;
```

Arrays are reference types: assigning `copy = original` would share one array. Clone creates separate storage; the cast tells C# it is a byte array. A constructor has the class name and no return type. A read-only property can be written `public int Length => expression;`. Later the desktop can supply bytes with File.ReadAllBytes(path); the memory object itself does not need file dialogs.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. In the constructor, retain an independent copy of the supplied bytes.
2. Implement Length and Read8; check the offset against the actual length.
3. Keep the original input independent and expose no ROM write method.

## Check it

The launcher runs **3 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- The length matches the supplied image.
- The first and final bytes can be read.
- Changing the input array after construction does not change ROM data.
- Negative and past-the-end offsets throw ArgumentOutOfRangeException.

<details>
<summary>A hint if you get stuck</summary>

This is an immutable input snapshot, not RAM. A path, an array, and a guest address are three different things.

</details>

Optional detail: [the existing hardware reference](../../docs/12-cartridges-and-roms/loading-and-playing.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [The CPU working registers](../05-registers/README.md). Press **N** in the launcher when this step is checked.
