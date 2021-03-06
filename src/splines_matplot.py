# -*- coding: utf-8 -*-
"""
splines_matplot.py
"""

import random as std_rand

from pylab import *
import numpy as N



rotation_matrix = [lambda phi:cos(phi) , lambda phi:sin(phi),
                   lambda phi:-sin(phi), lambda phi:cos(phi)]

def rotate(v, angle):
    angle = angle * pi/180
    def _comp_rotation(v, matrix_line, angle):
        return sum([v[i] * matrix_line[i](angle) for i in range(2)])
    
    return (_comp_rotation(v, rotation_matrix[0:2], angle),
            _comp_rotation(v, rotation_matrix[2:4], angle))
    #return tuple([_comp_rotation(v, rotation_matrix[i*2:i*2+2], angle) for i in range(2)])



def cubic_spline_F(t, (A, B, C, D)):
	return A*t**3 + B*t**2 + C*t + D

def cubic_spline_derived(t, (A, B, C, D)):
	return 3*A*t**2 + 2*B*t + C

def spline_params_from_points(c0, c1, c2, c3):
	return (c3 - 3*c2 + 3*c1 - c0,
			     3*c2 - 6*c1 + 3*c0,
			 			3*c1 - 3*c0,
							   c0)



def bezier_f(t, c1, c2, c3, c4):
   return ( (1-t)**3           *  c1   + 
			(1-t)**2  *  t     *  c2   + 
			(1-t)     *  t**2  *  c3   + 
			             t**3  *  c4)
			
def bezier_F(t, a, b, c, d):
	x_t = bezier_f(t, a[0], b[0], c[0], d[0])
	y_t = bezier_f(t, a[1], b[1], c[1], d[1])
	return (x_t, y_t)



def unzip(l):
    return tuple(map(list(*zip(l))))


def add_vectors(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])


def sub_vectors(v1, v2):
	return (v1[0] - v2[0], v1[1] - v2[1])


def mul_vector(v, s):
	return (s*v[0], s*v[1])
    

def predict_points(p_old, v_old, p, v_p, a_p, t):
	"""
	"""
	p1 = add_vectors(p_old, v_old)
	p2 = add_vectors(add_vectors(p, mul_vector(v_p, t)), (.5*a_p[0]*t**2, .5*a_p[1]*t**2))
	p3 = sub_vectors(p2, add_vectors(v_p, mul_vector(a_p, t)))
	
	return [p_old, p1, p2, p3]


def derive(v1, v2, dt):
	return (float(v1[0]-v2[0]) / dt,
		float(v1[1]-v2[1]) / dt)


def make_spline(points, T):
    p1,p2,p3,p4 = points
    
    x_params = spline_params_from_points(*[x for (x, y) in (p1, p2, p3, p4)])
    y_params = spline_params_from_points(*[y for (x, y) in (p1, p2, p3, p4)])
		
    #splines = [(cubic_spline_F(float(t)/T, x_params),
    #            cubic_spline_F(float(t)/T, y_params)) for t in range(T) ]

    x_t = [cubic_spline_F(float(t)/T, x_params)for t in range(T)]
    y_t = [cubic_spline_F(float(t)/T, y_params)for t in range(T)]

    return (x_t, y_t)



def make_bezier_spline(points, T):
    a, b, c, d = points
    spline = [bezier_F(float(t)/T, a, b, c, d) for t in range(T)]
    x_t = [x for (x,y) in spline]
    y_t = [y for (x,y) in spline]
    return (x_t, y_t)
    

def plot_points(points):
    print points
    px = [x for (x,y) in points]
    py = [y for (x,y) in points]
    plot(px, py, "ro")
    plot(px, py)


