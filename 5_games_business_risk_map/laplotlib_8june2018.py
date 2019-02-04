def draw_vectors_2d(vectors=[[0,0],[0,0],[0,0]], SIZE_X=[-4,5], AXIS_LENGTH=1):
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.arange(SIZE_X[0], SIZE_X[1]).tolist()
    y = np.arange(SIZE_X[0], SIZE_X[1]).tolist()
    for v in vectors:
        x = [0,v[0]]
        y = [0,v[1]]
        plt.plot(x, y)
        plt.scatter(x, y)
    #axis
    plt.plot([0,0], [0,AXIS_LENGTH])
    plt.plot([0,AXIS_LENGTH], [0,0])
    plt.grid()
    plt.show()
#draw_vectors_2d([[3,2],[0,0],[3.14,2.71]])

def draw_axis_3d(plane_size=10, plane_size_minus=-2, points_scale=0.3):
    import numpy as np
    from mayavi import mlab
    s = plane_size
    s_m = plane_size_minus
    mlab.mesh([[s_m, s_m],[s,   s]], [[s_m, s],  [s_m, s]], [[0,   0],  [0,   0]], color=(1,1,1), opacity=0.5) # xy
    mlab.mesh([[s_m, s_m],[s,   s]], [[0,   0],  [0,   0]], [[s_m, s],  [s_m, s]], color=(1,1,1), opacity=0.5) # xz
    mlab.mesh([[0,   0],  [0,   0]], [[s_m, s_m],[s,   s]], [[s_m, s],  [s_m, s]], color=(1,1,1), opacity=0.5) # yz
    mlab.view(azimuth=45, elevation=60, distance=(s*5), focalpoint=(0,0,0))
    for i in np.linspace(-s, s, 2*s+1): # for i in range(-s,s+1):
        if i%5==0: sf=points_scale
        else: sf=points_scale/2
        mlab.points3d(i,0,0, scale_factor=sf,color =(1,0,0)) #red   point on ox
        mlab.points3d(0,i,0, scale_factor=sf,color =(0,1,0)) #green point on oy            
        mlab.points3d(0,0,i, scale_factor=sf,color =(0,0,1)) #blue  point on oz

def draw_lines_3d(origin=(0,0,0), target=[[1,1,1], [-1,-1,-1], [1,-1,-1]], size=0.2, density=20, clr =[(0.,0.,0.), (0.,0.,0.), (0.,0.,0.)]):
    from mayavi import mlab
    import numpy as np
    draw_axis_3d()  
    for v in target:
        for i in np.linspace(0, 1, density): # np.linspace(0, 1,10)=>[ 0.,0.11,0.22,0.33,0.44,0.55,0.66,0.77,0.88,1.]
            x = origin[0]*(1-i) + v[0]*i
            y = origin[1]*(1-i) + v[1]*i
            z = origin[2]*(1-i) + v[2]*i
            sf = size*2 if i==1 else size
            mlab.points3d(x,y,z,scale_factor=sf, color=clr[target.index(v)]) #radius
    mlab.show() 
#draw_lines_3d(target=[[5,5,5], [1,2,3], [-1,-2,6]], clr=[(1,0,0), (0,1,0), (0,0,1)], size=0.4)

def draw_planes_3d(v4=[[1,1,1,1], [-1,-1,-1,-1], [1,-1,-1,1]], scale=50, clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)]):
    # style: 1*x + 2*y + 3*z = 4; 3 weighted unknowns = number
    draw_axis_3d()  
    from mayavi import mlab
    def groupBy2(vector): 
        return [vector[i:i+2] for i in range(0, len(vector), 2)]#[1,2,3,4] => [[1,2], [3,4]]
    for v in v4:
        x,y,z = ([] for i in range(3)) #x1 - list (len=4), x-coords of each point of plane1
        for i in [-scale,scale]: #algorithm: y=2x -> x = i; y=2*i; z=0 (wrong, z=unused iterator=j)
            for j in [-scale,scale]:
                if v[0]!=0: #vs division on zero
                    x.append( (-v[1]*i - v[2]*j + v[3]) / v[0] ) #plane1
                    y.append(i)
                    z.append(j)
                elif v[1]!=0:#vs division on zero
                    x.append(i)
                    y.append( (-v[0]*i - v[2]*j + v[3]) / v[1] ) #plane1
                    z.append(j)
                elif v[2]!=0:#vs division on zero
                    x.append(i)
                    y.append(j)
                    z.append( (-v[0]*i - v[1]*j + v[3]) / v[2] ) #plane1
        mlab.mesh(groupBy2(x), groupBy2(y), groupBy2(z), color=clr[v4.index(v)])
    mlab.show()  
# import laplotlib as lpl
# lpl.draw_planes_3d(v4=[[10,0,0,0],[0,10,0,0],[0,0,10,0]], scale=5, clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)])

