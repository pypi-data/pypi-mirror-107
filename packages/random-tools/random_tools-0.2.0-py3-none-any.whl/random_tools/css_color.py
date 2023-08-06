from matplotlib import colors as mcolors
import copy, random

class CSS4_ColorPicker():
    """
    Class helping to get random colors from the available CSS4 palette without replacement.
    The set of available color resets when all colors have been sampled.
    You can also reset manually the available colors
    """
    
    def reset(self):
        self.__available_colors = self.CSS4_COLORS
        random.shuffle(self.__available_colors)
        
    def __init__(self):
        self.CSS4_COLORS = list(mcolors.CSS4_COLORS.keys())
        self.reset()
        
    def sample_color(self):
        if len(self.__available_colors) == 0:
            self.reset()
        return self.__available_colors.pop(0)
    
    
    @property
    def CSS4_COLORS(self):
        return copy.copy(self.__CSS4_COLORS)

    @CSS4_COLORS.setter
    def CSS4_COLORS(self, x):
        self.__CSS4_COLORS = x
        