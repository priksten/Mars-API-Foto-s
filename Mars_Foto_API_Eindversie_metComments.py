# Allereerst een beschrijving van hoe dit programma is opgebouwd:
# 1. Wanneer je het programma opstart, dan wordt het hoofdvenster gemaakt. Vervolgens worden ook de twee frames gemaakt. 
#       Dat wil zeggen: het linkerframe met een aantal labels en de button 'show_button'
#                       het rechterframe met daarin een aantal labels, het frame dat de canvas bevat waarin foto's worden getoond en de knoppen 'button_previous' en 'button_next'
# 2. Bij het opstarten van het programma worden er ook meteen twee functies uitgevoerd. De eerste is de functie 'create_rover_frame': deze maakt de radiobuttons waarin je een rover 
#       naar keus kunt kiezen. Daarnaast zorgt deze functie ervoor dat het menu waarin je opties voor de curiosity-rover kunt kiezen, standaard wordt getoond.
# 3. Wanneer de gebruiker op een van de radiobuttons klikt, dan verandert het menu:
#       - curiosity: activeert de functie 'create_curiosity_frame'
#       - opportunity: activeert de functie 'create_opportunity_frame'
#       - spirit: ativeert de functie 'create_spirit_frame'
#       De verschillende menu-opties, zoals keuze voor camera en de kalender voor het selecteren van data wordt in deze functies door het aanroepen van andere functies gedaan.
#       Merk hierbij op dat in elk van deze functies een eigen zoek-knop wordt gemaakt met daaraan gekoppeld een eigen get_pictures() functie.
#       De reden hiervoor is dat voor iedere rover het API-verzoek naar een ander adres moet. 
# 4. De knop 'Toon foto's': deze knop is altijd zichtbaar. Als er bij het opstarten van het programma blijkt dat er al foto's staan 
#       in de map 'D:\Mars Foto API\Eindversie\Downloaded_Images', dan worden de eerste foto getoond als je op deze knop klikt. 
#       Als er nog geen foto's zijn in deze map, dan krijgt de gebruiker een melding dat er nog geen foto's zijn en dat hij eerst foto's moet downloaden.
#
# Het programma werkt via een handjevol grote belangrijke functies. Deze grote functies werken door ondersteunende functies:
# 1. create_rover_frame(): show_menu voor het tonen van het menu dat bij een specifieke Mars-rover hoort, gaat werken wanneer de gebruiker een radiobutton selecteert
# 2. show_menu(): create_curiosity_frame, create_opportunity_frame, create_spririt_frame (via bijvoorbeeld: create_search_button, choose_date_curiosity, choose_data_opportunity, choose_date_spirit)
# 3. get_pictures: deze functie doet op basis van de door de gebruiker ingevoerde rover en parameters een API-verzoek 
#       Vervolgens downloadt hij de foto's naar een hiervoor aangemaakte map (set_parameters_earth_date, create_pictures_directory, download_image)  
# 4. show_pictures: Toont een foto in het rechterframe en zorgt ervoor dat de hele set foto's op volgorde bekeken kan worden. 
#           make_folder_list, create_ctime_list, choose_newest_folder, create_header_info, update_picture_label, count_images, create_photo_list, get_image_dimensions, resize_image
# 5. Start_info: Zorgt ervoor dat de informatie van de laatst opgeslagen zoekopdracht in de header 
#           (onder de kop 'Afbeeldingen van Mars' zichtbaar is, en dat je kunt zien hoeveel foto's er in deze opdracht zijn gevonden (label tussen de knoppen 'Vorige' en 'Volgende')) 
#           gebruikte functies hierbij: make_folder_list, create_ctime_list, choose_newest_folder, create_header_info, update_picture_label, count_images, create_photo_list
# 6. load_previous, load_next: functies die maken dat de knoppen waarmee je door de foto's kunt klikken werken. 
#            Deze functies gebruiken: get_image_dimensions, resize_image, update_picture_label
# Merk dus op dat in dit programma de foto's allemaal herschaald worden zodat de breedte van de foto overal hetzelfde is, namelijk 600. De lengte wordt dan naar ratio hieraan aangepast. 
#
# Als je dit programma gebruikt, denk er dan om dat je een map aanmaakt waarin gedwonloade afbeeldingen kunnen worden geplaatst.
# Het pad naar deze map moet op verschillende plekken in de code worden ingevoerd:
#   1. create_pictures_directory (functie-definitie begint op regel 552, 'directory' in regel 562)
#   2. show_pictures(functie-definitie begint op regel 618, 'image_folder' in regel 626)
#   3. start_info(start op regel 698, 'directory' in regel 707 en 'image_folder' in regel 733)

# --------------------------------------------------------------------------------------------------------------------------------------
# We importeren alle modules die we voor dit programma nodig hebben
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from tkcalendar import Calendar
from datetime import date
import datetime
import os
from tkinter import *
from PIL import Image,ImageTk

