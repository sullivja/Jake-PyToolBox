import arcpy
import os
import datetime
import string
import re

class Toolbox(object):
    def __init__(self):

        self.label = "Toolbox"
        self.alias = "Jake's Toolbox"
        # List of tool classes associated with this toolbox
        self.tools = [Bulk_Text_Replace]


class Bulk_Text_Replace(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Bulk Layout Text Replace"
        self.alias = " Jake's Toolbox Alias Property True"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(0)
        param0.name = "Parameter0"
        param0.displayName = "Target Folder:"
        param0.parameterType = "Required"
        param0.direction = "Input"
        param0.datatype = "Folder"

        param1 = arcpy.Parameter(1)
        param1.name = "Parameter1"
        param1.displayName = "Old String?:"
        param1.parameterType = "Required"
        param1.direction = "Input"
        param1.datatype = "String"

        param2 = arcpy.Parameter(2)
        param2.name = "Parameter2"
        param2.displayName = "New String?:"
        param2.parameterType = "Required"
        param2.direction = "Input"
        param2.datatype = "String"

        param3 = arcpy.Parameter(3)
        param3.name = "Parameter3"
        param3.displayName = "Case Sensative?"
        param3.parameterType = "Optional"
        param3.direction = "Input"
        param3.datatype = "Boolean"

        param4 = arcpy.Parameter(4)
        param4.name = "Parameter4"
        param4.displayName = "Exact Phrase?"
        param4.parameterType = "Optional"
        param4.direction = "Input"
        param4.datatype = "Boolean"

        param5 = arcpy.Parameter(5)
        param5.name = "Parameter5"
        param5.displayName = "Create PDF?:"
        param5.parameterType = "Optional"
        param5.direction = "Input"
        param5.datatype = "Boolean"

        return[param0,param1,param2,param3,param4,param5]

        
    def execute(self, parameters, messages):

        input_folder = parameters[0].ValueAsText
        input_folder = input_folder+"\\"
        output_folder = (input_folder+"\\local_temp\\")
        pdf_folder = output_folder
        old_string = parameters[1].ValueAsText
        new_string = parameters[2].ValueAsText
        case = parameters[3].Value
        exact = parameters[4].Value
        make_pdf = parameters[5].Value

        strcase = str(case)
        strexact = str(exact)
        
        messages.addMessage("case is "+strcase)
        messages.addMessage("exact is "+strexact)
        messages.addMessage("New String is "+new_string)

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
                    #mxd.saveACopy(output_folder + mapvar)
                    if os.path.isdir(output_folder) == True:
                        print("yup,that folder is there")
                    else:
                        os.makedirs(output_folder)
                        print("gotta make that folder")

                    mxd.save()
                    if make_pdf:
                        arcpy.mapping.ExportToPDF(mxd, (pdf_folder+mapvar), "PAGE_LAYOUT", 640, 480, 300, "BEST", "RGB", "False", "ADAPTIVE", "VECTORIZE_BITMAP", "False", "True", "LAYERS_ONLY", "True", 90)
                else:
                    print("No Changes were made to "+ mapvar)
                del mxd

            except:
                print("oops")
