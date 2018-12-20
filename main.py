# -*- coding: utf8 -*-

import vkclasses
import json
import authsettings
import time
from tqdm import tqdm


def get_difference_set():
    '''
    Returns a set of groups in vk.com in which the user is composed,
    but none of his friends are members.
    '''
    print('Поиск групп:')
    main_user = vkclasses.VkUser(authsettings.get_setting('settings.ini', 'Settings', 'user_id'))
    main_groupset = main_user.groups()
    main_friedset = main_user.friends()

    common_set = set()
    pbar = tqdm(main_friedset, ncols=120)
    for friend in pbar:
        current_user = vkclasses.VkUser(str(friend))
        common_set = common_set.union(current_user.groups())
        pbar.set_description("Обрабатывается пользователь id %s" % friend)

    difference_set = main_groupset.difference(common_set)

    return difference_set


def get_common_set():
    '''
    Returns a set of groups in vk.com
    in which there are common friends, but no more than N people,
    where N is specified in the code..
    '''
    n = 3
    main_user = vkclasses.VkUser(authsettings.get_setting('settings.ini', 'Settings', 'user_id'))
    main_groupset = main_user.groups()
    main_friedset = main_user.friends()
    common_groups_set = set()

    print('Получение списка общих групп, где друзей не более {} человек:'.format(n))
    pbar = tqdm(main_groupset, ncols=120)
    for group in pbar:
        pbar.set_description("Обрабатывается группа id %s" % group)
        current_group = vkclasses.VkGroup(str(group))
        current_group_members = current_group.members()
        # current_group_members.remove(int(main_user.user_id))

        if 0 < len(main_friedset.intersection(current_group_members)) < n:
            common_groups_set.add(group)

    return common_groups_set


def result_data_to_json(group_id_list, file_name):
    '''
    The function takes group data by their id
    and returns the result to a json file.
    '''
    print('\n\nЗапись информации о группах в файл:')
    group_list = []
    pbar = tqdm(group_id_list, ncols=120)
    for group in pbar:
        pbar.set_description("Обрабатывается группа id %s" % group)
        current_group = vkclasses.VkGroup(str(group))
        group_data = current_group.information()
        iter_dict = dict()
        try:
            for item in group_data['response']:
                iter_dict['name'] = item['name']
                iter_dict['gid'] = item['id']
                iter_dict['members_count'] = item['members_count']
        except KeyError:
            iter_dict['name'] = 'Error'
            iter_dict['gid'] = group
            iter_dict['members_count'] = 'Error'

        group_list.append(iter_dict)
        time.sleep(0.3)

    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # result_data_to_json(get_difference_set(), 'groups.json')
    result_data_to_json(get_common_set(), 'groups2.json')
