namespace Gba.Desktop;

// Host file loading only. Mapping/executing these bytes belongs to your emulator.
public static class BiosFile
{
    public static string DefaultPath => Path.Combine(AppContext.BaseDirectory, "roms", "gba_bios.bin");

    public static bool IsAvailable => File.Exists(DefaultPath);

    public static byte[] Load()
    {
        if (!IsAvailable)
            throw new FileNotFoundException("Place your BIOS at roms/gba_bios.bin in the project, then rebuild.", DefaultPath);

        byte[] bytes = File.ReadAllBytes(DefaultPath);
        if (bytes.Length != 16 * 1024)
            throw new InvalidDataException("The GBA BIOS must be exactly 16,384 bytes. Check roms/gba_bios.bin.");

        return bytes;
    }
}
