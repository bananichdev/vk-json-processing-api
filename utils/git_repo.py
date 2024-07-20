import git

from settings import GIT_PATH


def git_commit_and_tag(tag: str, message: str):
    repo = git.Repo(GIT_PATH)
    repo.git.add(update=True)
    repo.index.commit(message)
    repo.create_tag(tag)
    repo.git.push("origin", "main")
    repo.git.push("origin", tag)


git_commit_and_tag("master", "master")
