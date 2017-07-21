import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

path = "Resources/arianna.jpg"

def detect_web(path):
  """Detects web annotations given an image."""
  vision_client = vision.Client()

  with io.open(path, 'rb') as image_file:
    content = image_file.read()

  image = vision_client.image(content=content)

  notes = image.detect_web()

  if notes.pages_with_matching_images:
    print('\n{} Pages with matching images retrieved'.format(
      len(notes.pages_with_matching_images)))

    for page in notes.pages_with_matching_images:
      print('Score : {}'.format(page.score))
      print('Url   : {}'.format(page.url))

  if notes.full_matching_images:
    print ('\n{} Full Matches found: '.format(
       len(notes.full_matching_images)))

    for image in notes.full_matching_images:
      print('Score:  {}'.format(image.score))
      print('Url  : {}'.format(image.url))

  if notes.partial_matching_images:
    print ('\n{} Partial Matches found: '.format(
      len(notes.partial_matching_images)))

    for image in notes.partial_matching_images:
      print('Score: {}'.format(image.score))
      print('Url  : {}'.format(image.url))

  if notes.web_entities:
    print ('\n{} Web entities found: '.format(len(notes.web_entities)))

    for entity in notes.web_entities:
        print('Score      : {}'.format(entity.score))
        print('Description: {}'.format(entity.description))


detect_web(path)