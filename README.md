# whatsappbot
This project is designed to manage family and member data in a Samaj system. It provides features like:
- Storing and retrieving family details, including family head and members.
- Adding new Samaj entries to the database.
- Storing and organizing member details (age, name, family association).

## Installation

Provide instructions on how to set up and run the project locally.

1. **Clone the repository:**

    ```bash
    git clone https://github.com/mangeshsonone/my-whatsapp-bot.git
    cd project-name
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Database setup (if applicable):**

    

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the application:**

    

    ```bash
    python manage.py runserver


    ```

6. **Connect Localhost with Ngrok:**

    ```bash
   
    Steps to Connect Localhost with Ngrok:
    Download and Install Ngrok

    Visit the Ngrok website to download Ngrok for your operating system.
    Extract the downloaded file and place it in a directory of your choice.
    
    Open a terminal window and run the following command to start ngrok, where 8000 is the port your server is running on:

    ngrok http 8000

    Ngrok will start and display a public URL (something like https://abcd1234.ngrok.io) in your terminal that tunnels to your local server.

    Use ngrok url insted of localhost url.


    ```


7. **twilio setup:**

   ```bash
    Install Twilio Python Package
    First, you need to install the Twilio package. Run the following command:

    
    pip install twilio

    Create a Twilio Account
    Go to Twilios website and sign up for an account if you dont already have one.

    Get Your Twilio Credentials
    Once youve signed up, log in to the Twilio console and grab the following credentials:

    Account SID
    Auth Token
    WhatsApp-enabled Twilio phone number (Make sure you get a number that supports WhatsApp)
    You can find these in your Twilio console.

    Configure Twilio in Your Project
    In your project, set up your environment variables or configuration file with the Twilio credentials.

     you can store them in a .env file: to connect twilio to whatsapp

    Scan twilo qr from sandbox in messeging column to connect twilio to whatsapp or save the whatsapp number
    provided by twilio.

    Add webhook url in "When a message comes in" column in sandbox settings, save.
    
    ```

7. **start working with whatsapp bot:**

    ```bash
    as twilio, whatsapp and backend webhook is setup,
    open whatsapp, you will see twilio contact is added,
    type 'start' or type any key in twilio (whatsapp contact) and send.


    you will get connected to whatsapp bot.
    

    ```

### webhookflow
8. **webhook integration process and flow:**

    ```bash

        whatsapp_webhook - Twilio WhatsApp Webhook Handler

The whatsapp_webhook function is a view that handles incoming WhatsApp messages sent via Twilio. It processes the user's input step-by-step, collects information about the user's Samaj and family, and stores it in a structured format.

Overview

This webhook is designed to interact with users via WhatsApp, guiding them through a series of steps to collect their family and Samaj information. The flow progresses with each message from the user, using a state machine approach where the current step is tracked in the all_data dictionary.
GET request: Used to confirm that the webhook is live. Responds with a status message.
POST request: Used to receive and process messages from the user. Based on the message, it guides the user through a set of steps, starting with asking for the Samaj name, family name, the number of family members, head of the family, and so on.
HTTP Methods
GET: Confirms the webhook is active.
Response: "Webhook is active. Use POST to send messages."
POST: Processes the message from the user.
Request Body: Contains data from Twilio, such as the sender's phone number (From) and the message body (Body).
Flow of Execution

Step 0 (Initial State):


Expected Input: Any message from the user.
Response: "Welcome! What is the name of your Samaj? (Please enter one of the following: Brahmin, Kshatriya, Vaishya, Shudra)"
Add the samaj in the all_data dictionary in key value pairs.
Next Step: Step 1.
Step 1 (Samaj Name):


Expected Input: A valid Samaj name ("Brahmin", "Kshatriya", "Vaishya", "Shudra").
Response: If valid, acknowledges the Samaj name and asks for the family name. If invalid, asks the user to enter a valid Samaj name.
Next Step: Step 2.
Step 2 (Family Name):


Expected Input: The family name.
Response: Acknowledges the family name and asks for the number of family members. The user can choose to go back by typing 'R'.
Next Step: Step 3.
Step 3 (Number of Family Members):


Expected Input: A number representing the total family members.
Response: Confirms the number of family members and asks the user to continue to enter the head of the family details.
Next Step: Step 4.
Step 4 (Head of the Family Information):


Expected Input: The user enters detailed information about the head of the family.
Response: Collects the information step-by-step, asks the user to confirm or go back if needed.
Next Step: Step 5 (Once all required details are entered).
Step 5 (Members Information):


Expected Input: Information for each family member.
Response: Collects member details one by one, confirming each member's data before proceeding to the next.
Next Step: Step 6 (Final step when all members' details are collected).
Example of all_data dictionary:
	all_data = {
    "info_from_number": "whatsapp:+1234567890",
    "step": 1,
    "samaj_name": "Brahmin",
    "surname": "Sharma",
    "members_list": {
        "total_members": 4,
        "current_member": 1,
        "the_members": {
            "member1": {"name": "John", "age": 35}
        }
    }
}



Created a function(memberdetail(md, msg, h)):


Purpose:
The memberdetail function is designed to interact with the user step-by-step and gather various details for a family member (like name, age, gender, marital status, etc.). The function handles each input by progressing through a series of steps, storing the data, and guiding the user through input validation and the next required step.
Parameters:
md: A dictionary containing the current data and state of the user interaction. It tracks the input details for a family member.
msg: The message (input from the user) that the function processes for the current step.
h: A string representing the "head" or a specific "member" of the family for which details are being gathered (e.g., "spouse", "child").
Returns:
A string response to the user, indicating either the next step in the interaction or a request for re-entry if the input is invalid.
The response also includes logging information at each step for debugging and tracking purposes.
Steps and Functionality:

Step 0 - Requesting Name:
The function begins by asking for the name of the member (h).
If the step is 0, it prompts the user to enter the name, then proceeds to step 1.

Step 1 - Storing Name:
After the name is entered, the function stores the name and asks for the age of the member.
If the member is the "head of family," the next step asks for the age.
If the member is not the "head of family," it moves to request the relation to the head of the family.

Step -1 - Requesting Relation:
If the user opts to re-enter the previous step ('R'), it goes back to step 1.
Otherwise, it stores the relation of the member to the head of the family and asks for the age.

Step 2 - Requesting Age:
After the user provides the age, if the input is valid (a positive number), it proceeds to ask for gender.
If the input is invalid (e.g., non-numeric), it asks the user to enter a valid age.

Step 3 - Requesting Gender:
The function prompts the user to enter the gender (Male, Female, Other).
If the input is valid, it proceeds to the marital status step.
If the input is invalid, it requests a valid gender input.

Step 4 - Requesting Marital Status:
The function asks the user to provide the marital status (Single, Married, Divorced, Widowed).
If the input is valid, it moves to the next step, requesting the qualification.
If invalid, it asks for a valid marital status.

Step 5 - Requesting Qualification:
After storing the qualification, the function asks for the occupation of the member.

Step 6 - Requesting Occupation:
After receiving the occupation, the function asks for the exact nature of duties.

Step 7 - Requesting Nature of Duties:
The function asks for the nature of duties. If the user is the head of the family, it proceeds to the next step requesting the state of residence. Otherwise, it skips to step 12 (skipping certain input steps).

Step 8 - Requesting State:
The function asks for the state of the member's residence.

Step 9 - Requesting District:
After receiving the state, it asks for the district of the member's residence.

Step 10 - Requesting Permanent Address:
The function requests the permanent address of the member.

Step 11 - Requesting Landline Number:
The function asks for the member's landline number.
If the number is invalid (non-numeric), it asks the user to re-enter it or enter 'null'.

Step 12 - Requesting Phone Number:
The function asks for a phone number (a 10-digit number).
If the input is invalid, it asks for the correct 10-digit phone number.

Step 13 - Requesting Alternative Phone Number:
After entering the primary phone number, the function asks for an alternative phone number (also 10 digits).

Step 14 - Requesting Email ID:
The function requests the email ID of the member.

Step 15 - Requesting Date of Birth:
The function asks for the date of birth in the format dd-mm-yyyy.

Step 16 - Finalizing:
Once the user confirms all details, the function moves to finalize the process and prepares to add more members, if needed.
Input Validation:
At each step, the function checks for input validity (e.g., numeric inputs for age, phone number, and landline number).
If the input is invalid, the function requests the user to enter the correct value or re-enter the previous input.
Logging:
Each action, including entering details and any errors, is logged for debugging purposes.
The function uses different log levels (info, debug, warning, error) to track normal flow and exceptions.

8.Database Integration with addin_database()
After the collection and validation of all data, the addin_database() function stores the information in the database. The following actions are carried out:
Process Overview:
Retrieve or Create Samaj Object:


The Samaj object is fetched or created using the samaj_name provided in the input data.
Retrieve or Create Family Object:


A Family object is created using the surname and associated with the Samaj object.
Process Head of Family Data:


The head of the family’s data is extracted and stored, including their name, age, and other personal details.
The family_head is linked to the corresponding family.
Process Members Data:


Each family member is processed individually.
The family_head is associated with each member, and personal details like age and contact info are stored.
Error Handling:


If any part of the process fails (e.g., creation of Samaj or Family), the error is logged, and an appropriate message is returned.

3. Detailed Function Breakdown - addin_database()
Here’s a detailed breakdown of what happens in the addin_database() function:
Step 1: Log Data Received
The function logs all the incoming data:
python
Copy
logger.info("Received Data: %s", all_data)

Step 2: Handle Samaj Object
The Samaj object is retrieved or created from the database using the samaj_name key.
A success message is logged, or an error message is returned if the creation or retrieval fails.
python
Copy
samaj, created = Samaj.objects.get_or_create(samaj_name=s_name)
logger.info("Samaj '%s' %s.", s_name, 'created' if created else 'retrieved')

Step 3: Handle Family Object
Similarly, the Family object is retrieved or created using the surname and the associated Samaj.
The success or failure of this operation is logged.
python
Copy
family, created = Family.objects.get_or_create(samaj=samaj, surname=surname)
logger.info("Family with familyname '%s' %s.", surname, 'created' if created else 'retrieved')

Step 4: Process Family Head Data
The family head’s data is processed and stored.
The name field is renamed to name_of_head, and the age is converted to an integer.
The family head object is created in the database.
python
Copy
head_data['family'] = family
head_data['name_of_head'] = head_data.pop('name')
head_data['age'] = int(head_data['age'])

Step 5: Process Members Data
The function processes a list of members under the members_list key. Each member’s details are validated and added to the database.
Members are associated with the correct family_head.
python
Copy
members_list = all_data.get('members_list').get('the_members')
if members_list:
    for member_key, member_data in members_list.items():
        member_data['family_head'] = family_head
        member_data['age'] = int(member_data['age'])

Step 6: Error Handling
In case of errors during any stage of data processing, appropriate error messages are logged, and the process returns an error message.
python
Copy
except Exception as e:
    logger.error(f"Error while processing member data for '{member_key}': {str(e)}")
    return f"Error while processing member data for '{member_key}': {str(e)}"

Example of Logging for Data Integrity:
python
Copy
logger.info("Family head '%s' created successfully.", head_data['name_of_head'])
logger.info("Member '%s' added to the database.", member_data.get('name', 'Unknown'))


4. HTTP Response Handling
Once the data has been successfully recorded, the system responds with an XML message indicating success:
python
Copy
reply = "Data is recorded successfully"
msg = response.message(reply)
return HttpResponse(str(response), content_type="text/xml")

If the request method is invalid, the system returns a 400 status response indicating an error.
python
Copy
return HttpResponse("Invalid request method", status=400)


5. Error Handling and Logging
Comprehensive logging ensures that all operations, whether successful or not, are traced for debugging and data integrity purposes.
Examples of Logs:
Successful creation of Samaj, Family, and FamilyHead.
Warnings for missing family head data or member data.
Error logs for any issues encountered during database operations.
python
Copy
logger.warning("No family head data provided!")
logger.error(f"An error occurred while adding data to the database: {str(e)}")


6. Conclusion
The provided code efficiently collects, validates, and stores family data in the database, ensuring proper logging and error handling at every step. By using Django ORM, the data integrity is maintained, and relationships between Samaj, Family, FamilyHead, and Member objects are properly structured.
This code is an excellent starting point for building a user-friendly interface for managing family data and storing it systematically in a backend database.





    ```