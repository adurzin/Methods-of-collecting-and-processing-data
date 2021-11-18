import scrapy
from scrapy.http import HtmlResponse
import re
import json
from instparse.items import InstparseItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = "https://www.instagram.com/accounts/login/ajax/"
    user_name = "Onliskill_udm"
    password = "#PWD_INSTAGRAM_BROWSER:10:1637258985:AchQAN88QIW9ZlZziJcXfvU/Yk1zHgjLW6vSm3ed/PqY8kxHVUAmn5I/" \
               "qBPFVZxRO4PnTEAFnXHXWK5AZqkqgnXIObvoRj7T44Bc1f/9HeAux7Zf/E+4bwCN52JzL1HOCYjSbrKRB2zUq6qm67og"
    user_for_parse = "ai_machine_learning"
    followers_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={"username": self.user_name,
                      "enc_password": self.password},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get("authenticated"):
            yield response.follow(
                f'/{self.user_for_parse}/',
                callback=self.user_parse,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        url_followers = f'{self.followers_url}{user_id}/followers/?count=12&search_surface=follow_list_page'
        url_following = f'{self.followers_url}{user_id}/following/?count=12'

        yield response.follow(url_followers,
                              callback=self.user_followers_pass,
                              cb_kwargs={'username': username,
                                         'user_id': user_id},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        yield response.follow(url_following,
                              callback=self.user_following_pass,
                              cb_kwargs={'username': username,
                                         'user_id': user_id},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_following_pass(self, response: HtmlResponse, username, user_id):
        j_data = response.json()
        if j_data.get('next_max_id'):
            max_id = j_data.get('next_max_id')
            url_following = f'{self.followers_url}{user_id}/following/?count=12&max_id={max_id}'

            yield response.follow(url_following,
                                  callback=self.user_following_pass,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        users = j_data.get('users')
        for user in users:
            item = InstparseItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                photo=user.get('profile_pic_url'),
                user_type='following'
            )
            yield item

    def user_followers_pass(self, response: HtmlResponse, username, user_id):
        j_data = response.json()
        if j_data.get('next_max_id'):
            max_id = j_data.get('next_max_id')
            url_followers = f'{self.followers_url}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

            yield response.follow(url_followers,
                                  callback=self.user_followers_pass,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        users = j_data.get('users')
        for user in users:
            item = InstparseItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                photo=user.get('profile_pic_url'),
                user_type='follower'
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
