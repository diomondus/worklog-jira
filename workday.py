import datetime
import sys
from typing import Union, List

from jira import JIRA, Worklog

import credentials
from extentions import worklogs_since_timestamp


def print_work(current_date, detailed):
    if detailed:
        print(current_date)
    jira = JIRA(options={'server': credentials.server}, basic_auth=(credentials.email, credentials.api_token))

    seconds = 0
    query = f'project=TNG4 AND worklogAuthor=currentUser() AND worklogDate = "{current_date.replace("-", "/")}"'
    issues_in_proj = jira.search_issues(query, maxResults=0)
    timestamp = int(datetime.datetime.strptime(current_date, "%Y-%m-%d").timestamp()) * 1000
    for issue in issues_in_proj:
        seconds_for_issue = 0
        worklogs = worklogs_since_timestamp(jira, issue.key, str(timestamp))
        for worklog in worklogs:
            if worklog.author.displayName == credentials.name and worklog.started.startswith(current_date):
                seconds_for_issue += worklog.timeSpentSeconds
        if seconds_for_issue != 0:
            seconds += seconds_for_issue
            if detailed:
                print(f'{issue.key}: {str(datetime.timedelta(seconds=seconds_for_issue))} {issue.fields.summary}')
    print(f'{current_date} total:     {str(datetime.timedelta(seconds=seconds))}')


if __name__ == '__main__':
    print_work(sys.argv[1], len(sys.argv) > 2 and sys.argv[2] == '-d')
