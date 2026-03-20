/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   VC PITCH GENERATOR — App logic
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

const API_BASE = 'http://localhost:8000';

/* ── Fallback examples (used if API is unavailable) ── */
const FALLBACK_EXAMPLES = [
  'Food delivery app for college students',
  'Uber for dog walking',
  'LinkedIn for plants',
  'Blockchain-based note-taking app',
  'AI alarm clock that judges your sleep schedule',
  'Dating app for leftover pizza slices',
  'NFT-based email service',
  'Web3 social network for houseplants',
  'AI-powered sock matching service',
  'Metaverse gym for lazy people',
  'ChatGPT but for grocery lists',
  'Tinder but for finding roommates',
  'Duolingo but for learning to code',
  'Discord but for plants',
  'Airbnb but for pet sitting',
];

/* ── Loading stages with emojis ── */
const LOADING_STAGES = [
  { emoji: '🚀', text: 'Initializing pitch engine...' },
  { emoji: '🧠', text: 'Generating buzzwords...' },
  { emoji: '🔮', text: 'Consulting the VC oracle...' },
  { emoji: '⚡', text: 'Synthesizing blockchain vibes...' },
  { emoji: '💥', text: 'Disrupting the industry...' },
  { emoji: '🤖', text: 'Adding AI to everything...' },
  { emoji: '📊', text: 'Running TAM/SAM/SOM analysis...' },
  { emoji: '✨', text: 'Polishing the pitch deck...' },
];

/* ── DOM refs ── */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const dom = {
  inputView:   $('#input-view'),
  loadingView: $('#loading-view'),
  pitchView:   $('#pitch-view'),

  ideaInput:   $('#idea-input'),
  charCounter: $('#char-counter'),
  charCurrent: $('#char-current'),
  generateBtn: $('#generate-btn'),
  surpriseBtn: $('#surprise-btn'),
  examplesGrid:$('#examples-grid'),

  loadingEmoji:     $('#loading-emoji'),
  loadingStages:    $('#loading-stages'),
  loadingCounter:   $('#loading-stage-counter'),

  backBtn:     $('#back-btn'),
  toggleAllBtn:$('#toggle-all-btn'),
  copyAllBtn:  $('#copy-all-btn'),
  downloadBtn: $('#download-pdf-btn'),
  shareBtn:    $('#share-btn'),
  pitchIdea:   $('#pitch-idea-display'),
  pitchHero:   $('#pitch-hero'),
  startupName: $('#startup-name'),
  startupTagline: $('#startup-tagline'),
  cardsContainer: $('#cards-container'),
  toastContainer: $('#toast-container'),
};

/* ── State ── */
let examples = [];
let pitchData = null;   // { input_idea, sections: [] }
let loadingInterval = null;
let currentStage = 0;

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   INIT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
document.addEventListener('DOMContentLoaded', () => {
  bindEvents();
  fetchExamples();
});

