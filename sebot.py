import sys
import smtplib

from email.mime.text import MIMEText
from slackclient import SlackClient

import credentials
from credentials import username, password, token, channel


EMAIL_TO = ['mabott@gmail.com']

sc = SlackClient(token)


class SeBot(object):
    def get_channel_id(self, channel_name):
        response = sc.api_call('channels.list', exclude_archive='1')
        # print response
        result = [channel for channel in response['channels']
                    if channel['name'] == channel_name][0]['id']
        return result

    def get_channel_history(self, channel_name, since='0'):
        channel_id = self.get_channel_id(channel_name)
        response = sc.api_call('channels.history', channel=channel_id, oldest=since)
        result = [line for line in response['messages']]
        return result

    def write_timestamp(self, timestamp):
        F = open('latest', 'w')
        F.write(timestamp)

    def read_timestamp(self):
        F = open('latest', 'r+')
        result = F.read()
        return result

    def update(self, channel_name):
        try:
            ts = self.read_timestamp()
        except IOError:  # the timestamp file doesn't exist
            ts = '0'
        result = self.get_channel_history(channel_name, since=ts)
        if result:
            new_ts = self.get_latest_timestamp(result)
            self.write_timestamp(new_ts)
        return result

    def get_latest_timestamp(self, history):
        # if you try to use str() here you will lose precision in the float!
        result = repr(max([float(line['ts']) for line in history]))
        return result

    def send_email(self, server, port, subject, sender, recipients, body):
        smtpserver = smtplib.SMTP(server, port)
        smtpserver.ehlo()
        smtpserver.starttls()
        try:
            smtpserver.login(username, password)
        except smtplib.SMTPException:
            print "SMTPAuth not supported by %s, skipping" % server
        msg = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        smtpserver.sendmail(sender, recipients, msg.as_string())
        smtpserver.quit()


if __name__ == '__main__':
    update_found = False
    SB = SeBot()
    lines = SB.update(channel)
    if not lines:
        print "No new updates"
        sys.exit(0)
    for line in lines:
        print line['text'].encode('utf-8')
        if '<!channel>' in line['text']:
            update_found = True
            SB.send_email(server=credentials.server,
                   port=credentials.port,
                   subject='Slack @channel->email update from SEBOT',
                   sender=credentials.username,
                   recipients=EMAIL_TO,  # TODO: add command line option
                   body=line['text'])
    if not update_found:
        print "No @channel mentions found"
    else:
        print "@channel mentions found, e-mail sent"