#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import requests
import base64

class TwitterInfo:

  def __init__(self):
    self.client_key = '59eI8467xSYcB3BQObzIKtZUi' # 여러분들의 Consumer API key를 넣으세요.
    self.client_secret = 'DwYmzj5wwZtVp80HuF1wGsACYBcPR0oGOuiQjv78Ux72q3laIk' # 여러분들의 Consumer API secret key를 넣으세요.

  def extractLastThreeTweetsFromTwitter(self, account_name):

    key_secret = '{}:{}'.format(self.client_key, self.client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }


    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    # account로 해당 사용자가 올린 tweet 중 마지막 세 개만 추출하라는 의미로 아래와 같은 URL을 만들었음
    search_url = '{}1.1/statuses/user_timeline.json?screen_name={}&count=3'.format(base_url, account_name)
    search_resp = requests.get(search_url, headers=search_headers)
    tweet_data = search_resp.json()

    list_tweets = []

    for i in range(len(tweet_data)):
        # store the text of the tweet
        text = tweet_data[i].get("text")

        # if the tweet contains an image add this to the tweet text
        if(tweet_data[i].get("entities").get("media")):
            image = tweet_data[i].get("entities").get("media")[0].get("media_url_https")
            width = tweet_data[i].get("entities").get("media")[0].get("sizes").get("small").get("w")
            height = tweet_data[i].get("entities").get("media")[0].get("sizes").get("small").get("h")
            url = tweet_data[i].get("entities").get("media")[0].get("url")
            final = text + "<a href = '" + url + "'>" + "<img src = '" +image + "' height =" + str(height) + " width = "+ str(width) + ">" + "</a>"
            list_tweets.append(final)
        # if there is no image, then just save the text of the tweet
        else:
            list_tweets.append(text)

    return list_tweets

def main(dict):

    list_tweets = []

    account_name = dict.get("account")[1:]

    ti = TwitterInfo()

    list_tweets = ti.extractLastThreeTweetsFromTwitter(account_name)

    return { 'message': list_tweets }
