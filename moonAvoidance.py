# script to measure the image median count
# level and plot the results versus moon angle
from astropy.io import fits
import matplotlib.pyplot as pl
from matplotlib import cm
from scipy.optimize import curve_fit
import argparse as ap
import numpy as np
import glob as g
import seaborn, os, time
from math import sqrt,ceil
from ds9 import *

# get command line args
def argParse():
	parser=ap.ArgumentParser(description="A script to measure the NGTS moon avoidance angle")
	parser.add_argument('--ghostlim',type=int,help = "Angle below which to check images for ghosts")
	parser.add_argument('--outdir',type=int,help = "Folder for saving output plots")
	parser.add_argument('--ds9',help = "Display the images in DS9?",action='store_true')
	args=parser.parse_args()
	return args

args=argParse()
if not args.outdir:
	outdir=os.getcwd()
else:
	outdir=args.outdir

def estimate_exp_coeffs(counts):
	return [max(counts)*2,0.154,min(counts)]

def exp_func(x, a, c, d):
    return a*np.exp(-c*x)+d

def getMoonData(outdir):
	moonFile='%s/moonSummary.txt' % (outdir)
	t=g.glob('*.fits')
	if os.path.exists(moonFile) == False:
		f=open(moonFile,'w')
		f.write('# MedCounts\tMoonAng\tMoonPhase\n')
		moon_ang=np.empty(len(t))
		moon_phase=np.empty(len(t))
		median_counts=np.empty(len(t))
		for i in range(0,len(t)):
			h=fits.open(t[i])
			d=h[0].data
			prescan=d[0:2048,:20]
			overscan=d[0:2048,2068:]
			data=d[0:2048,20:2068]
			median_counts[i]=np.median(data)-np.median(overscan)
			moon_ang[i]=float(h[0].header['MOONDIST'])
			moon_phase[i]=float(h[0].header['MOONFRAC'])
			h.close()
			f.write('%d\t%.2f\t%.2f\n'%(median_counts[i],moon_ang[i],moon_phase[i]))
			print ("[%d/%d]..." % (i+1,len(t)))
		f.close()
	else:
		print "Found moonFile, reading it..."
		median_counts,moon_ang,moon_phase=np.loadtxt(moonFile,usecols=[0,1,2],unpack=True)
	return t,median_counts,moon_ang,moon_phase

def fitMoonData(p0,moon_ang,median_counts):
	popt, pcov = curve_fit(exp_func, moon_ang, median_counts, p0)
	xfit=np.linspace(0,180,180)
	yfit=exp_func(xfit,*popt)
	return popt,pcov,xfit,yfit

def plotMoonDataFit(moon_ang,median_counts,xfit,yfit,moon_phase):
	action=os.getcwd().split('/')[-1]
	fig,ax=pl.subplots(1,figsize=(10,10))
	seaborn.axes_style("darkgrid")
	ax.plot(moon_ang,median_counts,'r.')
	ax.plot(xfit,yfit,'k--')
	ax.set_xlabel('Moon Distance (deg)')
	ax.set_ylabel('Median ADU (image)')
	ax.set_yticks(np.arange(0,max(yfit),2000))
	ax.set_title('Moon Avoidance Test (%s - %d%% illuminated)' % (action, int(np.average(moon_phase)*100)))
	ax.set_xlim(0,180)
	ax.set_ylim(0,max(median_counts))
	ax.grid(True)
	fig.savefig("%s/MoonAvoidance_%s.png" % (outdir,action), dpi=300)
	return action

# check for ghosts on images where MOONDIST <= ghostlim
def checkGhostLimit(moon_ang,t,action):
	check_img,check_ang=[],[]
	for i in range(0,len(moon_ang)):
		if moon_ang[i] <= args.ghostlim:
			check_ang.append(moon_ang[i])
			check_img.append(t[i])
	temp=zip(check_ang,check_img)
	temp.sort()
	check_ang_s,check_img_s=zip(*temp)

	if args.ds9:
		ds=ds9()
		time.sleep(5)
		ds.set('scale zscale')
		ds.set('preserve scale')
		ds.set('preserve pan')
		artefacts=[]
		for i in range(0,len(check_img_s)):
			ds.set('tile yes')
			ds.set('frame 1')
			ds.set('file %s' % (check_img_s[i]))
			ds.set('zoom to fit')
			ds.set('cmap invert yes')
			print "%s MOONDIST: %.2f" % (check_img_s[i],check_ang_s[i])
			next_yn=raw_input("Are the image artefacts? e.g. (y/n): ")
			artefacts.append(next_yn.lower())

	fig = pl.figure(2,figsize=(15,15))
	img_stack=[]
	montage_dim=int(ceil(sqrt(len(check_img_s))))
	c=0
	for i in range(0,montage_dim):
		for j in range(0,montage_dim):
			ax = fig.add_subplot(montage_dim, montage_dim, c+1, xticks=[], yticks=[])
			if c < len(check_img_s):
				cd=fits.open(check_img_s[c])[0].data
				cdata=cd[0:2048,20:2068]
				coscan=cd[0:2048,2068:]
				cdcor=cdata-np.median(coscan)
				ax.imshow(cdcor,cmap=cm.afmhot,vmin=0.8*np.median(cdcor),vmax=1.2*np.median(cdcor),interpolation=None)        
				ax.set_title('MD: %.2f' % (check_ang_s[c]))
			print c
			c+=1
	print ("Saving figure...")
	fig.savefig('%s/GhostCheck-%d_%s.png' % (outdir,args.ghostlim,action),dpi=300)

def main():
	t,median_counts,moon_ang,moon_phase=getMoonData(outdir)
	p0=estimate_exp_coeffs(median_counts)
	popt,pcov,xfit,yfit=fitMoonData(p0,moon_ang,median_counts)
	action=plotMoonDataFit(moon_ang,median_counts,xfit,yfit,moon_phase)
	if args.ghostlim:
		checkGhostLimit(moon_ang,t,action)

if __name__ == '__main__':
	main()
