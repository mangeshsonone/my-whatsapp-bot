import gspread
from django.db import models
from .models import FamilyHead, Member

def get_google_sheet_for_head(sheet_id, sender=None, credential_file='testapp/credential.json'):
    # Authenticate with Google Sheets using service account
    gc = gspread.service_account(filename=credential_file)
    sh = gc.open_by_key(sheet_id)
    

    # Add headers conditionally based on sender value
    available_sheets = sh.worksheets()  # List all worksheets
    print(f"Available sheets for FamilyHead sheet: {[sheet.title for sheet in available_sheets]}")
    
    
    worksheet = sh.sheet1
    add_headers_if_missing_for_head(worksheet)  # Add headers specific to FamilyHead data
    
    return worksheet

def get_google_sheet_for_members(sheet_id, sender=None, credential_file='testapp/credential.json'):
    # Authenticate with Google Sheets using service account
    gc = gspread.service_account(filename=credential_file)
    sh = gc.open_by_key(sheet_id)
    

    # Add headers conditionally based on sender value
    available_sheets = sh.worksheets()  # List all worksheets
    print(f"Available sheets for member sheet: {[sheet.title for sheet in available_sheets]}")
    
    
    worksheet = sh.sheet1
    add_headers_if_missing_for_members(worksheet)  # Add headers specific to FamilyHead data
    
    
    return worksheet


def get_model_fields(model_class):
    # This function dynamically gets field names from a Django model
    return {field.name for field in model_class._meta.get_fields()}

def add_headers_if_missing_for_head(worksheet):
    # Get current headers from the first row
    current_headers = worksheet.row_values(1)

    # Dynamically create headers based on the FamilyHead and Member models
    valid_head_fields = get_model_fields(FamilyHead)
    # valid_member_fields = get_model_fields(Member)
    

    # Combine valid fields to create a comprehensive header list
    all_headers =[
    'id',
    'name_of_head',
    'family',
    'age',
    'birth_date',
    'gender',
    'marital_status',
    'qualification',
    'occupation',
    'exact_nature_of_duties',
    'state',
    'district',
    'permanent_address',
    'landline_no',
    'phone_no',
    'alternative_no',
    'email_id',
    
    'info_from_number'
] 
    # + list(valid_member_fields)

    # Check if the current headers match the expected headers
    if not current_headers or current_headers != all_headers:
        worksheet.insert_row(all_headers, 1)
        print("Headers added to the Google Sheet.")
    else:
        print("Headers already exist in the Google Sheet, skipping header addition.")

def add_familyhead_to_sheet(worksheet, family_head, members_list=None):
    # Prepare the family head data
    family_head_data = [
    family_head.id,                            # field_name: id (assuming the model has an ID field)
    family_head.name_of_head,  
    family_head.family.surname,                        
    family_head.age,                           
    family_head.birth_date,                     # field_name: birth_date
    family_head.gender,                         # field_name: gender
    family_head.marital_status,                 # field_name: marital_status
    family_head.qualification,                  # field_name: qualification
    family_head.occupation,                     # field_name: occupation
    family_head.exact_nature_of_duties,        # field_name: exact_nature_of_duties
    family_head.state,                          # field_name: state
    family_head.district,                       # field_name: district
    family_head.permanent_address,              # field_name: permanent_address
    family_head.landline_no,                    # field_name: landline_no
    family_head.phone_no,                       # field_name: phone_no
    family_head.alternative_no,                 # field_name: alternative_no
    family_head.email_id,                       # field_name: email_id
                       
    family_head.info_from_number               # field_name: info_from_number
]

    
    # Append the family head data
    worksheet.append_row(family_head_data)  # Add FamilyHead data first

    # If members data is provided, append member data as well
    # if members_list:
    #     for member in members_list:
    #         member_data = [
    #             member.name,  # Member's name
    #             member.age,  # Member's age
    #             member.relation_with_family_head,  # Relationship to the Head
    #         ]
    #         worksheet.append_row(member_data)  # Add Member data

    print("Family and members data added to Google Sheet successfully.")


def add_headers_if_missing_for_members(worksheet):
    current_headers = worksheet.row_values(1)

    # Dynamically create headers based on the FamilyHead and Member models
    valid_head_fields = get_model_fields(FamilyHead)
    # valid_member_fields = get_model_fields(Member)
    

    # Combine valid fields to create a comprehensive header list
    all_headers =[
    'id',
    'name',
    'relation_with_family_head',
    'family_head',
    'age',
    'birth_date',
    'gender',
    'marital_status',
    'qualification',
    'occupation',
    'exact_nature_of_duties',
    'state',
    'district',
    'permanent_address',
    'landline_no',
    'phone_no',
    'alternative_no',
    'email_id',
    
    'info_from_number'
] 
    # + list(valid_member_fields)

    # Check if the current headers match the expected headers
    if not current_headers or current_headers != all_headers:
        worksheet.insert_row(all_headers, 1)
        print("Headers added to the Google Sheet.")
    else:
        print("Headers already exist in the Google Sheet, skipping header addition.")


def add_familymembers_to_sheet(worksheet, family_head, members_list=None):
    if members_list:
        for member in members_list:
            # Prepare the member data in the same order as defined in the headers for members
            member_data = [
                member.id,                                   # ID of the member
                member.name,                                  # Member's name
                member.relation_with_family_head,             # Relationship to the family head
                member.family_head.name_of_head,                        # Reference to the family head ID (foreign key)
                member.age,                                   # Age of the member
                member.birth_date,                            # Birth date of the member
                member.gender,                                # Gender of the member
                member.marital_status,                        # Marital status of the member
                member.qualification,                         # Qualification of the member
                member.occupation,                            # Occupation of the member
                member.exact_nature_of_duties,                # Exact nature of duties of the member
                member.state,                                 # State of the member
                member.district,                              # District of the member
                member.permanent_address,                     # Permanent address of the member
                member.landline_no,                           # Landline number of the member
                member.phone_no,                              # Phone number of the member
                member.alternative_no,                        # Alternative phone number of the member
                member.email_id,                              # Email ID of the member
                                          # Blood group of the member
                member.info_from_number                       # Info from number for the member
            ]

            # Append the member data to the Google Sheet
            worksheet.append_row(member_data)  # Add Member data

        print("Family members data added to Google Sheet successfully.")
    else:
        print("No members data provided to add to Google Sheet.")
