#include "Chat.h"
#include "Creature.h"
#include "CreatureScript.h"
#include "DatabaseEnv.h"
#include "Guild.h"
#include "GuildMgr.h"
#include "Item.h"
#include "ItemScript.h"
#include "LootScript.h"
#include "LootMgr.h"
#include "Map.h"
#include "ObjectMgr.h"
#include "Player.h"
#include "PlayerScript.h"
#include "QuestDef.h"
#include "Random.h"
#include "ScriptMgr.h"
#include "ScriptedGossip.h"
#include "SpellAuras.h"
#include "WorldSession.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <sstream>
#include <string>
#include <unordered_map>

namespace Remix
{
constexpr uint32 ITEM_CHRONOTHREAD_SHIRT = 900100;
constexpr uint32 ITEM_TOKEN_CREDIT = 900101;
constexpr uint32 SPELL_REMIX_STAMINA = 900103;
constexpr uint32 SPELL_REMIX_AGILITY = 900104;
constexpr uint32 SPELL_REMIX_STRENGTH = 900105;
constexpr uint32 SPELL_REMIX_INTELLECT = 900106;
constexpr uint32 SPELL_REMIX_CRIT = 900107;
constexpr uint32 SPELL_REMIX_HIT = 900108;
constexpr uint32 SPELL_REMIX_SPELL_POWER = 900109;
constexpr uint32 SPELL_REMIX_ATTACK_POWER = 900110;
constexpr uint32 SPELL_REMIX_XP = 900111;
constexpr uint32 SPELL_REMIX_GOLD = 900112;
constexpr uint32 ITEM_REBORN_TOKEN = 900113;
constexpr uint32 SPELL_REBORN_XP = 900114;
constexpr uint32 SPELL_REBORN_REPUTATION = 900115;
constexpr uint32 SPELL_REBORN_TOKEN_DROP = 900116;
constexpr uint32 SPELL_REBORN_MOVEMENT = 900117;
constexpr uint32 GOSSIP_TEXT = 900100;
constexpr uint32 GOSSIP_TEXT_REBORN = 900101;
constexpr uint32 GOSSIP_TEXT_UNICUS = 900102;
constexpr uint32 CHROMIE_REBORN_MIN_LEVEL = 80;
constexpr uint32 REBORN_XP_STACK_CAP = 20;
constexpr uint32 REBORN_REPUTATION_STACK_CAP = 100;
constexpr uint32 REBORN_TOKEN_DROP_STACK_CAP = 15;
constexpr uint32 REBORN_MOVEMENT_STACK_CAP = 15;
constexpr uint32 UNICUS_MOUNT_COST = 10;

enum Action : uint32
{
    ACTION_REFRESH = 1,
    ACTION_STAMINA,
    ACTION_AGILITY,
    ACTION_STRENGTH,
    ACTION_INTELLECT,
    ACTION_CRIT,
    ACTION_HIT,
    ACTION_SPELL_POWER,
    ACTION_ATTACK_POWER,
    ACTION_XP,
    ACTION_GOLD,
    ACTION_REBORN_CONFIRM = 100,
    ACTION_REBORN_CANCEL,
    ACTION_UNICUS_FIRST_MOUNT = 1000
};

struct Progress
{
    uint32 stamina = 0;
    uint32 agility = 0;
    uint32 strength = 0;
    uint32 intellect = 0;
    uint32 crit = 0;
    uint32 hit = 0;
    uint32 spellPower = 0;
    uint32 attackPower = 0;
    uint32 xp = 0;
    uint32 gold = 0;
};

struct Applied
{
    bool active = false;
    uint32 timer = 0;
    std::array<int32, 4> stat = {0, 0, 0, 0}; // strength, agility, stamina, intellect
    int32 crit = 0;
    int32 hit = 0;
    int32 spellPower = 0;
    int32 attackPower = 0;
};

std::unordered_map<uint32, Progress> CharacterProgress;
std::unordered_map<uint32, Progress> AccountProgress;
std::unordered_map<uint32, uint32> RebornProgress;
std::unordered_map<uint32, Applied> AppliedBonuses;

struct PendingLootMoney
{
    uint32 remixBonus = 0;
};

std::unordered_map<uint32, PendingLootMoney> PendingLootMoneyBonuses;

constexpr std::array<uint32, 10> StatusSpells =
{
    SPELL_REMIX_STAMINA,
    SPELL_REMIX_AGILITY,
    SPELL_REMIX_STRENGTH,
    SPELL_REMIX_INTELLECT,
    SPELL_REMIX_CRIT,
    SPELL_REMIX_HIT,
    SPELL_REMIX_SPELL_POWER,
    SPELL_REMIX_ATTACK_POWER,
    SPELL_REMIX_XP,
    SPELL_REMIX_GOLD
};

struct StartPosition
{
    uint32 map = 0;
    float x = -8949.95f;
    float y = -132.493f;
    float z = 83.5312f;
    float o = 0.0f;
};

struct MountSale
{
    uint32 item;
    char const* name;
};

constexpr std::array<MountSale, 10> UnicusMounts =
{{
    {19902, "Swift Zulian Tiger"},
    {19872, "Swift Razzashi Raptor"},
    {21176, "Black Qiraji Resonating Crystal"},
    {33809, "Amani War Bear"},
    {43599, "Big Blizzard Bear"},
    {49284, "Reins of the Swift Spectral Tiger"},
    {49282, "Big Battle Bear"},
    {49290, "Magic Rooster Egg"},
    {49285, "X-51 Nether-Rocket"},
    {49286, "X-51 Nether-Rocket X-TREME"}
}};

uint32 Guid(Player const* player)
{
    return player->GetGUID().GetCounter();
}

uint32 Account(Player const* player)
{
    return player->GetSession()->GetAccountId();
}

Progress LoadCharacterProgress(Player const* player)
{
    uint32 guid = Guid(player);
    auto itr = CharacterProgress.find(guid);
    if (itr != CharacterProgress.end())
        return itr->second;

    Progress progress;
    if (QueryResult result = CharacterDatabase.Query(
        "SELECT stamina_rank, agility_rank, strength_rank, intellect_rank, crit_rank, hit_rank, spell_power_rank, attack_power_rank "
        "FROM remix_character_progress WHERE guid = {}", guid))
    {
        Field* fields = result->Fetch();
        progress.stamina = fields[0].Get<uint32>();
        progress.agility = fields[1].Get<uint32>();
        progress.strength = fields[2].Get<uint32>();
        progress.intellect = fields[3].Get<uint32>();
        progress.crit = fields[4].Get<uint32>();
        progress.hit = fields[5].Get<uint32>();
        progress.spellPower = fields[6].Get<uint32>();
        progress.attackPower = fields[7].Get<uint32>();
    }

    CharacterProgress[guid] = progress;
    return progress;
}

Progress LoadAccountProgress(Player const* player)
{
    uint32 account = Account(player);
    auto itr = AccountProgress.find(account);
    if (itr != AccountProgress.end())
        return itr->second;

    Progress progress;
    if (QueryResult result = CharacterDatabase.Query("SELECT xp_rank, gold_rank FROM remix_account_progress WHERE account_id = {}", account))
    {
        Field* fields = result->Fetch();
        progress.xp = fields[0].Get<uint32>();
        progress.gold = fields[1].Get<uint32>();
    }

    AccountProgress[account] = progress;
    return progress;
}

uint32 LoadRebornProgress(Player const* player)
{
    uint32 account = Account(player);
    auto itr = RebornProgress.find(account);
    if (itr != RebornProgress.end())
        return itr->second;

    uint32 reborns = 0;
    if (QueryResult result = CharacterDatabase.Query("SELECT reborn_count FROM remix_reborn_progress WHERE account_id = {}", account))
        reborns = result->Fetch()[0].Get<uint32>();

    RebornProgress[account] = reborns;
    return reborns;
}

void SaveCharacterProgress(Player const* player, Progress const& progress)
{
    uint32 guid = Guid(player);
    CharacterProgress[guid] = progress;
    CharacterDatabase.Execute(
        "REPLACE INTO remix_character_progress "
        "(guid, stamina_rank, agility_rank, strength_rank, intellect_rank, crit_rank, hit_rank, spell_power_rank, attack_power_rank) "
        "VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})",
        guid, progress.stamina, progress.agility, progress.strength, progress.intellect, progress.crit, progress.hit, progress.spellPower, progress.attackPower);
}

void SaveAccountProgress(Player const* player, Progress const& progress)
{
    uint32 account = Account(player);
    AccountProgress[account] = progress;
    CharacterDatabase.Execute(
        "REPLACE INTO remix_account_progress (account_id, xp_rank, gold_rank) VALUES ({}, {}, {})",
        account, progress.xp, progress.gold);
}

void SaveRebornProgress(Player const* player, uint32 reborns)
{
    uint32 account = Account(player);
    RebornProgress[account] = reborns;
    CharacterDatabase.Execute(
        "REPLACE INTO remix_reborn_progress (account_id, reborn_count) VALUES ({}, {})",
        account, reborns);
}

bool HasShirtEquipped(Player const* player)
{
    if (Item const* item = player->GetItemByPos(INVENTORY_SLOT_BAG_0, EQUIPMENT_SLOT_BODY))
        return item->GetEntry() == ITEM_CHRONOTHREAD_SHIRT;
    return false;
}

bool IsCasterClass(Player const* player)
{
    switch (player->getClass())
    {
        case CLASS_MAGE:
        case CLASS_PRIEST:
        case CLASS_WARLOCK:
        case CLASS_DRUID:
        case CLASS_SHAMAN:
        case CLASS_PALADIN:
            return true;
        default:
            return false;
    }
}

bool IsAttackPowerClass(Player const* player)
{
    switch (player->getClass())
    {
        case CLASS_WARRIOR:
        case CLASS_ROGUE:
        case CLASS_HUNTER:
        case CLASS_DEATH_KNIGHT:
        case CLASS_DRUID:
        case CLASS_SHAMAN:
        case CLASS_PALADIN:
            return true;
        default:
            return false;
    }
}

uint32 PercentRank(uint32 rank)
{
    return std::min<uint32>(rank * 5, 500);
}

uint8 AuraStack(uint32 rank)
{
    return uint8(std::clamp<uint32>(rank, 1, 255));
}

uint32 RebornBonusPercent(Player const* player, uint32 percentPerStack, uint32 cap)
{
    return std::min<uint32>(LoadRebornProgress(player), cap) * percentPerStack;
}

uint32 UpgradeCost(uint32 rank, uint32 baseCost)
{
    return baseCost + (rank + 1) * (rank + 1) * (baseCost / 2);
}

uint32 PercentOfMoneyRoundedUp(uint32 copper, uint32 percent)
{
    if (!copper || !percent)
        return 0;

    return uint32((uint64(copper) * percent + 99) / 100);
}

std::string FormatMoney(uint32 copper)
{
    uint32 gold = copper / 10000;
    uint32 silver = (copper / 100) % 100;
    uint32 copperOnly = copper % 100;
    std::ostringstream ss;

    if (gold)
        ss << gold << " Gold";

    if (silver)
    {
        if (ss.tellp() > 0)
            ss << " ";
        ss << silver << " Silver";
    }

    if (copperOnly || !copper)
    {
        if (ss.tellp() > 0)
            ss << " ";
        ss << copperOnly << " Copper";
    }

    return ss.str();
}

bool DepositGuildBankMatch(Player* player, uint32 lootedGold, uint32& depositedGold)
{
    depositedGold = 0;
    if (!player || !lootedGold || !player->GetGuildId())
        return false;

    Guild* guild = sGuildMgr->GetGuildById(player->GetGuildId());
    if (!guild)
        return false;

    depositedGold = PercentOfMoneyRoundedUp(lootedGold, 10);
    if (!depositedGold || guild->GetTotalBankMoney() > GUILD_BANK_MONEY_LIMIT - depositedGold)
    {
        depositedGold = 0;
        return false;
    }

    CharacterDatabaseTransaction trans = CharacterDatabase.BeginTransaction();
    if (!guild->ModifyBankMoney(trans, depositedGold, true))
    {
        depositedGold = 0;
        return false;
    }

    CharacterDatabase.CommitTransaction(trans);
    return true;
}

std::string Icon(std::string const& name)
{
    return "|TInterface/Icons/" + name + ":30:30:-18:0|t";
}

int32 PercentBonus(float base, uint32 rank, int32 minimumPerRank = 1)
{
    if (!rank)
        return 0;

    int32 amount = int32(std::floor(base * float(PercentRank(rank)) / 100.0f));
    return std::max<int32>(amount, int32(rank) * minimumPerRank);
}

uint32 TokenCount(Player const* player)
{
    return player->GetItemCount(ITEM_TOKEN_CREDIT, true);
}

bool SpendTokens(Player* player, uint32 cost)
{
    if (TokenCount(player) < cost)
    {
        ChatHandler(player->GetSession()).PSendSysMessage("You need {} Token Credits.", cost);
        return false;
    }

    player->DestroyItemCount(ITEM_TOKEN_CREDIT, cost, true);
    return true;
}

void RemoveStatusAuras(Player* player)
{
    for (uint32 spellId : StatusSpells)
        player->RemoveAurasDueToSpell(spellId);
}

void SetStatusAura(Player* player, uint32 spellId, uint32 rank)
{
    if (!rank)
    {
        player->RemoveAurasDueToSpell(spellId);
        return;
    }

    Aura* aura = player->GetAura(spellId);
    if (!aura)
        aura = player->AddAura(spellId, player);

    if (aura)
        aura->SetStackAmount(AuraStack(rank));
}

void SyncStatusAuras(Player* player)
{
    if (!HasShirtEquipped(player))
    {
        RemoveStatusAuras(player);
        return;
    }

    Progress character = LoadCharacterProgress(player);
    Progress account = LoadAccountProgress(player);

    SetStatusAura(player, SPELL_REMIX_STAMINA, character.stamina);
    SetStatusAura(player, SPELL_REMIX_AGILITY, character.agility);
    SetStatusAura(player, SPELL_REMIX_STRENGTH, character.strength);
    SetStatusAura(player, SPELL_REMIX_INTELLECT, character.intellect);
    SetStatusAura(player, SPELL_REMIX_CRIT, character.crit);
    SetStatusAura(player, SPELL_REMIX_HIT, character.hit);
    SetStatusAura(player, SPELL_REMIX_SPELL_POWER, IsCasterClass(player) ? character.spellPower : 0);
    SetStatusAura(player, SPELL_REMIX_ATTACK_POWER, IsAttackPowerClass(player) ? character.attackPower : 0);
    SetStatusAura(player, SPELL_REMIX_XP, account.xp);
    SetStatusAura(player, SPELL_REMIX_GOLD, account.gold);
}

void SyncRebornAuras(Player* player)
{
    uint32 reborns = LoadRebornProgress(player);
    SetStatusAura(player, SPELL_REBORN_XP, std::min<uint32>(reborns, REBORN_XP_STACK_CAP));
    SetStatusAura(player, SPELL_REBORN_REPUTATION, std::min<uint32>(reborns, REBORN_REPUTATION_STACK_CAP));
    SetStatusAura(player, SPELL_REBORN_TOKEN_DROP, std::min<uint32>(reborns, REBORN_TOKEN_DROP_STACK_CAP));
    SetStatusAura(player, SPELL_REBORN_MOVEMENT, std::min<uint32>(reborns, REBORN_MOVEMENT_STACK_CAP));
}

void RemoveApplied(Player* player, Applied& applied)
{
    if (!HasShirtEquipped(player))
        RemoveStatusAuras(player);

    if (!applied.active)
        return;

    player->HandleStatFlatModifier(UNIT_MOD_STAT_STRENGTH, TOTAL_VALUE, float(applied.stat[0]), false);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_AGILITY, TOTAL_VALUE, float(applied.stat[1]), false);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_STAMINA, TOTAL_VALUE, float(applied.stat[2]), false);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_INTELLECT, TOTAL_VALUE, float(applied.stat[3]), false);
    player->UpdateStatBuffMod(STAT_STRENGTH);
    player->UpdateStatBuffMod(STAT_AGILITY);
    player->UpdateStatBuffMod(STAT_STAMINA);
    player->UpdateStatBuffMod(STAT_INTELLECT);

    player->ApplyRatingMod(CR_CRIT_MELEE, applied.crit, false);
    player->ApplyRatingMod(CR_CRIT_RANGED, applied.crit, false);
    player->ApplyRatingMod(CR_CRIT_SPELL, applied.crit, false);
    player->ApplyRatingMod(CR_HIT_MELEE, applied.hit, false);
    player->ApplyRatingMod(CR_HIT_RANGED, applied.hit, false);
    player->ApplyRatingMod(CR_HIT_SPELL, applied.hit, false);
    player->ApplySpellPowerBonus(applied.spellPower, false);
    player->HandleStatFlatModifier(UNIT_MOD_ATTACK_POWER, TOTAL_VALUE, float(applied.attackPower), false);
    player->HandleStatFlatModifier(UNIT_MOD_ATTACK_POWER_RANGED, TOTAL_VALUE, float(applied.attackPower), false);

    applied = Applied();
    player->UpdateAllStats();
}

