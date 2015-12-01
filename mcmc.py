import math
import numpy
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

# Read in data:
Dx = []
Dy = []
for line in open("data2.txt"):
	rows = line.split()
	Dx.append(float(rows[0]))
	Dy.append(float(rows[1]))

# Model
def y(x, theta):
	return theta[0] + theta[1] * x

# Chi Squared
def chi2(Dx, Dy, theta):
	s = 0.
	for i in xrange(len(Dx)):
		s += (y(Dx[i], theta) - Dy[i]) ** 2
	return s/len(Dx)
	
# Likelihood function
def P(Dx, Dy, theta):
	return -chi2(Dx, Dy, theta)
	
# Initial guess for model parameters
theta_current = [-350., 18.]
P_current = P(Dx, Dy, theta_current)

chain = []
for i in xrange(20000):
	theta_proposed = [theta+numpy.random.randn() 
					for theta in theta_current]	
	P_proposed = P(Dx, Dy, theta_proposed)
	diff = P_proposed - P_current
	ratio = math.exp(P_proposed - P_current)
	r = numpy.random.rand()
	
	if ratio > r:
		theta_current = theta_proposed
		P_current = P_proposed
	#if i >= 5000: # save chain only after burn-in	
	chain.append(theta_current)

theta0 = [c[0] for c in chain]
theta1 = [c[1] for c in chain]

##Calculate average:
#theta_avg = [0., 0.]
#for theta in chain:
	#for i in xrange(2):
		#theta_avg[i] += theta[i]
#for i in xrange(2):
	#theta_avg[i] /= len(chain)
	
## Calculate model y
#My = []
#for x in Dx:
	#My.append(y(x, theta_avg))

#plt.plot(Dx, Dy, "ro")
#plt.plot(Dx, My, ".")
#print "theta average: ", theta_avg
#print "Dx: ", Dx
#print "Dy: ", Dy
#print "My: ", My

ax1 = plt.subplot(211)
plt.plot(theta0, '-b', label='Theta[0] vs generations')
plt.legend()

ax2 = plt.subplot(212, sharex=ax1)
plt.plot(theta1, '-r', label='Theta[1] vs generations')

plt.legend()
plt.savefig("mcmc.pdf")
