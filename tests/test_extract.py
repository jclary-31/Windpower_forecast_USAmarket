import src.utils as utils
import xarray as xr
import os


def test_nearest_index():
    location=[(40.7128, -74.0060,'New York','tzone'),
            (34.0522, -118.2437,'Los Angeles','tzone')]

    if os.name == 'nt':
        ds=xr.open_dataset('tests/testfile.nc',engine='netcdf4',decode_timedelta=True)
    else:
        ds=utils.load_grib2('tests/testfile.grib2')

    idy,idx=utils.nearest_index(ds,location)

    assert idy==[321,289]
    assert idx==[679,250]


#######tests for data extraction and processing

def test_extract_atlocation():
    iy=[321,289]
    ix=[679,250]
    if os.name == 'nt':
        ds=xr.open_dataset('tests/testfile.nc',engine='netcdf4',decode_timedelta=True)
    else:
        ds=utils.load_grib2('tests/testfile.grib2')

    newds=utils.extract_atlocation(ds,iy,ix)

    assert isinstance(newds, xr.Dataset)
    assert newds.sizes['models']==20
    assert newds.sizes['loc']==len(ix)


def test_extract_fromfiles():
    files=['tests/testfile.nc','tests/testfile.nc']
    location=[(40.7128, -74.0060,'New York','junk'),
            (34.0522, -118.2437,'Los Angeles','junk')]

    newds=utils.extract_fromfiles(files,location)

    assert isinstance(newds, xr.Dataset)
    assert newds.sizes['models']==20
    assert newds.sizes['loc']==len(location)
    assert newds.sizes['time']==len(files)