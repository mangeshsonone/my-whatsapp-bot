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


    ```


7. **twilio setup:**

   ```bash
    Install Twilio Python Package
    First, you need to install the Twilio package. Run the following command:

    
    pip install twilio

    Create a Twilio Account
    Go to Twilio's website and sign up for an account if you don't already have one.

    Get Your Twilio Credentials
    Once you've signed up, log in to the Twilio console and grab the following credentials:

    Account SID
    Auth Token
    WhatsApp-enabled Twilio phone number (Make sure you get a number that supports WhatsApp)
    You can find these in your Twilio console.

    Configure Twilio in Your Project
    In your project, set up your environment variables or configuration file with the Twilio credentials.

     you can store them in a .env file: to connect twilio to whatsapp

    Scan twilo qr from sandbox in messeging column to connect twilio to whatsapp

    Add webhook url in "When a message comes in" column, save.
    
    ```

7. **start working with whatsapp bot:**

    ```bash
    as twilio, whatsapp and backend webhook is setup,
    enter start or any key in twilio (whatsapp contact).

    you will get connected to whatsapp bot.

    ```
