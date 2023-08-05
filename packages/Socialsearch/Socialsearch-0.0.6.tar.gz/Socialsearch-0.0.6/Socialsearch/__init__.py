



class Github:
    def __init__(self):
        class Repository:
            def __init__(self, username, repository_name):
                self.username = username
                self.repository_name = repository_name
            def __str__(self):
                return self.repository_name
            def __repr__(self):
                return f"Repository(username='{self.username}', repository_name='{self.repository_name}')"
        class User:
            def __init__(self,username):
                self.username = username
            def __str__(self):
                return self.username
            def __repr__(self):
                return f"User(username='{self.username}')"
        def GetRepoLink(repo):
            link = "https://github.com/{}/{}".format(repo.username, repo.repository_name)
            return link
class Youtube:
    def __init__(self):
        def Search(Search):
            link = 'https://www.youtube.com/results?search_query={}'.format(Search)
            return link
class Facebook:
    def __init__(self):
        def Search(Search):
            link = 'https://www.facebook.com/search/top?q={}'.format(Search)
            return link
class Google:
    def __init__(self):
        def Search(Search):
            link = 'https://www.google.com/search?q={}'.format(Search)
            return link
