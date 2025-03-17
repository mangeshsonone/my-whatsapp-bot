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
import logging

load_dotenv()

# Twilio Credentials


account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
content_sid = os.getenv('CONTENT_SID')


content_sid = os.getenv('CONTENT_SID')


client = Client(account_sid, auth_token)
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"


logger = logging.getLogger('whatsapp_webhook')  

# Send WhatsApp Template Message with Quick Reply Buttons
def message_to(request):
    message = client.messages.create(
        # from_='+15856481063',
        # body='hello from twilio',
        # to='+917775889251'
        from_=TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:+918308522448',
        content_sid=content_sid,
        content_variables='{"1":"12/1","2":"3pm"}'
        
    )
    
    return HttpResponse("Message sent to WhatsApp")


def addin_database(all_data):
    # print("Received Data:", all_data)
    
    logger.info("Received Data: %s", all_data)

    
    s_name = all_data.get('samaj_name')
    samaj, created = Samaj.objects.get_or_create(samaj_name=s_name)
    logger.info("Samaj '%s' %s.", s_name, 'created' if created else 'retrieved')

    
    surname = all_data.get('surname')
    family, _ = Family.objects.get_or_create(samaj=samaj, surname=surname)
    logger.info("Family with familyname '%s' %s.", surname, 'created' if created else 'retrieved')

    
    head_data = all_data.get('head of family')
    if head_data:
        head_data['family'] = family  
        head_data['name_of_head'] = head_data.pop('name') 
        head_data['age'] = int(head_data['age']) 

        logger.info("Processing family head data: %s", head_data)
        

        valid_head_fields = {field.name for field in FamilyHead._meta.get_fields()}
        
        head_data = {k: v for k, v in head_data.items() if k in valid_head_fields}

        
        family_head = FamilyHead.objects.create(**head_data)
        logger.info("Family head '%s' created successfully.", head_data['name_of_head'])

    else:
        # print("No family head data provided!")
        logger.warning("No family head data provided!")
        return

    
    members_list = all_data.get('members_list').get('the_members')
   
    for member_key, member_data in members_list.items():
        member_data['family_head'] = family_head  
        member_data['age'] = int(member_data['age'])

        logger.info("Processing member data: %s", member_data)
    

        valid_member_fields = {field.name for field in Member._meta.get_fields()}
        member_data = {k: v for k, v in member_data.items() if k in valid_member_fields}

        Member.objects.create(**member_data)
        logger.info("Member '%s' added to the database.", member_data.get('name', 'Unknown'))
    
        
     
