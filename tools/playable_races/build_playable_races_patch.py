import importlib.util
import shutil
import struct
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(r"C:\Users\monty\Documents\Codex\2026-04-29\i-am-creating-a-world-of")
SERVER_DBC = Path(r"C:\Build\bin\Debug\data\dbc")
OUT_DIR = WORKSPACE / "artifacts" / "playable_races"
CLIENT_PATCH = Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\patch-4.MPQ")
CLIENT_LOCALE = Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\enUS\locale-enUS.MPQ")
MPQCLI = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools\mpqcli.exe")
REMIX_BUILDER = WORKSPACE / "tools" / "remix_system" / "build_remix_client_patch.py"
DOWNPORT_TOOL = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools\downport_md21_to_wotlk.py")
STATIC_MODEL_TOOL = Path(r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools\static_from_modern_m2.py")
MODEL_EXTRACTION_CHARACTER = Path(r"C:\Users\monty\OneDrive\Desktop\Model Extraction\character")
WORGOBLIN_PATCH = WORKSPACE / "vendor" / "mod-worgoblin" / "data" / "patch"
DOWNPORTED_MODEL_DIR = OUT_DIR / "downported_models"
REMIX_SHIRT_DISPLAY_ID = 900100
REMIX_SHIRT_DISPLAY_SOURCE_ID = 9891
REMIX_SHIRT_ICON_NAME = "INV_Shirt_Duelist_A_01_Brown"
REMIX_SHIRT_ICON_SOURCE = Path(r"C:\Users\monty\OneDrive\Desktop\New folder (3)\interface\icons\inv_shirt_duelist_a_01_brown.blp")
DEMON_HUNTER_ASSET_DIR = Path(r"C:\Users\monty\OneDrive\Desktop\New folder (3)")

GOBLIN_RACE = 9
WORGEN_RACE = 12
OLD_WORGEN_RACE = 22
DEMON_HUNTER_CLASS = 10
DEMON_HUNTER_MASK = 1 << (DEMON_HUNTER_CLASS - 1)
DEMON_HUNTER_SKILL = 910
DEMON_HUNTER_HAVOC_SKILL = 911
DEMON_HUNTER_VENGEANCE_SKILL = 912
DEMON_HUNTER_SPELLBOOK_SKILLS = {
    DEMON_HUNTER_SKILL: ("Demon Hunter", "Demon Hunter class abilities."),
    DEMON_HUNTER_HAVOC_SKILL: ("Havoc", "Havoc Demon Hunter abilities."),
    DEMON_HUNTER_VENGEANCE_SKILL: ("Vengeance", "Vengeance Demon Hunter abilities."),
}
DEMON_HUNTER_MAIN_HAND = 139012
DEMON_HUNTER_OFF_HAND = 139013
DEMON_HUNTER_MAIN_DISPLAY = 910301
DEMON_HUNTER_OFF_DISPLAY = 910302
DEMON_HUNTER_GLAIVE_ICON = "inv_glaive_1h_demonhunter_a_01"
DEMON_HUNTER_GLAIVE_MODEL = "glaive_1h_demonhunter_a_01"
DEMON_HUNTER_OFFHAND_GLAIVE_MODEL = "glaive_1h_demonhunter_a_01_offhand"
DEMON_HUNTER_GLAIVE_TEXTURE = "glaive_1h_demonhunter_a_01_green"
UNSAFE_DEMON_HUNTER_SPELL_VISUAL_STEMS = {
    # This retail state model has produced ERROR #132 crashes in the 3.3.5a renderer.
    "cfx_demonhunter_felrush_statebase",
}
DEMON_HUNTER_SPELLS = {
    910201: ("Demon's Bite", "A quick attack that bites into the enemy with demonic fury.", "ability_demonhunter_felblade", 1752),
    910202: ("Chaos Strike", "Strike with chaotic power, dealing weapon damage to the enemy.", "ability_demonhunter_chaosstrike", 1752),
    910203: ("Throw Glaive", "Hurl a demonic glaive at your target.", "ability_demonhunter_throwglaive", 2764),
    910204: ("Fel Rush", "Rush forward in a burst of fel energy.", "ability_demonhunter_felrush", 2983),
    910205: ("Eye Beam", "Blast enemies in front of you with a focused beam of chaotic fel energy.", "ability_demonhunter_eyebeam", 15407),
    910206: ("Blade Dance", "Strike all nearby enemies with a rapid dance of blades.", "ability_demonhunter_bladedance", 51723),
    910207: ("Immolation Aura", "Ignite yourself with fel fire, damaging nearby enemies.", "ability_demonhunter_immolation", 1949),
    910208: ("Vengeful Retreat", "Vault backward away from danger.", "ability_demonhunter_vengefulretreat", 781),
    910209: ("Blur", "Increase your chance to dodge for a short time.", "ability_demonhunter_blur", 5277),
    910210: ("Metamorphosis", "Leap into the air and land with explosive demonic force, empowering yourself.", "ability_demonhunter_metamorphasisdps", 59672),
    910211: ("Spectral Sight", "Sharpen your spectral senses to detect hidden enemies.", "ability_demonhunter_spectralsight", 2836),
    910212: ("Chaos Nova", "Unleash an eruption of fel energy, stunning nearby enemies.", "ability_demonhunter_chaosnova", 30283),
    910213: ("Consume Magic", "Dispel one beneficial magic effect from an enemy.", "ability_demonhunter_consumemagic", 370),
    910214: ("Disrupt", "Interrupt the enemy's spellcasting and prevent spells from that school for a short time.", "warrior_disruptingshout", 1766),
    910215: ("Imprison", "Imprison a demon, beast, or humanoid, incapacitating it for up to 1 minute.", "ability_demonhunter_imprison", 6770),
    910216: ("Torment", "Taunt the target to attack you.", "ability_demonhunter_torment", 355),
    910217: ("Shear", "Shear the target with demonic power, dealing weapon damage.", "ability_demonhunter_hatefulstrike", 1752),
    910218: ("Soul Cleave", "Cleave nearby enemies with a sweeping strike.", "ability_demonhunter_soulcleave", 845),
    910219: ("Infernal Strike", "Charge toward an enemy in a burst of fel force.", "ability_demonhunter_infernalstrike1", 100),
    910220: ("Demon Spikes", "Harden your skin with demonic spikes, increasing your chance to dodge.", "ability_demonhunter_demonspikes", 5277),
    910221: ("Fiery Brand", "Brand the enemy with fel fire, burning it over time.", "ability_demonhunter_fierybrand", 11366),
    910222: ("Sigil of Flame", "Place a sigil that erupts in flame around you.", "ability_demonhunter_sigilyellow", 26573),
    910223: ("Felblade", "Charge to your target and strike with a burning demonic blade.", "ability_demonhunter_felblade", 100),
    910224: ("Death Sweep", "Unleash a devastating sweeping attack around you.", "ability_demonhunter_bladedance", 51723),
    910225: ("Darkness", "Summon darkness around you, protecting allies standing within it.", "ability_demonhunter_darkness", 33206),
    910226: ("The Hunt", "Charge to your prey with savage fel momentum.", "inv_ability_demonhunter_thehunt", 100),
    910227: ("Fel Devastation", "Unleash fel energy in front of you, burning enemies caught in the blast.", "ability_demonhunter_feldevastation", 15407),
    910228: ("Sigil of Misery", "Place a sigil that erupts to disorient nearby enemies.", "ability_demonhunter_sigilofmisery", 8122),
    910229: ("Sigil of Silence", "Place a sigil that erupts to silence nearby enemies.", "ability_demonhunter_sigilofsilence", 15487),
    910230: ("Sigil of Chains", "Place a sigil that erupts with binding fel chains.", "ability_demonhunter_sigilofchains", 122),
    910231: ("Glide", "Slow your falling speed with demonic wings.", "ability_demonhunter_glide", 130),
    910232: ("Double Jump", "Leap again while already in the air.", "ability_demonhunter_doublejump", 131),
    910233: ("Reverse Magic", "Remove harmful magic effects from yourself and nearby allies.", "ability_demonhunter_reversemagic", 527),
    910234: ("Shattered Souls", "Your killing blows can shatter lesser soul fragments from enemies.", "ability_demonhunter_shatteredsouls", 1949),
    910235: ("Chaos Brand", "Brand your target with chaos, increasing magic damage taken.", "ability_demonhunter_chaoticimprint_shadow", 1490),
    910236: ("Annihilation", "A devastating Chaos Strike empowered by Metamorphosis.", "ability_demonhunter_chaosstrike", 1752),
    910237: ("Glaive Tempest", "Launch two demonic glaives in a destructive storm around you.", "ability_demonhunter_bladedance", 51723),
    910238: ("Fel Barrage", "Channel a torrent of fel energy at enemies in front of you.", "ability_demonhunter_eyebeam", 15407),
    910239: ("Demonic", "Eye Beam briefly triggers a demonic transformation.", "ability_demonhunter_metamorphasisdps", 59672),
    910240: ("Netherwalk", "Slip into the Nether, avoiding incoming harm for a short time.", "ability_demonhunter_netherbond", 31224),
    910241: ("Fracture", "Brutally slash the enemy, tearing loose soul fragments.", "ability_demonhunter_hatefulstrike", 1752),
    910242: ("Spirit Bomb", "Consume nearby soul fragments and explode with fel energy.", "ability_demonhunter_soulcleave2", 30283),
    910243: ("Soul Barrier", "Shield yourself with gathered souls.", "ability_demonhunter_soulcleave3", 17),
    910244: ("Soul Carver", "Carve into the enemy's soul, burning them over time.", "artifactability_vengeancedemonhunter_painbringer", 11366),
    910245: ("Demon Blades", "Your auto attacks are empowered by demonic fury, replacing Demon's Bite as a passive Fury generator.", "ability_demonhunter_hatefulstrike", 1752),
    910246: ("Essence Break", "Slash enemies in front of you with chaotic energy, increasing the damage they take from your blade techniques.", "ability_demonhunter_chaosstrike", 845),
    910247: ("Fel Eruption", "Impale the target with fel energy, dealing Chaos damage and stunning them.", "ability_demonhunter_chaosnova", 30283),
    910248: ("Unbound Chaos", "Immolation Aura empowers your next Fel Rush to deal Chaos damage to enemies in its path.", "ability_demonhunter_chaoticimprint_fire", 1949),
    910249: ("Momentum", "Fel Rush and Vengeful Retreat increase your damage for a short time.", "ability_demonhunter_felrush", 5277),
    910250: ("Tactical Retreat", "Vengeful Retreat generates Fury and refreshes your momentum in combat.", "ability_demonhunter_vengefulretreat2", 781),
    910251: ("Burning Hatred", "Immolation Aura generates additional Fury while burning nearby enemies.", "ability_demonhunter_immolation", 1949),
    910252: ("Reaver's Glaive", "Throw an empowered glaive that marks your prey for follow-up strikes.", "inv_ability_aldrachireaverdemonhunter_reaversglaive", 2764),
    910253: ("Demonic Wards", "Your demonic physiology reduces magic damage taken.", "ability_demonhunter_empowerwards", 5277),
    910254: ("Mastery: Fel Blood", "Increases your armor and attack power through fel-infused blood.", "ability_demonhunter_spectank", 5277),
    910255: ("Sigil of Spite", "Place a sigil that detonates in a violent burst of fel energy.", "ability_demonhunter_sigilofinquisition", 26573),
    910256: ("Elysian Decree", "Place a kyrian sigil that explodes for Arcane damage and shatters lesser soul fragments.", "ability_bastion_demonhunter", 26573),
    910257: ("Frailty", "Your soul-consuming attacks afflict enemies with Frailty, causing you to heal from damage dealt to them.", "ability_demonhunter_soulcleave3", 1490),
    910258: ("Bulk Extraction", "Rip soul fragments from nearby enemies and draw them to yourself.", "ability_demonhunter_soulcleave4", 30283),
    910259: ("Charred Warblades", "Fire damage you deal heals you for a portion of the damage done.", "ability_demonhunter_fierybrand", 11366),
    910260: ("Demonsurge", "Metamorphosis surges with fel power, empowering your core demonic attacks.", "inv_ability_felscarreddemonhunter_demonsurge", 59672),
    910261: ("Chaos Theory", "Blade Dance has a chance to empower your next Chaos Strike.", "ability_demonhunter_chaosstrike", 51723),
    910262: ("Trail of Ruin", "Blade Dance leaves enemies burning with Chaos damage over time.", "ability_demonhunter_bladedance", 703),
    910263: ("First Blood", "Blade Dance strikes your primary target with increased force.", "ability_demonhunter_bladedance", 51723),
    910264: ("Ragefire", "Immolation Aura stores part of its damage and erupts when it expires.", "ability_demonhunter_immolation", 1949),
    910265: ("Any Means Necessary", "Your non-Physical damage is converted into Chaos damage where possible.", "ability_demonhunter_chaoticimprint_arcane", 1490),
    910266: ("Know Your Enemy", "Critical strike strengthens your Chaos damage.", "ability_demonhunter_spectralsight", 1490),
    910267: ("Inner Demon", "Entering Metamorphosis unleashes the demon within on nearby enemies.", "ability_demonhunter_metamorphasisdps", 59672),
    910268: ("Initiative", "Damaging an enemy before they damage you increases your critical strike chance.", "ability_demonhunter_vengefulretreat", 5277),
    910269: ("Burning Wound", "Demon's Bite wounds the target, increasing fire damage taken from you.", "ability_demonhunter_fierybrand", 11366),
    910270: ("Rush of Chaos", "Metamorphosis recovers faster, keeping your burst windows closer to retail pacing.", "ability_demonhunter_felrush", 59672),
    910271: ("Soul Furnace", "Soul Cleave increases the damage of your next Spirit Bomb.", "ability_demonhunter_soulcleave2", 845),
    910272: ("Calcified Spikes", "Demon Spikes lingers as hardened fel plating after it fades.", "ability_demonhunter_demonspikes2", 5277),
    910273: ("Illuminated Sigils", "Your sigils activate more reliably and recover more quickly.", "ability_demonhunter_concentratedsigils", 26573),
    910274: ("Void Reaver", "Frailty causes affected enemies to deal reduced damage to you.", "ability_demonhunter_soulcleave3", 1490),
    910275: ("Fallout", "Immolation Aura has a chance to shatter lesser soul fragments.", "ability_demonhunter_shatteredsouls", 1949),
    910276: ("Feed the Demon", "Consuming soul fragments reduces Demon Spikes cooldown.", "ability_demonhunter_demonspikes", 5277),
    910277: ("Burning Alive", "Fiery Brand spreads to nearby enemies over time.", "ability_demonhunter_fierybrand", 11366),
    910278: ("Down in Flames", "Fiery Brand gains an additional charge.", "ability_demonhunter_brandofthehunt", 11366),
    910279: ("Ruinous Bulwark", "Fel Devastation shields you after channeling.", "ability_demonhunter_feldevastation", 17),
    910280: ("Last Resort", "Fatal damage instead triggers Metamorphosis and saves you from death.", "ability_demonhunter_metamorphasistank", 31224),
}
DEMON_HUNTER_SPELL_SKILLS = {
    910201: DEMON_HUNTER_HAVOC_SKILL,
    910202: DEMON_HUNTER_HAVOC_SKILL,
    910203: DEMON_HUNTER_SKILL,
    910204: DEMON_HUNTER_SKILL,
    910205: DEMON_HUNTER_HAVOC_SKILL,
    910206: DEMON_HUNTER_HAVOC_SKILL,
    910207: DEMON_HUNTER_VENGEANCE_SKILL,
    910208: DEMON_HUNTER_HAVOC_SKILL,
    910209: DEMON_HUNTER_HAVOC_SKILL,
    910210: DEMON_HUNTER_HAVOC_SKILL,
    910211: DEMON_HUNTER_SKILL,
    910212: DEMON_HUNTER_SKILL,
    910213: DEMON_HUNTER_SKILL,
    910214: DEMON_HUNTER_SKILL,
    910215: DEMON_HUNTER_SKILL,
    910216: DEMON_HUNTER_SKILL,
    910217: DEMON_HUNTER_VENGEANCE_SKILL,
    910218: DEMON_HUNTER_VENGEANCE_SKILL,
    910219: DEMON_HUNTER_VENGEANCE_SKILL,
    910220: DEMON_HUNTER_VENGEANCE_SKILL,
    910221: DEMON_HUNTER_VENGEANCE_SKILL,
    910222: DEMON_HUNTER_VENGEANCE_SKILL,
    910223: DEMON_HUNTER_HAVOC_SKILL,
    910224: DEMON_HUNTER_HAVOC_SKILL,
    910225: DEMON_HUNTER_SKILL,
    910226: DEMON_HUNTER_HAVOC_SKILL,
    910227: DEMON_HUNTER_VENGEANCE_SKILL,
    910228: DEMON_HUNTER_VENGEANCE_SKILL,
    910229: DEMON_HUNTER_VENGEANCE_SKILL,
    910230: DEMON_HUNTER_VENGEANCE_SKILL,
    910231: DEMON_HUNTER_SKILL,
    910232: DEMON_HUNTER_SKILL,
    910233: DEMON_HUNTER_SKILL,
    910234: DEMON_HUNTER_SKILL,
    910235: DEMON_HUNTER_SKILL,
    910236: DEMON_HUNTER_HAVOC_SKILL,
    910237: DEMON_HUNTER_HAVOC_SKILL,
    910238: DEMON_HUNTER_HAVOC_SKILL,
    910239: DEMON_HUNTER_HAVOC_SKILL,
    910240: DEMON_HUNTER_HAVOC_SKILL,
    910241: DEMON_HUNTER_VENGEANCE_SKILL,
    910242: DEMON_HUNTER_VENGEANCE_SKILL,
    910243: DEMON_HUNTER_VENGEANCE_SKILL,
    910244: DEMON_HUNTER_VENGEANCE_SKILL,
    910245: DEMON_HUNTER_HAVOC_SKILL,
    910246: DEMON_HUNTER_HAVOC_SKILL,
    910247: DEMON_HUNTER_HAVOC_SKILL,
    910248: DEMON_HUNTER_HAVOC_SKILL,
    910249: DEMON_HUNTER_HAVOC_SKILL,
    910250: DEMON_HUNTER_HAVOC_SKILL,
    910251: DEMON_HUNTER_HAVOC_SKILL,
    910252: DEMON_HUNTER_HAVOC_SKILL,
    910253: DEMON_HUNTER_VENGEANCE_SKILL,
    910254: DEMON_HUNTER_VENGEANCE_SKILL,
    910255: DEMON_HUNTER_VENGEANCE_SKILL,
    910256: DEMON_HUNTER_SKILL,
    910257: DEMON_HUNTER_VENGEANCE_SKILL,
    910258: DEMON_HUNTER_VENGEANCE_SKILL,
    910259: DEMON_HUNTER_VENGEANCE_SKILL,
    910260: DEMON_HUNTER_HAVOC_SKILL,
    910261: DEMON_HUNTER_HAVOC_SKILL,
    910262: DEMON_HUNTER_HAVOC_SKILL,
    910263: DEMON_HUNTER_HAVOC_SKILL,
    910264: DEMON_HUNTER_HAVOC_SKILL,
    910265: DEMON_HUNTER_HAVOC_SKILL,
    910266: DEMON_HUNTER_HAVOC_SKILL,
    910267: DEMON_HUNTER_HAVOC_SKILL,
    910268: DEMON_HUNTER_HAVOC_SKILL,
    910269: DEMON_HUNTER_HAVOC_SKILL,
    910270: DEMON_HUNTER_HAVOC_SKILL,
    910271: DEMON_HUNTER_VENGEANCE_SKILL,
    910272: DEMON_HUNTER_VENGEANCE_SKILL,
    910273: DEMON_HUNTER_VENGEANCE_SKILL,
    910274: DEMON_HUNTER_VENGEANCE_SKILL,
    910275: DEMON_HUNTER_VENGEANCE_SKILL,
    910276: DEMON_HUNTER_VENGEANCE_SKILL,
    910277: DEMON_HUNTER_VENGEANCE_SKILL,
    910278: DEMON_HUNTER_VENGEANCE_SKILL,
    910279: DEMON_HUNTER_VENGEANCE_SKILL,
    910280: DEMON_HUNTER_VENGEANCE_SKILL,
}
DEMON_HUNTER_VISUAL_EFFECTS = {
    910501: ("GPT Demon's Bite Cast", "Spells\\cfx_demonhunter_demonsbite_impact.mdx", "cfx_demonhunter_demonsbite_impact"),
    910502: ("GPT Demon's Bite Impact", "Spells\\cfx_demonhunter_demonsbite_impact.mdx", "cfx_demonhunter_demonsbite_impact"),
    910503: ("GPT Chaos Strike Cast", "Spells\\shadowflame_cast_hand.mdx", "shadowflame_cast_hand"),
    910504: ("GPT Chaos Strike Impact", "Spells\\cfx_demonhunter_chaosstrike_impact.mdx", "cfx_demonhunter_chaosstrike_impact"),
    910505: ("GPT Throw Glaive Missile", "Spells\\7fx_demonhunter_warglaivesofthedeceiver_missile.mdx", "7fx_demonhunter_warglaivesofthedeceiver_missile"),
    910506: ("GPT Throw Glaive Impact", "Spells\\hunter_glaiveleft_impact.mdx", "hunter_glaiveleft_impact"),
    910507: ("GPT Fel Rush Channel", "Spells\\11fx_felrush_channel.mdx", "11fx_felrush_channel"),
    # Fel Rush's retail state model currently crashes the 3.3.5a renderer when
    # cast. Keep its custom visual rows out of the client patch until the model
    # conversion is stable.
    910510: ("GPT Eye Beam Channel", "Spells\\cfx_demonhunter_eyebeam_channelbase.mdx", "cfx_demonhunter_eyebeam_channelbase"),
    910511: ("GPT Eye Beam Impact", "Spells\\cfx_demonhunter_eyebeam_beamimpact.mdx", "cfx_demonhunter_eyebeam_beamimpact"),
    910512: ("GPT Blade Dance Impact", "Spells\\cfx_demonhunter_bladedance_impactbase.mdx", "cfx_demonhunter_bladedance_impactbase"),
    910513: ("GPT Immolation Aura Cast", "Spells\\cfx_demonhunter_immolationaura_castbase.mdx", "cfx_demonhunter_immolationaura_castbase"),
    910514: ("GPT Immolation Aura State", "Spells\\cfx_demonhunter_immolationaura_statewaist.mdx", "cfx_demonhunter_immolationaura_statewaist"),
    910515: ("GPT Metamorphosis Impact", "Spells\\cfx_demonhunter_metamorphosisdps_impactbase.mdx", "cfx_demonhunter_metamorphosisdps_impactbase"),
    910516: ("GPT Chaos Nova Cast", "Spells\\cfx_demonhunter_chaosnova_castbase.mdx", "cfx_demonhunter_chaosnova_castbase"),
    910517: ("GPT Darkness Impact", "Spells\\cfx_demonhunter_darkness_impactbase.mdx", "cfx_demonhunter_darkness_impactbase"),
    910518: ("GPT Darkness State", "Spells\\cfx_demonhunter_darkness_state.mdx", "cfx_demonhunter_darkness_state"),
    910519: ("GPT Demon Spikes State", "Spells\\cfx_demonhunter_demonspikes_statechest.mdx", "cfx_demonhunter_demonspikes_statechest"),
    910520: ("GPT Fiery Brand Impact", "Spells\\cfx_demonhunter_fierybrand_impactplayername.mdx", "cfx_demonhunter_fierybrand_impactplayername"),
    910521: ("GPT Sigil Flame Cast", "Spells\\cfx_demonhunter_sigilofflame_castworld.mdx", "cfx_demonhunter_sigilofflame_castworld"),
    910522: ("GPT Sigil Flame Impact", "Spells\\cfx_demonhunter_sigilofflame_impactworld.mdx", "cfx_demonhunter_sigilofflame_impactworld"),
    910523: ("GPT Sigil Misery Cast", "Spells\\cfx_demonhunter_sigilofmisery_castworld.mdx", "cfx_demonhunter_sigilofmisery_castworld"),
    910524: ("GPT Sigil Misery Impact", "Spells\\cfx_demonhunter_sigilofmisery_impactworld.mdx", "cfx_demonhunter_sigilofmisery_impactworld"),
    910525: ("GPT Sigil Silence Cast", "Spells\\cfx_demonhunter_sigilofsilence_castworld.mdx", "cfx_demonhunter_sigilofsilence_castworld"),
    910526: ("GPT Sigil Silence Impact", "Spells\\cfx_demonhunter_sigilofsilence_impactworld.mdx", "cfx_demonhunter_sigilofsilence_impactworld"),
    910527: ("GPT Sigil Chains Cast", "Spells\\cfx_demonhunter_sigilofchains_castworld.mdx", "cfx_demonhunter_sigilofchains_castworld"),
    910528: ("GPT Sigil Chains Impact", "Spells\\cfx_demonhunter_sigilofchains_impactworld.mdx", "cfx_demonhunter_sigilofchains_impactworld"),
    910529: ("GPT The Hunt Precast", "Spells\\cfx_demonhunter_thehunt_precast.mdx", "cfx_demonhunter_thehunt_precast"),
    910530: ("GPT The Hunt Impact", "Spells\\cfx_demonhunter_thehunt_impact.mdx", "cfx_demonhunter_thehunt_impact"),
    910531: ("GPT Vengeful Retreat Impact", "Spells\\cfx_demonhunter_vengefulretreat_impactbase.mdx", "cfx_demonhunter_vengefulretreat_impactbase"),
    910532: ("GPT Demon Hunter Wings", "Spells\\cfx_demonhunter_wings.mdx", "cfx_demonhunter_wings"),
    910533: ("GPT Shattered Souls Impact", "Spells\\cfx_demonhunter_shatteredsouls_impact.mdx", "cfx_demonhunter_shatteredsouls_impact"),
    910534: ("GPT Soul Carver Impact", "Spells\\7fx_demonhunter_soulcarver_impact.mdx", "7fx_demonhunter_soulcarver_impact"),
}
DEMON_HUNTER_VISUAL_KITS = {
    910401: (733, {6: 910501, 7: 910501, 9: 910501, 10: 910501}),
    910402: (3049, {4: 910502}),
    910403: (7086, {6: 910503, 7: 910503, 9: 910503, 10: 910503}),
    910404: (9840, {4: 910504}),
    910405: (394, {6: 910505, 7: 910505, 9: 910505, 10: 910505}),
    910406: (437, {4: 910506}),
    910407: (867, {4: 910507, 5: 910507}),
    910409: (7712, {5: 910510}),
    910410: (437, {4: 910511}),
    910411: (12317, {4: 910512}),
    910412: (5423, {4: 910513, 5: 910514}),
    910413: (12038, {4: 910515}),
    910414: (7732, {4: 910516}),
    910415: (33206, {4: 910517, 5: 910518}),
    910416: (5277, {5: 910519}),
    910417: (11366, {4: 910520}),
    910418: (26573, {4: 910522, 5: 910521}),
    910419: (8122, {4: 910524, 5: 910523}),
    910420: (15487, {4: 910526, 5: 910525}),
    910430: (122, {4: 910528, 5: 910527}),
    910431: (100, {3: 910529, 4: 910530}),
    910432: (781, {4: 910531}),
    910433: (130, {5: 910532}),
    910434: (1949, {4: 910533}),
    910435: (11366, {4: 910534}),
}
DEMON_HUNTER_SPELL_VISUALS = {
    910201: 910421,
    910202: 910422,
    # Throw Glaive uses the glaive missile/impact visual so the projectile reads
    # as fel magic instead of a plain helper model.
    910203: 910423,
    # Fel Rush keeps its current movement animation, with a lightweight channel
    # overlay. Do not stage or reference the crashy retail state model.
    910204: 910424,
    910205: 910425,
    910206: 910426,
    910207: 910427,
    910208: 910440,
    910210: 910428,
    910212: 910429,
    910220: 910431,
    910221: 910432,
    910222: 910433,
    910223: 910421,
    910224: 910426,
    910225: 910430,
    910226: 910441,
    910227: 910425,
    910228: 910434,
    910229: 910435,
    910230: 910436,
    910231: 910437,
    910234: 910438,
    910236: 910422,
    910237: 910426,
    910238: 910425,
    910239: 910428,
    910241: 910421,
    910242: 910427,
    910244: 910439,
    910246: 910422,
    910247: 910429,
    910248: 910427,
    910251: 910427,
    910252: 910423,
    910255: 910433,
    910256: 910433,
    910258: 910429,
    910259: 910432,
    910260: 910428,
    910261: 910422,
    910262: 910426,
    910263: 910426,
    910264: 910427,
    910265: 910422,
    910266: 910422,
    910267: 910428,
    910268: 910440,
    910269: 910432,
    910270: 910428,
    910271: 910427,
    910272: 910431,
    910273: 910433,
    910274: 910438,
    910275: 910434,
    910276: 910431,
    910277: 910432,
    910278: 910432,
    910279: 910425,
    910280: 910428,
}
GOBLIN_MASK = 1 << (GOBLIN_RACE - 1)
WORGEN_MASK = 1 << (WORGEN_RACE - 1)
OLD_WORGEN_MASK = 1 << (OLD_WORGEN_RACE - 1)
ORC_MASK = 1 << (2 - 1)
HUMAN_MASK = 1 << (1 - 1)
NIGHTELF_MASK = 1 << (4 - 1)
DEMON_HUNTER_RACE_MASK = NIGHTELF_MASK | (1 << (10 - 1))
HORDE_MASK = ORC_MASK | (1 << (5 - 1)) | (1 << (6 - 1)) | (1 << (8 - 1)) | (1 << (10 - 1)) | GOBLIN_MASK
ALLIANCE_MASK = HUMAN_MASK | (1 << (3 - 1)) | NIGHTELF_MASK | (1 << (7 - 1)) | (1 << (11 - 1)) | WORGEN_MASK
OLD_HORDE_MASK = HORDE_MASK
OLD_ALLIANCE_MASK = HUMAN_MASK | (1 << (3 - 1)) | NIGHTELF_MASK | (1 << (7 - 1)) | (1 << (11 - 1)) | OLD_WORGEN_MASK

GOBLIN_CLASSES = [1, 3, 4, 5, 6, 7, 8, 9]
WORGEN_CLASSES = [1, 3, 4, 5, 6, 8, 9, 11]
RETAIL_ICON_DIR = Path(r"C:\Users\monty\OneDrive\Desktop\Model Extraction\interface\icons")
DEMON_HUNTER_ICON_DIR = DEMON_HUNTER_ASSET_DIR / "interface" / "icons"
CHARACTER_MODEL_SOURCES = [
    (MODEL_EXTRACTION_CHARACTER / "goblin" / "male", r"Character\Goblin\Male", "GoblinMale", "goblinmale_sdr.m2", "goblinmale_sdr00.skin"),
    (MODEL_EXTRACTION_CHARACTER / "goblin" / "female", r"Character\Goblin\Female", "GoblinFemale", "goblinfemale_sdr.m2", "goblinfemale_sdr00.skin"),
    (MODEL_EXTRACTION_CHARACTER / "worgen" / "male", r"Character\Worgen\Male", "WorgenMale", "worgenmale_sdr.m2", "worgenmale_sdr00.skin"),
    (MODEL_EXTRACTION_CHARACTER / "worgen" / "female", r"Character\Worgen\Female", "WorgenFemale", "worgenfemale_sdr.m2", "worgenfemale_sdr00.skin"),
]
CHARACTER_MODEL_TEXTURE_OVERRIDES = {
    "GoblinMale": {0: "goblinmaleskin00_00.blp", 1: "goblinmalefaceupper00_00.blp"},
    "GoblinFemale": {0: "goblinfemaleskin00_00.blp", 1: "goblinfemalefaceupper00_00.blp"},
    "WorgenMale": {0: "worgenmaleskin00_00.blp", 1: "worgenmalefaceupper00_00.blp"},
    "WorgenFemale": {0: "worgenfemaleskin00_00.blp", 1: "worgenfemalefaceupper00_00.blp"},
}
CHARACTER_DISPLAY_IDS = {
    "GoblinMale": 910090,
    "GoblinFemale": 910091,
    "WorgenMale": 910120,
    "WorgenFemale": 910121,
}

# The modern extracted Goblin/Worgen M2s currently crash the 3.3.5a client even
# after the lightweight downport pass. Keep the race/class work usable by
# falling back to native character display rows until the model conversion is
# complete enough for the character renderer.
ENABLE_CUSTOM_CHARACTER_MODELS = False
USE_WORGOBLIN_VENDOR_PATCH = True
SAFE_CHARACTER_DISPLAY_IDS = {
    "GoblinMale": 51,      # Orc male
    "GoblinFemale": 52,    # Orc female
    "WorgenMale": 49,      # Human male
    "WorgenFemale": 50,    # Human female
}

RACIAL_SPELLS = {
    69041: ("Rocket Barrage", "Launches your belt rockets at an enemy, causing Fire damage.", "Interface\\Icons\\INV_Gizmo_RocketLauncher"),
    69042: ("Time is Money", "Attack and casting speed increased by 1%.", "Interface\\Icons\\INV_Gizmo_GoblinBoomBox_01"),
    69044: ("Best Deals Anywhere", "Always receive the best possible vendor discount.", "Interface\\Icons\\INV_Misc_Coin_02"),
    69045: ("Better Living Through Chemistry", "Alchemy skill increased.", "Interface\\Icons\\Trade_Alchemy"),
    69046: ("Pack Hobgoblin", "Calls in your trusted pack hobgoblin.", "Interface\\Icons\\INV_Misc_Bag_10"),
    69070: ("Rocket Jump", "Activates your rocket belt to leap forward.", "Interface\\Icons\\ability_vehicle_rocketboost"),
    68975: ("Viciousness", "Critical strike chance increased by 1%.", "Interface\\Icons\\Ability_CriticalStrike"),
    68976: ("Aberration", "Reduces the chance you will be hit by Nature and Shadow spells.", "Interface\\Icons\\Spell_Nature_ResistMagic"),
    68978: ("Flayer", "Skinning skill increased.", "Interface\\Icons\\INV_Misc_Pelt_Wolf_01"),
    68992: ("Darkflight", "Activates your true form, increasing movement speed for a short time.", "Interface\\Icons\\Ability_Druid_Dash"),
    68996: ("Two Forms", "Turn into your currently inactive form.", "Interface\\Icons\\Ability_Hunter_Pet_Wolf"),
    87840: ("Running Wild", "Drop to all fours to run as fast as a wild beast.", "Interface\\Icons\\Ability_Mount_BlackDireWolf"),
}

SPELL_NAME_FIELDS = range(136, 152)
SPELL_NAME_FLAG = 152
SPELL_RANK_FIELDS = range(153, 169)
SPELL_RANK_FLAG = 169
SPELL_DESCRIPTION_FIELDS = range(170, 186)
SPELL_DESCRIPTION_FLAG = 186
SPELL_AURA_DESCRIPTION_FIELDS = range(187, 203)
SPELL_AURA_DESCRIPTION_FLAG = 203


class DBC:
    def __init__(self, path: Path):
        self.path = path
        self.data = path.read_bytes()
        magic, self.rows, self.fields, self.record_size, self.string_size = struct.unpack_from("<4sIIII", self.data, 0)
        if magic != b"WDBC":
            raise ValueError(f"{path} is not a WDBC file")
        self.records = [
            bytearray(self.data[20 + i * self.record_size:20 + (i + 1) * self.record_size])
            for i in range(self.rows)
        ]
        self.strings = bytearray(self.data[20 + self.rows * self.record_size:20 + self.rows * self.record_size + self.string_size])

    def u32_rows(self):
        if self.record_size != self.fields * 4:
            raise ValueError(f"{self.path.name} is not a flat uint32 DBC")
        return [list(struct.unpack("<" + "I" * self.fields, rec)) for rec in self.records]

    def set_u32_rows(self, rows):
        self.record_size = self.fields * 4
        self.records = [bytearray(struct.pack("<" + "I" * self.fields, *row)) for row in rows]

    def add_string(self, text: str) -> int:
        if not text:
            return 0
        raw = text.encode("utf-8") + b"\0"
        found = bytes(self.strings).find(raw)
        if found >= 0:
            return found
        offset = len(self.strings)
        self.strings.extend(raw)
        return offset

    def write(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            f.write(struct.pack("<4sIIII", b"WDBC", len(self.records), self.fields, self.record_size, len(self.strings)))
            for rec in self.records:
                if len(rec) != self.record_size:
                    raise ValueError(f"{self.path.name} record has wrong size")
                f.write(rec)
            f.write(self.strings)


def assert_spell_visual(path: Path, spell_id: int, expected_visual: int, label: str):
    spell = DBC(path)
    row = next((record for record in spell.u32_rows() if record[0] == spell_id), None)
    if row is None:
        raise ValueError(f"{label} is missing spell {spell_id}")
    if row[131] != expected_visual or row[132] != 0:
        raise ValueError(f"{label} spell {spell_id} has unexpected visuals {row[131]}/{row[132]}; expected {expected_visual}/0")


def assert_unsafe_spell_visual_models_absent(staging: Path):
    staged_spells = staging / "Spells"
    if not staged_spells.exists():
        return
    unsafe = []
    for stem in UNSAFE_DEMON_HUNTER_SPELL_VISUAL_STEMS:
        unsafe.extend(staged_spells.glob(f"{stem}*"))
    if unsafe:
        names = ", ".join(path.name for path in sorted(unsafe))
        raise ValueError(f"Unsafe Demon Hunter spell visual models were staged: {names}")


def fill_localized(row, fields, flag_field, offset):
    for field in fields:
        row[field] = offset
    row[flag_field] = 0xFFFF


def f32_bits(value: float) -> int:
    return struct.unpack("<I", struct.pack("<f", value))[0]


def patched_chr_races() -> Path:
    dbc = DBC(SERVER_DBC / "ChrRaces.dbc")
    rows = dbc.u32_rows()
    strings = dbc
    display_ids = CHARACTER_DISPLAY_IDS if ENABLE_CUSTOM_CHARACTER_MODELS else SAFE_CHARACTER_DISPLAY_IDS

    rows = [row for row in rows if row[0] not in (WORGEN_RACE, OLD_WORGEN_RACE)]
    goblin = next(row for row in rows if row[0] == GOBLIN_RACE)
    human = next(row for row in rows if row[0] == 1)

    goblin[1] = goblin[1] & ~0x01
    goblin[2] = 2
    goblin[4] = display_ids["GoblinMale"]
    goblin[5] = display_ids["GoblinFemale"]
    goblin[7] = 1
    goblin[13] = 1
    goblin[68] = 2

    worgen = list(human)
    worgen[0] = WORGEN_RACE
    worgen[1] = (worgen[1] & ~0x01) | 0x04
    worgen[2] = 1
    worgen[4] = display_ids["WorgenMale"]
    worgen[5] = display_ids["WorgenFemale"]
    worgen[6] = strings.add_string("Wo")
    worgen[7] = 7
    worgen[11] = strings.add_string("Worgen")
    worgen[12] = 0
    worgen[13] = 0
    fill_localized(worgen, range(14, 30), 30, strings.add_string("Worgen"))
    fill_localized(worgen, range(31, 47), 47, strings.add_string("Worgen"))
    fill_localized(worgen, range(48, 64), 64, strings.add_string("Worgen"))
    worgen[65] = strings.add_string("NORMAL")
    worgen[66] = strings.add_string("NONE")
    worgen[67] = strings.add_string("NORMAL")
    worgen[68] = 2
    rows.append(worgen)

    rows.sort(key=lambda row: row[0])
    dbc.set_u32_rows(rows)
    out = OUT_DIR / "ChrRaces.dbc"
    dbc.write(out)
    return out


def patched_char_base_info() -> Path:
    dbc = DBC(SERVER_DBC / "CharBaseInfo.dbc")
    pairs = {(rec[0], rec[1]) for rec in dbc.records if rec[0] not in (WORGEN_RACE, OLD_WORGEN_RACE)}
    for cls in GOBLIN_CLASSES:
        pairs.add((GOBLIN_RACE, cls))
    for cls in WORGEN_CLASSES:
        pairs.add((WORGEN_RACE, cls))
    dbc.records = [bytearray([race, cls]) for race, cls in sorted(pairs)]
    out = OUT_DIR / "CharBaseInfo.dbc"
    dbc.write(out)
    return out


def patched_creature_display_models():
    model_dbc = DBC(SERVER_DBC / "CreatureModelData.dbc")
    display_dbc = DBC(SERVER_DBC / "CreatureDisplayInfo.dbc")
    model_rows_all = model_dbc.u32_rows()
    display_rows_all = display_dbc.u32_rows()
    model_by_id = {row[0]: row for row in model_rows_all}
    display_by_id = {row[0]: row for row in display_rows_all}
    model_rows = [row for row in model_rows_all if row[0] not in CHARACTER_DISPLAY_IDS.values()]
    display_rows = [row for row in display_rows_all if row[0] not in CHARACTER_DISPLAY_IDS.values()]

    if not ENABLE_CUSTOM_CHARACTER_MODELS:
        model_dbc.set_u32_rows(model_rows)
        display_dbc.set_u32_rows(display_rows)
        model_out = OUT_DIR / "CreatureModelData.dbc"
        display_out = OUT_DIR / "CreatureDisplayInfo.dbc"
        model_dbc.write(model_out)
        display_dbc.write(display_out)
        return [model_out, display_out]

    model_paths = {
        "GoblinMale": r"Character\Goblin\Male\GoblinMale.mdx",
        "GoblinFemale": r"Character\Goblin\Female\GoblinFemale.mdx",
        "WorgenMale": r"Character\Worgen\Male\WorgenMale.mdx",
        "WorgenFemale": r"Character\Worgen\Female\WorgenFemale.mdx",
    }
    source_display_ids = {
        "GoblinMale": 51,      # Orc male
        "GoblinFemale": 52,    # Orc female
        "WorgenMale": 49,      # Human male
        "WorgenFemale": 50,    # Human female
    }

    for name, display_id in CHARACTER_DISPLAY_IDS.items():
        model_id = display_id
        source_display_id = source_display_ids[name]
        source_display = list(display_by_id[source_display_id])
        source_model = list(model_by_id[source_display[1]])

        source_model[0] = model_id
        source_model[2] = model_dbc.add_string(model_paths[name])
        display_rows.append([display_id, model_id, *source_display[2:]])
        model_rows.append(source_model)

    model_rows.sort(key=lambda row: row[0])
    display_rows.sort(key=lambda row: row[0])
    model_dbc.set_u32_rows(model_rows)
    display_dbc.set_u32_rows(display_rows)
    model_out = OUT_DIR / "CreatureModelData.dbc"
    display_out = OUT_DIR / "CreatureDisplayInfo.dbc"
    model_dbc.write(model_out)
    display_dbc.write(display_out)
    return [model_out, display_out]


def patched_char_start_outfit() -> Path:
    dbc = DBC(SERVER_DBC / "CharStartOutfit.dbc")
    records = {}
    max_id = 0
    for rec in dbc.records:
        entry = struct.unpack_from("<I", rec, 0)[0]
        race, cls, gender = struct.unpack_from("<BBB", rec, 4)
        if race in (WORGEN_RACE, OLD_WORGEN_RACE):
            max_id = max(max_id, entry)
            continue
        records[(race, cls, gender)] = bytearray(rec)
        max_id = max(max_id, entry)

    source_for = {
        (GOBLIN_RACE, 1): 2,
        (GOBLIN_RACE, 3): 2,
        (GOBLIN_RACE, 4): 2,
        (GOBLIN_RACE, 5): 8,
        (GOBLIN_RACE, 6): 2,
        (GOBLIN_RACE, 7): 2,
        (GOBLIN_RACE, 8): 5,
        (GOBLIN_RACE, 9): 2,
        (WORGEN_RACE, 1): 1,
        (WORGEN_RACE, 3): 4,
        (WORGEN_RACE, 4): 1,
        (WORGEN_RACE, 5): 1,
        (WORGEN_RACE, 6): 1,
        (WORGEN_RACE, 8): 1,
        (WORGEN_RACE, 9): 1,
        (WORGEN_RACE, 11): 4,
    }

    for (race, cls), source_race in source_for.items():
        for gender in (0, 1):
            source = records[(source_race, cls, gender)]
            max_id += 1
            rec = bytearray(source)
            struct.pack_into("<I", rec, 0, max_id)
            struct.pack_into("<BBB", rec, 4, race, cls, gender)
            records[(race, cls, gender)] = rec

    dbc.records = sorted(records.values(), key=lambda rec: struct.unpack_from("<I", rec, 0)[0])
    out = OUT_DIR / "CharStartOutfit.dbc"
    dbc.write(out)
    return out


def patched_skill_race_class_info() -> Path:
    dbc = DBC(SERVER_DBC / "SkillRaceClassInfo.dbc")
    rows = dbc.u32_rows()
    skill_line = DBC(SERVER_DBC / "SkillLine.dbc")
    skill_ids = {row[0] for row in skill_line.u32_rows()}

    # An earlier build accidentally ORed race-mask bits into field 1 (SkillID)
    # instead of field 2 (RaceMask). If this builder is run on that DBC, restore
    # the original candidate rows by adding valid SkillID variants back in.
    recovered = []
    for row in rows:
        skill_id = row[1]
        for mask in (GOBLIN_MASK, WORGEN_MASK, GOBLIN_MASK | WORGEN_MASK):
            if (skill_id & mask) != mask:
                continue
            candidate = skill_id - mask
            if candidate not in skill_ids:
                continue
            buggy = candidate
            if candidate & ORC_MASK:
                buggy |= GOBLIN_MASK
            if candidate & (HUMAN_MASK | NIGHTELF_MASK):
                buggy |= WORGEN_MASK
            if buggy == skill_id:
                restored = list(row)
                restored[1] = candidate
                recovered.append(restored)
    rows.extend(recovered)

    for row in rows:
        row[2] &= ~OLD_WORGEN_MASK
        if row[2] & ORC_MASK:
            row[2] |= GOBLIN_MASK
        if row[2] & (HUMAN_MASK | NIGHTELF_MASK):
            row[2] |= WORGEN_MASK
    deduped = []
    seen = set()
    for row in rows:
        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    rows = deduped
    dbc.set_u32_rows(rows)
    out = OUT_DIR / "SkillRaceClassInfo.dbc"
    dbc.write(out)
    return out


def patched_factions() -> list[Path]:
    faction = DBC(SERVER_DBC / "Faction.dbc")
    rows = [row for row in faction.u32_rows() if row[0] not in (1133, 1134)]

    for row in rows:
        for idx in range(2, 6):
            if row[idx] in (690, OLD_HORDE_MASK):
                row[idx] = HORDE_MASK
            elif row[idx] in (1101, OLD_ALLIANCE_MASK):
                row[idx] = ALLIANCE_MASK

    rows.sort(key=lambda row: row[0])
    faction.set_u32_rows(rows)
    faction_out = OUT_DIR / "Faction.dbc"
    faction.write(faction_out)

    templates = DBC(SERVER_DBC / "FactionTemplate.dbc")
    t_rows = [row for row in templates.u32_rows() if row[0] not in (19000, 19001)]
    t_rows.sort(key=lambda row: row[0])
    templates.set_u32_rows(t_rows)
    templates_out = OUT_DIR / "FactionTemplate.dbc"
    templates.write(templates_out)

    return [faction_out, templates_out]


def by_template(rows, template_id):
    return next(row for row in rows if row[0] == template_id)


def empty_spell_row(fields: int, spell_id: int, name: str, description: str, strings: DBC):
    row = [0] * fields
    row[0] = spell_id
    row[28] = 1
    row[40] = 21
    row[46] = 1
    fill_localized(row, SPELL_NAME_FIELDS, SPELL_NAME_FLAG, strings.add_string(name))
    fill_localized(row, SPELL_RANK_FIELDS, SPELL_RANK_FLAG, 0)
    fill_localized(row, SPELL_DESCRIPTION_FIELDS, SPELL_DESCRIPTION_FLAG, strings.add_string(description))
    fill_localized(row, SPELL_AURA_DESCRIPTION_FIELDS, SPELL_AURA_DESCRIPTION_FLAG, strings.add_string(description))
    return row


def patched_racial_spells() -> list[Path]:
    spell = DBC(OUT_DIR / "Spell.dbc" if (OUT_DIR / "Spell.dbc").exists() else SERVER_DBC / "Spell.dbc")
    rows = [row for row in spell.u32_rows() if row[0] not in RACIAL_SPELLS]
    templates = {row[0]: row for row in rows}

    def clone(template_id, spell_id, name, desc):
        row = list(templates[template_id])
        row[0] = spell_id
        fill_localized(row, SPELL_NAME_FIELDS, SPELL_NAME_FLAG, spell.add_string(name))
        fill_localized(row, SPELL_RANK_FIELDS, SPELL_RANK_FLAG, 0)
        fill_localized(row, SPELL_DESCRIPTION_FIELDS, SPELL_DESCRIPTION_FLAG, spell.add_string(desc))
        fill_localized(row, SPELL_AURA_DESCRIPTION_FIELDS, SPELL_AURA_DESCRIPTION_FLAG, spell.add_string(desc))
        return row

    custom = [
        clone(133, 69041, *RACIAL_SPELLS[69041][:2]),
        clone(2983, 68992, *RACIAL_SPELLS[68992][:2]),
        clone(20593, 69045, *RACIAL_SPELLS[69045][:2]),
        clone(20592, 68976, *RACIAL_SPELLS[68976][:2]),
        clone(20593, 68978, *RACIAL_SPELLS[68978][:2]),
        clone(59752, 68996, *RACIAL_SPELLS[68996][:2]),
        empty_spell_row(spell.fields, 69042, *RACIAL_SPELLS[69042][:2], spell),
        empty_spell_row(spell.fields, 69044, *RACIAL_SPELLS[69044][:2], spell),
        empty_spell_row(spell.fields, 69046, *RACIAL_SPELLS[69046][:2], spell),
        empty_spell_row(spell.fields, 69070, *RACIAL_SPELLS[69070][:2], spell),
        empty_spell_row(spell.fields, 68975, *RACIAL_SPELLS[68975][:2], spell),
        empty_spell_row(spell.fields, 87840, *RACIAL_SPELLS[87840][:2], spell),
    ]
    for row in custom:
        row[133] = row[0]
        row[134] = row[0]
        rows.append(row)
    rows.sort(key=lambda row: row[0])
    spell.set_u32_rows(rows)
    spell_out = OUT_DIR / "Spell.dbc"
    spell.write(spell_out)

    icons = DBC(OUT_DIR / "SpellIcon.dbc" if (OUT_DIR / "SpellIcon.dbc").exists() else SERVER_DBC / "SpellIcon.dbc")
    icon_rows = [row for row in icons.u32_rows() if row[0] not in RACIAL_SPELLS]
    for spell_id, (_name, _desc, icon) in RACIAL_SPELLS.items():
        icon_rows.append([spell_id, icons.add_string(icon)])
    icon_rows.sort(key=lambda row: row[0])
    icons.set_u32_rows(icon_rows)
    icons_out = OUT_DIR / "SpellIcon.dbc"
    icons.write(icons_out)
    return [spell_out, icons_out]


def dbc_source(staging: Path, name: str) -> Path:
    staged = staging / "DBFilesClient" / name
    if staged.exists():
        return staged
    vendor = WORGOBLIN_PATCH / "DBFilesClient" / name
    if vendor.exists():
        return vendor
    out = OUT_DIR / name
    if out.exists():
        return out
    return SERVER_DBC / name


def clone_spell(spell: DBC, rows: list[list[int]], template_id: int, spell_id: int, name: str, description: str, icon_id: int) -> list[int]:
    template = next((row for row in rows if row[0] == template_id), None)
    if template is None:
        return empty_spell_row(spell.fields, spell_id, name, description, spell)

    row = list(template)
    row[0] = spell_id
    fill_localized(row, SPELL_NAME_FIELDS, SPELL_NAME_FLAG, spell.add_string(name))
    fill_localized(row, SPELL_RANK_FIELDS, SPELL_RANK_FLAG, 0)
    fill_localized(row, SPELL_DESCRIPTION_FIELDS, SPELL_DESCRIPTION_FLAG, spell.add_string(description))
    fill_localized(row, SPELL_AURA_DESCRIPTION_FIELDS, SPELL_AURA_DESCRIPTION_FLAG, spell.add_string(description))
    row[133] = icon_id
    row[134] = icon_id
    return row


def patched_demon_hunter_dbcs(staging: Path) -> list[Path]:
    patched: list[Path] = []

    chr_classes = DBC(dbc_source(staging, "ChrClasses.dbc"))
    class_rows = [row for row in chr_classes.u32_rows() if row[0] not in {DEMON_HUNTER_CLASS, 12}]
    rogue = next(row for row in class_rows if row[0] == 4)
    demon_hunter = list(rogue)
    demon_hunter[0] = DEMON_HUNTER_CLASS
    demon_hunter[2] = 3  # Energy is the closest WotLK power type to Fury without a client binary patch.
    fill_localized(demon_hunter, range(4, 20), 20, chr_classes.add_string("Demon Hunter"))
    fill_localized(demon_hunter, range(21, 37), 37, chr_classes.add_string("Demon Hunter"))
    fill_localized(demon_hunter, range(38, 54), 54, chr_classes.add_string("Demon Hunter"))
    demon_hunter[55] = chr_classes.add_string("DEMONHUNTER")
    demon_hunter[59] = 2
    class_rows.append(demon_hunter)
    class_rows.sort(key=lambda row: row[0])
    chr_classes.set_u32_rows(class_rows)
    chr_classes_out = OUT_DIR / "ChrClasses.dbc"
    chr_classes.write(chr_classes_out)
    patched.append(chr_classes_out)

    base_info = DBC(dbc_source(staging, "CharBaseInfo.dbc"))
    pairs = {(rec[0], rec[1]) for rec in base_info.records}
    pairs.add((4, DEMON_HUNTER_CLASS))
    pairs.add((10, DEMON_HUNTER_CLASS))
    base_info.records = [bytearray([race, cls]) for race, cls in sorted(pairs)]
    base_info_out = OUT_DIR / "CharBaseInfo.dbc"
    base_info.write(base_info_out)
    patched.append(base_info_out)

    outfits = DBC(dbc_source(staging, "CharStartOutfit.dbc"))
    outfit_records = {}
    max_id = 0
    for rec in outfits.records:
        entry = struct.unpack_from("<I", rec, 0)[0]
        race, cls, gender = struct.unpack_from("<BBB", rec, 4)
        outfit_records[(race, cls, gender)] = bytearray(rec)
        max_id = max(max_id, entry)

    for race, template_race in ((4, 4), (10, 10)):
        for gender in (0, 1):
            source = outfit_records.get((template_race, 4, gender))
            if source is None:
                continue
            max_id += 1
            rec = bytearray(source)
            struct.pack_into("<I", rec, 0, max_id)
            struct.pack_into("<BBB", rec, 4, race, DEMON_HUNTER_CLASS, gender)
            struct.pack_into("<i", rec, 8, DEMON_HUNTER_MAIN_HAND)
            struct.pack_into("<i", rec, 12, DEMON_HUNTER_OFF_HAND)
            outfit_records[(race, DEMON_HUNTER_CLASS, gender)] = rec
    outfits.records = sorted(outfit_records.values(), key=lambda rec: struct.unpack_from("<I", rec, 0)[0])
    outfits_out = OUT_DIR / "CharStartOutfit.dbc"
    outfits.write(outfits_out)
    patched.append(outfits_out)

    skill_line = DBC(dbc_source(staging, "SkillLine.dbc"))
    skill_rows = [row for row in skill_line.u32_rows() if row[0] not in DEMON_HUNTER_SPELLBOOK_SKILLS]
    combat = next(row for row in skill_rows if row[0] == 38)
    for skill_id, (name, description) in DEMON_HUNTER_SPELLBOOK_SKILLS.items():
        dh_skill = list(combat)
        dh_skill[0] = skill_id
        fill_localized(dh_skill, range(3, 19), 19, skill_line.add_string(name))
        fill_localized(dh_skill, range(20, 36), 36, skill_line.add_string(description))
        skill_rows.append(dh_skill)
    skill_rows.sort(key=lambda row: row[0])
    skill_line.set_u32_rows(skill_rows)
    skill_line_out = OUT_DIR / "SkillLine.dbc"
    skill_line.write(skill_line_out)
    patched.append(skill_line_out)

    skill_race_class = DBC(dbc_source(staging, "SkillRaceClassInfo.dbc"))
    src_rows = skill_race_class.u32_rows()
    skill_rows = [row for row in src_rows if not (row[2] == DEMON_HUNTER_RACE_MASK and row[3] in {DEMON_HUNTER_MASK, 2048})]
    wanted_skills = {43, 95, 98, 109, 113, 137, 162, 173, 176, 414, 415, 473, 777, 778}
    next_id = max(row[0] for row in skill_rows) + 1
    for skill_id in sorted(wanted_skills | set(DEMON_HUNTER_SPELLBOOK_SKILLS)):
        source = next((list(row) for row in src_rows if row[1] == skill_id and (row[3] == 0 or (row[3] & (1 << (4 - 1))))), None)
        if source is None:
            source = [next_id, skill_id, DEMON_HUNTER_RACE_MASK, DEMON_HUNTER_MASK, 1040, 0, 0, 0]
        else:
            source[0] = next_id
            source[2] = DEMON_HUNTER_RACE_MASK
            source[3] = DEMON_HUNTER_MASK
        skill_rows.append(source)
        next_id += 1
    skill_rows.sort(key=lambda row: row[0])
    skill_race_class.set_u32_rows(skill_rows)
    skill_race_class_out = OUT_DIR / "SkillRaceClassInfo.dbc"
    skill_race_class.write(skill_race_class_out)
    patched.append(skill_race_class_out)

    spell_icons = DBC(OUT_DIR / "SpellIcon.dbc" if (OUT_DIR / "SpellIcon.dbc").exists() else dbc_source(staging, "SpellIcon.dbc"))
    icon_rows = [row for row in spell_icons.u32_rows() if row[0] not in DEMON_HUNTER_SPELLS and row[0] not in {DEMON_HUNTER_CLASS, 12}]
    for spell_id, (_name, _desc, icon, _template) in DEMON_HUNTER_SPELLS.items():
        icon_rows.append([spell_id, spell_icons.add_string(f"Interface\\Icons\\{icon}")])
    icon_rows.append([DEMON_HUNTER_CLASS, spell_icons.add_string("Interface\\Icons\\classicon_demonhunter")])
    icon_rows.sort(key=lambda row: row[0])
    spell_icons.set_u32_rows(icon_rows)
    spell_icons_out = OUT_DIR / "SpellIcon.dbc"
    spell_icons.write(spell_icons_out)
    patched.append(spell_icons_out)

    spell = DBC(OUT_DIR / "Spell.dbc" if (OUT_DIR / "Spell.dbc").exists() else dbc_source(staging, "Spell.dbc"))
    spell_rows = [row for row in spell.u32_rows() if row[0] not in DEMON_HUNTER_SPELLS]
    for spell_id, (name, desc, _icon, template_id) in DEMON_HUNTER_SPELLS.items():
        custom_spell = clone_spell(spell, spell_rows, template_id, spell_id, name, desc, spell_id)
        custom_spell[42] = 40 if spell_id == 910202 else 0
        if spell_id in DEMON_HUNTER_SPELL_VISUALS:
            custom_spell[131] = DEMON_HUNTER_SPELL_VISUALS[spell_id]
            custom_spell[132] = 0
        custom_spell[206] = 1000
        spell_rows.append(custom_spell)
    spell_rows.sort(key=lambda row: row[0])
    spell.set_u32_rows(spell_rows)
    spell_out = OUT_DIR / "Spell.dbc"
    spell.write(spell_out)
    assert_spell_visual(spell_out, 910204, 910424, "rebuilt Demon Hunter Spell.dbc")
    patched.append(spell_out)

    ability = DBC(dbc_source(staging, "SkillLineAbility.dbc"))
    ability_rows = [row for row in ability.u32_rows() if row[2] not in DEMON_HUNTER_SPELLS]
    next_ability_id = max(row[0] for row in ability_rows) + 1
    for spell_id in sorted(DEMON_HUNTER_SPELLS):
        ability_rows.append([next_ability_id, DEMON_HUNTER_SPELL_SKILLS[spell_id], spell_id, DEMON_HUNTER_RACE_MASK, DEMON_HUNTER_MASK, 0, 0, 1, 0, 2, 0, 0, 0, 0])
        next_ability_id += 1
    ability_rows.sort(key=lambda row: row[0])
    ability.set_u32_rows(ability_rows)
    ability_out = OUT_DIR / "SkillLineAbility.dbc"
    ability.write(ability_out)
    patched.append(ability_out)

    for gt_name in [
        "gtChanceToMeleeCrit.dbc",
        "gtChanceToMeleeCritBase.dbc",
        "gtChanceToSpellCrit.dbc",
        "gtChanceToSpellCritBase.dbc",
        "gtOCTClassCombatRatingScalar.dbc",
    ]:
        source = dbc_source(staging, gt_name)
        gt = DBC(source)
        stride_by_name = {
            "gtChanceToMeleeCrit.dbc": 100,
            "gtChanceToMeleeCritBase.dbc": 1,
            "gtChanceToSpellCrit.dbc": 100,
            "gtChanceToSpellCritBase.dbc": 1,
            "gtOCTClassCombatRatingScalar.dbc": 32,
        }
        stride = stride_by_name[gt_name]
        base_rows = 11 * stride
        if len(gt.records) >= base_rows:
            gt.records = gt.records[:base_rows]
            rogue_start = (4 - 1) * stride
            demon_hunter_start = (DEMON_HUNTER_CLASS - 1) * stride
            gt.records[demon_hunter_start:demon_hunter_start + stride] = [
                bytearray(rec) for rec in gt.records[rogue_start:rogue_start + stride]
            ]
        gt_out = OUT_DIR / gt_name
        gt.write(gt_out)
        patched.append(gt_out)

    return patched


def patch_demon_hunter_spell_visual_dbcs(staging: Path, install_server_dbc=False):
    effect_path = staging / "DBFilesClient" / "SpellVisualEffectName.dbc"
    if not effect_path.exists():
        shutil.copy2(dbc_source(staging, "SpellVisualEffectName.dbc"), effect_path)
    effects = DBC(effect_path)
    effect_rows = [row for row in effects.u32_rows() if row[0] not in DEMON_HUNTER_VISUAL_EFFECTS]
    default_effect = next((list(row) for row in effect_rows if row[0] == 4697), None)
    if default_effect is None:
        default_effect = [0, 0, 0, f32_bits(1.0), f32_bits(1.0), f32_bits(0.01), f32_bits(100.0)]
    for effect_id, (name, model_path, _stem) in DEMON_HUNTER_VISUAL_EFFECTS.items():
        row = list(default_effect)
        row[0] = effect_id
        row[1] = effects.add_string(name)
        row[2] = effects.add_string(model_path)
        effect_rows.append(row)
    effect_rows.sort(key=lambda row: row[0])
    effects.set_u32_rows(effect_rows)
    effects.write(effect_path)

    kit_path = staging / "DBFilesClient" / "SpellVisualKit.dbc"
    if not kit_path.exists():
        shutil.copy2(dbc_source(staging, "SpellVisualKit.dbc"), kit_path)
    kits = DBC(kit_path)
    source_kit_rows = kits.u32_rows()
    kit_rows = [row for row in source_kit_rows if row[0] not in DEMON_HUNTER_VISUAL_KITS]
    for kit_id, (source_id, overrides) in DEMON_HUNTER_VISUAL_KITS.items():
        source = next((list(row) for row in source_kit_rows if row[0] == source_id), None)
        if source is None:
            source = [0] * kits.fields
        source[0] = kit_id
        for field, value in overrides.items():
            source[field] = value
        kit_rows.append(source)
    kit_rows.sort(key=lambda row: row[0])
    kits.set_u32_rows(kit_rows)
    kits.write(kit_path)

    visual_path = staging / "DBFilesClient" / "SpellVisual.dbc"
    if not visual_path.exists():
        shutil.copy2(dbc_source(staging, "SpellVisual.dbc"), visual_path)
    visuals = DBC(visual_path)
    source_visual_rows = visuals.u32_rows()
    visual_ids = {visual_id for visual_id in DEMON_HUNTER_SPELL_VISUALS.values() if visual_id}
    visual_rows = [row for row in source_visual_rows if row[0] not in visual_ids]

    visual_specs = {
        910421: (253, 0, 910401, 910402, 0, 0, 0, 0),
        910422: (11240, 0, 910403, 910404, 0, 0, 0, 0),
        910423: (11780, 0, 910405, 910406, 0, 0, 0, 910505),
        910424: (867, 0, 910407, 910407, 0, 0, 0, 0),
        910425: (12637, 0, 0, 910410, 0, 0, 910409, 0),
        910426: (12317, 0, 910411, 910411, 0, 0, 0, 0),
        910427: (5423, 0, 910412, 0, 910412, 0, 0, 0),
        910428: (12038, 0, 910413, 910413, 0, 0, 0, 0),
        910429: (7732, 0, 910414, 910414, 0, 0, 0, 0),
        910430: (33206, 0, 0, 910415, 910415, 0, 0, 0),
        910431: (5277, 0, 0, 0, 910416, 0, 0, 0),
        910432: (11366, 0, 0, 910417, 0, 0, 0, 0),
        910433: (26573, 0, 910418, 910418, 0, 0, 0, 0),
        910434: (8122, 0, 910419, 910419, 0, 0, 0, 0),
        910435: (15487, 0, 910420, 910420, 0, 0, 0, 0),
        910436: (122, 0, 910430, 910430, 0, 0, 0, 0),
        910437: (130, 0, 0, 0, 910433, 0, 0, 0),
        910438: (1949, 0, 0, 910434, 910434, 0, 0, 0),
        910439: (11366, 0, 0, 910435, 0, 0, 0, 0),
        910440: (781, 0, 0, 910432, 0, 0, 0, 0),
        910441: (100, 0, 910431, 910431, 0, 0, 0, 0),
    }
    for visual_id, (source_id, precast, casting, impact, state, state_done, channel, missile) in visual_specs.items():
        source = next((list(row) for row in source_visual_rows if row[0] == source_id), None)
        if source is None:
            source = [0] * visuals.fields
        source[0] = visual_id
        source[1] = precast
        source[2] = casting
        source[3] = impact
        source[4] = state
        source[5] = state_done
        source[6] = channel
        if missile:
            source[7] = 1
            source[8] = missile
        visual_rows.append(source)
    visual_rows.sort(key=lambda row: row[0])
    visuals.set_u32_rows(visual_rows)
    visuals.write(visual_path)

    if install_server_dbc:
        for path in (effect_path, kit_path, visual_path):
            shutil.copy2(path, SERVER_DBC / path.name)


def patch_demon_hunter_glue(staging: Path):
    glue = staging / "Interface" / "GlueXML"
    lua_path = glue / "CharacterCreate.lua"
    xml_path = glue / "CharacterCreate.xml"
    strings_path = glue / "GlueStrings.lua"

    if lua_path.exists():
        lua = lua_path.read_text(encoding="utf-8")
        lua = lua.replace("MAX_CLASSES_PER_RACE = 10;", "MAX_CLASSES_PER_RACE = 11;")
        if '["DEMONHUNTER"]' not in lua:
            lua = lua.replace(
                '\t["DEATHKNIGHT"]\t= {0.25, 0.49609375, 0.5, 0.75},\n};',
                '\t["DEATHKNIGHT"]\t= {0.25, 0.49609375, 0.5, 0.75},\n'
                '\t["DEMONHUNTER"]\t= {0.49609375, 0.7421875, 0.5, 0.75},\n};',
            )
        lua_path.write_text(lua, encoding="utf-8", newline="")

    if xml_path.exists() and "CharacterCreateClassButton11" not in xml_path.read_text(encoding="utf-8"):
        xml = xml_path.read_text(encoding="utf-8")
        insert = '''\t\t\t\t\t\t\t<CheckButton name="CharacterCreateClassButton11" inherits="CharacterCreateClassButtonTemplate" id="11">
\t\t\t\t\t\t\t\t<Anchors>
\t\t\t\t\t\t\t\t\t<Anchor point="TOP" relativeTo="CharacterCreateClassButton6" relativePoint="BOTTOM" x="0" y="-6"/>
\t\t\t\t\t\t\t\t</Anchors>
\t\t\t\t\t\t\t</CheckButton>
'''
        xml = xml.replace('\t\t\t\t\t\t\t<Button name="CharCreateRandomizeButton"', insert + '\t\t\t\t\t\t\t<Button name="CharCreateRandomizeButton"', 1)
        xml_path.write_text(xml, encoding="utf-8", newline="")

    if strings_path.exists():
        strings = strings_path.read_text(encoding="utf-8")
        if "CLASS_DEMONHUNTER" not in strings:
            strings += '\nCLASS_DEMONHUNTER = "Demon hunters are agile fel-touched fighters who wield glaives and demonic magic to hunt their enemies. They favor speed, burst movement, and relentless melee pressure.|n|nTheir primary stat is Agility. In this Wrath downport they use Energy as a Fury-like resource until a deeper client resource patch is added.";\n'
            strings += 'CLASS_DEMONHUNTER_FEMALE = CLASS_DEMONHUNTER;\n'
            strings += 'CLASS_INFO_DEMONHUNTER0 = "- Role: Tank, Damage";\n'
            strings += 'CLASS_INFO_DEMONHUNTER1 = "- Light Armor (Leather)";\n'
            strings += 'CLASS_INFO_DEMONHUNTER2 = "- Uses demonic agility and glaive techniques.";\n'
            strings += 'CLASS_INFO_DEMONHUNTER3 = "- Available to Night Elves and Blood Elves.";\n'
            strings += 'DEMONHUNTER_DISABLED = "Demon Hunter\\nAvailable to Night Elves and Blood Elves";\n'
        strings_path.write_text(strings, encoding="utf-8", newline="")


def build_demon_hunter_class_icons(staging: Path):
    sys.path.insert(0, str(WORKSPACE / "tools" / "remix_system"))
    sys.path.insert(0, r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools")
    import wow335_patch_tools as wow
    from PIL import Image

    icon_dir = staging / "Interface" / "Icons"
    icon_dir.mkdir(parents=True, exist_ok=True)
    for _spell_id, (_name, _desc, icon, _template) in DEMON_HUNTER_SPELLS.items():
        src = DEMON_HUNTER_ICON_DIR / f"{icon}.blp"
        if src.exists():
            shutil.copy2(src, icon_dir / f"{icon}.blp")
    class_icon = DEMON_HUNTER_ICON_DIR / "classicon_demonhunter.blp"
    if class_icon.exists():
        shutil.copy2(class_icon, icon_dir / "classicon_demonhunter.blp")

    base_blp = OUT_DIR / "UI-CharacterCreate-Classes.base.blp"
    if not base_blp.exists():
        subprocess.run([str(MPQCLI), "extract", str(CLIENT_LOCALE), "-o", str(OUT_DIR), "-f", r"Interface\GLUES\CHARACTERCREATE\UI-CharacterCreate-Classes.blp"], check=True)
        extracted = OUT_DIR / "UI-CharacterCreate-Classes.blp"
        if extracted.exists():
            extracted.replace(base_blp)
    if not base_blp.exists() or not class_icon.exists():
        return

    sheet = Image.open(base_blp).convert("RGBA").resize((256, 256), Image.Resampling.LANCZOS)
    icon = Image.open(class_icon).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
    sheet.paste(icon, (128, 128), icon)
    patched_png = OUT_DIR / "UI-CharacterCreate-Classes.demonhunter.png"
    patched_blp = staging / "Interface" / "GLUES" / "CHARACTERCREATE" / "UI-CharacterCreate-Classes.blp"
    patched_blp.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(patched_png)
    wow.image_to_blp2_dxt1(patched_png, patched_blp)


def patch_glue_files(staging: Path):
    lua_src = OUT_DIR / "CharacterCreate.lua.orig"
    xml_src = OUT_DIR / "CharacterCreate.xml.orig"
    if not lua_src.exists():
        subprocess.run([str(MPQCLI), "extract", str(Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\enUS\locale-enUS.MPQ")), "-o", str(OUT_DIR), "-f", r"Interface\GlueXML\CharacterCreate.lua"], check=True)
        (OUT_DIR / "CharacterCreate.lua").replace(lua_src)
    if not xml_src.exists():
        subprocess.run([str(MPQCLI), "extract", str(Path(r"C:\Program Files (x86)\ChromieCraft_3.3.5a\Data\enUS\locale-enUS.MPQ")), "-o", str(OUT_DIR), "-f", r"Interface\GlueXML\CharacterCreate.xml"], check=True)
        (OUT_DIR / "CharacterCreate.xml").replace(xml_src)

    lua = lua_src.read_text(encoding="utf-8")
    lua = lua.replace("MAX_RACES = 10;", "MAX_RACES = 12;")
    lua = lua.replace('["DRAENEI_FEMALE"]\t= {0.5, 0.625, 0.5, 0.75}, \n};',
                      '["DRAENEI_FEMALE"]\t= {0.5, 0.625, 0.5, 0.75}, \n\t["GOBLIN_MALE"]\t= {0, 0.5, 0, 0.5},\n\t["GOBLIN_FEMALE"]\t= {0.5, 1.0, 0, 0.5},\n\t["WORGEN_MALE"]\t= {0, 0.5, 0.5, 1.0},\n\t["WORGEN_FEMALE"]\t= {0.5, 1.0, 0.5, 1.0},\n};\nCUSTOM_RACE_ICON_TEXTURE = {\n\t["GOBLIN"] = "Interface\\\\Glues\\\\CharacterCreate\\\\UI-CharacterCreate-CustomRaces",\n\t["WORGEN"] = "Interface\\\\Glues\\\\CharacterCreate\\\\UI-CharacterCreate-CustomRaces",\n};')
    lua = lua.replace('coords = RACE_ICON_TCOORDS[strupper(select(i+1, ...).."_"..gender)];\n\t\tgetglobal("CharacterCreateRaceButton"..index.."NormalTexture"):SetTexCoord(coords[1], coords[2], coords[3], coords[4]);',
                      'local fileString = strupper(select(i+1, ...));\n\t\tcoords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];\n\t\tgetglobal("CharacterCreateRaceButton"..index.."NormalTexture"):SetTexture(CUSTOM_RACE_ICON_TEXTURE[fileString] or "Interface\\\\Glues\\\\CharacterCreate\\\\UI-CharacterCreate-Races");\n\t\tgetglobal("CharacterCreateRaceButton"..index.."NormalTexture"):SetTexCoord(coords[1], coords[2], coords[3], coords[4]);')
    lua = lua.replace('local coords = RACE_ICON_TCOORDS[fileString.."_"..gender];\n\tCharacterCreateRaceIcon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);',
                      'local coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];\n\tCharacterCreateRaceIcon:SetTexture(CUSTOM_RACE_ICON_TEXTURE[fileString] or "Interface\\\\Glues\\\\CharacterCreate\\\\UI-CharacterCreate-Races");\n\tCharacterCreateRaceIcon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);')
    lua = lua.replace('local race, fileString = GetNameForRace();\n\tCharacterCreateRaceLabel:SetText(race);\n\tfileString = strupper(fileString);\n\tlocal coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];',
                      'local race, fileString = GetNameForRace(GetSelectedRace());\n\tCharacterCreateRaceLabel:SetText(race);\n\tfileString = strupper(fileString);\n\tlocal coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];')
    lua += '\nRACE_INFO_GOBLIN = "        Cunning, sharp-eyed, and always watching the balance sheet, the goblins bring invention and opportunism to the Horde. These Bilgewater survivors begin their new fortunes in Durotar, where grit matters as much as gold.";\n'
    lua += 'RACE_INFO_GOBLIN_FEMALE = RACE_INFO_GOBLIN;\n'
    lua += 'ABILITY_INFO_GOBLIN1 = "- May leap forward with rocket technology.";\nABILITY_INFO_GOBLIN2 = "- May fire a belt rocket at enemies.";\nABILITY_INFO_GOBLIN3 = "- Haste increased.";\nABILITY_INFO_GOBLIN4 = "- Alchemy skill increased.";\n'
    lua += 'RACE_INFO_WORGEN = "        Behind the walls of Gilneas, a savage curse transformed proud citizens into worgen. Now disciplined by will and loyalty, they bring ferocity and resolve to the Alliance from their first steps in Elwynn Forest.";\n'
    lua += 'RACE_INFO_WORGEN_FEMALE = RACE_INFO_WORGEN;\n'
    lua += 'ABILITY_INFO_WORGEN1 = "- May run with unnatural speed.";\nABILITY_INFO_WORGEN2 = "- Critical strike chance increased.";\nABILITY_INFO_WORGEN3 = "- Resistant to Nature and Shadow effects.";\nABILITY_INFO_WORGEN4 = "- Skinning skill increased.";\n'
    lua += r'''

CUSTOM_RACE_BUTTON_SLOT = {
	["HUMAN"] = 1,
	["DWARF"] = 2,
	["NIGHTELF"] = 3,
	["GNOME"] = 4,
	["DRAENEI"] = 5,
	["WORGEN"] = 11,
	["ORC"] = 6,
	["SCOURGE"] = 7,
	["TAUREN"] = 8,
	["TROLL"] = 9,
	["BLOODELF"] = 10,
	["GOBLIN"] = 12,
};

function CharacterCreate_SetRaceButtonIcon(button, fileString, gender)
	local coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];
	getglobal(button:GetName().."NormalTexture"):SetTexture(CUSTOM_RACE_ICON_TEXTURE[fileString] or "Interface\\Glues\\CharacterCreate\\UI-CharacterCreate-Races");
	getglobal(button:GetName().."NormalTexture"):SetTexCoord(coords[1], coords[2], coords[3], coords[4]);
end

function CharacterCreate_GetGenderToken()
	local selectedSex = GetSelectedSex();
	if ( selectedSex == 1 or selectedSex == 2 ) then
		return "MALE";
	end
	return "FEMALE";
end

function CharacterCreate_TargetSelectedSex(sex)
	if ( sex == 1 ) then
		return 2;
	elseif ( sex == 2 ) then
		return 3;
	end
	return sex;
end

function CharacterCreateEnumerateRaces(...)
	CharacterCreate.numRaces = select("#", ...)/3;
	if ( CharacterCreate.numRaces > MAX_RACES ) then
		message("Too many races!  Update MAX_RACES");
		return;
	end

	local gender = CharacterCreate_GetGenderToken();

	for slot=1, MAX_RACES, 1 do
		local button = getglobal("CharacterCreateRaceButton"..slot);
		button.raceIndex = nil;
		button.tooltip = nil;
		button:Hide();
	end

	local index = 1;
	for i=1, select("#", ...), 3 do
		local fileString = strupper(select(i+1, ...));
		local slot = CUSTOM_RACE_BUTTON_SLOT[fileString] or index;
		local button = getglobal("CharacterCreateRaceButton"..slot);
		button.raceIndex = index;
		button.tooltip = select(i, ...);
		CharacterCreate_SetRaceButtonIcon(button, fileString, gender);
		button:Show();
		if ( select(i+2, ...) == 1 ) then
			button:Enable();
			SetButtonDesaturated(button);
		else
			button:Disable();
			SetButtonDesaturated(button, 1);
		end
		index = index + 1;
	end
end

CUSTOM_BACKGROUND_RACE = {
	["HUMAN"] = "HUMAN",
	["ORC"] = "ORC",
	["DWARF"] = "DWARF",
	["NIGHTELF"] = "NIGHTELF",
	["SCOURGE"] = "SCOURGE",
	["TAUREN"] = "TAUREN",
	["GNOME"] = "DWARF",
	["TROLL"] = "ORC",
	["BLOODELF"] = "BLOODELF",
	["DRAENEI"] = "DRAENEI",
	["GOBLIN"] = "ORC",
	["WORGEN"] = "HUMAN",
	["DEATHKNIGHT"] = "DEATHKNIGHT",
};

GlueAmbienceTracks["GNOME"] = GlueAmbienceTracks["DWARF"];
GlueAmbienceTracks["TROLL"] = GlueAmbienceTracks["ORC"];
GlueAmbienceTracks["GOBLIN"] = GlueAmbienceTracks["ORC"];
GlueAmbienceTracks["WORGEN"] = GlueAmbienceTracks["HUMAN"];

CUSTOM_CLASS_ID = {
	["WARRIOR"] = 1,
	["PALADIN"] = 2,
	["HUNTER"] = 3,
	["ROGUE"] = 4,
	["PRIEST"] = 5,
	["DEATHKNIGHT"] = 6,
	["SHAMAN"] = 7,
	["MAGE"] = 8,
	["WARLOCK"] = 9,
	["DRUID"] = 11,
};

function CharacterCreate_SetClassButtonIcon(button, fileString)
	local coords = CLASS_ICON_TCOORDS[fileString];
	getglobal(button:GetName().."NormalTexture"):SetTexCoord(coords[1], coords[2], coords[3], coords[4]);
end

function CharacterCreateEnumerateClasses(...)
	CharacterCreate.numClasses = select("#", ...)/3;
	if ( CharacterCreate.numClasses > MAX_CLASSES_PER_RACE ) then
		message("Too many classes!  Update MAX_CLASSES_PER_RACE");
		return;
	end

	for slot=1, MAX_CLASSES_PER_RACE, 1 do
		local button = getglobal("CharacterCreateClassButton"..slot);
		button.classIndex = nil;
		button.tooltip = nil;
		button:Hide();
	end

	local index = 1;
	for i=1, select("#", ...), 3 do
		local fileString = strupper(select(i+1, ...));
		local button = getglobal("CharacterCreateClassButton"..index);
		button.classIndex = CUSTOM_CLASS_ID[fileString] or index;
		button.tooltip = select(i, ...);
		CharacterCreate_SetClassButtonIcon(button, fileString);
		button:Show();
		if ( select(i+2, ...) == 1 ) then
			button:Enable();
			SetButtonDesaturated(button);
		else
			button:Disable();
			SetButtonDesaturated(button, 1);
		end
		index = index + 1;
	end
end

function SetCharacterRace(id)
	CharacterCreate.selectedRace = id;
	for slot=1, MAX_RACES, 1 do
		local button = getglobal("CharacterCreateRaceButton"..slot);
		if ( button.raceIndex == id ) then
			getglobal("CharacterCreateRaceButton"..slot.."HighlightText"):SetText(button.tooltip);
			button:SetChecked(1);
			button:LockHighlight();
		else
			getglobal("CharacterCreateRaceButton"..slot.."HighlightText"):SetText("");
			button:SetChecked(0);
			button:UnlockHighlight();
		end
	end

	local name, faction = GetFactionForRace(id);
	if ( faction == "Alliance" ) then
		CharacterCreateFactionIcon:SetTexCoord(0, 0.5, 0, 1.0);
	else
		CharacterCreateFactionIcon:SetTexCoord(0.5, 1.0, 0, 1.0);
	end
	CharacterCreateFactionScrollFrameScrollBar:SetValue(0);
	CharacterCreateFactionLabel:SetText(name);
	CharacterCreateFactionText:SetText(getglobal("FACTION_INFO_"..strupper(faction)));

	local race, fileString = GetNameForRace(id);
	CharacterCreateRaceLabel:SetText(race);
	fileString = strupper(fileString);
	local gender = CharacterCreate_GetGenderToken();
	local coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];
	CharacterCreateRaceIcon:SetTexture(CUSTOM_RACE_ICON_TEXTURE[fileString] or "Interface\\Glues\\CharacterCreate\\UI-CharacterCreate-Races");
	CharacterCreateRaceIcon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);

	local abilityIndex = 1;
	local tempText = getglobal("ABILITY_INFO_"..fileString..abilityIndex);
	abilityText = "";
	while ( tempText ) do
		abilityText = abilityText..tempText.."\n\n";
		abilityIndex = abilityIndex + 1;
		tempText = getglobal("ABILITY_INFO_"..fileString..abilityIndex);
	end

	CharacterCreateRaceScrollFrameScrollBar:SetValue(0);
	CharacterCreateRaceText:SetText(GetFlavorText("RACE_INFO_"..fileString, GetSelectedSex()));
	if ( abilityText and abilityText ~= "" ) then
		CharacterCreateRaceAbilityText:SetText(abilityText);
	else
		CharacterCreateRaceAbilityText:SetText("");
	end

	local backdropColor = FACTION_BACKDROP_COLOR_TABLE[faction];
	local frame;
	for index, value in pairs(FRAMES_TO_BACKDROP_COLOR) do
		frame = getglobal(value);
		frame:SetBackdropColor(backdropColor[4], backdropColor[5], backdropColor[6]);
	end

	local _, classFilename = GetSelectedClass();
	if (classFilename == "DEATHKNIGHT" ) then
		fileString = classFilename;
	end
	SetBackgroundModel(CharacterCreate, CUSTOM_BACKGROUND_RACE[fileString] or "ORC");
end

function SetCharacterClass(id)
	CharacterCreate.selectedClass = id;
	for slot=1, MAX_CLASSES_PER_RACE, 1 do
		local button = getglobal("CharacterCreateClassButton"..slot);
		if ( button.classIndex == id ) then
			getglobal("CharacterCreateClassButton"..slot.."HighlightText"):SetText(button.tooltip);
			button:SetChecked(1);
			button:LockHighlight();
		else
			getglobal("CharacterCreateClassButton"..slot.."HighlightText"):SetText("");
			button:UnlockHighlight();
			button:SetChecked(0);
		end
	end

	local className, classFileName = GetSelectedClass();
	local coords = CLASS_ICON_TCOORDS[classFileName];
	CharacterCreateClassIcon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);
	CharacterCreateClassLabel:SetText(className);
	CharacterCreateClassScrollFrameScrollBar:SetValue(0);
	CharacterCreateClassText:SetText(GetFlavorText("CLASS_"..strupper(classFileName), GetSelectedSex()));
end

function CharacterCreate_GetFirstVisibleClassIndex()
	for slot=1, MAX_CLASSES_PER_RACE, 1 do
		local button = getglobal("CharacterCreateClassButton"..slot);
		if ( button:IsShown() and button.classIndex ) then
			return button.classIndex;
		end
	end
	return 1;
end

function CharacterClass_OnClick(self, id)
	PlaySound("gsCharacterCreationClass");
	local classIndex = id;
	if ( self and self.classIndex ) then
		classIndex = self.classIndex;
	end
	SetSelectedClass(classIndex);
	SetCharacterClass(classIndex);
	SetCharacterRace(GetSelectedRace());
end

function CharacterRace_OnClick(self, id)
	PlaySound("gsCharacterCreationClass");
	local raceIndex = self.raceIndex or id;
	if ( not self:GetChecked() ) then
		self:SetChecked(1);
		return;
	end
	if ( GetSelectedRace() ~= raceIndex ) then
		SetSelectedRace(raceIndex);
		SetCharacterRace(raceIndex);
		SetSelectedSex(GetSelectedSex());
		SetCharacterCreateFacing(-15);
		CharacterCreateEnumerateClasses(GetClassesForRace());
		local firstClassIndex = CharacterCreate_GetFirstVisibleClassIndex();
		SetSelectedClass(firstClassIndex);
		SetCharacterClass(firstClassIndex);
		CharacterCreate_UpdateFacialHairCustomization();
		CharacterCreate_UpdateHairCustomization();
	end
end

function SetCharacterGender(sex, forceRefresh)
	local gender;
	local raceIndex = GetSelectedRace();
	local classIndex = CharacterCreate.selectedClass;
	local targetSelectedSex = CharacterCreate_TargetSelectedSex(sex);
	local sexChanged = forceRefresh or (GetSelectedSex() ~= targetSelectedSex);
	SetSelectedSex(sex);
	gender = CharacterCreate_GetGenderToken();
	if ( gender == "MALE" ) then
		CharacterCreateGenderButtonMaleHighlightText:SetText(MALE);
		CharacterCreateGenderButtonMale:SetChecked(1);
		CharacterCreateGenderButtonMale:LockHighlight();
		CharacterCreateGenderButtonFemaleHighlightText:SetText("");
		CharacterCreateGenderButtonFemale:SetChecked(nil);
		CharacterCreateGenderButtonFemale:UnlockHighlight();
		if ( CustomCharacterCreateGenderButtonMale ) then
			CustomCharacterCreateGenderButtonMaleHighlightText:SetText(MALE);
			CustomCharacterCreateGenderButtonMale:SetChecked(1);
			CustomCharacterCreateGenderButtonMale:LockHighlight();
			CustomCharacterCreateGenderButtonFemaleHighlightText:SetText("");
			CustomCharacterCreateGenderButtonFemale:SetChecked(nil);
			CustomCharacterCreateGenderButtonFemale:UnlockHighlight();
		end
	else
		CharacterCreateGenderButtonMaleHighlightText:SetText("");
		CharacterCreateGenderButtonMale:SetChecked(nil);
		CharacterCreateGenderButtonMale:UnlockHighlight();
		CharacterCreateGenderButtonFemaleHighlightText:SetText(FEMALE);
		CharacterCreateGenderButtonFemale:SetChecked(1);
		CharacterCreateGenderButtonFemale:LockHighlight();
		if ( CustomCharacterCreateGenderButtonFemale ) then
			CustomCharacterCreateGenderButtonMaleHighlightText:SetText("");
			CustomCharacterCreateGenderButtonMale:SetChecked(nil);
			CustomCharacterCreateGenderButtonMale:UnlockHighlight();
			CustomCharacterCreateGenderButtonFemaleHighlightText:SetText(FEMALE);
			CustomCharacterCreateGenderButtonFemale:SetChecked(1);
			CustomCharacterCreateGenderButtonFemale:LockHighlight();
		end
	end

	CharacterCreateEnumerateRaces(GetAvailableRaces());
	SetSelectedRace(raceIndex);
	SetCharacterRace(raceIndex);
	if ( sexChanged ) then
		SetSelectedSex(sex);
		SetSelectedRace(raceIndex);
		CharacterCreateEnumerateClasses(GetClassesForRace());
		if ( not classIndex or classIndex == 0 ) then
			classIndex = CharacterCreate_GetFirstVisibleClassIndex();
		end
		SetSelectedClass(classIndex);
		SetCharacterRace(raceIndex);
		SetCharacterClass(classIndex);
		SetCharacterCreateFacing(-15);
	end
	CharacterCreate_UpdateFacialHairCustomization();
	CharacterCreate_UpdateHairCustomization();
	UpdateCustomizationScene();

	local race, fileString = GetNameForRace(raceIndex);
	if ( fileString ) then
		CharacterCreateRaceLabel:SetText(race);
		fileString = strupper(fileString);
		local coords = RACE_ICON_TCOORDS[fileString.."_"..gender] or RACE_ICON_TCOORDS[fileString.."_MALE"];
		if ( coords ) then
			CharacterCreateRaceIcon:SetTexture(CUSTOM_RACE_ICON_TEXTURE[fileString] or "Interface\\Glues\\CharacterCreate\\UI-CharacterCreate-Races");
			CharacterCreateRaceIcon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);
		end
	end
end

'''

    xml = xml_src.read_text(encoding="utf-8")
    xml = xml.replace('CharacterClass_OnClick(self:GetID());', 'CharacterClass_OnClick(self, self:GetID());')
    xml = xml.replace('if ( CharacterCreate.selectedClass == self:GetID() ) then',
                      'if ( CharacterCreate.selectedClass == self.classIndex ) then')
    xml = xml.replace('if ( GetSelectedSex() ~= 1 ) then\n\t\t\t\t\t\t\t\t\t\t\tSetCharacterGender(1);\n\t\t\t\t\t\t\t\t\t\tend',
                      'SetCharacterGender(1, true);', 1)
    xml = xml.replace('if ( GetSelectedSex() ~= 2 ) then\n\t\t\t\t\t\t\t\t\t\t\tSetCharacterGender(2);\n\t\t\t\t\t\t\t\t\t\tend',
                      'SetCharacterGender(2, true);', 1)
    xml = xml.replace('<AbsDimension x="35" y="-78"/>', '<AbsDimension x="35" y="-68"/>', 1)
    xml = xml.replace('getglobal(self:GetName().."NormalTexture"):SetTexCoord(0, 0.5, 0, 1.0);',
                      'getglobal(self:GetName().."NormalTexture"):SetTexCoord(0, 0.5, 0, 1.0);\n\t\t\t\t\t\t\t\t\t\tself:SetFrameStrata("FULLSCREEN_DIALOG");\n\t\t\t\t\t\t\t\t\t\tself:SetFrameLevel(100);', 1)
    xml = xml.replace('getglobal(self:GetName().."NormalTexture"):SetTexCoord(0.5, 1.0, 0, 1.0);',
                      'getglobal(self:GetName().."NormalTexture"):SetTexCoord(0.5, 1.0, 0, 1.0);\n\t\t\t\t\t\t\t\t\t\tself:SetFrameStrata("FULLSCREEN_DIALOG");\n\t\t\t\t\t\t\t\t\t\tself:SetFrameLevel(100);', 1)
    insert = '''\t\t\t\t\t\t\t<CheckButton name="CharacterCreateRaceButton11" inherits="CharacterCreateRaceButtonTemplate" id="11">
\t\t\t\t\t\t\t\t<Anchors>
\t\t\t\t\t\t\t\t\t<Anchor point="TOPLEFT" relativeTo="CharacterCreateRaceButton5" relativePoint="BOTTOMLEFT">
\t\t\t\t\t\t\t\t\t\t<Offset>
\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="0" y="-5"/>
\t\t\t\t\t\t\t\t\t\t</Offset>
\t\t\t\t\t\t\t\t\t</Anchor>
\t\t\t\t\t\t\t\t</Anchors>
\t\t\t\t\t\t\t</CheckButton>
\t\t\t\t\t\t\t<CheckButton name="CharacterCreateRaceButton12" inherits="CharacterCreateRaceButtonTemplate" id="12">
\t\t\t\t\t\t\t\t<Anchors>
\t\t\t\t\t\t\t\t\t<Anchor point="TOPLEFT" relativeTo="CharacterCreateRaceButton10" relativePoint="BOTTOMLEFT">
\t\t\t\t\t\t\t\t\t\t<Offset>
\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="0" y="-5"/>
\t\t\t\t\t\t\t\t\t\t</Offset>
\t\t\t\t\t\t\t\t\t</Anchor>
\t\t\t\t\t\t\t\t</Anchors>
\t\t\t\t\t\t\t</CheckButton>
'''
    xml = xml.replace('\t\t\t\t\t\t\t<CheckButton name="CharacterCreateGenderButtonMale" inherits="CharacterCreateGenderButtonTemplate">', insert + '\t\t\t\t\t\t\t<CheckButton name="CharacterCreateGenderButtonMale" inherits="CharacterCreateGenderButtonTemplate">')
    xml = xml.replace('relativeTo="CharacterCreateRaceButton5" relativePoint="BOTTOMLEFT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="25" y="-25"/>',
                      'relativeTo="CharacterCreateFrame" relativePoint="TOPLEFT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="145" y="-410"/>', 1)
    xml = xml.replace('relativeTo="CharacterCreateGenderButtonMale" relativePoint="RIGHT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="5" y="0"/>',
                      'relativeTo="CharacterCreateFrame" relativePoint="TOPLEFT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="198" y="-410"/>', 1)
    xml = xml.replace('<Anchor point="LEFT" relativeTo="CharacterCreateRaceButton11" relativePoint="BOTTOMLEFT">',
                      '<Anchor point="TOPLEFT" relativeTo="CharacterCreateRaceButton11" relativePoint="BOTTOMLEFT">', 1)
    xml = xml.replace('relativeTo="CharacterCreateGenderButtonMale" relativePoint="BOTTOMLEFT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="-52" y="-10"/>',
                      'relativeTo="CharacterCreateFrame" relativePoint="TOPLEFT">\n\t\t\t\t\t\t\t\t\t\t<Offset>\n\t\t\t\t\t\t\t\t\t\t\t<AbsDimension x="35" y="-465"/>', 1)
    glue = staging / "Interface" / "GlueXML"
    glue.mkdir(parents=True, exist_ok=True)
    (glue / "CharacterCreate.lua").write_text(lua, encoding="utf-8")
    (glue / "CharacterCreate.xml").write_text(xml, encoding="utf-8")


def build_custom_race_icons(staging: Path):
    sys.path.insert(0, str(WORKSPACE / "tools" / "remix_system"))
    sys.path.insert(0, r"C:\Users\monty\Documents\Codex\2026-04-30\files-mentioned-by-the-user-akheva\tools")
    import wow335_patch_tools as wow
    from PIL import Image

    sheet = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    cells = [
        (0, 0, RETAIL_ICON_DIR / "achievement_goblinhead.blp"),
        (64, 0, RETAIL_ICON_DIR / "achievement_femalegoblinhead.blp"),
        (0, 64, RETAIL_ICON_DIR / "achievement_worganhead.blp"),
        (64, 64, RETAIL_ICON_DIR / "achievement_worganhead.blp"),
    ]
    for x, y, src in cells:
        icon = Image.open(src).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
        sheet.paste(icon, (x, y), icon)
    patched_png = OUT_DIR / "UI-CharacterCreate-CustomRaces.png"
    patched_blp = staging / "Interface" / "GLUES" / "CHARACTERCREATE" / "UI-CharacterCreate-CustomRaces.blp"
    patched_blp.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(patched_png)
    wow.image_to_blp2_dxt1(patched_png, patched_blp)


def load_downport_tool():
    spec = importlib.util.spec_from_file_location("downport_md21_to_wotlk", DOWNPORT_TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_texture_name_for_id = module.texture_name_for_id

    def texture_name_for_id(src_dir: Path, filedata_id: int, fallback_index: int) -> str:
        try:
            return original_texture_name_for_id(src_dir, filedata_id, fallback_index)
        except ValueError:
            blps = sorted(src_dir.glob("*.blp"))
            preferred = [
                item for item in blps
                if "skin00_00" in item.name.lower() or item.stem.lower().endswith("01")
            ]
            choices = preferred or blps
            if choices:
                return choices[min(fallback_index, len(choices) - 1)].name
            raise

    module.texture_name_for_id = texture_name_for_id
    return module


def load_static_model_tool():
    tool_dir = STATIC_MODEL_TOOL.parent
    if str(tool_dir) not in sys.path:
        sys.path.insert(0, str(tool_dir))
    spec = importlib.util.spec_from_file_location("static_from_modern_m2", STATIC_MODEL_TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_texture_name_for_id = module.texture_name_for_id

    def texture_name_for_id(src_dir: Path, filedata_id: int, fallback_index: int) -> str:
        try:
            return original_texture_name_for_id(src_dir, filedata_id, fallback_index)
        except ValueError:
            blps = sorted(src_dir.glob("*.blp"))
            preferred = [
                item for item in blps
                if "skin00_00" in item.name.lower() or item.stem.lower().endswith("01")
            ]
            choices = preferred or blps
            if choices:
                return choices[min(fallback_index, len(choices) - 1)].name
            raise

    module.texture_name_for_id = texture_name_for_id
    return module


def stage_playable_race_models(staging: Path):
    if not ENABLE_CUSTOM_CHARACTER_MODELS:
        return

    if not MODEL_EXTRACTION_CHARACTER.exists():
        print(f"Skipping playable race models; missing {MODEL_EXTRACTION_CHARACTER}")
        return

    downport = load_downport_tool()
    if DOWNPORTED_MODEL_DIR.exists():
        shutil.rmtree(DOWNPORTED_MODEL_DIR)

    for src_dir, model_dir, model_name, m2_name, skin_name in CHARACTER_MODEL_SOURCES:
        if not src_dir.exists():
            print(f"Skipping {model_name}; missing {src_dir}")
            continue

        source_m2 = src_dir / m2_name
        source_skin = src_dir / skin_name
        if not source_m2.exists() or not source_skin.exists():
            print(f"Skipping {model_name}; missing base M2/SKIN in {src_dir}")
            continue

        out_dir = DOWNPORTED_MODEL_DIR
        for part in model_dir.split("\\"):
            out_dir = out_dir / part
        out_dir.mkdir(parents=True, exist_ok=True)

        report = downport.downport_m2(
            source_m2,
            out_dir / f"{model_name}.m2",
            src_dir,
            model_dir,
            model_name,
        )
        for skin in sorted(src_dir.glob(f"{Path(m2_name).stem}*.skin")):
            suffix = skin.stem[len(Path(m2_name).stem):]
            if suffix.startswith("_lod"):
                continue
            if not suffix:
                suffix = "00"
            downport.downport_skin(skin, out_dir / f"{model_name}{suffix}.skin")

        source_stem = Path(m2_name).stem
        for anim in sorted(src_dir.glob(f"{source_stem}*.anim")):
            suffix = anim.stem[len(source_stem):]
            shutil.copy2(anim, out_dir / f"{model_name}{suffix}.anim")

        source_skel = src_dir / f"{source_stem}.skel"
        if source_skel.exists():
            shutil.copy2(source_skel, out_dir / f"{model_name}.skel")

        used_textures = {
            Path(item["source_name"]).name.lower()
            for item in report.get("rewrite", {}).get("texture_names", [])
        }
        for index, override_name in CHARACTER_MODEL_TEXTURE_OVERRIDES.get(model_name, {}).items():
            used_textures.add(override_name.lower())
        for texture_name in sorted(used_textures):
            texture = src_dir / texture_name
            if texture.exists():
                shutil.copy2(texture, out_dir / texture.name)

    staged_character = staging / "Character"
    if staged_character.exists():
        shutil.rmtree(staged_character)
    if (DOWNPORTED_MODEL_DIR / "Character").exists():
        shutil.copytree(DOWNPORTED_MODEL_DIR / "Character", staged_character)


def rotate_static_m2_z_180(path: Path):
    data = bytearray(path.read_bytes())
    if data[:4] != b"MD20":
        return

    fields = struct.unpack_from("<40I", data, 4)
    vertex_count = fields[14]
    vertex_offset = fields[15]
    vertex_size = 48
    if vertex_offset <= 0 or vertex_count <= 0 or vertex_offset + vertex_count * vertex_size > len(data):
        return

    for index in range(vertex_count):
        offset = vertex_offset + index * vertex_size
        x, y, z = struct.unpack_from("<3f", data, offset)
        nx, ny, nz = struct.unpack_from("<3f", data, offset + 20)
        struct.pack_into("<3f", data, offset, -x, -y, z)
        struct.pack_into("<3f", data, offset + 20, -nx, -ny, nz)

    path.write_bytes(data)


def stage_demon_hunter_glaive_model(staging: Path):
    src_dir = DEMON_HUNTER_ASSET_DIR / "item" / "objectcomponents" / "weapon"
    model_m2 = src_dir / f"{DEMON_HUNTER_GLAIVE_MODEL}.m2"
    model_skin = src_dir / f"{DEMON_HUNTER_GLAIVE_MODEL}00.skin"
    texture = src_dir / f"{DEMON_HUNTER_GLAIVE_TEXTURE}.blp"
    if not model_m2.exists() or not model_skin.exists() or not texture.exists():
        print(f"Skipping Demon Hunter glaive model; missing files in {src_dir}")
        return

    static_tool = load_static_model_tool()
    out_root = OUT_DIR / "downported_glaives"
    if out_root.exists():
        shutil.rmtree(out_root)

    model_dir = r"Item\ObjectComponents\Weapon"
    static_tool.build_static(
        src_dir,
        out_root,
        model_dir,
        DEMON_HUNTER_GLAIVE_MODEL,
        scale=1.0,
        m2_name=f"{DEMON_HUNTER_GLAIVE_MODEL}.m2",
        skin_name=f"{DEMON_HUNTER_GLAIVE_MODEL}00.skin",
        texture_overrides={0: f"{DEMON_HUNTER_GLAIVE_TEXTURE}.blp"},
        animated_root=False,
    )

    source_weapon_dir = out_root / "Item" / "ObjectComponents" / "Weapon"
    main_m2 = source_weapon_dir / f"{DEMON_HUNTER_GLAIVE_MODEL}.m2"
    main_skin = source_weapon_dir / f"{DEMON_HUNTER_GLAIVE_MODEL}00.skin"
    offhand_m2 = source_weapon_dir / f"{DEMON_HUNTER_OFFHAND_GLAIVE_MODEL}.m2"
    offhand_skin = source_weapon_dir / f"{DEMON_HUNTER_OFFHAND_GLAIVE_MODEL}00.skin"
    if main_m2.exists() and main_skin.exists():
        shutil.copy2(main_m2, offhand_m2)
        shutil.copy2(main_skin, offhand_skin)
        rotate_static_m2_z_180(offhand_m2)

    weapon_staging = staging / "Item" / "ObjectComponents" / "Weapon"
    weapon_staging.mkdir(parents=True, exist_ok=True)
    for item in source_weapon_dir.iterdir():
        shutil.copy2(item, weapon_staging / item.name)
    shutil.copy2(texture, weapon_staging / texture.name)


def stage_demon_hunter_spell_visual_models(staging: Path):
    src_dir = DEMON_HUNTER_ASSET_DIR / "spells"
    if not src_dir.exists():
        print(f"Skipping Demon Hunter spell visuals; missing {src_dir}")
        return

    downport = load_downport_tool()
    out_root = OUT_DIR / "downported_spell_visuals"
    if out_root.exists():
        shutil.rmtree(out_root)

    spell_out = out_root / "Spells"
    spell_out.mkdir(parents=True, exist_ok=True)
    staged_spells = staging / "Spells"
    staged_spells.mkdir(parents=True, exist_ok=True)

    staged_stems = {
        stem
        for _name, _path, stem in DEMON_HUNTER_VISUAL_EFFECTS.values()
        if stem not in UNSAFE_DEMON_HUNTER_SPELL_VISUAL_STEMS
    }
    for stem in sorted(staged_stems):
        source_m2 = src_dir / f"{stem}.m2"
        source_skin = src_dir / f"{stem}00.skin"
        if not source_m2.exists():
            print(f"Skipping spell visual {stem}; missing {source_m2.name}")
            continue

        try:
            report = downport.downport_m2(source_m2, spell_out / f"{stem}.m2", src_dir, "Spells", stem)
            if source_skin.exists():
                downport.downport_skin(source_skin, spell_out / f"{stem}00.skin")
        except Exception as exc:
            print(f"Skipping spell visual {stem}; downport failed: {exc}")
            continue

        m2_out = spell_out / f"{stem}.m2"
        if m2_out.exists():
            shutil.copy2(m2_out, staged_spells / f"{stem}.m2")
            shutil.copy2(m2_out, staged_spells / f"{stem}.mdx")
        skin_out = spell_out / f"{stem}00.skin"
        if skin_out.exists():
            shutil.copy2(skin_out, staged_spells / f"{stem}00.skin")
        texture_names = {
            Path(item["source_name"]).name.lower()
            for item in report.get("rewrite", {}).get("texture_names", [])
        }
        for texture in sorted(src_dir.glob(f"{stem}*.blp")):
            texture_names.add(texture.name.lower())
        for texture_name in sorted(texture_names):
            texture = src_dir / texture_name
            if texture.exists():
                shutil.copy2(texture, staged_spells / texture.name)
    assert_unsafe_spell_visual_models_absent(staging)


def load_remix_builder():
    spec = importlib.util.spec_from_file_location("remix_builder", REMIX_BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_tree_contents(src: Path, dst: Path):
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def copy_vendor_patch(staging: Path):
    if not WORGOBLIN_PATCH.exists():
        raise FileNotFoundError(f"Missing mod-worgoblin patch assets: {WORGOBLIN_PATCH}")
    copy_tree_contents(WORGOBLIN_PATCH, staging)
    # The vendor patch includes an in-game FrameXML override. ChromieCraft's
    # client rejects it after login, so keep only glue UI/model/DBC assets here.
    framexml = staging / "Interface" / "FrameXML"
    if framexml.exists():
        shutil.rmtree(framexml)
    patch_vendor_glue_parent(staging)


def read_client_text(path: str) -> str:
    result = subprocess.run(
        [str(MPQCLI), "read", path, str(CLIENT_LOCALE)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def stage_minimal_glue_parent(staging: Path):
    glue_parent = read_client_text(r"Interface\GlueXML\GlueParent.lua")
    glue_parent = glue_parent.replace(
        'CharModelFogInfo["SCOURGE"] = { r=0, g=0.22, b=0.22, far=26 };\n',
        'CharModelFogInfo["SCOURGE"] = { r=0, g=0.22, b=0.22, far=26 };\n'
        'CharModelFogInfo["GOBLIN"] = CharModelFogInfo["ORC"];\n'
        'CharModelFogInfo["WORGEN"] = CharModelFogInfo["HUMAN"];\n'
        'CharModelFogInfo["GILNEAN"] = CharModelFogInfo["HUMAN"];\n',
    )
    glue_parent = glue_parent.replace(
        'GlueAmbienceTracks["DEATHKNIGHT"] = "GlueScreenIntro";\n',
        'GlueAmbienceTracks["DEATHKNIGHT"] = "GlueScreenIntro";\n'
        'GlueAmbienceTracks["GOBLIN"] = "GlueScreenOrcTroll";\n'
        'GlueAmbienceTracks["WORGEN"] = "GlueScreenHuman";\n'
        'GlueAmbienceTracks["GILNEAN"] = "GlueScreenHuman";\n'
        'GlueAmbienceTracks["CHARACTERSELECT"] = "GlueScreenIntro";\n',
    )
    glue_parent = glue_parent.replace(
        'PlayGlueAmbience(GlueAmbienceTracks[strupper(race)], 4.0);',
        'PlayGlueAmbience(GlueAmbienceTracks[strupper(race)] or GlueAmbienceTracks["CHARACTERSELECT"], 4.0);',
    )
    target = staging / "Interface" / "GlueXML" / "GlueParent.lua"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(glue_parent, encoding="utf-8", newline="")


def patch_vendor_glue_parent(staging: Path):
    target = staging / "Interface" / "GlueXML" / "GlueParent.lua"
    if not target.exists():
        stage_minimal_glue_parent(staging)
        return

    glue_parent = target.read_text(encoding="utf-8")
    if 'GlueAmbienceTracks["CHARACTERSELECT"]' not in glue_parent:
        glue_parent = glue_parent.replace(
            'GlueAmbienceTracks["DEATHKNIGHT"] = "GlueScreenIntro";\n',
            'GlueAmbienceTracks["DEATHKNIGHT"] = "GlueScreenIntro";\n'
            'GlueAmbienceTracks["CHARACTERSELECT"] = "GlueScreenIntro";\n',
        )
    glue_parent = glue_parent.replace(
        'PlayGlueAmbience(GlueAmbienceTracks[nameupper], 4.0);',
        'PlayGlueAmbience(GlueAmbienceTracks[nameupper] or GlueAmbienceTracks["CHARACTERSELECT"], 4.0);',
    )
    target.write_text(glue_parent, encoding="utf-8", newline="")


def normalize_goblin_better_living_spell(path: Path):
    """Keep the imported Goblin alchemy racial at the retail +5 value."""
    dbc = DBC(path)
    rows = dbc.u32_rows()
    for row in rows:
        if row[0] == 69045:
            row[80] = 4  # EffectBasePoints_1: DBC stores +5 as 4 plus one die side.
            break
    else:
        raise ValueError("Spell 69045 missing from Spell.dbc")
    dbc.set_u32_rows(rows)
    dbc.write(path)


def patch_remix_shirt_icon(staging: Path, install_server_dbc=False):
    if not REMIX_SHIRT_ICON_SOURCE.exists():
        raise FileNotFoundError(REMIX_SHIRT_ICON_SOURCE)

    icon_dir = staging / "Interface" / "Icons"
    icon_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REMIX_SHIRT_ICON_SOURCE, icon_dir / f"{REMIX_SHIRT_ICON_NAME}.blp")

    dbc_path = staging / "DBFilesClient" / "ItemDisplayInfo.dbc"
    dbc = DBC(dbc_path)
    rows = dbc.u32_rows()
    source = next((list(row) for row in rows if row[0] == REMIX_SHIRT_DISPLAY_SOURCE_ID), None)
    if source is None:
        raise ValueError(f"ItemDisplayInfo row {REMIX_SHIRT_DISPLAY_SOURCE_ID} missing")

    custom = list(source)
    custom[0] = REMIX_SHIRT_DISPLAY_ID
    custom[5] = dbc.add_string(REMIX_SHIRT_ICON_NAME)
    rows = [row for row in rows if row[0] != REMIX_SHIRT_DISPLAY_ID]
    rows.append(custom)
    rows.sort(key=lambda row: row[0])
    dbc.set_u32_rows(rows)
    dbc.write(dbc_path)

    if install_server_dbc:
        shutil.copy2(dbc_path, SERVER_DBC / "ItemDisplayInfo.dbc")


def patch_demon_hunter_glaive_displays(staging: Path, install_server_dbc=False):
    icon_source = DEMON_HUNTER_ICON_DIR / f"{DEMON_HUNTER_GLAIVE_ICON}.blp"
    if icon_source.exists():
        icon_dir = staging / "Interface" / "Icons"
        icon_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon_source, icon_dir / f"{DEMON_HUNTER_GLAIVE_ICON}.blp")

    dbc_path = staging / "DBFilesClient" / "ItemDisplayInfo.dbc"
    dbc = DBC(dbc_path)
    rows = dbc.u32_rows()
    display_sources = {
        DEMON_HUNTER_MAIN_DISPLAY: (45479, DEMON_HUNTER_GLAIVE_MODEL),
        DEMON_HUNTER_OFF_DISPLAY: (45481, DEMON_HUNTER_OFFHAND_GLAIVE_MODEL),
    }
    new_rows = [row for row in rows if row[0] not in display_sources]
    for display_id, (source_id, model_name) in display_sources.items():
        source = next((list(row) for row in rows if row[0] == source_id), None)
        if source is None:
            raise ValueError(f"ItemDisplayInfo row {source_id} missing")
        custom = list(source)
        custom[0] = display_id
        custom[1] = dbc.add_string(f"{model_name}.mdx")
        custom[2] = 0
        custom[3] = dbc.add_string(DEMON_HUNTER_GLAIVE_TEXTURE)
        custom[4] = 0
        custom[5] = dbc.add_string(DEMON_HUNTER_GLAIVE_ICON)
        new_rows.append(custom)
    new_rows.sort(key=lambda row: row[0])
    dbc.set_u32_rows(new_rows)
    dbc.write(dbc_path)

    if install_server_dbc:
        shutil.copy2(dbc_path, SERVER_DBC / "ItemDisplayInfo.dbc")


def patch_demon_hunter_items(staging: Path, install_server_dbc=False):
    dbc_path = staging / "DBFilesClient" / "Item.dbc"
    if not dbc_path.exists():
        shutil.copy2(dbc_source(staging, "Item.dbc"), dbc_path)

    dbc = DBC(dbc_path)
    rows = dbc.u32_rows()
    source_rows = {row[0]: list(row) for row in rows}
    new_rows = [row for row in rows if row[0] not in {DEMON_HUNTER_MAIN_HAND, DEMON_HUNTER_OFF_HAND}]
    glaives = {
        DEMON_HUNTER_MAIN_HAND: (32837, DEMON_HUNTER_MAIN_DISPLAY, 21),
        DEMON_HUNTER_OFF_HAND: (32838, DEMON_HUNTER_OFF_DISPLAY, 22),
    }
    for item_id, (source_id, display_id, inventory_type) in glaives.items():
        source = list(source_rows.get(source_id, [source_id, 2, 7, 0xFFFFFFFF, 1, display_id, inventory_type, 1]))
        source[0] = item_id
        source[1] = 2              # ITEM_CLASS_WEAPON
        source[2] = 7              # One-handed sword; closest WotLK weapon subclass for glaive requirements.
        source[3] = 0xFFFFFFFF
        source[4] = 1
        source[5] = display_id
        source[6] = inventory_type
        source[7] = 1
        new_rows.append(source)
    new_rows.sort(key=lambda row: row[0])
    dbc.set_u32_rows(new_rows)
    dbc.write(dbc_path)

    if install_server_dbc:
        shutil.copy2(dbc_path, SERVER_DBC / "Item.dbc")


def stage_demon_hunter_ingame_ui(staging: Path):
    addon_dir = staging / "Interface" / "AddOns" / "GPT_DemonHunterUI"
    addon_dir.mkdir(parents=True, exist_ok=True)
    (addon_dir / "GPT_DemonHunterUI.toc").write_text(
        """## Interface: 30300
## Title: GPT Demon Hunter UI
## Notes: Displays the custom Demon Hunter identity while the server uses a Rogue client shell.
## DefaultState: Enabled
GPT_DemonHunterUI.lua
""",
        encoding="utf-8",
        newline="",
    )
    (addon_dir / "GPT_DemonHunterUI.lua").write_text(
        r'''local DH_MARKER_SPELLS = {
    [910201] = true,
    [910202] = true,
    [910203] = true,
    [910204] = true,
    [910205] = true,
    [910206] = true,
    [910207] = true,
    [910208] = true,
    [910209] = true,
    [910210] = true,
    [910211] = true,
    [910212] = true,
    [910213] = true,
    [910214] = true,
    [910215] = true,
    [910216] = true,
    [910217] = true,
    [910218] = true,
    [910219] = true,
    [910220] = true,
    [910221] = true,
    [910222] = true,
    [910223] = true,
    [910224] = true,
    [910225] = true,
    [910226] = true,
    [910227] = true,
    [910228] = true,
    [910229] = true,
    [910230] = true,
    [910231] = true,
    [910232] = true,
    [910233] = true,
    [910234] = true,
    [910235] = true,
    [910236] = true,
    [910237] = true,
    [910238] = true,
    [910239] = true,
    [910240] = true,
    [910241] = true,
    [910242] = true,
    [910243] = true,
    [910244] = true,
    [910245] = true,
    [910246] = true,
    [910247] = true,
    [910248] = true,
    [910249] = true,
    [910250] = true,
    [910251] = true,
    [910252] = true,
    [910253] = true,
    [910254] = true,
    [910255] = true,
    [910256] = true,
    [910257] = true,
    [910258] = true,
    [910259] = true,
    [910260] = true,
    [910261] = true,
    [910262] = true,
    [910263] = true,
    [910264] = true,
    [910265] = true,
    [910266] = true,
    [910267] = true,
    [910268] = true,
    [910269] = true,
    [910270] = true,
    [910271] = true,
    [910272] = true,
    [910273] = true,
    [910274] = true,
    [910275] = true,
    [910276] = true,
    [910277] = true,
    [910278] = true,
    [910279] = true,
    [910280] = true,
}
local DH_SPELL_TABS = {
    [910201] = "Havoc",
    [910202] = "Havoc",
    [910203] = "Demon Hunter",
    [910204] = "Demon Hunter",
    [910205] = "Havoc",
    [910206] = "Havoc",
    [910207] = "Vengeance",
    [910208] = "Havoc",
    [910209] = "Havoc",
    [910210] = "Havoc",
    [910211] = "Demon Hunter",
    [910212] = "Demon Hunter",
    [910213] = "Demon Hunter",
    [910214] = "Demon Hunter",
    [910215] = "Demon Hunter",
    [910216] = "Demon Hunter",
    [910217] = "Vengeance",
    [910218] = "Vengeance",
    [910219] = "Vengeance",
    [910220] = "Vengeance",
    [910221] = "Vengeance",
    [910222] = "Vengeance",
    [910223] = "Havoc",
    [910224] = "Havoc",
    [910225] = "Demon Hunter",
    [910226] = "Havoc",
    [910227] = "Vengeance",
    [910228] = "Vengeance",
    [910229] = "Vengeance",
    [910230] = "Vengeance",
    [910231] = "Demon Hunter",
    [910232] = "Demon Hunter",
    [910233] = "Demon Hunter",
    [910234] = "Demon Hunter",
    [910235] = "Demon Hunter",
    [910236] = "Havoc",
    [910237] = "Havoc",
    [910238] = "Havoc",
    [910239] = "Havoc",
    [910240] = "Havoc",
    [910241] = "Vengeance",
    [910242] = "Vengeance",
    [910243] = "Vengeance",
    [910244] = "Vengeance",
    [910245] = "Havoc",
    [910246] = "Havoc",
    [910247] = "Havoc",
    [910248] = "Havoc",
    [910249] = "Havoc",
    [910250] = "Havoc",
    [910251] = "Havoc",
    [910252] = "Havoc",
    [910253] = "Vengeance",
    [910254] = "Vengeance",
    [910255] = "Vengeance",
    [910256] = "Demon Hunter",
    [910257] = "Vengeance",
    [910258] = "Vengeance",
    [910259] = "Vengeance",
    [910260] = "Havoc",
    [910261] = "Havoc",
    [910262] = "Havoc",
    [910263] = "Havoc",
    [910264] = "Havoc",
    [910265] = "Havoc",
    [910266] = "Havoc",
    [910267] = "Havoc",
    [910268] = "Havoc",
    [910269] = "Havoc",
    [910270] = "Havoc",
    [910271] = "Vengeance",
    [910272] = "Vengeance",
    [910273] = "Vengeance",
    [910274] = "Vengeance",
    [910275] = "Vengeance",
    [910276] = "Vengeance",
    [910277] = "Vengeance",
    [910278] = "Vengeance",
    [910279] = "Vengeance",
    [910280] = "Vengeance",
}
local DH_MARKER_NAMES = {
    ["Demon's Bite"] = true,
    ["Chaos Strike"] = true,
    ["Throw Glaive"] = true,
    ["Fel Rush"] = true,
    ["Eye Beam"] = true,
    ["Blade Dance"] = true,
    ["Immolation Aura"] = true,
    ["Vengeful Retreat"] = true,
    ["Blur"] = true,
    ["Metamorphosis"] = true,
    ["Spectral Sight"] = true,
    ["Chaos Nova"] = true,
    ["Consume Magic"] = true,
    ["Disrupt"] = true,
    ["Imprison"] = true,
    ["Torment"] = true,
    ["Shear"] = true,
    ["Soul Cleave"] = true,
    ["Infernal Strike"] = true,
    ["Demon Spikes"] = true,
    ["Fiery Brand"] = true,
    ["Sigil of Flame"] = true,
    ["Felblade"] = true,
    ["Death Sweep"] = true,
    ["Darkness"] = true,
    ["The Hunt"] = true,
    ["Fel Devastation"] = true,
    ["Sigil of Misery"] = true,
    ["Sigil of Silence"] = true,
    ["Sigil of Chains"] = true,
    ["Glide"] = true,
    ["Double Jump"] = true,
    ["Reverse Magic"] = true,
    ["Shattered Souls"] = true,
    ["Chaos Brand"] = true,
    ["Annihilation"] = true,
    ["Glaive Tempest"] = true,
    ["Fel Barrage"] = true,
    ["Demonic"] = true,
    ["Netherwalk"] = true,
    ["Fracture"] = true,
    ["Spirit Bomb"] = true,
    ["Soul Barrier"] = true,
    ["Soul Carver"] = true,
    ["Demon Blades"] = true,
    ["Essence Break"] = true,
    ["Fel Eruption"] = true,
    ["Unbound Chaos"] = true,
    ["Momentum"] = true,
    ["Tactical Retreat"] = true,
    ["Burning Hatred"] = true,
    ["Reaver's Glaive"] = true,
    ["Demonic Wards"] = true,
    ["Mastery: Fel Blood"] = true,
    ["Sigil of Spite"] = true,
    ["Elysian Decree"] = true,
    ["Frailty"] = true,
    ["Bulk Extraction"] = true,
    ["Charred Warblades"] = true,
    ["Demonsurge"] = true,
    ["Chaos Theory"] = true,
    ["Trail of Ruin"] = true,
    ["First Blood"] = true,
    ["Ragefire"] = true,
    ["Any Means Necessary"] = true,
    ["Know Your Enemy"] = true,
    ["Inner Demon"] = true,
    ["Initiative"] = true,
    ["Burning Wound"] = true,
    ["Rush of Chaos"] = true,
    ["Soul Furnace"] = true,
    ["Calcified Spikes"] = true,
    ["Illuminated Sigils"] = true,
    ["Void Reaver"] = true,
    ["Fallout"] = true,
    ["Feed the Demon"] = true,
    ["Burning Alive"] = true,
    ["Down in Flames"] = true,
    ["Ruinous Bulwark"] = true,
    ["Last Resort"] = true,
}
local DH_NAME_TABS = {
    ["Demon's Bite"] = "Havoc",
    ["Chaos Strike"] = "Havoc",
    ["Throw Glaive"] = "Demon Hunter",
    ["Fel Rush"] = "Demon Hunter",
    ["Eye Beam"] = "Havoc",
    ["Blade Dance"] = "Havoc",
    ["Immolation Aura"] = "Vengeance",
    ["Vengeful Retreat"] = "Havoc",
    ["Blur"] = "Havoc",
    ["Metamorphosis"] = "Havoc",
    ["Spectral Sight"] = "Demon Hunter",
    ["Chaos Nova"] = "Demon Hunter",
    ["Consume Magic"] = "Demon Hunter",
    ["Disrupt"] = "Demon Hunter",
    ["Imprison"] = "Demon Hunter",
    ["Torment"] = "Demon Hunter",
    ["Shear"] = "Vengeance",
    ["Soul Cleave"] = "Vengeance",
    ["Infernal Strike"] = "Vengeance",
    ["Demon Spikes"] = "Vengeance",
    ["Fiery Brand"] = "Vengeance",
    ["Sigil of Flame"] = "Vengeance",
    ["Felblade"] = "Havoc",
    ["Death Sweep"] = "Havoc",
    ["Darkness"] = "Demon Hunter",
    ["The Hunt"] = "Havoc",
    ["Fel Devastation"] = "Vengeance",
    ["Sigil of Misery"] = "Vengeance",
    ["Sigil of Silence"] = "Vengeance",
    ["Sigil of Chains"] = "Vengeance",
    ["Glide"] = "Demon Hunter",
    ["Double Jump"] = "Demon Hunter",
    ["Reverse Magic"] = "Demon Hunter",
    ["Shattered Souls"] = "Demon Hunter",
    ["Chaos Brand"] = "Demon Hunter",
    ["Annihilation"] = "Havoc",
    ["Glaive Tempest"] = "Havoc",
    ["Fel Barrage"] = "Havoc",
    ["Demonic"] = "Havoc",
    ["Netherwalk"] = "Havoc",
    ["Fracture"] = "Vengeance",
    ["Spirit Bomb"] = "Vengeance",
    ["Soul Barrier"] = "Vengeance",
    ["Soul Carver"] = "Vengeance",
    ["Demon Blades"] = "Havoc",
    ["Essence Break"] = "Havoc",
    ["Fel Eruption"] = "Havoc",
    ["Unbound Chaos"] = "Havoc",
    ["Momentum"] = "Havoc",
    ["Tactical Retreat"] = "Havoc",
    ["Burning Hatred"] = "Havoc",
    ["Reaver's Glaive"] = "Havoc",
    ["Demonic Wards"] = "Vengeance",
    ["Mastery: Fel Blood"] = "Vengeance",
    ["Sigil of Spite"] = "Vengeance",
    ["Elysian Decree"] = "Demon Hunter",
    ["Frailty"] = "Vengeance",
    ["Bulk Extraction"] = "Vengeance",
    ["Charred Warblades"] = "Vengeance",
    ["Demonsurge"] = "Havoc",
    ["Chaos Theory"] = "Havoc",
    ["Trail of Ruin"] = "Havoc",
    ["First Blood"] = "Havoc",
    ["Ragefire"] = "Havoc",
    ["Any Means Necessary"] = "Havoc",
    ["Know Your Enemy"] = "Havoc",
    ["Inner Demon"] = "Havoc",
    ["Initiative"] = "Havoc",
    ["Burning Wound"] = "Havoc",
    ["Rush of Chaos"] = "Havoc",
    ["Soul Furnace"] = "Vengeance",
    ["Calcified Spikes"] = "Vengeance",
    ["Illuminated Sigils"] = "Vengeance",
    ["Void Reaver"] = "Vengeance",
    ["Fallout"] = "Vengeance",
    ["Feed the Demon"] = "Vengeance",
    ["Burning Alive"] = "Vengeance",
    ["Down in Flames"] = "Vengeance",
    ["Ruinous Bulwark"] = "Vengeance",
    ["Last Resort"] = "Vengeance",
}
local DH_REAL_TABS = {
    ["Demon Hunter"] = true,
    ["Havoc"] = true,
    ["Vengeance"] = true,
}
local DH_MARKER_SKILL = "Demon Hunter"
local DH_LOCALIZED = "Demon Hunter"
local DH_TOKEN = "DEMONHUNTER"
local DH_ID = 10
local DH_ROGUE_TAB_REPLACEMENTS = {
    ["Combat"] = "Demon Hunter",
    ["Assassination"] = "Havoc",
    ["Subtlety"] = "Vengeance",
    ["Rogue"] = "Demon Hunter",
}

local GPTDH_IsDemonHunter = false
local Original_UnitClass = UnitClass
local Original_UnitClassBase = UnitClassBase

local function GPTDH_ScanSpellBook()
    if not GetNumSpellTabs or not GetSpellTabInfo or not GetSpellName then
        return false
    end

    for tab = 1, GetNumSpellTabs() do
        local _, _, offset, numSpells = GetSpellTabInfo(tab)
        offset = offset or 0
        numSpells = numSpells or 0
        for i = offset + 1, offset + numSpells do
            local spellName, _, spellId = GetSpellName(i, BOOKTYPE_SPELL)
            if spellId and DH_MARKER_SPELLS[spellId] then
                return true
            end
            if spellName and DH_MARKER_NAMES[spellName] then
                return true
            end
        end
    end

    return false
end

local function GPTDH_HasDemonHunterMarker()
    for spellId in pairs(DH_MARKER_SPELLS) do
        if IsSpellKnown and IsSpellKnown(spellId) then
            return true
        end
    end

    if GetNumSkillLines and GetSkillLineInfo then
        for i = 1, GetNumSkillLines() do
            local skillName = GetSkillLineInfo(i)
            if skillName == DH_MARKER_SKILL then
                return true
            end
        end
    end

    return GPTDH_ScanSpellBook()
end

local function GPTDH_RefreshMarker()
    GPTDH_IsDemonHunter = GPTDH_HasDemonHunterMarker()
    return GPTDH_IsDemonHunter
end

RAID_CLASS_COLORS = RAID_CLASS_COLORS or {}
RAID_CLASS_COLORS[DH_TOKEN] = RAID_CLASS_COLORS[DH_TOKEN] or { r = 0.64, g = 0.19, b = 0.79, colorStr = "ffa330c9" }
if CUSTOM_CLASS_COLORS then
    CUSTOM_CLASS_COLORS[DH_TOKEN] = CUSTOM_CLASS_COLORS[DH_TOKEN] or RAID_CLASS_COLORS[DH_TOKEN]
end
if CLASS_ICON_TCOORDS and CLASS_ICON_TCOORDS.ROGUE then
    CLASS_ICON_TCOORDS[DH_TOKEN] = CLASS_ICON_TCOORDS[DH_TOKEN] or CLASS_ICON_TCOORDS.ROGUE
end

function UnitClass(unit)
    if unit == "player" and (GPTDH_IsDemonHunter or GPTDH_RefreshMarker()) then
        return DH_LOCALIZED, DH_TOKEN, DH_ID
    end

    return Original_UnitClass(unit)
end

if Original_UnitClassBase then
    function UnitClassBase(unit)
        if unit == "player" and (GPTDH_IsDemonHunter or GPTDH_RefreshMarker()) then
            return DH_TOKEN, DH_ID
        end

        return Original_UnitClassBase(unit)
    end
end

local function GPTDH_UpdateCharacterClassText()
    if not GPTDH_RefreshMarker() then
        return
    end

    local race = UnitRace("player") or ""
    local level = UnitLevel("player") or 1
    if CharacterLevelText then
        CharacterLevelText:SetText("Level "..level.." "..race.." "..DH_LOCALIZED)
    end
end

local function GPTDH_GetDemonHunterTabReplacement(offset, numSpells)
    if not GetSpellName then
        return nil
    end

    offset = offset or 0
    numSpells = numSpells or 0
    for i = offset + 1, offset + numSpells do
        local spellName, _, spellId = GetSpellName(i, BOOKTYPE_SPELL)
        if spellId and DH_SPELL_TABS[spellId] then
            return DH_SPELL_TABS[spellId]
        end
        if spellName and DH_NAME_TABS[spellName] then
            return DH_NAME_TABS[spellName]
        end
    end

    return nil
end

local function GPTDH_UpdateSpellbookClassText()
    if not GPTDH_RefreshMarker() then
        return
    end

    if not GetNumSpellTabs or not GetSpellTabInfo then
        return
    end

    for tab = 1, GetNumSpellTabs() do
        local tabName, _texture, offset, numSpells = GetSpellTabInfo(tab)
        local replacement = nil
        if DH_REAL_TABS[tabName] then
            replacement = tabName
        elseif DH_ROGUE_TAB_REPLACEMENTS[tabName] then
            replacement = DH_ROGUE_TAB_REPLACEMENTS[tabName]
        else
            replacement = GPTDH_GetDemonHunterTabReplacement(offset, numSpells)
        end

        if replacement then
            local button = _G["SpellBookSkillLineTab"..tab]
            local text = _G["SpellBookSkillLineTab"..tab.."Text"]
            if button then
                button.tooltip = replacement
            end
            if text then
                text:SetText(replacement)
            end
        end
    end
end

local frame = CreateFrame("Frame")
frame:RegisterEvent("PLAYER_ENTERING_WORLD")
frame:RegisterEvent("PLAYER_LOGIN")
frame:RegisterEvent("SKILL_LINES_CHANGED")
frame:RegisterEvent("LEARNED_SPELL_IN_TAB")
frame:RegisterEvent("SPELLS_CHANGED")
frame:RegisterEvent("UNIT_LEVEL")
frame:SetScript("OnEvent", function(self, event, unit)
    if event == "UNIT_LEVEL" and unit ~= "player" then
        return
    end
    GPTDH_UpdateCharacterClassText()
    GPTDH_UpdateSpellbookClassText()
end)

if hooksecurefunc then
    if CharacterFrame_OnShow then
        hooksecurefunc("CharacterFrame_OnShow", GPTDH_UpdateCharacterClassText)
    end
    if PaperDollFrame_SetLevel then
        hooksecurefunc("PaperDollFrame_SetLevel", GPTDH_UpdateCharacterClassText)
    end
    if PaperDollFrame_UpdateStats then
        hooksecurefunc("PaperDollFrame_UpdateStats", GPTDH_UpdateCharacterClassText)
    end
    if SpellBookFrame_UpdateSkillLineTabs then
        hooksecurefunc("SpellBookFrame_UpdateSkillLineTabs", GPTDH_UpdateSpellbookClassText)
    end
    if SpellBookFrame_Update then
        hooksecurefunc("SpellBookFrame_Update", GPTDH_UpdateSpellbookClassText)
    end
end
''',
        encoding="utf-8",
        newline="",
    )


def build_patch(install_server_dbc=False, output_path=None):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    remix = load_remix_builder()
    remix_server_dbc = remix.SERVER_DBC

    staging = OUT_DIR / "mpq_staging"
    if staging.exists():
        shutil.rmtree(staging)
    (staging / "DBFilesClient").mkdir(parents=True)

    if USE_WORGOBLIN_VENDOR_PATCH:
        copy_vendor_patch(staging)
    patch_remix_shirt_icon(staging, install_server_dbc)
    patch_demon_hunter_glaive_displays(staging, install_server_dbc)
    patch_demon_hunter_items(staging, install_server_dbc)
    patch_demon_hunter_spell_visual_dbcs(staging, install_server_dbc)

    # Preserve the existing Remix and Razorhill flight-path client DBCs.
    for name in ["TaxiNodes.dbc", "TaxiPath.dbc", "TaxiPathNode.dbc"]:
        src = remix.TAXI_DIR / name
        if src.exists():
            shutil.copy2(src, staging / "DBFilesClient" / name)
    remix.SERVER_DBC = remix_server_dbc
    shutil.copy2(remix.patched_currency_types(), staging / "DBFilesClient" / "CurrencyTypes.dbc")
    if USE_WORGOBLIN_VENDOR_PATCH:
        remix.SERVER_DBC = WORGOBLIN_PATCH / "DBFilesClient"
    shutil.copy2(remix.patched_spell(), OUT_DIR / "Spell.dbc")
    normalize_goblin_better_living_spell(OUT_DIR / "Spell.dbc")
    shutil.copy2(remix.patched_spell_icon(), OUT_DIR / "SpellIcon.dbc")
    remix.SERVER_DBC = remix_server_dbc
    remix.build_icon_textures(staging)

    if USE_WORGOBLIN_VENDOR_PATCH:
        patched = patched_demon_hunter_dbcs(staging)
    else:
        patched = [
            patched_chr_races(),
            *patched_creature_display_models(),
            patched_char_base_info(),
            patched_char_start_outfit(),
            patched_skill_race_class_info(),
            *patched_factions(),
            *patched_racial_spells(),
            *patched_demon_hunter_dbcs(staging),
        ]

    for dbc in patched:
        shutil.copy2(dbc, staging / "DBFilesClient" / dbc.name)
        if install_server_dbc and dbc.name in {"ChrRaces.dbc", "CreatureModelData.dbc", "CreatureDisplayInfo.dbc", "CharBaseInfo.dbc", "CharStartOutfit.dbc", "SkillRaceClassInfo.dbc", "Faction.dbc", "FactionTemplate.dbc", "Spell.dbc", "SpellIcon.dbc"}:
            shutil.copy2(dbc, SERVER_DBC / dbc.name)

    if not USE_WORGOBLIN_VENDOR_PATCH:
        patch_glue_files(staging)
        build_custom_race_icons(staging)

    patch_demon_hunter_glue(staging)
    build_demon_hunter_class_icons(staging)
    stage_demon_hunter_ingame_ui(staging)
    stage_demon_hunter_glaive_model(staging)
    stage_demon_hunter_spell_visual_models(staging)
    assert_unsafe_spell_visual_models_absent(staging)

    if not USE_WORGOBLIN_VENDOR_PATCH:
        stage_playable_race_models(staging)

    if install_server_dbc and USE_WORGOBLIN_VENDOR_PATCH:
        for dbc in (staging / "DBFilesClient").glob("*.dbc"):
            shutil.copy2(dbc, SERVER_DBC / dbc.name)
        assert_spell_visual(SERVER_DBC / "Spell.dbc", 910204, 910424, "installed server Spell.dbc")

    target_patch = output_path or CLIENT_PATCH
    if target_patch.exists():
        target_patch.unlink()

    subprocess.run([str(MPQCLI), "create", str(staging), "--output", str(target_patch), "--game", "wow-wotlk"], check=True)
    print(f"Wrote {target_patch}")


if __name__ == "__main__":
    output = None
    if "--output" in sys.argv:
        output_index = sys.argv.index("--output")
        try:
            output = Path(sys.argv[output_index + 1])
        except IndexError as exc:
            raise SystemExit("--output requires a path") from exc
    build_patch("--install-server-dbc" in sys.argv, output)