import requests
import urllib.request
import os
import shutil

# Allereerst hieronder alle functies die we in het programma gebruiken. 
# Dit zijn circa 750 regels aan code. 
# De regels waarin daadwerkelijk is te vinden hoe het programma loopt, beginnen van regel 806.
def create_photo_list(n):
    """Deze functie maakt een lijst met elemnten van de vorm 'Photo_0', 'Photo_1', ... , 'Photo_n' """
    photo_list = []
    for i in range(0, n):
        name = str("photo_" + str(i))
        photo_list.append(name)
    
    return photo_list

def update_progress_label(pb):
    """Deze functie retourneert een string waarin te zien is hoe op hoeveel procent het proces van downloaden van foto's is"""
    return f"Current Progress: {int(pb['value'])}%"

# Functies ten behoeve van GUI
def create_search_button(container, com):
    """Deze functie maakt een zoek-knop en plaatst deze in 'frame' """
    search_button = ttk.Button(container, text = "Zoek foto's", command = com)
    search_button.grid()

def create_show_button(container, show):
    show_button = ttk.Button(container, text = "Toon foto's", command = show)
    show_button.grid()

def print_counters():
    print("Count Curiosity: " + str(count_curiosity))
    print("Count Opportunity: " + str(count_opportunity))
    print("Count Spirit: " + str(count_spirit))

def create_rover_frame(container):
    """Deze functie maakt het menu waarmee een Mars Rover kan worden gekozen"""
    global start_frame
    rover_label = ttk.Label(container, text = "Kies een Mars rover:")
    start_frame = create_curiosity_frame(menu_frame)
    start_frame.grid(row = 5, column = 0)

    def show_menu():
        """Deze functie laat bij de gekozen rover het juiste menu zien""" 
        rover_choice = selected_rover.get()
        global count_curiosity
        global count_opportunity
        global count_spirit
        
        global curiosity_frame
        global opportunity_frame
        global spirit_frame 
        global start_frame

        start_frame.grid_forget()    

        if rover_choice == 'curiosity' and count_curiosity == 0:
            print_counters()
            print(rover_choice)
            count_curiosity += 1
            count_opportunity = 0
            count_spirit = 0
            print_counters()
            if opportunity_frame == None and spirit_frame == None: 
                curiosity_frame = create_curiosity_frame(menu_frame)
                curiosity_frame.grid()
            elif opportunity_frame != None and spirit_frame == None: 
                opportunity_frame.grid_forget()
                opportunity_frame = None
                curiosity_frame = create_curiosity_frame(menu_frame)
                curiosity_frame.grid()
            elif spirit_frame != None and opportunity_frame == None:
                spirit_frame.grid_forget()
                spirit_frame = None
                curiosity_frame = create_curiosity_frame(menu_frame)
                curiosity_frame.grid()
                    
        elif rover_choice == 'opportunity' and count_opportunity == 0:
            print_counters()
            print(rover_choice)
            count_curiosity = 0
            count_opportunity += 1
            count_spirit = 0
            print_counters()

            if curiosity_frame == None and spirit_frame == None: 
                opportunity_frame = create_opportunity_frame(menu_frame)
                opportunity_frame.grid()
            elif curiosity_frame != None and spirit_frame == None: 
                curiosity_frame.grid_forget()
                curiosity_frame = None
                opportunity_frame = create_opportunity_frame(menu_frame)
                opportunity_frame.grid()
            elif spirit_frame != None and curiosity_frame == None:
                spirit_frame.grid_forget()
                spirit_frame = None
                opportunity_frame = create_opportunity_frame(menu_frame)
                opportunity_frame.grid()
            
        elif rover_choice == 'spirit' and count_spirit == 0:
            print_counters()
            print(rover_choice)
            count_curiosity = 0
            count_opportunity = 0
            count_spirit += 1
            print_counters()

            if curiosity_frame == None and opportunity_frame == None: 
                spirit_frame = create_spirit_frame(menu_frame)
                spirit_frame.grid()
            elif curiosity_frame != None and opportunity_frame == None: 
                curiosity_frame.grid_forget()
                curiosity_frame = None                          
                spirit_frame = create_spirit_frame(menu_frame)
                spirit_frame.grid()
            elif opportunity_frame != None and curiosity_frame == None:
                opportunity_frame.grid_forget()
                opportunity_frame = None          
                spirit_frame = create_spirit_frame(menu_frame)                      
                spirit_frame.grid() 

                                            
    selected_rover = tk.StringVar(container, "curiosity")
    curiosity = ttk.Radiobutton(container, text='Curiosity', value='curiosity', variable=selected_rover, command = show_menu)
    opportunity = ttk.Radiobutton(container, text='Opportunity', value='opportunity', variable=selected_rover, command = show_menu)
    spirit = ttk.Radiobutton(container, text='Spirit', value='spirit', variable=selected_rover, command = show_menu)    
    
    # title_get_photo_frame = ttk.Label(get_photos, text = "Menu")
    # title_get_photo_frame.grid(row = 0, column = 0)
    rover_label.grid(row = 1, column = 0, sticky = tk.W)	
    curiosity.grid(row = 2, column= 0, sticky = tk.W)
    opportunity.grid(row = 3, column = 0, sticky = tk.W)
    spirit.grid(row = 4, column = 0, sticky = tk.W)

