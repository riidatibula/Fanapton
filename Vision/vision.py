import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
vision_client = vision.Client()

# The name of the image file to annotate
file_name = "Resources/Fire Black T-Shirt Women PHP499.jpg"

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
        content=content)

# Performs label detection on the image file
labels = image.detect_labels()

print 'Labels:' 
for label in labels:
    print(label.description)

# Property detection
props = image.detect_properties()

print '\nColor Properties:'
for color in props.colors:
  print('fraction: {}'.format(color.pixel_fraction))
  print('score: {}'.format(color.score))
  print('\tr: {}'.format(color.color.red))
  print('\tg: {}'.format(color.color.green))
  print('\tb: {}'.format(color.color.blue))
  print('\ta: {}'.format(color.color.alpha))


# Read more in the Python API Reference Documentation for 