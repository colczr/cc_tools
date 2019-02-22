import cc_dat_utils
import json
import cc_data

in_json = "data/tianyinc_cc1.json"

#open and read json file
with open(in_json, "r") as reader:
    json_data = json.load(reader)

#convert json into cc file
def make_cc_data_file_from_json(json_data):
    data_file = cc_data.CCDataFile()
    #assign data from json to cc data file
    for level_data in json_data["levels"]:
        cc_level = cc_data.CCLevel()
        cc_level.level_number = level_data["level_no"]
        cc_level.num_chips = level_data["chips"]
        cc_level.time = level_data["time"]
        cc_level.upper_layer = level_data["upper"]
        cc_level.lower_layer = level_data["lower"]
        #handle optional fields
        optional_fields = level_data["optional fields"]
        for field_data in optional_fields:
            field_type = field_data["type"]
            if field_type == "title":
                cc_title = cc_data.CCMapTitleField(field_data["title"])
                cc_level.add_field(cc_title)
            elif field_type == "pw":
                cc_password = cc_data.CCEncodedPasswordField(field_data["pw"])
                cc_level.add_field(cc_password)
            elif field_type == "hint":
                cc_hint = cc_data.CCMapHintField(field_data["hint"])
                cc_level.add_field(cc_hint)
            elif field_type == "monster":
                cc_monster_position = []
                #monster coordinate takes a list, make list to pass
                for position in field_data["monster"]:
                    cc_monster_position.append(cc_data.CCCoordinate(position["x"], position["y"]))
                cc_monster = cc_data.CCMonsterMovementField(cc_monster_position)
                cc_level.add_field(cc_monster)

        data_file.add_level(cc_level)
        print(cc_level)

    return data_file

game_data = make_cc_data_file_from_json(json_data)
#write dat file from cc file
cc_dat_utils.write_cc_data_to_dat(game_data, "data/tianyinc_cc1.dat")

