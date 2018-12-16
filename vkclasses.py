import requests
import authsettings
import time


USER_ID = authsettings.get_setting('settings.ini', 'Settings', 'user_id')
TOKEN = authsettings.get_setting('settings.ini', 'Settings', 'token')


class VkUser:

    def __init__(self, user_id):
        self.user_id = user_id

    def friends(self):
        '''
        Returns a set of id of friends of the user.
        The function uses the method friends.get from API vk.com
        https://vk.com/dev/friends.get
        '''
        params = {
            'user_id': self.user_id,
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'domain'
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friends_data = response.json()

        friends_set = set()
        for friend in friends_data['response']['items']:
            friends_set.add(friend['id'])

        return friends_set

    def groups(self):
        '''
        Returns a set of id of communities for the specified user.
        The function uses the method groups.get from API vk.com
        https://vk.com/dev/groups.get
        '''

        errors = [18, 7]  # possible errors from api vk
        repeat = True
        groups_set = set()
        while repeat:
            params = {
                'user_id': self.user_id,
                'extended': '1',
                'access_token': TOKEN,
                'v': '5.92',
                'fields': 'members_count'
            }
            response = requests.get('https://api.vk.com/method/groups.get', params)
            groups_data = response.json()

            if 'error' in groups_data and 'error_code' in groups_data['error']\
                    and groups_data['error']['error_code'] in errors:
                groups_set = set()
                repeat = False
            elif 'error' in groups_data and 'error_code' in groups_data['error']\
                    and groups_data['error']['error_code'] == 6:
                time.sleep(1)
            else:
                repeat = False
                for group in groups_data['response']['items']:
                    groups_set.add(group['id'])

        return groups_set


class VkGroup:

    def __init__(self, group_id):
        self.group_id = group_id

    def information(self):
        '''
        Returns information about the specified community or multiple communities.
        The function uses the method groups.getById from API vk.com
        https://vk.com/dev/groups.getById
        '''
        params = {
            'group_id': self.group_id,
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        group_data = response.json()

        return group_data
