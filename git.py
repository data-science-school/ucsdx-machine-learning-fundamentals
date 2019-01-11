# -*- coding: utf-8 -*-
"""Clone and Push GitHub Repository.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kfBBrErPGcXm49MfLWwBSmjpumU1lyto

# Clone GitHub remote repository to Google Colaboratory (run the following code cell one time only)
"""

import os

def clone(url, dpath=".", branch="master"):
  """
  Clone remote branch(es) from url into dpath
  branch: name of branch to clone ('None' will clone all branches)
  """
  
  url = url.strip("/")
  repo_name = os.path.basename(url)
  os.chdir(dpath)
  
  # Clone specific branch
  if branch:
    !git clone --single-branch --branch "$branch" "$url"
  # Clone all branches
  else:
    !git clone "$url"
    !git branch
    print("Use !git checkout <branchname> to switch to desired branch")
  os.chdir(repo_name)

  print("Current directory: {}". format(os.getcwd()))

"""# Push local repository (in Google Colaboratory) to GitHub remote repository"""

from google.colab import files
import json
from urllib.parse import urlsplit

def push(url, branch="master"):
  """
  Push local branch(es) to repository url
  User provides .json file containing account information
  Text in .json file: {"username": <username>, "email": <email>, "password": <password>, "name": <display name>}
  If name not provided, defaults to username
  branch: name of branch to push ('None' will push all branches)
  """
  
  # Obtain account information
  uploaded = files.upload() # upload .json file
  [fpath] = [*uploaded] # key of dict uploaded is filepath
  with open(fpath) as f:
    account = json.load(f)
  !rm "$fpath" # remove .json file
  account.setdefault("name", account["username"]) # name defaults to username if not provided
  
  # Construct push-authorized url by adding username and password to repository url
  r = urlsplit(url)
  r_auth = r._replace(netloc="{username}:{password}@{hostname}".format(username=account["username"], password=account["password"], hostname=r.hostname))
  url_auth = r_auth.geturl()

  # Set up git
  name, email = account["name"], account["email"]
  !git config --global user.name "$name"
  !git config --global user.email "$email"
  !git remote add origin_auth "$url_auth"
  
  # Push
  if branch:
    input("Press Enter to push {}...".format(branch))
    !git push origin_auth "$branch"
  else:
    input("Press Enter to push all branches...")
    !git push --all origin_auth