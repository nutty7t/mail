import asyncio
import os
import sys
import tempfile

from aiosmtpd.controller import Controller
from colorama import Fore
from mailbox import Maildir
from server import MessageHandler
from telnetlib import Telnet


# ----------------------------------------------------------------------
#  TEST CASES
# ----------------------------------------------------------------------


async def test_send_message(mailbox):
    mail_count = len(mailbox)
    tn = Telnet('localhost', port=8025)
    tn.write(b'EHLO test.nutty.dev\r\n')
    tn.write(b'MAIL FROM: integration@test.nutty.dev\r\n')
    tn.write(b'RCPT TO: someone@nutty.email\r\n')
    tn.write(b'DATA\r\n')
    tn.write(b'Subject: Test Email\r\n\r\n')
    tn.write(b'Hello, this is a test email from test_send_message\r\n\r\n')
    tn.write(b'.\r\n')
    tn.write(b'QUIT\r\n')
    tn.read_all()
    assert len(mailbox) > mail_count


# ----------------------------------------------------------------------
#  TEST RUNNER
# ----------------------------------------------------------------------


# plz don't fail (・_・;)
failed_tests = 0


def succeed():
    # (✿◠‿◠)
    print(Fore.GREEN + 'OK' + Fore.RESET)


def fail():
    # (╯°□°)╯︵ ┻━┻
    print(Fore.RED + 'FAIL' + Fore.RESET)
    global failed_tests
    failed_tests += 1


async def run_tests():
    with tempfile.TemporaryDirectory() as maildir:
        # create temporary mailbox
        for d in ['cur', 'new', 'tmp']:
            maildirdir = os.path.join(maildir, d)
            os.mkdir(maildirdir)
        mailbox = Maildir(maildir)

        # start smtp server
        handler = MessageHandler(maildir)
        controller = Controller(handler)
        controller.start()

        # run tests
        tests = filter(
            lambda f: f.startswith('test_'),
            globals().keys(),
        )
        for test in tests:
            print(test + '...', end=' ')
            try:
                await globals()[test](mailbox)
            except AssertionError:
                fail()
                continue
            succeed()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_tests())
    sys.exit(failed_tests)

