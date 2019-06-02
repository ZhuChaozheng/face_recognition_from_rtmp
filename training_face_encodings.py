# import face_recognition
# import numpy as np
import pickle

obama_face_encoding = [[-0.1231, 0.31314, 0.12222111], [-1.12312312464, 3.538592887,-0.14313587]]
biden_face_encoding = [[-1.1231, 0.11314, 0.62222111], [-1.121112312464, 0.538592887,0.14313587]]
# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "yang",
    "zhu"
]

known_model = list(zip(known_face_encodings, known_face_names))
print(known_model)
# a = [1,2,3,4]
# b = ['x','y','x','w']
# c = list(zip(a,b))
# print(c)


#
# rfc = [known_face_encodings, known_face_names]
#
# print(rfc)
#save model
f = open('saved_model/rfc.yaml','wb')
pickle.dump(known_model,f)
f.close()
#load model
f = open('saved_model/rfc.yaml','rb')
known_model_read = pickle.load(f)
f.close()
known_face_encodings, known_face_names = zip(*known_model_read)
print(known_face_encodings, known_face_names)


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

        if len(encodings) > 1:
            click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(file))

        if len(encodings) == 0:
            click.echo("WARNING: No faces found in {}. Ignoring file.".format(file))
        else:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])

    return known_names, known_face_encodings

@click.command()
@click.argument('known_people_folder')
def main(known_people_folder):
    known_names, known_encodings = scan_known_people(known_people_folder)
    print(known_names, known_encodings)


if __name__ == "__main__":
    main()
