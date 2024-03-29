# Saagar Deshpande
# CS 205
# Homework 0 P3.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def predictS(A, s_k, a):
        return (A*s_k + a)

def predictSig(A, sigma_k, B):
        return (A*sigma_k*A.T + B*B.T).I

def updateSig(sigma_approx,C):
        return (sigma_approx + C.T * C).I

def updateS(sigma_k1,sigma_approx,s_approx, C, m_k1):
        return (sigma_k1 * (sigma_approx * s_approx + C.T * m_k1))

if __name__ == '__main__':
	# Model parameters
	K = 121    # Number of times steps
	dt = 0.01  # Delta t
	c = 0.1    # Coefficient of drag
	g = -9.81  # Gravity
	# For constructing matrix B
	bx = 0
	by = 0
	bz = 0
	bvx = 0.25
	bvy = 0.25
	bvz = 0.1
	# For constructing matrix C
	rx = 1.0
	ry = 5.0
	rz = 5.0

	# Create 3D axes for plotting
	ax = Axes3D(plt.figure())


	# Part 1:
	# Load true trajectory and plot it
	# Normally, this data wouldn't be available in the real world

	#ax.plot(x-coords, y-coords, z-coords,
	#				'--b', label='True trajectory')

	# load data from P3_trajectory.txt and plot
	s_true = np.loadtxt('P3_trajectory.txt',delimiter=',',unpack=True)
	ax.plot(s_true[0],s_true[1],s_true[2],'--b',label='True trajectory')

	# Part 2:
	# Read the observation array and plot it (Part 2)

	#ax.plot(x-coords, y-coords, z-coords,
	#				'.g', label='Observed trajectory')
	
	# load data from P3_measurements.txt and plot
	s_tracker = np.loadtxt('P3_measurements.txt',delimiter=',',unpack=True)
	ax.plot((s_tracker[0] * (1/rx)),(s_tracker[1] * (1/ry)), (s_tracker[2] * (1/rz)),'.g', label='Observed trajectory')

	# Part 3:
	# Use the initial conditions and propagation matrix for prediction
	# A = ?
	# a = ?
	# s = ?

	# Initial conditions for s0
	s0 = np.matrix([0,0,2,15,3.5,4.0]).transpose()
	a = np.matrix([0,0,0,0,0,g*dt]).transpose()

	A = np.asmatrix(np.zeros([6,6]))
	A[0,0] = 1
	A[1,1] = 1
	A[2,2] = 1
	A[0,3] = dt
	A[1,4] = dt
	A[2,5] = dt
	A[3,3] = 1 - c*dt
	A[4,4] = 1 - c*dt
	A[5,5] = 1 - c*dt

	predicted_pos_matrix = np.asmatrix(np.zeros([6,K]))
	predicted_pos_matrix[:,0] = s0
	
	# Compute the rest of sk using Eq (1)
	i = 0
	while i < (K-1):
		predicted_pos_matrix[:,(i+1)] = (A*predicted_pos_matrix[:,i])+a
		i = i+1

	predicted_pos_array = np.asarray(predicted_pos_matrix)
	
	#ax.plot(x-coords, y-coords, z-coords,
	#				'-k', label='Blind trajectory')

	ax.plot(predicted_pos_array[0],predicted_pos_array[1],predicted_pos_array[2],'-k',label='Blind trajectory')
	
	# Part 4:
	# Use the Kalman filter for prediction
	# B = ?
	# C = ?
	B = np.asmatrix(np.zeros([6,6]))
	B[0,0] = bx
	B[1,1] = by
	B[2,2] = bz
	B[3,3] = bvx
	B[4,4] = bvy
	B[5,5] = bvz

	C = np.asmatrix(np.zeros([3,6]))
	C[0,0] = rx
	C[1,1] = ry
	C[2,2] = rz

	# Initial conditions for s0 and Sigma0
	Sigma0 = 0.01 * np.identity(6)
	Sigma_k = Sigma0
	s_k = s0
	#measurements matrix
	m_full = np.asmatrix(s_tracker)

	# Compute the rest of sk using Eqs (2), (3), (4), and (5)
	kalmanmatrix = np.asmatrix(np.zeros([6,K]))
	kalmanmatrix[:,0] = s0

	i = 0
	while i < K-1:
		s_approx = predictS(A,kalmanmatrix[:,i],a)
		Sigma_approx = predictSig(A,Sigma_k,B)
		Sigma_k = updateSig(Sigma_approx,C)
		kalmanmatrix[:,(i+1)] = updateS(Sigma_k, Sigma_approx,s_approx,C,m_full[:,(i+1)])
		i = i+1
	#ax.plot(x-coords, y-coords, z-coords,
	#				'-r', label='Filtered trajectory')

	kalmanarray = np.asarray(kalmanmatrix)
	ax.plot(kalmanarray[0,:],kalmanarray[1,:],kalmanarray[2,:],'-r',label='Filtered trajectory')

	# Show the plot
	ax.legend()
	plt.show()
