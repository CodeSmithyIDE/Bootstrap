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
            Downloader.downloadAndUnzip(chr(i), download.subdir, download.name, download.url)

    def downloadAndUnzip(substep, organization, name, url):
        print("Step 1" + substep + ": Fetching " + name + " code from " + url,
              flush=True)
        downloadPath = "Downloads/" + name + "-master.zip"
        extractPathPrefix = "Build"
        if len(organization) > 0:
            Path("Downloads/" + organization).mkdir(exist_ok=True)
            Path("Build/" + organization).mkdir(exist_ok=True)
            downloadPath = "Downloads/" + organization + "/" + name + "-master.zip"
            extractPathPrefix = "Build/" + organization
        urllib.request.urlretrieve(url, downloadPath)
        print("Step 1" + substep + ": Unzipping " + downloadPath + "\n",
              flush=True)
        zip_ref = zipfile.ZipFile(downloadPath, "r")
        zip_ref.extractall(extractPathPrefix)
        zip_ref.close()
        shutil.rmtree(extractPathPrefix + "/" + name, ignore_errors=True)
        os.rename(extractPathPrefix + "/" + name + "-master",
                  extractPathPrefix + "/" + name)
        return
