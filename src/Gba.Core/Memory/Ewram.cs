namespace Gba.Core.Memory;

public class Ewram
{
    // TODO 1: EWRAM holds 262,144 bytes. Give this array that capacity.
    private byte[] bytes = new byte[0];

    public byte Read8(int offset)
    {
        // TODO 2: Return the byte stored at this offset.
        throw new NotImplementedException("Implement Read8: retrieve a stored byte.");
    }

    public void Write8(int offset, byte value)
    {
        // TODO 3: Store value at this offset in the same array.
        throw new NotImplementedException("Implement Write8: store a byte.");
    }
}
