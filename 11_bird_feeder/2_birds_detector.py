
# coding: utf-8

# # Webcam access

# In[1]:


10%100


# In[24]:


import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")


# # Move detections simple

# In[7]:


def sent_email(img_name):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    import os
    
    #parse txt
    emails=[]
    with open('email.txt') as file:
        for line in file: emails.append(line.rstrip())
    fromaddr = emails[1]
    pwd = emails[3]
    toaddr = emails[5]
    
    #attach test.html
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE MAIL"
    # body = open('result.html',encoding='utf8').read()
    # body = "YOUR MESSAGE HERE"
    # msg.attach(MIMEText(body, 'plain'))
    
    # attach img
    #img_name = "base/0.jpg"
    img_data = open(img_name, 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename(img_name))
    msg.attach(image)
    
    #ligin and send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

import keyboard
import cv2
import time
video_capture = cv2.VideoCapture(0)
video_capture.set(3,1280)
video_capture.set(4,720)
video_capture.set(10, 0.6)
ret, frame_old = video_capture.read()
i=0
j=0
while True:
    time.sleep(0.5)
    ret, frame = video_capture.read()
    diffimg = cv2.absdiff(frame, frame_old) #Просто вычитаем старый и новый кадр
    d_s = cv2.sumElems(diffimg)
    d = (d_s[0]+d_s[1]+d_s[2])/(1280*720)
    frame_old=frame
    print (d)
#     if i>10 & i%10 == 0: 
#         print('update')
#         frame_old = video_capture.read() # обновляем базовый кадр, с которым сравниваем
    if i>30: #Первые 5-10 кадров камера выходит на режим, их надо пропустить
        if (d>14): #15 Порог срабатывания
            cv2.imwrite("base/"+str(j)+".jpg", frame) # create folder base manually
            sent_email("base/"+str(j)+".jpg")
            j=j+1
    else: i=i+1
    if keyboard.is_pressed('q'): break
print('exit')        


# # Move detection improved

# In[10]:


import keyboard
import cv2
import time
video_capture = cv2.VideoCapture(0)
video_capture.set(3,1280)
video_capture.set(4,720)
video_capture.set(10, 0.6)
ret, frame_old = video_capture.read()
i=0
j=0
while True:
    time.sleep(0.5)
    ret, frame = video_capture.read()
    diffimg = cv2.absdiff(frame, frame_old) #Просто вычитаем старый и новый кадр
    d_s = cv2.sumElems(diffimg)
    d = (d_s[0]+d_s[1]+d_s[2])/(1280*720)
    frame_old=frame
    print (d)
    if i>30: #Первые 5-10 кадров камера выходит на режим, их надо пропустить
        if (d>20):
          frame = frame[:, :, [2, 1, 0]] # Подготавливаем кадр
          transformed_image = transformer.preprocess('data', frame) # Подготавливаем кадр
          net.blobs['data'].data[0] = transformed_image # Подготавливаем сеть
          net.forward() # Запускаем сеть
          if (net.blobs['pool10'].data[0].argmax()!=0): # 0 - отсутствие цели
              misc.imsave("base/"+str(j)+"_"+
                   str(net.blobs['pool10_Q'].data[0].argmax())+".jpg",frame)
              j=j+1
          else: #Кто-то спросит: ЗАЧЕМ?!
              misc.imsave("base_d/"+str(k)+".jpg",frame)
              k=k+1
    else: i=i+1
    if keyboard.is_pressed('q'): break
print('exit')            

