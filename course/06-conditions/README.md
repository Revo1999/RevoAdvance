# 06. Deciding whether an ARM instruction runs

**Read this page → edit `src/Gba.Core/Cpu/Conditions.cs` → save and check.**

Double-click **learn.cmd in this folder** to select this lesson, or continue in the root launcher. It prepares missing starter/check files and shows your current file. Existing code is preserved. **O** opens this page; **N** goes to the next lesson after checking your work.

## The GBA behavior

ARM instructions normally carry a four-bit condition. Test it against CPSR flags N/Z/C/V in bits 31/30/29/28. A failed condition leaves architectural results unchanged (timing is still consumed later).

| Code | Passes when | Code | Passes when |
| --- | --- | --- | --- |
| 0 EQ | Z | 1 NE | !Z |
| 2 CS | C | 3 CC | !C |
| 4 MI | N | 5 PL | !N |
| 6 VS | V | 7 VC | !V |
| 8 HI | C && !Z | 9 LS | !C || Z |
| A GE | N == V | B LT | N != V |
| C GT | !Z && N == V | D LE | Z || N != V |
| E AL | always | F NV | never in this ARMv4T learning contract |

## C# you need now

```csharp
bool enabled = (settings & 0x10u) != 0;
bool ready = enabled && !busy;
// settings is a uint and busy is a bool supplied by your caller.
```

This is a syntax fragment, not a separate program. `!= 0` converts selected bits into a Boolean. `!`, `&&`, and `||` mean not, and, and or. A switch can choose one result for each condition code. Parentheses make grouped Boolean rules explicit. Implement a pure method: it returns a decision without changing CPSR.

## Write it

The starter supplies structure, not the emulator behavior. For later lessons you also connect the component to earlier code; those connections are named below. Work on one numbered step at a time.

1. Extract N, Z, C, and V as Booleans.
2. Translate the table into Matches(condition, cpsr).
3. Evaluate all codes 0–15; return false for F rather than importing newer ARM extensions.

## Check it

The launcher runs **3 supplied checks** for this lesson, plus earlier automatic checks. Save to rerun them. All must pass before **N** moves on.

- Every condition is checked against all sixteen flag combinations.
- AL always passes and NV never passes.
- Unrelated CPSR mode/control bits do not affect condition results.

<details>
<summary>A hint if you get stuck</summary>

Signed comparisons use N and V together. N alone does not tell you whether a signed subtraction was less than zero after overflow.

</details>

Optional detail: [the existing hardware reference](../../docs/04-arm-instruction-set/README.md). You can start with this page. The reference supplies the broader rules when you expand beyond this lesson's stated scope.

Next: [Reading fields from an ARM instruction](../07-arm-fields/README.md). Press **N** in the launcher when this step is checked.
