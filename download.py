from pathlib import Path
import shutil
import urllib.request
import os
import zipfile

class Downloader:
    def __init__(self):
        pass

    def downloadAndUnzip(substep, organization, name, url):
        print("Step 1" + substep + ": Fetching " + name + " code from " + url, flush=True)
        downloadPath = "Downloads/" + name + "-master.zip"
        extractPathPrefix = "Build"
        if len(organization) > 0:
            Path("Downloads/" + organization).mkdir(exist_ok=True)
            Path("Build/" + organization).mkdir(exist_ok=True)
            downloadPath = "Downloads/" + organization + "/" + name + "-master.zip"
            extractPathPrefix = "Build/" + organization 
        urllib.request.urlretrieve(url, downloadPath)
        print("Step 1" + substep + ": Unzipping " + downloadPath + "\n", flush=True)
        zip_ref = zipfile.ZipFile(downloadPath, "r")
        zip_ref.extractall(extractPathPrefix)
        zip_ref.close()
        shutil.rmtree(extractPathPrefix + "/" + name, ignore_errors=True)
        os.rename(extractPathPrefix + "/" + name + "-master", extractPathPrefix + "/" + name)
        return

    def fetchSource():
        Downloader.downloadAndUnzip("a", "Ishiko", "Errors", "https://github.com/CodeSmithyIDE/Errors/archive/master.zip")
        Downloader.downloadAndUnzip("b", "Ishiko", "Process", "https://github.com/CodeSmithyIDE/Process/archive/master.zip")
        Downloader.downloadAndUnzip("c", "Ishiko", "WindowsRegistry", "https://github.com/CodeSmithyIDE/WindowsRegistry/archive/master.zip")
        Downloader.downloadAndUnzip("d", "Ishiko", "FileTypes", "https://github.com/CodeSmithyIDE/FileTypes/archive/master.zip")
        Downloader.downloadAndUnzip("e", "Ishiko", "TestFramework", "https://github.com/CodeSmithyIDE/TestFramework/archive/master.zip")
        Downloader.downloadAndUnzip("f", "", "libgit2", "https://github.com/CodeSmithyIDE/libgit2/archive/master.zip")
        Downloader.downloadAndUnzip("g", "", "wxWidgets", "https://github.com/CodeSmithyIDE/wxWidgets/archive/master.zip")
        Downloader.downloadAndUnzip("h", "CodeSmithyIDE", "CodeSmithy", "https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip")
