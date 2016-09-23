#!/usr/bin/env python
import slackweb
import sys
import base64
import argparse
import os
from jira import JIRA

def notify(): 
    parser = argparse.ArgumentParser(description='JIRA list slack script')
    parser.add_argument('--jira_host_url', help='url for the jira', required=True)
    parser.add_argument('--username', help='username for the jira', required=True)
    parser.add_argument('--password', help='password for the jira', required=True)
    parser.add_argument('--webhook_url', help='URL to the webhook', required=True)
    parser.add_argument('--jira_filter_id', help='JIRA filter id', required=True)
    parser.add_argument('--slack_username', help='user name for the slack bot', required=True)

    args = parser.parse_args()

    jira_host_url = args.jira_host_url
    jira_filter_id = args.jira_filter_id
    webhook_url = args.webhook_url
    slack_username = args.slack_username
    username = args.username
    password = args.password

    options = {
        'server': jira_host_url
    }

    jira = JIRA(options, basic_auth=(username, password))

    issues = jira.search_issues('filter=' + jira_filter_id)
    slack = slackweb.Slack(url=webhook_url);

    message_body = ""

    if len(issues) == 0:
        message_body = "Hooray! No Issues to Verify Today!"
    else: 
        for issue in issues: 
            link = jira_host_url + "/browse/" + issue.key
            summary = issue.fields.summary
            key = issue.key
            assignee = issue.fields.assignee.name
            reporter = issue.fields.reporter.name
            resolution = issue.fields.resolution.name
            message_body += '<{}|{}> {}\nassignee: `{}`,  resolution: `{}`\n\n'.format(link, key, summary.encode('utf-8'), assignee, resolution, ) 

    print message_body
    slack.notify(username=slack_username, text=message_body)

if __name__ == '__main__':
    notify()