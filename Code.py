import json
import os
from flask import Flask
from flask import request
from flask import make_response
import requests
from bs4 import BeautifulSoup
import random

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) #Using post as a method

def AEC():

    #Getting intent from Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)

    #Call generating_answer function to classify the question
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #Make a respond back to Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #Setting Content Type
  
    print (r)
    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent that recived from dialogflow.
    
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))
   

    #Getting intent name form intent that recived from dialogflow.
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 

    #Select function for answering question
  
    print ("0",intent_group_question_str)
    if intent_group_question_str == 'News - custom': 
        answer_str = Newsfinder(question_from_dailogflow_dict)
    elif intent_group_question_str == 'Sickness - custom': 
        answer_str = SICKNESS_advise(question_from_dailogflow_dict)
    #elif intent_group_question_str == 'Sickness - custom - more': 
      
        #answer_str = SICKNESS_advise(question_from_dailogflow_dict)
    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"

    #Build answer dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    #answer_from_bot = {"fulfillmentText":[answer_str, answer_str]}
    #er_from_bot = {"fulfillmentMessages":[{ "text": {"text": ["Response 1"]},"plantform": "LINE"},{
       #"text": {"text":["Response 2"]},"platform": "LINE"}]}
    print (answer_from_bot)
    #Convert dict to JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
   
    print (answer_from_bot)

    return answer_from_bot
'''

'''
def Newsfinder(respond_dict):

    
    newwwType = int(respond_dict["queryResult"]["outputContexts"][2]["parameters"]["N.original"])
   
    print (newwwType)
  
        
    #Type=input("ข่าว")
    if  newwwType==1 :
        page = requests.get("https://mthai.com/sport") 
        
    elif  newwwType==2 :
        page = requests.get("https://mthai.com/tag/%e0%b8%81%e0%b8%a3%e0%b8%b0%e0%b8%97%e0%b8%a3%e0%b8%a7%e0%b8%87%e0%b8%a8%e0%b8%b6%e0%b8%81%e0%b8%a9%e0%b8%b2%e0%b8%98%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a3") 
        
    elif  newwwType==3 :
        page = requests.get("https://mthai.com/tag/%E0%B9%82%E0%B8%84%E0%B8%A7%E0%B8%B4%E0%B8%94-19") 
        
    elif  newwwType==4 :
        page = requests.get("https://mthai.com/tag/%E0%B8%9E%E0%B8%A2%E0%B8%B2%E0%B8%81%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B8%AD%E0%B8%B2%E0%B8%81%E0%B8%B2%E0%B8%A8")
        
    elif  newwwType==5 :
        page = requests.get("https://mthai.com/tag/%e0%b8%a3%e0%b8%96%e0%b9%83%e0%b8%ab%e0%b8%a1%e0%b9%88")  
    elif newwwType==6 :
        page = requests.get("https://mthai.com/women")
    elif newwwType==7 :
        page = requests.get("https://mthai.com/entertainment")
    elif newwwType==8 :
        page = requests.get("https://mthai.com/food")
    else:
        page = requests.get("https://mthai.com") 
    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.find_all('a')
    title = []
    href = []
    paragraphs = []
    for x in links:
        if x.get('title'):
            paragraphs.append(str(x))

            title.append(x.get('title'))
            href.append(x.get('href'))
            #print(x.get('title'))
         
            #print(x.get('href'))            
            #print(set(title),set(href))

    sran = random.randint(0,len(title))
    print(sran)
    answer_function = title[sran]+'\n'+href[sran]
    print(answer_function)
    return answer_function
    
