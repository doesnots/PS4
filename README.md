# PS-4
- This Itienarary Application uses OpenAI Text Completion Model "**text-davinci-002**" which takes Destination, Trip Type and Trip Purpose as Prompt and generates Itinerary day-by-day based on the start date and end date of the trip. 
- Later the Itinerary can be Saved in PDF format to access it in offline mode. 
---
# Screenshot
![screenshot](https://gateway.pinata.cloud/ipfs/QmRdB7WSEcV6dx7i3PDkJJ5YpktihW6HzfuHQKUuJJV1XM)

---
# To Run this Itinerary

## Installations
- Python3 
- pip (latest version 23.0.1)
---

## Libraries 
1. openai (Access API)

   ```bash
   pip install openai
   ```
2. tkinter (For UI written in python, would not work in notebooks like Jupyter Lab or Google Colab)
      ```bash
   pip install tkinter
   ```
3. reportlab (To Generate PDF)
      ```bash
   pip install reportlab
   ```
---

## To Generate the Itienerary
1. Visit OpenAI Website to generate an API-Key (https://platform.openai.com/account/api-keys) 
2. Replace the OpenAI-API-KEY in itineraryF.py file with the new key generated to access the text-davinci-002 model. 
