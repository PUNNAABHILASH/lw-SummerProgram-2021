import cv2
import numpy as np
import os
import time
import pywhatkit as py


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):
    
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


# Open Webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    
    image, face = face_detector(frame)
    
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Pass face to prediction model
        # "results" comprises of a tuple containing the label and the confidence value
        results = model.predict(face)
       
        
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is User'
            
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)
        
        if confidence > 90:
            cv2.putText(image, "Hello!", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            cv2.imshow('Face Recognition', image )
            

	    #code for whatsapp message
            py.sendwhatmsg_instantly(f"+91{receiver_number}", message="Message sent by Face Recognition model")
            print('message sent!!')
            
            from mailer import Mailer

            mail = Mailer(email='sender_mail@gmail.com',password='sender_password')

            mail.send(receiver='receiver_mail@gmail.com',  # Email From Any service Provider
                      subject='image from face recognition',
                      message='Howdy! this is face of Obama')
            print("mail sent!!")
            
           
            break
         
        else:
           
            os.system("aws ec2 run-instances --image-id ami-0ad704c126371a549 --instance-type t2.micro --count 1 --subnet-id subnet-3455a05f --security-group-ids sg-1fba4b63 --key-name keyface> ec2.txt")
            print("Instance Launched")
            os.system("aws ec2 create-volume --availability-zone ap-south-1a --size 5 --volume-type gp2 --tag-specifications ResourceType = volume,Tags=[{Key=keyface,Value=volume}]  > ebs.txt")
            print("Volume Created")
            print("Please wait till instance is initializing")
            time.sleep(10)
            ec2_id = open("ec2.txt", 'r').read().split(',')[3].split(':')[1].split('"')[1]
            ebs_id = open("ebs.txt", 'r').read().split(',')[6].split(':')[1].split('"')[1]
            os.system("aws ec2 attach-volume --instance-id   " + ec2_id +"  --volume-id  " + ebs_id  +"  --device /dev/xvdf")
            
            break
           
            
            
            
            
           
        
            #cv2.putText(image, "I dont know you", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv2.imshow('Face Recognition', image )

    except:
        cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.putText(image, "looking for face", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.imshow('Face Recognition', image )
        pass
        
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows() 
