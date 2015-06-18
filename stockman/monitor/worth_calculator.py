from monitor.models.Trigger import Trigger
from monitor.attribute import Attribute

worth = 0

tl = Trigger.objects.filter(bias='-')
for t in tl:
  try:
    worth += Attribute.expected_returns(trigger=t)
  except Exception as e:
    print e

print worth
