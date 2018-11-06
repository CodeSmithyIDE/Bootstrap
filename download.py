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
        if subdir == "":
            self.downloadPath = "Downloads/" + self.name + "-master.zip"
            self.extractPathPrefix = "Build"
        else:
            self.downloadPath = "Downloads/" + subdir + "/" + \
                                self.name + "-master.zip"
            self.extractPathPrefix = "Build/" + subdir

    def download(self, substep):
        print("    Step 1" + substep + ": Fetching " + self.name +
              " code from " + self.url,
              flush=True)
        Path(self.downloadPath).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(self.url, self.downloadPath)

    def unzip(self, substep):
        print("    Step 2" + substep + ": Unzipping " + self.downloadPath,
              flush=True)
        zip_ref = zipfile.ZipFile(self.downloadPath, "r")
        zip_ref.extractall(self.extractPathPrefix)
        zip_ref.close()
        shutil.rmtree(self.extractPathPrefix + "/" + self.name,
                      ignore_errors=True)
        os.rename(self.extractPathPrefix + "/" + self.name + "-master",
                  self.extractPathPrefix + "/" + self.name)


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
            download.unzip(chr(i))
