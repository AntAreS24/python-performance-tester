class Frame:
    def __init__(self, src, x, y) -> None:
        self.src = src
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"{self.src} | x,y:({self.x},{self.y})"

class Effect:
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type
