import requests

base_url = "http://127.0.0.1:5000"

# endpoint = "/api/is_key_used"
#
# headers = {
#     "key": "yteyertyterrtytryer"
# }
#
# response = requests.get(base_url + endpoint, headers=headers)
#
# print(response.status_code)
# print(response.text)

endpoint = "/api/vote"

headers = {
    "key": "hdjytyeurtyertyerty",
    "number": "1"
}

response = requests.post(base_url + endpoint, headers=headers)

print(response.status_code)
print(response.text)
