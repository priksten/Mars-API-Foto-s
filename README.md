# Mars-API-Foto-s

# Omschrijving:
De NASA heeft in de afgelopen decennia een aantal marslanders foto’s laten nemen van het oppervlak van Mars. Denk hierbij bijvoorbeeld aan de Curiosity, de Opportunity en de Spirit. De foto’s die door deze marslanders worden gemaakt, kun je via een API opvragen. 
Het doel van dit project is om een applicatie te ontwikkelen waarin je foto’s kunt opvragen die door marslanders zijn gemaakt. De bedoeling is dat je hierbij kunt kiezen uit de marslander waarmee foto’s gemaakt zijn, de camera waarmee deze foto’s gemaakt zijn en de datum waarop deze foto’s gemaakt zijn. Hiervoor is ook een GUI ontwikkeld. 

# Programmeertaal + versie:
Python

# Gebruikte modules:
Datetime
OS
PIL
Requests
Shutil
Tkcalendar
Tkinter
Urllib.request

# Screenshots:
De basale opzet van het programma is als volgt:
![image](https://github.com/priksten/Mars-API-Foto-s/assets/85739742/6615396f-2b2f-47bd-bce5-76ca529b2ea5)

In de linkerkolom is er een menu waarin je een keuze kunt maken voor de marslander, de camera waarmee de foto’s gemaakt zijn en de datum waarop de foto’s gemaakt zijn. Wanneer de gebruiker zijn keuze heeft gemaakt, dan kan hij klikken op de knop ‘Zoek foto’s’
Als de gebruiker op de knop ‘Zoek foto’s’ klikt, dan zijn er twee mogelijke gevolgen. De eerste zien we in het volgende screenshot: er zijn voor de aangegeven combinatie van rover, camera en datum geen foto’s gevonden.

![image](https://github.com/priksten/Mars-API-Foto-s/assets/85739742/8cb0c498-8f5d-4761-8dca-ca15d9963f74)

In het tweede scenario worden er wel foto’s gevonden. In dat geval worden de foto’s gedownload. Er is altijd een progressbar zichtbaar die aangeeft hoe ver het proces van het ophalen en downloaden van de foto’s gevorderd is:
![image](https://github.com/priksten/Mars-API-Foto-s/assets/85739742/301e42a3-ec31-4731-b17f-b6dd379231ee)

Als de foto’s gedownload zijn, dan kun je deze bekijken door op de knop ‘Toon foto’s’ te klikken. De foto’s verschijnen dan in de rechterkolom. De foto’s zijn te bekijken door op knoppen ‘Vorige’ of ‘Volgende’ te klikken. Tussen deze twee knoppen, is er een label dat aangeeft hoeveel foto’s er zijn en wat het nummer van deze foto in het rijtje is. 
![image](https://github.com/priksten/Mars-API-Foto-s/assets/85739742/58ecb0da-37c4-4a12-83ef-79628860ca9b)
