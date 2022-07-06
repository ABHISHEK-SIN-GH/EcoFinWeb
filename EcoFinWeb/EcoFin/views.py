from urllib import response
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import date
import requests
import json
from urllib3 import HTTPResponse

def hrdoAPI(countries):
    url = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code='+countries+'/indicator_id=137506'
    responseIMF = requests.get(url).json()
    extData = []      
    jsonDataBRA = responseIMF["indicator_value"]["BRA"]["137506"]
    jsonDataCHN = responseIMF["indicator_value"]["CHN"]["137506"]
    jsonDataIND = responseIMF["indicator_value"]["IND"]["137506"]
    jsonDataMEX = responseIMF["indicator_value"]["MEX"]["137506"]
    jsonDataTUR = responseIMF["indicator_value"]["TUR"]["137506"]     
    jsonDataZAF = responseIMF["indicator_value"]["ZAF"]["137506"]
    extData.append(jsonDataBRA)
    extData.append(jsonDataCHN)
    extData.append(jsonDataIND)
    extData.append(jsonDataMEX)
    extData.append(jsonDataTUR)
    extData.append(jsonDataZAF)
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile) 
    return extData    

def imfAPI(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/'+database+'/' + \
        frequency+'.'+countries+'.'+indicators + \
        '?startPeriod='+startPeriod+'&endPeriod='+endPeriod
    responseIMF = requests.get(url).json()
    jsonData = responseIMF
    series = jsonData['CompactData']['DataSet']['Series']
    # if(database=="FAS" and indicators=="FCLODCG_GDP_PT"):
    #     with open('datax.json', 'w') as jsonfile:
    #         json.dump(series, jsonfile)
    extData = []
    for s in series:
        newSeries = []
        countryCode = s['@REF_AREA']
        indicatorCode = s['@INDICATOR']
        timeSeries = []
        for i in s['Obs']:
            try:
                timeSeries.append(dict({"time": i['@TIME_PERIOD'], "value": i['@OBS_VALUE']}))
            except KeyError:
                pass
        newSeries.append(dict({"countryCode": countryCode, "indicatorCode": indicatorCode, "timeSeries": timeSeries}))
        extData.append(newSeries)
    with open('data.json', 'w') as jsonfile:
            json.dump(series, jsonfile)
    return extData

def imfAPIone(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/'+database+'/' + \
        frequency+'.'+countries+'.'+indicators + \
        '?startPeriod='+startPeriod+'&endPeriod='+endPeriod
    responseIMF = requests.get(url).json()
    jsonData = responseIMF
    series = jsonData['CompactData']['DataSet']['Series']
    extData = []
    countryCode = series['@REF_AREA']
    indicatorCode = series['@INDICATOR']
    timeSeries = []
    for i in series['Obs']:
        try:
            timeSeries.append(dict({"time": i['@TIME_PERIOD'], "value": i['@OBS_VALUE']}))
        except KeyError:
            pass
    extData.append(dict({"countryCode": countryCode, "indicatorCode": indicatorCode, "timeSeries": timeSeries})) 
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile)       
    return extData    

def wbAPI(database, frequency, countries, indicators, startPeriod, endPeriod):
    url = "http://api.worldbank.org/"+database+"/country/"+countries+"/indicator/"+indicators + \
        "?format=json"+"&date="+startPeriod+":"+endPeriod + \
        "&frequency="+frequency+"&per_page=1000"
    responseWB = requests.get(url).json()
    extData = []
    for s in responseWB[1]:
        try:
            extData.append(dict({"countryCode": s["countryiso3code"], "indicatorCode": s["indicator"]["id"], "time": s["date"], "value": s["value"]}))
        except KeyError:
            pass    
    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData, jsonfile)
    return extData

