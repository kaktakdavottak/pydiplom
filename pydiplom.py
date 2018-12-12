import requests
import time
import json


USER_ID = '171691064'  # eshmargunov id on vk.com
TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


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
        params = {
            'user_id': self.user_id,
            'extended': '1',
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        groups_data = response.json()

        groups_set = set()
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


def get_difference_set():
    '''
    Returns a set of groups in vk.com in which the user is composed,
    but none of his friends are members.
    '''
    main_user = VkUser(USER_ID)
    main_groupset = main_user.groups()
    main_friedset = main_user.friends()

    common_set = set()
    for e, friend in enumerate(main_friedset):
        try:
            current_user = VkUser(str(friend))
            common_set = common_set.union(current_user.groups())
            print('Осталось {} обращений к API'.format(len(main_friedset) - e))
            time.sleep(0.3)
        except KeyError:
            print('Осталось {} обращений к API'.format(len(main_friedset) - e))
            time.sleep(0.3)

    difference_set = main_groupset.difference(common_set)

    return difference_set


def result_data_to_json():
    '''
    The function takes group data by their id
    and returns the result to a json file.
    '''
    group_id_list = get_difference_set()
    group_list = []

    for group in group_id_list:
        current_group = VkGroup(str(group))
        group_data = current_group.information()
        iter_dict = dict()

        for item in group_data['response']:
            iter_dict['name'] = item['name']
            iter_dict['gid'] = item['id']
            iter_dict['members_count'] = item['members_count']

        group_list.append(iter_dict)

    with open('groups.json', 'w') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    result_data_to_json()
