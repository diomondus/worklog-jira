import calendar
import datetime
import sys
from datetime import date

from jira import JIRA

import credentials
import exclude
from extentions import worklogs_since_timestamp


def print_work(detailed):
    current_day = date.today()
    current_year = current_day.year
    current_month = current_day.month
    month_calendar = calendar.monthcalendar(current_year, current_month)

    days = get_workdays_in_month(current_day, current_month, current_year, month_calendar)

    jira = JIRA(options={'server': credentials.server}, basic_auth=(credentials.email, credentials.api_token))
    seconds = 0
    start_date = current_day.replace(current_year, current_month, days[0])
    timestamp = int(datetime.datetime.strptime(str(start_date), "%Y-%m-%d").timestamp()) * 1000
    start = str(start_date).replace("-", "/")
    end = str(current_day).replace("-", "/")
    query = f'project=TNG4 AND worklogAuthor=currentUser() AND (worklogDate >= "{start}" OR worklogDate <= "{end}")'
    issues_in_proj = jira.search_issues(query, maxResults=0)
    for issue in issues_in_proj:
        seconds_for_issue = 0
        worklogs = worklogs_since_timestamp(jira, issue.key, str(timestamp))
        for worklog in worklogs:
            if worklog.author.displayName == credentials.name \
                    and datetime.datetime.strptime(worklog.started[0:10], '%Y-%m-%d').date() >= start_date:
                seconds_for_issue += worklog.timeSpentSeconds
        if seconds_for_issue != 0:
            seconds += seconds_for_issue
            if detailed:
                print(f'{issue.key}: {str(datetime.timedelta(seconds=seconds_for_issue))} {issue.fields.summary}')

    hours = seconds / 3600.0
    work_days = len(days) - exclude.days
    # print(days)
    # print(f'{len(issues_in_proj)} tasks')
    print(
        f'{current_day.strftime("%B")}: {hours}h, {work_days} work days, {str(hours / work_days)}h avg, {str(hours - 8 * work_days)}h diff'
    )


def get_workdays_in_month(current_day, current_month, current_year, month_calendar):
    days = []
    for week in month_calendar:
        for day in week:
            if day != 0 and 0 <= calendar.weekday(current_year, current_month, day) <= 4:
                if day > current_day.day:
                    raise Exception('relax')
                days.append(day)
                if day == current_day.day:
                    return days
    raise Exception('impossible, the universe might be broken')


if __name__ == '__main__':
    print_work(len(sys.argv) > 1 and sys.argv[1] == '-d')
