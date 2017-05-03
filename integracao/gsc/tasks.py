# -*- coding: utf-8 -*-

from .models import Book
import requests
import ssl
import kajiki
import re

getList = [
    "ns0:idarquivo",
    "ns0:no_req",
    "ns0:no_wo",
    "ns0:datahorageracaoarquivo",
]


getResult = [
    "ns0:tipoarquivo",
    "ns0:processado",
    
]


def request(xml):
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    client = "https://sigscext.caixa.gov.br/arsys/services/ARService?server=arsapp-int.caixa&webService=GSC_RF010_FornecedorExterno_V401_WS"
    header = {"Accept-Encoding": "gzip,deflate","Content-Type": "text/xml;charset=UTF-8","SOAPAction": "urn:GSC_RF010_FornecedorExterno_V401_WS/GetList_Abertura","Content-Length": "626","Host": "sigscext.caixa.gov.br","Connection": "Keep-Alive","User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)"}
    return requests.post(client, data=xml, headers=header, verify=False).text


def get_list_abertura():
    
    xml = open('integracao/gsc/xml/GetList_Abertura.xml', 'r').read()
    call = request(xml)
    response = get_list_response(call, getList)
    return response



def create_item(item):
    
    return Book.objects.update_or_create(
        idarquivo=item['idarquivo'],
        req=item['no_req'],
        wo=item['no_wo'],
        datahorageracaoarquivo=item['datahorageracaoarquivo']
        )


def insert_in_database():
    for item in get_list_abertura():
        create_item(item)





def set_aceite_recusa(req, desc, status):
    query = Book.objects.get(req=req)
    xml = open('integracao/gsc/xml/SetAceiteRecusa.xml', 'r').read()
    Template = kajiki.XMLTemplate(xml.decode('latin1'))
    create_xml = Template(dict(idarquivo=query.idarquivo,datahorageracaoarquivo=query.datahorageracaoarquivo,wo=query.wo,tipo_retorno=status,chamado_fornecedor=query.id,desc=desc)).render()    
    call = request(create_xml)
    rest = get_list_response(call, getResult)
    response = rest[0]
    return response

def set_atualizacao(req, desc, status, dataagenda, contato):
    query = Book.objects.get(req=req)
    xml = open('integracao/gsc/xml/SetAtualizacao.xml', 'r').read()
    Template = kajiki.XMLTemplate(xml.decode('latin1'))
    create_xml = Template(dict(idarquivo=query.idarquivo,datahorageracaoarquivo=query.datahorageracaoarquivo,wo=query.wo,tipo_retorno=status,chamado_fornecedor=query.id,desc=desc,dataagenda=dataagenda,contato=contato)).render()    
    call = request(create_xml)
    rest = get_list_response(call, getResult)
    response = rest[0]
    return response


def get_list_response(xml, data):
    response = []
    soap = []

    for substr in data:
        c = 0
        occurences = [m.start() for m in re.finditer(substr, xml)]
        
        while(c < len(occurences)):

            p1 = occurences[c] - 1
            p2 = occurences[c + 1 ] - 2
            
            k = substr.split(":")[-1]
            v = xml[ p1 : p2 ].split("<{}>".format(substr))[-1]

            response.append({ k: v })
            c = c + 2

    c = 0   
    size = len( occurences )/2

    while ( c < size ):
        attr = {}

        for j in range(c, len(response), size) :
            attr.update(response[j])

        soap.append(attr)

        c = c + 1
    return soap