void ApplyProgress(Player* player, bool force = false)
{
    uint32 guid = Guid(player);
    Applied& applied = AppliedBonuses[guid];

    if (!force && applied.timer < 3000)
        return;

    applied.timer = 0;
    bool equipped = HasShirtEquipped(player);
    if (!equipped)
    {
        RemoveApplied(player, applied);
        RemoveStatusAuras(player);
        return;
    }

    Progress progress = LoadCharacterProgress(player);
    bool restoreHealth = player->IsAlive();
    uint32 healthBeforeRefresh = restoreHealth ? player->GetHealth() : 0;
    RemoveApplied(player, applied);

    applied.active = true;
    applied.stat[0] = PercentBonus(player->GetStat(STAT_STRENGTH), progress.strength);
    applied.stat[1] = PercentBonus(player->GetStat(STAT_AGILITY), progress.agility);
    applied.stat[2] = int32(progress.stamina * 10);
    applied.stat[3] = PercentBonus(player->GetStat(STAT_INTELLECT), progress.intellect);

    uint32 critBase = player->GetUInt32Value(PLAYER_FIELD_COMBAT_RATING_1 + CR_CRIT_MELEE);
    uint32 hitBase = player->GetUInt32Value(PLAYER_FIELD_COMBAT_RATING_1 + CR_HIT_MELEE);
    applied.crit = PercentBonus(float(critBase), progress.crit, 2);
    applied.hit = PercentBonus(float(hitBase), progress.hit, 2);

    if (IsCasterClass(player))
        applied.spellPower = PercentBonus(float(player->GetBaseSpellPowerBonus()), progress.spellPower, 2);

    if (IsAttackPowerClass(player))
        applied.attackPower = PercentBonus(player->GetTotalAttackPowerValue(BASE_ATTACK), progress.attackPower, 2);

    player->HandleStatFlatModifier(UNIT_MOD_STAT_STRENGTH, TOTAL_VALUE, float(applied.stat[0]), true);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_AGILITY, TOTAL_VALUE, float(applied.stat[1]), true);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_STAMINA, TOTAL_VALUE, float(applied.stat[2]), true);
    player->HandleStatFlatModifier(UNIT_MOD_STAT_INTELLECT, TOTAL_VALUE, float(applied.stat[3]), true);
    player->UpdateStatBuffMod(STAT_STRENGTH);
    player->UpdateStatBuffMod(STAT_AGILITY);
    player->UpdateStatBuffMod(STAT_STAMINA);
    player->UpdateStatBuffMod(STAT_INTELLECT);

    player->ApplyRatingMod(CR_CRIT_MELEE, applied.crit, true);
    player->ApplyRatingMod(CR_CRIT_RANGED, applied.crit, true);
    player->ApplyRatingMod(CR_CRIT_SPELL, applied.crit, true);
    player->ApplyRatingMod(CR_HIT_MELEE, applied.hit, true);
    player->ApplyRatingMod(CR_HIT_RANGED, applied.hit, true);
    player->ApplyRatingMod(CR_HIT_SPELL, applied.hit, true);
    player->ApplySpellPowerBonus(applied.spellPower, true);
    player->HandleStatFlatModifier(UNIT_MOD_ATTACK_POWER, TOTAL_VALUE, float(applied.attackPower), true);
    player->HandleStatFlatModifier(UNIT_MOD_ATTACK_POWER_RANGED, TOTAL_VALUE, float(applied.attackPower), true);
    player->UpdateAllStats();
    if (restoreHealth)
        player->SetHealth(std::min<uint32>(healthBeforeRefresh, player->GetMaxHealth()));
    SyncStatusAuras(player);
}

