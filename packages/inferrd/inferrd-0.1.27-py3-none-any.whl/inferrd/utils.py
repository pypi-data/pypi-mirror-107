import zipfile
import os
from easysettings import EasySettings
from pathlib import Path
from importlib import metadata
import requests

api_host = 'https://api.inferrd.com'

settings = EasySettings(str(Path.home()) + "/.inferrd.conf")

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            filePath = os.path.join(root, file)
            inZipPath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            # remove base folder
            ziph.write(filePath, inZipPath.replace(path.split('/')[-1] + '/', ''))


def auth(key):
  settings.set('api_key', key)
  settings.save()

def get_model(name):
  api_key = settings.get('api_key')

  r = requests.get(api_host + '/service/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def new_version(modelId):
  api_key = settings.get('api_key')

  r = requests.post(api_host + '/service/' + modelId + '/versions', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def deploy_version(versionId):
  api_key = settings.get('api_key')

  r = requests.post(api_host + '/version/' + versionId + '/deploy', headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def find_version(modelId, name):
  api_key = settings.get('api_key')

  r = requests.get(api_host + '/service/' + modelId + '/versions/find/' + name, headers={'Content-Type': 'application/json', 'Authorization': 'Token ' + api_key})

  return r.json()

def generate_requirements_file():
  dists = metadata.distributions()

  with open('./reqs.txt', 'a') as requirementsFile:
    for dist in dists:
      name = dist.metadata["Name"]
      version = dist.version
      requirementsFile.write(f'{name}=={version}\n')