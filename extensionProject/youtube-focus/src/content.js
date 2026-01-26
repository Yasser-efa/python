/**
 * Content Script - YouTube Focus
 * Affiche les modals d'avertissement et de rappel
 */

let modalContainer = null;
let activityThrottle = null;

/**
 * Crée le conteneur pour les modals
 */
function createModalContainer() {
  if (modalContainer && document.body.contains(modalContainer)) {
    return modalContainer;
  }

  modalContainer = document.createElement('div');
  modalContainer.id = 'youtube-focus-container';
  document.body.appendChild(modalContainer);

  return modalContainer;
}

/**
 * Affiche le modal d'avertissement initial
 */
function showWarningModal() {
  const container = createModalContainer();

  // Ne pas afficher si déjà présent
  if (container.querySelector('#ytf-warning-overlay')) {
    return;
  }

  container.innerHTML = `
    <div class="ytf-overlay" id="ytf-warning-overlay">
      <div class="ytf-modal ytf-warning-modal">
        <div class="ytf-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
        </div>
        <h2 class="ytf-title">Attention !</h2>
        <p class="ytf-message">
          Tu es sur le point de passer du temps sur YouTube.<br><br>
          <strong>Rappelle-toi :</strong> Le temps passe vite ici.<br>
          Fixe-toi une limite et respecte-la !
        </p>
        <div class="ytf-tips">
          <span>Tu recevras un rappel toutes les 15 minutes</span>
        </div>
        <button class="ytf-button ytf-button-primary" id="ytf-acknowledge">
          J'ai compris, je fais attention
        </button>
      </div>
    </div>
  `;

  const button = container.querySelector('#ytf-acknowledge');
  button.addEventListener('click', () => {
    const overlay = container.querySelector('#ytf-warning-overlay');
    overlay.classList.add('ytf-fade-out');

    // Notifier le background
    chrome.runtime.sendMessage({ type: 'WARNING_SHOWN' }).catch(() => {});

    setTimeout(() => {
      overlay.remove();
    }, 300);
  });

  console.log('[YouTube Focus] Warning modal affiché');
}

/**
 * Affiche le modal de rappel périodique
 */
function showReminderModal(minutes) {
  const container = createModalContainer();

  // Supprimer un ancien reminder s'il existe
  const existingReminder = container.querySelector('#ytf-reminder-overlay');
  if (existingReminder) {
    existingReminder.remove();
  }

  const reminderHtml = `
    <div class="ytf-overlay ytf-reminder-overlay" id="ytf-reminder-overlay">
      <div class="ytf-modal ytf-reminder-modal">
        <div class="ytf-icon ytf-icon-time">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12,6 12,12 16,14"/>
          </svg>
        </div>
        <h2 class="ytf-title">Rappel</h2>
        <div class="ytf-time-display">
          <span class="ytf-time-value">${minutes}</span>
          <span class="ytf-time-label">minutes écoulées</span>
        </div>
        <p class="ytf-message">
          ${getTimeMessage(minutes)}
        </p>
        <div class="ytf-actions">
          <button class="ytf-button ytf-button-secondary" id="ytf-continue">
            Je continue un peu
          </button>
          <button class="ytf-button ytf-button-primary" id="ytf-leave">
            Je quitte YouTube
          </button>
        </div>
      </div>
    </div>
  `;

  container.insertAdjacentHTML('beforeend', reminderHtml);

  // Bouton continuer
  const continueBtn = container.querySelector('#ytf-continue');
  continueBtn.addEventListener('click', () => {
    const overlay = container.querySelector('#ytf-reminder-overlay');
    overlay.classList.add('ytf-fade-out');
    setTimeout(() => {
      overlay.remove();
    }, 300);
  });

  // Bouton quitter
  const leaveBtn = container.querySelector('#ytf-leave');
  leaveBtn.addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
  });

  console.log(`[YouTube Focus] Reminder modal affiché: ${minutes} minutes`);
}

/**
 * Retourne un message adapté au temps passé
 */
function getTimeMessage(minutes) {
  if (minutes < 30) {
    return "Tu as encore le contrôle. Prends une décision consciente.";
  } else if (minutes < 60) {
    return "Ça fait un moment que tu es là. Peut-être temps de faire autre chose ?";
  } else if (minutes < 120) {
    return "Plus d'une heure sur YouTube... Est-ce vraiment ce que tu voulais faire ?";
  } else {
    return "Tu es sur YouTube depuis longtemps. Pense à prendre soin de toi !";
  }
}

/**
 * Enregistre l'activité utilisateur (throttled)
 */
function registerActivity() {
  if (activityThrottle) return;

  activityThrottle = setTimeout(() => {
    activityThrottle = null;
  }, 10000); // Throttle de 10 secondes

  chrome.runtime.sendMessage({ type: 'USER_ACTIVITY' }).catch(() => {});
}

/**
 * Initialisation
 */
function init() {
  console.log('[YouTube Focus] Content script chargé sur', window.location.href);

  // Créer le conteneur
  createModalContainer();

  // Notifier le background
  chrome.runtime.sendMessage({ type: 'PAGE_LOADED' }, (response) => {
    if (chrome.runtime.lastError) {
      console.error('[YouTube Focus] Erreur:', chrome.runtime.lastError.message);
      // En cas d'erreur, afficher quand même le warning
      showWarningModal();
      return;
    }

    console.log('[YouTube Focus] Réponse du background:', response);

    if (response && response.isNewSession) {
      showWarningModal();
    }
  });

  // Écouter les messages du background
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('[YouTube Focus] Message reçu dans content:', message);

    if (message.type === 'SHOW_REMINDER') {
      showReminderModal(message.minutes);
      sendResponse({ success: true });
    }
    return true;
  });

  // Enregistrer l'activité utilisateur
  const activityEvents = ['mousemove', 'keydown', 'scroll', 'click', 'touchstart'];
  activityEvents.forEach(event => {
    document.addEventListener(event, registerActivity, { passive: true });
  });

  // Gérer la visibilité de la page
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      chrome.runtime.sendMessage({ type: 'USER_ACTIVITY' }).catch(() => {});
    }
  });
}

// Lancer l'initialisation
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