uint32 ScaledDrop(Creature const* killed)
{
    uint32 level = std::clamp<uint32>(killed->GetLevel(), 1, 80);
    uint32 min = 1;
    uint32 max = 500;

    uint32 rank = killed->GetCreatureTemplate()->rank;
    if ((killed->isWorldBoss() || killed->IsDungeonBoss()) && killed->GetMap() && killed->GetMap()->IsRaid())
    {
        min = 5000; max = 15000;
    }
    else if (killed->isWorldBoss() || killed->IsDungeonBoss() || rank == CREATURE_ELITE_WORLDBOSS)
    {
        min = 50; max = 5000;
    }
    else if (rank == CREATURE_ELITE_RAREELITE)
    {
        min = 100; max = 3500;
    }
    else if (rank == CREATURE_ELITE_RARE)
    {
        min = 50; max = 2000;
    }
    else if (rank == CREATURE_ELITE_ELITE)
    {
        min = 25; max = 2500;
    }

    uint32 scaledMax = min + uint32((uint64(max - min) * (level - 1)) / 79);
    return urand(min, std::max(min, scaledMax));
}

void AddUpgradeLine(Player* player, std::string const& icon, std::string const& label, uint32 rank, uint32 maxRank, uint32 cost, uint32 action)
{
    std::ostringstream ss;
    ss << Icon(icon) << label << " ";
    if (maxRank)
        ss << "(" << rank << "/" << maxRank << ") ";
    else
        ss << "(" << rank << ") ";
    ss << "- Cost: " << cost;
    if (maxRank && rank >= maxRank)
        ss << " [Capped]";
    AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, ss.str(), GOSSIP_SENDER_MAIN, action);
}

