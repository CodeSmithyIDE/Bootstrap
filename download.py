from pathlib import Path
import shutil
import urllib.request
import os
import zipfile


class Download:
    def __init__(self, name, url, subdir=""):
        self.name = name
        self.url = url
        if subdir == "":
            self.download_path = "Downloads/" + self.name + "-master.zip"
            self.extract_path_prefix = "Build"
        else:
            self.download_path = "Downloads/" + subdir + "/" + \
                                self.name + "-master.zip"
            self.extract_path_prefix = "Build/" + subdir
        self.unzipped = False

    def download(self, substep):
        print("    Step 1" + substep + ": Fetching " + self.name +
              " code from " + self.url,
              flush=True)
        Path(self.download_path).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(self.url, self.download_path)

    def unzip(self):
        if not self.unzipped:
            print("    Unzipping " + self.download_path, flush=True)
            shutil.rmtree(self.extract_path_prefix + "/" + self.name,
                          ignore_errors=True)
            shutil.rmtree(self.extract_path_prefix + "/" + self.name + "-master",
                          ignore_errors=True)
            zip_ref = zipfile.ZipFile(self.download_path, "r")
            zip_ref.extractall(self.extract_path_prefix)
            zip_ref.close()
            os.rename(self.extract_path_prefix + "/" + self.name + "-master",
                      self.extract_path_prefix + "/" + self.name)
        else:
            print("    " + self.download_path + " already unzipped",
                  flush=True)
        self.unzipped = True


class Downloader:
    def __init__(self):
        self.downloads = []
      #  self.downloads.append(Download("FileTypes", "TODO", "Ishiko"))
      #  self.downloads.append(Download("wxWidgets", "TODO"))

    def download(self):
        for download, i in zip(self.downloads, range(ord("a"), ord("z"))):
            download.download(chr(i))

    def unzip(self, name):
        for download in self.downloads:
            if download.name == name:
                download.unzip()
