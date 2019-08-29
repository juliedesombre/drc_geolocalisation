from shapely.geometry import LineString, Polygon, Point
import geopandas as gpd
import pandas as pd
import matplotlib.colors as colors
import numpy as np
from fuzzywuzzy import process



def dist_between_duplicates(cluster):
    for_dist = ""
    cluster = cluster.to_crs(epsg=3310)
    if len(cluster) == 2:
        for_dist = LineString(cluster["geometry"].tolist())
    if len(cluster) > 2:
        for_dist = pd.DataFrame()
        for_dist['geometry'] = cluster['geometry'].apply(lambda x: x.coords[0])
        for_dist = Polygon(for_dist['geometry'].tolist())
    if (type(for_dist) == str) is False:
        centroid = for_dist.centroid    
        distance = cluster.distance(centroid) / 1000
        out = gpd.GeoDataFrame({"geometry":[centroid], "mean_distance":[distance.mean()]},crs={'init':'epsg:3310'})
        out = out.to_crs(epsg=4326)
        return out




def love_machine(source_1, source_2, province):
    out = pd.DataFrame()
    match = 0
    dhis_names = source_1.fosa_name
    kemri_names = source_2.loc[(source_2.province_zone == province[0]) & (source_2.zone == province[1]),"fosa_name"]
    matched_dhis = pd.DataFrame()
    matched_kemri = pd.DataFrame()
    ratio_array = []
    if len(kemri_names) > 0:
        for row in dhis_names:
            lover_1 = process.extract(row, kemri_names, limit=1)[0]
            lover_2 = process.extract(lover_1[0], dhis_names, limit=1)[0]
            if lover_2[0] == row:
                matched_dhis = source_1[source_1.fosa_name == row].reset_index(drop=True)
                matched_dhis["match_id"] = match
                matched_kemri = source_2[(source_2.province_zone == province[0]) & 
                                         (source_2.zone == province[1]) & 
                                         (source_2.fosa_name == lover_1[0])].reset_index(drop=True)
                matched_kemri["match_id"] = match
                matched = matched_kemri.merge(matched_dhis, 
                                              left_on = ["match_id", "province_zone", "zone"], right_on = ["match_id", "province", "zone"], 
                                              suffixes=["_kemri","_snis"])
                matched["name_distance"] = lover_1[1]
                match = match + 1
                out = out.append(matched, sort = False)
        return out.reset_index()

class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
        
def matching_metrics(matched_data, string_threshold):
    print("Raw Number Matches: " + str(len(matched)))
    print("Raw % matched in Kemri: " + str(len(matched) / kemri_n))
    print("-----------------------")
    over_threshold = matched[matched.name_distance > string_threshold]
    print("Matches over string_threshold : " + str(len(over_threshold)))
    print("% matched over string_threshold in Kemri: " + str(len(over_threshold)/ kemri_n))
    return over_threshold