def create_curiosity_frame(container):
    """Deze functie maakt een frame waarmee een camera van de Curiosity-rover kan worden gekozen"""
    
    curiosity_frame = ttk.Frame(container)
    curiosity_frame_title = ttk.Label(curiosity_frame, text = "Curiosity", font=("Helvetica", 12))
    curiosity_label = ttk.Label(curiosity_frame, text="Kies een datum waarop de foto's zijn genomen: ")
    calendar_curiosity = choose_date_curiosity(curiosity_frame)
    
    curiosity_cam_label = ttk.Label(curiosity_frame, text = "Maak een keuze uit een van de volgende camera-opties: ")
    
    selected_cam = tk.StringVar()
    all_cam = ttk.Radiobutton(curiosity_frame, text = "Alle camera's", value = 'None', variable= selected_cam)
    fhaz = ttk.Radiobutton(curiosity_frame, text='fhaz', value='fhaz', variable=selected_cam)
    rhaz = ttk.Radiobutton(curiosity_frame, text='rhaz', value='rhaz', variable=selected_cam)
    mast = ttk.Radiobutton(curiosity_frame, text='mast', value='mast', variable=selected_cam) 
    chemcam = ttk.Radiobutton(curiosity_frame, text='chemcam', value = 'chemcam', variable= selected_cam)
    mahli = ttk.Radiobutton(curiosity_frame, text = 'mahli', value = 'mahli', variable=selected_cam)
    mardi = ttk.Radiobutton(curiosity_frame, text = 'mardi', value = 'mardi', variable=selected_cam)
    navcam = ttk.Radiobutton(curiosity_frame, text = 'navcam', value = 'navcam', variable = selected_cam)   
    
    curiosity_frame_title.grid(row = 0, column = 0, )
    curiosity_label.grid(row = 1, column = 0, sticky = tk.W, pady = 10)
    calendar_curiosity.grid(row = 2, column = 0, sticky = tk.W)
    curiosity_cam_label.grid(row = 3, column = 0, sticky = tk.W, pady = 10)
    all_cam.grid(row = 4, column = 0, sticky = tk.W)
    fhaz.grid(row = 5, column = 0, sticky = tk.W)
    rhaz.grid(row = 6, column = 0, sticky = tk.W)
    mast.grid(row = 7, column = 0, sticky = tk.W)
    chemcam.grid(row = 8, column = 0, sticky = tk.W)
    mahli.grid(row = 9, column = 0, sticky = tk.W)
    mardi.grid(row = 10, column = 0, sticky = tk.W)
    navcam.grid(row = 11, column = 0, sticky = tk.W)
     
    def get_pictures():
        rover = "Curiosity"
        date = calendar_curiosity.get_date()
        print(date)
        cam = selected_cam.get()
        print(cam)

        parameters = set_parameters_earth_date(date, cam)        
        url_curiosity = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?'

        if cam != 'None':    
            r = requests.get(url_curiosity, params = parameters)
            print("Status code:", r.status_code)
        
            output = r.json()
        
        elif cam == 'None':
            all_cam = parameters
            del all_cam['camera']
            print(parameters)
            print(all_cam)
            
            r = requests.get(url_curiosity, params = all_cam)
            print("Status code:", r.status_code)

            output = r.json()
        
        for key, value in output.items():
            if key == 'photos':
                photo_list_dict = value  

        photo_list = []

        for photo in photo_list_dict:
            photo_list.append(photo['img_src'])

        number_photos = len(photo_list)
    
        print("Aantal foto's: " + str(len(photo_list)))

        # Hier splitsen we: als len(photo_list) = 0, dan messagebox 'geen foto's gevonden'
        # Als len_(photo_list) != 0, dan pop up met progressbar

        if number_photos == 0:
            showinfo(message="Geen foto's gevonden!")
        elif number_photos > 0:

            top = tk.Toplevel(root)
            top.geometry('320x120')
            top.title("Status")

            # progressbar
            pb = ttk.Progressbar(
                    top,
                    orient='horizontal',
                    mode='determinate',
                    length=300)
            # place the progressbar
            pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

            # label
            value_label = ttk.Label(top, text=update_progress_label(pb))
            value_label.grid(column=0, row=1, columnspan=2)  
         
            directory = create_pictures_directory(rover, parameters)

            def download_image(url, file_name, directory):
                """Functie die een plaatje download van een website met url 'url' en deze opslaat in 'file_name.jpg'"""
                full_path = os.path.join(directory, file_name + '.jpg')
                urllib.request.urlretrieve(url, full_path)

            for i in range(0, len(photo_list)):
                url = photo_list[i]
                file_name = str('Photo_' + str(i))
                download_image(url, file_name, directory) 
                if pb['value'] < 100:
                    pb['value'] += 100*1/int(number_photos)
                    #print(pb['value'])
                    value_label['text'] = update_progress_label(pb)
                    top.update()
            
            top.destroy()
            showinfo(message="Alle foto's zijn gedownload!") 
            
    create_search_button(curiosity_frame, get_pictures)

    return curiosity_frame

