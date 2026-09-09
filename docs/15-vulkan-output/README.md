# Vulkan: presenting the finished framebuffer


## The boundary

Vulkan is a host API, not GBA hardware. The PPU has already decided the pixel colours. Desktop uploads that result and presents it. Core remains testable with no window, driver or GPU. A 240 × 160 image contains only 38,400 pixels; even RGBA8 is 153,600 bytes per frame, so this is a very small GPU workload. API correctness and ownership matter more than elaborate rendering techniques.

![Framebuffer to monitor](../assets/vulkan-flow.svg)

## First presentation experiment

Start with a synthetic colour grid in Desktop, independent of the PPU. Learn window/surface creation, device/queues, swapchain, image upload, sampling and presentation in that order. A fullscreen triangle or quad samples the uploaded image. Use a nearest-neighbour sampler so adjacent texels are not blended. Integer scale factors (2×, 3×, etc.) give uniform pixel sizes; letterbox to preserve the 3:2 aspect ratio. When the window is too small, choose an explicit downscale policy.

Then connect Core's framebuffer with a documented pixel format, row stride, ownership and completion boundary. Staging buffers and GPU images have different memory requirements. Image layout transitions, command submission and synchronization are required even for this small texture. Keep CPU/GPU writes from racing; wait for in-flight use before recycling or destroying resources. Handle resize, minimized windows and swapchain recreation.

## Silk.NET and no SDL

The intended path is Silk.NET Vulkan bindings with a GLFW window/input backend. Packages are deliberately deferred. At that milestone inspect the current stable packages `Silk.NET.Vulkan`, `Silk.NET.Windowing.Glfw` and `Silk.NET.Input.Glfw`, plus required abstractions, rather than accepting a backend-agnostic bundle blindly. Verify the dependency graph and shipped native assets contain no SDL. GLFW is a native library accessed from C#; you do not write C++.

```text
Native VkImage handle → Silk.NET typed handle struct → value, not ownership
Native create-info*  → pointer/ref binding parameter → unsafe / ref / lifetime
Native flags        → binding enum                  → bitwise combinations
Native destroy call → explicit binding call         → deterministic cleanup
```

Bindings translate native declarations into C# signatures. They do not turn Vulkan into a managed scene graph or automatically manage GPU synchronization. Exact overloads vary with package version: read the selected binding signature. Only enable AllowUnsafeBlocks in Desktop once required and after the pointer refresher.

Optional later shaders may emulate original GBA LCD, GBA SP display characteristics, colour correction or ghosting. Keep them after faithful framebuffer output and playable-game milestones. Host audio uses a separate non-SDL backend; Vulkan does not output sound.


## C#/.NET concepts used here

- [Unsafe code and pointers](../csharp-and-dotnet/unsafe-and-pointers.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code): Unsafe contexts, pointers and fixed.
- [Native interop and resource lifetime](../csharp-and-dotnet/native-interop.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/): Marshalling, ABI and native ownership.
- [Structs versus classes](../csharp-and-dotnet/structs-vs-classes.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/struct): Value copying versus shared identity.
- [Arrays, spans and byte order](../csharp-and-dotnet/arrays-and-spans.md) — [Microsoft](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/arrays): Zero-based indexing and array reference semantics.

## What you should understand now

- [ ] The framebuffer is a contract between Core and Desktop.
- [ ] Native handles need lifetime and synchronization policies.

## C#/.NET refresher

Work through the local explanations linked above, then use their paired official references for the named details. Prefer ordinary managed code; optional optimization pages are explicitly marked.

## Your implementation task

Build the synthetic host presentation yourself, then connect the PPU buffer. No Vulkan implementation is supplied here.

## Definition of done

- A colour grid appears with correct channels, orientation and nearest sampling.
- Integer scaling preserves aspect ratio.
- Resize/close succeeds with Vulkan validation enabled and no resource-lifetime errors.
- Core still builds without any Silk.NET package.

## Common mistakes

- Making the PPU create Vulkan textures.
- Assuming a fixed pointer remains valid after its scope.
- Destroying in-flight GPU resources or accidentally pulling in SDL packages.

## Further reading

- [Khronos tutorial](https://docs.vulkan.org/tutorial/latest/00_Introduction.html) — concepts and lifecycle; translate concepts rather than copy its C++.
- [Silk.NET documentation](https://dotnet.github.io/Silk.NET/docs/) — binding model and package guidance.
- [Silk.NET backends](https://dotnet.github.io/Silk.NET/docs/hlu/troubleshooting/) — GLFW backend/platform support.

## Next chapter

[Evidence before game compatibility](../16-testing/README.md)
