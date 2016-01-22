# script to measure the image median count
# level and plot the results versus moon angle
from astropy.io import fits
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit
import numpy as np
import glob as g
import seaborn, os

def estimate_exp_coeffs(counts):
	return [max(counts)*2,0.154,min(counts)]

def exp_func(x, a, c, d):
    return a*np.exp(-c*x)+d

t=g.glob('*.fits')
moon_ang=np.empty(len(t))
moon_phase=np.empty(len(t))
median_counts=np.empty(len(t))
for i in range(0,len(t)):
	h=fits.open(t[i])
	d=h[0].data
	median_counts[i]=np.median(d)
	moon_ang[i]=h[0].header['MOONDIST']
	moon_phase[i]=h[0].header['MOONFRAC']

# fit exponential decay to the data - not quite right but close enough
p0=estimate_exp_coeffs(median_counts)
popt, pcov = curve_fit(exp_func, moon_ang, median_counts, p0)
xfit=np.linspace(0,180,180)
yfit=exp_func(xfit,*popt)

fig,ax=pl.subplots(1,figsize=(10,10))
seaborn.axes_style("darkgrid")
ax.plot(moon_ang,median_counts,'r.')
ax.plot(xfit,yfit,'k--')
ax.set_xlabel('Moon Distance (deg)')
ax.set_ylabel('Median ADU (image)')
ax.set_title('Moon Avoidance Test (%s - %d%% illuminated)' % (os.getcwd().split('/')[-1], int(np.average(moon_phase)*100)))
ax.set_xlim(0,180)
ax.grid(True)
pl.show()