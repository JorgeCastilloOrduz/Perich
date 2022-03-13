import subprocess
import random
from random import randint
from subprocess import call
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from pdf2image import convert_from_path


def mintCertificate(student_first_name,student_last_name,student_nin,course_name,professor_name,graduation_date):    
    token_call = str(subprocess.check_output("apps/new_token.sh"))
    token_id=str(token_call[55:len(token_call)-4])   
    image_name= createPDF(student_first_name,student_last_name,student_nin,course_name,professor_name,graduation_date,token_id)
    ipfs_result = subprocess.check_output("apps/add_ipfs.sh").decode("utf-8").split('\n')
    files = {}
    for i in ipfs_result:
        if i=="" or i[53:]=="certificates":
            continue
        files[i[53:].replace("certificates/","")[:-4]]=i[6:52]
    link = files[image_name]
    
    title="Certificado Académico - "+course_name 

    new_certificate(student_nin, token_id)   
    with open ('apps/mint.sh', 'w') as rsh:
        rsh.write("#!/bin/bash \n near call nftattootest.testnet nft_mint '{\"token_id\": \""+token_id+"\", \"receiver_id\": \"nftattootest.testnet\", \"token_metadata\": { \"description\":\""+" Certificamos que "+student_first_name+" "+student_last_name+ " completó el curso "+ course_name + "\",\"title\": \""+ title+"\",\"student_first_name \": \""+ student_first_name+"\", \"student_last_name \": \""+ student_last_name+"\", \"student_nin \": \""+ student_nin+"\", \"course_name \": \""+ course_name+"\", \"professor_name \": \""+ professor_name+"\", \"graduation_date \": \""+ graduation_date+"\",\"media\": \"https://ipfs.io/ipfs/"+link+"\", \"copies\": 1}}' --accountId nftattootest.testnet --deposit 0.1")

    # with open ('apps/mint.sh', 'w') as rsh:
    #     rsh.write("#!/bin/bash \n near view nftattootest.testnet nft_tokens_for_owner '{\"account_id\":\"nftattootest.testnet\"}")


    minted_result = subprocess.check_output("apps/mint.sh")
    nft_result = subprocess.check_output("apps/nft_tokens_for_owner.sh")
    new_nft = subprocess.check_output("apps/new_certificate.sh")
    return minted_result.decode("utf-8"), nft_result.decode("utf-8") 


def nft_list():
    id="nftattootest.testnet"
    with open ('apps/nft_tokens_for_owner.sh', 'w') as rsh:
        rsh.write("#!/bin/bash \n near view nftattootest.testnet nft_tokens_for_owner '{\"account_id\":\"nftattootest.testnet\"}' #")
    result = subprocess.check_output("apps/nft_tokens_for_owner.sh")
    return result.decode("utf-8") 

def nft_list_by_account(account):
    id="nftattootest.testnet"
    with open ('apps/nft_tokens_for_owner.sh', 'w') as rsh:
        rsh.write("#!/bin/bash \n near view nftattootest.testnet nft_tokens_for_owner '{\"account_id\":\""+account+"\"}' #")
    result = subprocess.check_output("apps/nft_tokens_for_owner.sh")
    return result.decode("utf-8")


def createPDF(student_first_name,student_last_name,student_nin,course_name,professor_name,graduation_date,token_id):
    PAGE_WIDTH  = defaultPageSize[1]
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=landscape(letter))

    #Nombre estudiante
    can.setFont('Helvetica', 30)
    name = student_first_name.upper()+" "+student_last_name.upper()
    text_width = stringWidth(name,'Helvetica', 30)
    y = 335
    x = ((PAGE_WIDTH-text_width) / 2.0)+15
    # x = (PAGE_WIDTH) / 2.0
    can.drawString(x, y, name)

    #Cédula
    can.setFont('Helvetica', 15)
    y = 305
    text_width = stringWidth("con cédula de ciudadanía "+student_nin,'Helvetica', 15)
    x = ((PAGE_WIDTH-text_width) / 2.0)+15
    can.drawString(x, y, "con cédula de ciudadanía "+student_nin)

    #Curso
    can.setFont('Helvetica', 20)
    y = 225
    text_width = stringWidth(course_name,'Helvetica', 20)
    x = ((PAGE_WIDTH-text_width) / 2.0)+15
    can.drawString(x, y, course_name)

    #Profesor
    can.setFont('Helvetica', 15)
    y = 165
    text_width = stringWidth(professor_name.upper(),'Helvetica', 15)
    x = ((PAGE_WIDTH-text_width) / 2.0)+15
    can.drawString(x, y, professor_name.upper())

    #Curso
    can.setFont('Helvetica', 15)
    y = 82
    text_width = stringWidth(graduation_date,'Helvetica', 15)
    x = ((PAGE_WIDTH-text_width) / 2.0)+15
    can.drawString(x, y, graduation_date)

    can.save()

    

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("apps/static/assets/certificates/certificado.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("apps/static/assets/certificates/certificado_nft.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    images = convert_from_path('apps/static/assets/certificates/certificado_nft.pdf')   
 
    for i in range(len(images)):
        images[i].save('apps/static/assets/certificates/certificado-'+token_id+'.jpg', 'JPEG')

    return "certificado-"+token_id

def new_certificate(student_national_id, token_id):
    print(token_id)
    print(type(token_id))
    with open ('apps/new_certificate.sh', 'w') as rsh:
        rsh.write("#!/bin/bash \n near call dev-1644439951111-36177096095742 setCertificate '{\"student_national_id\": \""+student_national_id+"\", \"token_id\": \""+token_id+"\"}' --accountId nftattootest.testnet --deposit 0.1")

    


    return None



# API
# print("Consultando la API de NEAR")
# print("espere....") 
# URL = 'https://rpc.testnet.near.org' 
# obj = {
#   "jsonrpc": "2.0",
#   "id": "dontcare",
#   "method": "query",
#   "params": {
#     "request_type": "call_function",
#     "finality": "final",
#     "account_id": "nftattootest.testnet",
#     "method_name": "nft_metadata",
#     "args_base64": "e30="
#   }
# }
# headersNEAR = {"Content-Type":"application/json"}

# data = requests.post(URL, json = obj, headers = headersNEAR) 
# print("data")
# print(data)
# print("text")
# print(data.text)
# print("request")
# print(data.request)
# print("content")
# print(data.content)
# print("headers")
# print(data.headers)
# print("url")
# print(data.url)
# data_to_json = data.json() #convertimos la respuesta en dict
# print(data_to_json)

# for element in data: #iteramos sobre data
#     print(element['name']) #Accedemos a sus valores

