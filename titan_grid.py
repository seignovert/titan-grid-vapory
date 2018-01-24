#!/bin/python
# -*- coding: utf-8 -*-
# @brief    PovRay Planetary Grid representation
# @date     2016/11/28
# @author   B.Seignovert (univ-reims@seignovert.fr)
# @version  1.0
#----------------------------------------------------

import vapory as pov
import numpy  as np

DIST_SUN    = {'TITAN': 1.5e9 }               # Distance to the Sun
BODY_RADIUS = {'TITAN':  2575 }               # Planetary body radius[km]
INST_FOV    = {'ISSNA': .352, 'ISSWA': 3.52 } # Instrument field of view [deg]

class PLANET_GRID:
    def __init__(self,planet,inst,verbose=True):
        self.target  = planet
        self.inst    = inst
        self.scene   = None
        self.verbose = verbose
        return

    def __repr__(self):
        return 'PovRay Planetary Grid representation of %s seen by %s.' % (self.target, self,inst)

    # Convert lon/lat in Cartesian coordinates
    def XYZ(self,lon,lat):
        return np.array([ np.cos(np.radians(-lon))*np.cos(np.radians(lat)),np.sin(np.radians(lat)),np.sin(np.radians(-lon))*np.cos(np.radians(lat)) ])

    # Set the observation geometry (Planet + Instrument positions)
    def setGeo(self,SS,SC,dist,North):
        SS_xyz = self.XYZ( SS['lon'], SS['lat'] ) ; SC_xyz = self.XYZ( SC['lon'], SC['lat'] )

        declares = [
        'SS_lon = %f; // Subsolar      longitude [deg_W]' % SS['lon'],
        'SS_lat = %f; // Subsolar      latitude  [deg_N]' % SS['lat'],
        'SC_lon = %f; // Subspacecraft longitude [deg_W]' % SC['lon'],
        'SC_lat = %f; // Subspacecraft latitude  [deg_N]' % SC['lat'],
        'R_Body = %f; // Planetary body radius   [km]'    % BODY_RADIUS[self.target]
        ]

        camera      = pov.Camera('angle', INST_FOV[self.inst], 'location', SC_xyz * dist, 'look_at', [0,0,0],'Axis_Rotate_Trans(',SC_xyz,',',-North,')')
        light       = pov.LightSource(SS_xyz * DIST_SUN[self.target], 'color','White')
        obj         = pov.Object('Grid')
        self.scene  = pov.Scene(declares=declares, camera=camera, objects=[light,obj], included=['colors.inc','transforms.inc','Planet_grid.inc'])
        return self

    # Render with PovRay script
    def render(self,filename=None,width=None,height=None):
        if filename is None: filename = '%s-%s.png' % (self.target, self.inst)

        if self.scene is None: raise ValueError('Planet geo is not set. Run self.setGeo(SS,SC,dist,North)')
        if self.verbose: print '>> Rendering PovRay Grid Globe...'
        self.scene.render(filename , width=width, height=height, antialiasing=0.01)
        return

if __name__ == '__main__':

    # ISS image of Titan (N1827821295_1)

    width  = 1024
    height = 1024

    inst   = 'ISSNA'
    target = 'TITAN'
    SS     = {'lat': 25.6, 'lon': 129.4}
    SC     = {'lat': 0.4, 'lon': 277.0}
    dist   = 1.4e6
    North  = -178.7
    filename = None

    import sys

    if sys.argv[1] in ['-h', '--help', 'usage']:
        print 'USAGE: python grid.py filename SC_lat SC_lon SS_lat SS_lon dist north [NAC|WAC]'
        sys.exit()

    if len(sys.argv) > 1:
        filename  = sys.argv[1]
        SC['lat'] = float(sys.argv[2])
        SC['lon'] = float(sys.argv[3])
        SS['lat'] = float(sys.argv[4])
        SS['lon'] = float(sys.argv[5])
        dist      = float(sys.argv[6])
        North     = float(sys.argv[7])
    if len(sys.argv) > 8:
        if 'NA' in sys.argv[8]:
            inst = 'ISSNA'
        elif 'WA' in sys.argv[8]:
            inst = 'ISSWA'
        else:
            raise ValueError('Instrument unknown')

    PLANET_GRID(target,inst).setGeo(SS,SC,dist,North).render(filename=filename,width=width,height=height)