def create_opportunity_frame(container):
    """Deze functie maakt een frame waarmee een camera van de Opportunity-rover kan worden gekozen"""
    opportunity_frame = ttk.Frame(container)  
    opportunity_frame_title = ttk.Label(opportunity_frame, text = "Opportunity", font=("Helvetica", 12))  
    opportunity_label = ttk.Label(opportunity_frame, text="Kies een datum waarop de foto's zijn genomen: ")
    calendar_opportunity = choose_date_opportunity(opportunity_frame)
    
    opportunity_cam_label = ttk.Label(opportunity_frame, text = "Maak een keuze uit een van de volgende camera-opties: ")
    selected_cam = tk.StringVar()
    all_cam = ttk.Radiobutton(opportunity_frame, text = "Alle camera's", value = 'None', variable= selected_cam)
    fhaz = ttk.Radiobutton(opportunity_frame, text='fhaz', value='fhaz', variable=selected_cam)
    rhaz = ttk.Radiobutton(opportunity_frame, text='rhaz', value='rhaz', variable=selected_cam)
    navcam = ttk.Radiobutton(opportunity_frame, text = 'navcam', value = 'navcam', variable = selected_cam) 
    pancam = ttk.Radiobutton(opportunity_frame, text='pancam', value = 'pancam', variable= selected_cam)
    minites = ttk.Radiobutton(opportunity_frame, text = 'minites', value = 'minites', variable=selected_cam)       
    
    opportunity_frame_title.grid(row = 0, column = 0, )
    opportunity_label.grid(row = 1, column = 0, sticky = tk.W, pady = 10)
    calendar_opportunity.grid(row = 2, column = 0, sticky = tk.W)

    opportunity_cam_label.grid(row = 3, column = 0, sticky = tk.W, pady = 10)
    all_cam.grid(row = 4, column = 0, sticky = tk.W)
    fhaz.grid(row = 5, column = 0, sticky = tk.W)
    rhaz.grid(row = 6, column = 0, sticky = tk.W)
    navcam.grid(row = 7, column = 0, sticky = tk.W)
    pancam.grid(row = 8, column = 0, sticky = tk.W)
    minites.grid(row = 9, column = 0, sticky = tk.W)

    def get_pictures():
        rover = "Opportunity"
        date = calendar_opportunity.get_date()
        print(date)
        cam = selected_cam.get()
        print(cam)

        parameters = set_parameters_earth_date(date, cam)        
        url_opportunity = 'https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos?'

        if cam != 'None':    
            r = requests.get(url_opportunity, params = parameters)
            print("Status code:", r.status_code)
        
            output = r.json()
        
        elif cam == 'None':
            all_cam = parameters
            del all_cam['camera']
            
            r = requests.get(url_opportunity, params = all_cam)
            print("Status code:", r.status_code)

            output = r.json()
        
        for key, value in output.items():
            if key == 'photos':
                photo_list_dict = value  

        photo_list = []

        for photo in photo_list_dict:
            photo_list.append(photo['img_src'])

        number_photos = len(photo_list)
        print("Aantal foto's: " + str(number_photos))

        if number_photos == 0:
            showinfo(message="Geen foto's gevonden!")
        elif number_photos > 0:
            top = tk.Toplevel(root)
            top.geometry('320x120')
            top.title("Status")

            # progressbar
            pb = ttk.Progressbar(
                    top,
                    orient='horizontal',
                    mode='determinate',
                    length=300)
            # place the progressbar
            pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

            # label
            value_label = ttk.Label(top, text=update_progress_label(pb))
            value_label.grid(column=0, row=1, columnspan=2)             

            directory = create_pictures_directory(rover, parameters)
            
            def download_image(url, file_name, directory):
                """Functie die een plaatje download van een website met url 'url' en deze opslaat in 'file_name.jpg'"""
                full_path = os.path.join(directory, file_name + '.jpg')
                urllib.request.urlretrieve(url, full_path)

            for i in range(0, len(photo_list)):
                url = photo_list[i]
                file_name = str('Photo_' + str(i))
                download_image(url, file_name, directory)
                if pb['value'] < 100:
                    pb['value'] += 100*1/int(number_photos)
                    #print(pb['value'])
                    value_label['text'] = update_progress_label(pb)
                    top.update()  
            
            top.destroy()
            showinfo(message="Alle foto's zijn gedownload!")
            
    create_search_button(opportunity_frame, get_pictures)

    return opportunity_frame