function bindEvents() {
  dom.ideaInput.addEventListener('input', onInputChange);
  dom.generateBtn.addEventListener('click', onGenerate);
  dom.surpriseBtn.addEventListener('click', onSurprise);
  dom.backBtn.addEventListener('click', showInputView);
  dom.toggleAllBtn.addEventListener('click', toggleAllCards);
  dom.copyAllBtn.addEventListener('click', copyAll);
  dom.downloadBtn.addEventListener('click', downloadPDF);
  dom.shareBtn.addEventListener('click', sharePitch);
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   VIEW MANAGEMENT
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function showView(viewId) {
  [dom.inputView, dom.loadingView, dom.pitchView].forEach((v) => v.classList.remove('active'));
  const target = document.getElementById(viewId);
  // Force reflow for animation restart
  void target.offsetWidth;
  target.classList.add('active');
}

function showInputView() {
  showView('input-view');
  stopLoadingMessages();
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   INPUT LOGIC
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function onInputChange() {
  const len = dom.ideaInput.value.length;
  dom.charCurrent.textContent = len;
  dom.charCounter.className = 'char-counter' + (len >= 200 ? ' limit' : len >= 180 ? ' warn' : '');
  dom.generateBtn.disabled = len < 10;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   EXAMPLES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
async function fetchExamples() {
  try {
    const res = await fetch(`${API_BASE}/api/examples`);
    const data = await res.json();
    if (data.success && Array.isArray(data.examples)) {
      examples = data.examples;
    } else {
      examples = FALLBACK_EXAMPLES;
    }
  } catch {
    examples = FALLBACK_EXAMPLES;
  }
  renderExamples();
}

function renderExamples() {
  dom.examplesGrid.innerHTML = '';
  examples.forEach((text, i) => {
    const card = document.createElement('div');
    card.className = 'example-card';
    card.style.animationDelay = `${.45 + i * .04}s`;
    card.innerHTML = `<span>${text}</span>`;
    card.addEventListener('click', () => selectExample(text, card));
    dom.examplesGrid.appendChild(card);
  });
}

function selectExample(text, card) {
  $$('.example-card').forEach((c) => c.classList.remove('selected'));
  card.classList.add('selected');
  dom.ideaInput.value = text;
  dom.ideaInput.focus();
  onInputChange();
}

function onSurprise() {
  const pick = examples[Math.floor(Math.random() * examples.length)];
  dom.ideaInput.value = pick;
  onInputChange();
  // Visually select the matching card
  $$('.example-card').forEach((c) => {
    c.classList.toggle('selected', c.textContent.trim() === pick);
  });
  toast('🎲 Random idea loaded!');
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   GENERATE PITCH
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
async function onGenerate() {
  const idea = dom.ideaInput.value.trim();
  if (idea.length < 10) return;

  // Show loading
  showView('loading-view');
  startLoadingMessages();

  try {
    const res = await fetch(`${API_BASE}/api/generate-pitch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idea }),
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || errData.error || `Server error (${res.status})`);
    }

    const data = await res.json();
    if (!data.success || !data.pitch) throw new Error('Invalid response from server');

    pitchData = data.pitch;

    // Complete all remaining stages quickly
    await completeLoadingStages();

    stopLoadingMessages();
    renderPitch();
    showView('pitch-view');
  } catch (err) {
    stopLoadingMessages();
    showView('input-view');
    toast(`❌ ${err.message}`, 'error');
  }
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   LOADING STAGES (Dramatic stacked animation)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function startLoadingMessages() {
  currentStage = 0;
  dom.loadingStages.innerHTML = '';
  dom.loadingEmoji.textContent = LOADING_STAGES[0].emoji;

  // Update progress bar fill to 0
  const fill = dom.loadingView.querySelector('.progress-bar-fill');
  fill.style.width = '0%';

  // Add first stage as active
  addStageElement(0, 'active');

  // Advance stages at intervals
  loadingInterval = setInterval(() => {
    if (currentStage >= LOADING_STAGES.length - 1) {
      // Stay on last stage, don't loop
      return;
    }

    // Mark current stage as done
    markStageDone(currentStage);

    // Advance
    currentStage++;

    // Update emoji
    dom.loadingEmoji.textContent = LOADING_STAGES[currentStage].emoji;

    // Update counter
    dom.loadingCounter.textContent = `Stage ${currentStage + 1} of ${LOADING_STAGES.length}`;

    // Update progress bar
    const progress = ((currentStage + 1) / LOADING_STAGES.length) * 100;
    fill.style.width = `${progress}%`;

    // Add new stage line
    addStageElement(currentStage, 'active');
  }, 1200);
}

function addStageElement(index, className) {
  const stage = LOADING_STAGES[index];
  const el = document.createElement('div');
  el.className = `loading-stage-line ${className}`;
  el.dataset.stageIndex = index;
  el.style.animationDelay = `${index * 0.05}s`;
  el.innerHTML = `
    <span class="stage-icon"><span class="stage-spinner"></span></span>
    <span>${stage.text}</span>
  `;
  dom.loadingStages.appendChild(el);
}

function markStageDone(index) {
  const el = dom.loadingStages.querySelector(`[data-stage-index="${index}"]`);
  if (el) {
    el.classList.remove('active');
    el.classList.add('done');
    el.querySelector('.stage-icon').innerHTML = '✓';
  }
}

async function completeLoadingStages() {
  // Rapidly mark all remaining stages as done
  const fill = dom.loadingView.querySelector('.progress-bar-fill');

  for (let i = currentStage; i < LOADING_STAGES.length; i++) {
    // If stage element doesn't exist, add it
    if (!dom.loadingStages.querySelector(`[data-stage-index="${i}"]`)) {
      addStageElement(i, 'active');
    }

    await sleep(120);
    markStageDone(i);
    dom.loadingEmoji.textContent = LOADING_STAGES[Math.min(i + 1, LOADING_STAGES.length - 1)].emoji;
    dom.loadingCounter.textContent = `Stage ${i + 1} of ${LOADING_STAGES.length}`;
    fill.style.width = `${((i + 1) / LOADING_STAGES.length) * 100}%`;
  }

  // Final moment
  dom.loadingEmoji.textContent = '🎉';
  dom.loadingCounter.textContent = 'Complete!';
  fill.style.width = '100%';
  await sleep(400);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function stopLoadingMessages() {
  clearInterval(loadingInterval);
  loadingInterval = null;
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RENDER PITCH
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function renderPitch() {
  dom.pitchIdea.textContent = `"${pitchData.input_idea}"`;
  dom.cardsContainer.innerHTML = '';
  dom.toggleAllBtn.dataset.state = 'collapsed';
  dom.toggleAllBtn.textContent = 'Expand All';

  // Parse Section 1 for hero display
  const section1 = pitchData.sections.find((s) => s.id === 1);
  if (section1) {
    renderPitchHero(section1);
  }

  pitchData.sections.forEach((section, i) => {
    // Skip section 1 — it's now the hero card
    if (section.id === 1) return;

    const isReality = section.id === 11;
    const card = document.createElement('div');
    card.className = `pitch-card${isReality ? ' reality-check' : ''}`;
    card.style.animationDelay = `${i * .06}s`;
    card.dataset.sectionId = section.id;

    card.innerHTML = `
      <div class="card-header" role="button" tabindex="0" aria-expanded="${isReality}">
        <div class="card-emoji">${section.emoji}</div>
        <div class="card-title">${section.title}</div>
        <svg class="card-chevron" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
        </svg>
      </div>
      <div class="card-body">
        <div class="card-content">${escapeHtml(section.content)}</div>
        <div class="card-actions">
          <button class="copy-section-btn" data-id="${section.id}">📋 Copy</button>
        </div>
      </div>
    `;

    // Expand reality check by default
    if (isReality) {
      card.classList.add('expanded');
      requestAnimationFrame(() => {
        const body = card.querySelector('.card-body');
        body.style.maxHeight = body.scrollHeight + 'px';
      });
    }

    // Toggle expand/collapse
    const header = card.querySelector('.card-header');
    header.addEventListener('click', () => toggleCard(card));
    header.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleCard(card); }
    });

    // Copy section
    card.querySelector('.copy-section-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      copySection(section, e.currentTarget);
    });

    dom.cardsContainer.appendChild(card);
  });

  // After render, auto-expand reality check with scroll
  setTimeout(() => {
    const rc = dom.cardsContainer.querySelector('.reality-check');
    if (rc) rc.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 600);
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   PITCH HERO — Startup Name & Tagline
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function renderPitchHero(section) {
  const content = section.content.trim();

  // Try to extract name and tagline
  // Common patterns from the LLM:
  // "StartupName - \"tagline here\""
  // "StartupName\nTagline here"
  // "StartupName — Tagline here"

  let name = '';
  let tagline = '';

  // Pattern 1: Name - "tagline" or Name — "tagline"
  const dashQuoteMatch = content.match(/^(.+?)\s*[-–—]\s*[""](.+?)[""]\s*$/s);
  if (dashQuoteMatch) {
    name = dashQuoteMatch[1].trim();
    tagline = dashQuoteMatch[2].trim();
  } else {
    // Pattern 2: Name\nTagline (multiline)
    const lines = content.split('\n').filter((l) => l.trim());
    if (lines.length >= 2) {
      name = lines[0].replace(/^[-–—•*]\s*/, '').trim();
      tagline = lines.slice(1).join(' ').replace(/^[-–—•*]\s*/, '').replace(/^[""]|[""]$/g, '').trim();
    } else {
      // Pattern 3: Single line with dash
      const dashMatch = content.match(/^(.+?)\s*[-–—]\s*(.+)$/);
      if (dashMatch) {
        name = dashMatch[1].trim();
        tagline = dashMatch[2].replace(/^[""]|[""]$/g, '').trim();
      } else {
        name = content;
        tagline = '';
      }
    }
  }

  // Clean up any remaining quotes around name
  name = name.replace(/^[""]|[""]$/g, '');

  dom.startupName.textContent = name;
  dom.startupTagline.textContent = tagline ? `"${tagline}"` : '';
  dom.pitchHero.style.display = 'block';
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   CARD EXPAND / COLLAPSE
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function toggleCard(card) {
  const body = card.querySelector('.card-body');
  const isExpanded = card.classList.contains('expanded');

  if (isExpanded) {
    // Collapse
    body.style.maxHeight = body.scrollHeight + 'px';
    void body.offsetHeight; // force reflow
    body.style.maxHeight = '0';
    card.classList.remove('expanded');
    card.querySelector('.card-header').setAttribute('aria-expanded', 'false');
  } else {
    // Expand
    card.classList.add('expanded');
    body.style.maxHeight = body.scrollHeight + 'px';
    card.querySelector('.card-header').setAttribute('aria-expanded', 'true');
    // Smooth scroll into view
    setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 200);
    // After transition, remove max-height so content can reflow
    body.addEventListener('transitionend', function handler() {
      if (card.classList.contains('expanded')) body.style.maxHeight = 'none';
      body.removeEventListener('transitionend', handler);
    });
  }
}

function toggleAllCards() {
  const cards = $$('.pitch-card');
  const expanding = dom.toggleAllBtn.dataset.state === 'collapsed';

  cards.forEach((card, i) => {
    setTimeout(() => {
      const isExpanded = card.classList.contains('expanded');
      if (expanding && !isExpanded) toggleCard(card);
      if (!expanding && isExpanded) toggleCard(card);
    }, i * 50);
  });

  dom.toggleAllBtn.dataset.state = expanding ? 'expanded' : 'collapsed';
  dom.toggleAllBtn.textContent = expanding ? 'Collapse All' : 'Expand All';
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   COPY / SHARE / PDF
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function copySection(section, btn) {
  const text = `${section.emoji} ${section.title}\n${section.content}`;
  navigator.clipboard.writeText(text).then(() => {
    btn.classList.add('copied');
    btn.textContent = '✅ Copied!';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.textContent = '📋 Copy';
    }, 1500);
    toast('Section copied!', 'success');
  });
}

function copyAll() {
  if (!pitchData) return;
  const text = pitchData.sections
    .map((s) => `${s.emoji} ${s.title}\n${'─'.repeat(30)}\n${s.content}`)
    .join('\n\n');
  const full = `🎯 VC PITCH: "${pitchData.input_idea}"\n${'═'.repeat(40)}\n\n${text}`;
  navigator.clipboard.writeText(full).then(() => toast('All sections copied!', 'success'));
}

function downloadPDF() {
  if (!pitchData || typeof html2pdf === 'undefined') {
    toast('PDF export not available', 'error');
    return;
  }

  // Build a clean renderable element
  const el = document.createElement('div');
  el.style.cssText = 'padding:32px;font-family:Inter,sans-serif;color:#1F2937;max-width:700px;';
  el.innerHTML = `
    <h1 style="font-size:24px;margin-bottom:4px;">VC Pitch: "${escapeHtml(pitchData.input_idea)}"</h1>
    <p style="color:#6B7280;font-size:13px;margin-bottom:24px;">Generated by VC Pitch Generator</p>
    ${pitchData.sections.map((s) => `
      <div style="margin-bottom:20px;padding:16px;border:1px solid #E5E7EB;border-radius:8px;${s.id === 11 ? 'background:#DC2626;color:#fff;' : ''}">
        <h3 style="font-size:16px;margin-bottom:8px;">${s.emoji} ${s.title}</h3>
        <p style="font-size:14px;line-height:1.7;white-space:pre-wrap;">${escapeHtml(s.content)}</p>
      </div>
    `).join('')}
  `;

  html2pdf()
    .set({
      margin: [10, 10],
      filename: `vc-pitch-${Date.now()}.pdf`,
      image: { type: 'jpeg', quality: .98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    })
    .from(el)
    .save()
    .then(() => toast('PDF downloaded!', 'success'));
}

function sharePitch() {
  if (!pitchData) return;
  const text = `🚀 Check out this VC pitch for "${pitchData.input_idea}"!\n\nGenerated by VC Pitch Generator`;
  if (navigator.share) {
    navigator.share({ title: 'VC Pitch Generator', text }).catch(() => {});
  } else {
    navigator.clipboard.writeText(text).then(() => toast('Share text copied to clipboard!', 'success'));
  }
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   TOAST
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function toast(message, type = '') {
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = message;
  dom.toastContainer.appendChild(el);
  setTimeout(() => {
    el.classList.add('out');
    el.addEventListener('animationend', () => el.remove());
  }, 2200);
}

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   UTIL
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}
