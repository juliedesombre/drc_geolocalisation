import pandas as pd
import numpy as np
import geopandas as gpd

replace_dico = {"common":{
                    "_":" ",
                    "-":" ",
                    "'":" ",
                    "ã¯":"i",
                    "ï":"i",
                    " 1":" i",
                    " 2":" ii",
                    " 3":" iii",
                    " 4":" iv",
                    "é":"e",
                    "è":"e",
                    "ô":"o",
                    "  ":" "
                    },
                "province":{
                    "mai ndombe":"maindombe",
                    "lulua":"kasai central",
                    "congo central":"kongo central",
                    "kasai occidental":"kasai",
                    "iturie":"ituri",
                    " province":"",
                    "orientale":"",
                    "buele":"bas uele",
                    "nordkivu":"nord kivu",
                    " dps":""
                    },
                "zone":{
                    'lolanga lolanga mampoko':"lolanga mampoko",
                    'nyirangongo':"nyiragongo",
                    'vuhuvi':'vuhovi',
                    'nsona pangu':'nsona mpangu',
                    'bena tshiadi':"bena tshadi",
                    'hors zone: tshiamilemba':"",
                    'mambre':"",
                    'divine':"",
                    'la police':'police',
                    'benaleka':'bena leka',
                    'mobayimbongo':'mobayi mbongo',
                    'ndjoko punda':'ndjoko mpunda',
                    'mwetshi':'muetshi',
                    'wamba luadi':'wamba lwadi',
                    'djalo djeka':'djalo ndjeka',
                    'kisandji':'kisanji',
                    'ruashi':'rwashi',
                    'haut plateau':'hauts plateaux',
                    'kiambi':'kiyambi',
                    'bogosenubea':'bogosenubia',
                    'muanda':'moanda',
                    'massa':'masa',
                    'pendjwa':'penjwa',
                    'yalifafu':'yalifafo',
                    'busanga':'bosanga',
                    'citenge':'tshitenge',
                    'banzow moke':'banjow moke',
                    'mweneditu':'mwene ditu',
                    'kimbao':'kimbau',
                    'kabeya kamwanga':'kabeya kamuanga',
                    'nyankunde':'nyakunde',
                    'gety':'gethy',
                    'mongbwalu':'mongbalu',
                    'mampoko':'lolanga mampoko',
                    " zone de sante":""
                    },
                "aire":{},
                "fosa":{
                    "centre de sante de reference":"centre de sante",
                    "hgr":"hopital general de reference",
                    "general referencia":"hopital general de reference",
                    "centre hopital":"centre hospitalier",
                    "poly clinique":"polyclinique",
                    "centre sante":"centre de sante",
                    "centre de de sante":"centre de sante",
                    "polyclinic":"polyclinique",
                    "polyclique":"polyclinique",
                    "centre hospistalier":"centre hospitalier",
                    "centre de medical":"centre medical",
                    "centre de centre de reference": "centre de sante",
                    "a general de reference":"a hopital general de reference",
                    "centre medico centre chirurgical":"centre medico chirurgical",
                    "poste sante":" poste de sante",
                    "centre hospital de reference":"hopital general de reference",
                    "posta de sante":"poste de sante",
                    "centre hospital general de reference":"hopital general de reference",
                    "centre centre chirurgical":"centre medico chirurgical",
                    "centrede sante":"centre de sante",
                    "centre de hospitalier":"centre hospitalier",
                    "poste de de sante":"poste de sante",
                    "medical center":"centre medical",
                    "health center":"centre de sante",
                    "cente de sante": "centre de sante",
                    " oste de sante": "poste de sante",
                    "cs": "centre de sante",
                    "postede sante": "poste de sante",
                    ". general de reference": " hopital general de reference",
                    " centre de hospitalier":"centre hospitalier",
                    "poste de sangte":"poste de sante",
                    "anoalite hospital":"anoalite hopital",
                    "jerusalem clinic": "jerusalem clinique",
                    "babonde ch":"babonde centre hospitalier",
                    "butembo 3 ch":"butembo 3 centre hospitalier",
                    "mushenyi centre de":"mushenyi centre de sante",
                    "de bangamba centre de sant":"de bangamba centre de sante"
                    }
                }

province_prefix = ['kl ', 'ks ', 'hk ', 'sk ', 'kr ', 'su ', 'kg ', 'it ', 'kn ',
                   'eq ', 'lm ', 'll ', 'kc ', 'hl ', 'ke ', 'tn ', 'nu ', 'mg ',
                   'tp ', 'nk ', 'bu ', 'md ', 'mn ', 'hu ', 'sn ', 'tu ']

