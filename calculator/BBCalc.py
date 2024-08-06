#Dependencies:
import random
import statistics
import collections
import math
# import sys

#Battle Brothers Damage Calculator Version 1.6.4:
#Welcome. Modify the below values as necessary until you reach the line ----- break.
#The calculator expects you to make smart decisions, such as not giving Xbow Mastery to a Hammer. 
#Written in Python 3.7, earlier versions of Python 3 should work, but Python 2 will not.
#If you wish to cancel an ongoing calculation, use ctrl + c.

#Attacker and Defender presets are provided further down.
#If you wish to use an attacker preset, skip the sections related to attacker settings and go to the attacker preset section.
#If you wish to use a defender preset, skip the sections related to defender settings and go to the defender preset section.

def main(
Trials = 10000, #Number of trials to run through. More trials leads to more accurate results but longer compute times.

#Data Returns: Set these values to 1 if you want more data returned, and 0 if you want less data returned.
#Note: If injuries/morale do not occur because defender is Undead then they will not display even if checked here.
#Note: Morale is a lot more dynamic in game than I can represent in a 1v1 sandbox. Please keep that in mind when looking at morale related data.
DeathMean = False,          #Returns the average number of hits until death.
DeathStDev = False,         #Returns standard deviation of hits until death.
DeathPercent = False,       #Returns % chance of death by each hit.
InjuryMean = False,         #Returns average number of hits until first injury.
InjuryPercent = False,      #Returns % chance of first injury by each hit.
HeavyInjuryMean = False,    #Returns average number of hits until chance of first heavy injury (heavy injuries are not guaranteed even when threshold is met).
HeavyInjuryPercent = False, #Returns % chance of first heavy injury chance by each hit.
MoraleChecksTotal = False,  #Returns the total number of morale checks before death.
MoraleMean = False,         #Returns average number of hits until first morale check.
MoralePercent = False,      #Returns % chance of first morale check by each hit.
MoraleDropsMean = False,    #Returns average number of hits to drop morale to each morale level.
MoraleDropsPercent = False, #Returns % chance of dropping morale to each morale level by each hit.

#Hit Chance: Use a whole number - 50% hit chance put "50" rather than .5
HitChance = None, #Not enabled by default

#Attacker Stats: #Example is 2h mace, follow that formatting. If you wish to use a attacker Preset, then skip this section.
Mind = 75,        #Mind = 75
Maxd = 95,        #Maxd = 95
Headchance = 25,  #Headchance = 25
Ignore = 50,      #Ignore = 50
ArmorMod = 125,   #ArmorMod = 125
Atk_Resolve = 50,        #Only used if Fearsome is selected. 20% of (Resolve -10) is applied as a penalty to defender Resolve during morale checks.

#Defender Stats: #Note: If you wish to use a defender Preset, skip the defender sections and check the Preset section instead.
Def_HP = 100,
Def_Helmet = 120,
Def_Armor = 95, 
Fatigue = -15,           #Fatigue value only effects Nimble.
Def_Resolve = 70,        #Used only if morale drop data returns are enabled.

#DEFENDER FLAGS: Set these values to 1 if they apply and 0 otherwise. If you select a Preset then leave these on 0.
#Perks:
NineLives = False,
Resilient = False,           #Reduces Bleeding duration.
SteelBrow = False,
Nimble = False,              #Will return Nimble% in the output.
Forge = False,               #Will return expected bonus armor derived from Forge in the output.
Indomitable = False,
#Attachments: Note: Only 1 attachment should be selected.
#IMPORTANT: Attachments will automatically add armor or subtract Fatigue. Use the base armor/Fatigue values in the Defender Stats section or else you will double dip the attachment.
Wolf_Hyena = False,          #+15 armor.
LindwurmCloak = False,       #+60 armor, -3 Fatigue.
AdFurPad = False,            #Additional Fur Padding. 33% reduced armor ignoring damage. -2 Fatigue.
Boneplate = False,           #Absorbs first body hit. -2 Fatigue.
HornPlate = False,           #Only select against melee attacks. +30 armor, 10% damage reduction.
UnholdFurCloak = False,      #Only select against range attacks. +10 armor, 20% damage reduction.
SerpentSkin = False,         #Only select in Handgonne tests. +30 armor, -2 Fatigue, 33% damage reduction.
#Light Padding Replacement -- Modify the Fatigue value directly if you wish to apply this. Has no effect except for Nimble.
#Traits:
Ironjaw = False,             #Reduces injury susceptibility.
GloriousEndurance = False,   #The Bear's unique trait. Reduces damage by 5% each time you are hit, up to a 25% max reduction.

#ATTACKER FLAGS: Set these values to 1 if they apply and 0 otherwise. If you select a Preset then leave these on 0.
#Weapons:
DoubleGrip = False,          #Only 1Handers are valid for DoubleGrip. Dagger Puncture tests should not be given DoubleGrip.
TwoHander20 = False,         #Damage +20. Applies to the single target 2Hander attacks Cudgel (Mace), Pound (Flail), Smite (Hammer), Overhead Strike (Long/GreatSword).
FlailLash = False,           #Gaurantees headshot. Also apply to 3Head Hail special.
Flail3Head = False,          #3Head Flail. Returns number of swings rather than number of hits.
Flail2HPound = False,        #Ignore +10% on body hits and +20% on headshots. Applies to 2H Flail Pound attack. Apply the +20 damage from Pound using the TwoHander20 switch.
FlailMastery = False,        #Flail Mastery. Will apply an extra 10% armor ignore on headshots for Pound. Does nothing unless Flail2HPound is set.
Hammer10 = False,            #Guarantees at least 10 hp damage, applies to 1H Hammer and Polehammer.
DestroyArmor = False,        #Will use Destroy Armor once and then switch to normal attacks.
DestroyArmorMastery = False, #Hammer Mastery. Will use Destroy Armor once and then switch to normal attacks.
DestroyArmorTwice = False,   #Uses Destroy Armor two times instead of 1. Does nothing unless DestroyArmor or DestroyArmorMastery are set.
Axe1H = False,               #Applies bonus damage to Headshots. Gets negated by SteelBrow.
SplitMan = False,            #Applies to single target 2HAxe except for Longaxe.
AoE2HAxe = False,            #Applies to Round Swing and Split in Two (Bardiche), reduces Ignore by 10%.
CleaverBleed = False,        #5 bleed damage per bleed tick.
CleaverMastery = False,      #10 bleed damage per bleed tick. 
Decapitate = False,          #Cleaver Decapitate. Will use Decapitate for all attacks.
SmartDecap50 = False,        #Switches from normal Cleaver attacks to Decapitate once opposing hp is <= 50%.
SmartDecap33 = False,        #Switches from normal Cleaver attacks to Decapitate once opposing hp is <= 33.33%.
Shamshir = False,            #Shamshir special Gash, acts like Crippling Strikes.
ShamshirMastery = False,     #Sword Mastery with Gash, 50% reduction to injury threshold instead of 33%.
Sword2HSplit = False,        #Ignore +5%. Applies to Greatsword Split attack. Does not apply to Overhead or Swing.
Puncture = False,            #Dagger Puncture. Do not apply Double Grip
Deathblow = False,           #Qatal special. Ignore +20%. Damage x1.33. Assumes target is always setup for Deathblow value in calculation.
Spearwall = False,           #Warning: May take a long time to compute against durable targets, considering lowering number of trials. 
AimedShot = False,           #HP Damage +10% for Bows. +5% Armor Ignore.
XbowMastery = False,         #Ignore +20%.
R2Throw = False,             #Throwing Mastery for 1 or 2 Range.
R3Throw = False,             #Throwing Mastery for 3 Range.
Scatter = False,             #Ranged attacks that hit an unintended target deal 75% damage.
Pierce = False,              #-50% health damage for Daggers, Spears, and Pikes against Ancient Dead, Alps, and Ifrits.
DogBite = False,             #-66% health damage for Dog bites against Alps.
XbowOrSling = False,         #-66% health damage for Xbows and Slings against Ancient Dead, Alps, and Ifrits.
Handgonne = False,           #-66% health damage for Handgonnes against Ancient Dead, -50% against Alps, and -75% against Ifrits.
Javelin = False,             #-75% health damage for Javelins against Ancient Dead, Alps, and Ifrits.
Ignite = False,              #-75% health damage for Ignite against Ancient Dead, -90% against Ifrits.
Arrow = False,               #-90% health damage for Bows against Ancient Dead, Alps, and Ifrits.
#Perks:
FastAdaptation = False,
CripplingStrikes = False,
Executioner = False,
HeadHunter = False,          #Will carry over HH stacks between kills as happens in game.
Duelist = False,             #All Duelists should also be given DoubleGrip except for Throwing weapons.
KillingFrenzy = False,
Fearsome = False,            #Will also return # of extra Fearsome checks, which are all attacks that deal 1-14 damage. Assign Attacker Resolve below.
#Traits:
Brute = False,               #Headshot damage +15%.
Drunkard = False,            #Damage +10%.
Huge = False,                #Damage +10%.
Tiny = False,                #Damage -15%.
#Backgrounds:
Juggler = False,             #Headchance +5%.
KillerOnTheRun = False,      #Headchance +10%.
#Injuries:
BrokenArm = False,           #Damage -50%. Heavy blunt/body.
SplitShoulder = False,       #Damage -50%. Heavy cutting/body.
CutArmSinew = False,         #Damage -40%. Light cutting/body.
InjuredShoulder = False,     #Damage -25%. Light piercing/body.
#Other:
Dazed = False,               #Damage -25%. Set this if you want to simulate the attacker always being Dazed.
Distracted = False,          #Damage -35%. Set this if you want to simulate the attacker always being Distracted (applied by Nomads).
Mushrooms = False,           #Damage +25%. Set this to simulate a Mushroom enhanced brother.

#RACE FLAGS (ATTACKER): Set these values to 1 if they apply and 0 otherwise. If late game only set the second option. #If you use a Preset then leave these on 0.
Young = False,               #Damage +15%.
Berserker = False,           #Damage +20%.
BerserkerDay190 = False,     #Damage +30%.
Warrior = False,             #Damage +15%.
WarriorDay200 = False,       #Damage +25%.
Warlord = False,             #Damage +35%.
WarlordDay200 = False,       #Damage +45%.
Conqueror = False,           #Damage +35%. Monolith.
FallenBetrayer = False,      #Damage +25%. Watermill.
FallenHeroDay100 = False,    #Damage +10%.
ArmoredZombieDay100 = False, #Damage +10%.
BarbKing = False,            #Damage +20%.
HedgeKnight = False,         #Damage +20%.
BrigandLeader = False,       #Armor Damage + 20%.
Ambusher = False,            #Ignore * 1.25
AmbusherDay180 = False,      #Ignore * 1.35
Skirmisher = False,          #Ignore * 1.25
Overseer = False,            #Ignore * 1.1
Wolfrider = False,           #Ignore * 1.25
MasterArcher = False,        #Ignore * 1.25
FrenziedDirewolf = False,    #Damage +20%.
UnholdDay90 = False,         #Damage +10%.
LindwurmDay170 = False,      #Damage +10%.

#RACE FLAGS (DEFENDER): Set these values to 1 if they apply and 0 otherwise.
Zombie = False,              #Immunity to Injury, Bleeding, Poison, and Morale.
Savant = False,              #Immunity to Injury and Morale.
Skeleton = False,            #Take only 10% damage from bows, 25% damage from javelins and fire lances' ignite, 33% damage from crossbows, slings and handgonnes, 50% from other piercing attacks.
Alp = False,                 #Take only 10% damage from bows, 25% damage from javelins, 33% damage from crossbows, slings and dog bites, 50% from other piercing attacks and handgonnes. 
Ifrit = False,               #Takes only 10% damage from bows and fire lances' ignite, 25% damage from javelins and handgonne, 33% damage from crossbows and slings, 50% damage from other piercing weapons.
PossessedUndead = False,     #25% damage reduction. Necromancer buff.
FallenBetrayerD = False,     #25% armor damage reduction for Watermill Betrayers.

#Attacker Preset: Set these values to 1 if you wish to use a attacker preset, and 0 otherwise.
#A preset will atutomatically set attacker stats and attacker perks.
#Attacker presets do not include the late game day related buffs that some races get.
#Does not disable perks that shouldn't be active. For example, don't activate Duelist and then check the Chosen Preset.
# APreAncientSword = False,    #Ancient Dead: 38-43, 20% Ignore, 80% Armor, Fearsome.
# APreBladedPike = False,      #Ancient Dead: 55-80, 30% Ignore, 125% Armor, 30% Head, Fearsome.
# APreWarscytheAoE = False,    #Ancient Dead: 55-80, 25% Ignore, 104% Armor, Fearsome.
# APreCryptCleaver = False,    #Ancient Dead: 60-80, 25% Ignore, 120% Armor, Fearsome, Cleaver Mastery.
# APreKhopesh = False,         #Necrosavant: 35-55, 25% Ignore, 120% Armor, HeadHunter, Crippling, Double Grip, CleaverBleed.
# APreFHGreatAxe = False,      #Fallen Hero: 80-100, 40 %Ignore, 150% Armor, Fearsome, Split Man.
# APreBerserkChain = False,    #Orc Berserker: 50-100, 30% Ignore, 125% Armor, 40% Head, TwoHander20, Flail2HPound, FlailMastery, Berserker.
# APreHeadSplitter = False,    #Orc Young/Warrior: 35-65, 30% Ignore, 130% Armor, 1HAxe, Warrior.
# APreHeadChopper = False,     #Orc Young/Warrior: 40-70, 25% Ignore, 110% Armor, Cleaver Mastery, Warrior.
# APreMansplitter = False,     #Orc Warlord: 90-120, 40% Ignore, 160% Armor, Split Man, Fearsome, Warlord.
# APreReinBoondock = False,    #Goblin Ambusher: 30-50, 35% Ignore, 60% Armor, Ambusher.
# APreSpikedImpaler = False,   #Goblin Overseer: 50-70, 50% Ignore, 75% Armor, Overseer, Xbow Mastery.
# APre2HSpikedMace = False,    #Chosen: 50-70, 60% Ignore, 115% Armor, Crippling, Executioner, TwoHander20.
# APre2HSkullHammer = False,   #Chosen: 45-65, 60% Ignore, 180% Armor, Crippling, Executioner, TwoHander20.
# APreHeavyRustyAxe = False,   #Chosen: 75-90, 50% Ignore, 150% Armor, Crippling, Executioner, Split Man.
# APreRustyWarblade = False,   #Chosen: 60-80, 35% Ignore, 110% Armor, Crippling, Executioner, Cleaver Mastery.
# APreBillhook = False,        #Billman: 55-85, 30% Ignore, 140% Armor, 30% Head.
# APreHeavyXbow = False,       #Arbalester: 50-70, 50% Ignore, 75% Armor, XbowMastery.
# APreFightingAxe = False,     #Knight: 35-55, 30% Ignore, 130% Armor, 1HAxe, Crippling, Executioner.
# APreWingedMace = False,      #Sergeant: 35-55, 40% Ignore, 110% Armor, Duelist, Double Grip
# APreGreatsword = False,      #Zweihander: 85-100, 25% Ignore, 100% Armor, 30% Head, TwoHander20.
# APreFlailDGrip = False,      #Raider: 25-55, 30% Ignore, 100% Armor, 35% Head, Double Grip, Executioner.
# APreLongAxe = False,         #Raider: 70-95, 30% Ignore, 110% Armor, 30% Head, Executioner. 
# APreMedXbow = False,         #Marksman: 40-60, 50% Ignore, 70% Armor, Xbow Mastery.
# APreNobleSword = False,      #Swordmaster: 45-50, 20% Ignore, 85% Armor, Duelist, Double Grip, Crippling, Executioner.
# APreWarbow = False,          #Master Archer: 50-70, 35% Ignore, 65% Armor, Crippling, Executioner, HeadHunter, Master Archer. 
# APrePoleMace = False,        #Conscript: 60-75, 40% Ignore, 120% Armor, 30% Head.
# APreHandgonne = False,       #Gunner: 35-75, 25% Ignore, 90% Armor, Fearsome.
# APre2HScimitar = False,      #Officer: 65-85, 25% Ignore, 110% Armor, Crippling, Executioner, Cleaver Mastery.
# APreQatal = False,           #Assassin: 30-45, 20% Ignore, 70% Armor, Duelist, Double Grip, Executioner.
# APreFDirewolf = False,       #Frenzied Direwolf: 30-50, 20% Ignore, 70% Armor, Executioner, Frenzied Direwolf.
# APreNachTier3 = False,       #Tier 3 Nachzehrer: 55-80, 10% Ignore, 75% Armor.
# APreLindwurm = False,        #Lindwurm Head: 80-140, 35% Ignore, 140% Armor, Fearsome.
# APreUnhold = False,          #Unhold: 40-80, 40% Ignore, 80% Armor, Crippling.
# APreSchrat = False,          #Schrat: 70-100, 50% Ignore, 80% Armor, Crippling.

# #Defender Preset: Set these values to 1 if you wish to use a defender preset, and 0 otherwise.
# #A preset will automatically set defender stats and defender perks.
# #Does not disable perks that shouldn't be active. For example, don't activate Nimble and then check the Orc Warrior Preset.
# DPreNimbleBro = False,       # 120hp, 120/95, Nimble (A generic Nimble line with just Nimble).
# DPreNimbleBroBP = False,     # 120hp, 120/80 Nimble, Bone Plates.
# DPreForgeBro = False,        # 80hp, 300/300, Forge (A generic Forge line with just Forge).
# DPreForgeBroAFP = False,     # 80hp, 300/300, Forge, Additional Fur Padding.
# DPreAncientLegion = False,   # 55hp, 130/135, Forge, SteelBrow, Undead. (Manually apply Skeleton flag if necessary).
# DPreHonorGuard = False,      # 65hp, 180/210, Forge, SteelBrow, Undead. (Manually apply Skeleton flag if necessary).
# DPreArmGangerHeavy = False,  # 130hp, 140/115, Forge, Undead.
# DPreFHeroHeavy = False,      # 180hp, 255/260, Forge, Undead.
# DPreYoungHeavy = False,      # 125hp, 120/120.
# DPreBerserkerHeavy = False,  # 250hp, 120/110, Resilient.
# DPreWarriorLight = False,    # 200hp, 240/280, Resilient.
# DPreWarriorHeavy = False,    # 200hp, 360/400, Resilient.
# DPreWarlord = False,         # 300hp, 500/500.
# DPreSkirmisherHeavy = False, # 40hp, 90/90.
# DPreAmbusher = False,        # 40hp, 25/35.
# DPreShaman = False,          # 70hp, 35/45.
# DPreOverseer = False,        # 70hp, 120/180.
# DPreReaverHeavy = False,     # 80hp, 145/95, Resilient.
# DPreChosenLight = False,     # 130hp, 145/140, Forge, Resilient.
# DPreChosenHeavy = False,     # 130hp, 190/230, Forge, Resilient.
# DPreBarbKing = False,        # 150hp, 250/270, Forge, Resilient.
# DPreBeastmaster = False,     # 70hp, 130/95, Resilient.
# DPreFootmanHeavy = False,    # 70hp, 215/150, Forge.
# DPreBillman = False,         # 70hp, 80/130, Forge.
# DPreArbalester = False,      # 60hp, 80/65.
# DPreBannerHeavy = False,     # 80hp, 215/150, SteelBrow.
# DPreKnight = False,          # 125hp, 300/300, Forge. 
# DPreSergeant = False,        # 100hp, 0/150, Nimble, SteelBrow. (-18 Fat)
# DPreZweiHeavy = False,       # 90hp, 160/240, Forge, SteelBrow. 
# DPreRaiderHeavy = False,     # 70hp, 140/115.
# DPreMarkman = False,         # 60hp, 45/70.
# DPreLeaderHeavy = False,     # 100hp, 250/230, NineLives.
# DPreMercenaryHeavy = False,  # 90hp, 230/260, Forge.
# DPreMercRange = False,       # 65hp, 115/115, Nimble. (-18 Fat)
# DPreHedgeKnight = False,     # 150hp, 300/300, Forge, Resilient.
# DPreSwordmaster = False,     # 70hp, 70/115, Nimble, SteelBrow. (-15 Fat)
# DPreMasterArcher = False,    # 80hp, 30/115, Nimble, SteelBrow. (-12 Fat)
# DPreOutlawHeavy = False,     # 75hp, 125/105.
# DPreConscript = False,       # 55hp, 105/110, Nimble. (-16 Fat)
# DPreOfficer = False,         # 100hp, 290/290, Forge.
# DPreAssassinHeavy = False,   # 80hp, 140/120, Nimble. (-15 Fat)

**kwargs
):
# ------------------------------------------------------------------------
#IMPORTANT --- ALL BELOW FIELDS SHOULD NOT BE MODIFIED. --- IMPORTANT
#DO NOT MODIFY BELOW FIELDS UNLESS YOU KNOW WHAT YOU ARE DOING.

