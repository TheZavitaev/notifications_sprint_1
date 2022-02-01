from .abstract import EmailSenderAbstract


class EmailSenderSendgrid(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        # todo do something
        pass
