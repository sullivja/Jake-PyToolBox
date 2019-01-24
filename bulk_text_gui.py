import arcpy
import os
import string
import re

input_folder = r"C:\\Users\\Jacob\Desktop\\Learning\\GIS\\Arcpy Data\\Bulk Text Change\\Dummy Maps"
input_folder = input_folder+"\\"
output_folder = (input_folder+"\\local_temp\\")
pdf_folder = output_folder
old_string = "Old String"
new_string = "New String"
make_pdf = True
case = False
exact = False

def bulk_change_text():
#creates a list of all mxd files within input folder
    if os.path.isdir(output_folder) == True:
        print("yup,that folder is there")
    else:
        os.makedirs(output_folder)
        print("gotta make that folder")

    file_list = []
    for file in os.listdir(input_folder):
        if file.endswith(".mxd"):
            file_list.append(file)

    for mapvar in file_list:

        print("inspecting "+mapvar+"...")

        try:

            change = False

            #Referent the map document
            mxd = arcpy.mapping.MapDocument(input_folder+mapvar)        

            #Find all page layout text elements
            for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):     
                if exact:
                    if case:
                        if old_string == elm.text:
                            change = True
                            elmText = elm.text.replace(old_string, new_string)
                            elm.text = elmText
                    else:
                        if old_string.upper() == elm.text.upper():
                            change = True
                            insensitive_string = re.compile(re.escape(old_string), re.IGNORECASE)
                            strelm= str(elm.text)
                            elm.text = (insensitive_string.sub(new_string, strelm))    
                else:
                    if case:
                        if old_string in elm.text:
                            change = True
                            elmText = elm.text.replace(old_string, new_string)
                            elm.text = elmText
                    else:
                        if old_string.upper() in elm.text.upper():
                            change = True
                            insensitive_string = re.compile(re.escape(old_string), re.IGNORECASE)
                            strelm= str(elm.text)
                            elm.text = (insensitive_string.sub(new_string, strelm)) 

            if change:
                mxd.saveACopy(output_folder + mapvar)
                if make_pdf:
                    arcpy.mapping.ExportToPDF(mxd, (pdf_folder+mapvar), "PAGE_LAYOUT", 640, 480, 300, "BEST", "RGB", "False", "ADAPTIVE", "VECTORIZE_BITMAP", "False", "True", "LAYERS_ONLY", "True", 90)
            else:
                print("No Changes were made to "+ mapvar)
            del mxd

        except:
            print("oops")

bulk_change_text()