def create_spirit_frame(container):
    """Deze functie maakt een frame waarmee een camera van de Spirit-rover kan worden gekozen"""
    spirit_frame = ttk.Frame(container) 
    spirit_frame_title = ttk.Label(spirit_frame, text = "Spirit", font=("Helvetica", 12))      
    spirit_label = ttk.Label(spirit_frame, text = "Kies een datum waarop de foto's zijn genomen: ")
    calendar_spirit = choose_date_spirit(spirit_frame) 
    
    spirit_cam_label = ttk.Label(spirit_frame, text = "Maak een keuze uit een van de volgende camera-opties: ")
    
    selected_cam = tk.StringVar()
    all_cam = ttk.Radiobutton(spirit_frame, text = "Alle camera's", value = 'None', variable= selected_cam)
    fhaz = ttk.Radiobutton(spirit_frame, text='fhaz', value='fhaz', variable=selected_cam)
    rhaz = ttk.Radiobutton(spirit_frame, text='rhaz', value='rhaz', variable=selected_cam)
    navcam = ttk.Radiobutton(spirit_frame, text = 'navcam', value = 'navcam', variable = selected_cam) 
    pancam = ttk.Radiobutton(spirit_frame, text='pancam', value = 'pancam', variable= selected_cam)
    minites = ttk.Radiobutton(spirit_frame, text = 'minites', value = 'minites', variable=selected_cam)       
    
    spirit_frame_title.grid(row = 0, column = 0, )
    spirit_label.grid(row = 1, column = 0, sticky = tk.W, pady = 10)
    calendar_spirit.grid(row = 2, column = 0, sticky = tk.W)  
    spirit_cam_label.grid(row = 3, column = 0, sticky = tk.W, pady = 10)
    all_cam.grid(row = 4, column = 0, sticky = tk.W)
    fhaz.grid(row = 5, column = 0, sticky = tk.W)
    rhaz.grid(row = 6, column = 0, sticky = tk.W)
    navcam.grid(row = 7, column = 0, sticky = tk.W)
    pancam.grid(row = 8, column = 0, sticky = tk.W)
    minites.grid(row = 9, column = 0, sticky = tk.W)   

    def get_pictures():
        rover = "Spirit"
        date = calendar_spirit.get_date()
        print(date)
        cam = selected_cam.get()
        print(cam)

        parameters = set_parameters_earth_date(date, cam)        
        url_spirit = 'https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos?'

        if cam != 'None':    
            r = requests.get(url_spirit, params = parameters)
            print("Status code:", r.status_code)
        
            output = r.json()
        
        elif cam == 'None':
            all_cam = parameters
            del all_cam['camera']
            print(parameters)
            print(all_cam)
            
            r = requests.get(url_spirit, params = all_cam)
            print("Status code:", r.status_code)

            output = r.json()
        
        for key, value in output.items():
            if key == 'photos':
                photo_list_dict = value  

        photo_list = []

        for photo in photo_list_dict:
            photo_list.append(photo['img_src'])
        
        number_photos = len(photo_list) 
        print("Aantal foto's: " + str(number_photos))

        if number_photos == 0:
            showinfo(message="Geen foto's gevonden!")
        elif number_photos > 0:

            top = tk.Toplevel(root)
            top.geometry('320x120')
            top.title("Status")

            # progressbar
            pb = ttk.Progressbar(
                    top,
                    orient='horizontal',
                    mode='determinate',
                    length=300)
            # place the progressbar
            pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

            # label
            value_label = ttk.Label(top, text=update_progress_label(pb))
            value_label.grid(column=0, row=1, columnspan=2)    

            directory = create_pictures_directory(rover, parameters)

            def download_image(url, file_name, directory):
                """Functie die een plaatje download van een website met url 'url' en deze opslaat in 'file_name.jpg'"""
                full_path = os.path.join(directory, file_name + '.jpg')
                urllib.request.urlretrieve(url, full_path)

            for i in range(0, len(photo_list)):
                url = photo_list[i]
                file_name = str('Photo_' + str(i))
                download_image(url, file_name, directory) 
                if pb['value'] < 100:
                    pb['value'] += 100*1/int(number_photos)
                    #print(pb['value'])
                    value_label['text'] = update_progress_label(pb)
                    top.update()

            top.destroy()
            showinfo(message="Alle foto's zijn gedownload!")  

    create_search_button(spirit_frame, get_pictures)

    return spirit_frame 

