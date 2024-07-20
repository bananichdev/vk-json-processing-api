import git

from settings import GIT_PATH


def git_commit_and_tag(tag: str, message: str):
    repo = git.Repo(GIT_PATH)
    repo.git.add(update=True)
    repo.index.commit(message)
    repo.create_tag(tag)
    repo.git.push("master", "main")
    repo.git.push("master", tag)


git_commit_and_tag("init", "master")
