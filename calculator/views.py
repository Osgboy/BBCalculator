from django.shortcuts import render
from django.http import HttpResponseBadRequest
from collections import defaultdict
from . import BBCalc
import json
import pathlib
import pdb

# Create your views here.

def parse(query: dict) -> dict:
    kwargs = {}
    intArgs = (
        'Trials',
        'Mind',
        'Maxd',
        'Ignore',
        'ArmorMod',
        'Headchance',
        'Atk_Resolve',
        'Def_HP',
        'Def_Helmet',
        'Def_Armor',
        'Fatigue',
        'Def_Resolve',
        'HitChance',
    )
    for k, v in query.lists():
        try:
            if k in intArgs:
                kwargs[k] = int(v[0])
            elif v != 'None':
                for arg in v:
                    kwargs[arg] = True # exploitable?
        except Exception:
            pass

    # Validation
    def clamp(x: int, lowerB: int, upperB: int) -> int:
        return max(min(x, upperB), lowerB)
    
    try:
        kwargs['Mind'] = max(kwargs['Mind'], 1)
        kwargs['Maxd'] = max(kwargs['Mind'], kwargs['Maxd'])
        kwargs['Ignore'] = max(kwargs['Ignore'], 0)
        kwargs['ArmorMod'] = max(kwargs['ArmorMod'], 1)
    except KeyError:
        pass
    try:
        kwargs['Def_HP'] = clamp(kwargs['Def_HP'], 1, 500)
        kwargs['Def_Helmet'] = clamp(kwargs['Def_Helmet'], 0, 500)
        kwargs['Def_Armor'] = clamp(kwargs['Def_Armor'], 0, 500)
    except KeyError:
        pass
    try:
        kwargs['HitChance'] = clamp(kwargs['HitChance'], 5, 95)
    except KeyError:
        pass
    try:
        kwargs['Trials'] = clamp(kwargs['Trials'], 2, 10000)
    except KeyError:
        kwargs['Trials'] = 1000
    return kwargs

def run_battery(battery: list, query: dict):
    output = defaultdict(lambda: '')
    output['ChartData'] = defaultdict(lambda: {})
    for v in battery:
        kwargs = {**query, **v}
        result = BBCalc.main(**kwargs)
        for field, value in result.items():
            if field == 'ChartData':
                for chart, data in value.items():
                    # for dataPoint in data:
                    #     dataPoint['y'] /= len(battery)
                    output['ChartData'][chart][v['name']] = data
            else:
                output[field] += f"{v['name']}: {value}\n"
    output['ChartData'] = dict(output['ChartData'])
    return dict(output)

def index(request):
    basedir = pathlib.Path(__file__).parent.parent.resolve()
    with open(basedir / 'static' / 'atkPresets.json', 'r') as f:
        atkPresetJSON = json.load(f)
    with open(basedir / 'static' / 'defPresets.json', 'r') as f:
        defPresetJSON = json.load(f)
    with open(basedir / 'static' / 'chartMeta.json', 'r') as f:
        chartMetaJSON = json.load(f)
    if request.GET:
        parsedRequest = parse(request.GET)
        trialsCap = 1000
        if request.GET['AtkPreset'] == '1Handers':
            with open(basedir / 'static' / '1handers.json', 'r') as f:
                parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results = run_battery(json.load(f), parsedRequest)
        elif request.GET['AtkPreset'] == '2Handers':
            with open(basedir / 'static' / '2handers.json', 'r') as f:
                parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results = run_battery(json.load(f), parsedRequest)
        elif request.GET['AtkPreset'] == 'AllAtkPresets':
            parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
            chartType = 'splineArea'
            results = run_battery(atkPresetJSON.values(), parsedRequest)
        elif request.GET['DefPreset'] == 'NimbleBattery':
            with open(basedir / 'static' / 'nimble.json', 'r') as f:
                parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
                chartType = 'stackedColumn'
                results = run_battery(json.load(f), parsedRequest)
        elif request.GET['DefPreset'] == 'AllDefPresets':
            parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
            chartType = 'stackedColumn'
            results = run_battery(defPresetJSON.values(), parsedRequest)
        else:
            results = BBCalc.main(**parsedRequest)
            chartType = 'default'
        context = {
            'atkPresetJSON': atkPresetJSON,
            'defPresetJSON': defPresetJSON,
            'chartMetaJSON': chartMetaJSON,
            'blank': False,
            'chartType': chartType,
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
        print('Results')
        print(results.keys())
        print(results['ChartData'])
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
        context = {
            'atkPresetJSON': atkPresetJSON,
            'defPresetJSON': defPresetJSON,
            'blank': True,
            'DataReturns': ['DeathMean', 'DeathStDev', 'DeathPercent', 'InjuryMean', 'HeavyInjuryMean'],
        }
    #return HttpResponseBadRequest('<p>Calculation computation time exceeded 60 seconds</p>')
    return render(request, 'index.html', context)
