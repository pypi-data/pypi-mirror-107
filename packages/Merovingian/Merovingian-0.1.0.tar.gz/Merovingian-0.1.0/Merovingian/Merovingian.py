class Merovingian:
  def Execute(self):
    self.Execute_Alma_Mater()
    self.Execute_Alma_Mater()
    print("printing __file__")
    print(open(__file__,"r").read())
  def Execute_Alma_Mater(self):
    return Passthrough(True)
    return "Passthrough"
class Passthrough(object):
  def __init__(self,index):
    return
