import json

class QueryItem:
    def __init__(self, query_id, title, code_text, collection, pipeline):
        self.id = query_id
        self.title = f"Req {query_id}: {title}"
        self.code_text = code_text
        self.collection = collection
        self.pipeline = pipeline

    def execute(self, bridge):
        return bridge.execute_pipeline(self.collection, self.pipeline)


def get_all_queries():
    queries = []

    # Auxiliar para cruces complejos
    lookup_maker_country_cont = [
        {"$lookup": {
            "from": "makers",
            "let": {"car_model": "$modelID"},
            "pipeline": [
                {"$unwind": "$models"},
                {"$match": {"$expr": {"$eq": ["$models.modelID", "$$car_model"]}}}
            ],
            "as": "maker_info"
        }},
        {"$unwind": "$maker_info"},
        {"$lookup": {"from": "countries", "localField": "maker_info.countryID", "foreignField": "_id", "as": "country_info"}},
        {"$unwind": "$country_info"},
        {"$lookup": {"from": "continents", "localField": "country_info.contID", "foreignField": "_id", "as": "cont_info"}},
        {"$unwind": "$cont_info"}
    ]

    # Req 0: Consola Libre
    q0_p = [{"$match": {"activo": True}}, {"$limit": 10}]
    queries.append(QueryItem(0, "Consola Libre", "# Req 0: Consola Libre\n# Colección asignada automáticamente: cars\npipeline = " + json.dumps(q0_p, indent=2), "cars", q0_p))

    # Req 1
    q1_p = [{"$match": {"activo": True, "year": {"$gte": 2024}, "mpg": {"$gte": 35}}}, {"$sort": {"mpg": -1}}, {"$project": {"_id": 0, "Descripción": "$descr", "Año": "$year", "Rendimiento": "$mpg"}}]
    queries.append(QueryItem(1, "Autos 2024+ con rendimiento >= 35 mpg", "# Req 1\npipeline = " + json.dumps(q1_p, indent=2), "cars", q1_p))

    # Req 2
    q2_p = [{"$match": {"activo": True, "cylinders": 4, "horsepower": {"$gte": 250}}}] + lookup_maker_country_cont + [{"$match": {"cont_info.continent": "europe"}}, {"$sort": {"horsepower": -1}}, {"$project": {"_id": 0, "Descripción": "$descr", "País": "$country_info.countryName", "Potencia": "$horsepower"}}]
    queries.append(QueryItem(2, "Autos europeos de 4 cilindros con >= 250 hp", "# Req 2\npipeline = " + json.dumps(q2_p, indent=2), "cars", q2_p))

    # Req 3
    q3_p = [{"$match": {"activo": True, "descr": {"$regex": "t$"}}}] + lookup_maker_country_cont + [{"$match": {"country_info.countryName": "japan"}}, {"$count": "Total Autos Japoneses Turbo"}]
    queries.append(QueryItem(3, "Conteo de autos japoneses con motor turbo", "# Req 3\npipeline = " + json.dumps(q3_p, indent=2), "cars", q3_p))

    # Req 4
    q4_p = [{"$match": {"activo": True, "$or": [{"$and": [{"weight": {"$lt": 3000}}, {"accel": {"$lt": 9}}]}, {"$and": [{"cylinders": {"$gte": 8}}, {"mpg": {"$gte": 19}}]}]}}, {"$project": {"_id": 0, "Descripción": "$descr", "Peso": "$weight", "Aceleración": "$accel", "Cilindros": "$cylinders", "Rendimiento": "$mpg"}}]
    queries.append(QueryItem(4, "Filtro combinado por peso/aceleración o cilindros/mpg", "# Req 4\npipeline = " + json.dumps(q4_p, indent=2), "cars", q4_p))

    # Req 5
    q5_p = [{"$match": {"activo": True}}, {"$project": {"_id": 0, "Fabricante": "$fullName", "countryID": "$countryID", "NumMarcas": {"$size": "$models"}, "Marcas": "$models.model"}}, {"$match": {"NumMarcas": {"$gt": 1}}}, {"$lookup": {"from": "countries", "localField": "countryID", "foreignField": "_id", "as": "c_info"}}, {"$unwind": "$c_info"}, {"$project": {"Fabricante": 1, "País": "$c_info.countryName", "Modelos": "$Marcas"}}]
    queries.append(QueryItem(5, "Fabricantes con más de una marca comercial", "# Req 5\npipeline = " + json.dumps(q5_p, indent=2), "makers", q5_p))

    # Req 6
    q6_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$project": {"_id": 0, "Descripción": "$descr", "Marca": "$maker_info.models.model", "Fabricante": "$maker_info.maker"}}, {"$match": {"$expr": {"$ne": ["$Marca", "$Fabricante"]}}}]
    queries.append(QueryItem(6, "Autos cuya marca es distinta de su grupo fabricante", "# Req 6\npipeline = " + json.dumps(q6_p, indent=2), "cars", q6_p))

    # Req 7
    q7_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": "$country_info.countryName", "NumAutos": {"$sum": 1}, "AvgMPG": {"$avg": "$mpg"}, "AvgHP": {"$avg": "$horsepower"}}}, {"$sort": {"NumAutos": -1}}, {"$project": {"_id": 0, "País": "$_id", "Total Autos": "$NumAutos", "MPG Promedio": {"$round": ["$AvgMPG", 1]}, "HP Promedio": {"$round": ["$AvgHP", 1]}}}]
    queries.append(QueryItem(7, "Estadísticas por país (Autos, MPG prom, HP prom)", "# Req 7\npipeline = " + json.dumps(q7_p, indent=2), "cars", q7_p))

    # Req 8
    q8_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": "$maker_info.fullName", "NumAutos": {"$sum": 1}, "Marcas": {"$addToSet": "$maker_info.models.modelID"}, "AvgHP": {"$avg": "$horsepower"}}}, {"$sort": {"NumAutos": -1}}, {"$project": {"_id": 0, "Fabricante": "$_id", "Total Autos": "$NumAutos", "Marcas Distintas": {"$size": "$Marcas"}, "HP Promedio": {"$round": ["$AvgHP", 1]}}}]
    queries.append(QueryItem(8, "Estadísticas por fabricante (Autos, Marcas, HP prom)", "# Req 8\npipeline = " + json.dumps(q8_p, indent=2), "cars", q8_p))

    # Req 9
    q9_p = [{"$match": {"activo": True}}, {"$lookup": {"from": "countries", "localField": "countryID", "foreignField": "_id", "as": "c_info"}}, {"$unwind": "$c_info"}, {"$lookup": {"from": "continents", "localField": "c_info.contID", "foreignField": "_id", "as": "cont_info"}}, {"$unwind": "$cont_info"}, {"$unwind": "$models"}, {"$group": {"_id": "$cont_info.continent", "TotalModelos": {"$sum": 1}}}, {"$project": {"_id": 0, "Continente": "$_id", "Total Modelos": "$TotalModelos"}}]
    queries.append(QueryItem(9, "Conteo de marcas/modelos por continente", "# Req 9\npipeline = " + json.dumps(q9_p, indent=2), "makers", q9_p))

    # Req 10
    q10_p = [{"$match": {"activo": True}}, {"$bucket": {"groupBy": "$mpg", "boundaries": [0, 20, 25, 30, 35, 40, 100], "default": "40+", "output": {"CantidadAutos": {"$sum": 1}, "PesoPromedio": {"$avg": "$weight"}}}}, {"$project": {"_id": 0, "Rango MPG": {"$switch": {"branches": [{"case": {"$eq": ["$_id", 0]}, "then": "[0, 20)"}, {"case": {"$eq": ["$_id", 20]}, "then": "[20, 25)"}, {"case": {"$eq": ["$_id", 25]}, "then": "[25, 30)"}, {"case": {"$eq": ["$_id", 30]}, "then": "[30, 35)"}, {"case": {"$eq": ["$_id", 35]}, "then": "[35, 40)"}], "default": "40+"}}, "Total Autos": "$CantidadAutos", "Peso Promedio (lb)": {"$round": ["$PesoPromedio", 1]}}}]
    queries.append(QueryItem(10, "Clasificación por rangos de rendimiento (mpg)", "# Req 10\npipeline = " + json.dumps(q10_p, indent=2), "cars", q10_p))

    # Req 11
    q11_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": "$maker_info.fullName", "NumAutos": {"$sum": 1}, "AvgMPG": {"$avg": "$mpg"}}}, {"$match": {"NumAutos": {"$gte": 8}}}, {"$sort": {"AvgMPG": -1}}, {"$limit": 5}, {"$project": {"_id": 0, "Fabricante": "$_id", "Total Autos": "$NumAutos", "MPG Promedio": {"$round": ["$AvgMPG", 1]}}}]
    queries.append(QueryItem(11, "Top 5 fabricantes con mayor rendimiento promedio (>=8 autos)", "# Req 11\npipeline = " + json.dumps(q11_p, indent=2), "cars", q11_p))

    # Req 12
    q12_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$project": {"continent": "$cont_info.continent", "categoria": {"$cond": [{"$gte": ["$mpg", 30]}, "Alta", {"$cond": [{"$gte": ["$mpg", 20]}, "Media", "Baja"]}]}}}, {"$group": {"_id": {"continente": "$continent", "categoria": "$categoria"}, "Total": {"$sum": 1}}}, {"$project": {"_id": 0, "Continente": "$_id.continente", "Categoría": "$_id.categoria", "Total Autos": "$Total"}}]
    queries.append(QueryItem(12, "Clasificación de autos por categoría y continente", "# Req 12\npipeline = " + json.dumps(q12_p, indent=2), "cars", q12_p))

    # Req 13
    q13_p = [{"$match": {"activo": True}}, {"$unwind": {"path": "$models", "preserveNullAndEmptyArrays": True}}, {"$lookup": {"from": "cars", "localField": "models.modelID", "foreignField": "modelID", "as": "car_list"}}, {"$group": {"_id": "$fullName", "TotalAutos": {"$sum": {"$size": "$car_list"}}}}, {"$project": {"_id": 0, "Fabricante": "$_id", "Total Autos": "$TotalAutos"}}]
    queries.append(QueryItem(13, "Total de autos por fabricante desde colección makers", "# Req 13\npipeline = " + json.dumps(q13_p, indent=2), "makers", q13_p))

    # Req 14
    q14_p = [{"$match": {"activo": True}}, {"$unwind": "$models"}, {"$lookup": {"from": "cars", "localField": "models.modelID", "foreignField": "modelID", "as": "car_list"}}, {"$match": {"car_list": {"$size": 0}}}, {"$project": {"_id": 0, "Fabricante": "$fullName", "Modelo Sin Registros": "$models.model"}}]
    queries.append(QueryItem(14, "Modelos de catálogo sin ningún auto registrado", "# Req 14\npipeline = " + json.dumps(q14_p, indent=2), "makers", q14_p))

    # Req 15
    q15_p = [{"$match": {"activo": True}}, {"$sort": {"horsepower": -1}}, {"$limit": 5}] + lookup_maker_country_cont + [{"$project": {"_id": 0, "Descripción": "$descr", "Potencia (hp)": "$horsepower", "Fabricante": "$maker_info.fullName"}}]
    queries.append(QueryItem(15, "Top 5 autos más potentes y su fabricante", "# Req 15\npipeline = " + json.dumps(q15_p, indent=2), "cars", q15_p))

    # Req 16
    q16_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$sort": {"mpg": -1}}, {"$group": {"_id": "$cont_info.continent", "TopAutos": {"$push": {"descr": "$descr", "mpg": "$mpg"}}}}, {"$project": {"_id": 0, "Continente": "$_id", "Top 3 Autos": {"$slice": ["$TopAutos", 3]}}}]
    queries.append(QueryItem(16, "Top 3 autos con mayor rendimiento por continente", "# Req 16\npipeline = " + json.dumps(q16_p, indent=2), "cars", q16_p))

    # Req 17
    q17_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": {"maker": "$maker_info.fullName", "model": "$maker_info.models.model"}, "Total": {"$sum": 1}}}, {"$sort": {"Total": -1}}, {"$group": {"_id": "$_id.maker", "ModeloDominante": {"$first": "$_id.model"}, "MaxAutos": {"$first": "$Total"}}}, {"$project": {"_id": 0, "Fabricante": "$_id", "Modelo Principal": "$ModeloDominante", "Autos": "$MaxAutos"}}]
    queries.append(QueryItem(17, "Modelo con más autos registrados por fabricante", "# Req 17\npipeline = " + json.dumps(q17_p, indent=2), "cars", q17_p))

    # Req 18
    q18_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": "$cont_info.continent", "Count": {"$sum": 1}}}, {"$group": {"_id": None, "TotalGlobal": {"$sum": "$Count"}, "Continentes": {"$push": {"cont": "$_id", "cnt": "$Count"}}}}, {"$unwind": "$Continentes"}, {"$project": {"_id": 0, "Continente": "$Continentes.cont", "Porcentaje": {"$round": [{"$multiply": [{"$divide": ["$Continentes.cnt", "$TotalGlobal"]}, 100]}, 2]}}}]
    queries.append(QueryItem(18, "Porcentaje de autos por continente", "# Req 18\npipeline = " + json.dumps(q18_p, indent=2), "cars", q18_p))

    # Req 19
    q19_p = [{"$match": {"activo": True}}, {"$group": {"_id": "$cylinders", "AvgCylMPG": {"$avg": "$mpg"}}}, {"$lookup": {"from": "cars", "localField": "_id", "foreignField": "cylinders", "as": "car_info"}}, {"$unwind": "$car_info"}, {"$project": {"_id": 0, "Descripción": "$car_info.descr", "Cilindros": "$_id", "MPG Auto": "$car_info.mpg", "Promedio Cilindrada": {"$round": ["$AvgCylMPG", 1]}, "Diferencia": {"$round": [{"$subtract": ["$car_info.mpg", "$AvgCylMPG"]}, 1]}}}, {"$sort": {"Diferencia": -1}}, {"$limit": 5}]
    queries.append(QueryItem(19, "Top 5 autos que superan el promedio de mpg de su cilindrada", "# Req 19\npipeline = " + json.dumps(q19_p, indent=2), "cars", q19_p))

    # Req 20
    q20_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$group": {"_id": "$cont_info.continent", "TotalAutos": {"$sum": 1}, "V8OrMore": {"$sum": {"$cond": [{"$gte": ["$cylinders", 8]}, 1, 0]}}}}, {"$project": {"_id": 0, "Continente": "$_id", "Total Autos": "$TotalAutos", "Autos V8+": "$V8OrMore", "Porcentaje V8+": {"$round": [{"$multiply": [{"$divide": ["$V8OrMore", "$TotalAutos"]}, 100]}, 1]}}}]
    queries.append(QueryItem(20, "Porcentaje de autos de 8+ cilindros por continente", "# Req 20\npipeline = " + json.dumps(q20_p, indent=2), "cars", q20_p))

    # Req 21
    q21_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$project": {"_id": 0, "Descripción": "$descr", "País": "$country_info.countryName", "HP/1000lb": {"$round": [{"$multiply": [{"$divide": ["$horsepower", "$weight"]}, 1000]}, 1]}}}, {"$sort": {"HP/1000lb": -1}}, {"$limit": 10}]
    queries.append(QueryItem(21, "Top 10 autos por potencia relativa por cada 1000 lb", "# Req 21\npipeline = " + json.dumps(q21_p, indent=2), "cars", q21_p))

    # Req 22
    q22_p = [{"$match": {"activo": True}}, {"$project": {"Fabricante": "$maker", "ModelosDiferentes": {"$filter": {"input": "$models.model", "as": "m", "cond": {"$ne": ["$$m", "$maker"]}}}}}, {"$match": {"$expr": {"$gt": [{"$size": "$ModelosDiferentes"}, 0]}}}, {"$project": {"_id": 0, "Fabricante": 1, "Modelos Distintos": "$ModelosDiferentes"}}]
    queries.append(QueryItem(22, "Modelos con nombre distinto a su fabricante", "# Req 22\npipeline = " + json.dumps(q22_p, indent=2), "makers", q22_p))

    # Req 23
    q23_p = [{"$match": {"activo": True}}, {"$facet": {"PorContinente": lookup_maker_country_cont + [{"$group": {"_id": "$cont_info.continent", "Total": {"$sum": 1}}}], "PorCilindros": [{"$group": {"_id": "$cylinders", "Total": {"$sum": 1}}}], "StatsMPG": [{"$group": {"_id": None, "MinMPG": {"$min": "$mpg"}, "MaxMPG": {"$max": "$mpg"}, "AvgMPG": {"$avg": "$mpg"}}}]}}]
    queries.append(QueryItem(23, "Consulta multifacética (Continentes, Cilindros, Stats MPG)", "# Req 23\npipeline = " + json.dumps(q23_p, indent=2), "cars", q23_p))

    # Req 24
    q24_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$match": {"country_info.countryName": "germany"}}, {"$sort": {"horsepower": -1}}, {"$group": {"_id": None, "autos": {"$push": {"descr": "$descr", "hp": "$horsepower"}}}}, {"$unwind": {"path": "$autos", "includeArrayIndex": "Posición"}}, {"$limit": 5}, {"$project": {"_id": 0, "Posición": {"$add": ["$Posición", 1]}, "Descripción": "$autos.descr", "Potencia": "$autos.hp"}}]
    queries.append(QueryItem(24, "Ranking de potencia de autos alemanes (Top 5)", "# Req 24\npipeline = " + json.dumps(q24_p, indent=2), "cars", q24_p))

    # Req 25
    q25_p = [{"$match": {"activo": True}}] + lookup_maker_country_cont + [{"$match": {"cont_info.continent": "europe"}}, {"$sort": {"mpg": -1}}, {"$group": {"_id": "$maker_info.fullName", "AutoEficiente": {"$first": "$descr"}, "MaxMPG": {"$first": "$mpg"}}}, {"$project": {"_id": 0, "Fabricante Europeo": "$_id", "Auto Más Eficiente": "$AutoEficiente", "MPG": "$MaxMPG"}}]
    queries.append(QueryItem(25, "Auto más eficiente por fabricante europeo", "# Req 25\npipeline = " + json.dumps(q25_p, indent=2), "cars", q25_p))

    return queries