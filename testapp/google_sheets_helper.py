
from gspread import worksheet
import gspread



gc=gspread.service_account(filename="testapp/credential.json")

sh=gc.open_by_key('11YaTF5xwRtipqTQMREsiFkyzr6_KTKf06HF_btStP08')
worksheet=sh.sheet1

res=worksheet.get_all_records()

student=["jay",20,"mumbai"]
worksheet.insert_row(student,1)
print(res) 


