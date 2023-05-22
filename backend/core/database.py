import json
import os


class JsonDatabase():
    name = "database"

    def getDatabase(self):
        f = open(f'{self.name}.json')
        data = json.load(f)
        f.close()
        return data
    def insertToDatabase(self, image):
        data = None
        print(1)
        print(os.getcwd())
        try:
            f = open(f'{self.name}.json')
            data = json.load(f)
            data[str(image["image_id"])] = image
            f.close()
            json_object = json.dumps(data, indent=4)
            with open(f"{self.name}.json", "w") as outfile:
                outfile.write(json_object)

        except:
            data = {image["image_id"]:image}
            json_object = json.dumps(data, indent=4)
            print(1)
            print(os.getcwd())
            outfile = open(f"{self.name}.json", "w")
            outfile.write(json_object)



