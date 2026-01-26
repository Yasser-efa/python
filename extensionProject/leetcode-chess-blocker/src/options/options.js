/**
 * Options Script - LeetCode Chess Unlocker
 * Gestion des paramètres de l'extension
 */

// Éléments du DOM
const requiredCountInput = document.getElementById('requiredCount');
const minDifficultySelect = document.getElementById('minDifficulty');
const blockChessCheckbox = document.getElementById('blockChess');
const blockLichessCheckbox = document.getElementById('blockLichess');
const resetHourSelect = document.getElementById('resetHour');
const weekendModeCheckbox = document.getElementById('weekendMode');
const saveBtn = document.getElementById('saveBtn');
const resetBtn = document.getElementById('resetBtn');
const saveStatus = document.getElementById('saveStatus');

// Configuration par défaut
const DEFAULT_SETTINGS = {
  requiredCount: 1,
  minDifficulty: 'easy',
  blockedSites: ['chess.com', 'lichess.org'],
  resetHour: 0,
  weekendMode: false
};

/**
 * Charge les paramètres depuis le stockage
 */
async function loadSettings() {
  try {
    const data = await chrome.storage.local.get(['settings']);
    const settings = data.settings || DEFAULT_SETTINGS;

    // Appliquer les valeurs aux inputs
    requiredCountInput.value = settings.requiredCount || 1;
    minDifficultySelect.value = settings.minDifficulty || 'easy';
    blockChessCheckbox.checked = settings.blockedSites?.includes('chess.com') ?? true;
    blockLichessCheckbox.checked = settings.blockedSites?.includes('lichess.org') ?? true;
    resetHourSelect.value = settings.resetHour || 0;
    weekendModeCheckbox.checked = settings.weekendMode || false;

  } catch (error) {
    console.error('Erreur chargement paramètres:', error);
    showStatus('Erreur de chargement', 'error');
  }
}

/**
 * Sauvegarde les paramètres
 */
async function saveSettings() {
  try {
    // Construire la liste des sites bloqués
    const blockedSites = [];
    if (blockChessCheckbox.checked) blockedSites.push('chess.com');
    if (blockLichessCheckbox.checked) blockedSites.push('lichess.org');

    // Construire l'objet settings
    const settings = {
      requiredCount: parseInt(requiredCountInput.value) || 1,
      minDifficulty: minDifficultySelect.value,
      blockedSites: blockedSites,
      resetHour: parseInt(resetHourSelect.value) || 0,
      weekendMode: weekendModeCheckbox.checked
    };

    // Validation
    if (settings.requiredCount < 1) settings.requiredCount = 1;
    if (settings.requiredCount > 10) settings.requiredCount = 10;

    // Envoyer au service worker
    const response = await chrome.runtime.sendMessage({
      type: 'UPDATE_SETTINGS',
      settings: settings
    });

    if (response?.success) {
      showStatus('✓ Paramètres sauvegardés', 'success');
    } else {
      showStatus('Erreur de sauvegarde', 'error');
    }

  } catch (error) {
    console.error('Erreur sauvegarde:', error);
    showStatus('Erreur de sauvegarde', 'error');
  }
}

/**
 * Réinitialise les paramètres par défaut
 */
async function resetSettings() {
  if (!confirm('Réinitialiser tous les paramètres par défaut?')) {
    return;
  }

  try {
    const response = await chrome.runtime.sendMessage({
      type: 'UPDATE_SETTINGS',
      settings: DEFAULT_SETTINGS
    });

    if (response?.success) {
      await loadSettings();
      showStatus('✓ Paramètres réinitialisés', 'success');
    } else {
      showStatus('Erreur de réinitialisation', 'error');
    }

  } catch (error) {
    console.error('Erreur reset:', error);
    showStatus('Erreur de réinitialisation', 'error');
  }
}

/**
 * Affiche un message de statut
 */
function showStatus(message, type) {
  saveStatus.textContent = message;
  saveStatus.className = `save-status ${type}`;

  // Effacer après 3 secondes
  setTimeout(() => {
    saveStatus.textContent = '';
    saveStatus.className = 'save-status';
  }, 3000);
}

// Événements
saveBtn.addEventListener('click', saveSettings);
resetBtn.addEventListener('click', resetSettings);

// Sauvegarder automatiquement quand on modifie un champ
[requiredCountInput, minDifficultySelect, blockChessCheckbox,
 blockLichessCheckbox, resetHourSelect, weekendModeCheckbox].forEach(el => {
  el.addEventListener('change', () => {
    // Indicateur visuel de modification
    saveBtn.style.animation = 'pulse 0.5s ease';
    setTimeout(() => saveBtn.style.animation = '', 500);
  });
});

// Initialisation
loadSettings();
