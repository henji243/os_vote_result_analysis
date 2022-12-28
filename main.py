import os
import requests
import json
import matplotlib.pyplot as plt


url = "https://clouddata.scratch.mit.edu/logs?projectid=643164196&limit=999&offset=0"
res = requests.get(url).json()


def extract_data(data):
    KEYS = ["user", "name", "value"]
    OS_TYPES = ["Windows", "Mac", "ChromeOS", "Linux", "Other"]
    extract_result = dict(filter(lambda dic: dic[0] in KEYS, data.items()))
    os_name = extract_result["name"][2:]

    if os_name.lower().replace(" ", "") in list(map(lambda x: x.lower(), OS_TYPES)):
        type_index = list(
            map(lambda x: x.lower(), OS_TYPES)
        ).index(os_name.lower().replace(" ", ""))
        extract_result["name"] = OS_TYPES[type_index]
    elif os_name == "その他":
        extract_result["name"] = "Other"
    return extract_result


latest_vote_count = {"Windows": 0, "Mac": 0, "Linux": 0, "ChromeOS": 0, "Other": 0}
for i in res:
    j = extract_data(i)
    try:
        if latest_vote_count[j["name"]] == 0:
            latest_vote_count[j["name"]] = j["value"]
    except KeyError:
        pass

all_vote_count = sum(latest_vote_count.values())

voter_list = [extract_data(i) for i in res]
voted_person = list()

original_data = {"Windows": 0, "Mac": 0, "Linux": 0, "ChromeOS": 0, "Other": 0}
extracted_data = original_data.copy()

for i in voter_list:
    if i["name"] not in original_data.keys():
        continue
    if (
        not (votedata := (i["user"], i["name"])) in voted_person
        or i["user"] == "henji243"
    ):
        voted_person.append(votedata)
        extracted_data[votedata[1]] += 1
    original_data[votedata[1]] += 1
del voted_person  # 一応軽量化の為消しておく

for _ in range(5):
    i = tuple(original_data.items())
    j = tuple(extracted_data.items())
    latest_vote_count[i[_][0]] -= i[_][1]
    latest_vote_count[i[_][0]] += j[_][1]

print(latest_vote_count)

plt.pie(
    latest_vote_count.values(),
    labels=latest_vote_count.keys(),
    autopct="%1.2f%%",
    startangle=90,
    counterclock=False,
)
plt.axis("equal")
plt.show()
