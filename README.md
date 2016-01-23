## Synopsis

A script to calculate the moon avoidance angle for NGTS. Requires astropy, numpy, scipy.optimize and seaborn

## Usage

> python moonAvoidance.py -h <br/>
usage: moonAvoidance.py [-h] [--ghostlim GHOSTLIM] [--ds9] <br/>
<br/>
A script measure the moon avoidance angle <br/>
<br/>
optional arguments: <br/>
  -h, --help           show this help message and exit <br/>
  --ghostlim GHOSTLIM  Angle below which to check images for ghosts <br/>
  --ds9                Display the images in DS9? <br/>

## Motivation

The 12 NGTS telescopes were recently fitted with new baffles and so the moon avoidance angle needed to be recalculated. 

## Installation

git clone git@github.com:NGTS/MoonAvoidance.git

## API Reference

N/A

## Tests

python moonAvoidance.py --ghostlim 30

_Insert image_

## Contributors

Let people know how they can dive into the project, include important links to things like issue trackers, irc, twitter accounts if applicable.

## License

_Update_
