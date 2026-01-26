/**
 * Content Script - Détection des parties de chess
 * Fonctionne sur chess.com et lichess.org
 */

console.log("[LeetCode Unlocker] Script chess chargé sur:", window.location.href);

let gameDetected = false;
let currentGameId = null;

/**
 * Extrait l'ID de la partie depuis l'URL
 */
function getGameId() {
  const url = window.location.href;

  // Chess.com: /game/live/12345 ou /play/game/12345
  const chessComMatch = url.match(/\/(?:game\/live|play\/game|game\/daily)\/(\d+)/);
  if (chessComMatch) return "chess_" + chessComMatch[1];

  // Lichess: /abcd1234
  const lichessMatch = url.match(/lichess\.org\/([a-zA-Z0-9]{8,12})/);
  if (lichessMatch) return "lichess_" + lichessMatch[1];

  return null;
}

/**
 * Détecte la fin d'une partie sur Chess.com
 */
function detectChessComGameEnd() {
  // Chercher spécifiquement le modal de fin de partie avec le message de victoire/défaite
  // Chess.com affiche un modal avec "You won", "You lost", etc.

  // Méthode 1: Modal de game-over visible avec texte de résultat
  const modal = document.querySelector('[class*="game-over-modal"], [class*="modal-game-over"], [data-cy*="game-over"]');
  if (modal && modal.offsetParent !== null) {
    const text = modal.textContent.toLowerCase();
    // Doit contenir un indicateur clair de fin de partie
    if (
      text.includes("you won") ||
      text.includes("you lost") ||
      text.includes("draw") ||
      text.includes("checkmate") ||
      text.includes("resigned") ||
      text.includes("timeout") ||
      text.includes("tu as gagné") ||
      text.includes("tu as perdu") ||
      text.includes("victoire") ||
      text.includes("défaite")
    ) {
      console.log("[LeetCode Unlocker] Modal de fin détecté:", text.substring(0, 80));
      return true;
    }
  }

  // Méthode 2: Le header du modal qui affiche explicitement le résultat
  const resultHeader = document.querySelector('[class*="game-over-header"], [class*="header-title-component"]');
  if (resultHeader && resultHeader.offsetParent !== null) {
    const text = resultHeader.textContent.toLowerCase();
    if (
      text.includes("won") ||
      text.includes("lost") ||
      text.includes("draw") ||
      text.includes("gagné") ||
      text.includes("perdu")
    ) {
      console.log("[LeetCode Unlocker] Header de résultat détecté:", text);
      return true;
    }
  }

  return false;
}

/**
 * Détecte la fin d'une partie sur Lichess
 */
function detectLichessGameEnd() {
  // Méthode 1: Classe result-wrap visible (apparaît uniquement à la fin)
  const resultWrap = document.querySelector(".result-wrap");
  if (resultWrap && resultWrap.offsetParent !== null) {
    // Vérifier que le contenu indique bien une fin de partie
    const text = resultWrap.textContent.toLowerCase();
    if (text.length > 0) {
      console.log("[LeetCode Unlocker] Lichess result-wrap trouvé:", text);
      return true;
    }
  }

  // Méthode 2: Status de fin explicite dans la zone de contrôle
  const status = document.querySelector(".rcontrols .status");
  if (status && status.offsetParent !== null) {
    const text = status.textContent.toLowerCase();
    if (
      text.includes("checkmate") ||
      text.includes("time out") ||
      text.includes("resign") ||
      text.includes("draw") ||
      text.includes("stalemate") ||
      text.includes("mat") ||
      text.includes("abandon") ||
      text.includes("nulle") ||
      text.includes("white wins") ||
      text.includes("black wins") ||
      text.includes("les blancs gagnent") ||
      text.includes("les noirs gagnent")
    ) {
      console.log("[LeetCode Unlocker] Lichess status trouvé:", text);
      return true;
    }
  }

  return false;
}

