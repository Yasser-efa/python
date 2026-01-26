/**
 * Service Worker - LeetCode Chess Unlocker
 * Système de crédits: 1 problème LeetCode = 1 partie de chess
 */

// Configuration par défaut
const DEFAULT_SETTINGS = {
  minDifficulty: "easy",
  blockedSites: ["chess.com", "lichess.org"],
  resetHour: 0,
  weekendMode: false,
};

const DEFAULT_STATE = {
  credits: 0,
  totalSolved: 0,
  totalGames: 0,
  lastResetDate: new Date().toISOString().split("T")[0],
  settings: DEFAULT_SETTINGS,
};

// IDs des règles de blocage
const CHESS_RULE_ID = 1;
const LICHESS_RULE_ID = 2;

// Mutex pour éviter les appels simultanés
let isUpdatingRules = false;
let isInitialized = false;

/**
 * Initialise l'extension au démarrage
 */
async function initialize() {
  if (isInitialized) {
    console.log("[LeetCode Unlocker] Déjà initialisé");
    return;
  }
  isInitialized = true;

  console.log("[LeetCode Unlocker] Initialisation...");

  const data = await chrome.storage.local.get(null);

  if (data.credits === undefined) {
    await chrome.storage.local.set(DEFAULT_STATE);
    console.log("[LeetCode Unlocker] État initial créé");
  }

  await updateBlockingRules();
  await updateBadge();
  await setupDailyAlarm();
}

/**
 * Configure l'alarme pour vérifications périodiques
 */
async function setupDailyAlarm() {
  await chrome.alarms.clear("dailyReset");
  chrome.alarms.create("dailyReset", {
    periodInMinutes: 60,
  });
}

/**
 * Met à jour les règles de blocage dynamiquement
 */
async function updateBlockingRules() {
  // Éviter les appels simultanés
  if (isUpdatingRules) {
    console.log("[LeetCode Unlocker] Mise à jour déjà en cours, ignoré");
    return;
  }
  isUpdatingRules = true;

  try {
    const data = await chrome.storage.local.get(["credits", "settings"]);
    const settings = data.settings || DEFAULT_SETTINGS;
    const credits = data.credits || 0;
    const hasCredits = credits > 0;

    // Vérifier le mode weekend
    const today = new Date();
    const isWeekend = today.getDay() === 0 || today.getDay() === 6;
    const shouldBlock = !hasCredits && !(settings.weekendMode && isWeekend);

    // URL de redirection vers la page bloquée
    const blockedPageUrl = chrome.runtime.getURL("src/blocked/blocked.html");

    // D'abord supprimer TOUTES les règles existantes
    const existingRules = await chrome.declarativeNetRequest.getDynamicRules();
    const existingRuleIds = existingRules.map((rule) => rule.id);

    console.log(`[LeetCode Unlocker] Règles existantes: ${existingRuleIds.length}`);

    if (existingRuleIds.length > 0) {
      await chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: existingRuleIds,
      });
      console.log("[LeetCode Unlocker] Règles supprimées");
    }

    // Ensuite ajouter les nouvelles règles si nécessaire
    if (shouldBlock) {
      const rulesToAdd = [];

      if (settings.blockedSites.includes("chess.com")) {
        rulesToAdd.push({
          id: CHESS_RULE_ID,
          priority: 1,
          action: { type: "redirect", redirect: { url: blockedPageUrl } },
          condition: {
            requestDomains: ["chess.com", "www.chess.com"],
            resourceTypes: ["main_frame"],
          },
        });
      }

      if (settings.blockedSites.includes("lichess.org")) {
        rulesToAdd.push({
          id: LICHESS_RULE_ID,
          priority: 1,
          action: { type: "redirect", redirect: { url: blockedPageUrl } },
          condition: {
            requestDomains: ["lichess.org", "www.lichess.org"],
            resourceTypes: ["main_frame"],
          },
        });
      }

      if (rulesToAdd.length > 0) {
        await chrome.declarativeNetRequest.updateDynamicRules({
          addRules: rulesToAdd,
        });
        console.log(`[LeetCode Unlocker] ${rulesToAdd.length} règles ajoutées`);
      }
    }

    // Vérifier les règles actuelles
    const currentRules = await chrome.declarativeNetRequest.getDynamicRules();
    console.log(
      `[LeetCode Unlocker] État: ${shouldBlock ? "BLOQUÉ" : "DÉBLOQUÉ"} | Crédits: ${credits} | Règles actives: ${currentRules.length}`
    );
  } catch (error) {
    console.error("[LeetCode Unlocker] Erreur mise à jour règles:", error);
  } finally {
    isUpdatingRules = false;
  }
}

/**
 * Met à jour le badge de l'icône
 */