void ShowMenu(Player* player, Item* item)
{
    Progress character = LoadCharacterProgress(player);
    Progress account = LoadAccountProgress(player);
    ClearGossipMenuFor(player);

    (void)character;
    (void)account;
    AddGossipItemFor(player, GOSSIP_ICON_CHAT, "|cffff2020Token Credits|r: " + std::to_string(TokenCount(player)), GOSSIP_SENDER_MAIN, ACTION_REFRESH);

    AddUpgradeLine(player, "remix_stamina", "Stamina +10", character.stamina, 0, UpgradeCost(character.stamina, 50), ACTION_STAMINA);
    AddUpgradeLine(player, "remix_agility", "Agility +5%", character.agility, 100, UpgradeCost(character.agility, 125), ACTION_AGILITY);
    AddUpgradeLine(player, "remix_strength", "Strength +5%", character.strength, 100, UpgradeCost(character.strength, 125), ACTION_STRENGTH);
    AddUpgradeLine(player, "remix_intellect", "Intellect +5%", character.intellect, 100, UpgradeCost(character.intellect, 125), ACTION_INTELLECT);
    AddUpgradeLine(player, "remix_critical_strike", "Critical Strike +5%", character.crit, 100, UpgradeCost(character.crit, 150), ACTION_CRIT);
    AddUpgradeLine(player, "remix_hit", "Hit +5%", character.hit, 100, UpgradeCost(character.hit, 150), ACTION_HIT);

    if (IsCasterClass(player))
        AddUpgradeLine(player, "remix_spell_damage", "Spell Damage +5%", character.spellPower, 100, UpgradeCost(character.spellPower, 175), ACTION_SPELL_POWER);

    if (IsAttackPowerClass(player))
        AddUpgradeLine(player, "remix_attack_power", "Attack Power +5%", character.attackPower, 100, UpgradeCost(character.attackPower, 175), ACTION_ATTACK_POWER);

    AddUpgradeLine(player, "remix_experience", "Account XP +5%", account.xp, 40, UpgradeCost(account.xp, 200), ACTION_XP);
    AddUpgradeLine(player, "remix_gold_loot", "Account Gold Loot +1%", account.gold, 50, UpgradeCost(account.gold, 150), ACTION_GOLD);
    SendGossipMenuFor(player, GOSSIP_TEXT, item->GetGUID());
}

