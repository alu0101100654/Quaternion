from math import *
import numpy as np
import quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def ramal(I,prev=[],base=0):
    # Convierte el robot a una secuencia de puntos para representar
    O = []
    if I:
        if isinstance(I[0][0],list):
            for j in range(len(I[0])):
                O.extend(ramal(I[0][j], prev, base or j < len(I[0])-1))
        else:
            O = [I[0]]
            O.extend(ramal(I[1:],I[0],base))
            if base:
                O.append(prev)
    return O

def muestra_robot(O,ef=[]):
    # Pinta en 3D
    OR = ramal(O)
    OT = np.array(OR).T
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Bounding box cúbico para simular el ratio de aspecto correcto
    max_range = np.array([OT[0].max()-OT[0].min()
                        ,OT[1].max()-OT[1].min()
                        ,OT[2].max()-OT[2].min()
                        ]).max()
    Xb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten()
        + 0.5*(OT[0].max()+OT[0].min()))
    Yb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten()
        + 0.5*(OT[1].max()+OT[1].min()))
    Zb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten()
        + 0.5*(OT[2].max()+OT[2].min()))
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')
    ax.plot3D(OT[0],OT[1],OT[2],marker='s')
    ax.plot3D([0],[0],[0],marker='o',color='k',ms=10)
    if not ef:
        ef = OR[-1]
    ax.plot3D([ef[0]],[ef[1]],[ef[2]],marker='s',color='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    return

def cuaternion_rotacion(n,theta):
    # n es un vector
    # theta es un angulo
    w = cos(theta/2)
    x = n[0]*sin(theta/2)
    y = n[1]*sin(theta/2)
    z = n[2]*sin(theta/2)
    return(np.quaternion(w,x,y,z))
# cuaterniones de desplazamiento
r1=np.quaternion(0,5,2,5)
r2=np.quaternion(0,7,5,5)

# vectores de rotaci�n
n1=[1,0,0]
n2=[1,0,0]

# introducci�n de las variables articulares
print('')
t1=float(input('valor de theta1 en grados  '))
t1=t1*pi/180
t2=float(input('valor de theta2 en grados  '))
t2=t2*pi/180

# calculo de los cuaterniones de rotaci�n
q1=cuaternion_rotacion(n1,t1)
q1c=np.conjugate(q1)

q2=cuaternion_rotacion(n2,t2)
q2c=np.conjugate(q2)


# calculo del punto o1
i1=q1 * r1
o1=i1 * q1c


# calculo del punto o2
i2=q1 * q2
i2=i2 * r2
i2=i2 * q2c
i2=i2 * q1c
o2=o1 + i2


# impresi�n de los resultados
print('')
print('punto uno del robot')
print(o1)
print('')
print('punto dos del robot')
print(o2)

muestra_robot([[0,0,0,0], quaternion.as_float_array(o1), quaternion.as_float_array(o2)])
input()