async function updateBadge() {
  const data = await chrome.storage.local.get(["credits", "settings"]);
  const settings = data.settings || DEFAULT_SETTINGS;
  const credits = data.credits || 0;

  const today = new Date();
  const isWeekend = today.getDay() === 0 || today.getDay() === 6;

  if (settings.weekendMode && isWeekend) {
    await chrome.action.setBadgeText({ text: "WE" });
    await chrome.action.setBadgeBackgroundColor({ color: "#3B82F6" });
  } else if (credits > 0) {
    await chrome.action.setBadgeText({ text: String(credits) });
    await chrome.action.setBadgeBackgroundColor({ color: "#22C55E" });
  } else {
    await chrome.action.setBadgeText({ text: "0" });
    await chrome.action.setBadgeBackgroundColor({ color: "#EF4444" });
  }
}

/**
 * Ajoute un crédit (problème LeetCode résolu)
 */
async function addCredit(difficulty) {
  const data = await chrome.storage.local.get(["credits", "totalSolved", "settings"]);
  const settings = data.settings || DEFAULT_SETTINGS;

  // Vérifier la difficulté minimale
  const difficultyOrder = { easy: 1, medium: 2, hard: 3 };
  const minDiff = difficultyOrder[settings.minDifficulty] || 1;
  const problemDiff = difficultyOrder[difficulty?.toLowerCase()] || 1;

  if (problemDiff < minDiff) {
    console.log(`[LeetCode Unlocker] Difficulté insuffisante: ${difficulty}`);
    return { success: false, reason: "difficulty" };
  }

  const newCredits = (data.credits || 0) + 1;
  const newTotalSolved = (data.totalSolved || 0) + 1;

  await chrome.storage.local.set({
    credits: newCredits,
    totalSolved: newTotalSolved,
  });

  console.log(`[LeetCode Unlocker] +1 crédit! Total: ${newCredits}`);

  await updateBlockingRules();
  await updateBadge();

  // Notification
  try {
    await chrome.notifications.create("credit-added", {
      type: "basic",
      iconUrl: chrome.runtime.getURL("icons/icon-128.png"),
      title: "+1 Crédit Chess!",
      message: `Tu as maintenant ${newCredits} partie${newCredits > 1 ? "s" : ""} de chess disponible${newCredits > 1 ? "s" : ""}.`,
      priority: 2,
    });
  } catch (e) {
    console.error("[LeetCode Unlocker] Erreur notification:", e);
  }

  return { success: true, credits: newCredits };
}

/**
 * Utilise un crédit (partie de chess jouée)
 */
async function useCredit() {
  const data = await chrome.storage.local.get(["credits", "totalGames"]);
  const credits = data.credits || 0;

  if (credits <= 0) {
    console.log("[LeetCode Unlocker] Pas de crédits disponibles");
    return { success: false, reason: "no_credits" };
  }

  const newCredits = credits - 1;
  const newTotalGames = (data.totalGames || 0) + 1;

  await chrome.storage.local.set({
    credits: newCredits,
    totalGames: newTotalGames,
  });

  console.log(`[LeetCode Unlocker] -1 crédit! Reste: ${newCredits}`);

  await updateBlockingRules();
  await updateBadge();

  // Notification si plus de crédits
  if (newCredits === 0) {
    try {
      await chrome.notifications.create("no-credits", {
        type: "basic",
        iconUrl: chrome.runtime.getURL("icons/icon-128.png"),
        title: "Plus de crédits!",
        message: "Résous un problème LeetCode pour débloquer une nouvelle partie.",
        priority: 2,
      });
    } catch (e) {
      console.error("[LeetCode Unlocker] Erreur notification:", e);
    }
  }

  return { success: true, credits: newCredits };
}

// --- Écouteurs d'événements ---

chrome.runtime.onInstalled.addListener(async (details) => {
  console.log("[LeetCode Unlocker] Installation:", details.reason);
  await initialize();
});

chrome.runtime.onStartup.addListener(async () => {
  console.log("[LeetCode Unlocker] Démarrage");
  await initialize();
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === "dailyReset") {
    await updateBlockingRules();
    await updateBadge();
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("[LeetCode Unlocker] Message reçu:", message);

  (async () => {
    try {
      switch (message.type) {
        case "PROBLEM_SOLVED":
          const addResult = await addCredit(message.difficulty);
          sendResponse(addResult);
          break;

        case "GAME_PLAYED":
          const useResult = await useCredit();
          sendResponse(useResult);
          break;

        case "GET_STATUS":
          // Forcer la mise à jour des règles à chaque vérification de statut
          await updateBlockingRules();
          const statusData = await chrome.storage.local.get([
            "credits",
            "totalSolved",
            "totalGames",
            "settings",
          ]);
          sendResponse({
            credits: statusData.credits || 0,
            totalSolved: statusData.totalSolved || 0,
            totalGames: statusData.totalGames || 0,
            settings: statusData.settings || DEFAULT_SETTINGS,
          });
          break;

        case "UPDATE_SETTINGS":
          await chrome.storage.local.set({ settings: message.settings });
          await updateBlockingRules();
          await updateBadge();
          sendResponse({ success: true });
          break;

        default:
          sendResponse({ error: "Type de message inconnu" });
      }
    } catch (error) {
      console.error("[LeetCode Unlocker] Erreur:", error);
      sendResponse({ error: error.message });
    }
  })();

  return true;
});

initialize();
