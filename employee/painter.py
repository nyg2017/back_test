import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from copy import deepcopy
class Painter(object):
    def __init__(self,bookkeeper):
        self.bookkeeper = bookkeeper

    def returnVis(self):
        date_list = []
        capital_list = []
        index_value_list = []
        for index in range(self.bookkeeper.index):
            date_dic = self.bookkeeper.account[index]
            date_list.append(date_dic['date_time'])
            capital_list.append(date_dic['capital'])
            index_value_list.append(date_dic['index_state']['index_value'])

        date_array = np.array(date_list)
        capital_array = np.array(capital_list)
        index_value_array = np.array(index_value_list)
        if index_value_array[0] == -1:
            index_value_array[0] = index_value_array[1]
            
        return_array = capital_array / capital_array[0] - 1.0
        #print (index_value_array,index_value_array[0])
        index_return_array = (index_value_array / index_value_array[0]) - 1.0

        
        capital_array_temp = deepcopy(capital_array)
        capital_array_temp[1:] = capital_array[:capital_array.shape[0]-1]
        index_value_array_temp = deepcopy(index_value_array)
        index_value_array_temp[1:] = index_value_array_temp[:index_value_array.shape[0]-1]
        
        return_per_day = capital_array/capital_array_temp - 1.0
        index_return_per_day = index_value_array/index_value_array_temp -1.0
        

        fig=plt.figure()
        ax1=fig.add_subplot(2,1,1)
        ax2=fig.add_subplot(2,1,2)
        
        font1 = FontProperties() 
        s = str(date_list[0]) + str(date_list[-1])
        #ax1.set_title(s,fontproperties=font1)
        x_array = np.arange(0,return_array.shape[0],1)
        ax1.set_title(u"return vis " + s,fontproperties=font1)
        ax1.set_xlabel(u"date",fontproperties=font1)
        ax1.set_ylabel(u"return",fontproperties=font1) 
        ax1.plot(x_array,return_array,'-',label ="return")
        ax1.plot(x_array,index_return_array,'-',label ="index_return")
        ax1.legend()

        ax2.set_title(u"return per day vis",fontproperties=font1)
        ax2.set_xlabel(u"date",fontproperties=font1)
        ax2.set_ylabel(u"return per day",fontproperties=font1) 
        ax2.plot(x_array,return_per_day,'-',label ="return per day")
        ax2.plot(x_array,index_return_per_day,'-',label ="index_return per day")
        ax2.legend()


        plt.show()


        