def imfData(request):

    currentYear = date.today().year
    # print(currentYear)

    # extData15 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF;WLD","NY.GDP.MKTP.KD", str(currentYear-22), str(currentYear-2)) # OKK 
    # extData14 = hrdoAPI('BRA,IDN,IND,MEX,TUR,ZAF') # OKK
    # extData1 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF","NY.GDP.PCAP.PP.KD", str(currentYear-22), str(currentYear-2)) # OKK
    # extData8 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF","CM.MKT.LCAP.GD.ZS", str(currentYear-22), str(currentYear-2)) # OKK
    # extData7 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA','GGXCNL_G01_GDP_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData9 = imfAPI('FM', 'A', 'BR+ID+IN+MX+TR+ZA','G_XWDG_G01_GDP_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData6 = imfAPI('CPI', 'M', 'BR+ID+IN+MX+ZA','PCPI_PC_CP_A_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData16 = imfAPI('IFS', 'M', 'IN+GB+U2','ENDA_XDC_USD_RATE', str(currentYear-12), str(currentYear)) # ID+IN+TR+ZA // BR+MX
    # extData4 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF","NE.EXP.GNFS.ZS", str(currentYear-12), str(currentYear-2)) # OKK
    # extData11 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA','FCLODCG_GDP_PT', str(currentYear-12), str(currentYear-2)) # OKK
    # extData17 = wbAPI("v2", "A", "BRA;IDN;IND;MEX;TUR;ZAF","FS.AST.PRVT.GD.ZS", str(currentYear-17), str(currentYear-2)) # OKK
    # extData13 = imfAPI('FAS', 'A', 'BR+ID+IN+MX+TR+ZA','FCBODCA_NUM', str(currentYear-17), str(currentYear-2)) # OKK
    
    # extData2 = imfAPI('IFS', 'A', 'BR+IN+MX+TR','AIP_IX', str(currentYear-12), str(currentYear)) # BR+IN+MX+TR // ID+ZA
    # extData3 = imfAPI('APDREO', 'A', 'AU+CN+IN+ID+SG','NGDP_RPCH', str(currentYear-12), str(currentYear)) # AU+CN+IN+ID+SG
    # extData5 = imfAPIone('IFS', 'M', 'IN','ENDA_XDC_USD_RATE', str(currentYear-12), str(currentYear)) # OKK
    # extData12 = imfAPI('FAS', 'A', 'ID+IN+TR+ZA','FCMTA_NUM', str(currentYear-8), str(currentYear)) # ID+IN+TR+ZA // BR+MX

    # with open('data.json', 'w') as jsonfile:
    #     json.dump(extData11, jsonfile)
    # print(response)

    f = open('data1.json')
    extData1 = json.load(f)

    f = open('data2.json')
    extData2 = json.load(f)

    f = open('data3.json')
    extData3 = json.load(f)

    f = open('data4.json')
    extData4 = json.load(f)

    f = open('data5.json')
    extData5 = json.load(f)

    f = open('data6.json')
    extData6 = json.load(f)

    f = open('data7.json')
    extData7 = json.load(f)

    f = open('data8.json')
    extData8 = json.load(f)

    f = open('data9.json')
    extData9 = json.load(f)

    f = open('data11.json')
    extData11 = json.load(f)

    f = open('data12.json')
    extData12 = json.load(f)

    f = open('data13.json')
    extData13 = json.load(f)

    f = open('data14.json')
    extData14 = json.load(f)

    f = open('data15.json')
    extData15 = json.load(f)

    f = open('data16.json')
    extData16 = json.load(f)

    f = open('data17.json')
    extData17 = json.load(f)

    extDataJson1 = json.dumps(extData1)
    extDataObj1 = json.loads(extDataJson1)

    extDataJson2 = json.dumps(extData2)
    extDataObj2 = json.loads(extDataJson2)

    extDataJson3 = json.dumps(extData3)
    extDataObj3 = json.loads(extDataJson3)

    extDataJson4 = json.dumps(extData4)
    extDataObj4 = json.loads(extDataJson4)

    extDataJson5 = json.dumps(extData5)
    extDataObj5 = json.loads(extDataJson5)

    extDataJson6 = json.dumps(extData6)
    extDataObj6 = json.loads(extDataJson6)

    extDataJson7 = json.dumps(extData7)
    extDataObj7 = json.loads(extDataJson7)

    extDataJson8 = json.dumps(extData8)
    extDataObj8 = json.loads(extDataJson8)

    extDataJson9 = json.dumps(extData9)
    extDataObj9 = json.loads(extDataJson9)

    extDataJson11 = json.dumps(extData11)
    extDataObj11 = json.loads(extDataJson11)

    extDataJson12 = json.dumps(extData12)
    extDataObj12 = json.loads(extDataJson12)

    extDataJson13 = json.dumps(extData13)
    extDataObj13 = json.loads(extDataJson13)

    extDataJson14 = json.dumps(extData14)
    extDataObj14 = json.loads(extDataJson14)

    extDataJson15 = json.dumps(extData15)
    extDataObj15 = json.loads(extDataJson15)

    extDataJson16 = json.dumps(extData16)
    extDataObj16 = json.loads(extDataJson16)

    extDataJson17 = json.dumps(extData17)
    extDataObj17 = json.loads(extDataJson17)

    extResponse = {
        'extDataJson1': extDataJson1,
        'extDataObj1': extDataObj1,
        'extDataJson2': extDataJson2,
        'extDataObj2': extDataObj2,
        'extDataJson3': extDataJson3,
        'extDataObj3': extDataObj3,
        'extDataJson4': extDataJson4,
        'extDataObj4': extDataObj4,
        'extDataJson5': extDataJson5,
        'extDataObj5': extDataObj5,
        'extDataJson6': extDataJson6,
        'extDataObj6': extDataObj6,
        'extDataJson7': extDataJson7,
        'extDataObj7': extDataObj7,
        'extDataJson8': extDataJson8,
        'extDataObj8': extDataObj8,
        'extDataJson9': extDataJson9,
        'extDataObj9': extDataObj9,
        'extDataJson11': extDataJson11,
        'extDataObj11': extDataObj11,
        'extDataJson12': extDataJson12,
        'extDataObj12': extDataObj12,
        'extDataJson13': extDataJson13,
        'extDataObj13': extDataObj13,
        'extDataJson14': extDataJson14,
        'extDataObj14': extDataObj14,
        'extDataJson15': extDataJson15,
        'extDataObj15': extDataObj15,
        'extDataJson16': extDataJson16,
        'extDataObj16': extDataObj16,
        'extDataJson17': extDataJson17,
        'extDataObj17': extDataObj17,
    }

    response = json.dumps(extResponse)

    return JsonResponse(response, safe=False)

