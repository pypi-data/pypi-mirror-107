class Github:
    def getSearchRepoLink(repo, Searchtype):
        if Searchtype=="all":
            link = "https://github.com/search?q={}".format(repo.repository_name)
        elif Searchtype=="user":
            link = "https://github.com/{}?tab=repositories&q={}&type=&language=&sort=".format(repo.user, repo.repository_name)
        return link
    def getRepoLink(self, repo):
        link="https://github.com/{}/{}".format(repo.user, repo.repository_name)
        return link
    class SearchType:
        def allgithub(self):
            return "all"
        def user(self):
            return "user"
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
class Youtube:
    def search(phase):
        link = "https://www.youtube.com/results?search_query={}".format(phase)
        return link
class Google:
    def search(phase):
        link="https://www.google.com/search?q={}".format(phase)
class Facebook:
    def Search(self, query):
        link = "https://www.facebook.com/search/top/?q={}".format(query)