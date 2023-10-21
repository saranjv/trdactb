from datetime import datetime
from email.policy import default
from typing import Text
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.


class CompanyInfo(models.Model):
    def __str__(self):
        return self.compCode
    compCode = models.CharField(max_length=50)
    compName = models.CharField(max_length=200)
    compAddress1 = models.CharField(max_length=200)
    compAddress2 = models.CharField(max_length=200)
    compCity = models.CharField(max_length=100)
    compState = models.CharField(max_length=100)
    compCountry = models.CharField(max_length=100)
    compZipcode = models.CharField(max_length=100)
    compTelephone = models.CharField(max_length=100)
    compFax = models.CharField(max_length=100)
    compEmail = models.CharField(max_length=100)
    compLogo = models.ImageField()
    compCurrency = models.CharField(max_length=3) 






class FinYear(models.Model):
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    finYear = models.IntegerField()
    dateFrom1 = models.DateField()
    dateTo1 = models.DateField()
    dateFrom2 = models.DateField()
    dateTo2 = models.DateField() 
    dateFrom3 = models.DateField()
    dateTo3 = models.DateField() 
    dateFrom4 = models.DateField()
    dateTo4 = models.DateField()
    dateFrom5 = models.DateField()
    dateTo5 = models.DateField() 
    dateFrom6 = models.DateField()
    dateTo6 = models.DateField() 
    dateFrom7 = models.DateField()
    dateTo7 = models.DateField() 
    dateFrom8 = models.DateField()
    dateTo8 = models.DateField() 
    dateFrom9 = models.DateField()
    dateTo9 = models.DateField() 
    dateFrom10 = models.DateField()
    dateTo10 = models.DateField() 
    dateFrom11 = models.DateField()
    dateTo11 = models.DateField() 
    dateFrom12 = models.DateField()
    dateTo12 = models.DateField() 


class Modaccess(models.Model):
    def __str__(self):
        return self.compCode
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    accesibleModules = models.TextField()
    


class UserModaccess(models.Model):
    def __str__(self):
        return self.userId
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    userAccess = models.TextField()
    accesibleCompany = models.TextField()
    

class CompanyCOA(models.Model):
    def __str__(self):
        return self.accountCode
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    accountCode = models.CharField(max_length=50)
    accountName = models.CharField(max_length=200)
    accountType = models.CharField(max_length=20)

class AutoNum(models.Model):
    def __str__(self):
        return self.tranType
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    tranType = models.CharField(max_length=50)
    prefix = models.CharField(max_length=200)
    autonum = models.IntegerField()

class DefaultAct(models.Model):
    def __str__(self):
        return self.tranType
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    tranType = models.CharField(max_length=50)
    accountCode = models.CharField(max_length=50)


class PartyInfo(models.Model):
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    partyCode = models.CharField(max_length=200)
    partyName = models.CharField(max_length=200)
    partyName2 = models.CharField(max_length=200)
    partyAddress1 = models.CharField(max_length=200)
    partyAddress2 = models.CharField(max_length=200)
    partyCity = models.CharField(max_length=100)
    partyState = models.CharField(max_length=100)
    partyCountry = models.CharField(max_length=100)
    partyZipcode = models.CharField(max_length=100)
    partyTelephone = models.CharField(max_length=100)
    partyFax = models.CharField(max_length=100)
    partyEmail = models.CharField(max_length=100)


class Subscribers(models.Model):
    compCode = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    subsId = models.CharField(max_length=200)
    subsName = models.CharField(max_length=200)
    subDOB = models.DateField(default=timezone.now) 
    subDOR = models.DateField(default=timezone.now) 
    subPPOno = models.CharField(max_length=200,default="")
    subBranch = models.CharField(max_length=200,default="")
    subAddr1 = models.CharField(max_length=200,default="")
    subAddr2 = models.CharField(max_length=200,default="")
    
    

class GLHeader(models.Model):    
    def __str__(self):
        return str(self.document_type) + '---'+ str(self.document_no)
    compCode            = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    uid                 = models.UUIDField(default = uuid.uuid4, editable = True)
    document_type       = models.CharField(max_length=50,default="")
    document_no         = models.CharField(max_length=50,default="")
    date_trans          = models.DateField(default=timezone.now)
    document_reference  = models.CharField(max_length=50,default="")
    additional_reference= models.CharField(max_length=50,default="")
    usercode            = models.CharField(max_length=50,default="")
    remarks             = models.TextField(default="")
    document_status     = models.CharField(max_length=50,default="a")
    party_code          = models.CharField(max_length=50,default="")
    party_name          = models.CharField(max_length=200,default="")
    currency_code       = models.CharField(max_length=3,default="")
    amount_local        = models.FloatField(max_length=50,default=0)
    amount_forex        = models.FloatField(max_length=50,default=0)
    ex_rate             = models.FloatField(max_length=50,default=1)
    tax_amount1         = models.FloatField(max_length=50,default=0)
    tax_amount2         = models.FloatField(max_length=50,default=0)
    tax_amount3         = models.FloatField(max_length=50,default=0)
    nontax_amount1      = models.FloatField(max_length=50,default=0)
    nontax_amount2      = models.FloatField(max_length=50,default=0)
    nontax_amount3      = models.FloatField(max_length=50,default=0)
    valid_till          = models.DateField(default=timezone.now)
    term_code           = models.CharField(max_length=50,default="")
    term_days           = models.IntegerField(default=0)
    trx_sign            = models.IntegerField(default=1)
    act_code            = models.CharField(max_length=50,default="")


