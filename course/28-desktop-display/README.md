# 28. Showing your framebuffer in a window

**Read this page → edit `src/Gba.Desktop/Window/EmulatorWindow.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

The GBA produces a 240×160 image; your desktop host presents those pixels. Vulkan and GLFW belong to the host, not to emulated memory or CPU behavior. Start by showing a synthetic image using the planned Silk.NET/Vulkan/GLFW backend, then connect the PPU buffer. Window creation, package versions, device setup, swapchain plumbing, and synchronization are support work you may ask me to implement; your learning task is the framebuffer handoff and visible result.

## C# you need now

```csharp
using var resource = CreateResource();
// A resource implementing IDisposable is released when this scope ends.
```

This syntax fragment explains lifetime. Managed arrays are collected automatically; GPU/window resources need explicit disposal in the right order. A ReadOnlySpan<uint> describes a temporary view of pixels; it must not be stored for later use after its owner changes/disappears. For asynchronous upload, copy or hand off an owned buffer.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Define the host handoff: 240×160 pixels, known channel format, and who owns the buffer during presentation.
2. Connect a synthetic asymmetric frame to the host backend. Have setup/plumbing supplied if needed; do not put Vulkan types into Core.
3. Connect completed PPU frames, preserving aspect ratio and nearest/integer scaling. Handle resize and orderly shutdown.

## Check it

The launcher checks compilation and earlier automatic checks. The behavior below needs **your observation**; a successful build does not verify it. Exercise one case at a time through your existing tests or app. Press **N** only after observing every case; the launcher records this as self-checked, not automatically tested.

- Four distinct corners appear in the correct positions and channels.
- Resize preserves aspect ratio and introduces borders where necessary.
- Repeated open/resize/close does not leak resources or report validation errors.
- The displayed frame is complete, not half from one guest frame and half from another.

<details>
<summary>A hint if you get stuck</summary>

The existing host is a placeholder, so the first build does not create a window. This is an observed integration lesson, not an automatic GPU test. Treat backend setup as assistance work, not a new prerequisite course.

</details>

Optional detail: [the existing hardware reference](../../docs/15-vulkan-output/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Loading a program and choosing a boot state](../29-boot/README.md). Press **N** in the launcher when this step is checked.
