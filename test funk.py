import vkclasses
import json
import authsettings
import time
from tqdm import tqdm
import requests
import authsettings
import time
from pprint import pprint

import requests


members_set = set()
count_members = 192274
ofsets = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000]

while len(members_set) < count_members:
    params = {
        'code': 'return [API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}),'
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}}), '
                'API.groups.getMembers({{"group_id": 24946565, "offset": {}, "count": 1000}})];'.format(*ofsets),
        'access_token': 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae',
        'v': '5.92'
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

print(len(members_set))
# print(members_set)

# print(members_set)
# print(len(members_set))
# print(len(group_members['response'][0]['items']) + len(group_members['response'][1]['items']) + len(group_members['response'][2]['items']))
# pprint(group_members)
# 'return API.groups.getMembers({"group_id": 30683033, "offset": 0, "count": 1000})'
