/**
 * Script de la page bloquée
 * Affiche le statut des crédits
 */

const creditsCountEl = document.getElementById("creditsCount");
const refreshBtn = document.getElementById("refreshBtn");

/**
 * Met à jour l'affichage du statut
 */
async function updateStatus() {
  try {
    const response = await chrome.runtime.sendMessage({ type: "GET_STATUS" });

    if (response) {
      const credits = response.credits || 0;
      creditsCountEl.textContent = credits;

      if (credits > 0) {
        // Rediriger automatiquement si des crédits sont disponibles
        setTimeout(() => {
          window.history.back();
        }, 1000);
      }
    }
  } catch (error) {
    console.error("Erreur lors de la récupération du statut:", error);
  }
}

/**
 * Vérifie manuellement le statut
 */
async function manualCheck() {
  refreshBtn.classList.add("loading");
  refreshBtn.textContent = "⏳ Vérification";

  try {
    await updateStatus();
  } catch (error) {
    console.error("Erreur:", error);
  } finally {
    refreshBtn.classList.remove("loading");
    refreshBtn.textContent = "🔄 Vérifier mon statut";
  }
}

// Événements
refreshBtn.addEventListener("click", manualCheck);

// Initialisation
updateStatus();
