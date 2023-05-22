import os
import sys
from pathlib import Path
from process import setup

from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
import json

from PIL import Image
from io import BytesIO
import base64


from code import lol



class JsonDatabase():
    name = "database"


    DATABASE_SRC = str(Path(os.getcwd()).parent.absolute()) + "/frontend" + "/public"

    path = f"{DATABASE_SRC}/{name}.json"
    def getImageById(self,id):
        f = open(self.path)
        data = json.load(f)
        img = data[str(id)]
        f.close()
        return img

    def reWriteNote(self,id, note):
        f = open(self.path)
        data = json.load(f)
        img = data[str(id)]
        img['notes'] = note
        data[str(id)] = img
        f.close()
        json_object = json.dumps(data, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_object)

    def removeImage(self,id):
        f = open(self.path)
        data = json.load(f)
        data.pop(str(id))
        f.close()
        json_object = json.dumps(data, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_object)

    def highlightImage(self,id):
        f = open(self.path)
        data = json.load(f)
        img = data[str(id)]
        img['highlighted'] = True
        data[str(id)] = img
        f.close()
        json_object = json.dumps(data, indent=4)
        with open(self.path, "w") as outfile:
            outfile.write(json_object)


    def getDatabase(self):
        f = open(self.path)
        print(f)
        data = json.load(f)
        data = json.dumps(data)
        f.close()
        return data
    def insertToDatabase(self, image):
        data = None

        try:
            f = open(self.path)
            data = json.load(f)
            data[str(image["image_id"])] = image
            f.close()
            json_object = json.dumps(data, indent=4)
            with open(self.path, "w") as outfile:
                outfile.write(json_object)

        except:
            data = {image["image_id"]:image}
            json_object = json.dumps(data, indent=4)
            with open(self.path,'w') as outfile:
                outfile.write(json_object)




class ImageInfoView(APIView):
    database = JsonDatabase()
    def post(self, request):
        print(lol())
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            img = self.database.getImageById(request.data["image_id"])
            return Response(img)




class DeleteImageView(APIView):
    def post(self, request):
        database = JsonDatabase()
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            database.removeImage(request.data['image_id'])
            return Response("d")

class HighlightImageView(APIView):
    database = JsonDatabase()
    def post(self, request):
        database = JsonDatabase()
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            database.highlightImage(request.data['image_id'])
            return Response("d")



class ReWriteNote(APIView):
    database = JsonDatabase()

    def post(self, request):
        database = JsonDatabase()
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            database.reWriteNote(
                id = request.data['image_id'],
                note = request.data['note']
            )
            return Response("d")

class ImageServiceView(APIView):

    database = JsonDatabase()



    def get(self, request):
        data = [self.database.getDatabase()]
        return Response(data)

    def createDir(self):
        try:
            path = Path(os.getcwd())
            img_storage = str(path.parent.absolute()) + "/hacaton-app"
            os.mkdir(os.path.join(img_storage, "first"))
            os.mkdir(os.path.join(img_storage+'/first', "second"))
            print(img_storage+'/first')
            return [img_storage+'/first',img_storage+'/first/second']
        except:
            pass

    def post(self, request):

        path = Path(os.getcwd())

        img_storage = str(path.parent.absolute()) + "/frontend" + "/public" + "/images"

        print(img_storage)

        serializer = SendImageSerializer(data=request.data)

        print(os.getcwd())

        print(request.data['image_id'])
        image_data = base64.b64decode(request.data['src'].split(',')[1])
        with open(f"{request.data['image_id']}.png", "wb") as f:
            f.write(image_data)


        if serializer.is_valid(raise_exception=True):

            current_image = f"{request.data['image_id']}.png"
            self.createDir()
            l1 = str(path.parent.absolute())+'/first/'
            l2 = str(path.parent.absolute())+'/first/second'

            res = setup(current_image, l2, l1, str(path.parent.absolute()) + "/frontend" + "/public" + "/images" + f"/{request.data['image_id']}.jpeg")
            info = res


            img = {
                    "image_id": request.data['image_id'],
                    # "file_src":request.data['src'],
                    "swans_count": info['Total'],
                    "shipuns_count": info['shipun'],
                    "clikuns_count": info['klikun'],
                    "small_count": info['maliy'],
                    "unrecognized_count": info['Total'] - info['shipun'] - info['maliy'] - info['klikun'],
                    "name": "wedfg",
                    "date": "12.02.2002",
                    "highlighted": False,
                    "notes": "",
                    "process": 2 if info['Total'] <= 0 else 1 if (info['Total'] - info['shipun'] - info['maliy'] - info['klikun']) != 0 else 0
                }
            self.database.insertToDatabase(img)
            return Response(img)

class UploadImageView():
    def post(self, request):
        serializer = UploadimageSerializer(data=request.data)
        path = Path(os.getcwd())
        if serializer.is_valid(raise_exception=True):

            return Response("img")