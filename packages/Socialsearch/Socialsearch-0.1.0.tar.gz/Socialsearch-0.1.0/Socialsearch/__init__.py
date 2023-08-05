class Github:
    def getRepoLink(repo):
        link = "https://github.com/{}/{}".format(repo.username, repo.repository_name)
        return link

    class Repository:
        def __init__(self, user, repository_name):
            self.user = user
            self.repository_name = repository_name

        def __str__(self):
            return self.repository_name

        def __repr__(self):
            return f"Repository(username='{self.user.username}', repository_name='{self.repository_name}')"

    class User:
        def __init__(self, username):
            self.username = username

        def __str__(self):
            return self.username

        def __repr__(self):
            return f"User(username='{self.username}')"



