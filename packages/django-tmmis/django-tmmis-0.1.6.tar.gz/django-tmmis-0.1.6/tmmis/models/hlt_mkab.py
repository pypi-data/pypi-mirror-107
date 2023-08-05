from .base_model import *


class Gender(models.IntegerChoices):
    FEMALE = 0,
    MALE = 1


class HltMkab(BaseModel):
    """
    Медицинская карта амбулаторного больного
    """
    id = models.AutoField(db_column='MKABID', primary_key=True)
    uuid = models.CharField(db_column='UGUID', max_length=36, unique=True, default=uuid.uuid4)
    family = models.CharField(db_column='FAMILY', max_length=40)
    name = models.CharField(db_column='NAME', max_length=40)
    ot = models.CharField(db_column='OT', max_length=40)
    ss = models.CharField(db_column='SS', max_length=14)
    d_type = models.CharField('Признак Особый случай', db_column='D_TYPE', max_length=3)
    num = models.CharField(db_column='NUM', max_length=40)
    w = models.IntegerField(db_column='W', choices=Gender.choices)
    date_bd = models.DateTimeField(db_column='DATE_BD')
    address = models.CharField(db_column='ADRES', max_length=200)
    inv = models.IntegerField(db_column='rf_INVID')
    smo = models.ForeignKey('OmsSmo', models.DO_NOTHING, related_name='+', db_column='rf_SMOID')
    other_smo = models.ForeignKey('OmsSmo', models.DO_NOTHING, related_name='+', db_column='rf_OtherSMOID')
    phone_work = models.CharField(db_column='PhoneWork', max_length=20)
    phone_home = models.CharField(db_column='PhoneHome', max_length=20)
    work = models.CharField(db_column='Work', max_length=200)
    profession = models.CharField(db_column='Profession', max_length=50)
    post = models.CharField(db_column='Post', max_length=50)
    dependent = models.BooleanField(db_column='Dependent')
    lpu = models.ForeignKey('OmsLpu', models.DO_NOTHING, db_column='rf_LPUID')
    # rf_group_of_blood = models.ForeignKey('HltGroupOfBloodRh', models.DO_NOTHING, db_column='rf_GroupOfBloodID')
    kindcod = models.BooleanField(db_column='KindCod')
    rh = models.BooleanField(db_column='RH')
    cod_person = models.CharField(db_column='COD_Person', max_length=20)
    military_cod = models.CharField(db_column='MilitaryCOD', max_length=3)
    uchastok = models.ForeignKey('HltUchastok', models.DO_NOTHING, db_column='rf_UchastokID')
    citizen = models.IntegerField(db_column='rf_CitizenID')
    type_doc = models.ForeignKey('OmsTypedoc', models.DO_NOTHING, db_column='rf_TYPEDOCID')
    s_doc = models.CharField(db_column='S_DOC', max_length=10)
    n_doc = models.CharField(db_column='N_DOC', max_length=15)
    tip_oms = models.ForeignKey('OmsKlTipOms', models.DO_NOTHING, related_name='+', db_column='rf_kl_TipOMSID')
    s_pol = models.CharField(db_column='S_POL', max_length=50)
    n_pol = models.CharField(db_column='N_POL', max_length=50)
    is_worker = models.BooleanField(db_column='IsWorker')
    mkab_location = models.IntegerField(db_column='rf_MKABLocationID')
    spec_event_cert = models.IntegerField(db_column='rf_SpecEventCertID')
    address_fact = models.CharField(db_column='AdresFact', max_length=200)
    date_pol_begin = models.DateTimeField(db_column='DatePolBegin')
    date_pol_end = models.DateTimeField(db_column='DatePolEnd')
    enterprise = models.IntegerField(db_column='rf_EnterpriseID')
    black_label = models.IntegerField(db_column='BlackLabel')
    okato = models.ForeignKey('OmsOkato', models.DO_NOTHING, db_column='rf_OKATOID')
    is_closed = models.IntegerField(db_column='isClosed')
    reason_close_mkab = models.IntegerField(db_column='rf_ReasonCloseMKABID')
    date_close = models.DateTimeField(db_column='DateClose')
    privilege_category = models.IntegerField(db_column='rf_kl_PrivilegeCategoryID')
    oms_okved = models.ForeignKey('OmsOkved', models.DO_NOTHING, db_column='rf_omsOKVEDID')
    soc_status = models.ForeignKey('OmsKlSocStatus', models.DO_NOTHING, related_name='+', db_column='rf_kl_SocStatusID')
    sex = models.IntegerField(db_column='rf_kl_SexID')
    health_group = models.IntegerField(db_column='rf_kl_HealthGroupID')
    address_live = models.ForeignKey('KlaAddress', models.DO_NOTHING, related_name='+', db_column='rf_AddressLiveID')
    address_reg = models.ForeignKey('KlaAddress', models.DO_NOTHING, related_name='+', db_column='rf_AddressRegID')
    address_work = models.ForeignKey('KlaAddress', models.DO_NOTHING, related_name='+', db_column='rf_AddressWorkID')
    confirm_agree = models.BooleanField(db_column='ConfirmAgree')
    confirm_date = models.DateTimeField(db_column='ConfirmDate')
    confirm_user_fio = models.CharField(db_column='ConfirmUserFIO', max_length=50)
    contact_confirm = models.BooleanField(db_column='contactConfirm')
    contact_email = models.CharField(db_column='contactEmail', max_length=100)
    contact_mphone = models.CharField(db_column='contactMPhone', max_length=25)
    create_username = models.CharField(db_column='CreateUserName', max_length=255)
    edit_username = models.CharField(db_column='EditUserName', max_length=255)
    confirm_user = models.ForeignKey('XUser', models.DO_NOTHING, related_name='+', db_column='rf_ConfirmUserID')
    create_user = models.ForeignKey('XUser', models.DO_NOTHING, related_name='+', db_column='rf_CreateUserID')
    edit_user = models.ForeignKey('XUser', models.DO_NOTHING, related_name='+', db_column='rf_EditUserID')
    hash0 = models.CharField(db_column='Hash0', max_length=65)
    hash1 = models.CharField(db_column='Hash1', max_length=65)
    hash2 = models.CharField(db_column='Hash2', max_length=65)
    hash3 = models.CharField(db_column='Hash3', max_length=65)
    hash4 = models.CharField(db_column='Hash4', max_length=65)
    is_encrypted = models.BooleanField(db_column='isEncrypted')
    main_contact = models.IntegerField(db_column='mainContact')
    message_flag = models.IntegerField(db_column='MessageFLAG')
    ridn = models.CharField(db_column='RIDN', max_length=10)
    mkab_info = models.TextField(db_column='MKABInfo')
    birth_place = models.CharField(db_column='Birthplace', max_length=200)
    date_doc = models.DateTimeField(db_column='DateDoc')
    is_ls_home = models.BooleanField(db_column='isLSHome')
    main_mkab = models.ForeignKey('self', models.DO_NOTHING, db_column='MainMKABGuid', to_field='uuid')
    date_mkab = models.DateTimeField(db_column='DateMKAB')
    doc_issued_by = models.CharField(db_column='DocIssuedBy', max_length=255)
    education_type = models.IntegerField(db_column='rf_kl_EducationTypeID')
    material_status = models.IntegerField(db_column='rf_kl_MaterialStatusID')
    is_auto = models.BooleanField(db_column='isAuto')
    black_label_comment = models.CharField(db_column='BlackLabelComment', max_length=255)
    is_exist_ipra = models.BooleanField(db_column='isExistIPRA')
    oksm = models.IntegerField(db_column='rf_OKSMID')
    identification_date = models.DateTimeField(db_column='IdentificationDate')
    identification_status = models.IntegerField(db_column='rf_IdentificationStatusID')
    is_no_email = models.BooleanField(db_column='IsNoEmail')
    is_no_phone = models.BooleanField(db_column='IsNoPhone')
    med_intervention = models.SmallIntegerField(db_column='MedIntervention')
    rhesus = models.SmallIntegerField(db_column='Rhesus')
    qualification = models.CharField(db_column='Qualification', max_length=255)
    group = models.CharField(db_column='Group', max_length=255)
    military_duty = models.IntegerField(db_column='rf_MilitaryDutyID')
    inn = models.CharField(db_column='INN', max_length=12)
    milk_food_type = models.IntegerField(db_column='rf_atc_MilkFoodTypeID')
    milk_food_payment = models.IntegerField(db_column='rf_atc_MilkFoodPaymentID')
    food_payment_date = models.DateTimeField(db_column='FoodPaymentDate')

    flags = models.IntegerField(db_column='FLAGS')

    class Meta:
        managed = False
        db_table = 'hlt_MKAB'
