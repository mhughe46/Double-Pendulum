import math

def PolarVector(theta, length=1):
    return Vector2(math.cos(theta-math.pi/2) * length, math.sin(theta-math.pi/2) * length)


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + " " + str(self.y)

    def ToTuple(self):
        return (self.x, self.y)
        
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
        
    def __iadd__(self,other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __isub__(self, other):
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)
        
    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)
        
    @property
    def magnitude(self):
        return math.sqrt(pow(self.x,2) + pow(self.y,2))
        
    @property
    def norm(self):
        return self / self.magnitude

    @property
    def orth(self):
        return Vector2(-self.y, self.x)
        
    @property
    def tuple(self):
        return (self.x, self.y)
    
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)