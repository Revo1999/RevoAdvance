# Testing with xUnit v2


The scaffold selects xUnit v2 with the VSTest adapter and Microsoft.NET.Test.Sdk. It deliberately starts with **zero test methods**. A successful build or empty discovery result is not emulator correctness.

```csharp
using Xunit;

public class ArithmeticExamples
{
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(0, 4, 4)]
    public void AdditionHasExpectedResult(int left, int right, int expected)
    {
        // Arrange: the input values are supplied above.
        int actual = left + right; // Act
        Assert.Equal(expected, actual); // Assert
    }
}
```

Attributes in square brackets attach metadata. `[Fact]` marks one test without supplied data; `[Theory]` runs a parameterized test; `[InlineData]` supplies one case. A public class and method allow test discovery. An assertion compares actual behavior with an independently chosen expectation. This language example teaches the testing tool, not an emulator operation.

Read [xUnit v2 getting started](https://xunit.net/docs/getting-started/v2/getting-started) for this scaffold's framework version. Do not mix v3 runner configuration into this project casually. Keep tests deterministic: fixed input, reproducible initial state and no real wall-clock waits.


## Where this meets the GBA

- [Testing](../16-testing/README.md)
- [Memory map](../02-memory-map/README.md)
- [Bus and memory](../06-bus-and-memory/README.md)

## What you should understand now

- [ ] I can explain test projects, assertions and parameterized tests in my own words.
- [ ] I can predict the example before running it.

## C#/.NET refresher

Read [Microsoft: Testing with xUnit v2](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test); look specifically for **Test projects, assertions and parameterized tests**.
Use the [refresher index](README.md) to revisit prerequisites. These pages use stable features supported by this scaffold; newer examples in online documentation may require a later compiler.

## Your implementation task

Write your first test file yourself: given a uint, check the low byte as a uint. Choose 0, 0xFF, 0x100 and 0x1234ABCD; calculate expected results on paper.

## Definition of done

- dotnet test discovers your cases and they pass.
- Deliberately changing one expected value makes a test fail; undo that change afterward.

## Common mistakes

- Treating a test that never runs as a pass.
- Deriving expected values using the same expression as the implementation.

## Further reading

[Official reference](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test) — Test projects, assertions and parameterized tests. Return to one of the hardware chapters above immediately after the exercise.

## Next chapter

[Choose the next concept needed by your milestone](README.md).
