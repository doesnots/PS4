# Set the base image to the official Python image
FROM python:3

# Set the working directory to /PS4
WORKDIR /PS4

# Copy the current directory contents into the container at /PS4
COPY . /PS4

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run when the container starts
CMD ["python", "src/itineraryF.py"]


