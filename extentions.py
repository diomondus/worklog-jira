from typing import Union, List

from jira import Worklog


def worklogs_since_timestamp(jira, issue: Union[str, int], timestamp: str) -> List[Worklog]:
    r_json = jira._get_json("issue/" + str(issue) + "/worklog?startedAfter=" + str(timestamp))
    worklogs = [
        Worklog(jira._options, jira._session, raw_worklog_json)
        for raw_worklog_json in r_json["worklogs"]
    ]
    return worklogs
