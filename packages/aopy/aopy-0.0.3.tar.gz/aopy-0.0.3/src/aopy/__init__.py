"""
Unofficial module for retrieving AoPS data using Python.
"""
import requests
import re
import json
import platform

__version__ = '0.0.3'


class Session(requests.Session):
    AJAX_URL = 'https://artofproblemsolving.com/m/community/ajax.php'
    AJAX_LOGIN_URL = 'https://artofproblemsolving.com/ajax.php'

    def __init__(self, reload_on_creation=False):
        """Creates a new AoPS session. If reload_on_creation is True it will also call reload_session."""
        super().__init__()
        self.headers.update({
            'User-Agent': f'aopy/{__version__} ({platform.system()}; Python {platform.release()}) \
python-requests/{__version__}'})
        self.session_data = None
        if reload_on_creation:
            self.reload()

    def send_ajax(self, url=AJAX_URL, **data):
        """Sends AJAX request with session data"""
        data_to_send = {key: (None, str(value)) for key, value in data.items()}
        data_to_send['aops_logged_in'] = (None, "false")
        data_to_send['aops_user_id'] = (None, self.session_data['user_id'])
        data_to_send['aops_session_id'] = (None, self.session_data['id'])
        return self.post(url, files=data_to_send).json()

    def send_request(self, data, add_session=True):
        """Try to use send_ajax instead. Sends a request. Adds session data if add_session is true."""
        data_to_send = {key: (None, value) for key, value in data.items()}
        if add_session:
            data_to_send['aops_logged_in'] = (None, str(self.session_data['logged_in'].lower()))
            data_to_send['aops_user_id'] = (None, self.session_data['user_id'])
            data_to_send['aops_session_id'] = (None, self.session_data['id'])
        return self.post(self.AJAX_URL, files=data_to_send).json()["response"]

    def reload(self):
        """Reloads the session."""
        self.session_data = json.loads(
            re.search(r"AoPS.session.+?}", self.get('https://artofproblemsolving.com/').text).group(0)[15:])

    def get_thread_posts(self, topic_id, start_post_num=1):
        """Gets posts in topic (up to 20,000)"""
        return self.send_ajax(
            topic_id=topic_id,
            direction='forwards',
            start_post_id=-1,
            start_post_num=start_post_num,
            show_from_time=-1,
            num_to_fetch=20000,  # Must implement segmented loading for longer threads.
            a='fetch_posts_for_topic',
        )

    def get_forum_score(self, category_id):
        """Retrieve the forum score. Returns -1 if not found."""
        data = self.send_ajax(
            category_id='9',
            log_visit='0',
            fetch_all='1',
            a='fetch_more_items')["response"]['items']
        for i in data:
            if category_id == i['item_id'] or category_id == i['item_text']:
                return int(i['item_score'])
        return -1

    def get_forum_threads(self, category_id):
        return self.send_ajax(
            category_id=category_id,
            a='fetch_category_data')

    def get_user(self, user_id):
        """Gets data for the user with id user_id."""
        return self.send_ajax(
            user_identifier=user_id,
            a='fetch_user_profile')

    def login(self, username, password, reload=True):
        """Log into AoPS. Experimental!"""
        data = self.send_ajax(
            self.AJAX_LOGIN_URL,
            a='login',
            username=username,
            password=password,
            stay='true')
        if reload:
            self.reload()
        return data

    def logout(self, reload=True):
        """Log out of AoPS. Experimental!"""
        data = self.send_ajax(
            self.AJAX_LOGIN_URL,
            a='logout')
        if reload:
            self.reload()
        return data

    def send_post(self, topic_id, post_text):
        """Send a post (must be logged in)"""
        return self.send_ajax(
            attachments=[],
            post_text=post_text,
            notify_email=0,
            topic_id=topic_id,
            allow_latex_errors=0,
            last_post_num=2,
            last_update_time=0,
            disable_bbcode=0,
            is_announcement=0,
            a='submit_post')

    def create_thread(self, category_id, title, post_text):
        return self.send_ajax(
            category_id=category_id,
            title=title,
            tags=[],
            linked_tag='',
            target_url='',
            target_text='',
            source='',
            post_as_halp=0,
            pm_as_sheriff=0,
            allow_latex_errors=0,
            hidden_tags=[],
            restricted_tags=[],
            removed_autotags=[],
            post_text=post_text,
            notify_email=0,
            attachments=[],
            has_poll=0,
            poll_data={},
            recipients=[],
            disable_bbcode=0,
            is_local_announcement=0,
            is_global_announcement=0,
            announce_through='',
            a='submit_new_topic')

    def fetch_user_posts(self, user_id, fetch_before=0):
        """Fetches a user's posts"""
        return self.send_ajax(
            category_type="user_search_posts",
            log_visit="0",
            required_tag="",
            fetch_before=fetch_before,
            user_id="0",
            fetch_archived="0",
            fetch_announcements="0",
            fetched_user_id=user_id,
            a="fetch_topics")

    def get_blog_posts(self, category_id, fetch_before=0):
        """Fetches blog posts"""
        return self.send_ajax(
            category_type='blog',
            log_visit=1,
            required_tag='',
            fetch_before=fetch_before,
            user_id=0,
            fetch_archived=0,
            fetch_announcements=1,
            category_id=category_id,
            a='fetch_topics',
        )
