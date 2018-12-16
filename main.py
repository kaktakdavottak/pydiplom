# -*- coding: utf8 -*-

import vkclasses
import time
import json
import authsettings


def get_difference_set():
    '''
    Returns a set of groups in vk.com in which the user is composed,
    but none of his friends are members.
    '''
    main_user = vkclasses.VkUser(authsettings.get_setting('settings.ini', 'Settings', 'user_id'))
    main_groupset = main_user.groups()
    main_friedset = main_user.friends()

    common_set = set()
    for e, friend in enumerate(main_friedset):
        try:
            current_user = vkclasses.VkUser(str(friend))
            common_set = common_set.union(current_user.groups())
            print('Осталось {} обращений к API'.format(len(main_friedset) - e))
            # time.sleep(0.3)
        except KeyError:
            print('Осталось {} обращений к API'.format(len(main_friedset) - e))
            # time.sleep(0.3)

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
        current_group = vkclasses.VkGroup(str(group))
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
