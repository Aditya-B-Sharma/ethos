import geocoder
import pandas as pd
import requests
import matplotlib

def geocode_fwd(location_text):
    """Takes a address/location as a string and uses google's API
    via geocoder to perform forward geocoding given the address/location
    e.g. 'Gungahlin, ACT' -> lat: -35.1831, lng: 149.1557105. Returns 
    latitude and longitude in list form, e.g. [-35.1831, 149.133]."""
    g = geocoder.arcgis(location_text)
    return g.latlng
    
def get_meshID_ACT(latlng_list):
    """Takes in a list of a latlng pair, and uses it to search up the corresponding
    mesh block ID in the gnaf dataset."""
    gnaf = pd.read_csv("C:/Users/Adi/Desktop/GovHack/e_thos/app/data/ACT_ADDRESS_DEFAULT_GEOCODE_psv.psv",sep="|")
    mb = pd.read_csv("C:/Users/Adi/Desktop/GovHack/e_thos/app/data/ACT_ADDRESS_MESH_BLOCK_2016_psv.psv",sep="|",low_memory=False)
    gnaf["LATITUDE"] = gnaf["LATITUDE"].round(3)
    gnaf["LONGITUDE"] = gnaf["LONGITUDE"].round(3)
    addresses = gnaf.loc[gnaf["LATITUDE"] == round(latlng_list[0], 3)]
    addresses_final = addresses.loc[addresses["LONGITUDE"] == round(latlng_list[1],3)]
    meshID = mb.loc[mb["ADDRESS_DETAIL_PID"] == addresses_final["ADDRESS_DETAIL_PID"].values[0]]
    output = meshID["MB_2016_PID"].values[0].replace("MB16", "")
    return int(output)
    
    
def get_district_ACT(meshID):
    """Takes in a mesh block id (int) as input.
    Returns the corresponding district as a string."""
    mb_boundaries = pd.read_csv("C:/Users/Adi/Desktop/GovHack/e_thos/app/data/MB_2016_ACT.csv")
    row = mb_boundaries.loc[mb_boundaries['MB_CODE_2016'] == meshID]
    return row["SA3_NAME_2016"].values[0]
    
def get_population_projections_ACT(district):
    """Takes in a string representing district name as input.
    Returns a time series graph of population projections for the 
    next 5 years."""
    pp_by_district = pd.read_csv("C:/Users/Adi/Desktop/GovHack/e_thos/app/data/ACT_Population_Projections_by_District__2015_-_2041_.csv")
    #output = []
    rows = pp_by_district.loc[pp_by_district['District'] == district.capitalize()]
    #i = pd.DatetimeIndex(['2019-06-30','2020-06-30','2021-06-30','2022-06-30','2023-06-30'])
    if not rows.empty:
        rows.index = pd.DatetimeIndex(rows['Year'])
        # del rows['Year']
        s = rows.iloc[4:9,-172:].sum(axis=1)
        print(s)
        graph = s.to_frame().plot()
        graph.set_ylabel("Number of people")
        graph.legend(['Population Projection'])
        return graph
        
    else:
        print("This district does not exist.")
        return "Unable to calculate district statistics." 
    return "end case - error"    
    
def get_district_pp(meshID):
    x = get_district_ACT(meshID)
    get_population_projections_ACT(x)       
    
    