bool UpgradeCharacter(Player* player, uint32 Progress::*field, uint32 maxRank, uint32 baseCost)
{
    Progress progress = LoadCharacterProgress(player);
    uint32 rank = progress.*field;
    if (maxRank && rank >= maxRank)
        return false;
    uint32 cost = UpgradeCost(rank, baseCost);
    if (!SpendTokens(player, cost))
        return false;
    progress.*field = rank + 1;
    SaveCharacterProgress(player, progress);
    ApplyProgress(player, true);
    return true;
}

bool UpgradeAccount(Player* player, uint32 Progress::*field, uint32 maxRank, uint32 baseCost)
{
    Progress progress = LoadAccountProgress(player);
    uint32 rank = progress.*field;
    if (rank >= maxRank)
        return false;
    uint32 cost = UpgradeCost(rank, baseCost);
    if (!SpendTokens(player, cost))
        return false;
    progress.*field = rank + 1;
    SaveAccountProgress(player, progress);
    SyncStatusAuras(player);
    return true;
}

void ResetRemixCharacterProgress(Player* player)
{
    Progress empty;
    SaveCharacterProgress(player, empty);
    ApplyProgress(player, true);
}

bool MoveItemToBank(Player* player, uint8 bag, uint8 slot)
{
    Item* item = player->GetItemByPos(bag, slot);
    if (!item)
        return true;

    ItemPosCountVec dest;
    InventoryResult msg = player->CanBankItem(NULL_BAG, NULL_SLOT, dest, item, false);
    if (msg != EQUIP_ERR_OK)
    {
        player->SendEquipError(msg, item, nullptr);
        return false;
    }

    player->RemoveItem(bag, slot, true);
    player->ItemRemovedQuestCheck(item->GetEntry(), item->GetCount());
    player->BankItem(dest, item, true);
    player->UpdateTitansGrip();
    return true;
}

bool MoveEquippedGearToBank(Player* player)
{
    bool movedAll = true;
    for (uint8 slot = EQUIPMENT_SLOT_HEAD; slot < EQUIPMENT_SLOT_END; ++slot)
    {
        if (slot == EQUIPMENT_SLOT_BODY)
            continue;

        if (Item* item = player->GetItemByPos(INVENTORY_SLOT_BAG_0, slot))
        {
            if (MoveItemToBank(player, INVENTORY_SLOT_BAG_0, slot))
                continue;
            else
            {
                movedAll = false;
                ChatHandler(player->GetSession()).PSendSysMessage("Could not move {} to the bank. Make bank space and try again.", item->GetTemplate()->Name1);
            }
        }
    }
    return movedAll;
}