class GLDetail(models.Model):
    def __str__(self):
        return str(self.document_type) + '---'+ str(self.document_no) + '---'+ str(self.line_number)
    compCode            = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    uid             = models.UUIDField(default = uuid.uuid4, editable = True)
    line_uid        = models.UUIDField(default = uuid.uuid4, editable = True)
    document_type   = models.CharField(max_length=50,default="")
    document_no     = models.CharField(max_length=50,default="")
    line_number     = models.IntegerField(default=0)
    item_code       = models.CharField(max_length=50,default="")
    item_description= models.CharField(max_length=200,default="")
    quantity        = models.IntegerField(default=1)
    bal_quantity    = models.FloatField(default=0)
    unit_price      = models.FloatField(default=0)
    stock_uom       = models.CharField(max_length=50,default="")
    selling_uom     = models.CharField(max_length=50,default="")
    amount_forex    = models.FloatField(default=0)
    amount_local    = models.FloatField(default=0)
    taxable_yn      = models.CharField(max_length=50,default="n")
    tax_code1       = models.CharField(max_length=50,default="")
    tax_code2       = models.CharField(max_length=50,default="")
    tax_code3       = models.CharField(max_length=50,default="")
    tax_pecent1     = models.FloatField(default=0)
    tax_pecent2     = models.FloatField(default=0)
    tax_pecent3     = models.FloatField(default=0)
    discount_percent= models.FloatField(default=0)
    location_code   = models.CharField(max_length=50,default="") 
    account_code    = models.CharField(max_length=50,default="")
    db_cr           = models.CharField(max_length=2,default="db")
    trx_sign        = models.IntegerField(default=1)
    ref_document_typ= models.CharField(max_length=50,default="")
    ref_document_no = models.CharField(max_length=50,default="")
    tag_header_yn   = models.CharField(max_length=1,default="d")
    party_code      = models.CharField(max_length=50,default="")
    ref_trx_curr    = models.CharField(max_length=3,default="")
    date_trans      = models.DateField(default=timezone.now)
    tax_amount_forex1=models.FloatField(default=0)
    tax_amount_forex2=models.FloatField(default=0)
    tax_amount_forex3=models.FloatField(default=0)
    tax_amount_local1=models.FloatField(default=0)
    tax_amount_local2=models.FloatField(default=0)
    tax_amount_local3=models.FloatField(default=0)
    extnamount_forex=models.FloatField(default=0)
    extnamount_local=models.FloatField(default=0)
    remarks         = models.TextField(max_length=50,default="")


class GLSummary(models.Model):
    def __str__(self):
        return str(self.document_type) + '---'+ str(self.document_no)+ '---'+ str(self.serial_no)
    compCode        = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE,default=1)
    uid             = models.UUIDField(default = uuid.uuid4, editable = True)
    reference_no    = models.CharField(max_length=50,default="")
    reference_uid   = models.UUIDField(default = uuid.uuid4, editable = True)
    act_year        = models.IntegerField(default=1)
    act_period      = models.IntegerField(default=1)
    document_type   = models.CharField(max_length=50,default="")
    document_no     = models.CharField(max_length=50,default="")
    document_date   = models.DateField(default=timezone.now)
    serial_no       = models.IntegerField(default=1)
    act_code        = models.CharField(max_length=50,default="")
    curr_code       = models.CharField(max_length=3,default="")
    sign            = models.IntegerField(default=1)
    amount_local    = models.FloatField(default=0)
    amount_forex    = models.FloatField(default=0)
    entered_by      = models.CharField(max_length=50,default="")
    enterd_date     = models.DateField(default=timezone.now)
    party_code      = models.CharField(max_length=50,default="")
    party_name      = models.CharField(max_length=200,default="")
    item_code       = models.CharField(max_length=50,default="")
    item_description= models.CharField(max_length=200,default="")
    remarks         = models.TextField(max_length=50,default="")
    trans_mode      = models.CharField(max_length=50,default="")
    offset_act      = models.CharField(max_length=50,default="")
    location_code   = models.CharField(max_length=50,default="")
    entry_type      = models.CharField(max_length=50,default="")