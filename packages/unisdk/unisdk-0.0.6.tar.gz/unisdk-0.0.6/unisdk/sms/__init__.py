from unisdk.core import Uni

class UniSMS:
  def __init__(self, *args, **kwargs):
    self.client = Uni(*args, **kwargs)

  def send(self, params):
    return self.client.request("sms.message.send", params)
