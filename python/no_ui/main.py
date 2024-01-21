from tkinter import Tk
from tkinter.filedialog import askdirectory
from time import sleep
import re as regex
import os,string

folder_escribir = None
type_ = None
drive = None
file_extension = ['jpg', 'png', 'pdf']
first_file_signature = {'jpg':b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', 'png':'', 'pdf':''}
last_file_signature = {'jpg': b'\xff\xd9', 'png':'', 'pdf':''}
drives = ['%s:'%d for d in string.ascii_uppercase if os.path.exists('%s:'%d)]

def intro(Select_drive_recover:bool ,Select_drive_save: bool,Select_file:bool):

    while Select_drive_save:
        global folder_escribir
        print("Select the folder where you are going to save the recovered files.")
        sleep(3)
        try:
            folder_escribir = askdirectory(title = "Please select the directory where you want to save the recovered files")
            if folder_escribir == None: raise ValueError("You have not choosen the drive to develop the recovery")
        except ValueError as error:
            print("Unexpected error: " + str(error))
        else:
            Select_drive_save = False
            Select_drive_recover = True
            Select_file = False
            break

    while Select_drive_recover:
        for i,j in enumerate(drives):
            print(i + 1, ' : ', j)
        global drive
        drive = int(input("Please select the drive where you want to apply the recovery: "))
        if drive not in range(1,4,1):
            print("fuera de rango")
            continue
        else:
            Select_drive_save = False
            Select_file = True
            Select_drive_recover = False
            break

    while Select_file:
        for i,j in enumerate(file_extension):
            print(i + 1, ':' , j)
        try:
            global type_     
            type_ = int(input('Please select the file type you want to recover: ')) 
        except ValueError:
            print("Debe ingresar un valor numérico")
            intro(Select=True)
        else: 
            if type_ not in range(1,4,1):
                print("Usted ha ingresado un valor que no está en el rango predefinido")
            else:
                Select_file = False
                Select_drive_recover = False
                Select_drive_save = False
                break
    recover()


def recover():
    log_file_handle = open("Log.txt", "w")
    counter_coincidencia = 0
    counter_file = 0
    pattern_beginning = first_file_signature[file_extension[type_-1]]
    pattern_end = last_file_signature[file_extension[type_-1]]
    drive_open = f"\\\\.\\{drives[drive-1]}"
    string =True
    with open(drive_open, "rb") as recover:
        while string:
            string = recover.read(512)
            find = regex.search(pattern_beginning, string, regex.IGNORECASE)
            log_file_handle.write("coincidencia: "+ str(counter_coincidencia) + ' = ' +str(find) + "\n")
            counter_coincidencia += 1
            if find: 
                print("→" * 15 + 'Archivo encontrado' +'←' * 15)
                print(f"Guardado como {counter_file}.{file_extension[type_-1]}")
                saving = True
                with open(f"{folder_escribir}/{counter_file}.{file_extension[type_-1]}", "wb") as recovered_file:
                    recovered_file.write(string[find.start():])
                    while saving:
                        string = recover.read(512)
                        coincidence = regex.search(pattern_end, string, regex.IGNORECASE)
                        if not coincidence:
                            recovered_file.write(string)
                        else:
                            recovered_file.write(string[:coincidence.start()] + pattern_end)
                            saving = False
                            break
                counter_file += 1
    log_file_handle.close()

if __name__ == "__main__":
    intro(Select_drive_recover=False, Select_drive_save=True, Select_file= False)