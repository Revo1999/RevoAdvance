# Scaffold validation

## Beginner lesson expansion (2026-09-12)

- Follow-up: all 46 lessons include explicit PowerShell setup, console file/run instructions, and commands or a clearly labeled paper check for their exercises. Hardware tests have suggested class names, matching filters, discovery/full-suite commands and expected outcomes. Host lessons describe manual run/ROM/save checks separately.
- Added [Exactly how to run and test](00-getting-started/running-and-testing.md), including SDK selection, working directory, saving files, command arguments, discovery failures and stale builds. Checked that all 74 previously verified example bodies remain unchanged and all local file links resolve.
- Exercised the documented terminal SDK selection and conditional SyntaxLab creation/run. xUnit discovery listed all three practice cases, the ArithmeticExamples filter ran two cases, and the full practice project ran three passing cases.

- Synchronized this checkout with `Revo1999/RevoAdvance` main at `386d0e7` (`Upgrade scaffold to .NET 10 LTS`); a subsequent fast-forward-only pull reported up to date. The previous local folder had no Git metadata and was backed up before synchronization.
- Added a beginner setup/stack guide and expanded all 18 main chapters, 9 focused subchapters and 19 C#/.NET lessons. Hardware lessons now include two complete console warm-ups each; language lessons include an additional complete warm-up. Introductions, output walkthroughs and small practice prompts precede the original technical material and implementation tasks.
- Extracted all 74 new complete console examples directly from the Markdown into separate temporary projects. Built them with .NET SDK 10.0.401 targeting `net10.0`: zero warnings/errors. All 74 executions matched the documented output.
- Copied the documented generic Fact and Theory examples into a separate temporary xUnit v2 project using the scaffold's package versions. Three cases passed. A deliberately incorrect Fact expectation produced one assertion failure; restoring it returned all three cases to passing.
- Release solution build: zero warnings/errors. Desktop run: printed the scaffold message and exited. Repository test discovery still reports no tests, as expected; it provides no emulator correctness evidence.
- Checked local Markdown file destinations and documentation whitespace, accounting for existing CRLF files. No broken local file links. Existing SVG/Mermaid diagrams were not changed or re-rendered. External links were not exhaustively revalidated in this pass.
- No tracked emulator source, test source, project settings, packages or solution files changed. Scratch examples and validation tools live under ignored `.work`; the only tracked C# file remains the Desktop placeholder. The actual emulator exercises remain unwritten.

The validation SDK is local to this checkout at `.work/dotnet10/dotnet.exe`; it was not added to the global PATH. For this checkout, prefix build/run/test commands with `& .work/dotnet10/dotnet.exe` in PowerShell to use that SDK. A fresh clone should follow the normal .NET 10 installation instructions in [Before you code](00-getting-started/before-you-code.md).

## Original scaffold checks

Checked on 2026-09-09. These checks concern the learning repository and build shell; they do not establish emulator correctness.

## Build and source boundary

- .NET SDK 8.0.420, target `net8.0` in all three projects.
- `dotnet build GbaEmulator.sln`: passed, zero warnings/errors.
- `dotnet build GbaEmulator.sln -c Release --no-restore`: passed, zero warnings/errors.
- `dotnet run --project src/Gba.Desktop --no-build`: printed the scaffold message and exited.
- `dotnet test GbaEmulator.sln --no-restore`: test assembly built and discovery ran; **no tests are present yet**. This is not a passing hardware test suite.
- The only handwritten `.cs` file is Desktop's placeholder entry statement. Core and tests contain no implementation source. Build-generated files under `obj` are tooling output.
- Core and Desktop have no NuGet package references. Tests have only Microsoft.NET.Test.Sdk, xUnit v2 and its VSTest adapter as direct dependencies. No Vulkan/SDL dependency or unsafe setting is enabled.
- Desktop → Core and Tests → Core are the only project references. No BIOS, ROM or emulator implementation is supplied.

## Learning structure and links

- 18 main numbered chapters, 9 focused CPU/PPU/game-workflow subchapters and 19 C#/.NET refresher lessons, with navigation indexes.
- Every roadmap phase has hardware/exercise and contextual C# links. All eight requested first-result milestones appear, including an early synthetic first pixel.
- Hardware chapters distinguish real hardware, software state and C# representation, then end with understanding checks, refresher links, your task, completion criteria, common mistakes, further reading and navigation.
- Relative Markdown destinations were checked against the filesystem. External fragment targets in GBATEK were checked against the page's actual IDs.
- All 61 distinct external document URLs returned HTTP 200 with normal certificate validation and redirects enabled. Microsoft links use official documentation; hardware/tutorial/test/host sources are labeled separately. [URL results](link-checks.json) record the final destinations. HTTP success establishes reachability, not a guarantee that an external page will never change.
- The original Arm browser landing page had a local TLS-chain issue; links instead use the verified official Arm-hosted DDI 0210C PDF. A moved Tonc sound page and stale GBATEK anchors were corrected.

## Visual verification

- All six original SVGs parse as XML and were rendered in Chrome and visually inspected for legible labels, contrast and clipping.
- All seven Mermaid diagrams were rendered with Mermaid CLI 11.17.0 and Chrome. Flow direction was adjusted for the longer device diagrams so labels remain useful at document width.
- ASCII bit fields, timing/layout diagrams and tables remain readable without a diagram plugin. SVGs have accessible titles and adjacent explanatory prose.

## Intentional limits

The follow-up loading/saving lessons explicitly cover Open ROM, game session controls, cartridge persistence across app restarts and later save-state slots. Relative links and all external reference pages were rechecked after these documentation-only additions. No source or project settings changed; the build results above remain the scaffold validation record.

At the original validation, the scaffold used the installed .NET 8 SDK. No SDK installation or renderer package selection was performed at that time. The docs distinguish initial functional/scanline timing from later accuracy work. A real-game milestone is scoped to a chosen game and its prerequisites, not complete hardware compatibility.

Start with [the first-session guide](00-getting-started/README.md). Your first low-byte exercise is intentionally unwritten.

## .NET 10 upgrade validation (2026-09-10)

- Retargeted all three projects to `net10.0` and updated setup documentation.
- Validated using .NET SDK 10.0.401 installed in the local working environment.
- Release build (including restore): passed with zero warnings/errors.
- Release test discovery completed successfully; no tests are present, so no emulator behavior was verified.
- Release desktop run printed the scaffold message and exited successfully.
- Existing test package versions restored and built without changes.
