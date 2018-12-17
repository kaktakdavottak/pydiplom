# -*- coding: utf8 -*-

import vkclasses
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
        current_user = vkclasses.VkUser(str(friend))
        common_set = common_set.union(current_user.groups())
        print('Осталось {} обращений к API'.format(len(main_friedset) - e))

    difference_set = main_groupset.difference(common_set)

    return difference_set


def get_common_set():
    '''
    Returns a set of groups in vk.com
    in which there are common friends, but no more than N people,
    where N is specified in the code..
    '''
    n = 197
    main_user = vkclasses.VkUser(authsettings.get_setting('settings.ini', 'Settings', 'user_id'))
    main_groupset = main_user.groups()
    main_friedset = main_user.friends()

    common_set = set()
    for e, friend in enumerate(main_friedset):
        current_user = vkclasses.VkUser(str(friend))
        common_set = common_set.union(current_user.groups())
        print('Осталось {} обращений к API'.format(len(main_friedset) - e))

    common_set_with_main = main_groupset.intersection(common_set)
    common_groups_set = set()
    try:
        for e, group in enumerate(common_set_with_main):
            current_group = vkclasses.VkGroup(str(group))
            current_group_members = current_group.members()
            if len(main_friedset.union(current_group_members)) < n:
                common_groups_set.add(group)
            print('Осталось {} обращений к API'.format(len(common_set_with_main) - e))
    except KeyError:
        print('Осталось {} обращений к API'.format(len(common_set_with_main) - e))

    return common_groups_set


def result_data_to_json(group_id_list, file_name):
    '''
    The function takes group data by their id
    and returns the result to a json file.
    '''
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

    with open(file_name, 'w') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # result_data_to_json(get_difference_set(), 'groups.json')
    result_data_to_json(get_common_set(), 'groups2.json')
