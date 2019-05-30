
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import warnings

warnings.filterwarnings("ignore")


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Node:

    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []
        self.subdivide = False



def recursive_subdivide(node, k):
    if len(node.points) <= k:
        return

    w_ = (node.width / 2)
    h_ = (node.height / 2)
    node.subdivide = True
    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p)
    recursive_subdivide(x1, k)

    p = contains(node.x0, node.y0 + h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0 + h_, w_, h_, p)
    recursive_subdivide(x2, k)

    p = contains(node.x0 + w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursive_subdivide(x3, k)

    p = contains(node.x0 + w_, node.y0 + h_, w_, h_, node.points)
    x4 = Node(node.x0 + w_, node.y0 + h_, w_, h_, p)
    recursive_subdivide(x4, k)

    node.points = None
    node.children = [x1, x2, x3, x4]


def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x + w and point.y >= y and point.y <= y + h:
            pts.append(point)
    return pts


def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += (find_children(child))
    return children


def get_input(n):
    f = open(n, "r")
    inputdata = []

    for i in range(100000):
        dt = f.readline()
        dt = dt.strip("\n")
        dt = dt.split(" ")
        tpx = []
        tpy = []

        tpx.append(int(dt[0]))
        tpy.append(int(dt[1]))

        inputdata.append(Point(int(tpx[0]), int(tpy[0])))

    return inputdata


class QTree:
    def __init__(self, k, n=None, wid=None, hei=None, ):

        if wid is not None:

            self.capacity = k
            self.points = [Point(random.randint(0, wid), random.randint(0, hei)) for x in range(n)]
            self.root = Node(0, 0, wid, hei, self.points)

        else:
            file = get_input(n)
            self.capacity = k
            self.points = file
            self.root = Node(0, 0, 1500, 1500, self.points)

    def subdivide(self):
        recursive_subdivide(self.root, self.capacity)

    def insert(self, x, y, node=None):
        if node is None:
            node = self.root
        if node.points is not None:
            if len(node.points) < 4:
                node.points.append(Point(x, y))
                self.points.append(Point(x, y))
            elif len(node.points) == 4:
                node.points.append(Point(x, y))
                self.points.append(Point(x, y))
                recursive_subdivide(node, self.capacity)
        else:
            if node.x0 + node.width / 2 >= x and node.y0 + node.height / 2 >= y:
                self.insert(x, y, node.children[0])
            elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 <= y:
                self.insert(x, y, node.children[3])
            elif node.x0 + node.width / 2 >= x and node.y0 + node.height / 2 <= y:
                self.insert(x, y, node.children[1])
            elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 >= y:
                self.insert(x, y, node.children[2])

    def delete(self, x, y, node=None,):
        if node is None:
            node = self.root
        if node.x0 + node.width / 2 >= x and node.y0 + node.height / 2 >= y:

            if node.points is None:

                self.delete(x, y, node.children[0])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        node.points.remove(Point(i.x, i.y))
                        self.points.remove(Point(i.x, i.y))

                        break
                if flag == 1:
                    print("The point founded and deleted")
                else:
                    print("This point does not exist")

        elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 <= y:

            if node.points is None:

                self.delete(x, y, node.children[3])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        node.points.remove(Point(i.x, i.y))
                        self.points.remove(Point(i.x, i.y))
                        break
                if flag == 1:
                    print("The point founded and deleted")
                else:
                    print("This point does not exist")

        elif node.x0 + node.width / 2 >= x and + node.y0 + node.height / 2 <= y:

            if node.points is None:

                self.delete(x, y, node.children[1])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        node.points.remove(Point(i.x, i.y))
                        self.points.remove(Point(i.x, i.y))

                        break
                if flag == 1:
                    print("The point founded and deleted")
                else:
                    print("This point does not exist")

        elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 >= y:

            if node.points is None:

                self.delete(x, y, node.children[2])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        node.points.remove(Point(i.x, i.y))
                        self.points.remove(Point(i.x, i.y))
                        break
                if flag == 1:
                    print("The point founded and deleted")
                else:
                    print("This point does not exist")

    def search(self, x, y, node=None):
        if node is None:
            node = self.root
        if node.x0 + node.width / 2 >= x and node.y0 + node.height / 2 >= y:

            if node.points is None:

                self.search(x, y, node.children[0])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        break
                if flag:
                    print("Found it")
                else:
                    print("Not in the dataset")
        elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 <= y:

            if node.points is None:

                self.search(x, y, node.children[3])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        break
                if flag:
                    print("Found it")
                else:
                    print("Not in the dataset")
        elif node.x0 + node.width / 2 >= x and + node.y0 + node.height / 2 <= y:

            if node.points is None:

                self.search(x, y, node.children[1])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        break
                if flag:
                    print("Found it")
                else:
                    print("Not in the dataset")
        elif node.x0 + node.width / 2 <= x and node.y0 + node.height / 2 >= y:

            if node.points is None:

                self.search(x, y, node.children[2])
            else:
                flag = 0
                for i in node.points:
                    if i.x == x and i.y == y:
                        flag = 1
                        break
                if flag:
                    print("Found it")
                else:
                    print("Not in the dataset")

    def graph(self):
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print("Number of segments: %d" % len(c))

        areas = set()
        for el in c:
            areas.add(el.width * el.height)
        print("Minimum segment area: %.3f units" % min(areas))
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, '.')
        plt.show()
        return

    '''
        def range(self, x, y, w, h, node=None):
            rangePoints = []

            if node is None:
                node = self.root

            if x <= node.x0 + node.width/2 and y+h <= node.y0 + node.height/2 and x>node.x0 and y+h>node.y0:
                if node.points is None:
                    self.range(x, y, w, h, node.children[0])
                else:
                    for i in node.points:
                        if i.x >= x and i.y <= y + h:
                            rangePoints.append(Point(i.x, i.y))

            if x <= node.x0 + node.width/2 and y >= node.y0 + node.height/2:
                if node.points is None:
                    self.range(x, y, w, h, node.children[1])
                else:
                    for i in node.points:
                        if i.x >= x and i.y <= y + h:
                            rangePoints.append(Point(i.x, i.y))

            if x > node.x0 + node.width/2 and y > node.y0 + node.height/2:
                if node.points is None:
                    self.range(x, y, w, h, node.children[2])
                else:
                    for i in node.points:
                        if i.x >= x and i.x <= x+w and i.y>= y and i.y<=y+h:
                            rangePoints.append(Point(i.x, i.y))

            if x > node.x0 + node.width / 2 and y < node.y0 + node.height / 2:
                if node.points is None:
                    self.range(x, y, w, h, node.children[3])
                else:
                    for i in node.points:
                        if i.x >= x and i.x <= x + w and i.y >= y and i.y <= y + h:
                            rangePoints.append(Point(i.x, i.y))
            for i in rangePoints:
                print("X = {}, Y = {}".format(i.x, i.y))
    '''