/**
 * Détecte si une partie est terminée
 */
function isGameOver() {
  const url = window.location.href;

  if (url.includes("chess.com")) {
    return detectChessComGameEnd();
  } else if (url.includes("lichess.org")) {
    return detectLichessGameEnd();
  }
  return false;
}

/**
 * Gère la fin d'une partie
 */
async function handleGameEnd() {
  const gameId = getGameId() || window.location.href;

  // Éviter de compter la même partie plusieurs fois
  if (gameDetected && currentGameId === gameId) {
    return;
  }

  gameDetected = true;
  currentGameId = gameId;

  console.log("[LeetCode Unlocker] 🎮 Partie terminée détectée! ID:", gameId);

  // Envoyer le message au background
  try {
    const response = await chrome.runtime.sendMessage({ type: "GAME_PLAYED" });
    console.log("[LeetCode Unlocker] Réponse du background:", response);

    if (response && response.success) {
      if (response.credits > 0) {
        showNotification(
          `Partie comptée! Il te reste ${response.credits} crédit${response.credits !== 1 ? "s" : ""}.`,
          "success"
        );
      } else {
        // Plus de crédits - rediriger vers la page de blocage
        showNotification("Plus de crédits! Redirection...", "warning");
        setTimeout(() => {
          window.location.href = chrome.runtime.getURL("src/blocked/blocked.html");
        }, 2000);
      }
    } else if (response && response.reason === "no_credits") {
      showNotification("Plus de crédits! Résous un problème LeetCode.", "error");
    }
  } catch (error) {
    console.error("[LeetCode Unlocker] Erreur:", error);
  }

  // Reset après 60 secondes pour permettre une nouvelle partie
  setTimeout(() => {
    console.log("[LeetCode Unlocker] Reset - prêt pour une nouvelle partie");
    gameDetected = false;
    currentGameId = null;
  }, 60000);
}

/**
 * Affiche une notification sur la page
 */
function showNotification(message, type = "info") {
  const existing = document.getElementById("leetcode-unlocker-notification");
  if (existing) existing.remove();

  const colors = {
    success: "#22C55E",
    warning: "#F59E0B",
    error: "#EF4444",
    info: "#3B82F6",
  };

  const notification = document.createElement("div");
  notification.id = "leetcode-unlocker-notification";
  notification.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 16px 24px;
      background: ${colors[type] || colors.info};
      color: white;
      border-radius: 12px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 10px 40px rgba(0,0,0,0.3);
      z-index: 2147483647;
      animation: lcuSlideIn 0.3s ease-out;
    ">
      <style>
        @keyframes lcuSlideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      </style>
      ♟️ ${message}
    </div>
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    const notif = document.getElementById("leetcode-unlocker-notification");
    if (notif) notif.remove();
  }, 5000);
}

/**
 * Vérifie périodiquement si la partie est terminée
 */
function startGameWatcher() {
  console.log("[LeetCode Unlocker] Démarrage surveillance...");

  // Vérifier toutes les 2 secondes
  setInterval(() => {
    if (!gameDetected && isGameOver()) {
      handleGameEnd();
    }
  }, 2000);

  // Observer aussi les changements DOM
  const observer = new MutationObserver(() => {
    if (!gameDetected && isGameOver()) {
      handleGameEnd();
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
}

/**
 * Initialisation
 */
function init() {
  console.log("[LeetCode Unlocker] Initialisation sur", window.location.host);

  // Démarrer immédiatement
  startGameWatcher();

  // Écouter les changements d'URL (SPA)
  let lastUrl = window.location.href;
  setInterval(() => {
    if (window.location.href !== lastUrl) {
      console.log("[LeetCode Unlocker] Navigation détectée:", window.location.href);
      lastUrl = window.location.href;
      gameDetected = false;
      currentGameId = null;
    }
  }, 1000);
}

// Démarrer
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