def main():
    p_old, v_old = (0, 0), (0.5, 0.0)
    p, v_p, a_p = (2, 0), (0.5, 0), (0, 0)
    points = predict_points(p_old, v_old, p, v_p, a_p, 0.5)

    

    #plot_points(points)
    plot(*make_spline(points, 50))
    #plot(*make_bezier_spline(points, 200))
    
    
    
    p_old, v_old = points[3], derive(points[3], points[2], 1)
    
    #v_old = (-0.1, -0.3)
    print v_old
    
    
    p, v_p, a_p = (4, 0), (0.5, 0.0), (0, 0)
    points = predict_points(p_old, v_old, p, v_p, a_p, 0.5)
    #points[2] = (-0.6, -0.77)
    #points[3] = (0,0)

    #plot_points(points)
    plot(*make_spline(points, 100))
    #plot(*make_bezier_spline(points, 100))


def main2():
    std_rand.seed()
    p_old, v_old = (0,0), (1.0, 1.0)
    
    for i in range(5):
        p = add_vectors(p_old, (std_rand.randint(-1, 1), std_rand.randint(-1, 1)))
        
        v_p = (std_rand.random(), std_rand.random())
        #v_p = rotate(mul_vector(v_old, std_rand.uniform(-0.7,0.7)), std_rand.uniform(-15,15))
        
        
        a_p = (0,0)
        points = predict_points(p_old, v_old, p, (-v_p[0], -v_p[1]), a_p, 1.0)
        #plot_points(points)
        plot(*make_spline(points, 100))
        
        #for p in points:
        #    print "(%.1f, %.1f)" % p
        #print
        
        p_old, v_old = p, v_p
    

def main3():
    points = [(0,0)  , (2,0)   , (0,-2)  , (-2,0) , (0,2)  , (4,0)]
    speed  = [(0,1.5), (0,1.0), (1.0,0), (0,-1), (-2,0), (0,1)]
    
    updates = zip(points, speed)
    
    p_old, v_old = updates[0]
    
    for (i, update) in enumerate(updates[1:]):
        p, v_p = (update[0], mul_vector(update[1], 1))
        a_p = (0,0)
        points = predict_points(p_old, v_old, p, v_p, a_p, 1.0)
        plot_points(points)
        plot(*make_spline(points, 60))
        
        for i, p in enumerate(points):
            print "%d (%.1f, %.1f)" % (i, p[0], p[1])
            
        print
        
        
        p_old, v_old = points[3], derive(points[3], points[2], 1)
        #v_old = v_p
    




def unpack(line):
    pos = [float(elem.strip("()")) for elem in line.split(" ")[4:10:2]]
    speed = [float(elem.strip("()\n")) for elem in line.split(" ")[12:18:2]]
    return ((pos[0], pos[2]), (speed[0], speed[2]))

def unpack2(line):
    pos =  [float(elem.strip("()")) for elem in line.split(" ")[4:10:2]]
    speed = [float(elem.strip("()")) for elem in line.split(" ")[10:15:2]]
    dt = float(line.split(" ")[16].strip())
    return ((pos[0], pos[2]), (speed[0], speed[2]), dt)


def main4():
    lines = open("network_receiver.log").readlines()[:-1]
    
    p_old, v_old = unpack(lines[0])
    print p_old, v_old
    
    for l in lines[1:20]:
        p, v_p = unpack(l)
        print p, v_p
        v_p = v_p[0]*125, v_p[1]*125
        a_p = (0,0)
        points = predict_points(p_old, v_old, p, (-v_p[0], -v_p[1]), a_p, 1.0)
        #print points
        #plot_points(points)
        plot(*make_spline(points, 100))
        p_old, v_old = p, v_p
    
    
def main5():
    lines = open("network.log").readlines()[:-1]
    
    p_old, v_old, dt = unpack2(lines[0])
    print p_old, v_old, dt
    
    for l in lines:
        p, v_p, dt = unpack2(l)
        print v_p, dt
        v_p = v_p[0] * (dt*100000), v_p[1]* (dt*100000)
        
        a_p = (0,0)
        
        points = predict_points(p_old, v_old, p, (-v_p[0], -v_p[1]), a_p, 1.0)
        #print points
        #plot_points(points)
        plot(*make_spline(points, 100))
        p_old, v_old = p, v_p
    
    

if __name__=="__main__":
    main5()
