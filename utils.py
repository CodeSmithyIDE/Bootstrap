import shutil

class Utils:
    def rmdir_with_retry(dir_path, input):
        while True:
            try:
                shutil.rmtree(dir_path)
                break
            except FileNotFoundError:
                break
            except BaseException as error:
                print("Error while trying to remove directory " + dir_path + ":",
                      error)
                answer = input.query("Do you want to retry?", ["y", "n"], "y")
                if answer == "n":
                    raise
