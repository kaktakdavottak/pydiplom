import requests
import authsettings
import time


USER_ID = authsettings.get_setting('settings.ini', 'Settings', 'user_id')
TOKEN = authsettings.get_setting('settings.ini', 'Settings', 'token')
API_VER = '5.92'


class VkUser:

    def __init__(self, user_id):
        if str(user_id).isdigit():
            self.user_id = user_id
        else:
            params = {
                'user_ids': user_id,
                'access_token': TOKEN,
                'v': API_VER
            }
            response = requests.get('https://api.vk.com/method/users.get', params)
            user_data = response.json()
            self.user_id = user_data['response'][0]['id']

    def friends(self):
        '''
        Returns a set of id of friends of the user.
        The function uses the method friends.get from API vk.com
        https://vk.com/dev/friends.get
        '''
        params = {
            'user_id': self.user_id,
            'access_token': TOKEN,
            'v': API_VER,
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
        retry_count = 0
        retry_max = 50
        groups_set = set()
        while retry_count < retry_max:
            try:
                repeat = True
                try:
                    while repeat:
                        params = {
                            'user_id': self.user_id,
                            'extended': '1',
                            'access_token': TOKEN,
                            'v': API_VER,
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
                except KeyError:
                    pass
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                retry_count += 1
                continue
            break

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
            'v': API_VER,
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        group_data = response.json()

        return group_data

    def members(self):
        '''
        Returns a set of community members.
        The function uses the method groups.getMembers and execute from API vk.com
        https://vk.com/dev/groups.getMembers, https://vk.com/dev/execute
        '''
        members_set = set()
        count_members = 26000
        ofsets = [of for of in range(0, 25000, 1000)]

        while len(members_set) < count_members:
            params = {
                'code': 'return [API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}),'
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}}), '
                        'API.groups.getMembers({{"group_id": {group_id}, "offset": {}, "count": 1000}})'
                        '];'.format(group_id=self.group_id, *ofsets),
                'access_token': TOKEN,
                'v': API_VER
            }
            response = requests.get('https://api.vk.com/method/execute', params)
            group_members = response.json()
            count_members = group_members['response'][0]['count']

            for i in range(0, 25):
                for item in group_members['response'][i]['items']:
                    members_set.add(item)

            ofsets_iter = [of + 25000 for of in ofsets]
            ofsets = ofsets_iter
            time.sleep(0.3)

        return members_set