#Attacker presets:
    # if APreAncientSword:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve = 38, 43, 25, 20, 80, True, 80
    # if APreBladedPike:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve = 55, 80, 30, 30, 125, True, 80
    # if APreWarscytheAoE:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve = 55, 80, 25, 25, 104, True, 100
    # if APreCryptCleaver: 
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve, CleaverMastery = 60, 80, 25, 25, 120, True, 100, True
    # if APreKhopesh:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, HeadHunter, CripplingStrikes, DoubleGrip, CleaverBleed = 35, 55, 25, 25, 120, True, True, True, True
    # if APreFHGreatAxe:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve, SplitMan = 80, 100, 25, 40, 150, True, 100, True
    # if APreBerserkChain:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, TwoHander20, Flail2HPound, FlailMastery, Berserker = 50, 100, 40, 30, 125, True, True, True, True
    # if APreHeadSplitter:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Axe1H, Warrior = 35, 65, 25, 30, 130, True, True
    # if APreHeadChopper:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CleaverMastery, Warrior = 40, 70, 25, 25, 110, True, True
    # if APreMansplitter:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, SplitMan, Fearsome, Atk_Resolve, Warlord = 90, 120, 25, 40, 160, True, True, 90, True
    # if APreReinBoondock:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Ambusher = 30, 50, 25, 35, 60, True
    # if APreSpikedImpaler:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Overseer, XbowMastery = 50, 70, 25, 50, 75, True, True
    # if APre2HSpikedMace:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes, Executioner, TwoHander20 = 50, 70, 25, 60, 115, True, True, True
    # if APre2HSkullHammer:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes, Executioner, TwoHander20 = 45, 65, 25, 60, 180, True, True, True
    # if APreHeavyRustyAxe:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes, Executioner, SplitMan = 75, 90, 25, 50, 150, True, True, True
    # if APreRustyWarblade:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes, Executioner, CleaverMastery = 60, 80, 25, 35, 110, True, True, True
    # if APreBillhook:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod = 55, 85, 30, 30, 140
    # if APreHeavyXbow:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, XbowMastery = 50, 70, 25, 50, 75, True
    # if APreFightingAxe:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Axe1H, CripplingStrikes, Executioner = 35, 55, 25, 30, 130, True, True, True
    # if APreWingedMace:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Duelist, DoubleGrip = 35, 55, 25, 40, 110, True, True
    # if APreGreatsword:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, TwoHander20 = 85, 100, 30, 25, 100, True
    # if APreFlailDGrip:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Executioner, DoubleGrip = 25, 55, 35, 30, 100, True, True
    # if APreLongAxe:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Executioner = 70, 95, 30, 30, 110, True
    # if APreMedXbow:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, XbowMastery = 40, 60, 25, 50, 70, True
    # if APreNobleSword:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Duelist, DoubleGrip, CripplingStrikes, Executioner = 45, 50, 25, 20, 85, True, True, True, True
    # if APreWarbow:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes, Executioner, MasterArcher, HeadHunter = 50, 70, 25, 35, 65, True, True, True, True
    # if APrePoleMace:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod = 60, 75, 30, 40, 120
    # if APreHandgonne:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve = 35, 75, 25, 25, 90, True, 70
    # if APre2HScimitar:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CleaverMastery, CripplingStrikes, Executioner = 65, 85, 25, 25, 110, True, True, True
    # if APreQatal:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Duelist, DoubleGrip, Executioner = 30, 45, 25, 20, 70, True, True, True
    # if APreFDirewolf:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Executioner, FrenziedDirewolf = 30, 50, 25, 20, 70, True, True
    # if APreNachTier3:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod = 55, 80, 25, 10, 75
    # if APreLindwurm:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, Fearsome, Atk_Resolve = 80, 140, 25, 35, 140, True, 180
    # if APreUnhold:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes = 40, 80, 25, 40, 80, True
    # if APreSchrat:
    #     Mind, Maxd, Headchance, Ignore, ArmorMod, CripplingStrikes = 70, 100, 25, 50, 80, True

    # #Defender presets:
    # if DPreNimbleBro:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble = 120, 120, 95, 50, -15, True
    # if DPreNimbleBroBP:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble, Boneplate = 120, 120, 80, 50, -13, True, True
    # if DPreForgeBro:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 80, 300, 300, 50, True
    # if DPreForgeBroAFP:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, AdFurPad = 80, 300, 300, 50, True, True
    # if DPreAncientLegion:
    #     Def_HP, Def_Helmet, Def_Armor, Forge, SteelBrow, Undead = 55, 130, 135, True, True, True
    # if DPreHonorGuard:
    #     Def_HP, Def_Helmet, Def_Armor, Forge, SteelBrow, Undead = 65, 180, 210, True, True, True
    # if DPreArmGangerHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Forge, Undead = 130, 140, 115, True, True
    # if DPreFHeroHeavy ==  1:
    #     Def_HP, Def_Helmet, Def_Armor, Forge, Undead = 180, 255, 260, True, True
    # if DPreYoungHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 125, 120, 120, 65
    # if DPreBerserkerHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Resilient = 250, 120, 110, 90, True
    # if DPreWarriorLight:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Resilient = 200, 240, 280, 75, True
    # if DPreWarriorHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Resilient = 200, 360, 400, 75, True
    # if DPreWarlord:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 300, 500, 500, 90
    # if DPreSkirmisherHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 40, 90, 90, 55
    # if DPreAmbusher:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 40, 25, 35, 45
    # if DPreShaman:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 70, 35, 45, 70
    # if DPreOverseer:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 70, 120, 180, 70
    # if DPreReaverHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Resilient = 80, 145, 95, 80, True
    # if DPreChosenLight:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, Resilient = 130, 145, 140, 90, True, True
    # if DPreChosenHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, Resilient = 130, 190, 230, 90, True, True
    # if DPreBarbKing:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, Resilient = 150, 250, 270, 110, True, True
    # if DPreBeastmaster:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Resilient = 70, 130, 95, 90, True
    # if DPreFootmanHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 70, 215, 150, 60,  True
    # if DPreBillman:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 70, 80, 130, 60, True
    # if DPreArbalester:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 60, 80, 65, 60
    # if DPreBannerHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, SteelBrow = 80, 215, 150, 80, True
    # if DPreKnight:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 125, 300, 300, 90, True
    # if DPreSergeant:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble, SteelBrow = 100, 0, 150, 80, -18, True, True
    # if DPreZweiHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, SteelBrow = 90, 160, 240, 70, True, True
    # if DPreRaiderHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 70, 140, 115, 55
    # if DPreMarkman:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 60, 45, 70, 50
    # if DPreLeaderHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, NineLives = 100, 250, 230, 70, True
    # if DPreMercenaryHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 90, 230, 260, 70, True
    # if DPreMercRange:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble = 65, 115, 115, 70, -18, True
    # if DPreHedgeKnight:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge, Resilient = 150, 300, 300, 90, True, True
    # if DPreSwordmaster:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble, SteelBrow = 70, 70, 115, 90, -15, True, True
    # if DPreMasterArcher:   
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble, SteelBrow = 80, 30, 115, 70, -12, True, True
    # if DPreOutlawHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve = 75, 125, 105, 60
    # if DPreConscript:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble = 55, 105, 110, 70, -16, True
    # if DPreOfficer:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Forge = 100, 290, 290, 80, True
    # if DPreAssassinHeavy:
    #     Def_HP, Def_Helmet, Def_Armor, Def_Resolve, Fatigue, Nimble = 80, 140, 120, 85, -15, True

    #Error Handling
    # if Mind <= 0 or Maxd <= 0:
    #     sys.exit("Damage must be positive.")
    # if Mind > Maxd:
    #     sys.exit("Min damage must be <= Max damage.")
    # if Ignore < 0:
    #     sys.exit("Ignore must be positive.")
    # if ArmorMod <= 0:
    #     sys.exit("Armor damage must be positive.")
    # if Def_HP <= 0 or Def_Helmet < 0 or Def_Armor < 0:
    #     sys.exit("Hp and armor must be positive or 0.")
    # if Def_HP > 500 or Def_Helmet > 500 or Def_Armor > 500:
    #     sys.exit("Hp and armor must be <= 500.")
    # if Trials < 2:
    #     sys.exit("Trials must be >= 2.")

    #Base damage modifiers:
    if TwoHander20:
        Mind += 20
        Maxd += 20

    #Headchance modifiers:
    if Juggler:
        Headchance += 5
    if KillerOnTheRun:
        Headchance += 10
    if FlailLash:
        Headchance = 100
    if Puncture:
        Headchance = 0
    Headshotchance = Headchance

    #Ignore modifiers:
    Ignore = Ignore/100
    if Flail2HPound:
        Flail2HBodyshot = Ignore + .1
        Flail2HHeadshot = Ignore + .2
        if FlailMastery:
            Flail2HHeadshot += .1
    if Sword2HSplit:
        Ignore += .05
    if Deathblow:
        Ignore += .2
    if AimedShot:
        Ignore += .05
    if XbowMastery:
        Ignore += .2
    if Ambusher:
        Ignore *= 1.25
    elif AmbusherDay180:
        Ignore *= 1.35
    if Skirmisher:
        Ignore *= 1.25
    if Overseer:
        Ignore *= 1.1
    if Wolfrider:
        Ignore *= 1.25
    if MasterArcher:
        Ignore *= 1.25
    if Duelist:
        Ignore += .25
    if AoE2HAxe:
        Ignore -= .1
    if Ignore > 1:
        Ignore = 1

    #Armor damage modifiers:
    ArmorMod = ArmorMod/100
    if BrigandLeader:
        ArmorMod += .2

    #Fatigue force negative:
    if Fatigue > 0 and Nimble:
        Fatigue *= -1

    #Attachment modifiers:
    AttachMod = 1
    if UnholdFurCloak:
        AttachMod = .8
        Def_Armor += 10
    if HornPlate:
        AttachMod = .9
        Def_Armor += 30
    if SerpentSkin:
        AttachMod = .66
        Def_Armor += 30
        Fatigue -= 2

    if Wolf_Hyena:
        Def_Armor += 15
    if LindwurmCloak:
        Def_Armor += 60
        Fatigue -= 3

    if AdFurPad:
        AdFurPadMod = .66
        Fatigue -= 2
    else: 
        AdFurPadMod = 1

    if Boneplate:
        Fatigue -= 2

    #Nimble calculation:
    Fatigue = min(0, Fatigue + 15)
    if Nimble:
        NimbleMod = 1.0 - 0.6 + pow(abs(Fatigue),1.23)*.01
        NimbleMod = min(1,NimbleMod)
    else:
        NimbleMod = 1

    #Headshot damage modifiers:
    HeadMod = 1.5
    if SteelBrow:
        HeadMod = 1
    else:
        if Brute:
            HeadMod += .15
        if Axe1H:
            HeadMod += .5

    #Fast Adaptation:
    FastAdMod = 0

    #HeadHunter
    HHStack = 0

    #Fearsome
    if Fearsome:
        FearsomeMod = min((Atk_Resolve - 10) / 5, 18)

    #Damage modifiers:
    DamageMod = 1
    if DoubleGrip:
        DamageMod *= 1.25
    if Flail3Head:
        DamageMod *= .33
    if Deathblow:
        DamageMod *= 1.33
    if Spearwall:
        DamageMod *= .5
    if R2Throw:
        DamageMod *= 1.3
    if R3Throw:
        DamageMod *= 1.2
    if Scatter:
        DamageMod *= .75
    if KillingFrenzy:
        DamageMod *= 1.25
    if Huge:
        DamageMod *= 1.1
    if Tiny:
        DamageMod *= .85
    if Drunkard:
        DamageMod *= 1.1
    if BrokenArm:
        DamageMod *= .5
    if SplitShoulder:
        DamageMod *= .5
    if CutArmSinew:
        DamageMod *= .6
    if InjuredShoulder:
        DamageMod *= .75
    if Dazed:
        DamageMod *= .75
    if Distracted:
        DamageMod *= .65
    if Mushrooms:
        DamageMod *= 1.25
    if Young:
        DamageMod *= 1.15
    if Berserker:
        DamageMod *= 1.2
    elif BerserkerDay190:
        DamageMod *= 1.3
    if Warrior:
        DamageMod *= 1.15
    elif WarriorDay200:
        DamageMod *= 1.25
    if Warlord:
        DamageMod *= 1.35
    elif WarlordDay200:
        DamageMod *= 1.45
    if Conqueror:
        DamageMod *= 1.35
    if FallenBetrayer:
        DamageMod *= 1.25
    if FallenHeroDay100:
        DamageMod *= 1.1
    if ArmoredZombieDay100:
        DamageMod *= 1.1
    if BarbKing:
        DamageMod *= 1.2
    if HedgeKnight:
        DamageMod *= 1.2
    if FrenziedDirewolf:
        DamageMod *= 1.2
    if UnholdDay90:
        DamageMod *= 1.1
    if LindwurmDay170:
        DamageMod *= 1.1

    if AimedShot:
        AimedShotMod = 1.1
    else:
        AimedShotMod = 1

    #Indomitable:
    if Indomitable:
        IndomMod = .5
    elif PossessedUndead: #This works just like Indom and they will never be both used together, so I put this here instead of writing a new variable.
        IndomMod = .75
    else:
        IndomMod = 1

    #Racial defense modifier:
    if Skeleton:
        if Pierce:
            RaceMod = .5
        elif XbowOrSling:
            RaceMod = 2/3
        elif Handgonne:
            RaceMod = 2/3
        elif Javelin:
            RaceMod = .25
        elif Ignite:
            RaceMod = .25
        elif Arrow:
            RaceMod = .1
        else:
            RaceMod = 1
    elif Alp:
        if Pierce:
            RaceMod = .5
        elif DogBite:
            RaceMod = 2/3
        elif XbowOrSling:
            RaceMod = 2/3
        elif Handgonne:
            RaceMod = .5
        elif Javelin:
            RaceMod = .25
        elif Arrow:
            RaceMod = .1
        else:
            RaceMod = 1
    elif Ifrit:
        if Pierce:
            RaceMod = .5
        elif XbowOrSling:
            RaceMod = 2/3
        elif Handgonne:
            RaceMod = .25
        elif Javelin:
            RaceMod = .25
        elif Ignite:
            RaceMod = .1
        elif Arrow:
            RaceMod = .1
        else:
            RaceMod = 1
    else:
        RaceMod = 1

    #Racial immunities:
    if Zombie or Savant or Skeleton or Alp or Ifrit or PossessedUndead or FallenBetrayerD:
        injuryImmune = True
    else:
        injuryImmune = False
    if Zombie or Skeleton or Alp or Ifrit or PossessedUndead or FallenBetrayerD:
        DOTImmune = True
    else:
        DOTImmune = False
    if Zombie or Savant or Skeleton or Ifrit or PossessedUndead or FallenBetrayerD:
        moraleImmune = True
    else:
        moraleImmune = False

    #Bleeding damage:
    BleedDamage = 0
    if CleaverBleed:
        BleedDamage = 5
    if CleaverMastery:
        BleedDamage = 10
    if Indomitable and BleedDamage > 0:
        BleedDamage = math.floor(BleedDamage / 2)

    #Lists for later analysis:
    hits_until_death = [] #This list will hold how many hits until death for each iteration.
    hits_until_1st_injury = [] #This list will hold how many hits until first injury for each iteration.
    hits_until_1st_heavy_injury_chance = [] #This list will hold how many hits until a chance of heavy injury for each iteration.
    hits_until_1st_morale = [] #This list will hold how many hits until first morale check for each iteration.
    Total_Morale_Checks = [] #This list will hold how many morale checks occur for each iteration.
    hits_until_wavering = [] #this list will hold how many hits until morale falls to for each iteration.
    hits_until_breaking = [] #this list will hold how many hits until morale falls to breaking for each iteration.
    hits_until_fleeing = [] #this list will hold how many hits until morale falls to fleeing for each iteration.
    NumberFearsomeProcs = [] #This list will hold number of Fearsome procs for each iteration (only displays if Fearsome is checked).
    Forge_bonus_armor = [] #This list will hold the amount of extra armor provided by Forge for each iteration (only displays if Forge is checked).
    hits_until_1st_poison = [] #This list will hold how many hits until first poisoning against Ambushers (only displays if Ambusher is checked).
    hits_until_1st_bleed = [] #This list will hold how many hits until first bleed against cleavers (only displays if CleaverBleed or CleaverMastery is checked).

    print("-----") #Added for readability. If this annoys you then remove this line.
    print(f"HP = {str(Def_HP)}, Helmet = {str(Def_Helmet)}, Armor = {str(Def_Armor)}")

    #Begin the simulation.
    for _ in range(Trials): #This will run a number of trials as set above by the trials variable.
        #Stat initialization:
        hp = Def_HP
        helmet = Def_Helmet
        body = Def_Armor   

        #Sets various flags to a default state at the start of each new trial. 
        if HeadHunter:
            Headshotchance = Headchance
        if Boneplate:
            BoneplateMod = True
        else:
            BoneplateMod = False
        if NineLives:
            NineLivesMod = True
        else:
            NineLivesMod = False
        Injury = 0                          #Tracker for when first injury occurs.
        HeavyInjuryChance = 0               #Tracker for when when first chance of heavy injury occurs.
        UseHeadShotInjuryFormula = 0        #Tracker to use headshot injury formula on headshots.
        FirstMoraleCheck = 0                #Tracker for when first morale check occurs.
        MoraleChecks = 0                    #Tracker to hold the number of morale checks each iteration.
        Wavering = 0                        #Tracker for when morale drops to Wavering.
        Breaking = 0                        #Tracker for when morale drops to Breaking.
        Fleeing = 0                         #Tracker for when morale drops to Fleeing.
        ResolveMod = 1                      #Tracker for morale check calculations. Will fall to .9 or .8 when morale drops to Wavering/Breaking.
        FearsomeProcs = 0                   #Tracker to hold the number of Fearsome procs each iteration.
        Bleedstack1T = 0                    #Tracker for bleed stacks with one turn remaining.
        Bleedstack2T = 0                    #Tracker for bleed stacks with two turns remaining.
        ForgeSaved = 0                      #Tracker to add the amount of armor gained from Forge for each iteration.
        Poison = 0                          #Tracker for when first poisoning occurs against Ambushers.
        Bleed = 0                           #Tracker for when first bleeding occurs against cleavers.

        count = 0 #Number of hits until death. Starts at 0 and goes up after each attack.
        Hits = 0 #Used for Glorious Endurance. Starts at 0 and goes up after each hit.

        while hp > 0: #Continue looping until death.
            #Check various modifiers that change over the course of one's life. These will be re-checked after each attack.
            #Decapitate:
            if Decapitate:
                DecapMod = 2 - hp / Def_HP
            elif SmartDecap50 and hp <= Def_HP / 2:
                DecapMod = 2 - hp / Def_HP
            elif SmartDecap33 and hp <= Def_HP / 3:
                DecapMod = 2 - hp / Def_HP
            else:
                DecapMod = 1
            #Destory Armor:
            if DestroyArmor and count == 0:
                DArmorMod = 1.5
            elif DestroyArmor and count == 1 and DestroyArmorTwice:
                DArmorMod = 1.5
            elif DestroyArmorMastery and count == 0:    
                DArmorMod = 2
            elif DestroyArmorMastery and count == 1 and DestroyArmorTwice:
                DArmorMod = 2
            else:
                DArmorMod = 1
            #Battleforged:
            if Forge:
                ForgeMod = 1 - ((helmet + body) *.0005)
                if FallenBetrayerD:
                    ForgeMod *= .75
            else:
                ForgeMod = 1
            #Gladiator - The Bear - Glorious Endurance:
            if GloriousEndurance:
                if SplitMan:
                    GladMod = 1 - (.05 * (Hits * 2))
                else:
                    GladMod = 1 - (.05 * Hits)
                if GladMod < .75:
                    GladMod = .75
            else:
                GladMod = 1
            #Executioner:
            if Injury and Executioner:
                ExecMod = 1.2
            else:
                ExecMod = 1
            #HeadHunter:
            if HeadHunter:
                if HHStack:
                    Headshotchance = 100
                else:
                    Headshotchance = Headchance

            HitChanceCheck = random.randint(1,100) #Random roll to determine hit chance check.
            if HitChance is None or HitChanceCheck <= (min(95,HitChance + FastAdMod)): #If hit chance roll is lower or equal to hit chance, hit is successful.
                FastAdMod = 0 #Reset FastAd because of successful hit.
                Hits += 1 #Used for Glorious Endurance.

                #Begin damage rolls:
                hp_roll = random.randint(Mind,Maxd) #Random roll to determine unmodified hp damage.
                head_roll = random.randint(1,100) #Random roll to determine if hit is a headshot.
                if head_roll <= Headshotchance: #If headshot, do the following code blocks.
                    #Headshot injuries use a different formula. This flag will signal later when Injury is checked.
                    UseHeadShotInjuryFormula = 1
                    #HeadHunter check -- Lose current stack if you had one. Gain stack if you didn't.
                    if HeadHunter:
                        if not HHStack:
                            HHStack = True
                        elif HHStack:
                            HHStack = False
                    #2H Flail Check -- Have a higher armor ignoring% on Pound for headshots compared to bodyshots.
                    if Flail2HPound:
                        Ignore = Flail2HHeadshot
                        
                    #Destroy armor check -- if Destroy Armor special is active do this code block and skip the rest.
                    if DArmorMod != 1:
                        hp_roll = 10 #DestroyArmor forces hp damage to = 10.
                        hp -= hp_roll 
                        armor_roll = random.randint(Mind,Maxd) * ArmorMod * DArmorMod * GladMod * IndomMod * DamageMod *  ExecMod
                        ForgeSaved += armor_roll - armor_roll * ForgeMod
                        armor_roll = min(helmet,(armor_roll * ForgeMod))
                        helmet = math.ceil(helmet - armor_roll) #Rounding armor damage.
                    #If not DestoryArmor, and no armor is present, apply damage directly to hp.
                    elif helmet == 0:
                        hp_roll = hp_roll * NimbleMod * RaceMod * GladMod * IndomMod * ((DamageMod *  ExecMod * AimedShotMod) * DecapMod) * HeadMod
                        if Hammer10: #If 1H Hammer, deal 10 damage minimum.
                            hp_roll = max(hp_roll,10)
                        hp = math.ceil(hp - hp_roll) #Rounding hp damage.
                    #Otherwise, do the following.
                    else:
                        armor_roll = random.randint(Mind,Maxd) * ArmorMod * GladMod * IndomMod * DamageMod *  ExecMod
                        ForgeSaved += armor_roll - armor_roll * ForgeMod #Calculate how much armor is saved by Forge.
                        armor_roll = min(helmet,(armor_roll * ForgeMod)) #Applying Forge, and armor damage cannot exceed current armor.
                        helmet -= armor_roll #Armor damage applied to helmet.
                        #If the helmet does not get destroyed by the attack, do the following.
                        if helmet > 0:
                            hp_roll = max(0,(hp_roll * Ignore * NimbleMod * RaceMod * GladMod * IndomMod * ((DamageMod *  ExecMod * AimedShotMod) * DecapMod) - (helmet * 0.1)) * HeadMod)
                            if Hammer10:
                                hp_roll = max(hp_roll,10) 
                            helmet = math.ceil(helmet)
                            hp = math.ceil(hp - hp_roll)
                        #If the helmet did get destoryed by the attack, do the following.
                        else:
                            OverflowDamage = max(0,(hp_roll * (1 - Ignore) * NimbleMod * RaceMod * GladMod * IndomMod * ((DamageMod *  ExecMod * AimedShotMod) * DecapMod) - armor_roll))
                            hp_roll = (hp_roll * Ignore * NimbleMod * RaceMod * GladMod * IndomMod * ((DamageMod *  ExecMod * AimedShotMod) * DecapMod) + OverflowDamage) * HeadMod
                            if Hammer10:
                                hp_roll = max(hp_roll,10)
                            hp = math.ceil(hp - hp_roll)
                    #If SplitMan is active, do the following code block for the bonus body hit.
                    if SplitMan:
                        if BoneplateMod:
                            BoneplateMod = False
                            SMhp_roll = 0
                        else:
                            SMhp_roll = random.randint(Mind,Maxd) * .5
                            if body == 0:
                                SMhp_roll = SMhp_roll * NimbleMod * GladMod * IndomMod * AttachMod
                                hp = math.ceil(hp - SMhp_roll)
                            else:
                                SMarmor_roll = random.randint(Mind,Maxd) * .5 * ArmorMod * GladMod * IndomMod * AttachMod
                                ForgeSaved += SMarmor_roll - SMarmor_roll * ForgeMod
                                SMarmor_roll = min(body,(SMarmor_roll * ForgeMod))
                                body -= SMarmor_roll
                                if body > 0:
                                    SMhp_roll = max(0,(SMhp_roll * Ignore * NimbleMod * AdFurPadMod * GladMod * IndomMod * AttachMod - (body * 0.1)))
                                    body = math.ceil(body)
                                    hp = math.ceil(hp - SMhp_roll)
                                else:
                                    OverflowDamage = max(0,(SMhp_roll * (1 - Ignore * AdFurPadMod) * NimbleMod * GladMod * IndomMod * AttachMod - SMarmor_roll))
                                    SMhp_roll = SMhp_roll * Ignore * NimbleMod * AdFurPadMod * GladMod * IndomMod * AttachMod + OverflowDamage
                                    hp = math.ceil(hp - SMhp_roll)
                            
                else: #If not a headshot, do the following. 
                    #2H Flail Check -- Have a higher armor ignoring% on Pound for headshots compared to bodyshots.
                    if Flail2HPound:
                        Ignore = Flail2HBodyshot
                    #Bone Plates check -- Attack is negated if Boneplates are online, then turns off Boneplates until next trial.
                    if BoneplateMod:
                        BoneplateMod = False
                        hp_roll = 0
                    else:
                        if DArmorMod != 1:
                            hp_roll = 10
                            hp -= hp_roll
                            armor_roll = random.randint(Mind,Maxd) * ArmorMod * DArmorMod * GladMod * IndomMod * DamageMod * ExecMod
                            ForgeSaved += armor_roll - armor_roll * ForgeMod
                            armor_roll = min(body,(armor_roll * ForgeMod))
                            body = math.ceil(body - armor_roll)
                        elif body == 0 or Puncture:
                            hp_roll = hp_roll * NimbleMod * RaceMod * GladMod * IndomMod * AttachMod * ((DamageMod * ExecMod * AimedShotMod) * DecapMod)
                            if Hammer10:
                                hp_roll = max(hp_roll,10)
                            hp = math.ceil(hp - hp_roll)
                        else:
                            armor_roll = random.randint(Mind,Maxd) * ArmorMod * GladMod * IndomMod * DamageMod * ExecMod * AttachMod
                            ForgeSaved += armor_roll - armor_roll * ForgeMod
                            armor_roll = min(body,(armor_roll * ForgeMod))
                            body -= armor_roll
                            if body > 0:
                                hp_roll = max(0,(hp_roll * Ignore * NimbleMod * RaceMod * AdFurPadMod * GladMod * IndomMod * AttachMod * ((DamageMod * ExecMod * AimedShotMod) * DecapMod) - (body * 0.1)))
                                if Hammer10:
                                    hp_roll = max(hp_roll,10)
                                body = math.ceil(body)
                                hp = math.ceil(hp - hp_roll)
                            else:
                                OverflowDamage = max(0,(hp_roll * (1 - Ignore * AdFurPadMod) * NimbleMod * RaceMod * GladMod * IndomMod * AttachMod * ((DamageMod * ExecMod * AimedShotMod) * DecapMod) - armor_roll))
                                hp_roll = hp_roll * Ignore * NimbleMod * RaceMod * AdFurPadMod * GladMod * IndomMod * AttachMod * ((DamageMod * ExecMod * AimedShotMod) * DecapMod) + OverflowDamage
                                if Hammer10:
                                    hp_roll = max(hp_roll,10)
                                hp = math.ceil(hp - hp_roll)
                    #If SplitMan is active, do the following code block for the bonus head hit.
                    if SplitMan:
                        SMhp_roll = random.randint(Mind,Maxd) * .5
                        if helmet == 0:
                            SMhp_roll = SMhp_roll * NimbleMod * GladMod * IndomMod
                            hp = math.ceil(hp - SMhp_roll)
                        else:
                            SMarmor_roll = random.randint(Mind,Maxd) * .5 * ArmorMod * GladMod * IndomMod
                            ForgeSaved += SMarmor_roll - SMarmor_roll * ForgeMod
                            SMarmor_roll = min(helmet,(SMarmor_roll * ForgeMod))
                            helmet -= SMarmor_roll
                            if helmet > 0:
                                SMhp_roll = max(0,(SMhp_roll * Ignore * NimbleMod * GladMod * IndomMod - (helmet * 0.1)))
                                helmet = math.ceil(helmet)
                                hp = math.ceil(hp - SMhp_roll)
                            else:
                                OverflowDamage = max(0,(SMhp_roll * (1 - Ignore) * NimbleMod * GladMod * IndomMod - SMarmor_roll))
                                SMhp_roll = SMhp_roll * Ignore * NimbleMod * GladMod * IndomMod + OverflowDamage
                                hp = math.ceil(hp - SMhp_roll)
            else: #This block is run if attack misses.
                hp_roll = 0
                if FastAdaptation == 1: #If Fast Adaptation is selected, gain a stack.
                    FastAdMod += 10

            count += 1 #Add +1 to the number of hits taken. 

            #Injury check:
            if not injuryImmune and (hp > 0 or NineLivesMod):
                InjuryThreshold = 1
                if UseHeadShotInjuryFormula:
                    InjuryThreshold *= 1.25
                if Ironjaw:
                    InjuryThreshold *= 1.25
                if CripplingStrikes:
                    InjuryThreshold *= 2/3
                if ShamshirMastery:
                    InjuryThreshold *= 0.5
                elif Shamshir:
                    InjuryThreshold *= 2/3
                if not Injury:
                    if math.floor(hp_roll) >= Def_HP * InjuryThreshold * 0.25:
                        Injury = 1
                        if Flail3Head:
                            hits_until_1st_injury.append(count/3)
                        else:
                            hits_until_1st_injury.append(count)
                #Heavy injury check: Heavy injuries are not guaranteed even when conditions are met, so this is only checking for chance of heavy injury.
                if not HeavyInjuryChance:
                    if math.floor(hp_roll) >= Def_HP * InjuryThreshold * 0.5:
                        HeavyInjuryChance = 1
                        if Flail3Head:
                            hits_until_1st_heavy_injury_chance.append(count/3)
                        else:
                            hits_until_1st_heavy_injury_chance.append(count)
                
            #Morale check:
            if (hp > 0 or NineLivesMod) and not Fleeing and not injuryImmune:
                if Fearsome:
                    if Flail3Head != 1 or (Flail3Head and count % 3 == 1): #Checking weapon and if 3Head only apply 1-14 Fearsome effect on every first hit.
                        if math.floor(hp_roll) > 0 and math.floor(hp_roll) < 15:
                            FearsomeProcs += 1
                        if math.floor(hp_roll) > 0:
                            MoraleChecks += 1
                            resolve_roll = random.randint(1,100) #Random number used to see if we pass/fail morale check.
                            chance_morale_drop = max(5, 100 - (((Def_Resolve * ResolveMod) - FearsomeMod) - 40 * (1 - hp/Def_HP))) #Formula for chance of losing morale from damage.
                            if resolve_roll <= chance_morale_drop: #If we fail the check, we will fall to Wavering, Breaking, or Fleeing, in that order.
                                if not Wavering:
                                    Wavering = True
                                    ResolveMod = .9 #Wavering morale gives a -10% Resolve penalty, making us more vulnerable to further drops.
                                    if Flail3Head:
                                        hits_until_wavering.append(count/3)
                                    else:
                                        hits_until_wavering.append(count) #Return the time until Wavering for later data analysis.
                                elif not Breaking:
                                    Breaking = True
                                    ResolveMod = .8
                                    if Flail3Head:
                                        hits_until_breaking.append(count/3)
                                    else:
                                        hits_until_breaking.append(count)
                                elif not Fleeing:
                                    Fleeing = True
                                    if Flail3Head:
                                        hits_until_fleeing.append(count/3)
                                    else:
                                        hits_until_fleeing.append(count)
                    else:
                        if Flail3Head and count % 3 != 1:                  #This block is only run for 3Head's second/third hits.
                            if math.floor(hp_roll) >= 15:
                                MoraleChecks += 1
                                resolve_roll = random.randint(1,100)
                                chance_morale_drop = max(5, 100 - (((Def_Resolve * ResolveMod) - FearsomeMod) - 40 * (1 - hp/Def_HP)))
                                if resolve_roll <= chance_morale_drop:
                                    if not Wavering:
                                        Wavering = True
                                        ResolveMod = .9
                                        hits_until_wavering.append(count/3)
                                    elif not Breaking:
                                        Breaking = True
                                        ResolveMod = .8
                                        hits_until_breaking.append(count/3)
                                    elif not Fleeing:
                                        Fleeing = True
                                        hits_until_fleeing.append(count/3)

                    if SplitMan:                                           #Split Man block. Split Man doesn't get the 1-14 Fearsome effect.
                        if math.floor(SMhp_roll) >= 15:
                            MoraleChecks += 1
                            resolve_roll = random.randint(1,100)
                            chance_morale_drop = max(5, 100 - (((Def_Resolve * ResolveMod) - FearsomeMod) - 40 * (1 - hp/Def_HP)))
                            if resolve_roll <= chance_morale_drop:
                                if not Wavering:
                                    Wavering = True
                                    ResolveMod = .9
                                    hits_until_wavering.append(count)
                                elif not Breaking:
                                    Breaking = True
                                    ResolveMod = .8
                                    hits_until_breaking.append(count)
                                elif not Fleeing:
                                    Fleeing = True
                                    hits_until_fleeing.append(count)
                else:
                    if math.floor(hp_roll) >= 15: #Rehash of prior code blocks but without Fearsome.
                        MoraleChecks += 1
                        resolve_roll = random.randint(1,100)
                        chance_morale_drop = max(5, 100 - ((Def_Resolve * ResolveMod) - 40 * (1 - hp/Def_HP)))
                        if resolve_roll <= chance_morale_drop:
                            if not Wavering:
                                Wavering = True
                                ResolveMod = .9
                                if Flail3Head:
                                    hits_until_wavering.append(count/3)
                                else:
                                    hits_until_wavering.append(count)
                            elif not Breaking:
                                Breaking = True
                                ResolveMod = .8
                                if Flail3Head:
                                    hits_until_breaking.append(count/3)
                                else:
                                    hits_until_breaking.append(count)
                            elif not Fleeing:
                                Fleeing = True
                                if Flail3Head:
                                    hits_until_fleeing.append(count/3)
                                else:
                                    hits_until_fleeing.append(count)
                    if SplitMan:
                        if math.floor(SMhp_roll) >= 15:
                            MoraleChecks += 1
                            resolve_roll = random.randint(1,100)
                            chance_morale_drop = max(5, 100 - ((Def_Resolve * ResolveMod) - 40 * (1 - hp/Def_HP)))
                            if resolve_roll <= chance_morale_drop:
                                if not Wavering:
                                    Wavering = True
                                    ResolveMod = .9
                                    hits_until_wavering.append(count)
                                elif not Breaking:
                                    Breaking = True
                                    ResolveMod = .8
                                    hits_until_breaking.append(count)
                                elif not Fleeing:
                                    Fleeing = True
                                    hits_until_fleeing.append(count)

            if not FirstMoraleCheck:
                if Fearsome:
                    if not Flail3Head or (Flail3Head and count % 3 == 1): #Checking weapon and if 3Head only apply 1-14 Fearsome effect on every first hit.
                        if math.floor(hp_roll) > 0:
                            FirstMoraleCheck = True
                            if Flail3Head:
                                hits_until_1st_morale.append(count/3)
                            else:
                                hits_until_1st_morale.append(count)
                else:
                    if math.floor(hp_roll) >= 15:
                        FirstMoraleCheck = True
                        if Flail3Head:
                            hits_until_1st_morale.append(count/3)
                        else:
                            hits_until_1st_morale.append(count)
                if SplitMan:
                    if math.floor(SMhp_roll) >= 15:
                        FirstMoraleCheck = True
                        hits_until_1st_morale.append(count)
                    
            #Bleeding check:
            if (CleaverBleed or CleaverMastery) and not DOTImmune:
                #If damage taken >= 6 and Decapitate isn't in play, then apply a 2 turn bleed stack.
                if hp > 0 or NineLivesMod:
                    if math.floor(hp_roll) >= 6 and DecapMod and not Decapitate:
                        Bleedstack2T += 1
                        #Track fist instance of bleed for later data return.
                        if not Bleed:
                            Bleed = True
                            hits_until_1st_bleed.append(count)
                    #Every two attacks (1 turn for Cleavers), apply bleed damage based on current bleed stacks.
                    #If Resilient, 2 turn bleed stacks apply damage and then are removed. Otherwise 2 turn bleed stacks apply damage and convert into 1 turn bleed stacks.
                    if count % 2 == 0:
                        if Resilient:
                            hp -= BleedDamage * Bleedstack2T
                            Bleedstack2T = 0
                        else:
                            hp -= BleedDamage * Bleedstack1T
                            Bleedstack1T = Bleedstack2T
                            hp -= BleedDamage * Bleedstack2T
                            Bleedstack2T = 0

            #Poison check:
            if Ambusher and not DOTImmune:
                if not Poison:
                    if math.floor(hp_roll) >= 6:
                        Poison = True
                        hits_until_1st_poison.append(count)

            #If death occurs, check for NineLives and otherwise add the hitcount to the list for later analysis and start the next trial.
            if hp <= 0: 
                if NineLivesMod:
                    hp = random.randint(11,15)
                    NineLivesMod = False
                    Bleedstack1T = 0
                    Bleedstack2T = 0
                else:
                    if Forge:
                        Forge_bonus_armor.append(ForgeSaved)
                    if Flail3Head:
                        hits_until_death.append(count/3)
                    else:
                        hits_until_death.append(count)
                    Total_Morale_Checks.append(MoraleChecks)
                    #Check if the following trackers were hit and if not, append the time until death to their lists for later analysis instead of having an empty data point.
                    if not Injury:
                        if Flail3Head:
                            hits_until_1st_injury.append(count/3)
                        else:
                            hits_until_1st_injury.append(count)
                    if not HeavyInjuryChance:
                        if Flail3Head:
                            hits_until_1st_heavy_injury_chance.append(count/3)
                        else:
                            hits_until_1st_heavy_injury_chance.append(count)
                    if not Wavering:
                        if Flail3Head:
                            hits_until_wavering.append(count/3)
                        else:
                            hits_until_wavering.append(count)
                    if not Breaking:
                        if Flail3Head:
                            hits_until_breaking.append(count/3)
                        else:
                            hits_until_breaking.append(count)
                    if not Fleeing:
                        if Flail3Head:
                            hits_until_fleeing.append(count/3)
                        else:
                            hits_until_fleeing.append(count)
                    if Fearsome:
                        NumberFearsomeProcs.append(FearsomeProcs)

    #Analysis on data collection:
    HitsToDeath = statistics.mean(hits_until_death)
    StDev = statistics.stdev(hits_until_death)
    hits_until_death.sort()
    HitsToDeathCounter = collections.Counter(hits_until_death)
    HitsToDeathPercent = [(round(i, 2),round(HitsToDeathCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToDeathCounter]
    if not injuryImmune:
        if len(hits_until_1st_injury) != 0:
            hits_to_injure = statistics.mean(hits_until_1st_injury)
            hits_until_1st_injury.sort()
            HitsToInjureCounter = collections.Counter(hits_until_1st_injury)
            HitsToInjurePercent = [(round(i, 2),round(HitsToInjureCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToInjureCounter]
        if len(hits_until_1st_heavy_injury_chance) != 0:
            hits_to_1st_heavy_injury_chance = statistics.mean(hits_until_1st_heavy_injury_chance)
            hits_until_1st_heavy_injury_chance.sort()
            HitsToHeavyInjuryChanceCounter = collections.Counter(hits_until_1st_heavy_injury_chance)
            HitsToHeavyInjuryChancePercent = [(round(i, 2),round(HitsToHeavyInjuryChanceCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToHeavyInjuryChanceCounter]
        if len(hits_until_1st_morale) != 0:
            hits_to_morale = statistics.mean(hits_until_1st_morale)
            hits_until_1st_morale.sort()
            HitsToMoraleCounter = collections.Counter(hits_until_1st_morale)
            HitsToMoralePercent = [(round(i, 2),round(HitsToMoraleCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToMoraleCounter]
    if not moraleImmune:
        if len(Total_Morale_Checks) != 0:
            AvgNumberMoraleChecks = statistics.mean(Total_Morale_Checks)
        if len(hits_until_wavering) != 0:
            hits_to_wavering = statistics.mean(hits_until_wavering)
            hits_until_wavering.sort()
            HitsToWaveringCounter = collections.Counter(hits_until_wavering)
            HitsToWaveringPercent = [(round(i, 2),round(HitsToWaveringCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToWaveringCounter]
        if len(hits_until_breaking) != 0:
            hits_to_breaking = statistics.mean(hits_until_breaking)
            hits_until_breaking.sort()
            HitsToBreakingCounter = collections.Counter(hits_until_breaking)
            HitsToBreakingPercent = [(round(i, 2),round(HitsToBreakingCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToBreakingCounter]
        if len(hits_until_fleeing) != 0:
            hits_to_fleeing = statistics.mean(hits_until_fleeing)
            hits_until_fleeing.sort()
            HitsToFleeingCounter = collections.Counter(hits_until_fleeing)
            HitsToFleeingPercent = [(round(i, 2),round(HitsToFleeingCounter[i]/len(hits_until_death)*100, 2)) for i in HitsToFleeingCounter]
        if Fearsome:
            AvgFearsomeProcs = statistics.mean(NumberFearsomeProcs)
    if Forge:
        if len(Forge_bonus_armor) != 0:
            AvgForgeArmor = statistics.mean(Forge_bonus_armor)
    if Ambusher:
        if len(hits_until_1st_poison) != 0:
            hits_to_posion = statistics.mean(hits_until_1st_poison)
    if (CleaverBleed or CleaverMastery):
        if len(hits_until_1st_bleed) != 0:
            hits_to_bleed = statistics.mean(hits_until_1st_bleed)

    #Results:
    results = {'ChartData': {}}
    if HitChance is None:
        hitOrSwing = "hits"
    else:
        hitOrSwing = "swings"
    if DeathMean:
        string = f"Death in {HitsToDeath:.2f} {hitOrSwing} on average."
        print(string)
        results['DeathMean'] = string
    if DeathStDev:
        string = f"StDev: {StDev:.2f}"
        print(string)
        results['DeathStDev'] = string
    if DeathPercent:
        string = f"% {hitOrSwing} to die: {str(HitsToDeathPercent)}"
        print(string)
        results['DeathPercent'] = string
        results['ChartData']['HitsToDeathPercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToDeathPercent]

    #Injury Data Return
    if injuryImmune or hits_to_injure >= HitsToDeath:
        if InjuryMean or InjuryPercent:
            string = "No chance of injury."
            print(string)
            if InjuryMean:
                results['InjuryMean'] = string
            if InjuryPercent:
                results['InjuryPercent'] = string
    else:        
        if InjuryMean:
            string = f"First injury in {hits_to_injure:.2f} {hitOrSwing} on average."
            print(string)
            results['InjuryMean'] = string
        if InjuryPercent:
            string = f"% First injury in: {str(HitsToInjurePercent)}"
            print(string)
            results['InjuryPercent'] = string
            results['ChartData']['HitsToInjurePercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToInjurePercent]
    if injuryImmune or hits_to_1st_heavy_injury_chance >= HitsToDeath:
        if HeavyInjuryMean or HeavyInjuryPercent:
            string = "No chance of heavy injury."
            print(string)
            if HeavyInjuryMean:
                results['HeavyInjuryMean'] = string
            if HeavyInjuryPercent:
                results['HeavyInjuryPercent'] = string
    else:
        if HeavyInjuryMean:
            string = f"Chance of first heavy injury in {hits_to_1st_heavy_injury_chance:.2f} {hitOrSwing} on average."
            print(string)
            results['HeavyInjuryMean'] = string
        if HeavyInjuryPercent:
            string = f"% First heavy injury chance in: {str(HitsToHeavyInjuryChancePercent)}"
            print(string)
            results['HeavyInjuryPercent'] = string
            results['ChartData']['HitsToHeavyInjuryChancePercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToHeavyInjuryChancePercent]
        
    if not moraleImmune:
        #Morale Data Return
        if MoraleChecksTotal:
            if len(Total_Morale_Checks) != 0:
                string = f"{AvgNumberMoraleChecks:.2f} morale checks before death on average."
                print(string)
                results['MoraleChecksTotal'] = string
        if len(hits_until_1st_morale) != 0:
            if MoraleMean:
                string = f"First morale check in {hits_to_morale:.2f} {hitOrSwing} on average."
                print(string)
                results['MoraleMean'] = string
            if MoralePercent:
                string = f"% First morale check in: {str(HitsToMoralePercent)}"
                print(string)
                results['MoralePercent'] = string
                results['ChartData']['HitsToMoralePercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToMoralePercent]
        
        if MoraleDropsMean:
            results['MoraleDropsMean'] = []
        if MoraleDropsPercent:
            results['MoraleDropsPercent'] = []
        #Wavering
        if hits_to_wavering >= HitsToDeath:
            if MoraleDropsMean or MoraleDropsPercent:
                string = "Cannot fall to Wavering morale prior to death."
                print(string)
                if MoraleDropsMean:
                    results['MoraleDropsMean'].append(string)
                if MoraleDropsPercent:
                    results['MoraleDropsPercent'].append(string)
        else:
            if MoraleDropsMean:
                string = f"Wavering morale (or death) in {hits_to_wavering:.2f} {hitOrSwing} on average."
                print(string)
                results['MoraleDropsMean'].append(string)
            if MoraleDropsPercent:
                string = f"% Wavering morale (or death) in: {str(HitsToWaveringPercent)}"
                print(string)
                results['MoraleDropsPercent'].append(string)
                results['ChartData']['HitsToWaveringPercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToWaveringPercent]
        
        #Breaking
        if hits_to_breaking >= HitsToDeath:
            if MoraleDropsMean or MoraleDropsPercent:
                string = "Cannot fall to Breaking morale prior to death."
                print(string)
                if MoraleDropsMean:
                    results['MoraleDropsMean'].append(string)
                if MoraleDropsPercent:
                    results['MoraleDropsPercent'].append(string)
        else:
            if MoraleDropsMean:
                string = f"Breaking morale (or death) in {hits_to_breaking:.2f} {hitOrSwing} on average."
                print(string)
                results['MoraleDropsMean'].append(string)
            if MoraleDropsPercent:
                string = f"% Breaking morale (or death) in: {str(HitsToBreakingPercent)}"
                print(string)
                results['MoraleDropsPercent'].append(string)
                results['ChartData']['HitsToBreakingPercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToBreakingPercent]
        
        #Fleeing
        if hits_to_fleeing >= HitsToDeath:
            if MoraleDropsMean or MoraleDropsPercent:
                string = "Cannot fall to Fleeing morale prior to death."
                print(string)
                if MoraleDropsMean:
                    results['MoraleDropsMean'].append(string)
                if MoraleDropsPercent:
                    results['MoraleDropsPercent'].append(string)
        else:
            if MoraleDropsMean:
                string = f"Fleeing morale (or death) in {hits_to_fleeing:.2f} {hitOrSwing} on average."
                print(string)
                results['MoraleDropsMean'].append(string)
            if MoraleDropsPercent:
                string = f"% Fleeing morale (or death) in: {str(HitsToFleeingPercent)}"
                print(string)
                results['MoraleDropsPercent'].append(string)
                results['ChartData']['HitsToFleeingPercent'] = [{'x':pair[0], 'y':pair[1]} for pair in HitsToFleeingPercent]

        if MoraleDropsMean:
            results['MoraleDropsMean'] = '\n'.join(results['MoraleDropsMean'])
        if MoraleDropsPercent:
            results['MoraleDropsPercent'] = '\n'.join(results['MoraleDropsPercent'])

        #Fearsome
        if Fearsome:
            string = f"{AvgFearsomeProcs:.2f} extra morale checks from Fearsome's 1-14 damage effect on average."
            print(string)
            results['Fearsome'] = string
    else:
        string = "Immune to morale."
        print(string)
        if MoraleChecksTotal:
            results['MoraleChecksTotal'] = string
        if MoraleMean:
            results['MoraleMean'] = string
        if MoralePercent:
            results['MoralePercent'] = string
        if MoraleDropsMean:
            results['MoraleDropsMean'] = string
        if MoraleDropsPercent:
            results['MoraleDropsPercent'] = string
        if Fearsome:
            results['Fearsome'] = string

    if Nimble:
        string = f"Nimble %: {str(NimbleMod)}"
        print(string)
        results['Nimble'] = string
    if Forge:
        string = f"{AvgForgeArmor:.2f} bonus armor from Forge on average."
        print(string)
        results['Forge'] = string
    if Ambusher:
        if len(hits_until_1st_poison) != 0:
            string = f"First poison in {hits_to_posion:.2f} {hitOrSwing} on average."
            print(string)
            results['Ambusher'] = string
        else:
            results['Ambusher'] = "No poison applied."
    if CleaverBleed or CleaverMastery:
        if len(hits_until_1st_bleed) != 0:
            string = f"First bleed in {hits_to_bleed:.2f} {hitOrSwing} on average."
            print(string)
            results['Cleaver'] = string
        else:
            results['Cleaver'] = "No bleed applied."
    print("-----") #Added for readability. If this annoys you then remove this line.

    return results

if __name__ == '__main__':
    main()
    
#CREDITS:
#Author: turtle225
#Contact: turtl225e@gmail.com
#Copyright 2019, turtle225. All rights reserved.
#Special Thanks:
#-- Abel (aka) Villain Joueur: For grabbing the damage formula out of the game code, writing the damage page on the wiki, and for helping me with many questions along the way.
#-- Wall (aka) Wlira: For helping me with some questions along the way and having an existing calculator for me to test against.
#-- You: If you are using the calculator, thank you! If you find any bugs or have feedback/questions/suggestions, you can usually find me on the Steam forums or send me an email.
#-- Overhype: For making an amazing game for us to play.

#History:
#Version 1.0.0 (12/24/2019)
#-- First released on Github.
#Version 1.0.1 (12/24/2019)
#-- Added Barbarian King, Brigand Leader, and Hedge Knight.
#Version 1.0.2 (12/25/2019)
#-- Added error handling.
#Version 1.0.3 (12/26/2019)
#-- Added 3HeadFlail unique Fearsome logic, and made 3Head results divided by 3 to show number of swings rather than hits.
#Version 1.1.0 (12/26/2019)
#-- Added defender presets.
#Version 1.1.1 (12/27/2019)
#-- Fixed an inconsistency where sometimes SteelBrow was called Steelbrow which caused it to not work properly.
#-- Fixed a typo on the Footman preset.
#Version 1.2.0 (12/28/2019)
#-- Added attacker presets.
#Version 1.2.1 (1/21/2020)
#-- Changed rounding logic to always round damage down after in game evidence suggested this was the case.
#Version 1.3.0 (2/6/2020)
#-- Added in headshot injury formula logic which is different than body injury logic.
#-- Added sorting to the return of %chance of death by hit so that it ascends from low to high instead of coming out randomly.
#-- Added in ability to return %chance of injury and morale by hit. 
#-- Added a tracker that checks for the first chance of receiving a heavy injury. 
#-- Added options to adjust the verbosity of the data returned to allow the user to easily choose what gets output.
#Version 1.3.1 (2/19/2020)
#-- Reworked Destroy Armor logic to make the results it provides more useful to the user.
#-- Destroy Armor will now be used once or twice and then switch to normal attacks, rather then checking armor levels like it used to.
#Version 1.3.2 (3/16/2020)
#-- Fixed an error in order of calculations for Goblin Overseer which incorrectly had his Ignore% at 75% instead of the correct 77% (Thanks Abel).
#-- Fixed an error with AimedShot where it provided bonus damage against hp and armor when it should only boost against hp (Thanks Abel).
#-- Added logic for Indomitable halving Bleed damage whereas before it wasn't doing so.
#-- Added option for Puncture tests.
#-- Added option for ranged shots that scatter into unintended targets.
#Version 1.3.3 (4/11/2020)
#-- Added logic to return the average amount of armor gained when using Forge.
#-- Added logic to return time of first poisoning against Ambushers.
#Version 1.3.4 (4/13/2020)
#-- Added option to give 2HFlails their +10% Ignore on single target attacks (thank you Andre27 for pointing this out).
#-- Added option to give 2HSwords their +5% Ignore on their Split attack (thank you Andre27 for pointing this out).
#-- Added Flail2HIgnore to the Orc Berserker preset.
#Version 1.5.0 (8/13/2020)
#-- Updated calculator with Blazing Deserts changes, see below for details.
#-- Reworked HeadHunter for Blazing Deserts change.
#-- Also removed HH option to not count stacks between kills as it doesn't make sense to calculate that way.
#-- Adjusted Nine Lives to clear existing Bleed stacks when it procs.
#-- Added ShamshirMastery to account for new logic with Sword Mastery.
#-- Adjusted injury logic to account for new Shamshir Mastery.
#-- Added The Bear's unique perk - Glorious Endurance.
#-- Changed Dazed to -25% damage instead of -35% damage.
#-- Changed Mushrooms to +25% damage global instead of its previous effect.
#-- Added Distracted effect that is applied by Nomads.
#-- Changed Ambusher ignore modifier to 1.25 (down from 1.4).
#-- Changed Ambusher presets to use a 30-50 Boondock Bow (up from 25-40).
#-- Removed AmbusherDay200 entry.
#-- Added Qatal special - Deathblow.
#-- Changed Fallen Hero preset to use a Greataxe instead of Winged Mace to demonstrate their most threatening loadout.
#-- Changed Sergeant preset to use a Winged Mace instead of Warhammer to make him more neutral to his loadout options.
#-- Added 4 new attacker presets and 4 new defender presets.
#-- Changed Billhook preset as per Billhook nerf.
#Version 1.5.1 (9/4/2020)
#-- Updated Conscript preset as per nerf to 55 HP.
#Version 1.5.2 (9/28/2020)
#-- Added Ironjaw option and logic.
#Version 1.5.3 (11/5/2020)
#-- Fixed inaccuracies with the Crypt Cleaver preset where I hadn't realized it had gotten nerfed in Blazing Deserts.
#Version 1.5.5 (1/30/2021)
#-- Changed attachments to automatically apply +Armor and -Fatigue, as per recent attachment changes.
#-- Added Wolf/Hyena, Lindwurm, and Serpent attachments as additional options.
#-- Changed Nimble with Bone Plate defender preset to use Padded Leather (80) so that it can still be at -15 after Bone Plate nerf.
#Version 1.6 (7/17/2021)
#-- Added feature to track/return the time it takes for morale to drop to Wavering, Breaking, and Fleeing.
#-- Added switches at the top to turn on or off the data returns for morale related data.
#-- Added Fearsome logic for morale check calculations.
#-- Added Atk_Resolve and Def_Resolve fields for use in morale calculations.
#-- Added Attacker and Defender Resolve to appropriate presets.
#-- Updated Lindwurms to have 35% armor ignore after they were "nerfed" from 40% after a game bug was fixed (where they had been doing 0% prior).
#-- Added logic to a few code blocks to prevent them from running reduntantly (ie checking for injury when already injured) to improve efficiency slightly.
#-- Added logic to a few code blocks to prevent them from running reduntantly (ie checking for injury on the turn a target dies) to improve efficiency slightly.
#Version 1.6.1 (3/10/2022) - Of Flesh and Faith DLC release.
#-- Added new 2HFlail logic as per the change where Pound does +10% ignore on headshots (and +20% with Flail Mastery)
#-- Changed Flail2HIgnore swtich to Flail2HPound and also added FlailMastery switch.
#-- Changed Nine Lives to retrun 11-15 hp, up from 5-10.
#-- Changed Handgonne attacker preset to have 90% armor damage, down from 100%.
#-- Changed R2Throw (two range Throwing) switch to deal +30% damage, down from +40%.
#-- Adjusted Fearsome to the new formula of (Resolve - 10) * 20%
#-- Added +5% armor ignore to Aimed Shot (this is not a new game change, just something I never realized before).
#Version 1.6.2 (3/14/2022)
#-- Adjusted Orc Berserker preset for new buff to Berserk Chain to 50-100, up from 40-100.
#Version 1.6.3 (4/11/2022)
#-- Fixed a bug with Forge + Split Man interaction where having low armor with Forge was giving much better survivability than it should have been against Split man.
#Version 1.6.4 (6/27/2023)
#-- Added a tracker that returns the average hits until first bleed proc for cleaver tests.