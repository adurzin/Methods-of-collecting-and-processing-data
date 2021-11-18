import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from instparse.items import InstparseItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = "https://www.instagram.com/accounts/login/ajax/"
    user_name = "_aleks_qwerty_"
    password = "#PWD_INSTAGRAM_BROWSER:10:1637146935:Ab1QAFNlvAm0NU3oQDbkIoaPaF5/t7gZsa01JsuqtQ6v7bIiy6hbomH" \
               "+CCVFOnNcRmYFLdS7iFR/ayl+iJ8UiBif/CrNr/fVriKxPO2waNdpVG6ipyt4jpSyor+DMMvSJ8AyR6mH968okhbl"
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

        yield response.follow(url_followers,
                              callback=self.user_followers_pass,
                              cb_kwargs={'username': username,
                                         # 'variables': deepcopy(variables),
                                         'user_id': user_id},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_followers_pass(self, response: HtmlResponse, username, user_id):
        j_data = response.json()
        page_info = j_data.get('users').get('user').get('edge_owner_to_timeline_media').get('page_info')
        if page_info.get('has_next_page'):
            max_id = j_data.get('next_max_id')
            url_followers = f'{self.followers_url}/followers/?count=12&max_id={max_id}&search_surface=follow_list_page'

            yield response.follow(url_followers,
                                  callback=self.user_followers_pass,
                                  cb_kwargs={'username': username,
                                             # 'variables': deepcopy(variables)
                                             'user_id': user_id})
        users = j_data.get('users')
        for user in users:
            item = InstparseItem(
                user_id=user.get('pk'),
                username=user.get('username'),
                photo=user.get('profile_pic_url')
            )
            yield item

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
