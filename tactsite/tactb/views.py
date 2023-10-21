from datetime import datetime
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render,redirect
from .models import CompanyCOA, CompanyInfo, FinYear, PartyInfo, AutoNum,DefaultAct,GLHeader,GLDetail,GLSummary,Subscribers
from .utilities import tactUtils
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import transaction
from django.utils.dateparse import parse_date
import uuid
from django.db.models import Q,F




# Create your views here.


def index(request):
    ormmodelHdrAll = GLHeader.objects.all().order_by("-date_trans","document_no")[:25]
    cntxt = {'tactUtils':tactUtils, "recentTran":ormmodelHdrAll}
    tactUtils.getCurrCompany()
    return render(request,'tactb/index.html',cntxt)

def ajaxcalls(request):
    rendtype = request.GET['rendtyp']
    errmsg = "Error Occured While Deleting"
    id = request.GET['id']
    action = request.GET["action"]
    if (rendtype == "openbal" or rendtype == "cashrcpt" or rendtype == "cashpaym" or rendtype == "acctjrnl"):
        if action == "delete":
            try:
                with transaction.atomic():		
                    glsum = GLSummary.objects.filter(uid=id)
                    glhdr = GLHeader.objects.filter(uid=id)
                    gldtl = GLDetail.objects.filter(uid=id)
                    glsum.delete()
                    glhdr.delete()
                    gldtl.delete()
            except:
                return JsonResponse({"status":errmsg,}, status=200)
            return JsonResponse({"status":'true',}, status=200)
    elif (rendtype == "finyears" or rendtype == "compcoa" or rendtype == "autonum" or rendtype == "defaultact" or rendtype == "custmaint" or rendtype == "subscription" ):
        if action == "delete":
            recordtodelete = None
            candelete = True
            if rendtype == "finyears":
                glsum = GLSummary.objects.filter(act_year=id)
                if len(glsum) != 0:
                    candelete = False
                else:
                    recordtodelete = FinYear.objects.filter(finYear=id)
            elif rendtype == "compcoa":
                defact = DefaultAct.objects.filter(accountCode=id)
                glhdr = GLHeader.objects.filter(act_code=id)
                gldtl = GLDetail.objects.filter(account_code=id)
                if len(defact) != 0 or len(glhdr) != 0 or len(gldtl) != 0:
                    candelete = False
                else:
                    recordtodelete = CompanyCOA.objects.filter(accountCode=id)
            elif rendtype == "defaultact":
                glhdr = GLHeader.objects.filter(document_type=id)
                #print("GLHeader",glhdr)
                if  len(glhdr) != 0:
                    candelete = False
                else:
                    recordtodelete = DefaultAct.objects.filter(tranType=id)
            elif rendtype == "autonum":
                glhdr = GLHeader.objects.filter(document_type=id)
                #print("GLHeader",glhdr)
                if  len(glhdr) != 0:
                    candelete = False
                else:
                    recordtodelete = AutoNum.objects.filter(tranType=id)
            elif rendtype == "custmaint":
                glhdr = GLHeader.objects.filter(party_code=id)
                #("GLHeader",glhdr)
                if  len(glhdr) != 0:
                    candelete = False
                else:
                    recordtodelete = PartyInfo.objects.filter(partyCode=id)
            elif rendtype == "subscription":
                recordtodelete = Subscribers.objects.filter(subsId=id)
                print("recordtodelete",recordtodelete,"id",id)    

            if candelete:
                try:
                    with transaction.atomic():		
                        recordtodelete.delete()
                        print("Deleted")
                except:
                    return JsonResponse({"status":errmsg,}, status=200)
                return JsonResponse({"status":"true",}, status=200)
            else:
                 return JsonResponse({"status":"Code In Use. Unable To Delete",}, status=200)
    
    

def compinfoHandler(request,rendertype,id=None):
    ormmodel = CompanyInfo.objects.filter(compCode=tactUtils.tactCompCode)
    ormmodelall = ormmodel
    if len(ormmodel) == 0:
        compfinfo = CompanyInfo(compCode=tactUtils.tactCompCode,compName=tactUtils.tactCompCode,compAddress1='India',compAddress2='India',compCity='India',compState='India',compCountry='India',compTelephone='India',compFax='India',compEmail='India',compLogo='India',compCurrency='INR')
        compfinfo.save()
        ormmodel = tactUtils.getCurrCompany()
    ormmodel = ormmodel[0]
    if request.method == "POST":
        ormmodel.compCode = request.POST.get("code")
        ormmodel.compName = request.POST.get("name")
        ormmodel.compAddress1 = request.POST.get("address1")
        ormmodel.compAddress2 = request.POST.get("address2")
        ormmodel.compCity = request.POST.get("city")
        ormmodel.compState = request.POST.get("state")
        ormmodel.compCountry = request.POST.get("country")
        ormmodel.compZipcode = request.POST.get("zipcode")
        ormmodel.compTelephone = request.POST.get("telephone")
        ormmodel.compFax = request.POST.get("fax")
        ormmodel.compEmail = request.POST.get("email")
        if len(request.FILES)  != 0:
            ormmodel.compLogo = request.FILES["logo"]
        ormmodel.compCurrency= request.POST.get("currency")
        ormmodel.save()
    tactUtils.getCurrCompany()
    return {'ormmodel':ormmodel,'rendertype':rendertype,'ormmodelall':ormmodelall,'tactUtils':tactUtils}

