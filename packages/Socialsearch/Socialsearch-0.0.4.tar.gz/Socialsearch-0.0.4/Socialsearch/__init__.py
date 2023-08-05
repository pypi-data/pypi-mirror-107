def Google_Search(Search):
    link = 'https://www.google.com/search?q={}'.format(Search)
    return link
def Facebook_Search(Search):
    link = 'https://www.facebook.com/search/top?q={}'.format(Search)
    return link
def YouTube_Search(Search):
    link = 'https://www.youtube.com/results?search_query={}'.format(Search)
    return link
def Github_search():
    def SearchUser(name):
        def SearchRepo(reposiory):
            link = "https://github.com/{}/{}".format(name,reposiory)
            def GetIssuesLink():
                return link + "/issues"
            def GetPullsLink():
                return link+"/pulls"
            def GetActionsLink():
                return link+"/actions"
            def GetProjectsLink():
                return link+"/projects"
            def GetWikiLink():
                return link+"/wiki"
            def GetSecurityLink():
                return link+"/security"
            def GetPulseLink():
                return link+"/pulse"
            def GetLink():
                return link