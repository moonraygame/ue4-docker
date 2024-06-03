#!/usr/bin/env python3
import os, re, sys


def readFile(filename):
    with open(filename, "rb") as f:
        return f.read().decode("utf-8")


def writeFile(filename, data):
    with open(filename, "wb") as f:
        f.write(data.encode("utf-8"))


def patchFile(filename, search, replace):
    contents = readFile(filename)
    patched = contents.replace(search, replace)
    writeFile(filename, patched)

patchFile(
    os.path.join(sys.argv[1], "Scripts", "CopyBuildToStagingDirectory.Automation.cs"),
    '''// if we aren't collecting multiple platforms, then it is expected to exist
								throw new AutomationException(ExitCode.Error_MissingExecutable, "Stage Failed. Missing receipt '{0}'. Check that this target has been built.", ReceiptFileName);''',
    """if (!FileReference.Exists(ReceiptFileName))
								{
									ReceiptFileName = TargetReceipt.GetDefaultPath(ReceiptBaseDir, Target + "-ASan", ReceiptPlatform, Config, Architecture);
								}

								if (!FileReference.Exists(ReceiptFileName))
								{
									// if we aren't collecting multiple platforms, then it is expected to exist
									throw new AutomationException(ExitCode.Error_MissingExecutable, "Stage Failed. Missing receipt '{0}'. Check that this target has been built.", ReceiptFileName);
								}""")
