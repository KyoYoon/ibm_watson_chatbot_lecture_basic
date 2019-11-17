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
import urllib3
import json
import requests

class WikiQAInfo:

  def __init__(self):
    self.openApiURL = 'http://aiopen.etri.re.kr:8000/WikiQA'
    self.accessKey = 'a54726fd-bc39-4197-a25e-83028b25f614' # 여러분들의 access key 를 넣으세요.
    self.type = "hybridqa"

  def extractSearchResultFromWiki(self, question):

    bot_answer = ''

    requestJson = {
      "access_key": self.accessKey,
      "argument": {
      "question": question,
        "type": self.type
      }
    }

    http = urllib3.PoolManager()
    response = http.request(
      "POST",
      self.openApiURL,
      headers = {"Content-Type": "application/json; charset=UTF-8"},
      body = json.dumps(requestJson)
    )

    r = response.data.decode('utf-8')
    json_obj = json.loads(r)

    # 4가지 경우를 다 대비해서 코드를 작성
    if response.status == 200 and json_obj['result'] == 0:

      if len(json_obj['return_object']['WiKiInfo']['AnswerInfo']) == 0: # 아예 답변이 비어있는 경우
        bot_answer = "문의하신 내용에 대해 답변을 찾을 수 없습니다."
      else: # 답변이 있는 경우 - 제대로 된 답변, 이상한 답변, "정의를 찾을 수 없습니다." 세 경우 중 하나
        bot_answer = json_obj['return_object']['WiKiInfo']['AnswerInfo'][0]['answer']

    else:
      bot_answer = "ETRI가 연결이 안되서 답변을 드리지 못하고 있습니다."

    return bot_answer

def main(dict):

    question = dict.get("wiki_sentence")

    wqai = WikiQAInfo()

    bot_answer = wqai.extractSearchResultFromWiki(question)

    return { 'message': bot_answer }
