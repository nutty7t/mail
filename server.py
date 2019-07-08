import asyncio

from aiosmtpd.controller import Controller


class MessageHandler:

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # TODO: check delivery rules
        if not address.endswith('@nutty.email'):
            return '550 Not Relaying to that Email Address'
        return '250 OK'

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        # TODO: validate SPF
        # ...
        pass

    async def handle_DATA(self, server, session, envelope):
        # TODO: validate DKIM
        # ...

        # TODO: deliver message to maildir
        message = self.prepare_message(session, envelope)
        # ...

        return '250 OK'


async def main():
    controller = Controller(MessageHandler())
    controller.start()


if __name__ == '__main__':
    print("hello from smtp server")
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(main())
    event_loop.run_forever()

