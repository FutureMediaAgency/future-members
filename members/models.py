from django.db import models
from django.utils import timezone
from datetime import timedelta
import io
import qrcode
from django.core.files.base import ContentFile

class Member(models.Model):
    TIERS=[("أساسية","أساسية"),("مهنية","مهنية"),("مميزة","مميزة"),("سفير فيوتشر","سفير فيوتشر")]
    STATUSES=[("قيد المراجعة","قيد المراجعة"),("نشطة","نشطة"),("قريبة الانتهاء","قريبة الانتهاء"),("منتهية","منتهية"),("موقوفة","موقوفة"),("ملغاة","ملغاة")]
    PAY=[("نقدي","نقدي"),("تحويل","تحويل"),("أخرى","أخرى")]
    membership_number=models.CharField(max_length=30,unique=True,blank=True)
    full_name=models.CharField(max_length=150); phone=models.CharField(max_length=30,blank=True); email=models.EmailField(blank=True)
    profession=models.CharField(max_length=120,blank=True); tier=models.CharField(max_length=30,choices=TIERS,default="أساسية")
    issue_date=models.DateField(default=timezone.localdate); expiry_date=models.DateField(blank=True,null=True)
    payment_method=models.CharField(max_length=20,choices=PAY,blank=True); status=models.CharField(max_length=30,choices=STATUSES,default="قيد المراجعة")
    photo=models.ImageField(upload_to="members/",blank=True,null=True); skills=models.TextField(blank=True); notes=models.TextField(blank=True)
    qr_code=models.ImageField(upload_to="qrcodes/",blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.membership_number:
            y=timezone.localdate().year; last=Member.objects.filter(membership_number__startswith=f"FM-{y}-").order_by("-id").first(); n=int(last.membership_number[-4:])+1 if last else 1; self.membership_number=f"FM-{y}-{n:04d}"
        if not self.expiry_date: self.expiry_date=self.issue_date+timedelta(days=365)
        generate_qr = not self.qr_code
        super().save(*args,**kwargs)
        if generate_qr:
            qr_img = qrcode.make(self.membership_number)
            buffer = io.BytesIO()
            qr_img.save(buffer, format="PNG")
            filename = f"{self.membership_number}.png"
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
            super().save(update_fields=["qr_code"])
    def __str__(self): return f"{self.membership_number} — {self.full_name}"
