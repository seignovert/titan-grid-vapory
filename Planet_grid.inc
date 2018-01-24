// @brief    PovRay model of Planetary grid module
// @author   B.Seignovert (univ-reims@seignovert.fr)
// @date     2016/10/12
//----------------------------------------------------

// External package
#include "colors.inc"

// Convert Latitude/Longitude coordinates in XYZ
#macro XYZ(lon,lat)
  <cos(radians(-lon))*cos(radians(lat)),sin(radians(lat)),sin(radians(-lon))*cos(radians(lat))>
#end

// Latitude / Longitude grid
#macro LonLatGrid(nLon,nLat,R)
  #if ( nLon >0 ) #local dLon = 360. / nLon; #end
  #if ( nLat >0 ) #local dLat = 180. / nLat; #end
  #local c = 0;
  #while (c < nLon)
    #local lon = c * dLon - 90;
    difference {
      torus { R_Body,R }
      plane { -z, 0 }
      rotate -90 * z
      rotate lon * y
    }
    #local c = c + 1;
  #end
  #local c = 1;
  #while (c < nLat)
    #local lat = radians(c * dLat - 90);
    torus {
      R_Body*cos(lat),R
      translate R_Body * sin(lat) * y
    }
    #local c = c + 1;
  #end
#end

// Draw circle on the planet
#macro circle(lon,lat,R,Color)
  torus {
    R_Body, R
    pigment{ color Color }
    finish { ambient .7 }
    rotate (lat+90) * z
    rotate lon * y
  }
  #local Vector = XYZ(lon,lat);
  sphere {
    Vector * R_Body, 100
    pigment{ color Color }
    finish { ambient 1 }
  }
#end

// Planetary grid
#declare Grid = difference {
    #ifndef ( SS_lat ) #local SS_lat = 0.; #warning "SubSolar      latitude  not defined." #end
    #ifndef ( SS_lon ) #local SS_lon = 0.; #warning "SubSolar      longitude not defined." #end
    #ifndef ( SC_lat ) #local SC_lat = 0.; #warning "SubSpacecraft latitude  not defined." #end
    #ifndef ( SC_lon ) #local SC_lon = 0.; #warning "SubSpacecraft longitude not defined." #end
    union{
        union {
            LonLatGrid(36,18, 2)
            LonLatGrid(12, 6,10)
            LonLatGrid(0,2,30)
            LonLatGrid(1,0,30)
            pigment { color Red }
            finish { ambient .7 }
        }
        circle(SS_lon,SS_lat,20,Yellow)
        circle(SC_lon,SC_lat,20,Blue)
    }
    plane { XYZ(SC_lon,SC_lat), 0 }
}
