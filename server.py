import asyncio
import email

from aiosmtpd.controller import Controller


class MessageHandler:

    # count of accepted messages
    accepted = 0

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # TODO: check delivery rules
        if not address.endswith('@nutty.email'):
            return '550 Email Does Not Exist'

        # update envelope
        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        # TODO: validate SPF
        # ...

        # update envelope
        envelope.mail_from = address
        envelope.mail_options.extend(mail_options)

        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        # TODO: validate DKIM
        # ...

        # TODO: deliver message to maildir
        # ...

        self.accepted += 1

        return '250 Message Accepted'


async def main():
    controller = Controller(MessageHandler())
    controller.start()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(main())
    event_loop.run_forever()

