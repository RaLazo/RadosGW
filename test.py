class Robot(object):
    def __init__(self, x, y, z):
        self.x=x
        self.y=y
        self.z=z
    def puts(self):
        print(self.x)
        print(self.y)
        print(self.z)

lisa = Robot("hallo",'aaa',3)
lisa.puts()