def home(request):
    recentUpdate = date.today().strftime("%B %Y")
    return render(request, 'EcoFin/imf.html', {"activeHome": "active","recentUpdate":recentUpdate})

def dashboard(request):

    country1 = "ind"
    country2 = "ind"
    country3 = "ind"
    country4 = "ind"
    country5 = "ind"
    country6 = "ind"
    country7 = "ind"
    country8 = "ind"
    country9 = "ind"
    country10 = "ind"
    country11 = "ind"
    country12 = "ind"
    country13 = "ind"

    indicator1 = "GDPG"
    indicator2 = "GDPC"
    indicator3 = "GDPCG"
    indicator4 = "PP"
    indicator5 = "PG"
    indicator6 = "UNER"
    indicator7 = "ISRP"
    indicator8 = "TR"
    indicator9 = "CAB"
    indicator10 = "EXP"
    indicator11 = "CPI"
    indicator12 = "GDPG"
    indicator13 = "GDPC"

    # WORLD BANK DATA

    GDPG = "NY.GDP.MKTP.KD.ZG"  # GDP growth (annual %)
    GDPC = "NY.GDP.PCAP.CD"  # GDP Per Capita (annual %)
    GDPCG = "NY.GDP.PCAP.KD.ZG"  # GDP Per Capita Growth Rate (annual %)
    PP = "SP.POP.TOTL"  # Population
    PG = "SP.POP.GROW"  # Population growth (annual %)
    UNER = "SL.UEM.TOTL.ZS"  # Unemployment Rate (annual %)
    ISRP = "FP.CPI.TOTL.ZG"  # Inflation Rate Consumer Prices
    TR = "FI.RES.TOTL.CD"  # Total Reserves
    CAB = "BN.CAB.XOKA.CD"  # Current Account Balance
    EXP = "GC.XPN.TOTL.GD.ZS"  # Expense
    CPI = "FP.CPI.TOTL"  # Consumer Price Index

    def indicatorFind(indicator):
        if(indicator == "GDPG"):
            indicator = GDPG
            return indicator
        elif(indicator == "GDPC"):
            indicator = GDPC
            return indicator
        elif(indicator == "GDPCG"):
            indicator = GDPCG
            return indicator
        elif(indicator == "PG"):
            indicator = PG
            return indicator
        elif(indicator == "PP"):
            indicator = PP
            return indicator
        elif(indicator == "UNER"):
            indicator = UNER
            return indicator
        elif(indicator == "ISRP"):
            indicator = ISRP
            return indicator
        elif(indicator == "TR"):
            indicator = TR
            return indicator
        elif(indicator == "CAB"):
            indicator = CAB
            return indicator
        elif(indicator == "EXP"):
            indicator = EXP
            return indicator
        elif(indicator == "CPI"):
            indicator = CPI
            return indicator
        else:
            return HttpResponse("404, Page not found !!!")

    indicator1 = indicatorFind(indicator1)
    indicator2 = indicatorFind(indicator2)
    indicator3 = indicatorFind(indicator3)
    indicator4 = indicatorFind(indicator4)
    indicator5 = indicatorFind(indicator5)
    indicator6 = indicatorFind(indicator6)
    indicator7 = indicatorFind(indicator7)
    indicator8 = indicatorFind(indicator8)
    indicator9 = indicatorFind(indicator9)
    indicator10 = indicatorFind(indicator10)
    indicator11 = indicatorFind(indicator11)
    indicator12 = indicatorFind(indicator12)
    indicator13 = indicatorFind(indicator13)

    url1 = "http://api.worldbank.org/v2/country/"+country1+"/indicator/" + \
        indicator1+"?format=json&per_page=200&mrv=10&frequency=Y"
    response1 = requests.get(url1).json()
    response1 = json.dumps(response1)
    responseObj1 = json.loads(response1)

    url2 = "http://api.worldbank.org/v2/country/"+country2+"/indicator/" + \
        indicator2+"?format=json&per_page=200&mrv=10&frequency=Y"
    response2 = requests.get(url2).json()
    response2 = json.dumps(response2)
    responseObj2 = json.loads(response2)

    url3 = "http://api.worldbank.org/v2/country/"+country3+"/indicator/" + \
        indicator3+"?format=json&per_page=200&mrv=10&frequency=Y"
    response3 = requests.get(url3).json()
    response3 = json.dumps(response3)
    responseObj3 = json.loads(response3)

    url4 = "http://api.worldbank.org/v2/country/"+country4+"/indicator/" + \
        indicator4+"?format=json&per_page=200&mrv=10&frequency=Y"
    response4 = requests.get(url4).json()
    response4 = json.dumps(response4)
    responseObj4 = json.loads(response4)

    url5 = "http://api.worldbank.org/v2/country/"+country5+"/indicator/" + \
        indicator5+"?format=json&per_page=200&mrv=10&frequency=Y"
    response5 = requests.get(url5).json()
    response5 = json.dumps(response5)
    responseObj5 = json.loads(response5)

    url6 = "http://api.worldbank.org/v2/country/"+country6+"/indicator/" + \
        indicator6+"?format=json&per_page=200&mrv=10&frequency=Y"
    response6 = requests.get(url6).json()
    response6 = json.dumps(response6)
    responseObj6 = json.loads(response6)

    url7 = "http://api.worldbank.org/v2/country/"+country7+"/indicator/" + \
        indicator7+"?format=json&per_page=200&mrv=10&frequency=Y"
    response7 = requests.get(url7).json()
    response7 = json.dumps(response7)
    responseObj7 = json.loads(response7)

    url8 = "http://api.worldbank.org/v2/country/"+country8+"/indicator/" + \
        indicator8+"?format=json&per_page=200&mrv=10&frequency=Y"
    response8 = requests.get(url8).json()
    response8 = json.dumps(response8)
    responseObj8 = json.loads(response8)

    url9 = "http://api.worldbank.org/v2/country/"+country9+"/indicator/" + \
        indicator9+"?format=json&per_page=200&mrv=10&frequency=Y"
    response9 = requests.get(url9).json()
    response9 = json.dumps(response9)
    responseObj9 = json.loads(response9)

    url10 = "http://api.worldbank.org/v2/country/"+country10+"/indicator/" + \
        indicator10+"?format=json&per_page=200&mrv=10&frequency=Y"
    response10 = requests.get(url10).json()
    response10 = json.dumps(response10)
    responseObj10 = json.loads(response10)

    url11 = "http://api.worldbank.org/v2/country/"+country11+"/indicator/" + \
        indicator11+"?format=json&per_page=200&mrv=10&frequency=Y"
    response11 = requests.get(url11).json()
    response11 = json.dumps(response11)
    responseObj11 = json.loads(response11)

    url12 = "http://api.worldbank.org/v2/country/"+country12+"/indicator/" + \
        indicator12+"?format=json&per_page=200&mrv=10&frequency=Y"
    response12 = requests.get(url12).json()
    response12 = json.dumps(response12)
    responseObj12 = json.loads(response12)

    url13 = "http://api.worldbank.org/v2/country/"+country13+"/indicator/" + \
        indicator13+"?format=json&per_page=200&mrv=10&frequency=Y"
    response13 = requests.get(url13).json()
    response13 = json.dumps(response13)
    responseObj13 = json.loads(response13)

    response = {
        "Title": "At a Glance: Indian Economy and Financial Markets",
        "Body": "",
        "response1": response1,
        "responseObj1": responseObj1,
        "response2": response2,
        "responseObj2": responseObj2,
        "response3": response3,
        "responseObj3": responseObj3,
        "response4": response4,
        "responseObj4": responseObj4,
        "response5": response5,
        "responseObj5": responseObj5,
        "response6": response6,
        "responseObj6": responseObj6,
        "response7": response7,
        "responseObj7": responseObj7,
        "response8": response8,
        "responseObj8": responseObj8,
        "response9": response9,
        "responseObj9": responseObj9,
        "response10": response10,
        "responseObj10": responseObj10,
        "response11": response11,
        "responseObj11": responseObj11,
        "response12": response12,
        "responseObj12": responseObj12,
        "response13": response13,
        "responseObj13": responseObj13,
    }

    return render(request, 'EcoFin/dashboard.html', {"res": response, "activeHome": "active"})

