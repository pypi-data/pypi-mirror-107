from dscal.calculus import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class graph(calculus):
    def __init__(self,*expression:list):
        '''Access graphs for tkinter GUI applications directly , power of dscal.calculus'''
        super().__init__(*expression)
        
    def get_graph2D(self,master,limit=[-10,10]):    
        '''Get FigureCanvasTkAgg figure with 2D projection.'''
        self.figure2=plt.figure()
        x=np.arange(limit[0],limit[1],0.01)
        y=np.arange(limit[0],limit[1],0.01)
        plt.plot(x,x*0,label='x-axis')
        try:
            for i in range(len(self.expressions)):
                f=ne.evaluate(self.expressions[i])
                plt.plot(x,f,label=self.expressions_[i])
        except ValueError:
            for i in range(len(self.expressions)):
                f=ne.evaluate(self.expressions[i])
                plt.plot(x,f,label=self.expressions_[i])
        plt.legend()
        return FigureCanvasTkAgg(self.figure2,master).get_tk_widget()


    def get_graph3D(self,master,limit=[-10,10],colormap=plt.cm.cool):
        '''Get FigureCanvasTkAgg figure with 3D projection.'''
        x,y=np.meshgrid(np.linspace(limit[0],limit[1],1000),np.linspace(limit[0],limit[1],1000))
        self.figure3=plt.figure()
        a=self.figure3.add_subplot(111,projection='3d')
        for exp in self.expressions:
            a.plot_surface(x,y,ne.evaluate(exp),cmap=colormap)
        return FigureCanvasTkAgg(self.figure3,master).get_tk_widget()

    def __add__(self, *others):
        '''Adds graph instances assigning to a new object.'''
        expressions_sum=self.expressions_
        for ex in others:
            expressions_sum+=ex.expressions_
        return graph(*expressions_sum)

    def __str__(self):
        return super().__str__()
    