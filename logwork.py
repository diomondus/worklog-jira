import sys

from jira import JIRA

import credentials


def print_work(issue_number, time, comment):  # e.g. '2h 30m'
    jira = JIRA(options={'server': credentials.server}, basic_auth=(credentials.email, credentials.api_token))
    jira.add_worklog(issue_number, timeSpent=time, comment=comment)


if __name__ == '__main__':
    print_work(sys.argv[1], sys.argv[2], '' if len(sys.argv) == 3 else sys.argv[3])