def SICKNESS_advise(respond_dict): 


    Sickness_value = respond_dict["queryResult"]["outputContexts"][2]["parameters"]["Value.original"]
    
    Advise =''
    print ( Sickness_value)
    print ("แขกแขกแขก")
  
    Covid=set([1,2,6,7])
    Diabete=set([11,12,15])
    Legend=set([16])
    Sickness_value
    number = [int(s) for s in Sickness_value.split() if s.isdigit()]
    GoodNumber=set(number)
    Alert=set(GoodNumber)
    
 
 
    for i in GoodNumber:
      
    
   
    
        if  i==1 :
            #page = requests.get("https://mthai.com/sport") 
            Advise=Advise+"1.ตัวร้อน มีไข้\n"
            Advise=Advise+"หากปวดมาก หนาวสั่น อาเจียน ก้มคอไม่ลง หอบเหนื่อย เหงื่อออก ตัวเย็น\n"
            Advise=Advise+"ปัสสาวะออกน้อย ควรไปพบแพทย์โดยเร็วที่สุด\n"
            Advise=Advise+"-ถ้าไม่มีอาการข้างต้นให้ +นอนพัก\n"
            Advise=Advise+"                           +ดื่นน้ำ น้ำหวาน น้ำข้าวต้มมากๆ\n"
            Advise=Advise+"                           +ถ้าไข้สูง ใช้ผ้าชุบน้ำเช็ดตัว\n"
            Advise=Advise+"                           +ถ้าไข้สูงให้กินยาพาราเซตามอลทุก 4-6 ชั่วโมง\n"
            Advise=Advise+"                           -หากไข้ไม่หายใน3-4 วัน หรืออาการทรุดลง ควรไปพบแพท์ให้เร็วที่สุด\n"
            Advise=Advise+"\n"
        elif  i==2 :
          #  page = requests.get("https://mthai.com/tag/%e0%b8%81%e0%b8%a3%e0%b8%b0%e0%b8%97%e0%b8%a3%e0%b8%a7%e0%b8%87%e0%b8%a8%e0%b8%b6%e0%b8%81%e0%b8%a9%e0%b8%b2%e0%b8%98%e0%b8%b4%e0%b8%81%e0%b8%b2%e0%b8%a3") 
            Advise=Advise+"2.ไอ\n"
            Advise=Advise+"งดบุหรี่ อย่ากินของมัน ของทอด\n"
            Advise=Advise+"+ถ้าไอต่อเนื่องจากเป็นหวัด คันคอ ให้จิบยาแก้ไอ\n"
            Advise=Advise+"+ถ้าไอมีเสมหะเหนียวสีขาว ให้ดื่มน้ำอุ่นและพักผ่อนให้มากๆ ห้ามจิบยาแก้ไอ\n"
            Advise=Advise+"-ถ้ามีเสมหะสีเหลืองหรือเขียว ควรไปพบแพทย์\n"
            Advise=Advise+"-ถ้าไอนานกว่า2สัปดาห์โดนไม่มีสาเหตุ หรืออ่อนเพลีย น้ำหนักลด ควรไปพบแพทย์\n"
            Advise=Advise+"\n"
        elif  i==3 :
           # page = requests.get("https://mthai.com/tag/%E0%B9%82%E0%B8%84%E0%B8%A7%E0%B8%B4%E0%B8%94-19") 
            Advise=Advise+"3.ปวดหัว\n"
            Advise=Advise+"-ถ้ารุนแรงอย่างไม่เคยเป็นมาก่อน อาเจียน ตาพร่า ปวดร้าวตามแขน มือ\n"
            Advise=Advise+"เท้าชาหรืออ่อนแรง เดินเซ ปวดถี่และแรงขึ้น หรือปวดติดจ่อเกิน 3 วัน\n"
            Advise=Advise+"ควรไปพบแพทย์\n"
            Advise=Advise+"+ให้ยาหม่องทานวด ถ้าไม่หายให้กินยาแก้ปวด\n"
            Advise=Advise+"-ถ้าไม่ดีขึ้น 1 สัปดาห์ ควรไปพบแพทย์\n"
            Advise=Advise+"+ปวดหัวเพราะไมเกรน กินยาแก้ปวดทันทีที่เริ่มมีอาการ\n"
            Advise=Advise+"หากเป็นบ่อยๆควรไปพบแพทย์\n"
            Advise=Advise+"\n"
        elif  i==4 :
           # page = requests.get("https://mthai.com/tag/%E0%B8%9E%E0%B8%A2%E0%B8%B2%E0%B8%81%E0%B8%A3%E0%B8%93%E0%B9%8C%E0%B8%AD%E0%B8%B2%E0%B8%81%E0%B8%B2%E0%B8%A8")
            Advise=Advise+"4.ท้องเสีย\n"
            Advise=Advise+"+ให้ดื่มน้ำแร่ กินน้ำข้าวต้มใส่เกลือ และดื่มน้ำให้มากๆ\n"
            Advise=Advise+"+หากมีไข้ร่วมด้วย ให้กินยาลดไข้หรือพาราเซตามอล\n"
            Advise=Advise+"-ห้ามกินยาเพื่อหยุดถ่าย\n"
            Advise=Advise+"-ถ้าไม่ดีขึ้นใน 48 ชั่วโมงหรือมีอาการอาเจียน ดื่มน้ำเกลือไม่ได้ หรือขาดน้ำรุนแรง\n"
            Advise=Advise+"ถ่ายมีมูกเลือดปน ค้องไปพบแพทย์โดยด่วน\n"
            Advise=Advise+"\n"
        elif  i==5 :
            Advise=Advise+"5.ครั่นเนื้อครั่นตัว\n"
            Advise=Advise+"+ควรใส่เสื้อหนาๆ หรือผ้าห่ม และดื่มของเรื่องๆเพื่อให้เหงื่อออก\n"
            Advise=Advise+"-ห้ามอาบน้ำเย็น หรือทานของเย็น\n"
            Advise=Advise+"+ดื่มน้ำให้เพียงพอและพักผ่อนนอนหลับให้เพียงพอ\n"
            Advise=Advise+"\n"
        elif  i==6 :
            Advise=Advise+"6.หายใจติดขัด\n"
            Advise=Advise+"-หายใจไม่ออก เหนื่อยหอบ แน่นอก เหงื่อท่วมตัว อาจเป็นโรคหัวใจ\n"
            Advise=Advise+"ให้รีบอมหรือพ่นยาทันทีและไปหาแพทย์ให้เร็วที่สุด\n"
            Advise=Advise+"-หายใจหอบ มีไข้ เจ็บหน้าอก อาจเป็นปอดอักเสบ ต้องรีบไปพบแพทย์โดยเร็ว\n"
            Advise=Advise+"\n"
            
        elif  i==7 :
             Advise=Advise+"7.ปวดเมื่อย\n"
             Advise=Advise+"+ห้ามตรากตรำทำงาน นอนหลับพักผ่อนให้เพียงพอ\n"
             Advise=Advise+"-หากมีไข้สูงเกิน38.5 ห้ามนวด\n"
             Advise=Advise+"\n"
        elif  i==8 :
            Advise=Advise+"8.วิงเวียน\n"
            Advise=Advise+"-หากมีอาการใจหวิวใจสั่น ชีพจรเต้นเร็ว เหงื่อท่วม ลุกนั่งจะเป็นลม เจ็บหน้าอก\n"
            Advise=Advise+"ปวดท้องอาเจียนรุนแรง อุจจาระดำ ต้องรีบไปหาหมอโดยเร็วที่สุด\n"
            Advise=Advise+"+เมื่อวิงเวียนให้นอนลงซักพักแล้วลุกขึ้นอย่างช้าๆ หากยังมีอาการให้กินยาหอม\n"
            Advise=Advise+"-ถ้าเป็นๆหายๆเรื้อรัง ควรพบแพทย์\n"
            Advise=Advise+"-ถ้าอาการบ้านหมุน ควรไปพบแพทย์\n"
            Advise=Advise+"\n"
        elif  i==9 :
            Advise=Advise+"9.เป็นผื่น\n"
            Advise=Advise+"-ไม่ควรเกา เพราะยิ่งเกาจะยิ่งคันและเห่อ\n"
            Advise=Advise+"+ใช้น้ำแข็ง หรือ น้ำเย็นประคบ และทาด้วยยาแก้ผดผื่นคัน หรือสมุนไพรแก้ผื่นคัน\n"
            Advise=Advise+"+ควรหาสาเหตุว่ากินอะไรหรือถูกกับอะไรเข้า และหลีกเลี่ยง\n"
            Advise=Advise+"-เป็นเรื้อรังควรไปพบแพทย์\n"
            Advise=Advise+"\n"
        elif  i==10 :
            Advise=Advise+"10.คัดจมูก\n"
            Advise=Advise+"+กินยาแก้แพ้ ครึ่งเม็ดหรือ1เม็ด วันละ2-3 ครั้ง หรือ ใช้สมุนไพรหอมแดง 2-3 ต้น\n"
            Advise=Advise+"นำไปทำอาหารรับประทาน หรือสูดดมยาหม่อง\n"
            Advise=Advise+"+ออกกำลังกายให้มากขึ้น\n"
            Advise=Advise+"-ถ้าไม่ดีขึ้นใน 1-2 สัปดาห์ควรไปพบแพทย์\n"
            Advise=Advise+"\n"
        elif i==11 :
        #ปัสวะ
            pass
        elif i==12 :
        #เป็นแผลหายยาก
            pass
        elif i==13 :
        #บวมน้ำ
            pass
        elif i==14 :
        #ตะคริว
            pass
        elif i==15 :
        #ชาปลายมือปลายเท้า
            pass
        elif i==16 :
        #ปวดเข่า
            pass
        else:
            Advise=Advise+"\n"
            Advise=Advise+"\n"
            
            Advise=Advise+"___รบกวนอย่าลืมใส่เลขแยกกันตั้งแต่ 1-15 ให้ถูกต้องด้วยนะคะ___\n"
            Advise=Advise+"\n"
            Advise=Advise+"\n"
            
            
            print ("เอลลลลลลลลลลลลล") 
            
            
            #answer_from_bot = {"fulfillmentText": "/////////////////////////////////////////"}
    
      #Convert dict to JSON
           # answer_from_bot = json.dumps(answer_from_bot, indent=4) 
            #r = make_response(answer_from_bot)
           # r.headers['Content-Type'] = 'application/json'
            
    if Covid.issubset(Alert):
        Advise=Advise+"!!!!!อาการของท่านอยู่ในหมวดหมู่ของอาการเริ่มต้นของCovid-19 หากทบทวนว่าได้เดินทางไปในพิ้นที่เสี่ยงแนะนำให้ไปพบแพทย์โดยเร็วที่สุดค่ะ!!!!!\n\n"
    if Diabete.issubset(Alert):
        Advise=Advise+"!!!!!อาการของท่านอยู่ในหมวดหมู่ของอาการเริ่มต้นของเบาหวาน หากสงสัยควรพบแพทย์โดยเร็ว!!!!!\n\n"
    if Legend.issubset(Alert):
        Advise=Advise+"!!!!!ระวังอาการเสี่ยงจะเป็นโรคไขข้อกระดูกเสื่อม!!!!!\n\n"
    print ( Advise)    
    answer_function = Advise
    print(answer_function)
    return answer_function
    
#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)