import zipfile
import urllib.request

print("CodeSmithy bootstrap build")

print("Fetching CodeSmithy code from https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip")
urllib.request.urlretrieve('https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip', 'master.zip')

print("Unzipping master.zip")
zip_ref = zipfile.ZipFile('master.zip', 'r')
zip_ref.extractall('.')
zip_ref.close()