def errorPage(request):
    return render(request, 'EcoFin/errorPage.html', {})

def about(request):
    currentYear = date.today().year
    currentMonth = date.today().strftime("%h %Y")

    # extData15 = wbAPI("v2", "A", "BRA;CHN;IND;MEX;TUR;ZAF;WLD","NY.GDP.MKTP.KD", str(currentYear-22), str(currentYear-1)) # OKK 
    # extData14 = hrdoAPI('BRA,CHN,IND,MEX,TUR,ZAF') # OKK
    # extData1 = wbAPI("v2", "A", "BRA;CHN;IND;MEX;TUR;ZAF","NY.GDP.PCAP.PP.KD", str(currentYear-22), str(currentYear-1)) # OKK
    # extData8 = wbAPI("v2", "A", "BRA;CHN;IND;MEX;TUR;ZAF","CM.MKT.LCAP.GD.ZS", str(currentYear-22), str(currentYear-1)) # OKK
    # extData7 = imfAPI('FM', 'A', 'BR+CN+IN+MX+TR+ZA','GGXCNL_G01_GDP_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData9 = imfAPI('FM', 'A', 'BR+CN+IN+MX+TR+ZA','G_XWDG_G01_GDP_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData6 = imfAPI('CPI', 'M', 'BR+CN+IN+MX+ZA','PCPI_PC_CP_A_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData16 = imfAPI('IFS', 'M', 'IN+GB+U2','ENDA_XDC_USD_RATE', str(currentYear-12), str(currentYear)) # ID+IN+TR+ZA // BR+MX
    # extData4 = wbAPI("v2", "A", "BRA;CHN;IND;MEX;TUR;ZAF","NE.EXP.GNFS.ZS", str(currentYear-12), str(currentYear-1)) # OKK
    # extData11 = imfAPI('FAS', 'A', 'BR+CN+IN+MX+TR+ZA','FCLODCG_GDP_PT', str(currentYear-12), str(currentYear-1)) # OKK
    # extData17 = wbAPI("v2", "A", "BRA;CHN;IND;MEX;TUR;ZAF","FS.AST.PRVT.GD.ZS", str(currentYear-15), str(currentYear-1)) # OKK
    # extData13 = imfAPI('FAS', 'A', 'BR+CN+IN+MX+TR+ZA','FCBODCA_NUM', str(currentYear-15), str(currentYear-1)) # OKK
    
    # extData2 = imfAPI('IFS', 'A', 'BR+IN+MX+TR','AIP_IX', str(currentYear-12), str(currentYear)) # BR+IN+MX+TR // ID+ZA
    # extData3 = imfAPI('APDREO', 'A', 'AU+CN+IN+ID+SG','NGDP_RPCH', str(currentYear-12), str(currentYear)) # AU+CN+IN+ID+SG
    # extData5 = imfAPIone('IFS', 'M', 'IN','ENDA_XDC_USD_RATE', str(currentYear-12), str(currentYear)) # OKK
    # extData12 = imfAPI('FAS', 'A', 'ID+IN+TR+ZA','FCMTA_NUM', str(currentYear-8), str(currentYear)) # ID+IN+TR+ZA // BR+MX
    
    # with open('data1.json', 'w') as jsonfile:
    #     json.dump(extData1, jsonfile) 
    # with open('data4.json', 'w') as jsonfile:
    #     json.dump(extData4, jsonfile) 
    # with open('data6.json', 'w') as jsonfile:
    #     json.dump(extData6, jsonfile) 
    # with open('data7.json', 'w') as jsonfile:
    #     json.dump(extData7, jsonfile) 
    # with open('data8.json', 'w') as jsonfile:
    #     json.dump(extData8, jsonfile) 
    # with open('data9.json', 'w') as jsonfile:
    #     json.dump(extData9, jsonfile) 
    # with open('data11.json', 'w') as jsonfile:
    #     json.dump(extData11, jsonfile) 
    # with open('data13.json', 'w') as jsonfile:
    #     json.dump(extData13, jsonfile)
    # with open('data14.json', 'w') as jsonfile:
    #     json.dump(extData14, jsonfile)
    # with open('data15.json', 'w') as jsonfile:
    #     json.dump(extData15, jsonfile)   
    # with open('data16.json', 'w') as jsonfile:
    #     json.dump(extData16, jsonfile)  
    # with open('data17.json', 'w') as jsonfile:
    #     json.dump(extData17, jsonfile) 

    # with open('data2.json', 'w') as jsonfile:
    #     json.dump(extData2, jsonfile) 
    # with open('data3.json', 'w') as jsonfile:
    #     json.dump(extData3, jsonfile)
    # with open('data5.json', 'w') as jsonfile:
    #     json.dump(extData5, jsonfile) 
    # with open('data12.json', 'w') as jsonfile:
    #     json.dump(extData12, jsonfile) 

    response = {
        "Title": "About Us",
        "Body": "About Us",
    }

    return render(request, 'EcoFin/about.html', {"res": response, "activeAbout": "active"})

