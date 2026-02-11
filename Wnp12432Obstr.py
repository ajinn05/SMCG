def main():
    ## Import relevant modules and functions
    import numpy   as np
    import netCDF4 as ncd4
    from readcell import readcell

    ## Set working directory and input files
    Wrkdir = '../DatGMC/'
    
    ## For regional domain, we usually only need the regional cell file
    ## If you created 'RegionalGridCels.dat' using the previous script
    Cel_file = Wrkdir + 'Wnp12432Cels.dat'

    ## Read regional cells
    ## For regional domain, na (Arctic cells) is typically 0
    headrs, Cel = readcell([Cel_file])
    ng = int(headrs[0].split()[0])
    print(' Total regional cell number = %d' % ng)

    ## Maximum resolution levels and factor
    MRLv = 4
    MFct = 2**(MRLv-1)
    print(" Multi-Resol Level, MFct =", MRLv, MFct)

    ## Use the cropped/regional bathymetry file we discussed
    bathyf = "../Bathys/Bathy0083deg.nc"

    ## Open and read obstruction ratio in bathymetry file
    datas = ncd4.Dataset(bathyf)
    print("--- Reading Regional Bathymetry ---")
    print(datas)

    NCobs = datas.dimensions['lon'].size
    NRobs = datas.dimensions['lat'].size
    
    ## Get coordinates from the cropped file
    xlon = datas.variables['lon'][:]
    ylat = datas.variables['lat'][:]
    
    ## These are the new origins for the cropped data
    FLonb = xlon[0]
    FLatb = ylat[0]
    
    ## Calculate grid spacing
    DLonb = (xlon[-1] - xlon[0]) / float(NCobs - 1)
    DLatb = (ylat[-1] - ylat[0]) / float(NRobs - 1)
    
    print(" NCobs, NRobs, FLonb, FLatb, DLonb, DLatb = \n",
           NCobs, NRobs, FLonb, FLatb, DLonb, DLatb)

    ## Read the obstruction variable (ensure it exists in your nc file)
    Fobsin = datas.variables['obstruction'][:,:]
    print(' Raw Obstr shape =', Fobsin.shape)

    datas.close()

    ## Declare obstruction array for regional cells
    Kobstr = np.zeros(ng, dtype=int)

    
    ## Identify the origin used when the Cels.dat was created.
    ## For a regional grid, this is usually the 'x0lon' and 'y0lat' 
    ## you used in the smcellgen script (e.g., 0.0 or the regional SW corner).
    grid_origin_lon = 115.0 
    grid_origin_lat = 20.0

    ## Calculate the index offset between your NetCDF file and the Grid origin.
    # How many NetCDF pixels is the Grid Origin away from the NetCDF start?
    ShtDlt = grid_origin_lon - FLonb 
    iShft  = int(round(ShtDlt / DLonb))

    EqtDlt = grid_origin_lat - FLatb
    jEqut  = int(round(EqtDlt / DLatb))
 
    print(' Regional iShft and jEqut =', iShft, jEqut)

    ## Generate obstruction ratios for all regional cells
    print(' Generating obstruction ratios for ng =', ng)

    for n in range(ng):
        ## Mapping cell indices to bathymetry indices
        i = Cel[n, 0] + iShft
        j = Cel[n, 1] + jEqut
        
        ## Handle longitude wrap-around (mostly for global, kept for safety)
        if i >= NCobs: i = i - NCobs
        if i < 0:      i = i + NCobs
        
        ## Check for latitude bounds to avoid index errors
        if j >= NRobs or j < 0:
            # print(f' Warning: j index out of bounds at n={n}, j={j}')
            j = np.clip(j, 0, NRobs - 1)

        mi = Cel[n, 2] # Cell width factor
        nj = Cel[n, 3] # Cell height factor

        ## Average obstruction over the cell area
        avrobs = 0.0
        for ii in range(i, i + mi):
            if ii >= NCobs: ii = ii - NCobs
            avrobs += np.sum(Fobsin[j:j + nj, ii])

        ## Enforce maximum 90% blocking as per WW3 practice
        Kobstr[n] = np.min([90, int(round(100.0 * avrobs / float(nj * mi)))])

    ## Output the obstruction data
    Obstrout = Wrkdir + "Wnp12432Obst.dat"
    hdrline = "{:8d} {:5d}".format(ng, 1)
    np.savetxt(Obstrout, Kobstr, fmt='%4d', header=hdrline, comments='')

    print(" Subgrid obstruction saved in \n" + Obstrout)
    print(" All done!")

if __name__ == '__main__':
    main()

## End of SMCRegionalObstr.py
