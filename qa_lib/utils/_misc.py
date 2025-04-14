def cached(fun):
  def modifier(self):
    name = '__' + fun.__name__
    if getattr(self, name, None) is None:
      setattr(self, name, fun(self))
    return getattr(self, name)
  return modifier

class Singleton(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]