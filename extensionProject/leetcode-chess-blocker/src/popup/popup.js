/**
 * Popup Script - LeetCode Chess Unlocker
 * Affiche le statut et les crédits disponibles
 */

const statusCard = document.getElementById("statusCard");
const statusIcon = document.getElementById("statusIcon");
const statusLabel = document.getElementById("statusLabel");
const statusDetail = document.getElementById("statusDetail");
const creditsCount = document.getElementById("creditsCount");
const creditPlural = document.getElementById("creditPlural");
const creditPlural2 = document.getElementById("creditPlural2");
const totalSolved = document.getElementById("totalSolved");
const totalGames = document.getElementById("totalGames");
const optionsLink = document.getElementById("optionsLink");

/**
 * Met à jour l'interface avec le statut actuel
 */
async function updateUI() {
  try {
    const response = await chrome.runtime.sendMessage({ type: "GET_STATUS" });

    if (response) {
      const credits = response.credits || 0;
      const solved = response.totalSolved || 0;
      const games = response.totalGames || 0;
      const settings = response.settings || {};

      // Mise à jour des crédits
      creditsCount.textContent = credits;
      creditPlural.style.display = credits === 1 ? "none" : "inline";
      creditPlural2.style.display = credits === 1 ? "none" : "inline";

      // Mise à jour des stats
      totalSolved.textContent = solved;
      totalGames.textContent = games;

      // Vérifier le mode weekend
      const today = new Date();
      const isWeekend = today.getDay() === 0 || today.getDay() === 6;

      // Mise à jour du statut
      statusCard.classList.remove("blocked", "unlocked", "weekend");

      if (settings.weekendMode && isWeekend) {
        statusCard.classList.add("weekend");
        statusIcon.textContent = "🏖️";
        statusLabel.textContent = "Mode weekend";
        statusDetail.textContent = "Pas de restriction aujourd'hui";
      } else if (credits > 0) {
        statusCard.classList.add("unlocked");
        statusIcon.textContent = "✅";
        statusLabel.textContent = "Accès autorisé";
        statusDetail.textContent = `Tu peux jouer ${credits} partie${credits > 1 ? "s" : ""}`;
      } else {
        statusCard.classList.add("blocked");
        statusIcon.textContent = "🔒";
        statusLabel.textContent = "Bloqué";
        statusDetail.textContent = "Résous un problème LeetCode";
      }
    }
  } catch (error) {
    console.error("Erreur:", error);
    statusIcon.textContent = "⚠️";
    statusLabel.textContent = "Erreur";
    statusDetail.textContent = "Impossible de charger le statut";
  }
}

/**
 * Ouvre la page des options
 */
function openOptions(e) {
  e.preventDefault();
  chrome.runtime.openOptionsPage();
}

// Événements
optionsLink.addEventListener("click", openOptions);

// Initialisation
updateUI();
