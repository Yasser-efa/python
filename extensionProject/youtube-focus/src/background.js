/**
 * Background Service Worker - YouTube Focus
 * Gère les timers et la persistence de l'état
 */

const REMINDER_INTERVAL = 15; // minutes
const INACTIVITY_RESET = 30; // minutes

/**
 * Initialise l'extension
 */
async function initialize() {
  console.log("[YouTube Focus] Initialisation...");

  const data = await chrome.storage.local.get("state");
  if (!data.state) {
    await resetState();
  }
}

/**
 * Réinitialise l'état complètement
 */
async function resetState() {
  await chrome.storage.local.set({
    state: {
      sessionStart: null,
      lastActivity: null,
      warningShown: false,
    },
  });
  await chrome.alarms.clear("youtubeReminder");
  console.log("[YouTube Focus] État réinitialisé");
}

/**
 * Démarre ou continue une session
 */
async function handlePageLoad() {
  const now = Date.now();
  const data = await chrome.storage.local.get("state");
  const state = data.state || {};

  // Vérifier si on doit reset (inactivité > 30 min ou première visite)
  const shouldReset =
    !state.lastActivity ||
    now - state.lastActivity > INACTIVITY_RESET * 60 * 1000;

  if (shouldReset) {
    console.log(
      "[YouTube Focus] Nouvelle session (reset après inactivité ou première visite)",
    );
    await chrome.storage.local.set({
      state: {
        sessionStart: now,
        lastActivity: now,
        warningShown: false,
      },
    });

    // Configurer l'alarme
    await setupReminderAlarm();

    return { isNewSession: true, minutes: 0 };
  } else {
    // Continuer la session existante
    await chrome.storage.local.set({
      state: {
        ...state,
        lastActivity: now,
      },
    });

    // S'assurer que l'alarme existe
    await setupReminderAlarm();

    const elapsed = Math.floor((now - state.sessionStart) / 60000);
    console.log(`[YouTube Focus] Session continue: ${elapsed} minutes`);

    return { isNewSession: false, minutes: elapsed };
  }
}

/**
 * Marque le warning comme affiché
 */
async function markWarningShown() {
  const data = await chrome.storage.local.get("state");
  const state = data.state || {};
  await chrome.storage.local.set({
    state: {
      ...state,
      warningShown: true,
    },
  });
}

/**
 * Met à jour l'activité
 */
async function updateActivity() {
  const now = Date.now();
  const data = await chrome.storage.local.get("state");
  const state = data.state || {};

  // Vérifier l'inactivité
  if (
    state.lastActivity &&
    now - state.lastActivity > INACTIVITY_RESET * 60 * 1000
  ) {
    // Reset si inactif trop longtemps
    return handlePageLoad();
  }

  await chrome.storage.local.set({
    state: {
      ...state,
      lastActivity: now,
    },
  });
}

/**
 * Configure l'alarme de rappel (toutes les 15 minutes)
 */
async function setupReminderAlarm() {
  // Vérifier si l'alarme existe déjà
  const existingAlarm = await chrome.alarms.get("youtubeReminder");
  if (!existingAlarm) {
    chrome.alarms.create("youtubeReminder", {
      delayInMinutes: REMINDER_INTERVAL,
      periodInMinutes: REMINDER_INTERVAL,
    });
    console.log("[YouTube Focus] Alarme créée pour dans 15 minutes");
  }
}

/**
 * Calcule le temps écoulé depuis le début de la session
 */
async function getElapsedTime() {
  const data = await chrome.storage.local.get("state");
  const state = data.state || {};

  if (!state.sessionStart) return 0;

  const now = Date.now();
  return Math.floor((now - state.sessionStart) / 60000);
}

/**
 * Envoie un rappel à tous les onglets YouTube
 */
async function sendReminderToTabs(minutes) {
  try {
    const tabs = await chrome.tabs.query({
      url: ["*://www.youtube.com/*", "*://youtube.com/*"],
    });

    console.log(`[YouTube Focus] Envoi rappel à ${tabs.length} onglet(s)`);

    for (const tab of tabs) {
      try {
        await chrome.tabs.sendMessage(tab.id, {
          type: "SHOW_REMINDER",
          minutes: minutes,
        });
      } catch (err) {
        console.log(
          `[YouTube Focus] Impossible d'envoyer à l'onglet ${tab.id}:`,
          err.message,
        );
      }
    }
  } catch (error) {
    console.error("[YouTube Focus] Erreur envoi message:", error);
  }
}

// --- Écouteurs d'événements ---

chrome.runtime.onInstalled.addListener(initialize);
chrome.runtime.onStartup.addListener(initialize);

// Alarme de rappel
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === "youtubeReminder") {
    console.log("[YouTube Focus] Alarme déclenchée!");

    const data = await chrome.storage.local.get("state");
    const state = data.state || {};

    // Vérifier l'inactivité
    const now = Date.now();
    if (
      !state.lastActivity ||
      now - state.lastActivity > INACTIVITY_RESET * 60 * 1000
    ) {
      console.log("[YouTube Focus] Inactivité détectée, pas de rappel");
      await resetState();
      return;
    }

    const elapsed = await getElapsedTime();
    console.log(`[YouTube Focus] Rappel: ${elapsed} minutes écoulées`);

    await sendReminderToTabs(elapsed);
  }
});

// Messages du content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("[YouTube Focus] Message reçu:", message.type);

  (async () => {
    try {
      switch (message.type) {
        case "PAGE_LOADED":
          const result = await handlePageLoad();
          console.log("[YouTube Focus] Réponse PAGE_LOADED:", result);
          sendResponse(result);
          break;

        case "WARNING_SHOWN":
          await markWarningShown();
          sendResponse({ success: true });
          break;

        case "USER_ACTIVITY":
          await updateActivity();
          sendResponse({ success: true });
          break;

        case "GET_STATUS":
          const minutes = await getElapsedTime();
          sendResponse({ minutes });
          break;

        default:
          sendResponse({ error: "Unknown message type" });
      }
    } catch (error) {
      console.error("[YouTube Focus] Erreur:", error);
      sendResponse({ error: error.message });
    }
  })();

  return true;
});

// Initialisation
initialize();
