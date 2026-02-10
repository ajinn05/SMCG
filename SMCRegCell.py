"""
## Program to generate 1-2-4km SMC cell arrays for Western North Pacific.
## 
## First created:        JGLi28Feb2023
## Last modified:        AJCho09Feb2026
##
"""

def main():
    ## Import relevant modules and functions
    import sys
    import numpy   as np
    import netCDF4 as nc

    from smcellgen import smcellgen

    Wrkdir = '../tmpfls/'
    bathyf = '../Bathys/Bathy0083deg.nc'
    
    ## Define Regional Domain parameters
    GridNm = 'RegionalGrid'  ## Name of the output grid
    Level  = 3               ## Resolution level (e.g., 1, 2, or 3)
    Global = False           ## Set to False for regional domain
    Arctic = False           ## Default value for non-polar regions

    ## Define the regional range [SW_lon, SW_lat, NE_lon, NE_lat]
    RegionalRange = [115.0, 20.0, 150.0, 50.0] 

    ## Define water level and depth parameters
    wlevel = 0.0             ## Water surface altitude (Sea level = 0.0)
    depmin = 0.0             ## Minimum elevation to cover
    dshalw = wlevel          ## Shallow water altitude for refinement

    ## Open and read bathymetry data
    datas = nc.Dataset(bathyf)
    print("--- Input Dataset Information ---")
    print(datas)

    nlat = datas.dimensions['lat'].size
    nlon = datas.dimensions['lon'].size
    ylat = datas.variables['lat'][:]
    xlon = datas.variables['lon'][:]
    
    ## Calculate grid resolution (dlat, dlon)
    dlat = (ylat[-1] - ylat[0]) / float(nlat - 1)
    dlon = (xlon[-1] - xlon[0]) / float(nlon - 1)
    print(" nlat, nlon, dlat, dlon =", nlat, nlon, dlat, dlon)

    ## Read bathymetry elevation variable
    Bathy = datas.variables['elevation'][:, :]
    depthmax = np.amin(Bathy)
    hightmax = np.amax(Bathy)
    print(' Bathy range =', depthmax, hightmax)
    print(' Bathy shape =', Bathy.shape)

    ## Pack bathy parameters into one list [nlon, nlat, dlon, dlat, lon0, lat0]
    ndzlonlat = [nlon, nlat, dlon, dlat, xlon[0], ylat[0]]

    datas.close()

    ## Set SMC grid i=j=0 origin (usually 0.0 for standard global reference)
    x0lon = xlon[0]
    y0lat = ylat[0]

    print(f"--- Generating Regional Grid: {GridNm} ---")
    print(" Domain range =", RegionalRange)

    ## Merge regional range with level and origin: [Level, x0, y0, West, South, East, North]
    mlvlxy0 = [Level, x0lon, y0lat] + RegionalRange

    ## Call the cell generation function
    smcellgen(Bathy, ndzlonlat, mlvlxy0, FileNm=Wrkdir + GridNm,
              Global=Global, Arctic=Arctic, depmin=depmin, 
              dshalw=dshalw, wlevel=wlevel)

    print(" Cells saved in: ", Wrkdir + GridNm + 'Cels.dat')

if __name__ == '__main__':
    main()

## End of program SMCRegionalCell.py
