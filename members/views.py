from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MemberRegistrationForm
from .models import Member
from .qr_utils import make_qr_svg

def home(request):
    return render(request, "members/home.html", {
        "active": Member.objects.filter(status="نشطة").count(),
        "total": Member.objects.count()
    })

def register(request):
    if request.method == "POST":
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.status = "قيد المراجعة"
            member.save()
            messages.success(request, f"تم استلام طلبك. رقم الطلب: {member.membership_number}")
            return redirect("home")
    else:
        form = MemberRegistrationForm()
    return render(request, "members/register.html", {"form": form})

def verify(request, membership_number):
    member = get_object_or_404(Member, membership_number=membership_number)
    return render(request, "members/verify.html", {"member": member})
def member_qr(request, membership_number):
    member = get_object_or_404(Member, membership_number=membership_number)

    verify_url = f"https://cheats-voices-hash-dean.trycloudflare.com/verify/{member.membership_number}/"

    return HttpResponse(
        make_qr_svg(verify_url),
        content_type="image/svg+xml"
    )
    return HttpResponse(make_qr_svg(verify_url), content_type="image/svg+xml")
def dashboard(request):
    total = Member.objects.count()
    active = Member.objects.filter(status="نشطة").count()
    pending = Member.objects.filter(status="قيد المراجعة").count()
    expiring = Member.objects.filter(status="قريبة الانتهاء").count()
    expired = Member.objects.filter(status="منتهية").count()

    recent_members = Member.objects.order_by("-created_at")[:10]

    search_query = request.GET.get("q", "").strip()

    search_results = Member.objects.none()

    if search_query:
        search_results = Member.objects.filter(
            models.Q(membership_number__icontains=search_query)
            | models.Q(full_name__icontains=search_query)
            | models.Q(phone__icontains=search_query)
            | models.Q(email__icontains=search_query)
        )

    return render(
        request,
        "members/dashboard.html",
        {
            "total": total,
            "active": active,
            "pending": pending,
            "expiring": expiring,
            "expired": expired,
            "recent_members": recent_members,
            "search_query": search_query,
            "search_results": search_results,
        },
    )
def member_detail(request, membership_number):
    member = get_object_or_404(
        Member,
        membership_number=membership_number
    )

    return render(
        request,
        "members/member_detail.html",
        {"member": member}
    )



