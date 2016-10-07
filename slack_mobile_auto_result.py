#!/usr/bin/env python
import slackweb
import argparse
import base64
from jira import JIRA

'''
python script to send slack notification

example of usage:
    ./slack.py \
    --platform iOS \ 
    --ts 12345678 \
    --server Staging \
    --device samsung \
    --os_version 4.4 \
    --commit_hash 123456ff \
    --test_summary "Passed: 40, Failed: 50, Skipped 1" \
    --log_link www.sohu.com --report_link www.sohu.com \
    --webhook_url https://hooks.slack.com/services/T047VPTNN/B0YNS77CM/xxxx
'''
def notify():
    parser = argparse.ArgumentParser(description='slack notification script for mobile test')
    parser.add_argument('--webhook_url', help='URL to the webhook', required=True)
    parser.add_argument('--platform', help='platform is either Android or iOS', required=True)
    parser.add_argument('--ts', help='timestamp in string', default="unknow")
    parser.add_argument('--server', help='server', default="Staging", required=True)
    parser.add_argument('--device', help='device model', required=True)
    parser.add_argument('--os_version', help='os version of device', required=True)
    parser.add_argument('--commit_hash', help='commit_hash of the build', default="N/A")
    parser.add_argument('--test_case_tags', help='cucumber tags of test cases', default="All")
    parser.add_argument('--test_summary', help='text of text summary', required=True)
    parser.add_argument('--log_link', help='hyperlink of the logs or videos', required=True)
    parser.add_argument('--report_link', help='hyperlink of the report', required=True)
    parser.add_argument('--jira_filter_id', help='jira filter id')

    args = parser.parse_args()

    # predefined ios/aos image
    aos_image = "http://www.alltechflix.com/wp-content/uploads/2015/05/android-websites.jpeg";
    ios_image = "http://www.ioscentral.com/wp-content/uploads/2014/01/Apple_Logo.jpg";

    # attachments variables
    if (args.platform == "Android"):
        thumb_url = aos_image;
        color="#36a64f" # green for aos
    else:
        thumb_url = ios_image;
        color="#a3a3c2" # light purple for ios

    jira_host_url = args.jira_host_url
    webhook_url = args.webhook_url;
    platform = args.platform;
    ts = args.ts;
    footer_text = "Triggered at: " + ts;
    footer_icon = "http://icons.iconarchive.com/icons/martin-berube/character/256/Robot-icon.png";
    server = args.server;
    device = args.device;
    os_version = args.os_version
    commit_hash = args.commit_hash;
    tc_tags = args.test_case_tags;
    test_summary = args.test_summary;
    log_link = args.log_link;
    report_link = args.report_link;
    jira_filter_id = args.jira_filter_id;
    username = args.username
    password = args.password

    slack = slackweb.Slack(url=webhook_url);

    # constructing attachments
    attachments = []
    attachment = {"fallback": platform + " test on " + commit_hash + " completed!",
                  "footer": footer_text,
                  "footer_icon": footer_icon,
                  "color": color,
                  "thumb_url": thumb_url,
                  "fields": [
                     
                      {
                          "title": "Platform",
                          "value": platform,
                          "short": "true"
                      },

                      {
                          "title": "Server",
                          "value": server,
                          "short": "true"
                      },

                      {
                          "title": "Device",
                          "value": device,
                          "short": "false"
                      },

                      {
                          "title": "OS Version",
                          "value": os_version,
                          "short": "false"
                      },

                      {
                          "title": "Build Hash",
                          "value": commit_hash,
                          "short": "true"
                      },

                      {
                          "title": "Test Case",
                          "value": tc_tags,
                          "short": "true"
                      },

                      {
                          "title": "Test Summary:",
                          "value": test_summary + "\n(<" + report_link + "|view report>)" + " (<" + log_link + "|logs/videos>)" 
                      }, 

                      # just separator line
                      {
                          "title": "", 
                          "value": ""
                      },

                      {
                          "title": platform + " Issues Impacts Automation:",
                          "value": get_jira_list(jira_filter_id),
                          
                      }

                  ], }

    attachments.append(attachment)
    slack.notify(attachments=attachments)

# get list of open jira issues
def get_jira_list(jira_filter_id): 
    jira_list = "";

    if not jira_filter_id: 
      jira_list = "JIRA filter is not configurated!"
      return jira_list

    options = {
        'server': jira_host_url
    }
    jira = JIRA(options, basic_auth=(username, password))
  
    issues = jira.search_issues('filter=' + jira_filter_id)

    if (len(issues) == 0):
      jira_list = "None"
    else: 
      for issue in issues:
        link = jira_host_url ＋ "/browse/" + issue.key
        summary = issue.fields.summary
        key = issue.key
        jira_list += "<%s|%s> %s\n" % (link, key, summary);
    return jira_list;

if __name__ == '__main__':
    notify()
