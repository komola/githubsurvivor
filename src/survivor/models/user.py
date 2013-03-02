from mongoengine import *
from mongoengine.queryset import QuerySet

from survivor import config

class UserQuerySet(QuerySet):
    """
    Custom user queries.
    """
    def competitors(self):
        return filter(lambda u: u.leaderboard_user(), self.all())

    def developers(self):
        return self.competitors()

class User(Document):
    """
    A GitHub collaborator.
    """
    meta = {'queryset_class': UserQuerySet}

    github_id = IntField(required=True, unique=True)
    login = StringField()
    name = StringField()
    email = StringField()
    avatar_url = StringField()
    gravatar_id = StringField()

    def __init__(self, **kwargs):
        self._closed_issues = None
        Document.__init__(self, **kwargs)

    def assigned_issues(self):
        return self.issues('open')

    def closed_issues(self):
        return self.issues('closed')

    def reported_issues(self):
        from survivor.models.issue import Issue
        return Issue.objects(reporter=self)

    def issues(self, state):
        from survivor.models.issue import Issue
        return Issue.objects(assignee=self, state=state)

    def leaderboard_user(self):
        "Returns true if user should be included in leaderboards."
        whitelist = config['leaderboard_users']
        return not whitelist or self.login in whitelist

    def assigned_issues_urls(self):
        urls = (('https://github.com/%s/issues/assigned/%s' % (repo,self.login),) for repo in config['github.repos'])

        return urls

    def assigned_issues_url(self):
        urls = u'hase'

        return urls
