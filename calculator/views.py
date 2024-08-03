from django.shortcuts import render
from . import BBCalc
import json
import os
import pdb

# Create your views here.
def index(request):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    os.chdir('..')
    with open('static/atkPresets.json', 'r') as f:
        # atkPresetJSON = f.read()
        atkPresetJSON = json.load(f)
    with open('static/defPresets.json', 'r') as f:
        # defPresetJSON = f.read()
        defPresetJSON = json.load(f)
    if request.GET:
        results = BBCalc.main(**BBCalc.parse(request.GET))
        context = {
            'atkPresetJSON': atkPresetJSON,
            'defPresetJSON': defPresetJSON,
            'results': results,
            'request': request.GET,
            'AtkWeapon': request.GET.getlist('AtkWeapon'),
            'AtkPerks': request.GET.getlist('AtkPerks'),
            'AtkTraits': request.GET.getlist('AtkTraits'),
            'AtkInjuries': request.GET.getlist('AtkInjuries'),
            'AtkStatus': request.GET.getlist('AtkStatus'),
            'DefPerks': request.GET.getlist('DefPerks'),
            'DefTraits': request.GET.getlist('DefTraits'),
            'DataReturns': request.GET.getlist('DataReturns'),
        }
        print('Context')
        print(context['request'])
        print(context['AtkWeapon'])
        print(context['AtkPerks'])
        print(context['AtkTraits'])
        print(context['AtkInjuries'])
        print(context['AtkStatus'])
        print(context['DefPerks'])
        print(context['DefTraits'])
        print('-----------------------------------')
    else:
        context = {'atkPresetJSON': atkPresetJSON, 'defPresetJSON': defPresetJSON, 'DataReturns': ['DeathMean', 'DeathStDev', 'DeathPercent', 'InjuryMean', 'HeavyInjuryMean'],}
    return render(request, 'index.html', context)