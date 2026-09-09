# Switch statements and pattern matching


A traditional switch chooses statements to execute. A switch expression computes a value. Start with statements when decoding involves several checks and effects; use expressions for small pure mappings.

```csharp
int size = 2;
string label;
switch (size)
{
    case 1: label = "small"; break;
    default: label = "other"; break;
}
string compact = size switch
{
    1 => "small",
    _ => "other"
};
```

In the expression, `=>` separates a pattern from its resulting value; `_` matches anything left over. Arms are considered in order. Pattern matching tests a value's shape or condition; a guard such as `when size > 0` adds a Boolean condition. Do not use clever patterns to conceal an instruction's mask and match rule.

ARM families overlap in their broad bit patterns. A readable table of masks and required values, with specific families considered before general ones, is more useful than a giant unexplained switch. Illegal and unimplemented instructions need distinguishable outcomes in your development tools.


## Where this meets the GBA

- [CPU state](../03-arm7tdmi/README.md)
- [ARM decoding](../04-arm-instruction-set/README.md)

## What you should understand now

- [ ] I can explain arms, ordering and exhaustive handling in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Switch statements and pattern matching](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression); look specifically for **Arms, ordering and exhaustive handling**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Write both switch styles for a generic numeric label mapping. Decide how an unexpected input should be reported. Do not implement an opcode decoder yet.

## Definition of done

- You can translate between the two forms and explain fallback ordering.

## Common mistakes

- Treating the first broad match as sufficient for every ARM encoding.
- Confusing a switch arm arrow with an assignment.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/switch-expression) — Arms, ordering and exhaustive handling. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
