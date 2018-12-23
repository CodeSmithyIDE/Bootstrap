from pathlib import Path
import shutil
import urllib.request
import os
import zipfile


class Download:
    def __init__(self, name, url, subdir=None, branch="master",
                 extract_path_prefix=None):
        self.name = name
        self.url = url
        self.branch = branch

        self.download_path = "Downloads/"
        if subdir is not None:
            self.download_path += subdir + "/"
        self.download_path += self.name + "-" + self.branch + ".zip"

        if extract_path_prefix is not None:
            self.extract_path_prefix = extract_path_prefix
        else:
            self.extract_path_prefix = "Build/"
            if subdir is not None:
                self.extract_path_prefix += subdir + "/"

        self.unzipped = False

    def download(self, substep):
        print("    Step 1" + substep + ": Fetching " + self.name +
              " code from " + self.url,
              flush=True)
        Path(self.download_path).parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(self.url, self.download_path)

    def unzip(self, destination_dirs=None):
        """Creates a downloader to download the package(s) for this project.

        Parameters
        ----------
        destination_dirs
            A list of directories where the package should be unzipped.
        """

        if not self.unzipped:
            print("    Unzipping " + self.download_path, flush=True)
            if destination_dirs is None:
                destination_dirs = [self.extract_path_prefix + "/" + self.name]
            destination_dir = destination_dirs[0]
            temp_destination_dir = self.extract_path_prefix + "/" + self.name + "-" + self.branch
            shutil.rmtree(destination_dir, ignore_errors=True)
            shutil.rmtree(temp_destination_dir, ignore_errors=True)
            zip_ref = zipfile.ZipFile(self.download_path, "r")
            zip_ref.extractall(self.extract_path_prefix)
            zip_ref.close()
            os.rename(temp_destination_dir, destination_dir)
        else:
            print("    " + self.download_path + " already unzipped",
                  flush=True)
        self.unzipped = True

    def __eq__(self, other):
        if not isinstance(other, Download):
            return False
        return ((self.name == other.name) and (self.url == other.url) and
                (self.download_path == other.download_path) and
                (self.extract_path_prefix == other.extract_path_prefix) and
                (self.unzipped == other.unzipped))


class Downloader:
    def __init__(self):
        self.downloads = []

    def merge(self, other_downloader):
        for other_download in other_downloader.downloads:
            already_present = False
            for download in self.downloads:
                if download.url == other_download.url:
                    if download != other_download:
                        exception_text = "Conflicting values for " + \
                                         "download " + download.name
                        raise RuntimeError(exception_text)
                    already_present = True
                    break
            if not already_present:
                self.downloads.append(other_download)

    def download(self):
        for download, i in zip(self.downloads, range(ord("a"), ord("z"))):
            download.download(chr(i))

    def unzip(self, name):
        for download in self.downloads:
            if download.name == name:
                download.unzip()
