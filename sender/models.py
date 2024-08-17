from django.db import models

# Create your models here.
class SmsLog(GUIDModel):
    METE = 'mete'
    CHANGE_METE = 'change_mete'
    PEST = 'pest'
    NEW_ACTIVITY = 'new_activity'
    OVERDUE_ACTIVITY = 'overdue_activity'
    PEST_VALIDATION = 'pest_validation'
    NUTRITION = 'nutrition'
    PEST_FEEDBACK = 'pest_feedback'
    WEATHER_FEEDBACK = 'weather_feedback'
    SALE = 'sale'
    AUCTION = 'auction'
    PREPAYMENT = 'prepayment'
    ADD_CULTIVATION_ALERT= 'add_cultivation_alert'
    EXPIRED_AGRI = 'expired_agri'
    EXPIRED_NONEAGRI = 'expired_noneagri'
    FARM_WITHOUT_CULTI = 'farm_without_culti'
    Farm_Permission = 'farm_permission'
    UTM_Report = 'utm_report'
    Invited_Number = 'invited_number'
    Chat_Market = 'chat_market'
    Chat_Shop = 'chat_shop'
    Card_To_Card = 'card_to_card'
    Violation = 'violation'
    Subscription_Inactive = 'subscription_inactive'
    OTHER = 'other'
    ALL = 'all'
    PROMOTION = "promotion"
    PUbLIC_NOTIFICATION = 'PUbLIC_NOTIFICATION'

    TYPE_CHOICES = [(METE, 'mete'),
                    (CHANGE_METE,'change_mete'),
                    (PEST, 'pest'),
                    (NEW_ACTIVITY, 'new_activity'),
                    (OVERDUE_ACTIVITY, 'overdue_activity'),
                    (PEST_VALIDATION, 'pest_validation'),
                    (NUTRITION, 'nutrition'),
                    (PEST_FEEDBACK, 'pest_feedback'),
                    (WEATHER_FEEDBACK, 'weather_feedback'),
                    (SALE, 'sale'),
                    (AUCTION, 'auction'),
                    (PREPAYMENT, 'prepayment'),
                    (EXPIRED_AGRI, 'expired_agri'),
                    (EXPIRED_NONEAGRI, 'expired_noneagri'),
                    (FARM_WITHOUT_CULTI, 'farm_without_culti'),
                    (ADD_CULTIVATION_ALERT, 'add_cultivation_alert'),
                    (Farm_Permission, 'farm_permission'),
                    (UTM_Report, 'utm_report'),
                    (Invited_Number, 'invited_number'),
                    (Chat_Market, 'chat_market'),
                    (Chat_Shop , 'chat_shop'),
                    (Card_To_Card, 'card_to_card'),                    
                    (Violation, 'violation'),
                    (Subscription_Inactive, 'subscription_inactive'),
                    (OTHER, 'other'),
                    (ALL, 'all'),
                    (PROMOTION, 'promotion'),
                    (PUbLIC_NOTIFICATION, 'PUbLIC_NOTIFICATION'),
                    ]
    
    sender = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100)
    message = models.TextField()
    message_id = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(blank=True, null=True, max_length=100, choices=TYPE_CHOICES)
    status = models.CharField(max_length=5, blank=True, null=True)
    status_text = models.CharField(max_length=100, blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    sender_promotion = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    advertisement_promoted = models.ForeignKey(BaseAdvertisement,blank=True,null=True,on_delete=models.SET_NULL)
    requirement_promoted = models.ForeignKey(BaseRequirement,blank=True,null=True,on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return self.phone
    
    
    
    
    from django.db import models
from apps.base.models.guidModel import GUIDModel


class WebPushLog(GUIDModel):
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    app = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    is_sent = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title








from django.db import models
from apps.base.models.guidModel import GUIDModel


class EmailLog(GUIDModel):
    
    PUBLIC_NOTIFICATION = 'public_notification'
    OTP = 'otp'
    

    TYPE_CHOICES = (
        (PUBLIC_NOTIFICATION, 'نوتیف عمومی'),
        (OTP, 'احراز هویت'),
    )
    
    SEND = 'send'
    FAIL = 'fail'

    STATUS_CHOICES = (
        (SEND, 'ارسال شده'),
        (FAIL, 'ارسال نشده'),
    )
                    
    sender_email = models.CharField(verbose_name="ارسال کننده",max_length=128)
    recipient_email = models.CharField(verbose_name="دریافت کننده",max_length=128)
    subject = models.CharField(max_length=512,blank=True,null=True)
    message = models.TextField(verbose_name="محتوا",blank=True,null=True)
    email_type = models.CharField(blank=True, null=True, max_length=100, choices=TYPE_CHOICES)
    status = models.CharField(verbose_name="وضعیت",max_length=16,blank=True,null=True,choices=STATUS_CHOICES)
    
    
    def __str__(self) -> str:
        
        return f"{self.email_type} to {self.recipient_email}"
    
    