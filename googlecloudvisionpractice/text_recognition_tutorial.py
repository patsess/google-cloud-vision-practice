
import os
import io
from google.cloud import vision

__author__ = 'psessford'

"""
Main tutorial:
https://medium.com/searce/
tips-tricks-for-using-google-vision-api-for-text-detection-2d6d1e0c6361

To get credentials for the application:
https://www.datacamp.com/community/tutorials/beginner-guide-google-vision-api

To help to get set up:
https://medium.com/better-programming/
exploring-google-cloud-vision-api-and-feature-demonstration-with-python-
1f02e1dbdfd3
"""


def draw_boxes(image, bounds, color,width=5):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y
        ], fill=color, width=width)
    return image


def get_document_bounds(response, feature):
    for i, page in enumerate(document.pages):
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

            for paragraph in block.paragraphs:
                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds


def assemble_word(word):
    assembled_word = ""
    for symbol in word.symbols:
        assembled_word += symbol.text

    return assembled_word


def find_word_location(document, word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word = assemble_word(word)
                    if (assembled_word == word_to_find):
                        return word.bounding_box


def main():
    credentials = ('/home/pat/python_projects/repos/'
                   'google-cloud-vision-practice/'
                   'google-cloud-vision-practice-7fdcbb2f8608.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
    client = vision.ImageAnnotatorClient()

    with io.open('../images/wachovia.jpeg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    bounds = get_document_bounds(response, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')

    location = find_word_location(document, 'Overdrafts')
    print(location)


if __name__ == '__main__':
    main()
