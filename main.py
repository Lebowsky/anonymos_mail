import requests
import random
import string
import os
import time


class OneSecMail:
    def __init__(self, mail: str = ''):
        self.api = 'https://www.1secmail.com/api/v1/'
        self.domains = [
            "1secmail.com",
            "1secmail.org",
            "1secmail.net",
            "wwjmp.com",
            "esiix.com",
            "xojxe.com",
            "yoggm.com"
        ]
        self.mail = mail or self.generate_user_name()

    def generate_user_name(self):
        name = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(name) for i in range(10))
        domain = random.choice(self.domains)
        return f'{username}@{domain}'

    @property
    def login(self):
        return self.mail.split('@')[0]

    @property
    def domain(self):
        return self.mail.split('@')[1]

    def create_mail(self):
        try:
            res = requests.get(f'{self.api}?login={self.login}&domain={self.domain}')
            return res.status_code == 200
        except requests.HTTPError:
            return False

    def get_messages(self):
        try:
            res = requests.get(f'{self.api}?action=getMessages&login={self.login}&domain={self.domain}')
            if res.status_code == 200:
                return res.json()
            else:
                raise requests.HTTPError('status code not 200')
        except requests.HTTPError:
            return []

    def read_message(self, message_id):
        try:
            res = requests.get(f'{self.api}?action=readMessage&login={self.login}&domain={self.domain}&id={message_id}')
            if res.status_code == 200:
                return res.json()
            else:
                raise requests.HTTPError('status code not 200')

        except requests.HTTPError:
            return {}

    def delete_mail(self):
        url = 'https://www.1secmail.com/mailbox'

        data = {
            'action': 'deleteMailBox',
            'login': self.login,
            'domain': self.domain
        }

        try:
            res = requests.post(url, data=data)
            return res.status_code == 200
        except requests.HTTPError:
            return False


def save_message(mail, file_name, msg):
    current_dir = os.getcwd()
    final_dir = os.path.join(current_dir, 'all_mails', mail.split('@')[0])

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    msg_data = dict(
        mail=mail,
        sender=msg.get('from'),
        subject=msg.get('subject'),
        date=msg.get('date'),
        content=msg.get('textBody')
    )

    mail_file_path = os.path.join(final_dir, f'{file_name}.txt')

    with open(mail_file_path, 'w', encoding='utf-8') as fp:
        text = 'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}'.format(**msg_data)
        fp.write(text)


def main():
    provider = OneSecMail()
    try:
        if not provider.create_mail():
            print(f'Ошибка создания почтового ящика: {provider.mail}')
            return

        print(f'Cоздан почтовый ящик: {provider.mail}')

        while True:
            messages = provider.get_messages()
            if messages:
                print(f'У вас {len(messages)} входящих')

                for msg in messages:
                    msg_id = msg.get('id')
                    msg_content = provider.read_message(msg_id)
                    save_message(provider.mail, str(msg_id), msg_content)
            else:
                print(f'Новых писем нет')

            time.sleep(5)

    except KeyboardInterrupt:
        provider.delete_mail()
        print('Программа прервана')


if __name__ == '__main__':
    main()
