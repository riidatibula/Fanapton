import requests

image_url = "https://storage.googleapis.com/fanapton.appspot.com/Darth%20Vader.jpg"

data = {
"requests":[
  {
    "image":{
      "source":{
        "imageUri":
          "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
      }
    },
    "features":[
      {
        "type":"LABEL_DETECTION",
        "maxResults":1
      }
    ]
  }
]
}

r = requests.post('https://vision.googleapis.com/v1/images:annotate?key=private_key', data)
print r.text