StartPosition GetStartPosition(Player* player)
{
    if (QueryResult result = WorldDatabase.Query(
        "SELECT map, position_x, position_y, position_z, orientation FROM playercreateinfo WHERE race = {} AND class = {}",
        player->getRace(), player->getClass()))
    {
        Field* fields = result->Fetch();
        return {fields[0].Get<uint32>(), fields[1].Get<float>(), fields[2].Get<float>(), fields[3].Get<float>(), fields[4].Get<float>()};
    }

    return {};
}

void ClearQuestState(Player* player)
{
    uint32 guid = Guid(player);

    for (uint8 slot = 0; slot < MAX_QUEST_LOG_SIZE; ++slot)
    {
        uint32 quest = player->GetQuestSlotQuestId(slot);
        if (!quest)
            continue;

        player->SetQuestSlot(slot, 0);
        player->SetQuestStatus(quest, QUEST_STATUS_NONE);
    }

    if (QueryResult result = CharacterDatabase.Query("SELECT quest FROM character_queststatus_rewarded WHERE guid = {}", guid))
    {
        do
        {
            player->RemoveRewardedQuest(result->Fetch()[0].Get<uint32>());
        } while (result->NextRow());
    }

    CharacterDatabase.Execute("DELETE FROM character_queststatus WHERE guid = {}", guid);
    CharacterDatabase.Execute("DELETE FROM character_queststatus_rewarded WHERE guid = {}", guid);
    CharacterDatabase.Execute("DELETE FROM character_queststatus_daily WHERE guid = {}", guid);
    CharacterDatabase.Execute("DELETE FROM character_queststatus_weekly WHERE guid = {}", guid);
    CharacterDatabase.Execute("DELETE FROM character_queststatus_monthly WHERE guid = {}", guid);
    CharacterDatabase.Execute("DELETE FROM character_queststatus_seasonal WHERE guid = {}", guid);
}

void GiveStarterItems(Player* player)
{
    if (QueryResult result = WorldDatabase.Query(
        "SELECT itemid, amount FROM playercreateinfo_item WHERE (race = 0 OR race = {}) AND (class = 0 OR class = {})",
        player->getRace(), player->getClass()))
    {
        do
        {
            Field* fields = result->Fetch();
            uint32 itemId = fields[0].Get<uint32>();
            if (itemId == ITEM_CHRONOTHREAD_SHIRT && player->HasItemCount(ITEM_CHRONOTHREAD_SHIRT, 1, true))
                continue;

            player->AddItem(itemId, std::max<uint32>(fields[1].Get<uint32>(), 1));
        } while (result->NextRow());
    }
}

void ResetStarterActions(Player* player)
{
    uint32 guid = Guid(player);
    CharacterDatabase.Execute("DELETE FROM character_action WHERE guid = {}", guid);

    if (QueryResult result = WorldDatabase.Query(
        "SELECT button, action, type FROM playercreateinfo_action WHERE race = {} AND class = {} ORDER BY button",
        player->getRace(), player->getClass()))
    {
        do
        {
            Field* fields = result->Fetch();
            uint8 button = fields[0].Get<uint8>();
            uint32 action = fields[1].Get<uint32>();
            uint8 type = fields[2].Get<uint8>();

            CharacterDatabase.Execute(
                "INSERT INTO character_action (guid, spec, button, action, type) VALUES ({}, 0, {}, {}, {})",
                guid, button, action, type);

            if (ActionButton* actionButton = player->addActionButton(button, action, type))
                actionButton->uState = ACTIONBUTTON_UNCHANGED;
        } while (result->NextRow());
    }

    player->SendInitialActionButtons();
}

void ResetLevel(Player* player)
{
    if (!player->IsAlive())
        player->ResurrectPlayer(1.0f);

    player->GiveLevel(1);
    player->SetUInt32Value(PLAYER_XP, 0);
    player->resetSpells();
    player->resetTalents(true);
    player->LearnDefaultSkills();
    player->LearnCustomSpells();
    player->InitTalentForLevel();
    player->InitStatsForLevel(true);
    player->SetFullHealth();
    player->SetPower(POWER_MANA, player->GetMaxPower(POWER_MANA));
}

bool RebornPlayer(Player* player)
{
    if (player->GetLevel() < CHROMIE_REBORN_MIN_LEVEL)
    {
        ChatHandler(player->GetSession()).PSendSysMessage("Chromie will only Reborn characters who have reached level {}.", CHROMIE_REBORN_MIN_LEVEL);
        return false;
    }

    CloseGossipMenuFor(player);
    RemoveApplied(player, AppliedBonuses[Guid(player)]);
    if (!MoveEquippedGearToBank(player))
        return false;

    ResetRemixCharacterProgress(player);
    ClearQuestState(player);
    ResetLevel(player);
    GiveStarterItems(player);
    ResetStarterActions(player);

    uint32 reborns = LoadRebornProgress(player) + 1;
    SaveRebornProgress(player, reborns);
    player->AddItem(ITEM_REBORN_TOKEN, 1);
    SyncRebornAuras(player);

    StartPosition start = GetStartPosition(player);
    player->TeleportTo(start.map, start.x, start.y, start.z, start.o);
    player->SaveToDB(false, false);

    ChatHandler(player->GetSession()).PSendSysMessage("You have been Reborn. Reborn count: {}.", reborns);
    return true;
}