def contact(request):
    response = {
        "Title": "Contact Us",
        "Body": "Contact Us",
    }
    return render(request, 'EcoFin/contact.html', {"res": response, "activeContact": "active"})

def gdp(request):
    response = {
        "Title": "Gross Domestic Product (GDP)",
        "Body": "Gross Domestic Product (GDP)",
    }
    return render(request, 'EcoFin/gdp.html', {"res": response})

def inflation(request):
    response = {
        "Title": "Inflation",
        "Body": "Infilation",
    }
    return render(request, 'EcoFin/inflation.html', {"res": response})

def businessPerformance(request):
    response = {
        "Title": "Business Performance",
        "Body": "Business Performance",
    }
    return render(request, 'EcoFin/businessPerformance.html', {"res": response})

def tradeForex(request):
    response = {
        "Title": "Trade and Forex",
        "Body": "Trade and Forex",
    }
    return render(request, 'EcoFin/tradeForex.html', {"res": response})

def unemployment(request):
    response = {
        "Title": "Unemployment",
        "Body": "Unemployment",
    }
    return render(request, 'EcoFin/unemployment.html', {"res": response})

def fiscalSituation(request):
    response = {
        "Title": "Fiscal Situation",
        "Body": "Fiscal Situation",
    }
    return render(request, 'EcoFin/fiscalSituation.html', {"res": response})

