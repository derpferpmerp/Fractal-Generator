TITLE = "The Carpet Fractal"
MAPNUM = 0
IMGPATH = "./EQ.png" # Path to the Image
DAT_PATH = "mapped.py" # Path to Mapped.Py


# Run This Command To Generate the Data File
print("python3 mapped.py {0} {1}".format(IMGPATH, MAPNUM))

FILLED_MAP_DESC = """
/give @s filled_map{display:{Name:'{"text":"__@@__","color":"dark_red","bold":true,"underlined":true}',Lore:['{"text":"Coded By Cole Fleming","bold":true,"italic":true}']},map:__!!__} 1
""".replace("__@@__", TITLE).replace("__!!__", str(MAPNUM))
print(FILLED_MAP_DESC)
