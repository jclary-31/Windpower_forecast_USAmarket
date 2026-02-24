import src.utils as utils
import pytest
import requests
import xarray as xr
import os

# note if on windows,  load_grib2 will create the following warning/error message
# untimeWarning: Engine 'cfgrib' loading failed: Cannot find the ecCodes library
# I don't know how to ignore this warning, but it is not a problem, as a created an .nc file for testing


@pytest.fixture
def setup():
    web_root='https://dd.meteo.gc.ca/today/ensemble/reps/10km/grib2/00/'
    web_dir=web_root+'000'+'/'
    maxhour=6
    var_code='WIND_AGL-80m'
    return web_root, web_dir, maxhour, var_code




##############tests for web data extraction

def test_web_root_dir_exist(setup):
    web_root, web_dir, _,_ = setup
    response_root=requests.get(web_root)
    response_dir=requests.get(web_dir)
    assert response_root.status_code == 200
    assert response_dir.status_code == 200


def test_files_to_download(setup):
    web_root, _, maxhour, var_code = setup
    assert len(utils.files_to_download(var_code,web_root, 0)) ==1 #only the 000 file
    assert len(utils.files_to_download(var_code,web_root, maxhour)) ==1+ maxhour//3 #one file every 3 hours


def test_download_file(setup):
    web_root, _, _, var_code = setup
    file_to_download=utils.files_to_download(var_code,web_root, 0)[0]
    assert utils.download_file(file_to_download) == True


def test_load_ds():
    if os.name == 'nt':
        ds=xr.open_dataset('tests/testfile.nc',engine='netcdf4',decode_timedelta=True) 
    else:   
        ds=utils.load_grib2('tests/testfile.grib2')

    assert isinstance(ds, xr.Dataset)