def choose_date_curiosity(root):
    """Deze functie geeft de gebruiker opties om een datum te selecteren voor de curiosity rover"""
    calendar = Calendar(root, mindate = datetime.datetime(2012, 8, 5), maxdate= date.today(), date_pattern = "yyyy-mm-dd")
    return calendar

def choose_date_opportunity(root):
    """Deze functie geeft de gebruiker opties om een datum te selecteren voor de opportunity rover"""
    calendar = Calendar(root, mindate = datetime.datetime(2004, 1, 25), maxdate= datetime.datetime(2018, 6, 10), date_pattern = "yyyy-mm-dd")
    return calendar

def choose_date_spirit(root):
    """Deze functie geeft de gebruiker opties om een datum te selecteren voor de spirit rover"""
    calendar = Calendar(root, mindate = datetime.datetime(2004, 1, 4), maxdate= datetime.datetime(2010, 3, 22), date_pattern = "yyyy-mm-dd")
    return calendar

def set_parameters_earth_date(date, camera):
    """Stelt de parameters in voor een API-Request met earth_date als parameter"""      
    parameters = {
        "earth_date": date,
        "camera": camera,
        "api_key": "DEMO_KEY"
    }
    return parameters   

def create_pictures_directory(rover, parameters):
    """Deze functie maakt een map aan met de naam die past bij de rover en de ingevoerde datum en camera"""
    date = str(parameters['earth_date'])
    if 'camera' not in parameters:
        selected_cam = "all"
    else:    
        cam = str(parameters['camera'])
        selected_cam = cam

    directory = str(rover + "_" + selected_cam + "_" + date)
    parent_dir = "C:\\Users\Administrator.REAGR008\\Documents\\Mars Foto's\\Downloaded_Images"

    path = os.path.join(parent_dir, directory)
    
    try:
        os.mkdir(path)
        return(path)
    except FileExistsError:
        showinfo(message = "Deze foto's zijn al een keer gedownload!")
        shutil.rmtree(path)
        os.mkdir(path)
        return(path)

def count_images(path):
    """Deze functie telt hoeveel jpg bestanden er zijn opgeslagen in een gegeven map (aangegeven met path)"""
    list = os.listdir(path)
    count = len(list)

    return count

def create_photo_list(number):
    """Deze functie accepteert het aantal bestanden in map en maakt een lijst met de bestandsnamen van de foto's"""
    name_list = []
    for i in range(0, number):
        name = "Photo_"+ str(i) + ".jpg"
        name_list.append(name)

    return name_list 

def make_folder_list(path):
    """Met deze functie maken we een lijst van mappen in path """
    folder_list = os.listdir(path) 
    
    return folder_list

def create_ctime_list(folder_list, home_folder):
    """Met deze functie maken we een lijst van tijden waarop de mappen zijn aangemaakt"""
    # folder_ctime_dict = {}
    ctime_list = []
    
    for folder in folder_list:
        path = os.path.join(home_folder, folder)
        c_time = os.path.getctime(path)
        ctime_list.append(c_time)
    
    return ctime_list

def choose_newest_folder(folder_list, time_list):
    """Deze functie retourneert de naam van de laatst aangemaakte map"""
    try:
        index_highest_time = time_list.index(max(time_list))
        name_newest_folder = folder_list[index_highest_time]
        return name_newest_folder
    except ValueError:
        pass

def show_pictures(): 
    global index_picture
    global name_list
    global path
    global header
    global navigation_frame
    global img

    image_folder = "C:\\Users\Administrator.REAGR008\\Documents\\Mars Foto's\\Downloaded_Images"
    try:
        folder_list = make_folder_list(directory)
        print(folder_list)
        time_list = create_ctime_list(folder_list, directory)
        print(time_list)
        name = choose_newest_folder(folder_list, time_list)
        print(name)

        # image_directory = os.path.join(image_folder, name)
        print(directory)

        image_directory = os.path.join(directory, name)
        print(image_directory)

        path = image_directory
    
        path = image_directory
        number = count_images(path)
        name_list = create_photo_list(number)
        print(name_list)

        rover, cam, datum = create_header_info(name)

        header.grid_forget()
        info_label.grid_forget()
        navigation_frame.grid_forget()
        header = str("Mars Lander: " + rover + "    Camera's: " + cam + "    Datum: " + datum )
        # Titel: Mars Foto met info: Rover, camera en datum
        header = ttk.Label(show_photos, text = header)
        header.grid(row = 1, column = 0)
    
        print([name_list[0]])
        image_name = name_list[0]
        print(image_name)
        url = full_path = os.path.join(path, image_name)
        img = Image.open(url)

        width, height = get_image_dimensions(img)
        print("The height of the image is: ", height) 
        print("The width of the image is: ", width) 

        resize_image(img, width, height)    
    
        # image_space.create_image(10,10, anchor = NW, image=original_image)
        index_picture = 0
        update_picture_label()
        info_label.grid(row = 0, column = 1)
        navigation_frame.grid(row = 1, column = 0)
    except TypeError:
        showinfo(message="Er zijn nog geen foto's om weer te geven. Download eerst foto's!")
    #except NameError:
    #    pass