def draw_lines_2d(v3=[[1,1,1], [1,-1,1]], grid_size=[-4,5], axis_length=1):
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.arange(grid_size[0], grid_size[1]).tolist() #grid wide
    y = np.arange(grid_size[0], grid_size[1]).tolist() #grid height
    for v in v3:
        if v[0]==0:                       #when 0*x + 1*y = 2; vs division on zero
            for i in y:
                y[i] = v[2]/v[1] #y = 2/1
        elif v[1]==0:                     #when 1*x + 0*y = 2
            for i in x:
                x[i] = v[2]/v[0] #y = 2/1
        else:                             #when 1*x + 2*y = 3
            for i in x:
                y[i] = (v[2]-v[0]*x[i])/v[1] #y = (3-1x)/2
        plt.plot(x, y)
        plt.scatter(x, y)
    # axis:
    plt.plot([0,0], [0,axis_length])
    plt.plot([0,axis_length], [0,0])
    plt.grid()
    plt.show()
# import numpy as np
# A = np.matrix([
#     [20,30,3], #20x + 30y = 3
#     [30,20,2], #30x + 20y = 2
#     [60,10,6], #60x + 10y = 6
# ])
# draw_lines_2d(v3=A.tolist(),grid_size=[-4,5], axis_length=10)

def draw_points_2d(v2=[[0,0],[0,0],[0,0]], size =[300,200,500], clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)], annotation =['name1','name2','name3'], an_clr=(0,0,1), an_antiheight=3, grid_size=[-4,5], axis_length=[5,1], origin=[0,0], title="plot 01", ylabel="oy", xlabel="ox"):
    import numpy as np
    import matplotlib.pyplot as plt
    x = np.arange(grid_size[0], grid_size[1]).tolist() #grid wide
    y = np.arange(grid_size[0], grid_size[1]).tolist() #grid height
    for v in v2:
        plt.scatter([v[0]], [v[1]], s=size[v2.index(v)], c=clr[v2.index(v)]) # plt.scatter([0.1,0.5], [0.4,0.8], s=[300, 5])
        #plt.annotate(annotation[v2.index(v)], (v[0],v[1]), color=an_clr)
        plt.annotate(annotation[v2.index(v)], (v[0],v[1]), color=an_clr, xytext=(v[0]+v[0]/an_antiheight,v[1]+v[0]/an_antiheight), #textcoords='offset points', 
            ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5), arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0') )
    # axis:
    plt.plot([origin[0],origin[0]], [origin[1],origin[1]+axis_length[1]]) #oy
    plt.plot([origin[0],axis_length[0]], [origin[1],origin[1]]) #ox
    plt.grid()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()
    #plt.savefig('books_read.png')
    
#draw_points_2d(v2=[[1,2017],[2,2017],[3,2018]], size =[300,200,500], clr =[(1.,0.,0.), (0.,1.,0.), (0.,0.,1.)], annotation =['name1','name2','name3'], an_clr=(0,0,1), an_antiheight=5, grid_size=[-4,5], axis_length=[5,1], origin=[0,2016])


def add_points_2d(points = [(1,3),(5,1),(2.5,0.5)], anns = ['b', 'a', 'p'], bias = (0,0.2), size=200, clr=(1,0,0)):
    import matplotlib.pyplot as plt
    #plt.plot([1,2.5], [3,0.5])
    for p in points: 
        plt.scatter(p[0], p[1], s=[size], c=clr)
        plt.annotate(anns[points.index(p)], (p[0]+bias[0], p[1]+bias[1]))

def add_line_2d(p = [(1,3),(2.5,0.5)]):
    import matplotlib.pyplot as plt
    plt.plot([p[0][0],p[1][0]], [p[0][1],p[1][1]])
    
# lpl.add_line_2d(p = [(1,3),(2.5,0.5)])
# lpl.add_points_2d(points = [(1,3),(5,1),(2.5,0.5)], anns = ['b', 'a', 'p'])    
# import matplotlib.pyplot as plt
# plt.title('title')
# plt.ylabel('outlier')
# plt.xlabel('xlabel')
# lpl.draw_vectors_2d([[1,3],[5,1]])


def draw_vectors_plt_3d (vectors = [(5,5,0),(8,0,8)], axis_length = 11, grid_size=10):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    soa = np.array([
        [0, 0, 0, axis_length, 0, 0], #ox
        [0, 0, 0, 0, axis_length, 0], #oy
        [0, 0, 0, 0, 0, axis_length], #oz
        #[0, 0, 0, 8, 8, 0], #vector n
    ])
    X, Y, Z, U, V, W = zip(*soa) #each var=column, type=tuple
    for v in vectors:
        X = list(X)
        X.append(0)
        Y = list(Y)
        Y.append(0)
        Z = list(Z)
        Z.append(0)
        U = list(U)
        U.append(v[0])
        V = list(V)
        V.append(v[1])
        W = list(W)
        W.append(v[2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(X, Y, Z, U, V, W)
    ax.set_xlim([0,grid_size])
    ax.set_ylim([grid_size,0])
    ax.set_zlim([0,grid_size])
    plt.show()

# b = (8,0,8)
# p = (6,0,0)
# lpl.draw_vectors_plt_3d(vectors = [b,p], axis_length = 11, grid_size=10)    
