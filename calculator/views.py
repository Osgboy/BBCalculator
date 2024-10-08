from django.shortcuts import render
# from django.http import HttpResponse, HttpResponseBadRequest
# from .models import Progress
from collections import defaultdict
from . import BBCalc
import json
import pathlib
# import pdb


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
            elif v[0] not in ('None', 'pID'): # not really necessary
                for arg in v:
                    kwargs[arg] = True
        except Exception:
            pass

    # Validation
    def clamp(x: int, lowerBound: int, upperBound: int) -> int:
        return max(min(x, upperBound), lowerBound)

    if 'Mind' in kwargs:
        kwargs['Mind'] = clamp(kwargs['Mind'], 1, 999)
    if 'Maxd' in kwargs:
        kwargs['Maxd'] = clamp(kwargs['Maxd'], kwargs['Mind'], 999)
    if 'Ignore' in kwargs:
        kwargs['Ignore'] = clamp(kwargs['Ignore'], 0, 999)
    if 'ArmorMod' in kwargs:
        kwargs['ArmorMod'] = clamp(kwargs['ArmorMod'], 1, 999)
    if 'Def_HP' in kwargs:
        kwargs['Def_HP'] = clamp(kwargs['Def_HP'], 1, 500)
    if 'Def_Helmet' in kwargs:
        kwargs['Def_Helmet'] = clamp(kwargs['Def_Helmet'], 0, 500)
    if 'Def_Armor' in kwargs:
        kwargs['Def_Armor'] = clamp(kwargs['Def_Armor'], 0, 500)
    if 'HitChance' in kwargs:
        kwargs['HitChance'] = clamp(kwargs['HitChance'], 5, 95)
    if 'Trials' in kwargs:
        kwargs['Trials'] = clamp(kwargs['Trials'], 2, 10000)
    else:
        kwargs['Trials'] = 1000

    return kwargs


def run_battery(battery: list, query: dict):
    # print(f"Progress ID: {p.id}")
    output = defaultdict(lambda: '')
    output['ChartData'] = defaultdict(lambda: {})
    exceptions = []
    # p.max_progress = len(battery)
    # p.save()
    for v in battery:
        kwargs = {**query, **v}
        try:
            result = BBCalc.main(**kwargs)
            for field, value in result.items():
                if field == 'ChartData':
                    for chart, data in value.items():
                        # for dataPoint in data:
                        #     dataPoint['y'] /= len(battery)
                        output['ChartData'][chart][v['name']] = data
                else:
                    output[field] += f"{v['name']}: {value}\n"
        except Exception as e:
            exceptions.append(f"{v['name']}: {e}")
        # p.progress += 1
        # p.save()
    output['ChartData'] = dict(output['ChartData'])
    return dict(output), '\n'.join(exceptions)


def index(request):
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     pID = int(request.GET['pID'])
    #     p = Progress.objects.get(id=pID)
    #     progressState = {
    #         'progress': p.progress,
    #         'max_progress': p.max_progress
    #     }
    #     print(f'Task: {pID} with progress of {p.progress}/{p.max_progress}')
    #     return HttpResponse(json.dumps(progressState), content_type='application/json')
    basedir = pathlib.Path(__file__).parent.parent.resolve()
    with open(basedir / 'static' / 'atkPresets.json', 'r') as f:
        atkPresetJSON = json.load(f)
    with open(basedir / 'static' / 'defPresets.json', 'r') as f:
        defPresetJSON = json.load(f)
    with open(basedir / 'static' / 'chartMeta.json', 'r') as f:
        chartMetaJSON = json.load(f)
    # p = Progress.objects.create(progress=0, max_progress=100)
    if request.GET:
        # pID = request.GET['pID']
        # pOld = Progress.objects.get(id=pID)
        parsedRequest = parse(request.GET)
        trialsCap = 1000
        if request.GET['AtkPreset'] == '1Handers':
            with open(basedir / 'static' / '1handers.json', 'r') as f:
                parsedRequest['Trials'] = min(
                    trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results, calcException = run_battery(json.load(f), parsedRequest)
        elif request.GET['AtkPreset'] == '2Handers':
            with open(basedir / 'static' / '2handers.json', 'r') as f:
                parsedRequest['Trials'] = min(
                    trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results, calcException = run_battery(json.load(f), parsedRequest)
        elif request.GET['AtkPreset'] == 'AllAtkPresets':
            parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
            chartType = 'splineArea'
            results, calcException = run_battery(atkPresetJSON.values(), parsedRequest)
        elif request.GET['DefPreset'] == 'NimbleBattery':
            with open(basedir / 'static' / 'nimble.json', 'r') as f:
                parsedRequest['Trials'] = min(
                    trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results, calcException = run_battery(json.load(f), parsedRequest)
        elif request.GET['DefPreset'] == 'HPBattery':
            with open(basedir / 'static' / 'hp.json', 'r') as f:
                parsedRequest['Trials'] = min(
                    trialsCap, parsedRequest['Trials'])
                chartType = 'splineArea'
                results, calcException = run_battery(json.load(f), parsedRequest)
        elif request.GET['DefPreset'] == 'AllDefPresets':
            parsedRequest['Trials'] = min(trialsCap, parsedRequest['Trials'])
            chartType = 'stackedColumn'
            results, calcException = run_battery(defPresetJSON.values(), parsedRequest)
        else:
            try:
                results = BBCalc.main(**parsedRequest)
                calcException = None
                print('Results')
                print(results.keys())
            except Exception as e:
                results = None
                calcException = str(e)
                print('Calculator Error!')
                print(calcException)
            chartType = 'default'
        context = {
            'atkPresetJSON': atkPresetJSON,
            'defPresetJSON': defPresetJSON,
            'chartMetaJSON': chartMetaJSON,
            'blank': False,
            'chartType': chartType,
            'results': results,
            'exception': calcException,
            # 'pID': p.id,
            'request': request.GET,
            'AtkWeapon': request.GET.getlist('AtkWeapon'),
            'AtkPerks': request.GET.getlist('AtkPerks'),
            'AtkTraits': request.GET.getlist('AtkTraits'),
            'AtkInjuries': request.GET.getlist('AtkInjuries'),
            'AtkStatus': request.GET.getlist('AtkStatus'),
            'DefPerks': request.GET.getlist('DefPerks'),
            'DefTraits': request.GET.getlist('DefTraits'),
            'IjirokHeal': request.GET.getlist('IjirokHeal'),
            'IjirokTurnHeal': request.GET.getlist('IjirokTurnHeal'),
            'DataReturns': request.GET.getlist('DataReturns'),
        }
        print('Context')
        for k, v in context['request'].lists():
            print(f"{k}: {v}")
        print('-----------------------------------')
    else:
        context = {
            'atkPresetJSON': atkPresetJSON,
            'defPresetJSON': defPresetJSON,
            'blank': True,
            # 'pID': p.id,
            'DataReturns': ['DeathMean', 'DeathStDev', 'DeathPercent', 'InjuryMean'],
        }
        # print(context['pID'])
    # return HttpResponseBadRequest('<h1>Calculation computation time exceeded 30 seconds</h1>')
    return render(request, 'index.html', context)
