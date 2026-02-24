from utils import *
import sys
#on my computer _tkinter.TclError: failed to allocate font due to internal system font engine problem
# if plt is called after using xarray.open_dataset() ... very strange
# I need a false call of plt before
x=[1,2,3,4,5,6,5,4,3]
plt.plot(x)
plt.close()

horizon=24#in hour
web_root='https://dd.meteo.gc.ca/today/ensemble/reps/10km/grib2/00/'
var_codes='WIND_AGL-80m'
uswt_file='data/US_Wind_Turbine_Database.csv'
eia_file='data/eia_generator_202506.xlsx'

#try to create a .nc file for testing purposes, only if NOT on windows session
convert_grib2_to_nc(file='tests/testfile.grib2')

#load
###load us wind turbine database
uswt_db=pd.read_csv(uswt_file,low_memory=False)
#uwstdb acronym here https://energy.usgs.gov/uswtdb/api-doc/
uswt_db=uswt_db .drop(uswt_db[uswt_db['eia_id']<0].index)
uswt_db=uswt_db .drop(uswt_db[uswt_db['t_cap']<0].index)
uswt_db=uswt_db .drop(uswt_db[uswt_db['p_cap']<0].index)
uswt_db=uswt_db.drop(uswt_db[uswt_db['t_hh']<0].index)


if len(sys.argv)==1:
    #test case/default
    sys.argv.append('-state')
    territory='TX'
    Df,location =WT_USagg(uswt_db,'state',territory)

elif len(sys.argv)>1:
    if sys.argv[-1]=='-market':
        #print('For a comprehensive map of US energy market : https://www.ferc.gov/electric-power-markets')
        territory=input('US market: ')
        uswt_db=get_market(uswt_db,eia_file)
        Df,location=WT_USagg(uswt_db,'market',territory)
    

    elif sys.argv[-1]=='-state':
        territory=input('US state (abbreviation): ') 
        Df,location =WT_USagg(uswt_db,'state',territory)

    else:
        'error'
        #return    


files=files_to_download(var_codes,web_root,horizon)
WForecast=extract_fromfiles(files,location)#dimensions are (time, nmodels,nlocation)
Power_agg=aggregate_power(WForecast,Df)


#figure
tzone=get_tzone(Df['ylat'].mean(),Df['xlong'].mean())
mean_loc=(Df['ylat'].mean(),Df['xlong'].mean(),territory,tzone) 
fig4prod(Power_agg,mean_loc,'Power')
#compare with https://www.ercot.com/gridmktinfo/dashboards/combinedwindandsolar for texas



