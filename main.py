from kivy.config import Config
Config.set('graphics','resizable',False)
from kivy.core.window import Window
Window.size = (800,600)

import pyrebase
import datetime
from random import randint

import os
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.properties import ListProperty

import sqlite3
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from Data.inference import inference

def word_search(doc_list, keyword):
    keyword=keyword.lower()
    l=len(keyword)
    c=0
    f=[]
    v=0
    for i in range(len(doc_list)):
        a=doc_list[i]
        a=a.split()
        for j in range(len(a)):
            c=0
            v=0
            for p in range(len(a[j])):
                b=a[j]
                if b[p]=="," or b[p]==".":
                    v=len(a[j])-1
            if l==len(a[j]) or l==v:
                for k in range(l):
                    b=a[j]
                    b=b.lower()
                    if keyword[k]==b[k]:
                        c+=1
                    if c==l:
                        if len(f)==0:
                            f.append(i)
                        if len(f)!=0 :
                            for z in range(len(f)):
                                if f[z]==i:
                                    break
                                else:
                                    f.append(i)

    return f


def multi_word_search(doc_list, keywords):
    keyword_to_indices = {}
    for keyword in keywords:
        keyword_to_indices[keyword] = word_search(doc_list, keyword)
    return keyword_to_indices

def Converter(Disease_prediction1):
    Model_tmp = []
    b = Disease_prediction1
    for j in range (len(b)):
        if b[j].isdigit():
            
            if b[j+1].isdigit():
                Model_tmp.append(b[j]+b[j+1])

            else:
                if b[j-1].isdigit():
                    continue
                Model_tmp.append(b[j])
    return Model_tmp

config = { Add your FireBase Config here 
                                }

Builder.load_string("""
<StartPage>:
  bcolor: 0,0,0,0
  canvas.before:
    Color:
      rgba: self.bcolor
    Rectangle:
      pos: self.pos
      size: self.size
""")
class LabelB(Label):
  bcolor = ListProperty([1,1,1,1])

class ScrollableLabel(ScrollView):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        
        self.layout = GridLayout(cols = 1,size_hint_y = None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y = None, markup = True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):
        sl = message.split('>')[1].lstrip()
        print(sl)
        incoming_message = inference(sl)
        print(message)

        self.chat_history.text += '\n' + message + '\n' + 'ALVERON >> ' + incoming_message["answers"][0]
        print(incoming_message)
        
        self.layout.height  = self.chat_history.texture_size[1] +15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)

        self.scroll_to(self.scroll_to_point)
      

class StartPage(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)


        os.environ["pause_on_minimize"] = "1"
        self.cols = 1
        self.rows = 4
        transition = FadeTransition()

        abc=Image(source='Graphics/StartPage/abc2.png')
        self.add_widget(abc)
        abc=Image(source='Graphics/StartPage/abc.png')
        self.add_widget(abc)
        abc=Image(source='Graphics/StartPage/abc3.png')
        self.add_widget(abc)

        self.login = Button(text = "Login")
        self.login.bind(on_press = self.login_button)

        self.signup = Button(text = "Signup")
        self.signup.bind(on_press = self.signup_button)

        self.offline = Button(text = "Run Offline")
        self.offline.bind(on_press = self.offline_button)

        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)

        bottom_line = GridLayout(cols=4)
        bottom_line.add_widget(self.login)
        bottom_line.add_widget(self.signup)
        bottom_line.add_widget(self.offline)
        bottom_line.add_widget(self.quit)
        self.add_widget(bottom_line)


    def signup_button(self , instance):
        MDRDS.screen_manager.current = "HomeS"

    def login_button(self , instance):
        MDRDS.screen_manager.current = "HomeL"

    def offline_button(self , instance):
        pass
        """MDRDS.screen_manager.current = "AboutO" """
        
    def quit_button(self , instance):
        App.get_running_app().stop()
        

class LoginError(GridLayout):
        def __init__(self , **kwargs):
            super().__init__(**kwargs)
            self.cols = 3
            abc=Image(source='Graphics/LoginError/(1,3).png')
            self.add_widget(abc)
            abc1=Image(source='Graphics/LoginError/(1,2).png')
            self.add_widget(abc1)
            abc2=Image(source='Graphics/LoginError/(1,1).png')
            self.add_widget(abc2)

            abc3=Image(source='Graphics/LoginError/(1,1)h.png')
            self.add_widget(abc3)
            self.back = Button(text = "Go Back")
            self.back.bind(on_press = self.back_button)
            self.add_widget(self.back)
            abc4=Image(source='Graphics/LoginError/(1,1)h.png')
            self.add_widget(abc4)
            
            abc5=Image(source='Graphics/LoginError/(1,1).png')
            self.add_widget(abc5)
            abc6=Image(source='Graphics/LoginError/(1,1).png')
            self.add_widget(abc6)
            abc7=Image(source='Graphics/LoginError/(1,1).png')
            self.add_widget(abc7)

        def back_button(self , instance):
            MDRDS.screen_manager.current = "HomeL"

        

class SignUpError(GridLayout):
        def __init__(self , **kwargs):
            super().__init__(**kwargs)
            self.cols = 3
            abc=Image(source='Graphics/SignUpError/(1,3).png')
            self.add_widget(abc)
            abc1=Image(source='Graphics/SignUpError/(1,2).png')
            self.add_widget(abc1)
            abc2=Image(source='Graphics/SignUpError/(1,1).png')
            self.add_widget(abc2)

            abc3=Image(source='Graphics/SignUpError/(1,1)h.png')
            self.add_widget(abc3)
            self.back = Button(text = "Go Back")
            self.back.bind(on_press = self.back_button)
            self.add_widget(self.back)
            abc4=Image(source='Graphics/SignUpError/(1,1)h.png')
            self.add_widget(abc4)

            abc5=Image(source='Graphics/SignUpError/(1,1).png')
            self.add_widget(abc5)
            abc6=Image(source='Graphics/SignUpError/(1,1).png')
            self.add_widget(abc6)
            abc7=Image(source='Graphics/SignUpError/(1,1).png')
            self.add_widget(abc7)

        def back_button(self , instance):
            MDRDS.screen_manager.current = "HomeS"

class FPE(GridLayout):
        def __init__(self , **kwargs):
            super().__init__(**kwargs)
            self.cols = 3
            abc=Image(source='Graphics/FPE/(1,3).png')
            self.add_widget(abc)
            abc1=Image(source='Graphics/FPE/(1,2).png')
            self.add_widget(abc1)
            abc2=Image(source='Graphics/FPE/(1,1).png')
            self.add_widget(abc2)

            abc3=Image(source='Graphics/FPE/(1,1)h.png')
            self.add_widget(abc3)
            self.back = Button(text = "Go Back")
            self.back.bind(on_press = self.back_button)
            self.add_widget(self.back)
            abc4=Image(source='Graphics/FPE/(1,1)h.png')
            self.add_widget(abc4)

            abc5=Image(source='Graphics/FPE/(1,1).png')
            self.add_widget(abc5)
            abc6=Image(source='Graphics/FPE/(1,1).png')
            self.add_widget(abc6)
            abc7=Image(source='Graphics/FPE/(1,1).png')
            self.add_widget(abc7)

        def back_button(self , instance):
            MDRDS.screen_manager.current = "HomeL"
        


class Verification1(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        abc=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/Verification1/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc2)

        abc3=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc3)
        abc5=Image(source='Graphics/Verification1/(3,2).png')
        self.add_widget(abc5)
        abc4=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc4)

        abc9=Image(source='Graphics/Verification1/(4,1).png')
        self.add_widget(abc9)
        self.login = TextInput(multiline = False)
        self.add_widget(self.login)
        abc6=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc6)

        abc10=Image(source='Graphics/Verification1/(5,1).png')
        self.add_widget(abc10)
        self.password = TextInput(multiline = False)
        self.add_widget(self.password)
        abc7=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc7)


        abc12=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc12)
        self.submit = Button(text = "Re-send Verification Mail")
        self.submit.bind(on_press = self.submit_button)
        self.add_widget(self.submit)
        abc8=Image(source='Graphics/Verification1/(1,1)p.png')
        self.add_widget(abc8)

    def submit_button(self , instance):
        EMAIL = self.login.text
        PASSWORD = self.password.text

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()

        try:
            signin = auth.sign_in_with_email_and_password(EMAIL,PASSWORD)
            auth.send_email_verification(signin['idToken'])
            MDRDS.screen_manager.current = "HomeL"

        except:
            MDRDS.screen_manager.current = "FPE"

        