all_data={}
def memberdetail(md,msg,h):
     step=md['step']
     if step==0:
        reply=f"Enter name of the {h}"
        md['step']=1
        # print(all_data)
        # print("\n\n\n")  
        # print("\n\n\n")
        # print(reply)
        # print("\n\n\n")
        logger.info(f"Step 0: Requesting name for {h}. Reply: {reply}")
        
        
        logger.debug(f"Message received : {msg}")
        logger.debug(f"all_data before reply: {md}")
        
        return reply
    
     
     if step==1:
        
        md['name']=msg
        if md==all_data["head of family"]:
            md['step']=2
            reply=f"You entered Name: {msg}\nEnter the age of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            
        else:
            md['step']=-1
            reply=f"You entered Name: {msg}\Enter the relation of the {h} with the Head of the family."
            
        # print(all_data)
        # print("\n\n\n")
        # print(reply)
        logger.info(f" Reply: {reply}")
        logger.debug(f"all_data after step 1: {all_data}")
        return reply


     if step==-1:
        md['relation_with_family_head']=msg
        reply=f"You entered Relation: {msg}\nEnter the age of the {h}"
        md['step']=2
        # print("\n\n\n")
        # print(all_data)
        # print("\n\n\n")
        # print(reply)
        logger.debug(f"State of all_data after entering relation: {all_data}")
        
        logger.info(f"Reply message : {reply}")

        return reply

     
     elif step==2:
        if msg=="R" or msg=="r":
            md['step']=1
            reply = f"Going back!\nEnter the name of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 1 for {h}.")
            
        else:
            if msg.isdigit() and int(msg) > 0:
                md['age']=msg
                reply=f"You entered age: {msg},\nEnter the gender of the {h}\nEnter 'M' for 'Male', 'F' for 'Female', 'O' for 'Other'.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                md['step']=3
                # print("\n\n\n")
                # print(all_data)
                # print("\n\n\n")
                # print(reply)
                logger.info(f"User entered age for {h}: {msg}")
                logger.debug(f"State of all_data after entering age: {all_data}")
            else:
                reply=f" Invalid input. Please enter a valid number."
                logger.warning(f"User entered invalid input: {msg}. Expected a positive number.")
        
        # Log the reply message
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==3:
        if msg=="R" or msg=="r":
            md['step']=2
            reply = f"Going back!\nEnter the age of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 2 for {h}.")
        else:
            l=['M','F','O']
            if msg in l:
                md['gender']=msg
                reply=f"You entered Gender: {md['gender']}\nEnter marital_status of the {h}\nEnter 'S' for 'Single','M' for 'Married','D' for 'Divorced','W' for 'Widowed'.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                md['step']=4
                # print(all_data)
                # print("\n\n\n")
                # print(reply)
                logger.info(f"User entered gender for {h}: {md['gender']}")
                logger.debug(f"State of all_data after entering gender: {all_data}")
            else:
                reply=f" Invalid input. Please enter 'M' for 'Male', 'F' for 'Female', 'O' for 'Other'."
                logger.warning(f"User entered invalid input: {msg}. Expected from the options.")
        
        # Log the reply message
        logger.info(f"Reply message : {reply}")
        return reply

     elif step==4:
        if msg=="R" or msg=="r":
            md['step']=3
            reply = f"Going back!\nEnter the gender of the {h},(enter 'M' for 'Male', 'F' for 'Female', 'O' for 'Other')."
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 3 for {h}.")
        else:
            l=['S','M','D','W']
            if msg in l:
                md['marital_status']=msg
                reply=f"You entered Marital Status: {md['marital_status']}\nEnter the Qualification of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                md['step']=5
                # print(all_data)
                # print("\n\n\n")
                # print(reply)
                logger.info(f"User entered marital status for {h}: {md['marital_status']}")
                logger.debug(f"State of all_data after entering marital status: {all_data}")
            else:
                reply=f" Invalid input. Please enter 'S' for 'Single','M' for 'Married','D' for 'Divorced','W' for 'Widowed'."
                logger.warning(f"User entered invalid input: {msg}. Expected from the options.")
        # Log the reply message
        logger.info(f"Reply message : {reply}")
        return reply

     elif step==5:
        if msg=="R" or msg=="r":
            md['step']=4
            reply = f"Going back!\nEnter marital_status of the {h}\nEnter 'S' for 'Single','M' for 'Married','D' for 'Divorced','W' for 'Widowed'.'"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 4 for {h}.")
        else:
            md['qualification']=msg
            reply=f"You entered Qualification: {msg}\nEnter the Occupation of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=6
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered qualification for {h}: {md['qualification']}")
            logger.debug(f"State of all_data after entering qualification: {all_data}")
        
        # Log the reply message
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==6:
        if msg=="R" or msg=="r":
            md['step']=5
            reply = f"Going back!\nEnter the Qualification of the {h}?"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 5 for {h}.")
        else:
            md['occupation']=msg
            reply=f"You entered Occupation: {msg}\nExplain the exact nature of duties of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=7
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered occupation for {h}: {md['occupation']}")
            logger.debug(f"State of all_data after entering occupation: {all_data}")
        
        # Log the reply message
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==7:
        if msg=="R" or msg=="r":
            md['step']=6
            reply = "Going back!\nEnter the Occupation of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 6 for {h}.")
        else:
            if md==all_data["head of family"]:
                md['exact_nature_of_duties']=msg
                reply=f"You enter Exact nature of duties: {msg}\nEnter the State of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                md['step']=8
                # print(all_data)
                # print("\n\n\n")
                # print(reply)
                logger.info(f" exact nature of duties for {h}: {msg}")
                logger.debug(f"State of all_data after entering exact nature of duties for {h}: {all_data}")
                
            else:
                md['exact_nature_of_duties']=msg
                md['state']=all_data["head of family"]["state"]
                md['district']=all_data["head of family"]["district"]
                md['permanent_address']=all_data["head of family"]["permanent_address"]
                md['step']=12
                reply=f"You entered Exact nature of duties: {msg}\nEnter phone no of the {h}"
                # print(all_data)
                # print("\n\n\n")
                logger.info(f"User entered exact nature of duties for {h}: {msg}")
                logger.debug(f"State of all_data after entering exact nature of duties and updating member {h}: {all_data}")

        
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==8: 
        if msg=="R" or msg=="r":
            md['step']=7
            reply = f"Going back!\nExplain the exact nature of duties of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            # print(reply)  
            logger.info(f"User entered 'R'. Going back to step 7 for {h}.")
        else: 
            md['state']=msg
            reply=f"You entered State: {msg}\nEnter the District of the {h}" 
            md['step']=9
            print(all_data)
            print("\n\n\n")
            print(reply)
            logger.info(f"User entered state for {h}: {msg}")
            logger.debug(f"State of all_data after entering state for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==9:
        if msg=="R" or msg=="r":
            md['step']=8
            reply = f"Going back!\nEnter the State of the {h}"
            print(reply) 
            logger.info(f"User entered 'R'. Going back to step 8 for {h}.")
        else:
            md['district']=msg
            reply=f"You entered District: {msg}\nEnter permanent address of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=10
            print(all_data)
            print("\n\n\n")
            print(reply)
            logger.info(f"User entered district for {h}: {msg}")
            logger.debug(f"State of all_data after entering district for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==10:
        if msg=="R" or msg=="r":
            md['step']=9
            reply = f"Going back!\nEnter the District of the {h}"
            # print(reply) 
            logger.info(f"User entered 'R'. Going back to step 9 for {h}.")
        else:
            md['permanent_address']=msg
            reply=f"You entered Permanent address: {msg}\nEnter Landline no of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=11
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered permanent address for {h}: {msg}")
            logger.debug(f"State of all_data after entering permanent address for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==11:
        if msg=="R" or msg=="r":
            md['step']=10
            reply = f"Going back!\nEnter Permanent Address of the {h}"
            # print(reply) 
            logger.info(f"User entered 'R'. Going back to step 10 for {h}.")
            
        else:
            md['landline_no']=msg
            reply=f"You entered Landline no: {msg}\nEnter Phone_no of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=12
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered landline number for {h}: {msg}")
            logger.debug(f"State of all_data after entering landline number for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
        
     
     elif step==12:
        if msg=="R" or msg=="r":
            if md==all_data["head of family"]:
                md['step']=11
                reply = f"Going back!\nEnter Landline no of the {h}"
                # print(reply)
                logger.info(f"User entered 'R'. Going back to step 11 for {h}.")
            else:
                md['step']=7
                reply = f"Going back!\nExact nature of duties the {h}"
                # print(reply)
                logger.info(f"User entered 'R'. Going back to step 7 for {h}.")
        else:
            md['phone_no']=msg
            reply=f"You entered Phone no: {msg},\nEnter Alternative_no of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=13
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered phone number for {h}: {msg}")
            logger.debug(f"State of all_data after entering phone number for {h}: {all_data}")
        
        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==13:
        if msg=="R" or msg=="r":
            md['step']=12
            reply = f"Going back!\nEnter Phone no of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 12 for {h}.")
        else:
            md['alternative_no']=msg
            reply=f"You entered Alternative no: {msg}\nEnter email_id of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=14
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered alternative phone number for {h}: {msg}")
            logger.debug(f"State of all_data after entering alternative number for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply

     
     elif step==14:
        if msg=="R" or msg=="r":
            md['step']=13
            reply = "Going back!\nEnter Alternative no of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 13 for {h}.")
        else:
            md['email_id']=msg
            md['step']=15
            reply=f"You entered Email id: {msg}\nEnter Date of Birth of the {h}.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered email ID for {h}: {msg}")
            logger.debug(f"State of all_data after entering email for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply

     elif step==15:
        if msg=="R" or msg=="r":
            md['step']=14
            reply = "Going back!\nemail id of the {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 14 for {h}.")
        else:
            md['birth_date']=msg
            reply=f"You entered DOB: {msg},\nenter submit.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
            md['step']=16
            # print(all_data)
            # print("\n\n\n")
            # print(reply)
            logger.info(f"User entered date of birth for {h}: {msg}")
            logger.debug(f"State of all_data after entering date of birth for {h}: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
     
     elif step==16:
        if msg=="R" or msg=="r":
            md['step']=15
            reply = "Going back!\nEnter DOB of {h}"
            # print(reply)
            logger.info(f"User entered 'R'. Going back to step 15 for {h}.")
        else:
            md['step']=17
            reply="Need to add members data enter ok to continue"
            
            logger.info(f"User moved to step 17, preparing to add members data.")
            logger.debug(f"State of all_data after moving to step 17: {all_data}")

        # Log the reply message to be sent to the user
        logger.info(f"Reply message : {reply}")
        return reply
  
     elif step==16:
        
        
        reply="Need to add members data enter ok to continue"
        md['step']=17
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

        # print(f"Received WhatsApp message from {from_number}: {message_body}")
        logger.info(f"Received WhatsApp message from {from_number}: {message_body}")

        
        response = MessagingResponse()
        
        

        
        if f"info_from_number" not in all_data:
            all_data["info_from_number"] = from_number
            all_data["step"]=0
        step = all_data["step"]
        # print(step)
        logger.debug(f"Current step: {step}")
        
        if step == 0:
            reply = "Welcome! What is the name of your Samaj? (Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra)"
            all_data["step"] = 1
            print("\n\n\n")
            # print(reply)
            logger.info(f"Reply to user: {reply}")
            print("\n\n\n")

        elif step == 1:
            valid_samaj_names = ["Brahmin", "Kshatriya", "Vaishya", "Shudra"]
            
            if message_body.capitalize() in valid_samaj_names:
                all_data["samaj_name"] = message_body.capitalize()
                reply = f"Thank you! You entered:\nSamaj: {message_body} \nWhat is the name of your Family?\n\nor\n\n(Enter 'R' to Re-enter the previous input)."
                all_data["step"] = 2
                # print(all_data["samaj_name"])
                logger.info(f"Samaj name entered: {message_body.capitalize()},\n reply from user:{reply}")
            else:
                reply = "Invalid Samaj name. Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra."
                print("\n\n\n")
                    # print(reply)
                logger.warning(f"Invalid Samaj name entered: {message_body} Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra.")
                print("\n\n\n")

        elif step==2:
            if message_body=="R" or message_body=="r":
                reply = "Going back!\nWhat is the name of your Samaj?(Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra)"
                # print(reply)
                logger.info(f"User chose 'R'. Reply: {reply}")
                all_data["step"] = 1
            else:
                all_data["surname"] = message_body
                reply=f"You entered:\nFamily name: {message_body} \nHow many members are there in your family?\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                all_data["step"] = 3

                print("\n\n\n")
                # print(reply)
                logger.info(f" {reply}")
                print("\n\n\n")
    


                
        elif step == 3:
            if message_body=="R" or message_body=="r":
                reply = "Going back!\nWhat is the name of your family?"
                # print(reply)
                logger.info(f"User chose 'R'. Reply: {reply}")
                all_data["step"] = 2
                
            else:
                msg=message_body
                if message_body.isdigit() and int(message_body) > 0:
                    all_data["members_list"] = {}
                    # if 'tota_members' not in all_data["members_list"]:
                    all_data["members_list"]['total_members']=int(message_body)
                    all_data["members_list"]['current_member']=1

                    
                    reply = f"You have total {message_body} members in the family.\nNeed to enter the details of the Head of the family, enter 'ok' to continue.\n\nor\n\n(Enter 'R' to Re-enter the previous input)"
                    all_data["step"] = 4  
                    print("\n\n\n")
                    # print(reply)
                    logger.info(f"User entered valid number of total members: {message_body}. Reply: {reply}")
                    print("\n\n\n")
                else:
                    reply=f" Invalid input. Please enter a valid number."
                    logger.warning(f"User entered invalid input: {message_body}. Expected a positive number.")
                


        elif step==4:
            msg=message_body
            if "head of family" in all_data :
                if all_data["head of family"]["step"]>=1 and message_body=='R':
                    pass
                    # all_data["head of family"]["step"]-=1
                else:
                    pass
                reply=memberdetail(all_data["head of family"],msg,"Head of the family")
                # print("step in webhook ",all_data["head of family"]["step"])
                
                if all_data["head of family"]["step"]==17:
                        # print("step in webhook and in if ",all_data["head of family"]["step"])
                        logger.info(f"Step reached 17. Updating step to 5. Current all_data: {all_data}")
                        all_data["step"] = 5
                        # print(all_data)

            elif message_body=='R' or message_body=="r":
                all_data["step"] = 3
                reply = "Going back!\nHow many members are there in your family?"
                # print(reply)
                logger.info(f"User pressed 'R'. Reply: {reply}")

            elif "head of family" not in all_data:
                
                all_data["head of family"] = {}
                all_data["head of family"]["info_from_number"]=from_number
                logger.info(f"Initializing head of family with number: {from_number}")
                # msg=message_body
                if 'step' not in all_data["head of family"]:
                    all_data["head of family"]["step"]=0

                reply=memberdetail(all_data["head of family"],msg,"Head of the family")
                # print("step in webhook ",all_data["head of family"]["step"])
                logger.debug(f"Step in webhook after initialization: {all_data['head of family']['step']}")

                if all_data["head of family"]["step"]==17:
                        print("step in webhook and in if ",all_data["head of family"]["step"])
                        all_data["step"] = 5
                        # print(all_data)
                        logger.info(f"Step reached 17. Updating step to 5. Current all_data: {all_data}")


        elif step==5:
             msg=message_body
             
             if "members_list" not in all_data:
                all_data["members_list"] = {}
                if 'tota_members' not in all_data["members_list"]:
                    all_data["members_list"]['total_members']=int(message_body)
                    all_data["members_list"]['current_member']=1

             
                logger.info(f"Initializing members_list with total_members: {message_body}, current_member set to 1")

             c=all_data["members_list"]['current_member']
             if 'the_members' not in all_data["members_list"]:
                all_data["members_list"]["the_members"]={}
             
             
             
             if f"member{c}" not in all_data["members_list"]['the_members']:
                    all_data["members_list"]['the_members'][f"member{c}"]={}

             if "step" not in all_data["members_list"]['the_members'][f"member{c}"]:
                    all_data["members_list"]['the_members'][f"member{c}"]["step"]=0
                    all_data["members_list"]['the_members'][f"member{c}"]["info_from_number"]=from_number
                 
                    logger.info(f"Initializing member{c} details with step 0 and info_from_number: {from_number}")

             reply=memberdetail(all_data["members_list"]['the_members'][f"member{c}"],msg,f"member{c+1}")
             
             if all_data["members_list"]['the_members'][f"member{c}"]["step"]==16:
                    all_data["members_list"]['current_member']=all_data["members_list"]['current_member']+1
                    print("\n\n\n")
                    logger.info(f"Member {c} reached step 15. Incrementing current_member to {all_data['members_list']['current_member']}")

                    
            #  print("the current member is",all_data["members_list"]['current_member'])
             logger.debug(f"The current member is: {all_data['members_list']['current_member']}")
             if all_data["members_list"]['current_member']==all_data["members_list"]['total_members']:
                 print('currentcurrent')
                 all_data["step"] = 6

            #  print(all_data)
             logger.debug(f"Updated all_data: {all_data}")



        elif step==6:

                addin_database(all_data)
                reply="data is recorded successfully"
                # all_data["step"] = 7

                print("\n\n\n")
                print(reply)
                print("\n\n\n")

       
        
        msg=response.message(reply)
        
        return HttpResponse(str(response), content_type="text/xml")

    return HttpResponse("Invalid request method", status=400)
    return HttpResponse("Invalid request method", status=400)


def gotobutton(request):
     return HttpResponse("message_sid")



