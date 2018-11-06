from pathlib import Path
import shutil
import urllib.request
import os
import zipfile


class Download:
    def __init__(self, name, subdir=""):
        self.name = name
        self.url = "https://github.com/CodeSmithyIDE/" + \
                   name + "/archive/master.zip"
        self.subdir = subdir

    def download(self, substep):
        print("Step 1" + substep + ": Fetching " + self.name + " code from " + self.url,
              flush=True)
        downloadPath = "Downloads/" + self.name + "-master.zip"
        extractPathPrefix = "Build"
        if len(self.subdir) > 0:
            Path("Downloads/" + self.subdir).mkdir(exist_ok=True)
            Path("Build/" + self.subdir).mkdir(exist_ok=True)
            downloadPath = "Downloads/" + self.subdir + "/" + self.name + "-master.zip"
            extractPathPrefix = "Build/" + self.subdir
        urllib.request.urlretrieve(self.url, downloadPath)
        print("Step 1" + substep + ": Unzipping " + downloadPath + "\n",
              flush=True)
        zip_ref = zipfile.ZipFile(downloadPath, "r")
        zip_ref.extractall(extractPathPrefix)
        zip_ref.close()
        shutil.rmtree(extractPathPrefix + "/" + self.name, ignore_errors=True)
        os.rename(extractPathPrefix + "/" + self.name + "-master",
                  extractPathPrefix + "/" + self.name)

    def unzip(self, substep):
        pass


class Downloader:
    def __init__(self):
        self.downloads = []
        self.downloads.append(Download("Errors", "Ishiko"))
        self.downloads.append(Download("Process", "Ishiko"))
        self.downloads.append(Download("WindowsRegistry", "Ishiko"))
        self.downloads.append(Download("FileTypes", "Ishiko"))
        self.downloads.append(Download("TestFramework", "Ishiko"))
        self.downloads.append(Download("libgit2"))
        self.downloads.append(Download("wxWidgets"))
        self.downloads.append(Download("CodeSmithy", "CodeSmithyIDE"))
        
    def download(self):
        for download, i in zip(self.downloads, range(ord("a"), ord("z"))):
            download.download(chr(i))

    def unzip(self):
        for download, i in zip(self.downloads, range(ord("a"), ord("z"))):
            download.unzip(i)        
