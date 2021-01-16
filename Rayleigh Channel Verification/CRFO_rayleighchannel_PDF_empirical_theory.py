# Author
# Prabhu Chandhar (email: prabhu@chandhar-labs.com)


# Importing libraries
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
from scipy.stats import rayleigh
import scipy.special as sp

######## Reading samples #############
sample_rate = 2400000 # Sampling rate

samp = np.fromfile('940400000_samples.dat',np.uint8)+np.int8(-127) # Adding a signed int8 to an unsigned one results in an int16 array
x1 = samp[::2]/128 # Even samples are real(In-phase)
x2 = samp[1::2]/128 # Odd samples are imaginary(Quadrature-phase)
iq_samples = x1+x2*1j # Create the complex data samples

iq_samples=iq_samples[2000:] # Neglecting first 2000 samples
r = abs(iq_samples)


# Estimation of scale parameter 
y = 0
for j in range(1, len(r)):
    y = y + (r[j]*r[j])

sig = math.sqrt(y/(2*len(r)))


######## Plotting and saving received signal amplitude #############
sam = 2500
y = range(1,sam)
y = [i/sample_rate/1e-3 for i in y]
plt1.plot(y,abs(iq_samples)[1:sam])
plt1.xlabel('Time (ms)')
plt1.ylabel('Received signal amplitude')
plt1.grid()
plt1.savefig("Received_Signal_Amplitude" + ".png", bbox_inches='tight', pad_inches=0.5)
plt1.close()


######## Plotting and saving PDF of Rayleigh distribution #############
plt2.hist(r, density=True,histtype='stepfilled', alpha=0.2, bins=100, label='Measured',color='red') # PDF of received samples
plt2.xlabel('Received signal amplitude')
plt2.ylabel('PDF')

x = np.linspace(.0001,2,1000)

rv = rayleigh(scale=sig)
plt2.plot(x, rv.pdf(x), 'k-', lw=2, label='Analytical') # Rayleigh PDF (Theory)
plt2.legend()
plt2.savefig("Rayleigh_PDF" + ".png", bbox_inches='tight', pad_inches=0.5)
plt2.close()

