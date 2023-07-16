import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from matplotlib.backend_bases import MouseButton
from matplotlib.lines import Line2D
from matplotlib.artist import Artist

class Graph:
    def __init__(self, ax, poly, name, method_interpolate):

        self.ax = ax
        canvas = poly.figure.canvas
        self.poly = poly

        x, y = zip(*self.poly.xy)
        self.line = Line2D(x, y,
                           marker='o', markerfacecolor='r',
                           animated=True)
        self.ax.add_line(self.line)

        # self.cid = self.poly.add_callback(self.poly_changed)
        # self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.on_draw)
        # canvas.mpl_connect('button_press_event', self.on_button_press)
        # canvas.mpl_connect('key_press_event', self.on_key_press)
        # canvas.mpl_connect('button_release_event', self.on_button_release)
        # canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas = canvas

        self.name = name
        self.method_interpolate = method_interpolate
        self.point_values = []
        self.point_interpolate = []

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.poly)
        self.ax.draw_artist(self.line)


