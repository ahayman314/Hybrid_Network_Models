import json 
from abc import abstractmethod
import os
import matplotlib as mpl
mpl.use('TkAgg')
mpl.interactive(True)
import matplotlib.pyplot as plt
 
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.5

class AbstractPlotter(): 
    def __init__(self, name, x, y, x_label, y_label): 
        self.name = name
        self.x = x 
        self.y = y
        # Common settings
        self.options = {}
        self.set_option('x_label', x_label)
        self.set_option('y_label', y_label) 
        self.set_option('figure_size_x', 6)
        self.set_option('figure_size_y', 6)
        self.set_option('marker', 'o')
        self.set_option('linestyle', 'solid')
        self.set_option('markersize', 2)
        self.set_option('linewidth', 1.0)

    def plot(self):
        self.setup_plot()
        plt.show()

    @abstractmethod
    def setup_plot(self): 
        pass

    def set_option(self, key, value):
        self.options[key] = value
    
    def get_options(self): 
        return self.options

    def close(self): 
        plt.close('all') 

    def apply_saved_settings(self, path): 
        try: 
            with open(path, 'r') as f:
                data = json.load(f)
            if data['name'] != self.name: 
                raise Exception("Attempting to apply settings from " + data['name'] + " to " + self.name)
            data.pop('name', None)
            for key, val in data.items():
                self.options[key] = val
        except: 
            print("You tried to apply settings from " + data['name'] + " to " + self.name + ". Please ensure the plot types match.")

    def save(self, savename): 
        self.setup_plot()
        os.mkdir(savename)
        filename = savename + '/' + savename
        plt.savefig(filename + '.pdf', format='pdf', dpi=1200, bbox_inches='tight')
        with open(filename + '.json', 'w') as f:
            self.options['name'] = self.name
            json.dump(self.options, f, indent=4)
            self.options.pop('name', None)

class BasicPlot(AbstractPlotter): 
    def __init__(self, x, y, x_label, y_label):
        super().__init__('Basic Plot', x, y, x_label, y_label)

    def setup_plot(self): 
        plt.figure(figsize = (float(self.options['figure_size_x']), float(self.options['figure_size_y'])))
        plt.subplot(111)
        plt.grid(True, linestyle=':')
        plt.xlabel(self.options['x_label'])
        plt.ylabel(self.options['y_label'])
        plt.plot(self.x, 
                self.y, 
                marker = self.options['marker'], 
                linestyle = self.options['linestyle'],
                markersize = float(self.options['markersize']),
                linewidth = float(self.options['linewidth'])
                )
        plt.tight_layout()
        
class MultiPlot(AbstractPlotter): 
    def __init__(self, x, y, x_label, y_label, legend, legend_position_x = 0.2, legend_position_y = 1.0):
        super().__init__('Multi Plot', x, y, x_label, y_label)
        self.legend = legend
        self.set_option('legend_position_x', legend_position_x)
        self.set_option('legend_position_y', legend_position_y)

    def setup_plot(self): 
        plt.figure(figsize = (float(self.options['figure_size_x']), float(self.options['figure_size_y'])))
        plt.subplot(111)
        plt.grid(True, linestyle=':')
        plt.xlabel(self.options['x_label'])
        plt.ylabel(self.options['y_label'])
        for i in range(len(self.x)): 
            plt.plot(self.x[i], 
                    self.y[i], 
                    marker = self.options['marker'], 
                    linestyle = self.options['linestyle'],
                    markersize = float(self.options['markersize']),
                    linewidth = float(self.options['linewidth'])
                    )
        plt.legend( labels = self.legend, 
                    ncol=2, 
                    loc="lower left", 
                    bbox_to_anchor=(float(self.options['legend_position_x']), float(self.options['legend_position_y'])), 
                    borderaxespad=0.
                    )
        plt.tight_layout()