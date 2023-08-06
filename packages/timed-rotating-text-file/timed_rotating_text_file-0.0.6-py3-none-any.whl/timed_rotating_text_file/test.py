import datetime
import os
import sys
import tempfile
import time
from unittest import TestCase

from timed_rotating_text_file import TimedRotatingTextFile


class Test(TestCase):
    def setUp(self):
        fd, self.fn = tempfile.mkstemp(".log", "test_timed_rotating_text_file-")
        os.close(fd)
        self.rm_files = []

    def tearDown(self):
        for fn in self.rm_files:
            os.unlink(fn)
        if os.path.exists(self.fn):
            os.unlink(self.fn)

    def assertFile(self, filename):
        self.assertTrue(os.path.exists(filename), msg=f"File {filename} does not exist")
        self.rm_files.append(filename)

    def listFiles(self, now):
        dn, fn = os.path.split(self.fn)
        files = [f for f in os.listdir(dn) if f.startswith(fn)]
        print('Test time: %s' % now.strftime("%Y-%m-%d %H-%M-%S"), file=sys.stderr)
        print('The only matching files are: %s' % files, file=sys.stderr)
        for f in files:
            print('Contents of %s:' % f)
            path = os.path.join(dn, f)
            with open(path, 'r') as tf:
                print(tf.read())

    def test_timed_rotating_text_file(self):
        now = datetime.datetime.now()
        with TimedRotatingTextFile(self.fn, when="s", backup_count=2) as filepath:
            filepath.write(f"Test Write on {datetime.datetime.now().strftime('%A %d %B %Y %H:%M:%S')}")
            self.assertFile(self.fn)

            time.sleep(2.1)

            filepath.write(f"Test Write on {datetime.datetime.now().strftime('%A %d %B %Y %H:%M:%S')}")

        self.listFiles(now)
        found = False
        go_back = 5 * 60  # seconds
        for secs in range(go_back):
            prev = now - datetime.timedelta(seconds=secs)
            fn = self.fn + prev.strftime(".%Y-%m-%d_%H-%M-%S")
            found = os.path.exists(fn)
            if found:
                self.rm_files.append(fn)
            break
        msg = 'No rotated files found, went back %d seconds' % go_back
        if not found:
            self.listFiles(now)

        self.assertTrue(found, msg=msg)
