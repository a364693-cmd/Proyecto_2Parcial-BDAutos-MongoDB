import pymongo

def init_database():
    # Conexión al servidor local de MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    
    # Reiniciar la base de datos 'BDAutos' 
    client.drop_database("BDAutos")
    db = client["BDAutos"]

    print("Inicializando la base de datos BDAutos en MongoDB...")

    # continents (Linking)
    continents_data = [
        {"_id": 1, "continent": "america", "activo": True},
        {"_id": 2, "continent": "europe", "activo": True},
        {"_id": 3, "continent": "asia", "activo": True},
        {"_id": 4, "continent": "africa", "activo": True},
        {"_id": 5, "continent": "australia", "activo": True}
    ]
    db.continents.insert_many(continents_data)

    # countries (Linking con continents)
    countries_raw = [
        (1, 'usa', 1), (2, 'germany', 2), (3, 'france', 2), (4, 'japan', 3),
        (5, 'italy', 2), (6, 'sweden', 2), (7, 'uk', 2), (8, 'korea', 3),
        (9, 'russia', 2), (10, 'nigeria', 4), (11, 'australia', 5),
        (12, 'new zealand', 5), (13, 'egypt', 4), (14, 'mexico', 1),
        (15, 'brazil', 1), (16, 'china', 3), (17, 'netherlands', 2)
    ]
    countries_data = [
        {"_id": c[0], "countryName": c[1], "contID": c[2], "activo": True}
        for c in countries_raw
    ]
    db.countries.insert_many(countries_data)

    # makers (Embedding con Model_Details)

    makers_raw = [
        (1, 'gm', 'General Motors', 1), (2, 'ford', 'Ford Motor Company', 1),
        (3, 'stellantis', 'Stellantis N.V.', 17), (4, 'toyota', 'Toyota Motor Corporation', 4),
        (5, 'honda', 'Honda Motor Co.', 4), (6, 'nissan', 'Nissan Motor Co.', 4),
        (7, 'mazda', 'Mazda Motor Corporation', 4), (8, 'subaru', 'Subaru Corporation', 4),
        (9, 'mitsubishi', 'Mitsubishi Motors', 4), (10, 'suzuki', 'Suzuki Motor Corporation', 4),
        (11, 'hyundai', 'Hyundai Motor Group', 8), (12, 'volkswagen', 'Volkswagen Group', 2),
        (13, 'bmw', 'BMW Group', 2), (14, 'mercedes-benz', 'Mercedes-Benz Group', 2),
        (15, 'renault', 'Renault Group', 3), (16, 'volvo', 'Volvo Cars', 6),
        (17, 'jlr', 'Jaguar Land Rover', 7), (18, 'ferrari', 'Ferrari N.V.', 5),
        (19, 'saic', 'SAIC Motor', 16), (20, 'chery', 'Chery Automobile', 16)
    ]

    models_raw = [
        (1, 1, 'chevrolet'), (2, 1, 'gmc'), (3, 1, 'cadillac'), (4, 1, 'buick'),
        (5, 2, 'ford'), (6, 2, 'lincoln'), (7, 3, 'jeep'), (8, 3, 'dodge'),
        (9, 3, 'ram'), (10, 3, 'chrysler'), (11, 3, 'fiat'), (12, 3, 'peugeot'),
        (13, 3, 'alfa romeo'), (14, 4, 'toyota'), (15, 4, 'lexus'), (16, 5, 'honda'),
        (17, 5, 'acura'), (18, 6, 'nissan'), (19, 6, 'infiniti'), (20, 7, 'mazda'),
        (21, 8, 'subaru'), (22, 9, 'mitsubishi'), (23, 10, 'suzuki'), (24, 11, 'hyundai'),
        (25, 11, 'kia'), (26, 11, 'genesis'), (27, 12, 'volkswagen'), (28, 12, 'audi'),
        (29, 12, 'porsche'), (30, 12, 'lamborghini'), (31, 12, 'bentley'), (32, 13, 'bmw'),
        (33, 13, 'mini'), (34, 14, 'mercedes-benz'), (35, 15, 'renault'), (36, 15, 'dacia'),
        (37, 16, 'volvo'), (38, 17, 'land rover'), (39, 17, 'jaguar'), (40, 18, 'ferrari'),
        (41, 19, 'mg'), (42, 20, 'chery')
    ]

    makers_dict = {}
    for m in makers_raw:
        makers_dict[m[0]] = {
            "_id": m[0],
            "maker": m[1],
            "fullName": m[2],
            "countryID": m[3],
            "models": [],
            "activo": True
        }

    for md in models_raw:
        makers_dict[md[1]]["models"].append({"modelID": md[0], "model": md[2]})

    db.makers.insert_many(list(makers_dict.values()))

    # cars (Embedding de Car_Names + Car_Details)
    
    car_names_raw = [
        (1, 1, 'chevrolet silverado 1500 lt 5.3'), (2, 1, 'chevrolet tahoe lt 5.3'),
        (3, 1, 'chevrolet equinox lt 1.5t'), (4, 1, 'chevrolet trax 1rs 1.2t'),
        (5, 1, 'chevrolet malibu lt 1.5t'), (6, 1, 'chevrolet corvette stingray 6.2'),
        (7, 1, 'chevrolet camaro ss 6.2'), (8, 1, 'chevrolet colorado z71 2.7t'),
        (9, 2, 'gmc sierra 1500 denali 6.2'), (10, 2, 'gmc yukon denali 6.2'),
        (11, 2, 'gmc terrain sle 1.5t'), (12, 3, 'cadillac escalade 6.2'),
        (13, 3, 'cadillac ct5-v blackwing 6.2'), (14, 3, 'cadillac xt5 premium luxury 2.0t'),
        (15, 4, 'buick envista 1.2t'), (16, 4, 'buick enclave 2.5t'),
        (17, 5, 'ford f-150 xlt 2.7 ecoboost'), (18, 5, 'ford f-150 raptor 3.5'),
        (19, 5, 'ford mustang gt 5.0'), (20, 5, 'ford mustang ecoboost 2.3'),
        (21, 5, 'ford bronco sport big bend 1.5t'), (22, 5, 'ford bronco badlands 2.7'),
        (23, 5, 'ford ranger lariat 2.3'), (24, 5, 'ford explorer st 3.0'),
        (25, 5, 'ford escape st-line 1.5t'), (26, 5, 'ford maverick xlt hybrid 2.5'),
        (27, 6, 'lincoln navigator 3.5'), (28, 6, 'lincoln aviator 3.0'),
        (29, 7, 'jeep wrangler rubicon 3.6'), (30, 7, 'jeep grand cherokee limited 3.6'),
        (31, 7, 'jeep compass latitude 2.0t'), (32, 7, 'jeep gladiator sport 3.6'),
        (33, 8, 'dodge durango r/t 5.7'), (34, 8, 'dodge charger scat pack 6.4'),
        (35, 8, 'dodge challenger srt hellcat 6.2'), (36, 8, 'dodge hornet gt 2.0t'),
        (37, 9, 'ram 1500 laramie 3.0 hurricane'), (38, 10, 'chrysler pacifica touring l 3.6'),
        (39, 11, 'fiat 500x sport 1.3t'), (40, 12, 'peugeot 2008 gt 1.2t'),
        (41, 12, 'peugeot 3008 gt 1.6t'), (42, 13, 'alfa romeo giulia 2.0t'),
        (43, 13, 'alfa romeo stelvio quadrifoglio 2.9'), (44, 14, 'toyota corolla le 2.0'),
        (45, 14, 'toyota corolla hybrid le 1.8'), (46, 14, 'toyota camry le hybrid 2.5'),
        (47, 14, 'toyota rav4 xle 2.5'), (48, 14, 'toyota rav4 hybrid xle 2.5'),
        (49, 14, 'toyota tacoma trd off-road 2.4t'), (50, 14, 'toyota tundra limited 3.4'),
        (51, 14, 'toyota 4runner sr5 2.4t'), (52, 14, 'toyota gr86 2.4'),
        (53, 14, 'toyota gr supra 3.0'), (54, 14, 'toyota hilux 2.7'),
        (55, 15, 'lexus rx 350 2.4t'), (56, 15, 'lexus es 300h 2.5'),
        (57, 15, 'lexus lx 600 3.4'), (58, 16, 'honda civic ex 1.5t'),
        (59, 16, 'honda civic type r 2.0t'), (60, 16, 'honda accord hybrid touring 2.0'),
        (61, 16, 'honda cr-v ex 1.5t'), (62, 16, 'honda hr-v lx 2.0'),
        (63, 16, 'honda pilot trailsport 3.5'), (64, 17, 'acura integra a-spec 1.5t'),
        (65, 17, 'acura mdx 3.5'), (66, 18, 'nissan versa sr 1.6'),
        (67, 18, 'nissan sentra sv 2.0'), (68, 18, 'nissan kicks sr 2.0'),
        (69, 18, 'nissan rogue sv 1.5t'), (70, 18, 'nissan frontier pro-4x 3.8'),
        (71, 18, 'nissan z performance 3.0'), (72, 18, 'nissan np300 2.5'),
        (73, 19, 'infiniti qx60 2.0t'), (74, 20, 'mazda 3 hatchback 2.5 s'),
        (75, 20, 'mazda cx-5 2.5 s'), (76, 20, 'mazda cx-50 2.5 turbo'),
        (77, 20, 'mazda cx-90 3.3 turbo'), (78, 20, 'mazda mx-5 miata 2.0'),
        (79, 21, 'subaru outback 2.5'), (80, 21, 'subaru wrx 2.4t'),
        (81, 21, 'subaru forester 2.5'), (82, 21, 'subaru crosstrek 2.5'),
        (83, 22, 'mitsubishi outlander se 2.5'), (84, 22, 'mitsubishi mirage g4 1.2'),
        (85, 22, 'mitsubishi l200 2.4'), (86, 23, 'suzuki swift 1.2'),
        (87, 23, 'suzuki vitara 1.4t'), (88, 23, 'suzuki jimny 1.5'),
        (89, 24, 'hyundai elantra sel 2.0'), (90, 24, 'hyundai elantra n 2.0t'),
        (91, 24, 'hyundai tucson sel 2.5'), (92, 24, 'hyundai santa fe 2.5t'),
        (93, 24, 'hyundai palisade 3.8'), (94, 24, 'hyundai creta 1.5'),
        (95, 25, 'kia forte lxs 2.0'), (96, 25, 'kia sportage lx 2.5'),
        (97, 25, 'kia telluride sx 3.8'), (98, 25, 'kia k5 gt 2.5t'),
        (99, 25, 'kia sorento 2.5'), (100, 26, 'genesis g70 3.3t'),
        (101, 26, 'genesis gv80 2.5t'), (102, 27, 'volkswagen jetta se 1.5t'),
        (103, 27, 'volkswagen golf gti 2.0t'), (104, 27, 'volkswagen golf r 2.0t'),
        (105, 27, 'volkswagen tiguan se 2.0t'), (106, 27, 'volkswagen atlas 2.0t'),
        (107, 27, 'volkswagen taos s 1.5t'), (108, 28, 'audi a4 45 tfsi 2.0t'),
        (109, 28, 'audi q5 45 tfsi 2.0t'), (110, 28, 'audi rs 6 avant 4.0'),
        (111, 29, 'porsche 911 carrera 3.0'), (112, 29, 'porsche cayenne 3.0'),
        (113, 29, 'porsche macan t 2.0t'), (114, 32, 'bmw 330i 2.0t'),
        (115, 32, 'bmw m3 competition 3.0'), (116, 32, 'bmw x3 xdrive30i 2.0t'),
        (117, 32, 'bmw x5 xdrive40i 3.0'), (118, 33, 'mini cooper s 2.0t'),
        (119, 34, 'mercedes-benz c 300 2.0t'), (120, 34, 'mercedes-benz e 350 2.0t'),
        (121, 34, 'mercedes-benz glc 300 2.0t'), (122, 34, 'mercedes-benz amg g 63 4.0'),
        (123, 35, 'renault duster 1.6'), (124, 35, 'renault kardian 1.0t'),
        (125, 37, 'volvo xc60 b5 2.0t'), (126, 37, 'volvo xc90 b6 2.0t'),
        (127, 37, 'volvo s60 b5 2.0t'), (128, 38, 'land rover defender 110 3.0'),
        (129, 38, 'land rover range rover sport 3.0'), (130, 39, 'jaguar f-pace p250 2.0t'),
        (131, 39, 'jaguar f-type r 5.0'), (132, 40, 'ferrari roma 3.9'),
        (133, 40, 'ferrari 812 competizione 6.5'), (134, 41, 'mg zs 1.5'),
        (135, 41, 'mg 5 1.5'), (136, 41, 'mg hs 1.5t'),
        (137, 42, 'chery tiggo 4 pro 1.5'), (138, 42, 'chery tiggo 7 pro 1.5t')
    ]

    car_details_raw = [
        (1, 18, 8, 325, 355, 5100, 6.7, 2024), (2, 17, 8, 325, 355, 5600, 7.0, 2024),
        (3, 26, 4, 91, 175, 3600, 8.5, 2025), (4, 30, 3, 73, 137, 3100, 9.0, 2025),
        (5, 32, 4, 91, 160, 3150, 8.0, 2024), (6, 19, 8, 376, 495, 3650, 2.9, 2025),
        (7, 19, 8, 376, 455, 3685, 4.0, 2024), (8, 19, 4, 165, 310, 4500, 6.5, 2025),
        (9, 17, 8, 376, 420, 5600, 5.9, 2024), (10, 16, 8, 376, 420, 5900, 6.1, 2025),
        (11, 26, 4, 91, 175, 3500, 9.1, 2024), (12, 16, 8, 376, 420, 5900, 5.9, 2024),
        (13, 15, 8, 376, 668, 4125, 3.6, 2024), (14, 24, 4, 122, 235, 4200, 7.3, 2024),
        (15, 30, 3, 73, 137, 3100, 9.2, 2025), (16, 22, 4, 152, 328, 4650, 6.5, 2025),
        (17, 21, 6, 165, 325, 4700, 6.3, 2024), (18, 16, 6, 214, 450, 5700, 5.4, 2024),
        (19, 18, 8, 307, 480, 3900, 4.2, 2024), (20, 25, 4, 140, 315, 3550, 5.3, 2024),
        (21, 26, 3, 91, 180, 3500, 8.8, 2024), (22, 17, 6, 165, 330, 4750, 6.4, 2024),
        (23, 21, 4, 140, 270, 4400, 6.8, 2024), (24, 20, 6, 183, 400, 4700, 5.2, 2025),
        (25, 30, 3, 91, 180, 3500, 8.3, 2025), (26, 37, 4, 152, 191, 3700, 7.7, 2024),
        (27, 18, 6, 214, 440, 5900, 6.0, 2024), (28, 21, 6, 183, 400, 4900, 5.6, 2024),
        (29, 19, 6, 220, 285, 4500, 7.0, 2024), (30, 22, 6, 220, 293, 4600, 7.5, 2024),
        (31, 25, 4, 122, 200, 3600, 7.5, 2024), (32, 19, 6, 220, 285, 4900, 7.5, 2024),
        (33, 17, 8, 348, 360, 5250, 6.2, 2024), (34, 18, 8, 392, 485, 4300, 4.3, 2023),
        (35, 16, 8, 376, 717, 4450, 3.6, 2023), (36, 24, 4, 122, 268, 3700, 6.5, 2024),
        (37, 20, 6, 183, 420, 5300, 5.8, 2025), (38, 22, 6, 220, 287, 4500, 7.4, 2024),
        (39, 27, 4, 79, 177, 3300, 8.2, 2023), (40, 40, 3, 73, 130, 2800, 8.7, 2024),
        (41, 32, 4, 98, 165, 3200, 8.5, 2024), (42, 27, 4, 122, 280, 3500, 5.5, 2024),
        (43, 19, 6, 177, 505, 4400, 3.6, 2024), (44, 35, 4, 122, 169, 3100, 8.3, 2024),
        (45, 50, 4, 110, 138, 3150, 9.0, 2024), (46, 51, 4, 152, 225, 3500, 7.2, 2025),
        (47, 30, 4, 152, 203, 3500, 8.0, 2024), (48, 40, 4, 152, 219, 3800, 7.5, 2024),
        (49, 20, 4, 146, 278, 4500, 7.0, 2024), (50, 20, 6, 210, 389, 5600, 6.0, 2024),
        (51, 20, 4, 146, 278, 4700, 7.5, 2025), (52, 22, 4, 146, 228, 2811, 6.1, 2024),
        (53, 26, 6, 183, 382, 3400, 3.9, 2024), (54, 24, 4, 165, 166, 4200, 11.5, 2024),
        (55, 24, 4, 146, 275, 4300, 7.2, 2024), (56, 44, 4, 152, 215, 3700, 8.0, 2024),
        (57, 19, 6, 210, 409, 5900, 6.8, 2024), (58, 36, 4, 91, 180, 3000, 7.4, 2024),
        (59, 24, 4, 122, 315, 3200, 5.0, 2024), (60, 44, 4, 122, 204, 3500, 6.9, 2024),
        (61, 30, 4, 91, 190, 3500, 8.4, 2024), (62, 28, 4, 122, 158, 3100, 9.5, 2024),
        (63, 20, 6, 214, 285, 4500, 7.0, 2024), (64, 33, 4, 91, 200, 3100, 7.0, 2024),
        (65, 22, 6, 214, 290, 4400, 6.5, 2024), (66, 35, 4, 98, 122, 2700, 9.5, 2024),
        (67, 34, 4, 122, 149, 3050, 8.7, 2024), (68, 31, 4, 122, 141, 3100, 9.5, 2025),
        (69, 33, 3, 91, 201, 3500, 7.8, 2024), (70, 19, 6, 232, 310, 4600, 6.8, 2024),
        (71, 22, 6, 183, 400, 3500, 4.3, 2024), (72, 23, 4, 152, 164, 4000, 11.0, 2024),
        (73, 25, 4, 122, 268, 4600, 7.0, 2025), (74, 31, 4, 152, 191, 3100, 7.5, 2024),
        (75, 26, 4, 152, 187, 3600, 8.2, 2024), (76, 25, 4, 152, 256, 3900, 6.6, 2024),
        (77, 25, 6, 201, 280, 4600, 6.8, 2024), (78, 30, 4, 122, 181, 2350, 5.7, 2024),
        (79, 29, 4, 152, 182, 3700, 8.8, 2024), (80, 22, 4, 146, 271, 3400, 5.5, 2024),
        (81, 29, 4, 152, 180, 3500, 8.5, 2025), (82, 29, 4, 152, 182, 3300, 8.5, 2024),
        (83, 26, 4, 152, 181, 3600, 8.6, 2024), (84, 39, 3, 73, 78, 2100, 11.5, 2024),
        (85, 22, 4, 146, 181, 4300, 10.5, 2024), (86, 44, 3, 73, 81, 2100, 12.0, 2024),
        (87, 36, 4, 85, 138, 2750, 9.5, 2024), (88, 34, 4, 91, 101, 2500, 12.0, 2024),
        (89, 36, 4, 122, 147, 2900, 8.5, 2024), (90, 25, 4, 122, 276, 3200, 5.3, 2024),
        (91, 28, 4, 152, 187, 3500, 8.6, 2024), (92, 24, 4, 152, 277, 4200, 6.5, 2024),
        (93, 22, 6, 232, 291, 4300, 7.2, 2024), (94, 35, 4, 91, 113, 2700, 11.5, 2024),
        (95, 34, 4, 122, 147, 2900, 8.6, 2024), (96, 28, 4, 152, 187, 3500, 8.6, 2024),
        (97, 23, 6, 232, 291, 4400, 7.1, 2024), (98, 27, 4, 152, 290, 3500, 5.5, 2024),
        (99, 26, 4, 152, 191, 3900, 9.0, 2024), (100, 20, 6, 201, 365, 3900, 4.5, 2024),
        (101, 22, 4, 152, 300, 4700, 6.0, 2024), (102, 35, 4, 91, 158, 3100, 8.0, 2024),
        (103, 28, 4, 122, 241, 3200, 5.9, 2024), (104, 25, 4, 122, 315, 3500, 4.5, 2024),
        (105, 26, 4, 122, 184, 3800, 8.5, 2024), (106, 22, 4, 122, 269, 4500, 7.0, 2024),
        (107, 31, 4, 91, 158, 3200, 7.9, 2024), (108, 27, 4, 122, 261, 3700, 5.2, 2024),
        (109, 25, 4, 122, 261, 4100, 5.7, 2024), (110, 17, 8, 244, 591, 4600, 3.5, 2024),
        (111, 21, 6, 183, 379, 3350, 3.9, 2024), (112, 21, 6, 183, 348, 4600, 5.7, 2024),
        (113, 21, 4, 122, 261, 4100, 5.9, 2024), (114, 30, 4, 122, 255, 3600, 5.6, 2024),
        (115, 19, 6, 183, 503, 3900, 3.8, 2024), (116, 26, 4, 122, 255, 4200, 6.0, 2025),
        (117, 24, 6, 183, 375, 4900, 5.3, 2024), (118, 31, 4, 122, 201, 2900, 6.4, 2025),
        (119, 29, 4, 122, 255, 3800, 5.9, 2024), (120, 27, 4, 122, 255, 4100, 6.2, 2024),
        (121, 26, 4, 122, 255, 4300, 6.2, 2024), (122, 14, 8, 244, 577, 5800, 4.4, 2024),
        (123, 32, 4, 98, 113, 2600, 12.0, 2024), (124, 40, 3, 61, 99, 2600, 11.0, 2025),
        (125, 25, 4, 122, 247, 4200, 6.4, 2024), (126, 22, 4, 122, 295, 4700, 6.1, 2024),
        (127, 28, 4, 122, 247, 3700, 6.3, 2024), (128, 18, 6, 183, 395, 5100, 5.7, 2024),
        (129, 20, 6, 183, 355, 5000, 5.7, 2024), (130, 39, 4, 122, 246, 4100, 6.9, 2024),
        (131, 39, 8, 305, 575, 3900, 3.5, 2024), (132, 40, 8, 238, 612, 3460, 3.4, 2024),
        (133, 40, 12, 397, 819, 3600, 2.8, 2023), (134, 41, 4, 91, 106, 2900, 12.0, 2024),
        (135, 41, 4, 91, 111, 2700, 11.5, 2024), (136, 41, 4, 91, 168, 3400, 9.5, 2024),
        (137, 42, 4, 91, 113, 3000, 12.0, 2024), (138, 42, 4, 91, 154, 3300, 10.0, 2024)
    ]

    car_names_dict = {cn[0]: {"modelID": cn[1], "descr": cn[2]} for cn in car_names_raw}

    cars_data = []
    for cd in car_details_raw:
        car_id = cd[0]
        cn_info = car_names_dict[car_id]
        cars_data.append({
            "_id": car_id,
            "descr": cn_info["descr"],
            "modelID": cn_info["modelID"],
            "mpg": cd[1],
            "cylinders": cd[2],
            "edispl": cd[3],
            "horsepower": cd[4],
            "weight": cd[5],
            "accel": cd[6],
            "year": cd[7],
            "activo": True  # Borrado lógico activo por defecto
        })

    db.cars.insert_many(cars_data)

    print("¡Base de datos BDAutos creada y poblada exitosamente!")
    print(f"Continentes insertados: {db.continents.count_documents({})}")
    print(f"Países insertados:     {db.countries.count_documents({})}")
    print(f"Fabricantes insertados:{db.makers.count_documents({})}")
    print(f"Autos insertados:      {db.cars.count_documents({})}")

if __name__ == "__main__":
    init_database() 
