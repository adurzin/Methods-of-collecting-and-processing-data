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
    user_name = "_alekskek_"
    password = "#PWD_INSTAGRAM_BROWSER:10:1637262838:AUpQAF3p5eN/+wadHJ/A4H720kHk0Dzp39ZGr+9wUeH7HSRbS8DBRIYjvP" \
               "mxlnS2RL853kT8aEoqjyupRPIMrFGUOpsjT/GO2KYXny9FxMEMHk8RhSPRbLJQiLVxiHYg5Pmkq2GNM5TLF+t6"
    user_for_parse = ["_alekskek_", "griboochka"]
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
            for user in self.user_for_parse:
                yield response.follow(
                    f'/{user}/',
                    callback=self.user_parse,
                    cb_kwargs={'username': user}
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
                account=username,
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
            url_followers = f'{self.followers_url}{user_id}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

            yield response.follow(url_followers,
                                  callback=self.user_followers_pass,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        users = j_data.get('users')
        for user in users:
            item = InstparseItem(
                account=username,
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
