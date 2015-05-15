from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

class Plotter(object):
  things_to_plot  = []

  def __init__(self):
    return None

  @staticmethod
  def get_plot_buffer():
    return Plotter.things_to_plot

  @staticmethod
  def xy_tuple_to_lists(lst_of_tuples):
    x_list  = []
    y_list  = []
    max_y   = float('-inf')
    min_y   = float('inf')
    for y,x in lst_of_tuples:
      y = float(y)
      max_y = max_y if max_y > y else y
      min_y = min_y if min_y < y else y
      x_list.append(x)
      y_list.append(y)
    return x_list, y_list, max_y, min_y
  
  @staticmethod
  def globe_plotter(plot_data):
    """
    plot_data is a list of lists; elements in
    each list is a tuple of a date and a floating
    value;
    For now, imagine that the y-axis range of all
    the lists are 0-100; TODO : we will have to
    merge plots such as price and RSI in the
    same graph
    """
      
    y_limit_raw = []
  
    host  = host_subplot(211, axes_class=AA.Axes)
    # plt.subplots_adjust(right=0.55)
  
    host.set_xlabel('Date')             # strong assumption
    host.set_ylabel(plot_data[0][0])    # name of the first plot
  
    host_x_list, host_y_list, max_y, min_y = Plotter.xy_tuple_to_lists(plot_data[0][1])
    y_limit_raw.append(
        [
          plot_data[0][0][:plot_data[0][0].index('_')],
          max_y, min_y, host
        ]
      )
  
    p1, = host.plot(host_x_list, host_y_list, label=plot_data[0][0])
    host.axis['left'].label.set_color(p1.get_color())
  
    if len(plot_data) > 1:
      offset      = 60
      for i in xrange(len(plot_data)-1):
        par = host.twinx()
        new_fixed_axis    = par.get_grid_helper().new_fixed_axis
        par.axis['right'] = new_fixed_axis(loc='right',
                                            axes=par,
                                            offset=(offset*i,0))
        par.axis['right'].toggle(all=True)
        par.set_ylabel(plot_data[i+1][0])
  
        par_x_list, par_y_list, max_y, min_y  = Plotter.xy_tuple_to_lists(
            plot_data[i+1][1]
          )
        y_limit_raw.append(
            [
              plot_data[i+1][0][:plot_data[i+1][0].index('_')],
              max_y, min_y, par
            ]
          )
  
        p, = par.plot(par_x_list, par_y_list, label=plot_data[i+1][0])
        par.axis['right'].label.set_color(p.get_color())
  
    # find limits of the y axis
    for i in xrange(len(y_limit_raw)-1):
      for j in xrange(i+1, len(y_limit_raw)):
        if y_limit_raw[i][0] == y_limit_raw[j][0]:
          i_max = y_limit_raw[i][1]; j_max  = y_limit_raw[j][1]
          i_min = y_limit_raw[i][2]; j_min  = y_limit_raw[j][2]
          y_limit_raw[i][1] = y_limit_raw[j][1] = max(i_max, j_max)
          y_limit_raw[i][2] = y_limit_raw[j][2] = min(i_min, j_min)
  
    for x,max_y,min_y,par in y_limit_raw:
      par.set_ylim(min_y, max_y)
    
    host.legend()
    host.grid()
    plt.draw()
    plt.show()
  
    return None
