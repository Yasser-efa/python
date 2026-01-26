/**
 * Content Script LeetCode
 * Détecte les soumissions réussies de problèmes
 */

(function() {
  'use strict';

  console.log('[LeetCode Unlocker] Content script chargé');

  // Éviter les doubles exécutions
  if (window.__leetcodeUnlockerLoaded) return;
  window.__leetcodeUnlockerLoaded = true;

  // Suivre les problèmes déjà comptés dans cette session
  const countedProblems = new Set();

  /**
   * Extrait la difficulté du problème depuis la page
   */
  function getProblemDifficulty() {
    // Chercher l'élément de difficulté
    const difficultySelectors = [
      '[data-degree]',
      '.text-difficulty-easy',
      '.text-difficulty-medium',
      '.text-difficulty-hard',
      '[class*="text-olive"]',  // Easy
      '[class*="text-yellow"]', // Medium
      '[class*="text-pink"]',   // Hard
      '[diff]'
    ];

    for (const selector of difficultySelectors) {
      const el = document.querySelector(selector);
      if (el) {
        const text = el.textContent.toLowerCase();
        if (text.includes('easy') || text.includes('facile')) return 'easy';
        if (text.includes('medium') || text.includes('moyen')) return 'medium';
        if (text.includes('hard') || text.includes('difficile')) return 'hard';

        // Vérifier les attributs
        const degree = el.getAttribute('data-degree') || el.getAttribute('diff');
        if (degree) {
          if (degree === '1' || degree.toLowerCase() === 'easy') return 'easy';
          if (degree === '2' || degree.toLowerCase() === 'medium') return 'medium';
          if (degree === '3' || degree.toLowerCase() === 'hard') return 'hard';
        }
      }
    }

    // Par défaut, considérer comme easy
    return 'easy';
  }

  /**
   * Extrait le slug du problème depuis l'URL
   */
  function getProblemSlug() {
    const match = window.location.pathname.match(/\/problems\/([^/]+)/);
    return match ? match[1] : null;
  }

  /**
   * Notifie le service worker d'un problème résolu
   */
  async function notifySolved(difficulty) {
    const slug = getProblemSlug();

    // Éviter de compter le même problème plusieurs fois
    if (slug && countedProblems.has(slug)) {
      console.log('[LeetCode Unlocker] Problème déjà compté:', slug);
      return;
    }

    try {
      const response = await chrome.runtime.sendMessage({
        type: 'PROBLEM_SOLVED',
        difficulty: difficulty,
        slug: slug
      });

      if (response?.success) {
        console.log('[LeetCode Unlocker] Problème résolu envoyé:', slug, difficulty);
        if (slug) countedProblems.add(slug);
        showSuccessToast();
      }
    } catch (error) {
      console.error('[LeetCode Unlocker] Erreur envoi:', error);
    }
  }

  /**
   * Affiche un toast de succès
   */
  function showSuccessToast() {
    // Supprimer un toast existant
    const existingToast = document.getElementById('leetcode-unlocker-toast');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.id = 'leetcode-unlocker-toast';
    toast.innerHTML = `
      <div style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(34, 197, 94, 0.4);
        z-index: 999999;
        animation: slideIn 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 10px;
      ">
        <span style="font-size: 20px;">♟️</span>
        <span>Chess débloqué! Bravo!</span>
      </div>
      <style>
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(100px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
      </style>
    `;

    document.body.appendChild(toast);

    // Supprimer après 5 secondes
    setTimeout(() => toast.remove(), 5000);
  }

  /**
   * Observe les changements DOM pour détecter "Accepted"
   */
  function setupDOMObserver() {
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        // Chercher les éléments de résultat de soumission
        const resultSelectors = [
          '[data-e2e-locator="submission-result"]',
          '.text-green-s',
          '[class*="success"]',
          '.status-accepted',
          '[data-status="Accepted"]'
        ];

        for (const selector of resultSelectors) {
          const elements = document.querySelectorAll(selector);
          for (const el of elements) {
            const text = el.textContent.toLowerCase();
            if (text.includes('accepted') || text.includes('accepté')) {
              console.log('[LeetCode Unlocker] Détecté via DOM:', text);
              const difficulty = getProblemDifficulty();
              notifySolved(difficulty);
              return;
            }
          }
        }
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    console.log('[LeetCode Unlocker] Observateur DOM configuré');
  }

  /**
   * Intercepte les requêtes fetch pour détecter les soumissions
   */
  function interceptFetch() {
    const originalFetch = window.fetch;

    window.fetch = async function(...args) {
      const response = await originalFetch.apply(this, args);
      const url = args[0]?.url || args[0];

      // Vérifier si c'est une requête de vérification de soumission
      if (typeof url === 'string' && url.includes('/submissions/detail/') && url.includes('/check/')) {
        try {
          const clonedResponse = response.clone();
          const data = await clonedResponse.json();

          if (data.status_msg === 'Accepted' || data.state === 'SUCCESS') {
            console.log('[LeetCode Unlocker] Détecté via fetch:', data);
            const difficulty = getProblemDifficulty();
            notifySolved(difficulty);
          }
        } catch (e) {
          // Ignorer les erreurs de parsing
        }
      }

      return response;
    };

    console.log('[LeetCode Unlocker] Interception fetch configurée');
  }

  /**
   * Intercepte XMLHttpRequest pour la compatibilité
   */
  function interceptXHR() {
    const originalOpen = XMLHttpRequest.prototype.open;
    const originalSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(method, url, ...rest) {
      this._url = url;
      return originalOpen.apply(this, [method, url, ...rest]);
    };

    XMLHttpRequest.prototype.send = function(...args) {
      this.addEventListener('load', function() {
        if (this._url && this._url.includes('/submissions/detail/') && this._url.includes('/check/')) {
          try {
            const data = JSON.parse(this.responseText);
            if (data.status_msg === 'Accepted' || data.state === 'SUCCESS') {
              console.log('[LeetCode Unlocker] Détecté via XHR:', data);
              const difficulty = getProblemDifficulty();
              notifySolved(difficulty);
            }
          } catch (e) {
            // Ignorer les erreurs de parsing
          }
        }
      });
      return originalSend.apply(this, args);
    };

    console.log('[LeetCode Unlocker] Interception XHR configurée');
  }

  // Initialisation
  function init() {
    // Attendre que le DOM soit prêt
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setupDOMObserver();
        interceptFetch();
        interceptXHR();
      });
    } else {
      setupDOMObserver();
      interceptFetch();
      interceptXHR();
    }
  }

  init();
})();
