from .models import AutoNum, CompanyInfo, FinYear
from django.utils.dateparse import parse_date
from django.http import HttpRequest

class tactUtils():
   
    
    defaultTranRows = 20
    tactCompCode = 'TACTB'
    tactCompName = 'TACTB'
    transactiontype= ['openbal','cashrcpt','cashpaym','acctjrnl']
    themestring = "bg-light text-black"
    
    companyMenu = [
        {"menukey":"compinfo","menudesc":"User Info"},
        {"menukey":"shareinfo","menudesc":"Shares Info"},
        
        
        ]
    transMenu = [
        {"menukey":"orderplace","menudesc":"Order Placement"},
        {"menukey":"ordertract","menudesc":"Order Tracking"},
        ]
    
    rptsMenu = [
        {"menukey":"tranenq","menudesc":"Transactions Dashboard"},
        {"menukey":"openbal","menudesc":"Order History"},
        ]

    orderOption = [
        {"inskey":"nifty","insdesc":"NIFTY","misnrml":"MIS"},
        {"inskey":"banknifty","insdesc":"BANKNIFTY","misnrml":"MIS"},
        {"inskey":"finnifty","insdesc":"FINNIFTY","misnrml":"MIS"},
        {"inskey":"midcapnifty","insdesc":"MIDCAP NIFTY","misnrml":"MIS"},
        {"inskey":"sensex","insdesc":"SENSEX","misnrml":"MIS"},
        {"inskey":"shares","insdesc":"SHARES","misnrml":"MIS"},
        {"inskey":"sharesoptions","insdesc":"SHARES OPTION","misnrml":"MIS"},
    ]
    def getDomain(req):
        httpstr = "http://"
        print(HttpRequest.is_secure(req))
        if HttpRequest.is_secure(req):
            httpstr = "http://"
        return httpstr + HttpRequest.get_host(req) + "/"

    def getCurrCompany():
        comprec = CompanyInfo.objects.filter(compCode=tactUtils.tactCompCode)[0]
        tactUtils.tactCompName = comprec.compName
        return comprec

    


    def getNextNumber(trantype):
        autoNumRec = AutoNum.objects.filter(tranType=trantype.upper())[0]
        return autoNumRec.prefix + str(autoNumRec.autonum)


    def updNextNumber(trantype):
        autoNumRec = AutoNum.objects.filter(tranType=trantype.upper())[0]
        autoNumRec.autonum = autoNumRec.autonum + 1
        autoNumRec.save()

    def getFinYearPeriod(datestr):
        trandate = parse_date(datestr)
        allfinyear = FinYear.objects.all().order_by("finYear")
        inyear = 0
        inperiod =0
        for eachyear in allfinyear:
            inyear = eachyear.finYear
            if eachyear.dateFrom1 <= trandate and eachyear.dateTo1 >= trandate :
                inperiod = 1
                break
            elif eachyear.dateFrom2 <= trandate and eachyear.dateTo2 >= trandate :
                inperiod = 2
                break
            elif eachyear.dateFrom3 <= trandate and eachyear.dateTo3 >= trandate :
                inperiod = 3
                break
            elif eachyear.dateFrom4 <= trandate and eachyear.dateTo4 >= trandate :
                inperiod = 4
                break
            elif eachyear.dateFrom5 <= trandate and eachyear.dateTo5 >= trandate :
                inperiod = 5
                break
            elif eachyear.dateFrom6 <= trandate and eachyear.dateTo6 >= trandate :
                inperiod = 6
                break
            elif eachyear.dateFrom7 <= trandate and eachyear.dateTo7 >= trandate :
                inperiod = 7
                break
            elif eachyear.dateFrom8 <= trandate and eachyear.dateTo8 >=trandate :
                inperiod = 8
                break
            elif eachyear.dateFrom9 <= trandate and eachyear.dateTo9 >= trandate :
                inperiod = 9
                break
            elif eachyear.dateFrom10 <= trandate and eachyear.dateTo10 >= trandate :
                inperiod = 10
                break
            elif eachyear.dateFrom11 <= trandate and eachyear.dateTo11 >= trandate :
                inperiod = 11
                break
            elif eachyear.dateFrom12 <= trandate and eachyear.dateTo12 >= trandate :
                inperiod = 12
                break
        return inyear, inperiod