void ShowChromieMenu(Player* player, Creature* creature)
{
    ClearGossipMenuFor(player);
    AddGossipItemFor(player, GOSSIP_ICON_CHAT, "Reborn my character.", GOSSIP_SENDER_MAIN, ACTION_REBORN_CONFIRM,
        "Are you sure you wish to Reborn?\n\nYou will:\nBe reset to level 1, lose Remix Shirt progress, and have all quests reset.\nYour current gear will be moved to your bank.\n\nThe trade off is:\n1 Reborn Token, a 5% experience buff that stacks, a 5% increase to all reputation gain, a 2% increase to all movement speeds, and a 100% more Remix token drop increase per Reborn.",
        0, false);
    AddGossipItemFor(player, GOSSIP_ICON_CHAT, "On second thought...", GOSSIP_SENDER_MAIN, ACTION_REBORN_CANCEL);
    SendGossipMenuFor(player, GOSSIP_TEXT_REBORN, creature->GetGUID());
}

void ShowUnicusMenu(Player* player, Creature* creature)
{
    ClearGossipMenuFor(player);
    AddGossipItemFor(player, GOSSIP_ICON_CHAT, "|cffff2020Token Credits|r: " + std::to_string(TokenCount(player)), GOSSIP_SENDER_MAIN, ACTION_REFRESH);

    for (uint32 i = 0; i < UnicusMounts.size(); ++i)
    {
        std::ostringstream ss;
        ss << UnicusMounts[i].name << " - " << UNICUS_MOUNT_COST << " Token Credits";
        AddGossipItemFor(player, GOSSIP_ICON_MONEY_BAG, ss.str(), GOSSIP_SENDER_MAIN, ACTION_UNICUS_FIRST_MOUNT + i);
    }

    SendGossipMenuFor(player, GOSSIP_TEXT_UNICUS, creature->GetGUID());
}

void BuyUnicusMount(Player* player, Creature* creature, uint32 action)
{
    uint32 index = action - ACTION_UNICUS_FIRST_MOUNT;
    if (index >= UnicusMounts.size())
        return;

    MountSale const& sale = UnicusMounts[index];
    if (!SpendTokens(player, UNICUS_MOUNT_COST))
    {
        ShowUnicusMenu(player, creature);
        return;
    }

    if (!player->AddItem(sale.item, 1))
    {
        player->AddItem(ITEM_TOKEN_CREDIT, UNICUS_MOUNT_COST);
        ChatHandler(player->GetSession()).PSendSysMessage("Make room in your bags and try again.");
    }

    ShowUnicusMenu(player, creature);
}
}

class remix_shirt_item : public ItemScript
{
public:
    remix_shirt_item() : ItemScript("item_remix_shirt") { }

    bool OnUse(Player* player, Item* item, SpellCastTargets const&) override
    {
        Remix::ShowMenu(player, item);
        return true;
    }

    void OnGossipSelect(Player* player, Item* item, uint32, uint32 action) override
    {
        switch (action)
        {
            case Remix::ACTION_STAMINA:
                Remix::UpgradeCharacter(player, &Remix::Progress::stamina, 0, 50);
                break;
            case Remix::ACTION_AGILITY:
                Remix::UpgradeCharacter(player, &Remix::Progress::agility, 100, 125);
                break;
            case Remix::ACTION_STRENGTH:
                Remix::UpgradeCharacter(player, &Remix::Progress::strength, 100, 125);
                break;
            case Remix::ACTION_INTELLECT:
                Remix::UpgradeCharacter(player, &Remix::Progress::intellect, 100, 125);
                break;
            case Remix::ACTION_CRIT:
                Remix::UpgradeCharacter(player, &Remix::Progress::crit, 100, 150);
                break;
            case Remix::ACTION_HIT:
                Remix::UpgradeCharacter(player, &Remix::Progress::hit, 100, 150);
                break;
            case Remix::ACTION_SPELL_POWER:
                Remix::UpgradeCharacter(player, &Remix::Progress::spellPower, 100, 175);
                break;
            case Remix::ACTION_ATTACK_POWER:
                Remix::UpgradeCharacter(player, &Remix::Progress::attackPower, 100, 175);
                break;
            case Remix::ACTION_XP:
                Remix::UpgradeAccount(player, &Remix::Progress::xp, 40, 200);
                break;
            case Remix::ACTION_GOLD:
                Remix::UpgradeAccount(player, &Remix::Progress::gold, 50, 150);
                break;
            default:
                break;
        }

        Remix::ShowMenu(player, item);
    }
};

class remix_player_hooks : public PlayerScript
{
public:
    remix_player_hooks() : PlayerScript("remix_player_hooks") { }

    void OnPlayerLogin(Player* player) override
    {
        Remix::LoadCharacterProgress(player);
        Remix::LoadAccountProgress(player);
        Remix::LoadRebornProgress(player);
        Remix::ApplyProgress(player, true);
        Remix::SyncRebornAuras(player);
    }

    void OnPlayerBeforeLogout(Player* player) override
    {
        Remix::RemoveStatusAuras(player);
        Remix::PendingLootMoneyBonuses.erase(Remix::Guid(player));
        auto itr = Remix::AppliedBonuses.find(Remix::Guid(player));
        if (itr != Remix::AppliedBonuses.end())
            Remix::RemoveApplied(player, itr->second);
    }

