import face_recognition

import cv2
import os



image = "C:/Users/андрюшка/OneDrive/Desktop/II/Images/ДАША.bmp"
image1 ="C:/Users/андрюшка/OneDrive/Desktop/II/Images/ГРУППОВОЕ1.bmp"
image2 ="C:/Users/андрюшка/OneDrive/Desktop/II/Images/ГРУППОВОЕ2.bmp"
image3 = "C:/Users/андрюшка/OneDrive/Desktop/II/Images/ГРУППОВОЕ3.bmp"
image4= "C:/Users/андрюшка/OneDrive/Desktop/II/Images/Аня ТугубаеваНастя Колошко.jpg"
image5 = "C:/Users/андрюшка/OneDrive/Desktop/II/Images/Вера.bmp"


def GenerateEncodings(imageSrc):
    loadedImage = face_recognition.load_image_file(imageSrc)
    #print(len(face_recognition.face_locations(loadedImage)))
    if len(face_recognition.face_locations(loadedImage)) == 0:
        return "person not found"
    if len(face_recognition.face_locations(loadedImage))==1:
        encoding = face_recognition.face_encodings(loadedImage)
        return encoding
    else:
        return "so many person"

def CheckPresenceOfImage(encodingOfknown,imageSrc):
    if not isinstance(encodingOfknown,str):
        loadedImage = face_recognition.load_image_file(imageSrc)
        NumberOfPresenceOnImage =len(face_recognition.face_locations(loadedImage))
        EncodingsOnImage =face_recognition.face_encodings(loadedImage)
        #print("Number Of Presence On Image:",NumberOfPresenceOnImage)
        for PersonEncoding in EncodingsOnImage:
                if face_recognition.compare_faces(encodingOfknown,PersonEncoding)[0]:
                    return True
        return False
    else:
        return False

def CheckTwoPresenceOfImage(EncodingOfFirstKnown,EncodingOfSecondKnown,imageSrc):
    if not isinstance(EncodingOfFirstKnown,str) and not isinstance(EncodingOfSecondKnown,str):
        loadedImage = face_recognition.load_image_file(imageSrc)
        NumberOfPresenceOnImage =len(face_recognition.face_locations(loadedImage))
        #print("Number Of Presence On Image:", NumberOfPresenceOnImage)
        if NumberOfPresenceOnImage>1:
            EncodingsOnImage =face_recognition.face_encodings(loadedImage)
            for FirstPersonEncoding in EncodingsOnImage:
                    if face_recognition.compare_faces(EncodingOfFirstKnown,FirstPersonEncoding)[0]:
                        #print("все хорошо с первым")
                        for SecondPersonEncoding in EncodingsOnImage:
                            if face_recognition.compare_faces(EncodingOfSecondKnown, SecondPersonEncoding)[0]:
                                #print("оба человека найдены")
                                return True
                       # print("не нашли одного человека")
                        return False
            #print("не нашли двух человек или первого")
            return False
        else:
            #print("на фото нехватает человек")
            return False
    else:
        #print("у кого-то неправильный encoding")
        return False

if __name__ == "__main__":
    encoding = GenerateEncodings(image)
    print(encoding)
    encoding2 = GenerateEncodings(image5)
    print(encoding2)

    print("IMAGE1" * 10)
    print(CheckPresenceOfImage(encoding, image1))
    print("IMAGE2" * 10)
    print(CheckPresenceOfImage(encoding, image2))
    print("IMAGE3" * 10)
    print(CheckPresenceOfImage(encoding, image3))
    print("IMAGE4" * 10)
    print(CheckPresenceOfImage(encoding, image4))

    print("IMAGE1" * 10)
    print(CheckPresenceOfImage(encoding2, image1))
    print("IMAGE2" * 10)
    print(CheckPresenceOfImage(encoding2, image2))
    print("IMAGE3" * 10)
    print(CheckPresenceOfImage(encoding2, image3))
    print("IMAGE4" * 10)
    print(CheckPresenceOfImage(encoding2, image4))

    print("IMAGE1" * 10)
    print(CheckTwoPresenceOfImage(encoding, encoding2, image1))
    print("IMAGE2" * 10)
    print(CheckTwoPresenceOfImage(encoding, encoding2, image2))
    print("IMAGE3" * 10)
    print(CheckTwoPresenceOfImage(encoding, encoding2, image3))
    print("IMAGE4" * 10)
    print(CheckTwoPresenceOfImage(encoding, encoding2, image4))






