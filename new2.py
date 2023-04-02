import sqlite3
from tkinter import *

import openai
# from PIL import ImageTk, Image as PilImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# OpenAI API credentials
openai.api_key = "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"

# Initialize Tkinter
root = Tk()
root.title("Itinerary Maker")

# Create the main frame
frame = Frame(root)
frame.pack()

# Create the database connection
conn = sqlite3.connect('itinerary.db')

# Create the itinerary table
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS itinerary
             (destination text, start_date text, end_date text, trip_type text, trip_purpose text, itinerary text)''')

# Function to generate the trip plan
# Function to generate the trip plan
def generate_itinerary():
    # Get the user inputs
    destination = destination_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    trip_type = trip_type_var.get()
    trip_purpose = trip_purpose_var.get()
    # trip_checkpoints = trip_checkpoints_entry.get() # added

    # Use the OpenAI API to generate the itinerary
    prompt = f"Generate a trip itinerary for a {trip_type} {trip_purpose} trip to {destination} from {start_date} (yyyy-mm-dd) to {end_date} (yyyy-mm-dd)."
    # if trip_checkpoints:
        # prompt += f" Also include the following checkpoints: {trip_checkpoints}."
    prompt += " Don't generate the arrival and departure details, arrange it in proper date-wise bullets."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    itinerary = response.choices[0].text

    # Update the itinerary display
    itinerary_text.delete(1.0, END)
    itinerary_text.insert(END, itinerary)

    # Save the itinerary to the database
    c.execute("INSERT INTO itinerary VALUES (?, ?, ?, ?, ?, ?)", (destination, start_date, end_date, trip_type, trip_purpose, itinerary))
    conn.commit()


def save_as_pdf():
    # Get the user inputs
    destination = destination_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Retrieve the itinerary from the database
    c.execute("SELECT itinerary FROM itinerary WHERE destination=? AND start_date=? AND end_date=?", (destination, start_date, end_date))
    row = c.fetchone()
    itinerary = row[0]

    # Create a PDF of the itinerary
    filename = f"{destination}_{start_date}_{end_date}.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)

    # Add the title to the PDF
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(1 * inch, 10.5 * inch, "Trip Itinerary")

    # Add the destination and dates to the PDF
    pdf.setFont("Helvetica", 14)
    pdf.drawString(1 * inch, 9.5 * inch, f"Destination: {destination}")
    pdf.drawString(1 * inch, 9.2 * inch, f"Dates: {start_date} to {end_date}")

    # Add the itinerary to the PDF
    pdf.setFont("Helvetica", 12)
    text_object = pdf.beginText(1 * inch, 8.5 * inch)
    text_object.textLines(itinerary)
    pdf.drawText(text_object)

    # # Add a map to the PDF
    # map_image = PilImage.open("map.jpg")
    # map_image = map_image.resize((400, 400))
    # map_image.save("map_resized.jpg")
    # map_tk_image = ImageTk.PhotoImage(PilImage.open("map_resized.jpg"))
    # pdf.drawImage(map_tk_image, 4.25 * inch, 1.5 * inch)

    # Save the PDF and close the canvas
    pdf.showPage()
    pdf.save()

    # Display a message to the user
    itinerary_text.delete(1.0, END)
    itinerary_text.insert(END, "Itinerary saved as PDF")




# Function to view the saved itinerary
def view_itineraries():
    # Create a new window for the saved itineraries
    window = Toplevel(root)
    window.title("Saved Itineraries")

    # Create a frame for the saved itineraries
    frame = Frame(window)
    frame.pack()

    # Create a scrollbar for the saved itineraries
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Create a listbox to display the saved itineraries
    listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    listbox.pack()

    # Populate the listbox with the saved itineraries
    for row in c.execute("SELECT * FROM itinerary"):
        listbox.insert(END, row)

    # Configure the scrollbar
    scrollbar.config(command=listbox.yview)

# Create the destination label and entry
destination_label = Label(frame, text="Destination")
destination_label.grid(row=0, column=0)
destination_entry = Entry(frame)
destination_entry.grid(row=0, column=1)

# Create the start date label and entry
start_date_label = Label(frame, text="Start Date (YYYY-MM-DD)")
start_date_label.grid(row=1, column=0)
start_date_entry = Entry(frame)
start_date_entry.grid(row=1, column=1)

# Create the end date label and entry
end_date_label = Label(frame, text="End Date (YYYY-MM-DD)")
end_date_label.grid(row=2, column=0)
end_date_entry = Entry(frame)
end_date_entry.grid(row=2, column=1)

# Create the trip type label & dropdown
trip_type_label = Label(frame, text="Trip Type")
trip_type_label.grid(row=3, column=0)
trip_type_var = StringVar()
trip_type_var.set("Solo")
trip_type_dropdown = OptionMenu(frame, trip_type_var, "Solo", "Couple", "Group", "Family")
trip_type_dropdown.grid(row=3, column=1)

# Create the trip purpose label & dropdown
trip_purpose_label = Label(frame, text="Trip Purpose")
trip_purpose_label.grid(row=4, column=0)
trip_purpose_var = StringVar()
trip_purpose_var.set("Vacation")
trip_purpose_dropdown = OptionMenu(frame, trip_purpose_var, "Vacation", "Business", "Education","Religious","Adventure","site seeing")
trip_purpose_dropdown.grid(row=4, column=1)

# # Create the checkpoint label & entry with tick
# trip_checkpoints_label = Label(frame, text="Checkpoint")
# trip_checkpoints_label.grid(row=5, column=0)
# trip_checkpoints_entry = Entry(frame)
# trip_checkpoints_entry.grid(row=5, column=1)
# trip_checkpoints_tick = Label(frame, text="✓")
# trip_checkpoints_tick.grid(row=5, column=2)

# Create the itinerary display
itinerary_text = Text(frame, height=10, width=50)
itinerary_text.grid(row=6, column=0, columnspan=2)

# Create the generate itinerary button
generate_itinerary_button = Button(frame, text="Generate Itinerary", command=generate_itinerary)
generate_itinerary_button.grid(row=7, column=0)

# Create the view itineraries button
view_itineraries_button = Button(frame, text="View Itineraries", command=view_itineraries)
view_itineraries_button.grid(row=7, column=1)

# Create the save as PDF button
save_as_pdf_button = Button(frame, text="Save as PDF", command=save_as_pdf)
save_as_pdf_button.grid(row=8, column=0)


# Start the GUI
root.mainloop()



