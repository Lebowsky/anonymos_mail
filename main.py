import requests
import random
import string
import os
import time

API = 'https://www.1secmail.com/api/v1/'
domains = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "wwjmp.com",
    "esiix.com",
    "xojxe.com",
    "yoggm.com"
]

domain = random.choice(domains)


def generate_user_name():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))

    return username


def check_mail(mail=''):
    username, domain = mail.split('@')
    rel_link = f'{API}?action=getMessages&login={username}&domain={domain}'
    r = requests.get(rel_link).json()
    if len(r):
        id_list = []
        for i in r:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)
        print(f'У вас {len(r)} входящих')
        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, 'all_mails')

        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        for _id in id_list:
            read_msg = f'{API}?action=readMessage&login={username}&domain={domain}&id={_id}'
            r = requests.get(read_msg).json()

            sender = r.get('from')
            subject = r.get('subject')
            date = r.get('date')
            content = r.get('textBody')

            mail_file_path = os.path.join(final_dir, f'{_id}.txt')

            with open(mail_file_path, 'w', encoding='utf-8') as fp:
                fp.write(f'Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')

    else:
        print('На почте пока нет сообщений')


def delete_mail(mail=''):
    url = 'https://www.1secmail.com/mailbox'

    username, domain = mail.split('@')

    data = {
        'action': 'deleteMailBox',
        'login': username,
        'domain': domain
    }

    r = requests.post(url, data=data)
    print(f'Почтовый адрес {mail} удален\n')


def main():
    username = generate_user_name()
    mail = f'{username}@{domain}'
    login, mail_domain = mail.split('@')
    print(mail)
    try:
        mail_req = requests.get(f'{API}?login={username}&domain={mail_domain}')

        while True:
            check_mail(mail=mail)
            time.sleep(5)

    except KeyboardInterrupt:
        delete_mail(mail)
        print('Программа прервана')


if __name__ == '__main__':
    main()
