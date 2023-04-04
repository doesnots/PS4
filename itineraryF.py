import sqlite3
from tkinter import *
import openai
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# import tkinter as tk
root = Tk()
root.geometry('1920x1080')
root.configure(bg='Black')
root.title('Travel Planner')
root.state('zoomed')

# OpenAI API credentials
openai.api_key = "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"

# sql connection
conn = sqlite3.connect('itinerary.db')

# Create the itinerary table
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS itinerary
             (destination text, start_date text, end_date text, trip_type text, trip_purpose text, itinerary text)''')


# Function to generate the trip plan
def generate_itinerary():
    # Get the user inputs
    destination = Des.get()
    start_date = Start.get()
    end_date = End.get()
    trip_type = trip_type_var.get()
    trip_purpose = trip_purpose_var.get()

    # Use the OpenAI API to generate the itinerary
    prompt = f"Generate a trip itinerary for a {trip_type} {trip_purpose} trip to {destination} from {start_date} (yyyy-mm-dd) to {end_date} (yyyy-mm-dd), Assume the User is already at destination, arrange it in proper date-wise bullets."

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
    c.execute("INSERT INTO itinerary VALUES (?, ?, ?, ?, ?, ?)",
              (destination, start_date, end_date, trip_type, trip_purpose, itinerary))
    conn.commit()


# Function to save the itinerary as a PDF
def save_as_pdf():
    # Get the user inputs
    destination = Des.get()
    start_date = Start.get()
    end_date = End.get()

    # Retrieve the itinerary from the database
    c.execute("SELECT itinerary FROM itinerary WHERE destination=? AND start_date=? AND end_date=?",
              (destination, start_date, end_date))
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
    frame1 = Frame(window)
    frame1.pack()

    # Create a scrollbar for the saved itineraries
    scrollbar = Scrollbar(frame1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Create a listbox to display the saved itineraries
    listbox = Listbox(frame1, yscrollcommand=scrollbar.set)
    listbox.pack()

    # Populate the listbox with the saved itineraries
    for row in c.execute("SELECT * FROM itinerary"):
        listbox.insert(END, row)

    # Configure the scrollbar
    scrollbar.config(command=listbox.yview)


# Create the GUI
canvas_h = root.winfo_screenheight()
canvas_w = root.winfo_screenwidth()
canv = Canvas(root, height=canvas_h, width=canvas_w)
img = PhotoImage(file='ezgif.com-resize.gif')
canv.create_image(768, canvas_w / 4, anchor=CENTER, image=img)
canv.pack()
# Create the Destination labels and entry boxes
Des = Label(canv, text="Destination", fg="Black", bg="#a7e8d0", font=("Georgia", 16, "italic"))
Des.place(relx=0.1, rely=0.1)
Des = Entry(canv, fg="GREEN", font=("Futura", 16, "bold"), relief='raised')
Des.place(relx=0.25, rely=0.1)

# Create the Start and End Date labels and entry boxes
Start = Label(canv, text="Start Date", fg="Black", bg="#a7e8d0", font=("Georgia", 16, "italic"))
Start.place(relx=0.1, rely=0.2)
Start = Entry(canv, fg="BLUE", font=("Futura", 16, "bold"), relief='raised')
Start.place(relx=0.25, rely=0.2)
End = Label(canv, text="End Date", fg="Black", bg="#a7e8d0", font=("Georgia", 16, "italic"))
End.place(relx=0.1, rely=0.3)
End = Entry(canv, fg="RED", font=("Futura", 16, "bold"), relief='raised')
End.place(relx=0.25, rely=0.3)

# Create the Trip Type and Trip Purpose labels and dropdowns
trip_type_label = Label(canv, text="Trip Type", fg="Black", bg="#a7e8d0", font=("Georgia", 16, "italic"))
trip_type_label.place(relx=0.1, rely=0.4)
trip_type_var = StringVar()
trip_type_var.set("Solo")
trip_type_dropdown = OptionMenu(canv, trip_type_var, "Solo", "Couple", "Group", "Family")
trip_type_dropdown.configure(bg="GREEN", fg="white", font=("Georgia", 16, "italic"), highlightthickness=0)
trip_type_dropdown.place(relx=0.25, rely=0.4)
trip_purpose_label = Label(canv, text="Trip Purpose", fg="Black", bg="#a7e8d0", font=("Georgia", 16, "italic"))
trip_purpose_label.place(relx=0.1, rely=0.5)
trip_purpose_var = StringVar()
trip_purpose_var.set("Vacation")
trip_purpose_dropdown = OptionMenu(canv, trip_purpose_var, "Vacation", "Business", "Education", "Religious",
                                   "Adventure", "site seeing")
trip_purpose_dropdown.configure(bg="GREEN", fg="white", font=("Georgia", 16, "italic"), highlightthickness=0)
trip_purpose_dropdown.place(relx=0.25, rely=0.5)

# Create the Get Itinerary and Show Itinerary buttons
get_itinerary = Button(canv, text="Generate Itinerary", font="Georgia 16", fg="Black", command=generate_itinerary)
get_itinerary.place(relx=0.15, rely=0.7)
view_itinerary = Button(canv, text="View Itinerary", font="Georgia 16", fg="Black", command=view_itineraries)
view_itinerary.place(relx=0.30, rely=0.7)
show_itinerary = Label(canv, text="Your Itinerary", font="FUTURA 16", fg="Black")
show_itinerary.place(relx=0.635, rely=0.05)

# Create the text box to display the itinerary
itinerary_text = Text(canv, height=30, width=60, font=("Helvetica", 12, "bold"))
itinerary_text.place(relx=0.50, rely=0.1)

# Create the Save as PDF button
save_as_pdf_button = Button(canv, text="Save as PDF", font="Helvetica 12", command=save_as_pdf)
save_as_pdf_button.place(relx=0.642, rely=0.83)

# Credit Label
credit = Label(canv, text="©️ By: OM HINGE,KAMALIKA GHORA,RISHIKA JAIN", font=("Arial", 10, "bold"), fg="Black")
credit.place(relx=0.75, rely=0.95)

# Run the main loop
root.mainloop()