fosa_types = ["centre de sante","poste de sante","hopital general de reference","centre medical",
              "dispensaire","centre hospitalier","hopital secondaire","polyclinique","hopital","clinique","centre medico chirurgical"]

drop = ["supprimer","structure a supprime","structure à supprime","to delete","aire de santte","aire de sante"," ",
        "zone de sante kikwit nord","bureau central dela zone de sante rurale de nioki",
        'bureau central de la zone de sante rurale de mushie']

def read_and_clean_carte_sanitaire(url):
    colnames = ["country", "province", "zone", "fosa_drop" , "fosa", "resp","address","phone","level","dhis2_id","gps"]
    carte_sanitaire = pd.read_excel(url, sheet_name = "Entités", 
                                    names=colnames )
    # Split GPS field  as separate Longitude and Latitude
    gps_as_list = carte_sanitaire.gps.str.replace("\[|\]","").str.split(",")
    carte_sanitaire["long"] = gps_as_list.apply(lambda x: x[0] if (type(x) is list ) is True else np.nan ).astype(float)
    carte_sanitaire["lat"] = gps_as_list.apply(lambda x: x[1] if (type(x) is list ) is True else np.nan ).astype(float)
    carte_sanitaire = carte_sanitaire.drop(["fosa_drop","resp","address","phone","level","gps","country"], axis=1)
    # Create a geopandas DataFrame
    carte_sanitaire = gpd.GeoDataFrame(carte_sanitaire[["province","zone","fosa","dhis2_id"]],
                             geometry=gpd.points_from_xy(carte_sanitaire.long, carte_sanitaire.lat),crs={'init':'epsg:4326'})
    # Format_names
    levels = ["province", "zone", "fosa"]
    for level in levels:
        carte_sanitaire[level] = carte_sanitaire[level].str[3:]
        carte_sanitaire[level] = name_formatter(carte_sanitaire[level], level)
    carte_sanitaire = split_names(carte_sanitaire, fosa_types, drop)
    return carte_sanitaire


def read_and_clean_kemri_data(url):
    colnames = ["country","province","fosa","fosa_type","ownership","lat","long","source"]
    kemri_data = pd.read_excel(url, names=colnames)
    # Subset only to DRC data
    kemri_drc  = kemri_data[kemri_data.country == "Democratic Republic of the Congo"]
    kemri_drc = kemri_drc.drop(["country"], axis=1)
    # Create a unique index
    kemri_drc["kemri_id"] = "km" + kemri_drc.index.astype(str)
    # Create a geopandas DataFrame
    kemri_drc = gpd.GeoDataFrame(kemri_drc[["province","fosa","kemri_id","fosa_type","ownership","source"]],
                                           geometry=gpd.points_from_xy(kemri_drc.long, kemri_drc.lat),crs={'init':'epsg:4326'}
                                            )
    # Format_names
    levels = ["province", "fosa"]
    for level in levels:
        kemri_drc[level] = name_formatter(kemri_drc[level], level)
    kemri_drc.fosa[kemri_drc.fosa.str[0:3].isin(province_prefix)] = kemri_drc.fosa[kemri_drc.fosa.str[0:3].isin(province_prefix)].str[3:]
    kemri_drc = split_names(kemri_drc, fosa_types, drop)
    return (kemri_data, kemri_drc)

def read_and_clean_zones_data(url, hierarchy):
    zones = gpd.read_file(url)
    zones.columns = ["zone_id","geometry"]
    hierarchy = pd.read_csv(hierarchy)
    hierarchy = hierarchy[hierarchy.level == 3]
    hierarchy = hierarchy[["id","name","level_2_name"]]
    hierarchy.columns = ["zone_id","zone","province"]
    # Format_names
    levels = ["province", "zone"]
    for level in levels:
        hierarchy[level] = hierarchy[level].str[3:]
        hierarchy[level] = name_formatter(hierarchy[level], level)
    zones = zones.merge(hierarchy)
    return zones


def name_formatter(name, name_level):
    name = name.str.lower().replace(replace_dico["common"], regex=True ).replace(replace_dico[name_level], regex=True ).str.strip()
    return name

def split_names(data, names, fosa_types, drop):
    type_pattern = '|'.join(fosa_types)
    data["fosa_type"] = data[names].str.extract('('+type_pattern+')', expand=True)
    data["fosa_name"] = data[names].str.replace(type_pattern, "")

    data = data[~(data[names].isin(drop))]
    data = data[~(data.fosa_name.isin(drop))]
    return data
