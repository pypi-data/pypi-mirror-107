from classes.karma import getKarma
from classes.raw import getRaw
#from gets.karma import getKarmaCount
#compare = getKarmaCount("RayhanADev")
class Parser:
  def __init__(self, request):
    self.data = request 
  def cycles(self):
    return getKarma(self.data)
  def raw(self):
    return getRaw(self.data)

# newerthing = Parser(newthing)
# print(type(newerthing.cycles()))