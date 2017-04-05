#! C:\Users\galvaing\AppData\Local\Programs\Python\Python35-32

# CREATE A TRANSACTION

import xmlrpclib
import pdb
import pickle
from datetime import datetime, date, time
import StringIO
import urllib2
import requests
from odoo.exceptions import UserError
from openerp import api, fields, models, _
from pyPdf import PdfFileReader

class UniversignConnector(object):

    #Alexandre ID
    LOGIN = "alexandre.magnat@gleize-energie.fr"
    PASSWORD = "PRFCJkc!48"
    host = "https://" + LOGIN + ":" + PASSWORD + "@ws.universign.eu/sign/rpc/"

    #Greenloc ID
    LOGIN2 = "candidature.greenloc@green-loc.fr"
    PASSWORD2 = "4Zl4ka_3"
    host2 = "https://" + LOGIN2 + ":" + PASSWORD2 + "@ws.universign.eu/sign/rpc/"

    def request_sign(self,  **kwargs):
        print "Request L1======================="
        proxy = xmlrpclib.ServerProxy(self.host2)
        print "Proxy done======================="
        print proxy
        universign_docs = kwargs['universign_docs']
        universign_signers = kwargs['universign_signers']
        universign_name = kwargs['universign_name']
        try:
            transactionRequest = {} #input
            transactionRequest["handwrittenSignatureMode"] = 1
            transactionRequest["finalDocRequesterSent"] = False
            transactionRequest["finalDocObserverSent"] = False
            transactionRequest["finalDocSent"] = False
            transactionRequest["mustContactFirstSigner"] = True
            transactionRequest["description"] = universign_name
            transactionRequest["signers"] = universign_signers
            transactionRequest["documents"] = universign_docs
            for doc in transactionRequest["documents"]:
                # Convert content in transaction document as file
                with open("/opt/odoo/temp.pdf", "wb") as fh:
                    fh.write(doc['content'].decode('base64'))
                with open("/opt/odoo/temp.pdf", "rb") as f3:
                    doc["content"] = xmlrpclib.Binary(f3.read())
                    # doc["checkBoxTexts"] = ["Mon <a href='https://www.universign.eu/fr/documents/universign-pc_fr.pdf' target='_blank'>Signe</a>", "Mon Signe 2"]
                    signatureFields = []
                    pdf = PdfFileReader(open('/opt/odoo/temp.pdf','rb'))
                    pdf_page_total = pdf.getNumPages()
                    y = 650
                    for signer_idx in range(len(universign_signers)):
                        if signer_idx % 2 == 0:
                            y -= 55
                            signatureFields.append({'page': pdf_page_total, 'x': 80, 'y': y, 'signerIndex': signer_idx})
                        else:
                            signatureFields.append({'page': pdf_page_total, 'x': 300, 'y': y, 'signerIndex': signer_idx})
                    doc["signatureFields"] = signatureFields

            registrationRequest = {} #input
            print 'Let seeeeee++++++++++++++++++++++++++++++'
            print transactionRequest
            response = proxy.requester.requestTransaction(transactionRequest)
            print response

            id = response["id"]
            url = response["url"]
            print 'DONE========================='
            print id
            print url
            return {'id': id, 'url': url}
        except Exception as e:
            print("ERROR", e)

    def request_sign_l3(self,  **kwargs):
        #Greenloc ID
        LOGINCUSTOM = kwargs['universign_login']
        PASSWORDCUSTOM = kwargs['universign_password']
        hostCUSTOM = "https://" + LOGINCUSTOM + ":" + PASSWORDCUSTOM + "@sign.test.cryptolog.com/sign/rpc/"
        print "========================"
        print LOGINCUSTOM
        print PASSWORDCUSTOM
        print hostCUSTOM

        proxy = xmlrpclib.ServerProxy(hostCUSTOM)
        universign_docs = kwargs['universign_docs']
        universign_signers = kwargs['universign_signers']
        universign_name = kwargs['universign_name']
        try:
            transactionRequest = {} #input
            transactionRequest["handwrittenSignatureMode"] = 1
            transactionRequest["finalDocRequesterSent"] = False
            transactionRequest["finalDocObserverSent"] = False
            transactionRequest["finalDocSent"] = False
            transactionRequest["mustContactFirstSigner"] = False
            transactionRequest["description"] = universign_name
            transactionRequest["signers"] = universign_signers
            transactionRequest["documents"] = universign_docs
            for doc in transactionRequest["documents"]:
                # Convert content in transaction document as file
                with open("/opt/odoo/temp.pdf", "wb") as fh:
                    fh.write(doc['content'].decode('base64'))
                with open("/opt/odoo/temp.pdf", "rb") as f3:
                    doc["content"] = xmlrpclib.Binary(f3.read())
                    # doc["checkBoxTexts"] = ["Mon <a href='https://www.universign.eu/fr/documents/universign-pc_fr.pdf' target='_blank'>Signe</a>", "Mon Signe 2"]
                    signatureFields = []
                    pdf = PdfFileReader(open('/opt/odoo/temp.pdf','rb'))
                    pdf_page_total = pdf.getNumPages()
                    y = 650
                    for signer_idx in range(len(universign_signers)):
                        if signer_idx % 2 == 0:
                            y -= 55
                            signatureFields.append({'page': pdf_page_total, 'x': 80, 'y': y, 'signerIndex': signer_idx})
                        else:
                            signatureFields.append({'page': pdf_page_total, 'x': 300, 'y': y, 'signerIndex': signer_idx})
                    doc["signatureFields"] = signatureFields

            registrationRequest = {} #input
            print 'Transaction Request Value'
            print transactionRequest
            response = proxy.requester.requestTransaction(transactionRequest)

            id = response["id"]
            url = response["url"]
            return {'id': id, 'url': url}
        except Exception as e:
            print("ERROR", e)

    def request_get(self,  **kwargs):
        # ID Alexandre
        proxy = xmlrpclib.ServerProxy(self.host)
        print proxy
        print kwargs['universign_id']
        print kwargs['lead_id']
        print '++++++++++++++++++++'
        try:
            print proxy.requester.getTransactionInfo(kwargs['universign_id'])['status']
            if proxy.requester.getTransactionInfo(kwargs['universign_id'])['status'] == 'completed':
                res = proxy.requester.getDocuments(kwargs['universign_id'])
                attachment_datas = {}
                for doc in res:
                    with open("/opt/odoo/result.pdf", "wb") as f5:
                        f5.write(doc['content'].data)
                    attachment_datas[doc['name']] = False
                    with open("/opt/odoo/result.pdf", "rb") as f5:
                        attachment_datas[doc['name']] = f5.read().encode('base64')
                return attachment_datas
            elif proxy.requester.getTransactionInfo(kwargs['universign_id'])['status'] in ['expired', 'canceled', 'failed']:
                print 'MUST BE ERROR!'
                return proxy.requester.getTransactionInfo(kwargs['universign_id'])['status']
        except Exception as e:
            print("ERROR", e)

        # ID Greenloc
        proxy2 = xmlrpclib.ServerProxy(self.host2)
        print proxy2
        print kwargs['universign_id']
        print kwargs['lead_id']
        print '++++++++++++++++++++'
        try:
            print proxy2.requester.getTransactionInfo(kwargs['universign_id'])['status']
            if proxy2.requester.getTransactionInfo(kwargs['universign_id'])['status'] == 'completed':
                res = proxy2.requester.getDocuments(kwargs['universign_id'])
                attachment_datas = {}
                for doc in res:
                    with open("/opt/odoo/result.pdf", "wb") as f5:
                        f5.write(doc['content'].data)
                    attachment_datas[doc['name']] = False
                    with open("/opt/odoo/result.pdf", "rb") as f5:
                        attachment_datas[doc['name']] = f5.read().encode('base64')
                return attachment_datas
            elif proxy2.requester.getTransactionInfo(kwargs['universign_id'])['status'] in ['expired', 'canceled', 'failed']:
                print 'MUST BE ERROR!'
                return proxy2.requester.getTransactionInfo(kwargs['universign_id'])['status']
        except Exception as e:
            print("ERROR", e)

        # Technician VT
        print 'Is it correct?'
        print kwargs['technician']
        for technician_id in kwargs['technician']:

            #Technician ID
            LOGINCUSTOM = technician_id[0]
            PASSWORDCUSTOM = technician_id[1]
            hostCUSTOM = "https://" + LOGINCUSTOM + ":" + PASSWORDCUSTOM + "@sign.test.cryptolog.com/sign/rpc/"

            proxyCustom = xmlrpclib.ServerProxy(hostCUSTOM)
            print proxyCustom
            print LOGINCUSTOM
            print PASSWORDCUSTOM
            print '++++++++++++++++++++'
            try:
                print proxyCustom.requester.getTransactionInfo(kwargs['universign_id'])['status']
                if proxyCustom.requester.getTransactionInfo(kwargs['universign_id'])['status'] == 'completed':
                    res = proxyCustom.requester.getDocuments(kwargs['universign_id'])
                    attachment_datas = {}
                    for doc in res:
                        with open("/opt/odoo/result.pdf", "wb") as f5:
                            f5.write(doc['content'].data)
                        attachment_datas[doc['name']] = False
                        with open("/opt/odoo/result.pdf", "rb") as f5:
                            attachment_datas[doc['name']] = f5.read().encode('base64')
                    return attachment_datas
                elif proxyCustom.requester.getTransactionInfo(kwargs['universign_id'])['status'] in ['expired', 'canceled', 'failed']:
                    print 'MUST BE ERROR!'
                    return proxyCustom.requester.getTransactionInfo(kwargs['universign_id'])['status']
            except Exception as e:
                print("ERROR", e)