def compcoaHandler(request,rendertype,id=None):
    ormmodel ={}
    if id != None:
        ormmodel = CompanyCOA.objects.filter(id=id)[0]
    ormmodelall = CompanyCOA.objects.all().order_by("accountCode")
    if request.method == "POST":
        accountCode = request.POST.get('accountCode')
        accountName = request.POST.get('accountName')
        accountType = request.POST.get('accountType')
        ormcompany = tactUtils.getCurrCompany()
        ormmodel = CompanyCOA.objects.filter(accountCode=accountCode)
        if len(ormmodel) == 0:
            ormmodel = CompanyCOA(compCode=ormcompany, accountCode=accountCode,accountName=accountName,accountType=accountType)
        else:
            ormmodel = ormmodel[0]
            ormmodel.accountCode = accountCode
            ormmodel.accountName = accountName
            ormmodel.accountType = accountType
        ormmodel.save()
    return {'ormmodel':ormmodel,'rendertype':rendertype,"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils}

def custmaintHandler(request,rendertype,id=None):
    ormmodel ={}
    if id != None:
        ormmodel = PartyInfo.objects.filter(id=id)[0]
    ormmodelall = PartyInfo.objects.all().order_by("partyCode")
    if request.method == "POST":
        partyCode = request.POST.get('partyCode')
        partyName = request.POST.get('partyName')
        partyName2 = request.POST.get('partyName2')
        partyAddress1 = request.POST.get('partyAddress1')
        partyAddress2 = request.POST.get('partyAddress2')
        partyCity= request.POST.get('partyCity')
        partyState= request.POST.get('partyState')
        partyCountry= request.POST.get('partyCountry')
        partyZipcode= request.POST.get('partyZipcode')
        partyTelephone= request.POST.get('partyTelephone')
        partyFax= request.POST.get('partyFax')
        partyEmail= request.POST.get('partyEmail')
        ormcompany = tactUtils.getCurrCompany()
        ormmodel = PartyInfo.objects.filter(partyCode=partyCode)
        if len(ormmodel) == 0:
            ormmodel = PartyInfo(compCode=ormcompany,partyCode=partyCode,partyName=partyName,partyName2=partyName2,partyAddress1=partyAddress1,partyAddress2=partyAddress2,partyCity=partyCity,partyState=partyState,partyCountry=partyCountry, partyZipcode=partyZipcode,partyTelephone=partyTelephone,partyFax=partyFax,partyEmail=partyEmail)
        else:
            ormmodel = ormmodel[0]
            ormmodel.partyCode = partyCode
            ormmodel.partyName = partyName
            ormmodel.partyName2 = partyName2
            ormmodel.partyAddress1 = partyAddress1
            ormmodel.partyAddress2 = partyAddress2
            ormmodel.partyCity = partyCity
            ormmodel.partyState = partyState
            ormmodel.partyCountry = partyCountry
            ormmodel.partyZipcode = partyZipcode
            ormmodel.partyTelephone = partyTelephone
            ormmodel.partyFax = partyFax
            ormmodel.partyEmail = partyEmail
        ormmodel.save()
    return {'ormmodel':ormmodel,'rendertype':rendertype,"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils}

def subscriptionHandler(request,rendertype,id=None):
    ormmodel ={}
    if id != None:
        ormmodel = Subscribers.objects.filter(id=id)[0]
    ormmodelall = Subscribers.objects.all().order_by("subsId")
    if request.method == "POST":
        subsId = request.POST.get('subsId')
        print("Subid:",subsId)
        subsName = request.POST.get('subsName')
        subDOB = request.POST.get('subDOB')
        subDOR = request.POST.get('subDOR')
        subPPOno = request.POST.get('subPPOno')
        subBranch= request.POST.get('subBranch')
        subAddr1= request.POST.get('subAddr1')
        subAddr2= request.POST.get('subAddr2')
        ormcompany = tactUtils.getCurrCompany()
        ormmodel = Subscribers.objects.filter(subsId=subsId)
        if len(ormmodel) == 0:
            ormmodel = Subscribers(compCode=ormcompany,subsId=subsId,subsName=subsName,subDOB=subDOB,subDOR=subDOR,subPPOno=subPPOno,subBranch=subBranch,subAddr1=subAddr1,subAddr2=subAddr2)
        else:
            ormmodel = ormmodel[0]
            ormmodel.subsId = subsId
            ormmodel.subsName = subsName
            ormmodel.subDOB = subDOB
            ormmodel.subDOR = subDOR
            ormmodel.subPPONo = subPPOno
            ormmodel.subBranch = subBranch
            ormmodel.subAddr1 = subAddr1
            ormmodel.subAddr2 = subAddr2
        ormmodel.save()
    return {'ormmodel':ormmodel,'rendertype':rendertype,"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils}


def finyearsHandler(request,rendertype,id):
    ormmodel ={}
    if id != None:
        ormmodel = FinYear.objects.filter(id=id)[0]
    ormmodelall = FinYear.objects.all().order_by("finYear")
    if request.method == "POST":
        finYear = request.POST.get('finyear')
        dateFrom1 = request.POST.get('dateFrom1')
        dateTo1 = request.POST.get('dateTo1')
        dateFrom2 = request.POST.get('dateFrom2')
        dateTo2 = request.POST.get('dateTo2')
        dateFrom3 = request.POST.get('dateFrom3')
        dateTo3 = request.POST.get('dateTo3')
        dateFrom4 = request.POST.get('dateFrom4')
        dateTo4 = request.POST.get('dateTo4')
        dateFrom5 = request.POST.get('dateFrom5')
        dateTo5 = request.POST.get('dateTo5')
        dateFrom6 = request.POST.get('dateFrom6')
        dateTo6 = request.POST.get('dateTo6')
        dateFrom7 = request.POST.get('dateFrom7')
        dateTo7 = request.POST.get('dateTo7')
        dateFrom8 = request.POST.get('dateFrom8')
        dateTo8 = request.POST.get('dateTo8')
        dateFrom9 = request.POST.get('dateFrom9')
        dateTo9 = request.POST.get('dateTo9')
        dateFrom10 = request.POST.get('dateFrom10')
        dateTo10 = request.POST.get('dateTo10')
        dateFrom11 = request.POST.get('dateFrom11')
        dateTo11 = request.POST.get('dateTo11')
        dateFrom12 = request.POST.get('dateFrom12')
        dateTo12 = request.POST.get('dateTo12')

        ormcompany = tactUtils.getCurrCompany()
        ormmodel = FinYear.objects.filter(finYear=finYear)
        if len(ormmodel) == 0:
            ormmodel = FinYear(compCode=ormcompany, finYear=finYear,dateFrom1=dateFrom1,dateTo1=dateTo1,dateFrom2=dateFrom2,dateTo2=dateTo2,dateFrom3=dateFrom3,dateTo3=dateTo3,dateFrom4=dateFrom4,dateTo4=dateTo4,dateFrom5=dateFrom5,dateTo5=dateTo5,dateFrom6=dateFrom6,dateTo6=dateTo6,dateFrom7=dateFrom7,dateTo7=dateTo7,dateFrom8=dateFrom8,dateTo8=dateTo8,dateFrom9=dateFrom9,dateTo9=dateTo9,dateFrom10=dateFrom10,dateTo10=dateTo10,dateFrom11=dateFrom11,dateTo11=dateTo11,dateFrom12=dateFrom12,dateTo12=dateTo12)
        else:
            ormmodel = ormmodel[0]
            ormmodel.finYear = finYear
            ormmodel.dateFrom1 = dateFrom1
            ormmodel.dateTo1 = dateTo1
            ormmodel.dateFrom2 = dateFrom2
            ormmodel.dateTo2 = dateTo2
            ormmodel.dateFrom3 = dateFrom3
            ormmodel.dateTo3 = dateTo3
            ormmodel.dateFrom4 = dateFrom4
            ormmodel.dateTo4 = dateTo4
            ormmodel.dateFrom5 = dateFrom5
            ormmodel.dateTo5 = dateTo5
            ormmodel.dateFrom6 = dateFrom6
            ormmodel.dateTo6 = dateTo6
            ormmodel.dateFrom7 = dateFrom7
            ormmodel.dateTo7 = dateTo7
            ormmodel.dateFrom8 = dateFrom8
            ormmodel.dateTo8 = dateTo8
            ormmodel.dateFrom9 = dateFrom9
            ormmodel.dateTo9 = dateTo9
            ormmodel.dateFrom10 = dateFrom10
            ormmodel.dateTo10 = dateTo10
            ormmodel.dateFrom11 = dateFrom11
            ormmodel.dateTo11 = dateTo11
            ormmodel.dateFrom12 = dateFrom12
            ormmodel.dateTo12 = dateTo12
        ormmodel.save()
    return {'ormmodel':ormmodel,'rendertype':rendertype,'noofyears':range(1,13),"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils}

def modaccesHandler(request,rendertype,id):
    return {'rendertype':rendertype,'tactUtils':tactUtils}

def reguserHandler(request,rendertype,id):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f'User {username} is created')
            return {'rendertype':rendertype,'redirect':"index"}
    else:
        form = UserCreationForm()
    return {'rendertype':rendertype,'form':form}

def autonumHandler(request,rendertype,id=None):
    ormmodel ={}
    if id != None:
        ormmodel = AutoNum.objects.filter(id=id)[0]
    ormmodelall = AutoNum.objects.all().order_by("tranType")
    if request.method == "POST":
        tranType = request.POST.get('tranType')
        prefix = request.POST.get('prefix')
        autonum = request.POST.get('autonum')
        ormcompany = tactUtils.getCurrCompany()
        ormmodel = AutoNum.objects.filter(tranType=tranType)
        if len(ormmodel) == 0:
            ormmodel = AutoNum(compCode=ormcompany, tranType=tranType,prefix=prefix,autonum=autonum)
        else:
            ormmodel = ormmodel[0]
            ormmodel.tranType = tranType
            ormmodel.prefix = prefix
            ormmodel.autonum = autonum
        ormmodel.save()
    #print(ormmodel)
    return {'ormmodel':ormmodel,'rendertype':rendertype,"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils}

def defaultactHandler(request,rendertype,id=None):
    ormcoa = CompanyCOA.objects.all().order_by("accountCode")
    ormmodel ={}
    if id != None:
        ormmodel = DefaultAct.objects.filter(id=id)[0]
    ormmodelall = DefaultAct.objects.all().order_by("tranType")
    if request.method == "POST":
        tranType = request.POST.get('tranType')
        accountCode = request.POST.get('accountCode')
        ormcompany = tactUtils.getCurrCompany()
        ormmodel = DefaultAct.objects.filter(tranType=tranType)
        if len(ormmodel) == 0:
            ormmodel = DefaultAct(compCode=ormcompany, tranType=tranType, accountCode=accountCode)
        else:
            ormmodel = ormmodel[0]
            ormmodel.tranType = tranType
            ormmodel.accountCode = accountCode
        ormmodel.save()
    return {'ormmodel':ormmodel,'rendertype':rendertype,"noofrecords":len(ormmodelall),'ormmodelall':ormmodelall,'tactUtils':tactUtils,"ormcoa":ormcoa}

def mapModel(request,rendertype,id=None):
    ormmodel = {}
    ormmodelall = {}
    if rendertype == "compinfo":
        return compinfoHandler(request,rendertype,id)
    elif rendertype == "finyears":
        return finyearsHandler(request,rendertype,id)
    elif rendertype == "modacces":
        return modaccesHandler(request,rendertype,id)
    elif rendertype == "reguser":
        return reguserHandler(request,rendertype,id)
    elif rendertype == "compcoa":
        return compcoaHandler(request,rendertype,id)
    elif rendertype == "custmaint":
        return custmaintHandler(request,rendertype,id)
    elif rendertype == "subscription":
        return subscriptionHandler(request,rendertype,id)
    elif rendertype == "autonum":
        return autonumHandler(request,rendertype,id)
    elif rendertype == "defaultact":
        return defaultactHandler(request,rendertype,id)
    
def master(request,rendertype):
    cntxt= mapModel(request,rendertype)
    if cntxt != None and "redirect" in cntxt.keys():
        return redirect(tactUtils.getDomain(request))
    else:
        return render(request,'tactb/master.html',cntxt)



        
    

def masterrec(request,rendertype,id):
    cntxt= mapModel(request,rendertype,id)
    return render(request,'tactb/master.html',cntxt)


def InsertGLSummary(hdr,dtlall):
    glsummary = GLSummary.objects.filter(uid=hdr.uid)
   
    if len(glsummary) != 0:
        glsummary.delete()
    glsummary = GLSummary() #Header details
    glsummary.compCode        = hdr.compCode
    glsummary.uid             = hdr.uid
    glsummary.reference_no    = hdr.document_no
    glsummary.reference_uid   = hdr.uid
    yr,pr = tactUtils.getFinYearPeriod(hdr.date_trans)
    glsummary.act_year        = yr
    glsummary.act_period      = pr
    glsummary.document_type   = hdr.document_type
    glsummary.document_no     = hdr.document_no
    glsummary.document_date   = hdr.date_trans
    glsummary.serial_no       = 0
    glsummary.act_code        = hdr.act_code
    glsummary.curr_code       = hdr.currency_code
    glsummary.sign            = hdr.trx_sign
    if hdr.document_type == "CASHPAYM":
         glsummary.sign         = -1
    if hdr.document_type == "CASHRCPT":
         glsummary.sign         = 1
    glsummary.amount_local    = hdr.amount_local
    glsummary.amount_forex    = hdr.amount_forex
    glsummary.entered_by      = hdr.usercode
    glsummary.party_code      = hdr.party_code
    glsummary.party_name      = hdr.party_name
    glsummary.item_code       = 'NOTSET'
    glsummary.item_description= 'NOTSET'
    glsummary.remarks         = hdr.remarks
    glsummary.trans_mode      = hdr.document_status
    glsummary.offset_act      = hdr.act_code
    glsummary.location_code   = 'NOTSET'
    glsummary.save()
    rowcnt = 0
    for dtl in dtlall:
        rowcnt = rowcnt +1
        glsummary = GLSummary() #Header details
        glsummary.compCode        = hdr.compCode
        glsummary.uid             = hdr.uid
        glsummary.reference_no    = hdr.document_no
        glsummary.reference_uid   = dtl.line_uid
        glsummary.act_year        = yr
        glsummary.act_period      = pr
        glsummary.document_type   = hdr.document_type
        glsummary.document_no     = hdr.document_no
        glsummary.document_date   = hdr.date_trans
        glsummary.serial_no       = rowcnt
        glsummary.act_code        = dtl.account_code
        glsummary.curr_code       = hdr.currency_code
        glsummary.sign            = dtl.trx_sign
        if hdr.document_type == "CASHPAYM":
            glsummary.sign         = 1
        if hdr.document_type == "CASHRCPT":
            glsummary.sign         = -1
        glsummary.amount_local    = dtl.amount_local
        glsummary.amount_forex    = dtl.amount_forex
        glsummary.entered_by      = hdr.usercode
        glsummary.party_code      = hdr.party_code
        glsummary.party_name      = hdr.party_name
        glsummary.item_code       = 'NOTSET'
        glsummary.item_description= 'NOTSET'
        glsummary.remarks         = dtl.remarks
        glsummary.trans_mode      = hdr.document_status
        glsummary.offset_act      = dtl.account_code
        glsummary.location_code   = 'NOTSET'
        glsummary.save()

def mapTrnModel(request,rendertype,uid=None,traction=None):
    #print("traction",traction)
    if rendertype == 'openbal':
        transDesc = 'Opening Balance'
    elif rendertype == 'cashrcpt':
        transDesc = 'Cash Receipts'
    elif rendertype == 'cashpaym':
         transDesc = 'Cash Payments'
    elif rendertype == 'acctjrnl':
          transDesc ='General Journal'
    if rendertype == 'cashrcpt':
        hdrAccountLabel = 'To / Receiving Account'
    else:
        hdrAccountLabel = 'From / Expense Account'
    ormmodelHdr ={}
    ormmodelDtl ={}
   
    ormmodelHdrAll = GLHeader.objects.filter(document_type=rendertype.upper()).order_by("-date_trans","document_no")[:500]
    currcomp = tactUtils.getCurrCompany()
    currUserCode = request.user.username
    transmode = 'new'
    transrows = 0
    if uid != None:
        ormmodelHdr = GLHeader.objects.filter(uid=uid)
        if len(ormmodelHdr)!=0:
            ormmodelHdr = ormmodelHdr[0]
            transmode = "edit"
        ormmodelDtl = GLDetail.objects.filter(uid=uid)
        transrows = len(ormmodelDtl)
       
    if request.method == "POST":
        postdict = request.POST
        compCode            = currcomp
        trxuid              = postdict['uuid']
        document_type       = postdict['document_type']
        document_no         = postdict['document_no']
        date_trans          = postdict['date_trans']
        document_reference  = postdict['document_reference']
        additional_reference= postdict['additional_reference']
        remarks             = postdict['remarks']
        document_status     = 'draft'
        party_code          = postdict['party_code']
        party_name          = postdict['party_code']
        currency_code       = postdict['currency_code']
        if rendertype == 'cashrcpt' or  rendertype == 'cashpaym': 
            amount_local        = postdict['amount_local']
            amount_forex        = postdict['amount_forex']
            act_code            = postdict['hdrAccount']
        else:
            amount_local        = 0
            amount_forex        = 0
            act_code            = 'NOTSET'
        ex_rate             = postdict['ex_rate']
        tax_amount1         = 0
        tax_amount2         = 0
        tax_amount3         = 0
        nontax_amount1      = 0
        nontax_amount2      = 0
        nontax_amount3      = 0
        valid_till          = postdict['date_trans']#handle valid date
        term_code           = ''
        term_days           = 0
        trx_sign            = 1
        if rendertype == 'cashrcpt':
            trx_sign            = -1
        
        
        line_uid        = []
        line_number     = []
        item_code       = []
        item_description= []
        quantity        = []
        bal_quantity    = []
        unit_price      = []
        stock_uom       = []
        selling_uom     = []
        r_amount_forex    = []
        r_amount_local    = []
        taxable_yn      = []
        tax_code1       = []
        tax_code2       = []
        tax_code3       = []
        tax_pecent1     = []
        tax_pecent2     = []
        tax_pecent3     = []
        discount_percent= []
        location_code   = []
        account_code    = []
        db_cr           = []
        r_trx_sign        = []
        ref_document_typ= []
        ref_document_no = []
        tag_header_yn   = []        
        tax_amount_forex1=[]
        tax_amount_forex2=[]
        tax_amount_forex3=[]
        tax_amount_local1=[]
        tax_amount_local2=[]
        tax_amount_local3=[]
        extnamount_forex=[]
        extnamount_local=[]
        r_remarks         = []
        ormmodelDtlAll = []
        for i in range(1,int(postdict.get('noofrows'))+1):
            currrow = str(i)
            chkkey = "trandelchk_"+currrow
            insrec = True;
            if rendertype == 'cashrcpt' or  rendertype == 'cashpaym': 
                if rendertype == 'cashrcpt':
                    r_trxsign = 1
                else:
                    r_trxsign = -1
                rowamt = postdict['amount_forex_'+currrow]
            else:
                cramt = postdict['tranLineCreditAmount_'+currrow]
                dramt = postdict['tranLineDebitAmount_'+currrow]
                if float(cramt) != 0 :
                    r_trxsign = -1
                    rowamt = cramt
                else:
                    r_trxsign = 1
                    rowamt = dramt
            if chkkey in postdict.keys() or postdict['actNumber_'+currrow] == "" or rowamt == 0:
                insrec = False
            if insrec:
                line_uid.append(postdict['line_uid_'+currrow])
                line_number.append(i)
                item_code.append(postdict['item_code_'+currrow])
                item_description.append(postdict['item_description_'+currrow])
                quantity.append(postdict['quantity_'+currrow])
                bal_quantity.append(postdict['bal_quantity_'+currrow])
                unit_price.append(postdict['unit_price_'+currrow])
                stock_uom.append(postdict['stock_uom_'+currrow])
                selling_uom.append(postdict['selling_uom_'+currrow])
            
                taxable_yn.append (postdict['taxable_yn_'+currrow])
                tax_code1.append(postdict['tax_code1_'+currrow])
                tax_code2.append(postdict['tax_code2_'+currrow])
                tax_code3.append(postdict['tax_code3_'+currrow])
                tax_pecent1.append(postdict['tax_pecent1_'+currrow])
                tax_pecent2.append(postdict['tax_pecent2_'+currrow])
                tax_pecent3.append (postdict['tax_pecent3_'+currrow])
                discount_percent.append(postdict['discount_percent_'+currrow])
                location_code.append(postdict['location_code_'+currrow])
                account_code.append(postdict['actNumber_'+currrow])
                db_cr.append(postdict['db_cr_'+currrow])
                
                r_trx_sign.append(r_trxsign)
                ref_document_typ.append(postdict['ref_document_typ_'+currrow])
                ref_document_no.append(postdict['ref_document_no_'+currrow])
                tag_header_yn.append(postdict['tag_header_yn_'+currrow])
                r_amount_forex.append(rowamt)
                r_amount_local.append(rowamt)
                    
                tax_amount_forex1.append(postdict['tax_amount_forex1_'+currrow])
                tax_amount_forex2.append(postdict['tax_amount_forex2_'+currrow])
                tax_amount_forex3.append(postdict['tax_amount_forex3_'+currrow])
                tax_amount_local1.append(postdict['tax_amount_local1_'+currrow])
                tax_amount_local2.append(postdict['tax_amount_local2_'+currrow])
                tax_amount_local3.append(postdict['tax_amount_local3_'+currrow])
                extnamount_forex.append(postdict['extnamount_forex_'+currrow])
                extnamount_local.append(postdict['extnamount_local_'+currrow])
                r_remarks.append(postdict['remarks_'+currrow])
        
        with transaction.atomic():
            # Header
            ormmodelHdr = GLHeader.objects.filter(uid=trxuid)
            if len(ormmodelHdr) == 0:
                ormmodelHdr = GLHeader()
            else:
                ormmodelHdr = ormmodelHdr[0]

            ormmodelHdr.compCode            = compCode
            ormmodelHdr.uid                 = trxuid
            ormmodelHdr.document_type       = document_type
            ormmodelHdr.document_no         = document_no
            ormmodelHdr.date_trans          = date_trans
            ormmodelHdr.document_reference  = document_reference
            ormmodelHdr.additional_reference= additional_reference
            ormmodelHdr.usercode            = currUserCode
            ormmodelHdr.remarks             = remarks
            ormmodelHdr.document_status     = document_status
            ormmodelHdr.party_code          = party_code
            ormmodelHdr.party_name          = party_name
            ormmodelHdr.currency_code       = currency_code
            ormmodelHdr.amount_local        = float(amount_local)
            ormmodelHdr.amount_forex        = float(amount_forex)
            ormmodelHdr.ex_rate             = float(ex_rate)
            ormmodelHdr.tax_amount1         = float(tax_amount1)
            ormmodelHdr.tax_amount2         = float(tax_amount2)
            ormmodelHdr.tax_amount3         = float(tax_amount3)
            ormmodelHdr.nontax_amount1      = float(nontax_amount1)
            ormmodelHdr.nontax_amount2      = float(nontax_amount2)
            ormmodelHdr.nontax_amount3      = float(nontax_amount3)
            ormmodelHdr.valid_till          = valid_till
            ormmodelHdr.term_code           = term_code
            ormmodelHdr.term_days           = float(term_days)
            ormmodelHdr.trx_sign            = float(trx_sign)
            ormmodelHdr.act_code            = act_code

            ormmodelDtlins = GLDetail.objects.filter(uid=trxuid)
            # Detail
            if len(ormmodelDtlins) != 0:
                ormmodelDtlins.delete()
            for i in range(0,len(line_uid)):
                ormmodelDtlins = GLDetail()
                ormmodelDtlins.compCode        = currcomp
                ormmodelDtlins.uid             = trxuid
                ormmodelDtlins.document_type   = document_type
                ormmodelDtlins.document_no     = document_no
                ormmodelDtlins.date_trans      = date_trans
                ormmodelDtlins.party_code      = party_code

                ormmodelDtlins.line_uid        = line_uid[i]
                ormmodelDtlins.line_number     = line_number[i]
                ormmodelDtlins.item_code       = item_code[i]
                ormmodelDtlins.item_description= item_description[i]
                ormmodelDtlins.quantity        = quantity[i]
                ormmodelDtlins.bal_quantity    = bal_quantity[i]
                ormmodelDtlins.unit_price      = unit_price[i]
                ormmodelDtlins.stock_uom       = stock_uom[i]
                ormmodelDtlins.selling_uom     = selling_uom[i]
                ormmodelDtlins.amount_forex    = float(r_amount_forex[i])
                ormmodelDtlins.amount_local    = float(r_amount_local[i])
                ormmodelDtlins.taxable_yn      = taxable_yn[i]
                ormmodelDtlins.tax_code1       = tax_code1[i]
                ormmodelDtlins.tax_code2       = tax_code2[i]
                ormmodelDtlins.tax_code3       = tax_code3[i]
                ormmodelDtlins.tax_pecent1     = tax_pecent1[i]
                ormmodelDtlins.tax_pecent2     = tax_pecent2[i]
                ormmodelDtlins.tax_pecent3     = tax_pecent3[i]
                ormmodelDtlins.discount_percent= discount_percent[i]
                ormmodelDtlins.location_code   = location_code[i]
                ormmodelDtlins.account_code    = account_code[i]
                ormmodelDtlins.db_cr           = db_cr[i]
                ormmodelDtlins.trx_sign        = r_trx_sign[i]
                ormmodelDtlins.ref_document_typ= ref_document_typ[i]
                ormmodelDtlins.ref_document_no = ref_document_no[i]
                ormmodelDtlins.tag_header_yn   = tag_header_yn[i]
                
                ormmodelDtlins.ref_trx_curr    = currency_code
                
                ormmodelDtlins.tax_amount_forex1=tax_amount_forex1[i]
                ormmodelDtlins.tax_amount_forex2=tax_amount_forex2[i]
                ormmodelDtlins.tax_amount_forex3=tax_amount_forex3[i]
                ormmodelDtlins.tax_amount_local1=tax_amount_local1[i]
                ormmodelDtlins.tax_amount_local2=tax_amount_local2[i]
                ormmodelDtlins.tax_amount_local3=tax_amount_local3[i]
                ormmodelDtlins.extnamount_forex=extnamount_forex[i]
                ormmodelDtlins.extnamount_local=extnamount_local[i]
                ormmodelDtlins.remarks         = r_remarks[i]  
                if ormmodelDtlins.amount_forex !=0:
                    ormmodelDtlAll.append(ormmodelDtlins)
                    ormmodelDtlins.save()  
            ormmodelHdr.save()
            
            if transmode == "new" or traction == 'copy':
                tactUtils.updNextNumber(rendertype)
            InsertGLSummary(ormmodelHdr,ormmodelDtlAll)
            if transmode == "new" or traction == 'copy':
                messages.success(request,f'{transDesc} {ormmodelHdr.document_no} Created')
            else:
                messages.success(request,f'{transDesc} {ormmodelHdr.document_no} Updated')
            return {'rendertype':rendertype,'redirect':"trans/"+rendertype}

    ormcoa = CompanyCOA.objects.all().order_by("accountCode")
    ormCust = PartyInfo.objects.all().order_by("partyCode")
    if transmode == 'new':
        nextNumber = tactUtils.getNextNumber(rendertype)
        currDate = datetime.now()
        newuuid = uuid.uuid4()
        defaultAct = DefaultAct.objects.filter(tranType=rendertype.upper())
        if len(defaultAct) != 0:
            defaultAct = defaultAct[0].accountCode;
        else:
            defaultAct = ""
        hdrremarks = ""
        hdrref = ""
        hdraddnlref = ""
        hdrrate = 1
        hdrparty = "GL"
    else:
        nextNumber = ormmodelHdr.document_no
        currDate = ormmodelHdr.date_trans
        newuuid = ormmodelHdr.uid
        if traction == 'copy':
            nextNumber = tactUtils.getNextNumber(rendertype)
            currDate = datetime.now()
            newuuid = uuid.uuid4()
        defaultAct = ormmodelHdr.act_code
        hdrremarks = ormmodelHdr.remarks
        hdrref = ormmodelHdr.document_reference
        hdraddnlref = ormmodelHdr.additional_reference
        hdrrate = ormmodelHdr.ex_rate
        hdrparty = ormmodelHdr.party_code

    
    
    totalrows = transrows + tactUtils.defaultTranRows;
    
    
    ormModelDtlAll = []

    for dtl in ormmodelDtl:
        dtl_line_uid = dtl.line_uid
        if traction == 'copy':
            dtl_line_uid = uuid.uuid4()
        if dtl.trx_sign == 1:
            cr_amt = 0
            dr_amt = dtl.amount_forex
        else:
            cr_amt = dtl.amount_forex
            dr_amt = 0
        ormModelDtlExist = {
            "line_uid" : dtl_line_uid,
            "line_number" : dtl.line_number,
            "item_code" : dtl.item_code,
            "item_description" : dtl.item_description,
            "quantity" : dtl.quantity,
            "bal_quantity" : dtl.bal_quantity,
            "unit_price" : dtl.unit_price,
            "stock_uom" : dtl.stock_uom,
            "selling_uom" : dtl.selling_uom,
            "amount_forex" : dtl.amount_forex,
            "amount_forex_cr" : cr_amt,
            "amount_forex_db" : dr_amt,
            "amount_local" : dtl.amount_local,
            "taxable_yn" : dtl.taxable_yn,
            "tax_code1" : dtl.tax_code1,
            "tax_code2" : dtl.tax_code2,
            "tax_code3" : dtl.tax_code3,
            "tax_pecent1" : dtl.tax_pecent1,
            "tax_pecent2" : dtl.tax_pecent2,
            "tax_pecent3" : dtl.tax_pecent3,
            "discount_percent" : dtl.discount_percent,
            "location_code" : dtl.location_code,
            "account_code" : dtl.account_code,
            "db_cr" : dtl.db_cr,
            "trx_sign" : dtl.trx_sign,
            "ref_document_typ" : dtl.ref_document_typ,
            "ref_document_no" : dtl.ref_document_no,
            "tag_header_yn" : dtl.tag_header_yn,                    
            "tax_amount_forex1" : dtl.tax_amount_forex1,
            "tax_amount_forex2" : dtl.tax_amount_forex2,
            "tax_amount_forex3" : dtl.tax_amount_forex3,
            "tax_amount_local1" : dtl.tax_amount_local1,
            "tax_amount_local2" : dtl.tax_amount_local2,
            "tax_amount_local3" : dtl.tax_amount_local3,
            "extnamount_forex" : dtl.extnamount_forex,
            "extnamount_local" : dtl.extnamount_local,
            "remarks" : dtl.remarks
        }
        ormModelDtlAll.append(ormModelDtlExist)
    for i in range(transrows + 1,totalrows + 1):
        rnewuuid = uuid.uuid4()
        if rendertype == 'cashrcpt':
            trxsign = 1
        else:
            trxsign = -1
        ormModelDtl = {
            "line_uid" : rnewuuid,
            "line_number" : i,
            "item_code" : "STD",
            "item_description" : "STD",
            "quantity" : 1,
            "bal_quantity" : 0,
            "unit_price" : 0,
            "stock_uom" : "STD",
            "selling_uom" : "STD",
            "amount_forex" : 0,
            "amount_forex_cr" : 0,
            "amount_forex_db" : 0,
            "amount_local" : 0,
            "taxable_yn" : "n",
            "tax_code1" : "STD",
            "tax_code2" : "STD",
            "tax_code3" : "STD",
            "tax_pecent1" : 0,
            "tax_pecent2" : 0,
            "tax_pecent3" : 0,
            "discount_percent" : 0,
            "location_code" : "STD",
            "account_code" : "STD",
            "db_cr" : "db",
            "trx_sign" : trxsign,
            "ref_document_typ" : "STD",
            "ref_document_no" : "",
            "tag_header_yn" : "n",                    
            "tax_amount_forex1" : 0,
            "tax_amount_forex2" : 0,
            "tax_amount_forex3" : 0,
            "tax_amount_local1" : 0,
            "tax_amount_local2" : 0,
            "tax_amount_local3" : 0,
            "extnamount_forex" : 0,
            "extnamount_local" : 0,
            "remarks" : ""
        }
        ormModelDtlAll.append(ormModelDtl)
    if traction =='copy':
        transmode = 'new'
    ormModelHdr = {
        "transDesc":transDesc,
        "nextNumber":nextNumber,
        "currDate":currDate,
        "currency": currcomp.compCurrency,
        "act_code": defaultAct,
        "party_code":hdrparty,
        "uuid":newuuid,
        "Reference":hdrref,
        "addnlReference":hdraddnlref,
        "tranRate":hdrrate,
        "narration":hdrremarks,
        "defaultTranRows":range(1,(totalrows)),
        "transmode":transmode,
        "totalrows":totalrows,
        "hdrAccountLabel":hdrAccountLabel,
        "ormmodelHdrAll":ormmodelHdrAll,
        "ormCust":ormCust,
        "ormcoa":ormcoa,
    }
    cntxt = {'rendertype':rendertype,'tactUtils':tactUtils,"noofrecords":len(ormmodelHdrAll),"ormModelHdr":ormModelHdr,"ormModelDtlAll":ormModelDtlAll}
    #print("Context",cntxt)
    return cntxt

def transrec(request,rendertype,uid):
    cntxt= mapTrnModel(request,rendertype,uid)
    if cntxt != None and "redirect" in cntxt.keys():
        return redirect(tactUtils.getDomain(request) + cntxt["redirect"])
    return render(request,'tactb/transactions.html',cntxt)

def transcopy(request,rendertype,uid):
    cntxt= mapTrnModel(request,rendertype,uid,"copy")
    if cntxt != None and "redirect" in cntxt.keys():
        return redirect(tactUtils.getDomain(request) + cntxt["redirect"])
    return render(request,'tactb/transactions.html',cntxt)


def transactions(request,rendertype):
    cntxt= mapTrnModel(request,rendertype)
    if cntxt != None and "redirect" in cntxt.keys():
        return redirect(tactUtils.getDomain(request) + cntxt["redirect"])
    return render(request,'tactb/transactions.html',cntxt)


def getReports(request,rendertype,opt=None):
    currentyear = datetime.now().year
    currfin = FinYear.objects.filter(finYear=currentyear)[0]
    
    datefrom = currfin.dateFrom1
    dateto = datetime.now()
    hdrAccount = ''
    party_code = ''
    search_by  = ''
    gldtl = {}
    if rendertype == "tranenq":
        reportDesc = "Transaction Enquiry"
    elif rendertype == "openbal":
        reportDesc = "Opening Balance"
    elif rendertype == "cashrcpt":
        reportDesc = "Receipts"
    elif rendertype == "cashpaym":
        reportDesc = "Expenses"
    elif rendertype == "acctjrnl": 
        reportDesc = "General Journal"
    elif rendertype == "subscard": 
        reportDesc = "Subscription Card"
    ormcoa = CompanyCOA.objects.all().order_by("accountCode")
    ormCust = PartyInfo.objects.all().order_by("partyCode")
    gldtlopen={}

    if request.method == "POST" or opt == "zoom":
        if opt == "zoom":
            postdict = request.GET
            date_trans_from = postdict["urlfromdate"]
            date_trans_to = postdict["urltodate"]
            hdrAccount = postdict["urlactcode"]
            party_code = ''
            search_by  = ''
        else:
            postdict = request.POST
            date_trans_from = postdict["date_trans_from"]
            date_trans_to = postdict["date_trans_to"]
            hdrAccount = postdict["hdrAccount"]
            party_code = postdict["party_code"]
            search_by  = postdict["search_by"]
        
        if rendertype.lower() != 'TRANENQ'.lower():
            gldtl = GLSummary.objects.filter(document_date__range=[date_trans_from,date_trans_to],document_type=rendertype.upper())
            gldtlopen = GLSummary.objects.filter(document_date__lt=date_trans_from) 
        else:
            gldtl = GLSummary.objects.filter(document_date__range=[date_trans_from,date_trans_to])
            gldtlopen = GLSummary.objects.filter(document_date__lt=date_trans_from)   
        if party_code != '':
            gldtl =gldtl.filter(party_code=party_code)
            gldtlopen = gldtlopen.filter(party_code=party_code)
        if hdrAccount != '':
            gldtl =gldtl.filter(act_code=hdrAccount)
            gldtlopen = gldtlopen.filter(act_code=hdrAccount)
        if search_by != '':
            gldtl = gldtl.filter(Q(document_no__contains=search_by) | Q(remarks__contains= search_by))
            gldtlopen = gldtlopen.filter(Q(document_no__contains=search_by) | Q(remarks__contains= search_by))

        
        gldtl = gldtl.order_by("document_date","document_no","document_type","serial_no")
       
        #print("gldtlopen",gldtlopen)
        datefrom = parse_date(date_trans_from)
        dateto = parse_date(date_trans_to)
        
    
   
    
    document_type = ""
    document_no = ""
    date_trans = ""
    document_reference = ""
    remarks = ""
    amount_forex = ""
    trx_sign = ""
    account_code = ''
    uid = ''

    ormDtlAll=[]
    totalamount = 0
    opbal = 0
    if (len(gldtlopen) > 0):
        for op in gldtlopen:
            opbal = opbal + (op.sign * op.amount_forex)
    
    for det in gldtl:
        displayamt = det.sign * det.amount_forex
        totalamount = totalamount + displayamt
        ormDtl = {
            "document_type":det.document_type,
            "document_no":det.document_no,
            "date_trans":det.document_date,
            "document_reference":det.reference_no,
            "party_code":det.party_code,
            "remarks":det.remarks,
            "account_code":det.act_code,
            "uid":det.uid,
            "amount_forex":displayamt,
            "trx_sign" : det.sign
            
        }
        ormDtlAll.append(ormDtl)

    totalamount = totalamount + opbal
    if totalamount < 0:
        totalamountColor="red"
    else:
        totalamountColor="blue" 
    col1 =50
    col2 =120
    col3 =140
    col4 =300
    col5 =100
    col6 =100
    col7 =140
    col8 =150
    paperwidth = col1 + col2 + col3 + col4+ col5 + col6 + col7 + col8 
    ormHdr = {
        "ormcoa":ormcoa,
        "ormCust":ormCust,
        "datefrom" : datefrom,
        "dateto": dateto,
        "party_code":"GL",
        "hdrAccount":hdrAccount,
        "party_code":party_code,
        "search_by":search_by,
        "noofrecords":len(gldtl),
        "displayamt" : totalamount,
        "displayamtColor" : totalamountColor,
        "opbal": opbal,
        "reportdate":datetime.now(),
        "col1":col1,
        "col2":col2,
        "col3":col3,
        "col4":col4,
        "col5":col5,
        "col6":col6,
        "col7":col7,
        "col8":col8,
        "paperwidth":paperwidth,
        "colspan":8,
        "tableconfig":'cellpadding=0 cellspacing=2 width='+str(paperwidth)+"px",
        "opt":opt
    }
    cntxt ={
        "reportDesc":reportDesc,
        'rendertype':rendertype,
        'tactUtils':tactUtils,
        "ormHdr" :ormHdr,
        "ormDtlAll":ormDtlAll
    }
    return cntxt


def getSubsCard(request,rendertype,opt=None):
    search_by  = ''
    gldtl = {}
    ormsub = {}
    reportDesc = "Member Cards"
    if request.method == "POST":
        postdict = request.POST
        search_by = postdict["search_by"]
        ormsub = Subscribers.objects.all().order_by("subsId")
        ormsub = ormsub.filter(Q(subsId__contains=search_by) | Q(subsName__contains= search_by)| Q(subBranch__contains= search_by)|Q(subPPOno__contains= search_by))
        
        

    ormDtlAll=[]
   
    
    for subs in ormsub:
        ormDtl = {
                "id":subs.id,
                "subsId":subs.subsId,
                "subsName":subs.subsName,
                "subDOB":subs.subDOB,
                "subDOR":subs.subDOR,
                "subPPOno":subs.subPPOno,
                "subBranch":subs.subBranch,
                "subAddr1":subs.subAddr1,
                "subAddr2":subs.subAddr2,

            }
        #print("Details:",ormDtl)
        ormDtlAll.append(ormDtl)

            

   
    col1 =2200
    paperwidth = col1 
    ormHdr = {
       
        "search_by":search_by,
        "noofrecords":len(ormDtlAll),
        "col1":col1,
        "paperwidth":paperwidth,
        "colspan":5,
        "tableconfig":'cellpadding=0 cellspacing=2 width='+str(paperwidth)+"px"
    }
    cntxt ={
        "reportDesc":reportDesc,
        'rendertype':rendertype,
        'tactUtils':tactUtils,
        "ormHdr" :ormHdr,
        "ormDtlAll":ormDtlAll
    }
    return cntxt

def getSummReports(request,rendertype,opt=None):
    currentyear = datetime.now().year
    currfin = FinYear.objects.filter(finYear=currentyear)[0]
    
    datefrom = currfin.dateFrom1
    dateto = datetime.now()
    hdrAccount = ''
    party_code = ''
    search_by  = ''
    gldtl = {}
    reportDesc = "Trial Balance"
        
    #ormcoa = CompanyCOA.objects.filter(accountCode='9999').order_by("accountCode")
    ormcoa = CompanyCOA.objects.all().order_by("accountCode")
   #print("ormcoa",ormcoa)
    if request.method == "POST":
        postdict = request.POST
        date_trans_from = postdict["date_trans_from"]
        date_trans_to = postdict["date_trans_to"]
        
        gldtl = GLSummary.objects.filter(document_date__lte=date_trans_to)
        
        #print("gldtl",len(gldtl))
        datefrom = parse_date(date_trans_from)
        dateto = parse_date(date_trans_to)
    
    amount_forex = ""
    account_code = ''

    ormDtlAll=[]
    totalamountdb = 0
    totalamountcr = 0
   
    
    for coa in ormcoa:
        if len(gldtl) > 0:
            det = gldtl.filter(act_code=coa.accountCode)
            displayamt =  0
            if len(det) > 0:
                for i in det:
                    displayamt = displayamt + i.sign * i.amount_forex
            amount_db = 0
            amount_cr = 0
            if displayamt < 0:
                totalamountcr = totalamountcr + displayamt
                amount_cr = displayamt
            else:
                totalamountdb = totalamountdb + displayamt
                amount_db = displayamt

            ormDtl = {
                "account_code":coa.accountCode,
                "account_desc":coa.accountName,
                "amount_db":abs(amount_db),
                "amount_cr":abs(amount_cr),
            }
            ormDtlAll.append(ormDtl)

   

    if totalamountdb < 0:
        totalamountColorDb="red"
    else:
        totalamountColorDb="blue" 
    if totalamountcr < 0:
        totalamountColorCr="red"
    else:
        totalamountColorCr="blue" 
    col1 =50
    col2 =150
    col3 =350
    col4 =200
    col5 =200
    paperwidth = col1 + col2 + col3 + col4 + col5
    ormHdr = {
        "datefrom" : datefrom,
        "dateto": dateto,
        "party_code":"GL",
        "hdrAccount":hdrAccount,
        "party_code":party_code,
        "search_by":search_by,
        "noofrecords":len(ormDtlAll),
        "displayamtdb" : abs(totalamountdb),
        "displayamtcr" : abs(totalamountcr),
        "displayamtColorDb":totalamountColorDb,
        "displayamtColorCr":totalamountColorCr,
        "reportdate":datetime.now(),
        "col1":col1,
        "col2":col2,
        "col3":col3,
        "col4":col4,
        "col5":col5,
        "paperwidth":paperwidth,
        "colspan":5,
        "tableconfig":'cellpadding=0 cellspacing=2 width='+str(paperwidth)+"px"
    }
    cntxt ={
        "reportDesc":reportDesc,
        'rendertype':rendertype,
        'tactUtils':tactUtils,
        "ormHdr" :ormHdr,
        "ormDtlAll":ormDtlAll
    }
    return cntxt



def reports(request,rendertype,opt=None):
    if rendertype.lower( ) == 'trialbal':
        cntxt = getSummReports(request,rendertype)
    elif rendertype.lower( ) == 'subscard':
        cntxt = getSubsCard(request,rendertype)
    else:
        cntxt = getReports(request,rendertype)
    return render(request,'tactb/reports.html',cntxt)

def reportsprint(request,rendertype,opt=None):
    if rendertype.lower( ) == 'trialbal':
        cntxt = getSummReports(request,rendertype)
    elif rendertype.lower( ) == 'subscard':
        cntxt = getSubsCard(request,rendertype)
    else:
        cntxt = getReports(request,rendertype)
    if rendertype.lower( ) != 'subscard':
        return render(request,'tactb/reportsprint.html',cntxt)
    else:
        return render(request,'tactb/printcard.html',cntxt)


def reportszoom(request,rendertype,opt=None):
    cntxt = getReports(request,rendertype,"zoom")
    return render(request,'tactb/reports.html',cntxt)


def siteadmin(request):
    cntxt= {}
    return render(request,'tactb/master.html',cntxt)