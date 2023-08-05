class Wfr(object):
  
  def __getattribute__(self, attr):
    try:
      attribute = object.__getattribute__(self,attr)
    except:
      return Wfr()
    if callable(attribute):
      return attribute
    else:
      return Wfr()
  def __call__(you):
    return Wfr()
  def set_occupation(self,job):
    self._job = job
  
  """ {'from': 'https://towardsdatascience.com/create-new-functionality-with-getattribute-a6757ee27428'} """
  """ """
class Fwe(Wfr):
  1
class Worker(Wfr):
  1
class Leftist(Wfr):
  1
