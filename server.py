import asyncio
import email
import mailbox
import os

from aiosmtpd.controller import Controller


class MessageHandler:
    """
    Message Handler aiosmtpd hook methods that get called at various
    points in the SMTP dialog.

    handle_RCPT: checks delivery rules in a SQL database to verify that
    the recipient email address exists; the idea is that the user can
    configure a whitelist of email addresses that dictate which emails
    the handler should allow to be delivered.

    handle_MAIL: validates that email messages protect against UVB
    rays -- just kidding -- it validates SPF records.

    handle_DATA: validates DKIM signatures and stores email messages
    in an Maildir directory.
    """

    def __init__(self, maildir=''):
        # check maildir directory
        if not os.path.exists(maildir):
            raise ValueError(f'maildir \'{maildir}\' does not exist')

        # check maildir subdirectories
        for d in ['cur', 'new', 'tmp']:
            maildirdir = os.path.join(maildir, d)
            if not os.path.isdir(maildirdir):
                raise ValueError('not a valid maildir')

        self.maildir = maildir
        self.mailbox = mailbox.Maildir(maildir)

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # TODO: check delivery rules
        if not address.endswith('@nutty.email'):
            return '550 Email Does Not Exist'

        # update envelope
        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        # TODO: validate SPF record
        # ...

        # update envelope
        envelope.mail_from = address
        envelope.mail_options.extend(mail_options)

        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        # TODO: validate DKIM signature
        # ...

        # TODO: check for DMARC compliance
        # ...

        # deliver message to maildir
        message = self.prepare_message(session, envelope)
        self.mailbox.add(message)

        return '250 Message Accepted'

    def prepare_message(self, session, envelope):
        data = envelope.content
        message = email.message_from_bytes(data)
        message['From'] = envelope.mail_from
        message['To'] = ', '.join(envelope.rcpt_tos)

        return message


async def main():
    controller = Controller(MessageHandler(), port=25)
    controller.start()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(main())
    event_loop.run_forever()

