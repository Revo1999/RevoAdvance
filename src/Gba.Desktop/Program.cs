// See https://aka.ms/new-console-template for more information
using Gba.Desktop;

// Host setup only. The CPU/bus implementation remains the learner's work.
try
{
    if (BiosFile.IsAvailable)
        Console.WriteLine($"BIOS ready: {BiosFile.Load().Length:N0} bytes. Firmware execution comes in the boot lesson.");
    else
        Console.WriteLine("No local BIOS yet. Early course lessons do not need it.");
}
catch (IOException error)
{
    Console.Error.WriteLine(error.Message);
    Environment.ExitCode = 1;
    return;
}

Console.WriteLine("Start with learn.cmd. The emulator is not implemented yet.");