    void OnPlayerUpdate(Player* player, uint32 diff) override
    {
        Remix::Applied& applied = Remix::AppliedBonuses[Remix::Guid(player)];
        applied.timer += diff;
        Remix::ApplyProgress(player);
    }

    void OnPlayerCreatureKill(Player* killer, Creature* killed) override
    {
        if (!killed || killed->IsPet() || !killed->GetCreatureTemplate() || !killed->GetCreatureTemplate()->lootid)
            return;

        uint32 amount = Remix::ScaledDrop(killed);
        uint32 rebornBonus = Remix::RebornBonusPercent(killer, 100, Remix::REBORN_TOKEN_DROP_STACK_CAP);
        if (rebornBonus)
            amount += uint32((uint64(amount) * rebornBonus) / 100);

        killer->AddItem(Remix::ITEM_TOKEN_CREDIT, amount);
    }

    void OnPlayerCreatureKilledByPet(Player* owner, Creature* killed) override
    {
        OnPlayerCreatureKill(owner, killed);
    }

    void OnPlayerGiveXP(Player* player, uint32& amount, Unit*, uint8) override
    {
        Remix::Progress progress = Remix::LoadAccountProgress(player);
        if (progress.xp)
            amount += uint32((uint64(amount) * std::min<uint32>(progress.xp * 5, 200)) / 100);

        uint32 rebornBonus = Remix::RebornBonusPercent(player, 5, Remix::REBORN_XP_STACK_CAP);
        if (rebornBonus)
            amount += uint32((uint64(amount) * rebornBonus) / 100);
    }

    void OnPlayerQuestComputeXP(Player* player, Quest const*, uint32& xpValue) override
    {
        Remix::Progress progress = Remix::LoadAccountProgress(player);
        if (progress.xp)
            xpValue += uint32((uint64(xpValue) * std::min<uint32>(progress.xp * 5, 200)) / 100);

        uint32 rebornBonus = Remix::RebornBonusPercent(player, 5, Remix::REBORN_XP_STACK_CAP);
        if (rebornBonus)
            xpValue += uint32((uint64(xpValue) * rebornBonus) / 100);
    }

    void OnPlayerGiveReputation(Player* player, int32, float& rate, ReputationSource) override
    {
        uint32 rebornBonus = Remix::RebornBonusPercent(player, 5, Remix::REBORN_REPUTATION_STACK_CAP);
        if (rebornBonus)
            rate *= 1.0f + (float(rebornBonus) / 100.0f);
    }

    void OnPlayerBeforeLootMoney(Player* player, Loot* loot) override
    {
        Remix::Progress progress = Remix::LoadAccountProgress(player);
        if (loot && loot->gold && progress.gold)
        {
            uint32 bonus = Remix::PercentOfMoneyRoundedUp(loot->gold, std::min<uint32>(progress.gold, 50));
            if (bonus)
            {
                Remix::PendingLootMoneyBonuses[Remix::Guid(player)].remixBonus = bonus;
                loot->gold += bonus;
            }
        }
    }
};

class npc_chromie_reborn : public CreatureScript
{
public:
    npc_chromie_reborn() : CreatureScript("npc_chromie_reborn") { }

    bool OnGossipHello(Player* player, Creature* creature) override
    {
        Remix::ShowChromieMenu(player, creature);
        return true;
    }

    bool OnGossipSelect(Player* player, Creature* creature, uint32, uint32 action) override
    {
        if (action == Remix::ACTION_REBORN_CONFIRM)
        {
            Remix::RebornPlayer(player);
            return true;
        }

        CloseGossipMenuFor(player);
        return true;
    }
};

class npc_unicus_reborn_vendor : public CreatureScript
{
public:
    npc_unicus_reborn_vendor() : CreatureScript("npc_unicus_reborn_vendor") { }

    bool OnGossipHello(Player* player, Creature* creature) override
    {
        Remix::ShowUnicusMenu(player, creature);
        return true;
    }

    bool OnGossipSelect(Player* player, Creature* creature, uint32, uint32 action) override
    {
        if (action >= Remix::ACTION_UNICUS_FIRST_MOUNT)
            Remix::BuyUnicusMount(player, creature, action);
        else
            Remix::ShowUnicusMenu(player, creature);

        return true;
    }
};

class remix_loot_hooks : public LootScript
{
public:
    remix_loot_hooks() : LootScript("remix_loot_hooks") { }

    void OnLootMoney(Player* player, uint32 gold) override
    {
        uint32 remixBonus = 0;
        auto itr = Remix::PendingLootMoneyBonuses.find(Remix::Guid(player));
        if (itr != Remix::PendingLootMoneyBonuses.end())
        {
            remixBonus = itr->second.remixBonus;
            Remix::PendingLootMoneyBonuses.erase(itr);
        }

        uint32 guildDeposit = 0;
        Remix::DepositGuildBankMatch(player, gold, guildDeposit);

        if (!remixBonus && !guildDeposit)
            return;

        ChatHandler chat(player->GetSession());
        if (remixBonus)
            chat.PSendSysMessage("You receive {} extra from |cff00c8c8Remix Gold Loot|r.", Remix::FormatMoney(remixBonus));

        if (guildDeposit)
            chat.PSendSysMessage("Your |cff00c8c8guild bank|r receives {}.", Remix::FormatMoney(guildDeposit));
    }
};

void AddSC_remix_system()
{
    new remix_shirt_item();
    new remix_player_hooks();
    new remix_loot_hooks();
    new npc_chromie_reborn();
    new npc_unicus_reborn_vendor();
}
