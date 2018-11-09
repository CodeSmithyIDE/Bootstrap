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
            self.download_path = "Downloads/" + self.name + "-master.zip"
            self.extract_path_prefix = "Build"
        else:
            self.download_path = "Downloads/" + subdir + "/" + \
                                self.name + "-master.zip"
            self.extract_path_prefix = "Build/" + subdir

    def download(self, substep):
        print("    Step 1" + substep + ": Fetching " + self.name +
              " code from " + self.url,
              flush=True)
        Path(self.download_path).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(self.url, self.download_path)

    def unzip(self, substep):
        print("    Step 2" + substep + ": Unzipping " + self.download_path,
              flush=True)
        shutil.rmtree(self.extract_path_prefix + "/" + self.name,
                      ignore_errors=True)
        shutil.rmtree(self.extract_path_prefix + "/" + self.name + "-master",
                      ignore_errors=True)
        zip_ref = zipfile.ZipFile(self.download_path, "r")
        zip_ref.extractall(self.extract_path_prefix)
        zip_ref.close()
        os.rename(self.extract_path_prefix + "/" + self.name + "-master",
                  self.extract_path_prefix + "/" + self.name)


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