def center_image(canvas, image):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    image_width = image.width()
    image_height = image.height()

    x = (canvas_width - image_width) // 2
    y = (canvas_height - image_height) // 2

    canvas.create_image(x, y, anchor=tk.NW, image=image)

def get_image_dimensions(image):
    width = image.width
    height = image.height

    return width, height

def start_info():
    """Als er al foto's in een eerdere sessie zijn gedownload, dan kunnen wordt de info hiervan getoond"""
    global directory
    global name_list
    global path
    global index_picture 
    global header
    global info_label
    
    directory = "C:\\Users\Administrator.REAGR008\\Documents\\Mars Foto's\\Downloaded_Images"
    index_picture = -1 
    folder_list = make_folder_list(directory)
    # print(folder_list)
    time_list = create_ctime_list(folder_list, directory)
    # print(time_list)
    name = choose_newest_folder(folder_list, time_list)
    # print(name)

    try:
        rover, cam, datum = create_header_info(name)
    except TypeError:
        pass

    try:
        header = str("Mars Lander: " + rover + "    Camera's: " + cam + "    Datum: " + datum ) 
        # Titel: Mars Foto met info: Rover, camera en datum
        header = ttk.Label(show_photos, text = header)
        header.grid(row = 1, column = 0)

    except NameError:
        header = str("Mars Lander: Geen"  + "    Camera's: Geen"  "    Datum: Geen" ) 
        # Titel: Mars Foto met info: Rover, camera en datum
        header = ttk.Label(show_photos, text = header)
        header.grid(row = 1, column = 0) 
  
    image_folder = "C:\\Users\Administrator.REAGR008\\Documents\\Mars Foto's\\Downloaded_Images"

    try:
        folder_list = make_folder_list(directory)
        # print(folder_list)
        time_list = create_ctime_list(folder_list, directory)
        # print(time_list)
        name = choose_newest_folder(folder_list, time_list)
        # print(name)

        # image_directory = os.path.join(image_folder, name)
        # print(directory)
        image_directory = os.path.join(directory, name)
        # print(image_directory)
   
        path = image_directory
        number = count_images(path)
        name_list = create_photo_list(number)
        # print(name_list)
        

        update_picture_label()
        info_label.grid(row = 0, column = 1)

        index_picture = -1
    
    except TypeError:
        message = str(" Foto 0" + " van 0") 
        info_label = ttk.Label(navigation_frame, text = message, width= 16) 
        info_label.grid(row = 0, column = 1)

def resize_image(image, width, height):
    global new_image
    ratio = width/height     
    resized_image= image.resize((600, int(600/ratio)), Image.LANCZOS)
    width_resized, height_resized = get_image_dimensions(resized_image)
    # print("The height of the resized image is: ", height_resized) 
    # print("The width of the resized image is: ", width_resized) 

    new_image = ImageTk.PhotoImage(resized_image)
    image_space.create_image(200,10, anchor = NW, image=new_image)    

def load_previous():
    """Deze functie laadt het vorige plaatje, wanneer er op button_previous is geklikt"""
    global original_image
    global index_picture
    global img
    if index_picture > 0:
        print(index_picture)
        index_picture -= 1
        print([name_list[index_picture]])
        image_name = name_list[index_picture]
        print(image_name)
        url = os.path.join(path, image_name)
        img = Image.open(url)

        width, height = get_image_dimensions(img)
        # print("The height of the image is: ", height) 
        # print("The width of the image is: ", width) 

        resize_image(img, width, height)  
        update_picture_label()
        info_label.grid(row = 0, column = 1)       

def load_next():
    """Deze functie laadt het volgende plaatje, wanneer er op buttne_next is geklikt"""
    global original_image
    global index_picture
    global img
    print(index_picture)
    if index_picture < len(name_list):
        index_picture += 1
        print([name_list[index_picture]])
        image_name = name_list[index_picture]
        print(image_name)
        url = full_path = os.path.join(path, image_name)
        img = Image.open(url)
        width, height = get_image_dimensions(img)
        #print("The height of the image is: ", height) 
        #print("The width of the image is: ", width) 

        resize_image(img, width, height)      
        update_picture_label()
        info_label.grid(row = 0, column = 1)

