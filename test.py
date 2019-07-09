import asyncio
import sys

from aiosmtpd.controller import Controller
from colorama import Fore
from server import MessageHandler
from telnetlib import Telnet


# ----------------------------------------------------------------------
#  TEST CASES
# ----------------------------------------------------------------------


async def test_send_message(h):
    before = h.accepted
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
    assert h.accepted > before


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
    # start smtp server
    handler = MessageHandler('./mailbox')
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
            await globals()[test](handler)
        except AssertionError:
            fail()
            continue
        succeed()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_tests())
    sys.exit(failed_tests)

