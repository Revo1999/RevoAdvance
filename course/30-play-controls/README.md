# 30. Run, pause, reset, and buttons

**Read this page → edit `src/Gba.Desktop/Input/SessionControls.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

Your host controls a session; the guest sees logical buttons and advancing time. Pause freezes all guest state while the window still responds. Reset starts a fresh guest state for the same cartridge while preserving persistent save data. Switching ROMs creates a new guest session and loads that game’s own save. KEYINPUT is read-only guest input; KEYCNT selects optional keypad IRQ sources and OR/AND matching.

## C# you need now

```csharp
public enum SessionState { Stopped, Running, Paused }
// Named states make allowed transitions explicit.
```

Convert host key-down/key-up events into a pressed-bit mask, then pass it to Keypad. Keep input state updates and CPU execution synchronized, initially on one thread if possible. Separate Reset from clearing every file or every object indiscriminately.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Connect physical keys to the logical keypad and clear held host inputs appropriately on focus loss.
2. Add run/pause/resume/reset through one session controller.
3. Add Open ROM and game switching with visible errors; implement KEYCNT source matching and feed its guest IRQ request into the existing controller.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Press/release A changes KEYINPUT and a supported game/menu responds.
- Pause freezes the cycle count; the window can still resize and resume.
- Reset reproduces boot state but does not erase a saved game.
- Switching games does not retain the previous CPU registers or held keys.
- KEYCNT OR matches one selected pressed key; AND requires all selected keys, with empty-selection behavior tested from the hardware reference.

<details>
<summary>A hint if you get stuck</summary>

Close the old session only after the new image and save have loaded successfully. UI event handling is host plumbing; the guest input semantics are your component.

</details>

Optional detail: [the existing hardware reference](../../docs/11-input/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Keeping a game save after the app closes](../31-sram/README.md). Press **N** in the launcher when this step is checked.
