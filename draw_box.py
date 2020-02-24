import base64
import numpy as np
from io import BytesIO

import face_recognition.face_recognition as fr
from PIL import Image, ImageDraw

def drawRectangle(image, known_encodings):
    status = False
    # Find all the faces and face encodings in the unknown image
    face_locations = fr.face_locations(image)

    known_face_names = [
        "Michael Reeves",
        "Michael Reeves"
    ]

    face_encodings = fr.face_encodings(image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(known_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            # Draw a label with a name below the face
            pad = 10
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left-pad, bottom - text_height - 10), (right+pad, bottom+pad)), fill=(255, 0, 0), outline=(255, 0, 0))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left-pad, top-pad), (right+pad, bottom+pad)), outline=(255, 0, 0), width=3)
            status = True

    del draw

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return [status, img_str]

    # You can also save a copy of the new image to disk if you want by uncommenting this line
    # pil_image.save("image_with_boxes.jpg")
