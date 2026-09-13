# 01. Memory that remembers bytes

**Read this page → edit `src/Gba.Core/Memory/Ewram.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Games keep changing data in RAM. The GBA has 262,144 bytes of external work RAM (EWRAM). Each byte holds 0–255. Today use offsets into that storage: first 0, last 262143. Write 42 at offset 7, then read 7: you should get 42. Writing 99 there replaces 42. This is physical storage only; guest addresses and timing come later. Callers supply valid offsets.

## C# you need now

```csharp
byte[] boxes = new byte[10];
boxes[3] = 42;
byte answer = boxes[3];
```

`byte[]` is similar to JavaScript Uint8Array: fixed size, one byte per element. Keep it in a field so calls use the same storage. `public byte Read8(int offset)` returns a byte using `return expression;`. `public void Write8(int offset, byte value)` changes storage and returns nothing. `private` keeps a field inside the object; `public` allows calls from other code. Leave the class/namespace structure in place.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Give the existing array 262,144 elements.
2. Replace the Read8 placeholder with a read at the given offset.
3. Replace the Write8 placeholder with a write to that same array.

## Check it

The launcher runs **6 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- A written value can be read.
- A second write replaces the first.
- Adjacent offsets stay independent.
- The first and last offsets work, including values 255 and 0.
- Two Ewram objects do not share storage.

<details>
<summary>A hint if you get stuck</summary>

Create the array once per object, not inside Read8 or Write8. The NotImplementedException lines are markers to replace.

</details>

Optional detail: [the existing hardware reference](../../docs/02-memory-map/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Reading two or four bytes together](../02-memory-widths/README.md). Press **N** in the launcher when this step is checked.
