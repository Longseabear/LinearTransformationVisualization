import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.animation as animation
import numpy as np

class rectangle(object):
    def __init__(self, left_top, right_top, left_bottom, right_bottom):
        self.left_top = left_top
        self.right_top = right_top
        self.left_bottom = left_bottom
        self.right_bottom = right_bottom

class graph(object):
    def __init__(self, ax, speed, rect):
        self.speed = speed
        self.point = []
        self.const_rect = rect
        self.rect = rectangle(0,0,0,0)
        self.e1 = [1,0]
        self.e2 = [0,1]
        self.ax = ax
        self.action_list = []
        self.fancy_list = []

    def action_remove(self):
        ax.clear()
        # ax.set_xlim([-2, 2])
        # ax.set_ylim([-2, 2])

        # for action in self.fancy_list:
        #     action.remove()

        self.action_list = []
        self.fancy_list = []

    def transform(self, tm):
        self.rect.right_top = np.transpose(np.dot(tm, np.transpose(self.const_rect.right_top)))
        self.rect.left_top = np.transpose(np.dot(tm, np.transpose(self.const_rect.left_top)))
        self.rect.right_bottom = np.transpose(np.dot(tm, np.transpose(self.const_rect.right_bottom)))
        self.rect.left_bottom = np.transpose(np.dot(tm, np.transpose(self.const_rect.left_bottom)))
        self.e1 = np.transpose(np.dot(tm, np.transpose([1,0])))
        self.e2 = np.transpose(np.dot(tm, np.transpose([0,1])))

    def draw_grid(self, num):
        up_line = np.linspace(self.rect.left_top, self.rect.right_top, num)
        bottom_line = np.linspace(self.rect.left_bottom, self.rect.right_bottom, num)

        left_line = np.linspace(self.rect.left_top, self.rect.left_bottom, num)
        right_line = np.linspace(self.rect.right_top, self.rect.right_bottom, num)

        for i in range(num):
            self.action_list.append(ax.plot([up_line[i, 1], bottom_line[i, 1]], [up_line[i, 0], bottom_line[i, 0]], 'k--', alpha=0.22))

        for i in range(num):
            self.action_list.append(ax.plot([left_line[i, 1], right_line[i, 1]], [left_line[i, 0], right_line[i, 0]], 'k--', alpha=0.22))

        self.fancy_list.append(ax.arrow(0, 0, self.e1[1], self.e1[0], edgecolor='red', fc='red', head_length=0.04, head_width=0.04))
        self.fancy_list.append(ax.arrow(0, 0, self.e2[1], self.e2[0], edgecolor='blue', fc='blue', head_length=0.04, head_width=0.04))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

rect = rectangle([-1, 1], [1, 1], [-1, -1], [1, -1])
g = graph(ax,1000,rect)

frame = 50
initial_matrix = [[1,0],[0,1]]
obj_matrix = [[2,1],[-5,0]]
current_matrix = np.linspace(initial_matrix, obj_matrix, frame)

def data_gen(t=0):
    while t<frame:
        g.transform(current_matrix[t])
        t = t+1
        yield t,

arr1 = [None]
def update(data):
    g.action_remove()
    g.draw_grid(10)

ani = animation.FuncAnimation(fig, update, data_gen, interval=10, blit=False, repeat=False)
# plt.annotate('',xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle="->"))
plt.show()