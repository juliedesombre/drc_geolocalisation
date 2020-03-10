import pandas as pd
import numpy as np
import geopandas as gpd

#toto

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
                    "katanga":"haut katanga",
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
                    'tshilenge':'tshitenge',
                    'banzow moke':'banjow moke',
                    "banjow moke":'banjow moke',
                    'mweneditu':'mwene ditu',
                    'kimbao':'kimbau',
                    'kabeya kamwanga':'kabeya kamuanga',
                    'penjwa':'pendjwa',
                    'nyankunde':'nyakunde',
                    'gety':'gethy',
                    'mongbwalu':'mongbalu',
                    'mampoko':'lolanga mampoko',
                    'bena tshiadi': 'bena tshadi',
                    'nsona-pangu':'nsona mpangu',
                    " zone de sante":""
                    },
                "aire":{},
                "fosa":{
                    "centre de sante de reference":"centre de sante",
                    "csr":"centre de sante",
                    "hgr":"hopital general de reference",
                    "general referencia":"hopital general de reference",
                    "centre hopital":"centre hospitalier",
                    "cs":"centre de sante",
                    "poly clinique":"polyclinique",
                    "centre sante":"centre de sante",
                    "centre de de sante":"centre de sante",
                    "polyclinic":"polyclinique",
                    "polyclique":"polyclinique",
                    "policlique":"polyclinique",
                    "palyclinique":"polyclinique",
                    "policlynique":"polyclinique",
                    "clinic":"clinique",
                    "centre hospistalier":"centre hospitalier",
                    "centre de medical":"centre medical",
                    "centre de centre de reference": "centre de sante",
                    "a general de reference":"a hopital general de reference",
                    "h?pital":"hopital",
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
                    "de bangamba centre de sant":"de bangamba centre de sante",
                    "ã‰":"e",
                    "?":"e",
                    "ste":"sainte",
                    "st":"saint",
                    "Centr?":"centre",
                    "centr?":"centre",
                    "ra©fa©rence":"reference",
                    "maternita©":"maternite",
                    "sant?":"sante",
                    "santa‰":"sante",
                    "santa©":"sante",
                    "ra‰fa‰renc":"reference",
                    "ra©ference":"reference",
                    "solidarita©":"solidarite"
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





def name_formatter(data, names, name_level):
    data[names] = data[names].str.lower().replace(replace_dico["common"], regex=True ).replace(replace_dico[name_level], regex=True ).str.strip()
    data.loc[data[names].str[0:3].isin(province_prefix), names] = data.loc[data[names].str[0:3].isin(province_prefix), names].str[3:]
    data.loc[data[names] == "", names] = None
    return data

def split_names(data, names, fosa_types, drop):
    type_pattern = '|'.join(fosa_types)
    data["fosa_type"] = data[names].str.extract('('+type_pattern+')', expand=True)
    data["fosa_name"] = data[names].str.replace(type_pattern, "")

    data = data[~(data[names].isin(drop))]
    data = data[~(data.fosa_name.isin(drop))]
    return data
