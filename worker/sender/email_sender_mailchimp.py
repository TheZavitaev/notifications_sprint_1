from sender.email_sender_abstract import EmailSenderAbstract
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

class EmailSenderMailchimp(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        pass


