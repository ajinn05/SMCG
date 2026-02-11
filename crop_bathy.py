import xarray as xr

# 1. Load the full bathymetry file
ds = xr.open_dataset('./Bathy0083deg_org.nc')

# 2. Define your regional domain (slightly larger than your target to be safe)
# Example: Jeju area
lon_min, lon_max = 115.0 - 0.1, 150.0 + 0.1
lat_min, lat_max = 20.0 - 0.1, 50.0 + 0.1

# 3. Slice the data
# Use .sel() for coordinate-based slicing
regional_ds = ds.sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))

# 4. Save the cropped data
regional_ds.to_netcdf('./Bathy0083deg.nc')

print("Cropped Bathy saved! New shape:", regional_ds.elevation.shape)
