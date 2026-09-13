using Gba.Core.Memory;

// Supplied lesson checks. Implement Ewram.cs; no test-tool setup is needed.
[Trait("Lesson", "01")]
public class EwramTests
{
    [Fact]
    public void Remembers_a_written_byte()
    {
        var ram = new Ewram();
        ram.Write8(7, 42);
        Assert.Equal((byte)42, ram.Read8(7));
    }

    [Fact]
    public void A_second_write_replaces_the_previous_value()
    {
        var ram = new Ewram();
        ram.Write8(7, 42);
        ram.Write8(7, 99);
        Assert.Equal((byte)99, ram.Read8(7));
    }

    [Fact]
    public void Neighboring_offsets_keep_separate_values()
    {
        var ram = new Ewram();
        ram.Write8(7, 42);
        ram.Write8(8, 99);
        Assert.Equal((byte)42, ram.Read8(7));
        Assert.Equal((byte)99, ram.Read8(8));
    }

    [Fact]
    public void The_first_byte_can_store_255()
    {
        var ram = new Ewram();
        ram.Write8(0, 255);
        Assert.Equal((byte)255, ram.Read8(0));
    }

    [Fact]
    public void The_last_byte_can_be_written_and_cleared()
    {
        var ram = new Ewram();
        ram.Write8(262143, 128);
        Assert.Equal((byte)128, ram.Read8(262143));
        ram.Write8(262143, 0);
        Assert.Equal((byte)0, ram.Read8(262143));
    }

    [Fact]
    public void Two_memory_objects_do_not_share_storage()
    {
        var first = new Ewram();
        var second = new Ewram();
        first.Write8(7, 12);
        second.Write8(7, 34);
        Assert.Equal((byte)12, first.Read8(7));
        Assert.Equal((byte)34, second.Read8(7));
    }
}
