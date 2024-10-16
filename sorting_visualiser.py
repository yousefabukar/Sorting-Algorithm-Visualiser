import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import RadioButtons
from algorithms import (bubble_sort, merge_sort, quick_sort, heap_sort, insertion_sort, selection_sort)
from utils import generate_data
from complexity import ALGO_COMPLEXITY

class SortingVisualizer:
    def __init__(self, algorithms):
        self.algorithms = algorithms
        self.algorithm_keys = list(self.algorithms.keys())
        self.n = 50
        self.data = generate_data(self.n)
        
        self.fig, (self.ax, self.info_ax) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
        self.fig.subplots_adjust(left=0.3, bottom=0.1, top=0.9, hspace=0.3)
        
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Sorting Algorithm Visualization")
        
        self.bar_rects = self.ax.bar(range(len(self.data)), self.data, align="edge")
        self.text = self.ax.text(0.02, 0.90, "", transform=self.ax.transAxes)
        self.iteration = [0]
        
        self.current_algorithm_index = 0
        self.current_algorithm = self.algorithm_keys[self.current_algorithm_index]
        self.sorting_generator = None
        self.is_sorting = False
        
        self.setup_radio_buttons()
        self.update_complexity_info()

        self.sorting_generator = None
        self.is_sorting = False
        self.algorithm_index = 0

    def setup_radio_buttons(self):
        radio_ax = self.fig.add_axes([0.05, 0.4, 0.2, 0.15])
        self.radio_buttons = RadioButtons(radio_ax, self.algorithm_keys)
        self.radio_buttons.on_clicked(self.algorithm_changed)

    def algorithm_changed(self, label):
        self.current_algorithm = label
        self.current_algorithm_index = self.algorithm_keys.index(label)
        self.update_complexity_info()
        self.reset()

    def update_complexity_info(self):
        self.info_ax.clear()
        self.info_ax.axis('off')
        complexity = ALGO_COMPLEXITY[self.current_algorithm]
        info_text = f"{self.current_algorithm} Complexity:\n"
        info_text += f"Time (Best): {complexity['time_best']}\n"
        info_text += f"Time (Average): {complexity['time_average']}\n"
        info_text += f"Time (Worst): {complexity['time_worst']}\n"
        info_text += f"Space: {complexity['space']}\n"
        info_text += f"Stability: {complexity['stability']}"
        self.info_ax.text(0.05, 0.5, info_text, va='center', fontsize=10)

    def update(self, frame):
        if not self.is_sorting:
            self.start_next_sort()
            return self.bar_rects

        try:
            arr = next(self.sorting_generator)
            for rect, val in zip(self.bar_rects, arr):
                rect.set_height(val)
            self.iteration[0] += 1
            self.text.set_text(f"{self.current_algorithm}\nIterations: {self.iteration[0]}")
        except StopIteration:
            self.is_sorting = False
            self.algorithm_index = (self.algorithm_index + 1) % len(self.algorithms)
            self.fig.canvas.draw_idle()

        return self.bar_rects

    def start_next_sort(self):
        self.current_algorithm = list(self.algorithms.keys())[self.algorithm_index]
        self.radio_buttons.set_active(self.algorithm_index)
        self.update_complexity_info()
        for rect, val in zip(self.bar_rects, self.data):
            rect.set_height(val)
        self.iteration[0] = 0
        self.text.set_text(f"{self.current_algorithm}\nIterations: 0")
        self.sorting_generator = self.algorithms[self.current_algorithm](self.data.copy())
        self.is_sorting = True

    def animate(self):
        self.anim = FuncAnimation(
            self.fig,
            func=self.update,
            frames=None,
            interval=50,
            repeat=True,
            blit=True
        )

    def algorithm_changed(self, label):
        self.algorithm_index = list(self.algorithms.keys()).index(label)
        self.is_sorting = False

    def reset(self):
        self.is_sorting = False
        self.start_next_sort()

    def show(self):
        self.reset()
        self.animate()
        plt.show()

algorithms = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort
}

visualizer = SortingVisualizer(algorithms)
visualizer.show()

        
