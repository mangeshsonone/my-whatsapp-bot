from django.shortcuts import render

from twilio.rest import Client
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import json 
import os
from dotenv import load_dotenv
from .models import Samaj,Family,Member,FamilyHead
from django.core.exceptions import ObjectDoesNotExist

load_dotenv()

# Twilio Credentials


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
content_sid = os.getenv('CONTENT_SID')


content_sid = os.getenv('CONTENT_SID')


client = Client(account_sid, auth_token)
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Send WhatsApp Template Message with Quick Reply Buttons
def message_to(request):
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        from_=TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:+917775889251',
        content_sid=content_sid,
        content_variables='{"1":"12/1","2":"3pm"}'
    )
    return HttpResponse("Message sent to WhatsApp")




    



def addin_database(all_data):
    print("Received Data:", all_data)

    # Get or create Samaj
    s_name = all_data.get('samaj_name')
    samaj, _ = Samaj.objects.get_or_create(samaj_name=s_name)

    # Get or create Family
    surname = all_data.get('surname')
    family, _ = Family.objects.get_or_create(samaj=samaj, surname=surname)

    # Process Family Head
    head_data = all_data.get('head of family')
    if head_data:
        head_data['family'] = family  
        head_data['name_of_head'] = head_data.pop('name') 
        head_data['age'] = int(head_data['age']) 
        

        valid_head_fields = {field.name for field in FamilyHead._meta.get_fields()}
        
        head_data = {k: v for k, v in head_data.items() if k in valid_head_fields}

        
        family_head = FamilyHead.objects.create(**head_data)
    else:
        print("No family head data provided!")
        return

    
    members_list = all_data.get('members_list').get('the_members')
   
    for member_key, member_data in members_list.items():
        member_data['family_head'] = family_head  
        member_data['age'] = int(member_data['age'])
    

        valid_member_fields = {field.name for field in Member._meta.get_fields()}
        member_data = {k: v for k, v in member_data.items() if k in valid_member_fields}

        Member.objects.create(**member_data)
    
        
     
all_data={}

def memberdetail(md,msg,h):
     step=md['step']
     if step==0:
        reply=f"enter name of {h}"
        print(all_data)
        md['step']=1
        print("\n\n\n")
        print(all_data)
        print(reply)
        print("\n\n\n")
        return reply
    
     
     if step==1:
        md['name']=msg
        reply=f"enter age of {h}"
        md['step']=2
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==2:
        md['age']=msg
        reply=f"enter gender of {h}"
        md['step']=3
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==3:
        md['marital_status']=msg
        reply=f"enter qualification of {h}"
        md['step']=4
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply

     elif step==4:
        md['qualification']=msg
        reply=f"enter occupation of {h}"
        md['step']=5
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==5:
        md['occupation']=msg
        reply=f"exact_nature_of_duties of {h}"
        md['step']=6
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==6:
        md['enter exact_nature_of_duties']=msg
        reply=f"enter state of {h}"
        md['step']=7
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==7:
        md['state']=msg
        reply=f"enter district of {h}"
        md['step']=8
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==8:
        md['district']=msg
        reply=f"enter permanent_address of {h}"
        md['step']=9
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==9:
        md['permanent_address']=msg
        reply=f"enter landline_no of {h}"
        md['step']=10
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==10:
        md['landline_no']=msg
        reply=f"enter phone_no of {h}"
        md['step']=11
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==11:
        md['phone_no']=msg
        reply="enter alternative_no of {h}"
        md['step']=12
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==12:
        md['alternative_no']=msg
        reply="enter email_id of {h}"
        md['step']=13
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==13:
        md['email_id']=msg
        md['step']=14
        reply="enter submit"
        
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
     
     elif step==14:
        md['email_id']=msg
        md['step']=15
        reply=" enter ok to continue"
        
        print(all_data)
        print("\n\n\n")
        print(reply)
        return reply
  
     elif step==15:
        
        reply="Need to add members data enter ok to continue"
        md['step']=15
        print(all_data)
        print(reply)
        return reply
     
    

     

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        return HttpResponse("Webhook is active. Use POST to send messages.", status=200)

    if request.method == 'POST':
        from_number = request.POST.get('From')  # Sender's WhatsApp number
        message_body = request.POST.get('Body')  # User message

        message_body = request.POST.get('Body')  # User message

        print(f"Received WhatsApp message from {from_number}: {message_body}")

        
        response = MessagingResponse()
        
        

        
        if from_number not in all_data:
            all_data[from_number] = {}
            all_data["step"]=6
        step = all_data["step"]
        print(step)
        Step-based conversation
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
            reply = f"Thank you! You entered:\nSamaj: {all_data['samaj_name']}\nSurname: {message_body}\n Need to Enter details of the Head of the Family, enter ok to continue"
            all_data["step"] = 3  # End or continue with next step

            print("\n\n\n")
            print(reply)
            print("\n\n\n")
            


        elif step==3:
             if "head of family" not in all_data:
                all_data["head of family"] = {}
             msg=message_body
             if 'step' not in all_data["head of family"]:
                 all_data["head of family"]["step"]=0

             reply=memberdetail(all_data["head of family"],msg,"head of family")
             print("step in webhook ",all_data["head of family"]["step"])
             if all_data["head of family"]["step"]==15:
                 print("step in webhook and in if ",all_data["head of family"]["step"])
                 all_data["step"] = 4
                 print(all_data)
            
             
             
             

        elif step==4:
            reply="how many members are there in your family"
            all_data["step"] = 5

            print("\n\n\n")
            print(reply)
            print("\n\n\n")

             

        elif step==5:
             msg=message_body
             if "members_list" not in all_data:
                all_data["members_list"] = {}
                if 'tota_members' not in all_data["members_list"]:
                    all_data["members_list"]['total_members']=int(message_body)
                    all_data["members_list"]['current_member']=1

             

             c=all_data["members_list"]['current_member']
             if 'the_members' not in all_data["members_list"]:
                all_data["members_list"]["the_members"]={}
             
             
             
             if f"member{c}" not in all_data["members_list"]['the_members']:
                    all_data["members_list"]['the_members'][f"member{c}"]={}

             if "step" not in all_data["members_list"]['the_members'][f"member{c}"]:
                    all_data["members_list"]['the_members'][f"member{c}"]["step"]=0
                 
                 
             reply=memberdetail(all_data["members_list"]['the_members'][f"member{c}"],msg,f"member{c}")
             
             if all_data["members_list"]['the_members'][f"member{c}"]["step"]==14:
                    all_data["members_list"]['current_member']=all_data["members_list"]['current_member']+1
                    print("\n\n\n")
                    
             print("the current member is",all_data["members_list"]['current_member'])
             if all_data["members_list"]['current_member']==all_data["members_list"]['total_members']+1:
                 print('currentcurrent')
                 all_data["step"] = 6

             print(all_data)



        elif step==6:

                
                
                addin_database(all_data)
                reply="data is recorded successfully"
                # all_data["step"] = 7

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

       
        
        response.message(reply)
        
        return HttpResponse(str(response), content_type="text/xml")

    return HttpResponse("Invalid request method", status=400)
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
             
            from_='whatsapp:+14155238886',  
            to='whatsapp:+917775889251', 
             
            content_variables='{}'
        )

         return JsonResponse({"message_sid": message.sid,"status": message.status})

    # return JsonResponse({"error": "Invalid request method"}, status=400)

def gotobutton(request):
     return JsonResponse("message_sid")




























 
 