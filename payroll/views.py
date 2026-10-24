from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Employee, Attendance, Payroll


@login_required
def dashboard(request):
    employee = get_object_or_404(Employee, user=request.user)
    attendance_all = Attendance.objects.filter(employee=employee)

    context = {
        'employee': employee,
        'present_count': attendance_all.filter(status='P').count(),
        'absent_count': attendance_all.filter(status='A').count(),
        'leave_count': attendance_all.filter(status='L').count(),
        'attendance_list': attendance_all.order_by('-date')[:30],
        'payroll_list': Payroll.objects.filter(employee=employee).order_by('-month'),
    }
    return render(request, 'payroll/dashboard.html', context)


@login_required
def payslip(request, pk):
    if request.user.is_staff:
        p = get_object_or_404(Payroll, pk=pk)
    else:
        p = get_object_or_404(Payroll, pk=pk, employee__user=request.user)
    return render(request, 'payroll/payslip.html', {'p': p})


@login_required
def profile(request):
    employee = get_object_or_404(Employee, user=request.user)
    return render(request, 'payroll/profile.html', {'employee': employee})


@login_required
def settings(request):
    employee = get_object_or_404(Employee, user=request.user)
    return render(request, 'payroll/settings.html', {'employee': employee})