class HomePageLogin(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        abc=Image(source='Graphics/HomePageLogin/(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/HomePageLogin/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/HomePageLogin/(1,1).png')
        self.add_widget(abc2)

        abc3=Image(source='Graphics/HomePageLogin/(2,1).png')
        self.add_widget(abc3)
        self.login = TextInput(multiline = False)
        self.add_widget(self.login)
        abc11=Image(source='Graphics/HomePageLogin/1.png')
        self.add_widget(abc11)

        abc4=Image(source='Graphics/HomePageLogin/(3,1).png')
        self.add_widget(abc4)
        self.password = TextInput(multiline = False ,password = True)
        self.add_widget(self.password)
        abc12=Image(source='Graphics/HomePageLogin/2.png')
        self.add_widget(abc12)

        abc6=Image(source='Graphics/HomePageLogin/(6,1).png')
        self.add_widget(abc6)
        self.fp_page = Button(text = "Forgot Password")
        self.fp_page.bind(on_press = self.fp_button)
        self.add_widget(self.fp_page)
        abc13=Image(source='Graphics/HomePageLogin/3.png')
        self.add_widget(abc13)

        abc7=Image(source='Graphics/HomePageLogin/(7,1).png')
        self.add_widget(abc7)
        abc5=Image(source='Graphics/HomePageLogin/(5,2).png')
        self.add_widget(abc5)
        abc14=Image(source='Graphics/HomePageLogin/4.png')
        self.add_widget(abc14)


        abc8=Image(source='Graphics/HomePageLogin/(8,1).png')
        self.add_widget(abc8)
        self.submit = Button(text = "Login")
        self.submit.bind(on_press = self.submit_button)
        self.add_widget(self.submit)
        abc15=Image(source='Graphics/HomePageLogin/5.png')
        self.add_widget(abc15)

        abc9=Image(source='Graphics/HomePageLogin/(5,2).png')
        self.add_widget(abc9)
        self.Signup_page = Button(text = "Don't have an account,\nSignup Now!!!!")
        self.Signup_page.bind(on_press = self.sign_up_page_button)
        self.add_widget(self.Signup_page)
        abc16=Image(source='Graphics/HomePageLogin/6.png')
        self.add_widget(abc16)

        abc10=Image(source='Graphics/HomePageLogin/(5,2).png')
        self.add_widget(abc10)
        self.offline = Button(text = "Run Offline")
        self.offline.bind(on_press = self.offline_button)
        self.add_widget(self.offline)
        abc17=Image(source='Graphics/HomePageLogin/(5,2).png')
        self.add_widget(abc17)
        

    def submit_button(self , instance):
        def changer(Email):
            a = ''
            for i in range(len(Email)):
                if Email[i].isdigit() or Email[i].isalpha():
                    a += Email[i]
            return a
        
        e = 0
        EMAIL = self.login.text
        print(EMAIL)
        Email = (changer(EMAIL)).lower()
        print(Email)
        PASSWORD = self.password.text
        print(PASSWORD)

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        try:
            signin = auth.sign_in_with_email_and_password(EMAIL,PASSWORD)
            ef = auth.get_account_info(signin['idToken'])
            ef = ef['users'][0]['emailVerified']    
        except:
            e = 1
           
        if e==0:
            MDRDS.result.User(Email.lower())
            MDRDS.doctor.User(Email.lower())
            MDRDS.about_page.User(Email)
            MDRDS.your_record.User(Email)
            MDRDS.account_page.User(Email)
            MDRDS.diagnosis_page.User(Email)
            MDRDS.result1.User(Email)
            MDRDS.account_page.update_ef(ef)


            MDRDS.screen_manager.current = "Diagnosis"
        if e==1:
            MDRDS.screen_manager.current = "LE"
            
    def sign_up_page_button(self , instance):
        MDRDS.screen_manager.current = "HomeS"

    def fp_button(self , instance):
        MDRDS.screen_manager.current = "HomeFP"

    def offline_button(self , instance):
        pass
        """MDRDS.screen_manager.current = "AboutO" """

        
class HomePageSignUp(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        Config.set('graphics', 'resizable', False)

        abc=Image(source='Graphics/HomePageSignUp/s(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/HomePageSignUp/s(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/HomePageSignUp/s(1,1).png')
        self.add_widget(abc2)

        abc3=Image(source='Graphics/HomePageSignUp/s(2,1).png')
        self.add_widget(abc3)
        self.user = TextInput(multiline = False)
        self.add_widget(self.user)
        abc11=Image(source='Graphics/HomePageSignUp/s1.png')
        self.add_widget(abc11)

        abc4=Image(source='Graphics/HomePageSignUp/s(3,1).png')
        self.add_widget(abc4)
        self.age = TextInput(multiline = False)
        self.add_widget(self.age)
        abc12=Image(source='Graphics/HomePageSignUp/s2.png')
        self.add_widget(abc12)

        abc5=Image(source='Graphics/HomePageSignUp/s(4,1).png')
        self.add_widget(abc5)
        self.gender = TextInput(multiline = False)
        self.add_widget(self.gender)
        abc13=Image(source='Graphics/HomePageSignUp/s3.png')
        self.add_widget(abc13)

        abc5=Image(source='Graphics/HomePageSignUp/s(5,1).png')
        self.add_widget(abc5)
        self.signup = TextInput(multiline = False)
        self.add_widget(self.signup)
        abc14=Image(source='Graphics/HomePageSignUp/s4.png')
        self.add_widget(abc14)


        abc6=Image(source='Graphics/HomePageSignUp/s(6,1).png')
        self.add_widget(abc6)
        self.password = TextInput(multiline = False)
        self.add_widget(self.password)
        abc15=Image(source='Graphics/HomePageSignUp/s5.png')
        self.add_widget(abc15)

        abc7=Image(source='Graphics/HomePageSignUp/s(cl,1).png')
        self.add_widget(abc7)
        abc8=Image(source='Graphics/HomePageSignUp/s(cl,1).png')
        self.add_widget(abc8)
        abc16=Image(source='Graphics/HomePageSignUp/s6.png')
        self.add_widget(abc16)


        abc9=Image(source='Graphics/HomePageSignUp/s(c,1).png')
        self.add_widget(abc9)
        self.submit = Button(text = "SignUp")
        self.submit.bind(on_press = self.submit_button)
        self.add_widget(self.submit)
        abc17=Image(source='Graphics/HomePageSignUp/s(c,1).png')
        self.add_widget(abc17)

        abc10=Image(source='Graphics/HomePageSignUp/s(c,1).png')
        self.add_widget(abc10)
        self.login_page = Button(text = "Already have an account,\nLogin Now!!!!")
        self.login_page.bind(on_press = self.Login_page_button)
        self.add_widget(self.login_page)
        abc17=Image(source='Graphics/HomePageSignUp/s(c,1).png')
        self.add_widget(abc17)

        

    def submit_button(self , instance):
        def changer(Email):
            a = ''
            for i in range(len(Email)):
                if Email[i].isdigit() or Email[i].isalpha():
                    a += Email[i]
            return a
        
        e = 0
        EMAIL = self.signup.text
        print(EMAIL)
        Email = (changer(EMAIL)).lower()
        print(Email)
        PASSWORD = self.password.text
        print(PASSWORD)
        USER = self.user.text
        AGE = self.age.text
        GENDER = self.gender.text
        

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        db = firebase.database()

        try:
            signup = auth.create_user_with_email_and_password(EMAIL , PASSWORD)
            data = {"Name":USER}
            db.child("MedApp").child("Users").child(Email.lower()).set(data)
            data1 = {AGE:GENDER}
            db.child("MedApp").child("Details").child("AgeGender").child(Email.lower()).set(data1)
            Data0 = {"Disease":"None"}
            Data2 = {"Disease":"None"}
            Data3 = {"Disease":"None"}
            Data4 = {"Disease":"None"}
            Data = {"Model_features":"None"}
            Data1 = {"Date": "None"}
            db.child("MedApp").child("Diagnosis").child("Disease").child(Email).child("GR").set(Data0)
            db.child("MedApp").child("Diagnosis").child("Disease").child(Email).child("MR").set(Data2)
            db.child("MedApp").child("Diagnosis").child("Disease").child(Email).child("BR").set(Data3)
            db.child("MedApp").child("Diagnosis").child("Disease").child(Email).child("LR").set(Data4)
            db.child("MedApp").child("ModelFeatures").child(Email).set(Data)            
            db.child("MedApp").child("Time").child(Email).set(Data1)
            auth.send_email_verification(signup['idToken'])
            ef = auth.get_account_info(signup['idToken'])
            ef = ef['users'][0]['emailVerified']

            
        except:
            e=1

            
        if e==0:
            MDRDS.result.User(Email.lower())
            MDRDS.doctor.User(Email.lower())
            MDRDS.about_page.User(Email.lower())
            MDRDS.your_record.User(Email.lower())
            MDRDS.account_page.User(Email.lower())
            MDRDS.result1.User(Email.lower())
            MDRDS.diagnosis_page.User(Email.lower())
            MDRDS.account_page.update_ef(ef)
            MDRDS.screen_manager.current = "Verification"
        if e==1:
            MDRDS.screen_manager.current = "SE"

    def Login_page_button(self , instance):
        MDRDS.screen_manager.current = "HomeL"

class Verification(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        abc=Image(source='Graphics/Verification/(1,1)s.png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/Verification/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/Verification/(1,1).png')
        self.add_widget(abc2)

        abc3=Image(source='Graphics/Verification/(1,1)l.png')
        self.add_widget(abc3)
        self.con = Button(text = "Continue")
        self.con.bind(on_press = self.con_button)
        self.add_widget(self.con)
        abc4=Image(source='Graphics/Verification/(1,1)l.png')
        self.add_widget(abc4)

        abc5=Image(source='Graphics/Verification/(1,1).png')
        self.add_widget(abc5)
        abc6=Image(source='Graphics/Verification/(1,1).png')
        self.add_widget(abc6)
        abc7=Image(source='Graphics/Verification/(1,1).png')
        self.add_widget(abc7)

    def con_button(self , instance):
        MDRDS.screen_manager.current = "HomeL"
            
        



class HomePageFP(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        abc=Image(source='Graphics/HomePageFP/(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/HomePageFP/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/HomePageFP/(1,1).png')
        self.add_widget(abc2)

        abc3=Image(source='Graphics/HomePageFP/(2,1).png')
        self.add_widget(abc3)
        self.Fp_email = TextInput(multiline = False)
        self.add_widget(self.Fp_email)
        abc10=Image(source='Graphics/HomePageFP/(2,3).png')
        self.add_widget(abc10)

        abc4=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc4)
        self.fp_button1 = Button(text = "Submit")
        self.fp_button1.bind(on_press = self.fp_button2)
        self.add_widget(self.fp_button1)
        abc11=Image(source='Graphics/HomePageFP/(3,3).png')
        self.add_widget(abc11)


        abc5=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc5)
        abc6=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc6)
        abc9=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc9)

        abc7=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc7)
        self.back = Button(text = "Back")
        self.back.bind(on_press = self.back_button)
        self.add_widget(self.back)
        abc8=Image(source='Graphics/HomePageFP/(1,1)p.png')
        self.add_widget(abc8)


    def fp_button2(self , instance):
        e = 0
        EMAIL = self.Fp_email.text

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        try:
            auth.send_password_reset_email(EMAIL)
        except:
            e=1
        if e==0:
            MDRDS.screen_manager.current = "HomeL"
        if e==1:
            MDRDS.screen_manager.current = "FPE"

    def back_button(sef , instance):
        MDRDS.screen_manager.current = "HomeL"


class Analysis(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
        
        self.add_widget(Label())
        self.add_widget(Label(text = 'Click on Analyse Button to\nPredict your Disease'))
        self.add_widget(Label())
        self.add_widget(Label())
        self.analysis = Button(text = "Analyse")
        self.analysis.bind(on_press = self.analysis_button)
        self.add_widget(self.analysis)

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        


    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)

    def analysis_button(self , instance):
        try:
        
            with open('Diseases.txt') as input_file:
                Diseases_list = [line.strip() for line in input_file]
            
            Model_features1 = list(self.Model_features.text)
            Model_features = Converter(Model_features1)
        
            Symptoms_X_Diseases_path = "Symptoms X Diseases.csv"
            Diagnostic_Data = pd.read_csv(Symptoms_X_Diseases_path)
            Diagnostic_Data = Diagnostic_Data.dropna(axis=0)
    
            X = Diagnostic_Data[Model_features]
            y = Diagnostic_Data.Index
            train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 1)
            Model_diagnostic = DecisionTreeRegressor(random_state=1)
    
            Model_diagnostic.fit(X,y)
            predict = Model_diagnostic.predict(X)
            l = list(predict)
            Disease_prediction = []
            for w in range(len(l)):
                if l[w]== float(w):
                    Disease_prediction.append(w)

            MDRDS.prediction_page.update(Disease_prediction)
            MDRDS.prediction_page.update1(Model_features)
            MDRDS.screen_manager.current = "Prediction"
        except:
            MDRDS.screen_manager.current = "Error"

