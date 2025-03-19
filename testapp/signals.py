from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FamilyHead, Member
from .main import add_familyhead_to_sheet,add_familymembers_to_sheet, get_google_sheet_for_head,get_google_sheet_for_members

@receiver(post_save, sender=FamilyHead)
def add_family_head_to_sheet(sender, instance, created, **kwargs):
    if created:
        # Assuming sheet_id is the ID of your Google Sheet.
        sheet_id = '1GT5mk7bnFBIzCBrQgF1G8AmQfW024WRt-IREw9dLN2g'
        worksheet = get_google_sheet_for_head(sheet_id)

        # Add family head data
        add_familyhead_to_sheet(worksheet, instance)

@receiver(post_save, sender=Member)
def add_member_to_sheet(sender, instance, created, **kwargs):
    if created:
        # Assuming sheet_id is the ID of your Google Sheet.
        sheet_id = '11YaTF5xwRtipqTQMREsiFkyzr6_KTKf06HF_btStP08'
        worksheet = get_google_sheet_for_members(sheet_id)

        # Add member data
        add_familymembers_to_sheet(worksheet, instance.family_head, [instance])
