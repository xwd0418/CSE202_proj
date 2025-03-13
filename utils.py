EMPTY = 0
STONE = 1
APPLE = 2
GRASS = 3

def cost_of_resource_collecting(resource):
    if resource == STONE:
        return 10
    elif resource == APPLE:
        return 0
    elif resource == GRASS:
        return 10
    

class Map:
    def __init__(self, matrix):
        self.matrix = matrix
        self.stones = []
        self.apples = []
        self.grass = []
        self.size = matrix.shape[0]

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] == STONE:
                    self.stones.append((i, j))
                elif matrix[i, j] == APPLE:
                    self.apples.append((i, j))
                elif matrix[i, j] == GRASS:
                    self.grass.append((i, j))

    

class Player:
    def __init__(self, start_point, initial_h, matrix):
        self.position = start_point
        self.h = initial_h
        self.rewards = 0
        self.matrix = matrix

    @property
    def x(self):
        return self.position[0]
    
    @x.setter
    def x(self, value):
        self.position[0] = value
    
    @property
    def y(self):
        return self.position[1]
    
    @y.setter
    def y(self, value):
        self.position[1] = value

    def able_to_arrive(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.h

    def able_to_go_and_collect(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.h + cost_of_resource_collecting(self.matrix[x, y])

    def go_and_collect_resource(self, x, y):
        resource = self.matrix[x, y]
        assert self.able_to_go_and_collect(x, y), "Not able to go and collect the resource"
        self.h -= abs(self.x - x) + abs(self.y - y) + cost_of_resource_collecting(resource)
        if resource == APPLE:
            self.h += 10
        
        self.x = x
        self.y = y
        self.matrix[x, y] = 0
        self.rewards += 1
        # print("rewards", self.rewards)


# collecting every 2 stones and 1 grass is considered as 1 point 
class Player_P3(Player):
    def __init__(self, start_point, initial_h, matrix):
        super().__init__(start_point, initial_h, matrix) 
        self.num_stones = 0
        self.num_grass = 0


    def able_to_arrive(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.h and self.num_stones + self.num_grass <= 3

    def able_to_go_and_collect(self, x, y):
        return abs(self.x - x) + abs(self.y - y) <= self.h + cost_of_resource_collecting(self.matrix[x, y]) and self.num_stones + self.num_grass <= 3

    def go_and_collect_resource(self, x, y):
        resource = self.matrix[x, y]
        assert self.able_to_go_and_collect(x, y), "Not able to go and collect the resource"
        self.h -= abs(self.x - x) + abs(self.y - y) + cost_of_resource_collecting(resource)
        self.x = x
        self.y = y
        
        if self.num_stones == 2 and self.num_grass == 1:
            self.num_stones = 0
            self.num_grass = 0
            self.rewards += 1