# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from app.models import UserSettings
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
import face_recognition
import cv2
import numpy as np
import os


def face_recog():
    video_capture = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    dirname = 'knowns'
    files = os.listdir(dirname)
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            known_face_names.append(name)
            pathname = os.path.join(dirname, filename)
            img = face_recognition.load_image_file(pathname)
            face_encoding = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(face_encoding)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    count = 0
    unknown = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:

                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                #얼굴 인식할 경우 count 1증가
                if min_value < 0.4:
                    index = np.argmin(distances)
                    name = known_face_names[index]
                    count = count +1
                else:
                    unknown = unknown +1
                face_names.append(name)
                global user_names
                user_names = name
                print(user_names)
        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)


        if count >= 10:
            video_capture.release()
            cv2.destroyAllWindows()
            return user_names

        if unknown >= 5:
            video_capture.release()
            cv2.destroyAllWindows()
            return 0


        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return 0

def login_view(request):

    #form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        #if form.is_valid():
        known_face_names = []
        dirname = 'knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                known_face_names.append(name)

        username = face_recog()

        if username in known_face_names:
            u = User.objects.get(username=username)
            if u is not None:
                login(request, u)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        # else:
        #     msg = 'Error validating the form'

    return render(request, "accounts/login.html", { "msg" : msg})


    # if request.method == "POST":
    #
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect("/")
    #         else:
    #             msg = 'Invalid credentials'
    #     else:
    #         msg = 'Error validating the form'
    #
    #return render(request, "accounts/login.html", {"form": form, "msg" : msg})


def image_capture(username):
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        cv2.imwrite('knowns/'+username+'.jpg', frame)
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    camera.release()
    cv2.destroyAllWindows()

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":

        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            image_capture(username)
            raw_password = form.cleaned_data.get("password1")

            # db
            userSettings = UserSettings(name=username)
            userSettings.save()
            print('databse: insert username in UserSettings')

            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True

            #return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })
