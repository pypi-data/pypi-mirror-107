import numpy as np
import matplotlib.pyplot as plt

from numerical_analysis.dependencies import GeometricalPlace
from numerical_analysis.splines import Bezier


class CompositeBezier(GeometricalPlace):

    def __init__(self, control_points: np.array, order, datatype=np.float):
        super().__init__()
        self.datatype = datatype
        self.cp = control_points
        self.order = order
        self.sectors = [Bezier(np.array([self.cp[order*i + j] for j in range(order + 1)]))
                        for i in range((len(self.cp) - 1)//order)]

    def global_to_local_index(self, index):
        point_ind = [index % self.order]
        sector_ind = [index // self.order]
        if point_ind[0] == 0:
            if sector_ind[0] == len(self.sectors):
                point_ind[0] = self.order
                sector_ind[0] -= 1
            elif sector_ind[0] > 0:
                point_ind.append(self.order)
                sector_ind.append(sector_ind[0] - 1)
        return sector_ind, point_ind

    def local_to_global_index(self, sector_index, point_index):
        return sector_index * self.order + point_index

    def translate_t(self, t):
        if t != 1.:
            i = int(t * len(self.sectors))
            u = t * len(self.sectors) - i
        else:
            i = len(self.sectors) - 1
            u = 1.
        return i, u

    def y_x(self, x):
        def detect_sector():
            i = 0
            while True:
                if self.sectors[i].x_t(1.) >= x:
                    return i
                i += 1
        return self.sectors[detect_sector()].y_x(x)

    def x_t(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].x_t(u)

    def y_t(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].y_t(u)

    def dx_dt(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].dx_dt(u)

    def dy_dt(self, t):
        i, u = self.translate_t(t)
        return self.sectors[i].dy_dt(u)

    def graph_cp(self):
        return [[self.cp[j, i] for j in range(len(self.cp))] for i in range(len(self.cp[0]))]

    def plot(self, dt, show_polyline=True, plot=True, export=False, filename="curve.png", title=None):
        plt.clf()
        if title:
            plt.title(title)
        graph = self.graph(dt)
        # noinspection PyUnresolvedReferences
        if show_polyline:
            plt.plot(graph[0], graph[1], "blue", self.graph_cp()[0], self.graph_cp()[1], "orange")
        else:
            plt.plot(graph[0], graph[1])

        if plot:
            plt.show()

        if export:
            plt.savefig(filename)

    def modify_control_point(self, i, new_control_point):
        x_diff = new_control_point[0] - self.cp[i][0]
        y_diff = new_control_point[1] - self.cp[i][1]
        diff = [x_diff, y_diff]
        self.cp[i][0] += x_diff
        self.cp[i][1] += y_diff
        sector_ind, point_ind = self.global_to_local_index(i)
        for j in range(len(sector_ind)):
            self.sectors[sector_ind[j]].modify_control_point(point_ind[j], self.cp[i])


class CompositeQuadraticBezier(CompositeBezier):

    def __init__(self, control_points: np.array, datatype=np.float):
        super().__init__(control_points, 2)
        self.datatype = datatype
        self.cp = control_points
        self.fake_cp = control_points
        self.calculate_fake_cp()
        self.sectors = [Bezier(np.array([self.fake_cp[2 * i + j] for j in range(3)]))
                        for i in range((len(self.fake_cp) - 1) // 2)]

    def global_to_local_index(self, index):
        if index == 0:
            sector_ind = 0
            point_ind = 0
        elif index == len(self.cp) - 1:
            sector_ind = len(self.sectors) - 1
            point_ind = 2
        else:
            sector_ind = index - 1
            point_ind = 1
        return sector_ind, point_ind

    def local_to_global_index(self, sector_index, point_index):
        return sector_index * self.order + point_index

    def calculate_fake_cp(self):
        i = 1
        for j in range(len(self.cp) - 3):
            self.fake_cp = np.insert(self.fake_cp, i + 1, self.mid_cp(self.fake_cp[i], self.fake_cp[i + 1]), 0)
            i += 2

    def modify_control_point(self, i, new_control_point):
        self.cp[i][0] = new_control_point[0]
        self.cp[i][1] = new_control_point[1]
        sector_ind, point_ind = self.global_to_local_index(i)
        self.sectors[sector_ind].modify_control_point(point_ind, self.cp[i])
        if point_ind == 1:
            if sector_ind != 0:
                mid = self.mid_cp(self.cp[i], self.cp[i-1])
                self.sectors[sector_ind].modify_control_point(0, mid)
                self.sectors[sector_ind - 1].modify_control_point(2, self.mid_cp(self.cp[i], self.cp[i-1]))
            if sector_ind != len(self.sectors) - 1:
                mid = self.mid_cp(self.cp[i], self.cp[i+1])
                self.sectors[sector_ind].modify_control_point(2, mid)
                self.sectors[sector_ind + 1].modify_control_point(0, mid)

    @staticmethod
    def mid_cp(cp0, cp1):
        return np.array([0.5 * (cp0[0] + cp1[0]), 0.5 * (cp0[1] + cp1[1])])



class CompositeCubicBezier(CompositeBezier):

    def __init__(self, control_points: np.array, datatype=np.float):
        super().__init__(control_points, 3, datatype)
