import face_recognition
import numpy as np
import pickle
import click
import os
import re

def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

#
# # automatic scan specific folder, then save known_names, known_face_encodings
# # to same folder as a yaml format file.
def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)
        print('training data from {}'. format(file))

        if len(encodings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings


# use command line to control training dataset
@click.command()
@click.argument('known_people_folder')
def main(known_people_folder):
    known_face_names, known_face_encodings = scan_known_people(known_people_folder)
    # print(known_face_names, known_face_encodings)
    known_model = list(zip(known_face_encodings, known_face_names))
    #save model
    f = open('saved_model/model.yaml','wb')
    pickle.dump(known_model,f)
    f.close()



if __name__ == "__main__":
    main()
