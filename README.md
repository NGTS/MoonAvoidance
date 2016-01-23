## Synopsis

A script to calculate the moon avoidance angle for NGTS. Requires astropy, numpy, scipy.optimize and seaborn

## Usage
```
python moonAvoidance.py -h 
usage: moonAvoidance.py [-h] [--ghostlim GHOSTLIM] [--ds9]

A script measure the moon avoidance angle 

optional arguments: 
  -h, --help           show this help message and exit 
  --outdir OUTDIR      Folder for saving output plots 
  --ghostlim GHOSTLIM  Angle below which to check images for ghosts 
  --ds9                Display the images in DS9? 
```
## Motivation

The 12 NGTS telescopes were recently fitted with new baffles and so the moon avoidance angle needed to be recalculated. 

## Installation

git clone git@github.com:NGTS/MoonAvoidance.git

## API Reference

N/A

## Tests
Navigate to the directory containing the fits images to analyse. Then run: <br/>
``` 
python /path/to/script/moonAvoidance.py --ghostlim 30 
```
If --outdir is set the plots are saved there. If not, they are saved in the local directory. See below for example output plots. 

![Alt text](MoonAvoidance_action116380_pointingSpiral.png?raw=true "Title")

![Alt text](GhostCheck-30_action116380_pointingSpiral.png?raw=true "Title")

## Contributors

James McCormac

## License

_Update_
