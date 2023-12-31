#pip install pyzbar
#pip install opencv-python
#pip install isbnlib
#pip install pandas


import cv2
from pyzbar.pyzbar import decode
import time
import isbnlib
import pandas as pd


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

used_codes = []
title_list = []
authors_list = []


camera = True
while camera == True:
    success, frame = cap.read()


    for code in decode(frame):
        if code.data.decode("utf-8") not in used_codes:
            #print("Calisiyor")
            print(code.data.decode("utf-8"))
            used_codes.append(code.data.decode("utf-8"))

            isbn = code.data.decode("utf-8")
            #book = isbnlib.meta(isbn)
            book = isbnlib.meta(isbn, service='goob')
            #print(book["Title"])
            try:
                title_list.append(book["Title"])
                #print(book["Authors"])
                authors_list.append(book["Authors"])
                #b = {"Title": book["Title"], "Authors": book["Authors"]}
                #print("Title : {}\nAuthors : {} ".format(book["Title"],book["Authors"]))
            except:
                print("Kitap bulunamadi. Elle giriş yapiniz./n")
                m_Title = input("Title :")
                m_Authors = input("Authors :")
                title_list.append(m_Title)
                authors_list.append(m_Authors)
            b = {"Title": title_list , "Authors": authors_list}

            df = pd.DataFrame(b)
            df.index +=1
            df.to_excel("kitaplar.xlsx")

            time.sleep(5)  

        elif code.data.decode("utf-8") in used_codes:
            print("ISBN Mevcuttur")  
            ###Bu hatadan sonra sürecin devam etmesi için kod eklenecek. Muhtemelen metot yazacağım.##     
        else:
            #print("Hata mevcut")
            pass


# isbn = code.data.decode("utf-8")
# book = isbnlib.meta(isbn)

# title = book["Title"]
# print(title)
# authors = book["Authors"]
#isbnlib.dev._exceptions.ISBNNotConsistentError: isbn request != isbn response (9786052229361 not in [{'type': 'ISBN_10', 'identifier': '625738706X'}, {'type': 'ISBN_13', 'identifier': '9786257387064'}])
#Üstteki hatanın sebebi ISBN numarasının kayıtlarda gerçekten bulunmamasıdır.
#isbnlib.dev._exceptions.ServiceIsDownError: the service is down (try later) (service timeout)
cv2.imshow(frame)
cv2.waitKey(1)

