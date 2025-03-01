from django.shortcuts import render

from twilio.rest import Client
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import json 
import os
from dotenv import load_dotenv
from .models import Samaj,Family,Member

load_dotenv()

# Twilio Credentials

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
content_sid = os.getenv('CONTENT_SID')


client = Client(account_sid, auth_token)
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Send WhatsApp Template Message with Quick Reply Buttons
def message_to(request):
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:+917775889251',
        content_sid=content_sid,
        content_variables='{"1":"12/1","2":"3pm"}'
    )
    return HttpResponse("Message sent to WhatsApp")




    
def addin_database(all_data):
     print("all data inside func",all_data)
     s_name=all_data['samaj_name']
     samaj= Samaj.objects.get(samaj_name=s_name)
     family,xyx= Family.objects.get_or_create(samaj=samaj, surname=all_data['surname'])

     member_data = all_data['members']
     member = Member.objects.create(
        family=family,
        name=member_data['name'],
        gender=member_data['gender'],
        age=member_data['age'],
        blood_group=member_data['bloodgroup'],
        mobile1=member_data['mobile'],
        
    )

     print(f" Successfully saved to DB: {member}")


        
     
all_data={}


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        return HttpResponse("Webhook is active. Use POST to send messages.", status=200)

    if request.method == 'POST':
        from_number = request.POST.get('From')  # Sender's WhatsApp number
        message_body = request.POST.get('Body')  # User message

        print(f"Received WhatsApp message from {from_number}: {message_body}")

        
        response = MessagingResponse()
        
        # if from_number not in all_data:
        #     all_data[from_number] = {}

        # response.message("reply") 

        
        if from_number not in all_data:
            all_data[from_number] = {}
            all_data["step"]=0
        step = all_data["step"]

        # Step-based conversation
        if step == 0:
            reply = "Welcome! What is the name of your Samaj? (Type your samaj from given: Brahmin, Kshatriya, Vaishya, Shudra)"
            all_data["step"] = 1
            print("\n\n\n")
            print(reply)
            print("\n\n\n")

        elif step == 1:
            valid_samaj_names = ["Brahmin", "Kshatriya", "Vaishya", "Shudra"]
            
            if message_body.capitalize() in valid_samaj_names:
                all_data["samaj_name"] = message_body.capitalize()
                reply = f"Thank you! You entered:\nSamaj: {message_body} \nWhat is your family surname?"
                all_data["step"] = 2
                print(all_data["samaj_name"])
            else:
                reply = "Invalid Samaj name. Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra."
            print("\n\n\n")
            print(reply)
            print("\n\n\n")

        elif step == 2:
            all_data["surname"] = message_body
            reply = f"Thank you! You entered:\nSamaj: {all_data['samaj_name']}\nSurname: {message_body}\n Enter your name"
            all_data["step"] = 3  # End or continue with next step

            print("\n\n\n")
            print(reply)
            print("\n\n\n")

        

        elif step==3:
                all_data['members']={}
                
                all_data['members']['name']=message_body
                reply="enter your age"
                all_data["step"] = 4
                print(all_data)

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

        elif step==4:
                
                all_data['members']['age']=message_body
                reply=f"entr your gender "
                all_data["step"] = 5
                print(all_data)

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

        elif step==5:
                
                all_data['members']['gender']=message_body
                all_data["step"] = 6
                reply=f"entr your bloodgroup "
                print(all_data)

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

        elif step==6:
                
                all_data['members']['bloodgroup']=message_body
                reply=f"entr your mobile no"
                all_data["step"] = 7
                print(all_data)

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

        elif step==7:
                
                all_data['members']['mobile']=message_body

                print("\n\n\n")
                print(all_data)
                print("\n\n\n")

                addin_database(all_data)
                all_data["step"] = 8
                reply = "Your data has been successfully saved!"
        

        else:
            reply = "We have recorded your details. Thank you!"

       
        
        response.message(reply)
        
        return HttpResponse(str(response), content_type="text/xml")

    return HttpResponse("Invalid request method", status=400)




@csrf_exempt  # Disable CSRF for external requests
def send_whatsapp_button(request):
    # if request.method == "POST":
        # to_number = request.POST.get("to", "")  # Get recipient number from request

        # if not to_number:
        #     return JsonResponse({"error": "Recipient number is required"}, status=400)

        # Send interactive message (buttons)
        
         message = client.messages.create(
            from_='whatsapp:+14155238886',  
            to='whatsapp:+917775889251', 
             
            content_variables='{}'
        )

         return JsonResponse({"message_sid": message.sid,"status": message.status})

    # return JsonResponse({"error": "Invalid request method"}, status=400)

def gotobutton(request):
     return JsonResponse("message_sid")




























 