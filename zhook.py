import requests
import openziti
import json
import sys
import os


class GithubWebhookBody:

  def __init__(self, eventJsonStr):
    self.eventJsonStr = eventJsonStr
    self.eventJson = json.loads(eventJsonStr)
    # self.repoJson = self.eventJson["repository"]
    # self.senderJson = self.eventJson["sender"]

    self.body = self.eventJson
    # self.body["inputs"] = self.inputs
    # self.body["data"] = self.extraData

  def dumpJson(self):
    return json.dumps(self.body)


if __name__ == '__main__':
  zitiId = os.getenv("INPUT_ZITIID")
  url = os.getenv("INPUT_WEBHOOKURL")
  eventJsonStr = os.getenv("INPUT_EVENTJSON")

  # Setup Ziti identity
  idFilename = "id.json"
  os.environ["ZITI_IDENTITIES"] = idFilename
  with open(idFilename, 'w') as f:
    f.write(zitiId)

  # Create webhook body
  try:
    webhook_body = GithubWebhookBody(eventJsonStr)
  except Exception as e:
    print(f"Exception creating webhook body: {e}")
    sys.exit(-1)

  # Post the webhook over Ziti
  headers = {'Content-Type': 'application/json'}
  data = webhook_body.dumpJson()
  print(f"{data}")

  with openziti.monkeypatch():
    try:
      r = requests.post(url, headers=headers, data=data)
      print(f"Response Status: {r.status_code}")
      print(r.headers)
      print(r.content)
    except Exception as e:
      print(f"Exception posting webhook: {e}")
      sys.exit(-1)
