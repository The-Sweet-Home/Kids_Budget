from django.shortcuts import render, redirect
from django.contrib import messages

from .utils import calculate_financials

KID_PASSWORDS = {
    'Shaina': 'shaina123',
    'Viana': 'viana123',
}


def index(request):
    if request.method == 'POST':
        kid = request.POST.get('kid')
        password = request.POST.get('password')
        if KID_PASSWORDS.get(kid) == password:
            request.session['authenticated_kid'] = kid
            return redirect('kid_dashboard', kid_name=kid)
        else:
            messages.error(request, 'Invalid password.')

    return render(request, 'budget/index.html')


def kid_dashboard(request, kid_name):
    if request.session.get('authenticated_kid') != kid_name:
        return redirect('index')

    data = calculate_financials(kid_name)
    
    return render(request, 'budget/kid_dashboard.html', {
        'kid_name': kid_name,
        'financial_data': data,
        'monthly_incomes': data['monthly_incomes'],
        'monthly_expenses': data['monthly_expenses'],
    })
        