def interestRatesBond(request):
    response = {
        "Title": "Interest Rates & Bond",
        "Body": "Interest Rates & Bond",
    }
    return render(request, 'EcoFin/interestRatesBond.html', {"res": response})

def equityMarkets(request):
    response = {
        "Title": "Equity Markets",
        "Body": "Equity Markets",
    }
    return render(request, 'EcoFin/equityMarkets.html', {"res": response})

def commodityMarkets(request):
    response = {
        "Title": "Ccommodity Markets",
        "Body": "Commodity Markets",
    }
    return render(request, 'EcoFin/commodityMarkets.html', {"res": response})

def foreignInvestment(request):
    response = {
        "Title": "Foreign Investment",
        "Body": "Foreign Investment",
    }
    return render(request, 'EcoFin/foreignInvestment.html', {"res": response})

def moneyCredit(request):
    response = {
        "Title": "Money & Credit",
        "Body": "Money & Credit",
    }
    return render(request, 'EcoFin/moneyCredit.html', {"res": response})

def realEstate(request):
    response = {
        "Title": "Real Estate",
        "Body": "Real Estate",
    }
    return render(request, 'EcoFin/realEstate.html', {"res": response})

def ventureCapitalIPO(request):
    response = {
        "Title": "Venture Capital & IPOs",
        "Body": "Venture Capital & IPOs",
    }
    return render(request, 'EcoFin/ventureCapitalIPO.html', {"res": response})