def create_input(x, y):
    f = open("dataset100000", "w+")
    for i in range(100000):
        f.write("{} {}\n".format(random.randint(0, x), random.randint(0, y)))
    f.close()




choose = input("Press 'random' to create a random dataset or 'load' to load a dataset")

while choose !='random' or choose !='load':

    if choose == 'random':
        c = int(input("Please enter capacity: "))
        n = int(input("Please enter the number of points: "))
        w = int(input("Please enter the width of graph: "))
        h = int(input("Please enter the height of graph: "))
        qt = QTree(c, n, w, h)
        start = time.time()

        qt.subdivide()
        print('It took', time.time() - start, 'seconds to initialize the tree with', n, 'data.')
        n = input("Please enter :\n 1: for insert \n 2: for search: \n 3: for delete \n 4: for graph \n exit: for exit ")
        while n != 'exit':
            if n == '1':
                x = int(input("Please enter x: "))
                y = int(input("Please enter y: "))
                start = time.time()
                qt.insert(x, y)
                print('It took', time.time() - start, 'seconds to insert.')

            elif n == '2':
                x = int(input("Please enter x "))
                y = int(input("Please enter y "))
                start = time.time()
                qt.search(x, y)
                print('It took', time.time() - start, 'seconds to perform an exact search.')

            elif n == '3':
                x = int(input("Please enter x: "))
                y = int(input("Please enter y: "))
                start = time.time()
                qt.delete(x, y)
                print('It took', time.time() - start, 'seconds to delete the point.')

            elif n == '4':
                qt.graph()
            elif n == '5':
                qt.range(1, 1, 8, 8)

            n = input("Please enter :\n 1: for insert \n 2: for search: \n 3: for delete \n 4: for graph \n exit: for exit ")

    elif choose == 'load':

        file = input("Please enter the name of the file: ")
        qt = QTree(4, file)
        start = time.time()
        qt.subdivide()
        print('It took', time.time() - start, 'seconds to initialize the tree with 100000 data.')
        n = input("Please enter :\n 1: for insert \n 2: for search: \n 3: for delete \n 4: for graph \n exit: for exit ")
        while n != 'exit':
            if n == '1':
                x = int(input("Please enter x: "))
                y = int(input("Please enter y: "))
                start = time.time()
                qt.insert(x, y)
                print('It took', time.time() - start, 'seconds to insert.')

            elif n == '2':
                x = int(input("Please enter x "))
                y = int(input("Please enter y "))
                start = time.time()
                qt.search(x, y)
                print('It took', time.time() - start, 'seconds to perform an exact search.')

            elif n == '3':
                x = int(input("Please enter x: "))
                y = int(input("Please enter y: "))
                start = time.time()
                qt.delete(x, y)
                print('It took', time.time() - start, 'seconds to delete the point.')

            elif n == '4':
                qt.graph()
            elif n == '5':
                qt.range(1, 1, 8, 8)

            n = input("Please enter :\n 1: for insert \n 2: for search: \n 3: for delete \n 4: for graph \n exit: for exit ")
    choose = input("Press 'random' to create a random dataset or 'load' to load a dataset")
# for i in qt.points:
#   print("X = {}, Y = {}".format(i.x, i.y))



