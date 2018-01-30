import os

from unittest import TestCase

import sebot
import credentials

test_channel = 'mbott-test'
test_email = 'mabott@gmail.com'


class TestSebot(TestCase):
    def setUp(self):
        self.sb = sebot.SeBot()

    def test_get_channel_id(self):
        channel_id = 'C17QAG7QU'
        result = self.sb.get_channel_id(test_channel)
        self.assertEqual(channel_id, result)

    def test_get_history(self):
        result = self.sb.get_channel_history(test_channel)
        print result
        self.assertTrue(result)

    def test_get_history_since(self):
        result = self.sb.get_channel_history(test_channel,
                                             since='1462922240.000014')
        print result
        self.assertTrue(result)

    def test_write_timestamp(self):
        ts = '1462922240.000014'
        self.sb.write_timestamp(ts)
        F = open('latest', 'r+')
        read_timestamp = F.read().strip()
        F.close()
        os.unlink('latest')
        self.assertEqual(ts, read_timestamp)

    def test_read_timestamp(self):
        ts = '1462922240.000014'
        F = open('latest', 'w')
        F.write(ts)
        F.close()
        result = self.sb.read_timestamp()
        os.unlink('latest')
        self.assertEqual(ts, result)

    def test_update(self):
        """update should read latest file (using 0 if not found)
        read history since then
        write latest timestamp"""
        ts = '1462922240.000014'
        ts_after = '1462922307.000016'
        F = open('latest', 'w')
        F.write(ts)
        F.close()
        target = self.sb.get_channel_history(test_channel,
                                             since='1462922240.000014')
        result = self.sb.update(test_channel)
        F = open('latest', 'r')
        read_ts = F.read().strip()
        F.close()
        os.unlink('latest')
        self.assertEqual(result, target)
        self.assertEqual(ts_after, read_ts)

    def test_update_no_latest_file(self):
        # ts = '1462922240.000014'
        ts_after = '1462922307.000016'
        target = self.sb.get_channel_history(test_channel)
        result = self.sb.update(test_channel)
        F = open('latest', 'r')
        read_ts = F.read().strip()
        F.close()
        os.unlink('latest')
        self.assertEqual(result, target)
        self.assertEqual(ts_after, read_ts)

    def test_get_latest_timestamp(self):
        ts = '1462922307.000016'
        read_timestamp = self.sb.get_latest_timestamp(
                            self.sb.get_channel_history(test_channel))
        self.assertEqual(ts, read_timestamp)

    def test_send_email(self):
        self.sb.send_email(server=credentials.server,
                           port=credentials.port,
                           subject='A test from SEBOT',
                           sender=credentials.username,
                           recipients=[test_email],
                           body='This is a test. Hello from SEBOT. Had this '
                                'been a real @channel mention, this might '
                                'contain a message from someone in #se.')