def update_picture_label():
    """Deze functie zorgt ervoor dat het nummer van de foto wordt geupdate en dat het totaal aantal foto's wordt weergegeven"""  
    global info_label
    global index_picture
    print(index_picture)
    message = str(" Foto " + str(index_picture + 1)) + " van " + str(len(name_list)) 
    info_label = ttk.Label(navigation_frame, text = message, width= 16)      

def create_header_info(name):
    """Deze functie zet de naam van de map met foto's om info: Rover, camera en datum"""
    try:
        split_name = name.split("_")
        rover_name = split_name[0]
        cam = split_name[1]
        datum = split_name[2]
        return rover_name, cam, datum
    except AttributeError:
        pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Variabelen (tbv frame 'Keuze Mars Rover')
count_curiosity = 0
count_opportunity = 0
count_spirit = 0

curiosity_frame = None
opportunity_frame = None
spirit_frame = None

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
# Start van het eigenlijke programma:
root = tk.Tk()
root.title('Mars in Beeld')

# Afmetingen van het basisvenster ('root') gelijk stellen aan de afmetingen van het scherm
# We halen eerst de lengte en de breedte van het scherm op. 
# Vervolgens zetten we de afmetingen van root gelijk aan de afmetingen van het scherm via root.geometry 
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# Nu maken we twee basisframes voor de GUI:
#   - Frame 1 (get_photos): linkerframe, hier komen alle menu-opties voor keuze rover, camera's, datum en knoppen voor zoeken en tonen van foto's
#   - Frame 2(show_photos): rechterframe, hier worden de foto's getoond met knoppen voor navigatie door de verzameling foto's en informatie over de foto's
get_photos = tk.Frame(root, width = 400)
show_photos = tk.Frame(root, width = 650)

# We zetten een padding voor de linkerkolom: anders zitten de meest linkse tekens te dicht tegen de rand van het scherm aan.
root.columnconfigure(0, pad = 15)

# De benadering is als volgt: eerst maken we de twee frames met hun onderdelen. Als deze onderdelen gemaakt zijn, plaatsen we deze vervolgens in de root. 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Frame 1: menu voor keuze rover, camera, datum en de knoppen 'Zoek foto's' en 'Toon foto's'
# We maken hier de verschillende widgets die erbij horen: de titel ('menu'), de menu-opties (via de functie create_rover_frame) en de knop 'Toon foto's'
menu_label = ttk.Label(get_photos, text = "Menu", font=("Helvetica", 16))
menu_label.grid(row = 0, column = 0, pady = 10)    
menu_frame = tk.Frame(get_photos)

show_button = ttk.Button(root, text ="Toon foto's", command = show_pictures)
show_button.grid(row = 2, column = 0)

menu_frame.grid(row = 1, column = 0)

# Met behulp van deze functie wordt het menu gemaakt waarin je kunt kiezen voor een rover.
# De standaard-instelling is dat je het curiosity-menu ziet
create_rover_frame(menu_frame)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Frame 2:  waar het plaatje in komt
# We maken hier de verschillende widgest die erbij horen: de titel('Afbeeldingen van Mars, het gedeelte waar de foto's worden getoond (image_frame) 
# en het gedeelte waar de navigatie-opties worden getoond ('navigation_frame')'.)
# Merk op dat de knoppen previous_button en next_button hier ook worden gemaakt. 
# Als er in een vorige sessie al foto's zijn gezocht en gedownload, wordt de informatie van de laatst gedownloade set met foto's weergegeven. 
# Dit wordt gedaan via de functie start_info()
title_show_photo_frame = ttk.Label(show_photos, text = "Afbeeldingen van Mars", font=("Helvetica", 16))
title_show_photo_frame.grid(row = 0, column = 0, pady = 10)
image_frame = ttk.Frame(show_photos)
image_frame.grid(row = 2, column = 0)

# Frame voor doorklikken en terugklikken van foto's
navigation_frame = ttk.Frame(image_frame, height = 250, width = 900)

previous_button = ttk.Button(navigation_frame, text = "Vorige", command = load_previous)
next_button = ttk.Button(navigation_frame, text = "Volgende", command= load_next)
# info_label.grid(row = 0, column = 1)

previous_button.grid(row = 0, column = 0)
next_button.grid(row = 0, column = 2)

# Als er al in een eerdere sessie foto's zijn gedownload, dan worden de gegevens van de laatste map die in deze sessie is gemaakt, weergegeven.
# De foto's uit deze map kunnen bekeken worden via de knoppen 'Toon foto's', 'Volgende' en 'Vorige'
start_info()

# Ruimte voor de foto
image_space = Canvas(image_frame, height= 650, width= 900)
image_space.grid(row = 0, column = 0)

navigation_frame.grid(row = 2, column = 0)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Code voor het tonen van de twee basisframes
get_photos.grid(row = 0, column = 0, sticky = tk.N)
show_photos.grid(row = 0, column = 1)

root.mainloop()