class Vector2:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def tuple(self):
    return (self.x,self.y)

  def list(self):
    return [self.x,self.y]