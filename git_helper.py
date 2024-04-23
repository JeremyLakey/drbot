from git import Repo
import os

GIT_PATH = os.getcwd() + "/recipes"
repo = Repo(GIT_PATH)
index = repo.index


def commit_file(f):
    index.add(f)
    index.commit("Adding recipe " + f)
    repo.remotes.origin.push()