class Error(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.add_widget(Label())

        self.add_widget(Label(text ="An Error Has Occured\nReport To The Develepors"))
        self.add_widget(Label())
        self.add_widget(Label())
        
        self.error = Button(text = 'Back to Login Page')
        self.error.bind(on_press = self.error_button)
        self.add_widget(self.error)
        self.add_widget(Label())

        self.add_widget(Label())

    def error_button(self, instance):
        MDRDS.screen_manager.current = "HomeL"
        

class Prediction(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()


        self.add_widget(Label())

        self.predict_text = Label(text = "To Predict The Disease Accurately\nAnswer the Questions")
        self.add_widget(self.predict_text)

        self.add_widget(Label())
        self.add_widget(Label())

        self.predict = Button(text = "Continue")
        self.predict.bind(on_press = self.predict_button)
        self.add_widget(self.predict)

        self.add_widget(Label())
        self.add_widget(Label())


    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def predict_button(self , instance):
      
        
        Disease_prediction1 = list(self.Disease_prediction.text)
        Disease_prediction = Converter(Disease_prediction1)

        Model_features1= list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        
        with open('Symptoms X Diseases.txt') as input_file:
            SXD = [line.strip() for line in input_file]

        
        DPA = []
        for i in range(len(Disease_prediction)):
            for j in range(len(SXD)):
                if j == int(Disease_prediction[i]):
                    for f in range(len(SXD[i])):
                        DPA.append(SXD[j])
        DPA1 = []
        [DPA1.append(x) for x in DPA if x not in DPA1]
        DPA2 = []
        for i in range(len(DPA1)):
            for j in range(len(DPA1[i])):
                if DPA1[i][j].isdigit():
                    if j < len(DPA1[i])-1:
                        if DPA1[i][j+1].isdigit():
                           DPA2.append(DPA1[i][j]+DPA1[i][j+1])

                        else:
                            if DPA1[i][j-1].isdigit():
                                continue
                            DPA2.append(DPA1[i][j])
                    else:
                        DPA2.append(DPA1[i][j])

        DPA3 = []
        [DPA3.append(x) for x in DPA2 if x not in DPA3]
        DPA4 = set(DPA3) - set(Model_features)
        DPA4 = list(DPA4)
        
        DPA4.sort(reverse = True)
        DPA5 = []
        [DPA5.append(x) for x in DPA4 if x not in DPA5]
        tmp1 = []
        length = len(tmp1)
        DPA5.sort(reverse = True)
        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
        for z in range (25):
            if length < 25 :
                tmp1.append(Main_symptom_list[randint(51,96)])

        for i in DPA5:
            tmp1.append(Main_symptom_list[int(i)])




        MDRDS.aquestion.update(Disease_prediction)
        MDRDS.aquestion.update1(Model_features)
        MDRDS.aquestion.update2(DPA1)
        MDRDS.aquestion.update3(DPA5)
        
        MDRDS.aquestion.update4(tmp1)
        MDRDS.aquestion1.update4(tmp1)
        MDRDS.aquestion2.update4(tmp1)
        MDRDS.aquestion3.update4(tmp1)
        MDRDS.aquestion4.update4(tmp1)
        MDRDS.aquestion5.update4(tmp1)
        MDRDS.aquestion6.update4(tmp1)
        MDRDS.aquestion7.update4(tmp1)
        MDRDS.aquestion8.update4(tmp1)
        MDRDS.aquestion9.update4(tmp1)
        MDRDS.aquestion10.update4(tmp1)
        MDRDS.aquestion11.update4(tmp1)
        MDRDS.aquestion12.update4(tmp1)
        MDRDS.aquestion13.update4(tmp1)
        MDRDS.aquestion14.update4(tmp1)
        MDRDS.aquestion15.update4(tmp1)
        MDRDS.aquestion16.update4(tmp1)
        MDRDS.aquestion17.update4(tmp1)
        MDRDS.aquestion18.update4(tmp1)
        MDRDS.aquestion19.update4(tmp1)
        MDRDS.aquestion20.update4(tmp1)
        MDRDS.aquestion21.update4(tmp1)
        MDRDS.aquestion22.update4(tmp1)
        MDRDS.aquestion23.update4(tmp1)
        MDRDS.aquestion24.update4(tmp1)

        MDRDS.screen_manager.current = "AQuestions"
        
class AQuestions(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()

        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[0]

    def yes_button(self, instance):



        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion1.update(Disease_prediction)
        MDRDS.aquestion1.update1(Model_features)
        MDRDS.aquestion1.update2(DPA1)
        MDRDS.aquestion1.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions1"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion1.update(Disease_prediction)
        MDRDS.aquestion1.update1(Model_features)
        MDRDS.aquestion1.update2(DPA1)
        MDRDS.aquestion1.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions1"
      
class AQuestions1(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[1]

    def yes_button(self, instance):

        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
        MDRDS.aquestion2.update(Disease_prediction)
        MDRDS.aquestion2.update1(Model_features)
        MDRDS.aquestion2.update2(DPA1)
        MDRDS.aquestion2.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions2"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion2.update(Disease_prediction)
        MDRDS.aquestion2.update1(Model_features)
        MDRDS.aquestion2.update2(DPA1)
        MDRDS.aquestion2.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions2"

class AQuestions2(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[2]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion3.update(Disease_prediction)
        MDRDS.aquestion3.update1(Model_features)
        MDRDS.aquestion3.update2(DPA1)
        MDRDS.aquestion3.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions3"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion3.update(Disease_prediction)
        MDRDS.aquestion3.update1(Model_features)
        MDRDS.aquestion3.update2(DPA1)
        MDRDS.aquestion3.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions3"

class AQuestions3(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[3]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion4.update(Disease_prediction)
        MDRDS.aquestion4.update1(Model_features)
        MDRDS.aquestion4.update2(DPA1)
        MDRDS.aquestion4.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions4"

                

    def no_button(self , instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion4.update(Disease_prediction)
        MDRDS.aquestion4.update1(Model_features)
        MDRDS.aquestion4.update2(DPA1)
        MDRDS.aquestion4.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions4"

class AQuestions4(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[4]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion5.update(Disease_prediction)
        MDRDS.aquestion5.update1(Model_features)
        MDRDS.aquestion5.update2(DPA1)
        MDRDS.aquestion5.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions5"

                

    def no_button(self , instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion5.update(Disease_prediction)
        MDRDS.aquestion5.update1(Model_features)
        MDRDS.aquestion5.update2(DPA1)
        MDRDS.aquestion5.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions5"

class AQuestions5(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[5]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion6.update(Disease_prediction)
        MDRDS.aquestion6.update1(Model_features)
        MDRDS.aquestion6.update2(DPA1)
        MDRDS.aquestion6.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions6"

                

    def no_button(self , instance):
  
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion6.update(Disease_prediction)
        MDRDS.aquestion6.update1(Model_features)
        MDRDS.aquestion6.update2(DPA1)
        MDRDS.aquestion6.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions6"

class AQuestions6(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[6]

    def yes_button(self, instance):


        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion7.update(Disease_prediction)
        MDRDS.aquestion7.update1(Model_features)
        MDRDS.aquestion7.update2(DPA1)
        MDRDS.aquestion7.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions7"

                

    def no_button(self , instance):
       
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion7.update(Disease_prediction)
        MDRDS.aquestion7.update1(Model_features)
        MDRDS.aquestion7.update2(DPA1)
        MDRDS.aquestion7.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions7"

class AQuestions7(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[7]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion8.update(Disease_prediction)
        MDRDS.aquestion8.update1(Model_features)
        MDRDS.aquestion8.update2(DPA1)
        MDRDS.aquestion8.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions8"

                

    def no_button(self , instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion8.update(Disease_prediction)
        MDRDS.aquestion8.update1(Model_features)
        MDRDS.aquestion8.update2(DPA1)
        MDRDS.aquestion8.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions8"

class AQuestions8(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[8]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion9.update(Disease_prediction)
        MDRDS.aquestion9.update1(Model_features)
        MDRDS.aquestion9.update2(DPA1)
        MDRDS.aquestion9.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions9"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion9.update(Disease_prediction)
        MDRDS.aquestion9.update1(Model_features)
        MDRDS.aquestion9.update2(DPA1)
        MDRDS.aquestion9.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions9"
        
class AQuestions9(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[9]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion10.update(Disease_prediction)
        MDRDS.aquestion10.update1(Model_features)
        MDRDS.aquestion10.update2(DPA1)
        MDRDS.aquestion10.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions10"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion10.update(Disease_prediction)
        MDRDS.aquestion10.update1(Model_features)
        MDRDS.aquestion10.update2(DPA1)
        MDRDS.aquestion10.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions10"
    
            
class AQuestions10(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[10]

    def yes_button(self, instance):
       
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion11.update(Disease_prediction)
        MDRDS.aquestion11.update1(Model_features)
        MDRDS.aquestion11.update2(DPA1)
        MDRDS.aquestion11.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions11"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion11.update(Disease_prediction)
        MDRDS.aquestion11.update1(Model_features)
        MDRDS.aquestion11.update2(DPA1)
        MDRDS.aquestion11.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions11"

class AQuestions11(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[11]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion12.update(Disease_prediction)
        MDRDS.aquestion12.update1(Model_features)
        MDRDS.aquestion12.update2(DPA1)
        MDRDS.aquestion12.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions12"

                

    def no_button(self , instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion12.update(Disease_prediction)
        MDRDS.aquestion12.update1(Model_features)
        MDRDS.aquestion12.update2(DPA1)
        MDRDS.aquestion12.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions12"

class AQuestions12(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[12]

    def yes_button(self, instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion13.update(Disease_prediction)
        MDRDS.aquestion13.update1(Model_features)
        MDRDS.aquestion13.update2(DPA1)
        MDRDS.aquestion13.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions13"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion13.update(Disease_prediction)
        MDRDS.aquestion13.update1(Model_features)
        MDRDS.aquestion13.update2(DPA1)
        MDRDS.aquestion13.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions13"

class AQuestions13(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[13]

    def yes_button(self, instance):

        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion14.update(Disease_prediction)
        MDRDS.aquestion14.update1(Model_features)
        MDRDS.aquestion14.update2(DPA1)
        MDRDS.aquestion14.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions14"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion14.update(Disease_prediction)
        MDRDS.aquestion14.update1(Model_features)
        MDRDS.aquestion14.update2(DPA1)
        MDRDS.aquestion14.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions14"

class AQuestions14(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[14]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion15.update(Disease_prediction)
        MDRDS.aquestion15.update1(Model_features)
        MDRDS.aquestion15.update2(DPA1)
        MDRDS.aquestion15.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions15"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion15.update(Disease_prediction)
        MDRDS.aquestion15.update1(Model_features)
        MDRDS.aquestion15.update2(DPA1)
        MDRDS.aquestion15.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions15"

class AQuestions15(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[15]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion16.update(Disease_prediction)
        MDRDS.aquestion16.update1(Model_features)
        MDRDS.aquestion16.update2(DPA1)
        MDRDS.aquestion16.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions16"

                

    def no_button(self , instance):
        
        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion16.update(Disease_prediction)
        MDRDS.aquestion16.update1(Model_features)
        MDRDS.aquestion16.update2(DPA1)
        MDRDS.aquestion16.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions16"

class AQuestions16(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[16]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion17.update(Disease_prediction)
        MDRDS.aquestion17.update1(Model_features)
        MDRDS.aquestion17.update2(DPA1)
        MDRDS.aquestion17.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions17"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion17.update(Disease_prediction)
        MDRDS.aquestion17.update1(Model_features)
        MDRDS.aquestion17.update2(DPA1)
        MDRDS.aquestion17.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions17"

class AQuestions17(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[17]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion18.update(Disease_prediction)
        MDRDS.aquestion18.update1(Model_features)
        MDRDS.aquestion18.update2(DPA1)
        MDRDS.aquestion18.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions18"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion18.update(Disease_prediction)
        MDRDS.aquestion18.update1(Model_features)
        MDRDS.aquestion18.update2(DPA1)
        MDRDS.aquestion18.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions18"

class AQuestions18(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[18]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion19.update(Disease_prediction)
        MDRDS.aquestion19.update1(Model_features)
        MDRDS.aquestion19.update2(DPA1)
        MDRDS.aquestion19.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions19"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion19.update(Disease_prediction)
        MDRDS.aquestion19.update1(Model_features)
        MDRDS.aquestion19.update2(DPA1)
        MDRDS.aquestion19.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions19"


class AQuestions19(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[19]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion20.update(Disease_prediction)
        MDRDS.aquestion20.update1(Model_features)
        MDRDS.aquestion20.update2(DPA1)
        MDRDS.aquestion20.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions20"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion20.update(Disease_prediction)
        MDRDS.aquestion20.update1(Model_features)
        MDRDS.aquestion20.update2(DPA1)
        MDRDS.aquestion20.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions20"

class AQuestions20(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[20]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion21.update(Disease_prediction)
        MDRDS.aquestion21.update1(Model_features)
        MDRDS.aquestion21.update2(DPA1)
        MDRDS.aquestion21.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions21"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion21.update(Disease_prediction)
        MDRDS.aquestion21.update1(Model_features)
        MDRDS.aquestion21.update2(DPA1)
        MDRDS.aquestion21.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions21"

class AQuestions21(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[21]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion22.update(Disease_prediction)
        MDRDS.aquestion22.update1(Model_features)
        MDRDS.aquestion22.update2(DPA1)
        MDRDS.aquestion22.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions22"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion22.update(Disease_prediction)
        MDRDS.aquestion22.update1(Model_features)
        MDRDS.aquestion22.update2(DPA1)
        MDRDS.aquestion22.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions22"

class AQuestions22(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[22]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion23.update(Disease_prediction)
        MDRDS.aquestion23.update1(Model_features)
        MDRDS.aquestion23.update2(DPA1)
        MDRDS.aquestion23.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions23"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion23.update(Disease_prediction)
        MDRDS.aquestion23.update1(Model_features)
        MDRDS.aquestion23.update2(DPA1)
        MDRDS.aquestion23.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions23"

class AQuestions23(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()


        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[23]

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.aquestion24.update(Disease_prediction)
        MDRDS.aquestion24.update1(Model_features)
        MDRDS.aquestion24.update2(DPA1)
        MDRDS.aquestion24.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions24"

                

    def no_button(self , instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.aquestion24.update(Disease_prediction)
        MDRDS.aquestion24.update1(Model_features)
        MDRDS.aquestion24.update2(DPA1)
        MDRDS.aquestion24.update3(DPA4)
        MDRDS.screen_manager.current = "AQuestions24"

class AQuestions24(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.tmp1 = Label()
        self.tmp2 = Label()
        self.offline = Label()



        self.add_widget(Label())
        self.add_widget(Label(text = "Do You Experience The Following"))
        self.add_widget(Label())

        self.add_widget(Label())

        
        self.add_widget(self.tmp1)
        self.add_widget(Label())

        self.add_widget(Label())
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)

        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)
        
    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def update4(self, tmp1):
        self.tmp1.text = tmp1[24]

    def offline_update(self , offline):
        self.offline.text = str(offline)

    def yes_button(self, instance):

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))
        tmp1 = (self.tmp1.text)
        offline = self.offline.text

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp1
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])
        
                      

        MDRDS.result.update(Disease_prediction)
        MDRDS.result.update1(Model_features)
        MDRDS.result.update2(DPA1)
        MDRDS.result.update3(DPA4)

        if offline == "1":
            MDRDS.screen_manager.current = "ResultO"
        if offline == "0":            
            MDRDS.screen_manager.current = "Result"

                

    def no_button(self , instance):
        offline = self.offline.text

        Disease_prediction = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))

        MDRDS.result.update(Disease_prediction)
        MDRDS.result.update1(Model_features)
        MDRDS.result.update2(DPA1)
        MDRDS.result.update3(DPA4)

        MDRDS.resulto.update(Disease_prediction)
        MDRDS.resulto.update1(Model_features)
        MDRDS.resulto.update2(DPA1)
        MDRDS.resulto.update3(DPA4)

        if offline == "1":
            MDRDS.screen_manager.current = "ResultO"
        if offline == "0":            
            MDRDS.screen_manager.current = "Result"


        


class DiagnosisPageOffline(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4        

        self.about = Button(text = "About")
        self.about.bind(on_press = self.about_button)
        self.add_widget(self.about)
        self.add_widget(Label())

        self.diagnosis_text = Label(text = "Diagnosis: Predict Your Disease \n By Entering the Symptom")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())

        self.login = Button(text = "Login")
        self.login.bind(on_press = self.login_button)
        self.add_widget(self.login)
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Enter Symptoms :")
        self.add_widget(self.enter_symptom_text)

        self.Enter_Symptoms = TextInput(multiline = False)
        self.add_widget(self.Enter_Symptoms)

        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)

        self.add_widget(Label())

        self.add_widget(Label())
        self.submit = Button(text = "Submit")
        self.submit.bind(on_press = self.submit_button)
        self.add_widget(self.submit)


        self.add_widget(Label())
        self.add_widget(Label(text = 'Not Working'))
        self.add_widget(Label())



        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label(text = "WRITE SYMPTOMS ONLY. AVOID\nSPACES BETWEEN MULTIWORD SYMPTOMS"))
        


    def about_button(self , instance):
        MDRDS.screen_manager.current = "AboutO"

    def login_button(self , instance):
        MDRDS.screen_manager.current = "Start"

    def quit_button(self , instance):
        App.get_running_app().stop()

    def submit_button(self , instance):

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = self.Enter_Symptoms.text
        keywords = Enter_Symptoms.split()
        Model_features = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)
        
        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features.append(str(Features_temp[keywords[i]][0]))
                
        with open('_0.txt') as input_file:
            _0 = [line.strip() for line in input_file]
        with open('_5.txt') as input_file:
            _5 = [line.strip() for line in input_file]
        with open('_12.txt') as input_file:
            _12 = [line.strip() for line in input_file]
        with open('_15.txt') as input_file:
            _15 = [line.strip() for line in input_file]
        with open('_17.txt') as input_file:
            _17 = [line.strip() for line in input_file]
        with open('_19.txt') as input_file:
            _19 = [line.strip() for line in input_file]
        with open('_20.txt') as input_file:
            _20 = [line.strip() for line in input_file]
        with open('_24.txt') as input_file:
            _24 = [line.strip() for line in input_file]
        with open('_26.txt') as input_file:
            _26 = [line.strip() for line in input_file]
        with open('_42.txt') as input_file:
            _42 = [line.strip() for line in input_file]
        with open('_43.txt') as input_file:
            _43 = [line.strip() for line in input_file]
        with open('_47.txt') as input_file:
            _47 = [line.strip() for line in input_file]
        with open('_AddOn.txt') as input_file:
            _AddOn = [line.strip() for line in input_file]
        tmp = []
        for z in range(len(Model_features)):
            if Model_features[z] == '0':
                tmp += _0
            if Model_features[z] == '5':
                tmp += _5
            if Model_features[z] == '12':
                tmp += _12
            if Model_features[z] == '15':
                tmp += _15
            if Model_features[z] == '17':
                tmp += _17
            if Model_features[z] == '19':
                tmp += _19
            if Model_features[z] == '20':
                tmp += _20
            if Model_features[z] == '24':
                tmp += _24
            if Model_features[z] == '26':
                tmp += _26
            if Model_features[z] == '42':
                tmp += _42
            if Model_features[z] == '43':
                tmp += _43
            if Model_features[z] == '47':
                tmp += _47
        length = len(tmp)
        for z in range (10):
            if length < 10 :
                tmp.append(Main_symptom_list[randint(0,51)])
        offline1 = 1
        MDRDS.question_page.update_info(tmp)
        MDRDS.question_page1.update_info(tmp)
        MDRDS.question_page2.update_info(tmp)
        MDRDS.question_page3.update_info(tmp)
        MDRDS.question_page4.update_info(tmp)
        MDRDS.question_page5.update_info(tmp)
        MDRDS.question_page6.update_info(tmp)
        MDRDS.question_page7.update_info(tmp)
        MDRDS.question_page8.update_info(tmp)
        MDRDS.question_page9.update_info(tmp)

        MDRDS.aquestion24.offline_update(offline1)
        MDRDS.question_page.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions"
    
          
class DiagnosisPage(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4        
        self.user = Label()
        
        self.my_account = Button(text = "My Account")
        self.my_account.bind(on_press = self.my_account_button)
        self.add_widget(self.my_account)
        abc=Image(source='Graphics/DiagnosisPage/(1,1).png')
        self.add_widget(abc)

        abc1=Image(source='Graphics/DiagnosisPage/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/DiagnosisPage/(1,1).png')
        self.add_widget(abc2)


        self.my_record = Button(text = "My Record")
        self.my_record.bind(on_press = self.my_record_button)
        self.add_widget(self.my_record)
        abc3=Image(source='Graphics/DiagnosisPage/(1,1)p.png')
        self.add_widget(abc3)

        abc6=Image(source='Graphics/DiagnosisPage/(2,2).png')
        self.add_widget(abc6)
        self.Enter_Symptoms = TextInput(multiline = False)
        self.add_widget(self.Enter_Symptoms)


        self.doctor = Button(text = "DocBot")
        self.doctor.bind(on_press = self.doctor_button)
        self.add_widget(self.doctor)
        abc4=Image(source='Graphics/DiagnosisPage/1.png')
        self.add_widget(abc4)


        abc7=Image(source='Graphics/DiagnosisPage/2.png')
        self.add_widget(abc7)
        self.submit = Button(text = "Submit")
        self.submit.bind(on_press = self.submit_button)
        self.add_widget(self.submit)

        self.about = Button(text = "About")
        self.about.bind(on_press = self.about_button)
        self.add_widget(self.about)
        abc5=Image(source='Graphics/DiagnosisPage/3.png')
        self.add_widget(abc5)
        abc8=Image(source='Graphics/DiagnosisPage/4.png')
        self.add_widget(abc8)
        abc9=Image(source='Graphics/DiagnosisPage/(3,2).png')
        self.add_widget(abc9)

        self.logout = Button(text = "Logout")
        self.logout.bind(on_press = self.logout_button)
        self.add_widget(self.logout)
        abc15=Image(source='Graphics/DiagnosisPage/5.png')
        self.add_widget(abc15)
        abc10=Image(source='Graphics/DiagnosisPage/6.png')
        self.add_widget(abc10)
        abc11=Image(source='Graphics/DiagnosisPage/(1,1)p.png')
        self.add_widget(abc11)


        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)
        abc12=Image(source='Graphics/DiagnosisPage/7.png')
        self.add_widget(abc12)
        abc13=Image(source='Graphics/DiagnosisPage/8.png')
        self.add_widget(abc13)
        abc14=Image(source='Graphics/DiagnosisPage/(1,1)p.png')
        self.add_widget(abc14)

    def User(self , user):
        self.user.text = str(user)

    def my_account_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:      
            username = db.child("MedApp").child("Users").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()        
            username = dict(username)
            detail = dict(detail)

            MDRDS.account_page.user_update(username)
            MDRDS.account_page.detail_update(detail)
            
            MDRDS.screen_manager.current = "Account"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def my_record_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()
            time = db.child("MedApp").child("Time").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()
            diagnosis = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").get().val()
            diagnosis1 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").get().val()
            diagnosis2 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").get().val()
            
            username = dict(username)
            time = dict(time)
            detail = dict(detail)
            diagnosis = dict(diagnosis)
            diagnosis1 = dict(diagnosis1)
            diagnosis2 = dict(diagnosis2)

            MDRDS.your_record.user_update(username)
            MDRDS.your_record.time_update(time)
            MDRDS.your_record.detail_update(detail)
            MDRDS.your_record.diagnosis_update(diagnosis)
            MDRDS.your_record.diagnosis_update1(diagnosis1)
            MDRDS.your_record.diagnosis_update2(diagnosis2)
            
            MDRDS.screen_manager.current = "Record"
        except:
            MDRDS.screen_manager.current = "ErrorI"


    def about_button(self , instance):
        MDRDS.screen_manager.current = "About"

    def logout_button(self , instance):
        MDRDS.screen_manager.current = "Start"
        
    def doctor_button(self , instance):
        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()          
            username = dict(username)
            username = username["Name"]
            

            MDRDS.doctor.user_update(username)

            
            MDRDS.screen_manager.current = "Doctor"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def quit_button(self , instance):
        App.get_running_app().stop()

    def submit_button(self , instance):

        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = self.Enter_Symptoms.text
        keywords = Enter_Symptoms.split()
        Model_features = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)
        
        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features.append(str(Features_temp[keywords[i]][0]))
                
        with open('_0.txt') as input_file:
            _0 = [line.strip() for line in input_file]
        with open('_1.txt') as input_file:
            _1 = [line.strip() for line in input_file]
        with open('_2.txt') as input_file:
            _2 = [line.strip() for line in input_file]
        with open('_3.txt') as input_file:
            _3 = [line.strip() for line in input_file]
        with open('_5.txt') as input_file:
            _5 = [line.strip() for line in input_file]
        with open('_6.txt') as input_file:
            _6 = [line.strip() for line in input_file]
        with open('_11.txt') as input_file:
            _11 = [line.strip() for line in input_file]
        with open('_12.txt') as input_file:
            _12 = [line.strip() for line in input_file]
        with open('_15.txt') as input_file:
            _15 = [line.strip() for line in input_file]
        with open('_17.txt') as input_file:
            _17 = [line.strip() for line in input_file]
        with open('_19.txt') as input_file:
            _19 = [line.strip() for line in input_file]
        with open('_20.txt') as input_file:
            _20 = [line.strip() for line in input_file]
        with open('_24.txt') as input_file:
            _24 = [line.strip() for line in input_file]
        with open('_26.txt') as input_file:
            _26 = [line.strip() for line in input_file]
        with open('_42.txt') as input_file:
            _42 = [line.strip() for line in input_file]
        with open('_43.txt') as input_file:
            _43 = [line.strip() for line in input_file]
        with open('_47.txt') as input_file:
            _47 = [line.strip() for line in input_file]
        with open('_AddOn.txt') as input_file:
            _AddOn = [line.strip() for line in input_file]
        tmp = []
        for z in range(len(Model_features)):
            if Model_features[z] == '0':
                tmp += _0
            if Model_features[z] == '1':
                tmp += _1
            if Model_features[z] == '2':
                tmp += _2
            if Model_features[z] == '3':
                tmp += _3
            if Model_features[z] == '5':
                tmp += _5
            if Model_features[z] == '6':
                tmp += _6
            if Model_features[z] == '11':
                tmp += _11
            if Model_features[z] == '12':
                tmp += _12
            if Model_features[z] == '15':
                tmp += _15
            if Model_features[z] == '17':
                tmp += _17
            if Model_features[z] == '19':
                tmp += _19
            if Model_features[z] == '20':
                tmp += _20
            if Model_features[z] == '24':
                tmp += _24
            if Model_features[z] == '26':
                tmp += _26
            if Model_features[z] == '42':
                tmp += _42
            if Model_features[z] == '43':
                tmp += _43
            if Model_features[z] == '47':
                tmp += _47
        length = len(tmp)
        for z in range (10):
            tmp.append(Main_symptom_list[randint(0,97)])

        offline1 = 0
        MDRDS.question_page.update_info(tmp)
        MDRDS.question_page1.update_info(tmp)
        MDRDS.question_page2.update_info(tmp)
        MDRDS.question_page3.update_info(tmp)
        MDRDS.question_page4.update_info(tmp)
        MDRDS.question_page5.update_info(tmp)
        MDRDS.question_page6.update_info(tmp)
        MDRDS.question_page7.update_info(tmp)
        MDRDS.question_page8.update_info(tmp)
        MDRDS.question_page9.update_info(tmp)

        MDRDS.aquestion24.offline_update(offline1)
        MDRDS.question_page.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions"
    
        
        

class AccountPage(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4 

        self.user = Label()
        self.detail = Label()
        self.user1 = Label()
        self.ef = Label()
        
        self.diagnosis = Button(text = "Diagnosis")
        self.diagnosis.bind(on_press = self.diagnosis_button)
        self.add_widget(self.diagnosis)
        
        abc=Image(source='Graphics/AccountPage/(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/AccountPage/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/AccountPage/(1,1).png')
        self.add_widget(abc2)
        
        self.record = Button(text = "My Record")
        self.record.bind(on_press = self.record_button)
        self.add_widget(self.record)

        abc11=Image(source='Graphics/AccountPage/(2,1).png')
        self.add_widget(abc11)
        self.add_widget(self.user1)
        abc3=Image(source='Graphics/AccountPage/1.png')
        self.add_widget(abc3)


        self.doctor = Button(text = "DocBot")
        self.doctor.bind(on_press = self.doctor_button)
        self.add_widget(self.doctor)

        abc12=Image(source='Graphics/AccountPage/(3,1).png')
        self.add_widget(abc12)
        self.add_widget(self.detail)
        abc4=Image(source='Graphics/AccountPage/2.png')
        self.add_widget(abc4)

        
        self.about = Button(text = "About")
        self.about.bind(on_press = self.about_button)
        self.add_widget(self.about)

        abc13=Image(source='Graphics/AccountPage/(4,1).png')
        self.add_widget(abc13)
        self.add_widget(self.ef)
        abc5=Image(source='Graphics/AccountPage/3.png')
        self.add_widget(abc5)

        
        self.logout = Button(text = "Logout")
        self.logout.bind(on_press = self.logout_button)
        self.add_widget(self.logout)

        abc6=Image(source='Graphics/AccountPage/(1,1)p.png')
        self.add_widget(abc6)
        self.verf = Button(text = "Re-send Mail")
        self.verf.bind(on_press = self.verf_button)
        self.add_widget(self.verf)
        abc7=Image(source='Graphics/AccountPage/(1,1)p.png')
        self.add_widget(abc7)
        
        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)        

        abc8=Image(source='Graphics/AccountPage/(1,1)p.png')
        self.add_widget(abc8)
        abc9=Image(source='Graphics/AccountPage/(1,1)p.png')
        self.add_widget(abc9)
        abc10=Image(source='Graphics/AccountPage/(1,1)p.png')
        self.add_widget(abc10)

    def detail_update(self , detail):
        self.detail.text = str(detail)

    def update_ef(self , ef):
        self.ef.text = str(ef)
        
    def user_update(self , user1):
        self.user1.text = str(user1)
        
    def User(self , user):
        self.user.text = str(user)
        
    def diagnosis_button(self , instance):
        MDRDS.screen_manager.current = "Diagnosis"
        
    def verf_button(self , instance):
        MDRDS.screen_manager.current = "Verification1"

    def record_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')

        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()
            time = db.child("MedApp").child("Time").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()
            diagnosis = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").get().val()
            diagnosis1 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").get().val()
            diagnosis2 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").get().val()
            
            username = dict(username)
            time = dict(time)
            detail = dict(detail)
            diagnosis = dict(diagnosis)
            diagnosis1 = dict(diagnosis1)
            diagnosis2 = dict(diagnosis2)

            MDRDS.your_record.user_update(username)
            MDRDS.your_record.time_update(time)
            MDRDS.your_record.detail_update(detail)
            MDRDS.your_record.diagnosis_update(diagnosis)
            MDRDS.your_record.diagnosis_update1(diagnosis1)
            MDRDS.your_record.diagnosis_update2(diagnosis2)
            
            MDRDS.screen_manager.current = "Record"
        except:
            MDRDS.screen_manager.current = "ErrorI"


    def about_button(self , instance):
        MDRDS.screen_manager.current = "About"

    def logout_button(self , instance):
        MDRDS.screen_manager.current = "Start"
        
    def doctor_button(self , instance):
        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()          
            username = dict(username)
            username = username["Name"]
            

            MDRDS.doctor.user_update(username)

            
            MDRDS.screen_manager.current = "Doctor"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def quit_button(self , instance):
        App.get_running_app().stop()


class YourRecord(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4

        self.user = Label()
        self.diagnosis = Label()
        self.diagnosis1 = Label()
        self.diagnosis2 = Label()
        self.time = Label()
        self.detail = Label()
        self.user1 = Label()

        
        self.diagnosisb = Button(text = "Diagnosis")
        self.diagnosisb.bind(on_press = self.diagnosis_button)
        self.add_widget(self.diagnosisb)
        
        abc=Image(source='Graphics/YourRecord/(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/YourRecord/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/YourRecord/(1,1).png')
        self.add_widget(abc2)
        
        self.account = Button(text = "My Account")
        self.account.bind(on_press = self.account_button)
        self.add_widget(self.account)

        abc2=Image(source='Graphics/YourRecord/(2,1).png')
        self.add_widget(abc2)
        self.add_widget(self.user1)

        gd = GridLayout(rows=2)
        gd.add_widget(self.detail)
        gd.add_widget(self.time)
        self.add_widget(gd)
        
        self.doctor = Button(text = "DocBot")
        self.doctor.bind(on_press = self.doctor_button)
        self.add_widget(self.doctor)

        abc3=Image(source='Graphics/YourRecord/(1,1)p.png')
        self.add_widget(abc3)
        abc5=Image(source='Graphics/YourRecord/(3,2).png')
        self.add_widget(abc5)
        abc4=Image(source='Graphics/YourRecord/(1,1)p.png')
        self.add_widget(abc4)
        
        self.about = Button(text = "About")
        self.about.bind(on_press = self.about_button)
        self.add_widget(self.about)

        abc6=Image(source='Graphics/YourRecord/(4,1).png')
        self.add_widget(abc6)
        self.add_widget(self.diagnosis)
        self.add_widget(Label())
        
        self.logout = Button(text = "Logout")
        self.logout.bind(on_press = self.logout_button)
        self.add_widget(self.logout)

        abc7=Image(source='Graphics/YourRecord/(5,1).png')
        self.add_widget(abc7)
        self.add_widget(self.diagnosis1)
        self.add_widget(Label())
        
        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)        

        abc8=Image(source='Graphics/YourRecord/(6,1).png')
        self.add_widget(abc8)
        self.add_widget(self.diagnosis2)
        self.add_widget(Label())

    def User(self , user):
        self.user.text = str(user)

    def time_update(self , time):
        self.time.text = str(time)
        
    def detail_update(self , detail):
        self.detail.text = str(detail)
        
    def user_update(self , user1):
        self.user1.text = str(user1)
        
    def diagnosis_update(self , diagnosis):
        self.diagnosis.text = str(diagnosis)
        
    def diagnosis_update1(self , diagnosis1):
        self.diagnosis1.text = str(diagnosis1)

    def diagnosis_update2(self , diagnosis2):
        self.diagnosis2.text = str(diagnosis2)
        
    def diagnosis_button(self , instance):
        MDRDS.screen_manager.current = "Diagnosis"

    def account_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:      
            username = db.child("MedApp").child("Users").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()        
            username = dict(username)
            detail = dict(detail)

            MDRDS.account_page.user_update(username)
            MDRDS.account_page.detail_update(detail)
            
            MDRDS.screen_manager.current = "Account"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def about_button(self , instance):
        MDRDS.screen_manager.current = "About"

    def logout_button(self , instance):
        MDRDS.screen_manager.current = "Start"
        
    def doctor_button(self , instance):
        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()          
            username = dict(username)
            username = username["Name"]
            

            MDRDS.doctor.user_update(username)

            
            MDRDS.screen_manager.current = "Doctor"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def quit_button(self , instance):
        App.get_running_app().stop()

class AboutPage(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4

        self.user = Label()
        
        self.diagnosis = Button(text = "Diagnosis")
        self.diagnosis.bind(on_press = self.diagnosis_button)
        self.add_widget(self.diagnosis)
        
        abc=Image(source='Graphics/About/(1,1).png')
        self.add_widget(abc)
        abc1=Image(source='Graphics/About/(1,2).png')
        self.add_widget(abc1)
        abc2=Image(source='Graphics/About/(1,1).png')
        self.add_widget(abc2)
        

        self.account = Button(text = "My Account")
        self.account.bind(on_press = self.account_button)
        self.add_widget(self.account)

        abc3=Image(source='Graphics/About/(2,1).png')
        self.add_widget(abc3)
        abc4=Image(source='Graphics/About/(2,2).png')
        self.add_widget(abc4)
        
        abc5=Image(source='Graphics/About/(2,3).png')
        self.add_widget(abc5)

        self.record = Button(text = "My Record")
        self.record.bind(on_press = self.record_button)
        self.add_widget(self.record)

        abc6=Image(source='Graphics/About/(3,1).png')
        self.add_widget(abc6)
        
        abc7=Image(source='Graphics/About/(3,2).png')
        self.add_widget(abc7)
        
        abc8=Image(source='Graphics/About/(3,3).png')
        self.add_widget(abc8)

        self.doctor = Button(text = "DocBot")
        self.doctor.bind(on_press = self.doctor_button)
        self.add_widget(self.doctor)
        

        abc9=Image(source='Graphics/About/(4,1).png')
        self.add_widget(abc9)
        abc10=Image(source='Graphics/About/(4,2).png')
        self.add_widget(abc10)
        abc11=Image(source='Graphics/About/(4,3).png')
        self.add_widget(abc11)
        
        self.logout = Button(text = "Logout")
        self.logout.bind(on_press = self.logout_button)
        self.add_widget(self.logout)

        abc12=Image(source='Graphics/About/(5,1).png')
        self.add_widget(abc12)
        abc13=Image(source='Graphics/About/(5,2).png')
        self.add_widget(abc13)
        abc14=Image(source='Graphics/About/(5,3).png')
        self.add_widget(abc14)
        
        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)        

        abc15=Image(source='Graphics/About/1.png')
        self.add_widget(abc15)
        abc16=Image(source='Graphics/About/2.png')
        self.add_widget(abc16)
        abc17=Image(source='Graphics/About/3.png')
        self.add_widget(abc17)
        
    def diagnosis_button(self , instance):
        MDRDS.screen_manager.current = "Diagnosis"
        
    def User(self , user):
        self.user.text = str(user)

    def record_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()
            time = db.child("MedApp").child("Time").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()
            diagnosis = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").get().val()
            diagnosis1 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").get().val()
            diagnosis2 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").get().val()

            diagnosis12 = dict(diagnosis1)
            diagnosis123 = dict(diagnosis2)
            username = dict(username)
            time = dict(time)
            detail = dict(detail)
            diagnosis = dict(diagnosis)

            MDRDS.your_record.user_update(username)
            MDRDS.your_record.time_update(time)
            MDRDS.your_record.detail_update(detail)
            MDRDS.your_record.diagnosis_update(diagnosis)
            MDRDS.your_record.diagnosis_update1(diagnosis12)
            MDRDS.your_record.diagnosis_update2(diagnosis123)
            
            MDRDS.screen_manager.current = "Record"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def account_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:      
            username = db.child("MedApp").child("Users").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()        
            username = dict(username)
            detail = dict(detail)

            MDRDS.account_page.user_update(username)
            MDRDS.account_page.detail_update(detail)
            
            MDRDS.screen_manager.current = "Account"
        except:
            MDRDS.screen_manager.current = "ErrorI"
            

    def logout_button(self , instance):
        MDRDS.screen_manager.current = "Start"
        
    def doctor_button(self , instance):
        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()          
            username = dict(username)
            username = username["Name"]
            

            MDRDS.doctor.user_update(username)

            
            MDRDS.screen_manager.current = "Doctor"
        except:
            MDRDS.screen_manager.current = "ErrorI"



    def quit_button(self , instance):
        App.get_running_app().stop()

class AboutPageO(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        
        self.diagnosis = Button(text = "Diagnosis")
        self.diagnosis.bind(on_press = self.diagnosis_button)
        self.add_widget(self.diagnosis)
        
        self.add_widget(Label())
        self.add_widget(Label(text = "Welcome To The MedApp"))
        self.add_widget(Label())
        
        self.login = Button(text = "Login")
        self.login.bind(on_press = self.login_button)
        self.add_widget(self.login)

        self.add_widget(Label())
        self.add_widget(Label(text = "In this app you can predict\nyour disease by giving the sympmtom\nthat the person is suffering."))
        self.add_widget(Label())

        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)
        self.add_widget(self.quit)

        self.add_widget(Label())
        self.add_widget(Label(text = "This app is created by two\nstudents of class XII-B who are\nAbhay And Aneesh."))
        self.add_widget(Label())

        self.add_widget(Label())
        

        self.add_widget(Label())
        self.add_widget(Label(text = "This UI of this app is created using kivy.\nThe prediction of the disease\n is done using Machine Learing. "))
        self.add_widget(Label())
        
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label(text ="The Authentication system and\nDataBase is made with Google\'s FireBase"))
        self.add_widget(Label())
        
        self.add_widget(Label())       

        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())
        
    def diagnosis_button(self , instance):
        MDRDS.screen_manager.current = "DiagnosisO"

    def login_button(self , instance):
        MDRDS.screen_manager.current = "Start"

    def quit_button(self , instance):
        App.get_running_app().stop()


class Questions(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()

                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[0]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):
        
        def Converter(Model_features):
            Model_tmp = []
            b = Model_features
            for j in range (len(b)):
                if b[j].isdigit():
        
                    if b[j+1].isdigit():
                        Model_tmp.append(b[j]+b[j+1])

                    else:
                        if b[j-1].isdigit():
                            continue
                        Model_tmp.append(b[j])

            return Model_tmp
        

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page1.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions1"
        


    def no_button(self , instance):                   
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page1.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions1"

class Questions1(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()

                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[1]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):
        
        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page2.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions2"
        


    def no_button(self , instance):
    
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page2.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions2"

class Questions2(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()

                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[2]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page3.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions3"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page3.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions3"
        
class Questions3(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()

                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[3]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page4.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions4"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page4.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions4"

class Questions4(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[4]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page5.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions5"
        


    def no_button(self , instance):

        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page5.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions5"

class Questions5(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[5]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page6.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions6"
        


    def no_button(self , instance):

        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page6.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions6"

class Questions6(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[6]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page7.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions7"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page7.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions7"

class Questions7(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[7]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])      
        MDRDS.question_page8.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions8"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page8.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions8"

class Questions8(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[8]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.question_page9.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions9"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page9.update_info1(Model_features)
        MDRDS.screen_manager.current = "Questions9"

class Questions9(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Model_features = Label()
                        
        self.add_widget(Label())
        self.diagnosis_text = Label(text = "Answer The Following Questions")
        self.add_widget(self.diagnosis_text)
        self.add_widget(Label())
        
        self.add_widget(Label())
        self.enter_symptom_text = Label(text = "Do You Experience The Following :")
        self.add_widget(self.enter_symptom_text)
        self.add_widget(Label())


        self.add_widget(Label())
        self.tmp = Label()
        self.add_widget(self.tmp)
        self.add_widget(Label())
        
        
        self.add_widget(Label()) 
        self.yes = Button(text = "Yes")
        self.yes.bind(on_press = self.yes_button)
        self.add_widget(self.yes)
        self.no = Button(text = "No")
        self.no.bind(on_press = self.no_button)
        self.add_widget(self.no)

    def update_info(self , tmp):

        self.tmp.text = tmp[9]

        
        
    def update_info1(self , Model_features):
        self.Model_features.text = str(Model_features)
     
    def yes_button(self , instance):

        tmp = self.tmp.text
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)


        with open('Main_symptom_list.txt') as input_file:
            Main_symptom_list = [line.strip() for line in input_file]
                
        Enter_Symptoms = tmp
        keywords = Enter_Symptoms.split()
        Model_features1 = []
        Features_temp = multi_word_search(Main_symptom_list,keywords)

        for i in range(len(keywords)):
            if len(Features_temp[keywords[i]])==0:
                break
            Model_features1.append(str(Features_temp[keywords[i]][0]))

        Model_features.append(Model_features1[0])

        

        MDRDS.analysis_page.update_info1(Model_features)
        MDRDS.screen_manager.current = "Analysis"
        


    def no_button(self , instance):
        
        Model_features1 = list(self.Model_features.text)
        Model_features = Converter(Model_features1)
        MDRDS.question_page9.update_info1(Model_features)
        MDRDS.screen_manager.current = "Analysis"


class Resulto(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.user = Label()

        self.add_widget(Label())
        self.title1 = Label(text = 'Enter The Result Button\nTo Show Your Result')
        self.add_widget(self.title1)
        self.add_widget(Label())
      
        self.add_widget(Label())
        self.result = Button(text = 'Result')
        self.result.bind(on_press = self.result_button)
        self.add_widget(self.result)
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())


    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def result_button(self , instance):
     
        Disease_prediction1 = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))


        with open('Diseases.txt') as input_file:
            Diseases_list = [line.strip() for line in input_file]
        with open('Symptoms X Diseases.txt') as input_file:
            SXD = [line.strip() for line in input_file]

        Disease_prediction = []
        for o in Disease_prediction1:
            Disease_prediction.append(Diseases_list[int(o)])
    
        DPA = []
        for i in range(len(Disease_prediction1)):
            for j in range(len(SXD)):
                if j == int(Disease_prediction1[i]):
                    for f in range(len(SXD[i])):
                        DPA.append(SXD[j])
        DPA1 = []
        [DPA1.append(x) for x in DPA if x not in DPA1]

        result123 = {}
        gr = []
        mr = []
        br = []
        for i in range (len(Disease_prediction)):
            result123[(Disease_prediction[i])] = Converter(list("["+(DPA1[i]+"]")))
        
        for key in result123:
            a=0
            for i in range(len(Model_features)):
                if Model_features[i] in result123[key]:
                    a+=1
                if len(result123[key])-1 == i:
                    if a == len(result123[key])-2:
                        gr.append(key)
                        break
        
                    if a > len(result123[key])-3:
                        mr.append(key)
                        break
                
                    if a > len(result123[key])-4:
                        br.append(key)
                        break

        MDRDS.result1o.Update_info1(gr)
        MDRDS.result1o.Update_info2(mr)
        MDRDS.result1o.Update_info3(br)
      
        MDRDS.screen_manager.current = "Result1o"



                        
class Result(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.Disease_prediction = Label()
        self.Model_features = Label()
        self.DPA1 = Label()
        self.DPA4 = Label()
        self.user = Label()

        self.add_widget(Label())
        self.title1 = Label(text = 'Enter The Result Button\nTo Show Your Result')
        self.add_widget(self.title1)
        self.add_widget(Label())
      
        self.add_widget(Label())
        self.result = Button(text = 'Result')
        self.result.bind(on_press = self.result_button)
        self.add_widget(self.result)
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(Label())

    def User(self , user):
        self.user.text = str(user)

    def update(self, Disease_prediction):
        self.Disease_prediction.text = str(Disease_prediction)

    def update1(self, Model_features):
        self.Model_features.text = str(Model_features)

    def update2(self, DPA1):
        self.DPA1.text = str(DPA1)

    def update3(self, DPA4):
        self.DPA4.text = str(DPA4)

    def result_button(self , instance):
   
        Disease_prediction1 = Converter(list(self.Disease_prediction.text))
        Model_features = Converter(list(self.Model_features.text))
        DPA1 = Converter(list(self.DPA1.text))
        DPA4 = Converter(list(self.DPA4.text))


        with open('Diseases.txt') as input_file:
            Diseases_list = [line.strip() for line in input_file]
        with open('Symptoms X Diseases.txt') as input_file:
            SXD = [line.strip() for line in input_file]

        Disease_prediction = []
        for o in Disease_prediction1:
            Disease_prediction.append(Diseases_list[int(o)])
    
        DPA = []
        for i in range(len(Disease_prediction1)):
            for j in range(len(SXD)):
                if j == int(Disease_prediction1[i]):
                    for f in range(len(SXD[i])):
                        DPA.append(SXD[j])
        DPA1 = []
        [DPA1.append(x) for x in DPA if x not in DPA1]

        result123 = {}
        gr = []
        mr = []
        br = []
        lr = []
        for i in range (len(Disease_prediction)):
            result123[(Disease_prediction[i])] = Converter(list("["+(DPA1[i]+"]")))
        
        for key in result123:
            a=0
            for i in range(len(Model_features)):
                if Model_features[i] in result123[key]:
                    a+=1
                if len(result123[key])-1 == i:
                    if a >= len(result123[key])-2:
                        gr.append(key)
                        break
        
                    if a >= len(result123[key])-3:
                        mr.append(key)
                        break
                
                    if a >= len(result123[key])-4:
                        br.append(key)
                        break
                    
                    if a < len(result123[key]):
                        lr.append(key)
                        break
                    
        gr1 = gr
        mr1 = mr
        br1 = br
        lr1 = lr

        gr1 = str(gr1)
        mr1 = str(mr1)
        br1 = str(br1)
        lr1 = str(lr1)
        Model_features = str(Model_features)
        
        user = self.user.text
        
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')

        Model_features=Model_features.lstrip("[")
        Model_features=Model_features.rstrip("[")
        Model_features=Model_features.lstrip(']')
        Model_features=Model_features.rstrip(']')
        
        gr1=gr1.lstrip("[")
        gr1=gr1.rstrip("[")
        gr1=gr1.lstrip(']')
        gr1=gr1.rstrip(']')

        mr1=mr1.lstrip("[")
        mr1=mr1.rstrip("[")
        mr1=mr1.lstrip(']')
        mr1=mr1.rstrip(']')

        br1=br1.lstrip("[")
        br1=br1.rstrip("[")
        br1=br1.lstrip(']')
        br1=br1.rstrip(']')

        lr1=lr1.lstrip("[")
        lr1=lr1.rstrip("[")
        lr1=lr1.lstrip(']')
        lr1=lr1.rstrip(']') 

        abc = gr1+mr1+br1
        x = datetime.datetime.now()
        b = str(x.strftime("%x"))
        c = str(x.strftime("%X"))
        
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        db = firebase.database()


        try:
            
            Data0 = {"Disease":gr1}
            Data2 = {"Disease":mr1}
            Data3 = {"Disease":br1}
            Data4 = {"Disease":lr1}
            Data = {"Model_features":Model_features}
            Data1 = {"Date": b}
            db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").set(Data0)
            db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").set(Data2)
            db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").set(Data3)
            db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("LR").set(Data4)
            db.child("MedApp").child("ModelFeatures").child(user).set(Data)            
            db.child("MedApp").child("Time").child(user).set(Data1)

        except:
            
            MDRDS.screen_manager.current = "ErrorI"


        MDRDS.result1.Update_info1(gr)
        MDRDS.result1.Update_info2(mr)
        MDRDS.result1.Update_info3(br)
        MDRDS.result1.Update_info4(result123)
        MDRDS.result1.Update_info5(Model_features)
      
        MDRDS.screen_manager.current = "Result1"
      

class Result1(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.gr = Label()
        self.mr = Label()
        self.br = Label()
        self.MF = Label()
        
        self.user = Label()
        self.a = Label()

        self.add_widget(Label())
        self.add_widget(Label(text = 'RESULT'))
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label(text = 'You Might Have :'))
        self.add_widget(Label())
        

        self.add_widget(Label(text = 'High Possibility :'))
        self.add_widget(self.gr)
        self.add_widget(Label())

        self.add_widget(Label(text = 'Average Possibility :'))
        self.add_widget(self.mr)
        self.add_widget(Label())

        self.add_widget(Label(text = 'Low Possibility :'))
        self.add_widget(self.br)
        self.add_widget(Label())


        self.add_widget(Label())        
        self.cont = Button(text = 'Continue')
        self.cont.bind(on_press = self.cont_button)
        self.add_widget(self.cont)
        self.add_widget(Label())
        self.add_widget(Label())


    def Update_info1(self , gr):
        self.gr.text = str(gr)
        
    def Update_info2(self , mr):
        self.mr.text = str(mr)

    def Update_info3(self , br):
        self.br.text = str(br)

    def Update_info4(self , a):
        self.a.text = str(a)
        
    def Update_info5(self , MF):
        self.MF.text = str(MF)

    def User(self , user):
        self.user.text = str(user)
        
    def cont_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')

        gr = self.gr.text
        mr = self.mr.text
        br = self.br.text
        MF = self.MF.text
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()
            time = db.child("MedApp").child("Time").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()
            diagnosis = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").get().val()
            diagnosis1 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").get().val()
            diagnosis2 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").get().val()
                
            username = dict(username)
            time = dict(time)
            detail = dict(detail)
            diagnosis = dict(diagnosis)
            diagnosis1 = dict(diagnosis1)
            diagnosis2 = dict(diagnosis2)

            MDRDS.your_record.user_update(username)
            MDRDS.your_record.time_update(time)
            MDRDS.your_record.detail_update(detail)
            MDRDS.your_record.diagnosis_update(diagnosis)
            MDRDS.your_record.diagnosis_update1(diagnosis1)
            MDRDS.your_record.diagnosis_update2(diagnosis2)
            MDRDS.screen_manager.current = "Record"

        except:
            MDRDS.screen_manager.current = "ErrorI"

        
class Result1o(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3

        self.gr = Label()
        self.mr = Label()
        self.br = Label()

        self.add_widget(Label())
        self.add_widget(Label(text = 'RESULT'))
        self.add_widget(Label())

        self.add_widget(Label())
        self.add_widget(Label(text = 'You Might Have :'))
        self.add_widget(Label())
        

        self.add_widget(Label(text = 'High Possibility :'))
        self.add_widget(self.gr)
        self.add_widget(Label())

        self.add_widget(Label(text = 'Average Possibility :'))
        self.add_widget(self.mr)
        self.add_widget(Label())

        self.add_widget(Label(text = 'Low Possibility :'))
        self.add_widget(self.br)
        self.add_widget(Label())

        self.add_widget(Label())        
        self.cont = Button(text = 'Continue')
        self.cont.bind(on_press = self.cont_button)
        self.add_widget(self.cont)
        self.add_widget(Label())
        self.add_widget(Label())


    def Update_info1(self , gr):
        self.gr.text = str(gr)
        
    def Update_info2(self , mr):
        self.mr.text = str(mr)

    def Update_info3(self , br):
        self.br.text = str(br)
        
    def cont_button(self , instance):

        MDRDS.screen_manager.current = "DiagnosisO"       
        

class Doctor(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)


        self.cols = 1
        
        self.rows = 2

        self.user = Label()
        self.user1 = Label()


        """self.account = Button(text = "My Account")
        self.account.bind(on_press = self.account_button)


        self.record = Button(text = "My Record")
        self.record.bind(on_press = self.record_button)

        
        self.about = Button(text = "About")
        self.about.bind(on_press = self.about_button)

        
        self.logout = Button(text = "Logout")
        self.logout.bind(on_press = self.logout_button)

        
        self.quit = Button(text = "Quit")
        self.quit.bind(on_press = self.quit_button)

        self.diagnosis = Button(text = "diagnosis")
        self.diagnosis.bind(on_press = self.diagnosis_button)
        
        bottom_line2 = GridLayout(rows=6)
        bottom_line2.add_widget(self.diagnosis)
        bottom_line2.add_widget(self.account)
        bottom_line2.add_widget(self.record)
        bottom_line2.add_widget(self.about)
        bottom_line2.add_widget(self.logout)
        self.add_widget(bottom_line2)"""
        
        self.history = ScrollableLabel(height = Window.size[1]*0.9, size_hint_y = None)
        self.add_widget(self.history)

        self.new_message = TextInput(width = Window.size[0]*0.8, size_hint_x = None, multiline = False)
        self.send = Button(text = "Send")
        self.send.bind(on_press = self.send_message)
        self.back = Button(text = "Back")
        self.back.bind(on_press = self.back_button)
        
        """bottom_line3 = GridLayout(cols=3)
        bottom_line3.add_widget(self.quit)

        self.add_widget(bottom_line3)"""

        
        bottom_line = GridLayout(cols=3)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        bottom_line.add_widget(self.back)

        self.add_widget(bottom_line)

        


        """bottom_line1 = GridLayout(cols=1)
        bottom_line.add_widget(Label(text = "Emotion State Enchancer : DOCBOT"))
        self.add_widget(bottom_line1)"""



        Window.bind(on_key_down = self.on_key_down)
        Clock.schedule_once(self.focus_text_input, 1)

        

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_message(None)


    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(f"[color=dd2020]{self.user1.text}[/color] > {message}")

        Clock.schedule_once(self.focus_text_input, 0.1)

    def back_button(self , instance):
        MDRDS.screen_manager.current = "Diagnosis"

    def focus_text_input(self, _):
        self.new_message.focus = True        
        

    def User(self , user):
        self.user.text = str(user)
        
    def user_update(self , user1):
        self.user1.text = str(user1)
    def diagnosis_button(self , instance):
        MDRDS.screen_manager.current = "Diagnosis"

    def account_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:      
            username = db.child("MedApp").child("Users").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()        
            username = dict(username)
            detail = dict(detail)

            MDRDS.account_page.user_update(username)
            MDRDS.account_page.detail_update(detail)
            
            MDRDS.screen_manager.current = "Account"
        except:
            MDRDS.screen_manager.current = "ErrorI"

    def about_button(self , instance):
        MDRDS.screen_manager.current = "About"

    def logout_button(self , instance):
        MDRDS.screen_manager.current = "Start"
        
    def record_button(self , instance):

        user = self.user.text
        user=user.lstrip("'")
        user=user.rstrip("'")
        user=user.lstrip('"')
        user=user.rstrip('"')
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        try:
            username = db.child("MedApp").child("Users").child(user).get().val()
            time = db.child("MedApp").child("Time").child(user).get().val()
            detail = db.child("MedApp").child("Details").child("AgeGender").child(user).get().val()
            diagnosis = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("GR").get().val()
            diagnosis1 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("MR").get().val()
            diagnosis2 = db.child("MedApp").child("Diagnosis").child("Disease").child(user).child("BR").get().val()
             
            username = dict(username)
            time = dict(time)
            detail = dict(detail)
            diagnosis = dict(diagnosis)
            diagnosis1 = dict(diagnosis1)
            diagnosis2 = dict(diagnosis2)

            MDRDS.your_record.user_update(username)
            MDRDS.your_record.time_update(time)
            MDRDS.your_record.detail_update(detail)
            MDRDS.your_record.diagnosis_update(diagnosis)
            MDRDS.your_record.diagnosis_update1(diagnosis1)
            MDRDS.your_record.diagnosis_update2(diagnosis2)
            
            MDRDS.screen_manager.current = "Record"
        except:
            MDRDS.screen_manager.current = "ErrorI"


    def quit_button(self , instance):
        App.get_running_app().stop()

class ErrorI(GridLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        
        self.add_widget(Label())
        self.add_widget(Label(text = 'No Internet Connection'))
        self.add_widget(Label())

        self.add_widget(Label())
        self.back = Button(text = 'Login')
        self.back.bind(on_press = self.back_button)
        self.add_widget(self.back)
        self.add_widget(Label())        

        self.add_widget(Label())

    def back_button(self , instance):
        MDRDS.screen_manager.current = "HomeL"
    


class MedAppUI(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.start_page = StartPage()
        screen = Screen(name="Start")
        screen.add_widget(self.start_page)
        self.screen_manager.add_widget(screen)

        self.home_page_login = HomePageLogin()
        screen = Screen(name="HomeL")
        screen.add_widget(self.home_page_login)
        self.screen_manager.add_widget(screen)

        self.diagnosis_page = DiagnosisPage()
        screen = Screen(name="Diagnosis")
        screen.add_widget(self.diagnosis_page)
        self.screen_manager.add_widget(screen)

        self.diagnosis_page_offline = DiagnosisPageOffline()
        screen = Screen(name="DiagnosisO")
        screen.add_widget(self.diagnosis_page_offline)
        self.screen_manager.add_widget(screen)

        self.home_page_sign_up = HomePageSignUp()
        screen = Screen(name="HomeS")
        screen.add_widget(self.home_page_sign_up)
        self.screen_manager.add_widget(screen)

        self.home_page_fp = HomePageFP()
        screen = Screen(name="HomeFP")
        screen.add_widget(self.home_page_fp)
        self.screen_manager.add_widget(screen)

        self.verf_page = Verification()
        screen = Screen(name="Verification")
        screen.add_widget(self.verf_page)
        self.screen_manager.add_widget(screen)

        self.verf_page1 = Verification1()
        screen = Screen(name="Verification1")
        screen.add_widget(self.verf_page1)
        self.screen_manager.add_widget(screen)

        self.login_error = LoginError()
        screen = Screen(name="LE")
        screen.add_widget(self.login_error)
        self.screen_manager.add_widget(screen)

        self.error = Error()
        screen = Screen(name="Error")
        screen.add_widget(self.error)
        self.screen_manager.add_widget(screen)     

        self.signup_error = SignUpError()
        screen = Screen(name="SE")
        screen.add_widget(self.signup_error)
        self.screen_manager.add_widget(screen)

        self.fpe = FPE()
        screen = Screen(name="FPE")
        screen.add_widget(self.fpe)
        self.screen_manager.add_widget(screen)

        self.account_page = AccountPage()
        screen = Screen(name="Account")
        screen.add_widget(self.account_page)
        self.screen_manager.add_widget(screen)

        self.your_record = YourRecord()
        screen = Screen(name="Record")
        screen.add_widget(self.your_record)
        self.screen_manager.add_widget(screen)

        self.about_page = AboutPage()
        screen = Screen(name="About")
        screen.add_widget(self.about_page)
        self.screen_manager.add_widget(screen)

        self.about_pageO = AboutPageO()
        screen = Screen(name="AboutO")
        screen.add_widget(self.about_pageO)
        self.screen_manager.add_widget(screen)

        self.question_page = Questions()
        screen = Screen(name="Questions")
        screen.add_widget(self.question_page)
        self.screen_manager.add_widget(screen)

        self.question_page1 = Questions1()
        screen = Screen(name="Questions1")
        screen.add_widget(self.question_page1)
        self.screen_manager.add_widget(screen)

        self.question_page2 = Questions2()
        screen = Screen(name="Questions2")
        screen.add_widget(self.question_page2)
        self.screen_manager.add_widget(screen)

        self.question_page3 = Questions3()
        screen = Screen(name="Questions3")
        screen.add_widget(self.question_page3)
        self.screen_manager.add_widget(screen)

        self.question_page4 = Questions4()
        screen = Screen(name="Questions4")
        screen.add_widget(self.question_page4)
        self.screen_manager.add_widget(screen)

        self.question_page5 = Questions5()
        screen = Screen(name="Questions5")
        screen.add_widget(self.question_page5)
        self.screen_manager.add_widget(screen)

        self.question_page6 = Questions6()
        screen = Screen(name="Questions6")
        screen.add_widget(self.question_page6)
        self.screen_manager.add_widget(screen)

        self.question_page7 = Questions7()
        screen = Screen(name="Questions7")
        screen.add_widget(self.question_page7)
        self.screen_manager.add_widget(screen)

        self.question_page8 = Questions8()
        screen = Screen(name="Questions8")
        screen.add_widget(self.question_page8)
        self.screen_manager.add_widget(screen)

        self.question_page9 = Questions9()
        screen = Screen(name="Questions9")
        screen.add_widget(self.question_page9)
        self.screen_manager.add_widget(screen)

        self.analysis_page = Analysis()
        screen = Screen(name="Analysis")
        screen.add_widget(self.analysis_page)
        self.screen_manager.add_widget(screen)

        self.prediction_page = Prediction()
        screen = Screen(name="Prediction")
        screen.add_widget(self.prediction_page)
        self.screen_manager.add_widget(screen)

        self.aquestion = AQuestions()
        screen = Screen(name="AQuestions")
        screen.add_widget(self.aquestion)
        self.screen_manager.add_widget(screen)

        self.aquestion1 = AQuestions1()
        screen = Screen(name="AQuestions1")
        screen.add_widget(self.aquestion1)
        self.screen_manager.add_widget(screen)

        self.aquestion2 = AQuestions2()
        screen = Screen(name="AQuestions2")
        screen.add_widget(self.aquestion2)
        self.screen_manager.add_widget(screen)

        self.aquestion3 = AQuestions3()
        screen = Screen(name="AQuestions3")
        screen.add_widget(self.aquestion3)
        self.screen_manager.add_widget(screen)

        self.aquestion4 = AQuestions4()
        screen = Screen(name="AQuestions4")
        screen.add_widget(self.aquestion4)
        self.screen_manager.add_widget(screen)

        self.aquestion5 = AQuestions5()
        screen = Screen(name="AQuestions5")
        screen.add_widget(self.aquestion5)
        self.screen_manager.add_widget(screen)

        self.aquestion6 = AQuestions6()
        screen = Screen(name="AQuestions6")
        screen.add_widget(self.aquestion6)
        self.screen_manager.add_widget(screen)

        self.aquestion7 = AQuestions7()
        screen = Screen(name="AQuestions7")
        screen.add_widget(self.aquestion7)
        self.screen_manager.add_widget(screen)

        self.aquestion8 = AQuestions8()
        screen = Screen(name="AQuestions8")
        screen.add_widget(self.aquestion8)
        self.screen_manager.add_widget(screen)

        self.aquestion9 = AQuestions9()
        screen = Screen(name="AQuestions9")
        screen.add_widget(self.aquestion9)
        self.screen_manager.add_widget(screen)

        self.aquestion10 = AQuestions10()
        screen = Screen(name="AQuestions10")
        screen.add_widget(self.aquestion10)
        self.screen_manager.add_widget(screen)

        self.aquestion11 = AQuestions11()
        screen = Screen(name="AQuestions11")
        screen.add_widget(self.aquestion11)
        self.screen_manager.add_widget(screen)

        self.aquestion12 = AQuestions12()
        screen = Screen(name="AQuestions12")
        screen.add_widget(self.aquestion12)
        self.screen_manager.add_widget(screen)

        self.aquestion13 = AQuestions13()
        screen = Screen(name="AQuestions13")
        screen.add_widget(self.aquestion13)
        self.screen_manager.add_widget(screen)

        self.aquestion14 = AQuestions14()
        screen = Screen(name="AQuestions14")
        screen.add_widget(self.aquestion14)
        self.screen_manager.add_widget(screen)

        self.aquestion15 = AQuestions15()
        screen = Screen(name="AQuestions15")
        screen.add_widget(self.aquestion15)
        self.screen_manager.add_widget(screen)

        self.aquestion16 = AQuestions16()
        screen = Screen(name="AQuestions16")
        screen.add_widget(self.aquestion16)
        self.screen_manager.add_widget(screen)

        self.aquestion17 = AQuestions17()
        screen = Screen(name="AQuestions17")
        screen.add_widget(self.aquestion17)
        self.screen_manager.add_widget(screen)

        self.aquestion18 = AQuestions18()
        screen = Screen(name="AQuestions18")
        screen.add_widget(self.aquestion18)
        self.screen_manager.add_widget(screen)

        self.aquestion19 = AQuestions19()
        screen = Screen(name="AQuestions19")
        screen.add_widget(self.aquestion19)
        self.screen_manager.add_widget(screen)

        self.aquestion20 = AQuestions20()
        screen = Screen(name="AQuestions20")
        screen.add_widget(self.aquestion20)
        self.screen_manager.add_widget(screen)

        self.aquestion21 = AQuestions21()
        screen = Screen(name="AQuestions21")
        screen.add_widget(self.aquestion21)
        self.screen_manager.add_widget(screen)

        self.aquestion22 = AQuestions22()
        screen = Screen(name="AQuestions22")
        screen.add_widget(self.aquestion22)
        self.screen_manager.add_widget(screen)

        self.aquestion23 = AQuestions23()
        screen = Screen(name="AQuestions23")
        screen.add_widget(self.aquestion23)
        self.screen_manager.add_widget(screen)

        self.aquestion24 = AQuestions24()
        screen = Screen(name="AQuestions24")
        screen.add_widget(self.aquestion24)
        self.screen_manager.add_widget(screen)

        self.result = Result()
        screen = Screen(name="Result")
        screen.add_widget(self.result)
        self.screen_manager.add_widget(screen)

        self.result1 = Result1()
        screen = Screen(name="Result1")
        screen.add_widget(self.result1)
        self.screen_manager.add_widget(screen)

        self.resulto = Resulto()
        screen = Screen(name="ResultO")
        screen.add_widget(self.resulto)
        self.screen_manager.add_widget(screen)

        self.result1o = Result1o()
        screen = Screen(name="Result1o")
        screen.add_widget(self.result1o)
        self.screen_manager.add_widget(screen)

        self.doctor = Doctor()
        screen = Screen(name="Doctor")
        screen.add_widget(self.doctor)
        self.screen_manager.add_widget(screen)

        self.errori = ErrorI()
        screen = Screen(name="ErrorI")
        screen.add_widget(self.errori)
        self.screen_manager.add_widget(screen)

        return self.screen_manager




""" CODE STARTS FROM HERE !!! """

if __name__ == "__main__":
    Config.set('graphics','resizable',False)
    MDRDS = MedAppUI()
    MDRDS.run()
