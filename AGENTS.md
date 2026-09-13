# This is a learner-owned emulator

The user wants to learn GBA behavior and the required C# syntax, then write the emulator themselves.

- The active course is `course/lessons.json` and each lesson's short README. Keep the read → write → save → check workflow consistent across the whole course.
- Do not fill in emulator method bodies, including temporarily for validation, unless the user explicitly asks for a solution. Existing learner source must be preserved.
- You may supply starter declarations, signatures, explanatory comments, fixtures, tests, hints, build scripts, package configuration, and host/backend plumbing. Explain only what the current task needs.
- Prefer one small next behavior over a broad architecture assignment. Keep old detailed docs as optional reference, not prerequisites.
- Automatic checks must report real executed results; observed hardware/app checks remain explicitly self-checked. Never mark a lesson complete because it merely builds.
- `tools/build_course.py` regenerates the course pages/templates and manifest; it must not modify learner source. Keep edits to generated lessons in that authoring file as well.
- The launcher copies missing starter files only. Never overwrite a learner's existing implementation to match a template.
