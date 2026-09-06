/**
 * BanglaBhasha Compiler Live Demo — Frontend Application Logic
 * Supports Day/Night Mode and explicit Run-on-click
 */

// Virtual Bangla Keyboard Chips Configuration
const KEYBOARD_CHIPS = [
  { label: "পূর্ণসংখ্যা", insert: "পূর্ণসংখ্যা ", type: "chip-type" },
  { label: "দশমিক", insert: "দশমিক ", type: "chip-type" },
  { label: "স্ট্রিং", insert: "স্ট্রিং ", type: "chip-type" },
  { label: "বুলিয়ান", insert: "বুলিয়ান ", type: "chip-type" },
  { label: "ধরি", insert: "ধরি ", type: "chip-type" },
  { label: "লেখো", insert: "লেখো()", offset: 5, type: "chip-flow" },
  { label: "যদি", insert: "যদি () {\n    \n}", offset: 4, type: "chip-flow" },
  { label: "নাহলে", insert: "নাহলে {\n    \n}", offset: 11, type: "chip-flow" },
  { label: "যতক্ষণ", insert: "যতক্ষণ () {\n    \n}", offset: 7, type: "chip-flow" },
  { label: "ফাংশন", insert: "ফাংশন নাম() -> পূর্ণসংখ্যা {\n    \n}", offset: 8, type: "chip-flow" },
  { label: "ফেরত", insert: "ফেরত ", type: "chip-flow" },
  { label: "স্ট্যাক", insert: "স্ট্যাক ", type: "chip-ds" },
  { label: "কিউ", insert: "কিউ ", type: "chip-ds" },
  { label: "ঠেলো", insert: ".ঠেলো()", offset: 6, type: "chip-ds" },
  { label: "বের_করো", insert: ".বের_করো()", type: "chip-ds" },
  { label: "ঢোকাও", insert: ".ঢোকাও()", offset: 7, type: "chip-ds" },
  { label: "ক্লাস", insert: "ক্লাস নাম {\n    \n}", offset: 9, type: "chip-flow" },
  { label: "নতুন", insert: "নতুন ", type: "chip-flow" },
  { label: "নিজে", insert: "নিজে", type: "chip-flow" },
  { label: "সত্য", insert: "সত্য", type: "chip-type" },
  { label: "মিথ্যা", insert: "মিথ্যা", type: "chip-type" },
  { label: "এবং", insert: " এবং ", type: "chip-flow" },
  { label: "অথবা", insert: " অথবা ", type: "chip-flow" },
];

let samplePrograms = {};
let currentCompiledData = null;

// DOM Elements
const codeEditor = document.getElementById("codeEditor");
const lineNumbers = document.getElementById("lineNumbers");
const cursorPos = document.getElementById("cursorPos");
const charCount = document.getElementById("charCount");
const exampleSelect = document.getElementById("exampleSelect");
const btnRun = document.getElementById("btnRun");
const btnCompile = document.getElementById("btnCompile");
const btnClear = document.getElementById("btnClear");
const btnReset = document.getElementById("btnReset");
const btnCopyPython = document.getElementById("btnCopyPython");
const btnCheatsheet = document.getElementById("btnCheatsheet");
const btnCloseModal = document.getElementById("btnCloseModal");
const cheatsheetModal = document.getElementById("cheatsheetModal");
const chipsContainer = document.getElementById("chipsContainer");

// Theme Elements
const btnThemeToggle = document.getElementById("btnThemeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeText = document.getElementById("themeText");

// Inspector Elements
const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanes = document.querySelectorAll(".tab-pane");
const errorAlert = document.getElementById("errorAlert");
const errorList = document.getElementById("errorList");
const terminalOutput = document.getElementById("terminalOutput");
const timeBadge = document.getElementById("timeBadge");
const tokensTableBody = document.getElementById("tokensTableBody");
const tokenFilter = document.getElementById("tokenFilter");
const tokenCount = document.getElementById("tokenCount");
const tokenMetaPill = document.getElementById("tokenMetaPill");
const astTreeContainer = document.getElementById("astTreeContainer");
const astTextContainer = document.getElementById("astTextContainer");
const btnAstTreeView = document.getElementById("btnAstTreeView");
const btnAstTextView = document.getElementById("btnAstTextView");
const symbolsTableBody = document.getElementById("symbolsTableBody");
const functionsClassesContainer = document.getElementById("functionsClassesContainer");
const tacContainer = document.getElementById("tacContainer");
const pythonCodeView = document.getElementById("pythonCodeView");

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  renderChips();
  setupEditorEvents();
  setupTabEvents();
  setupModalEvents();
  loadExamples();
});

// ============================================================
// 1. THEME HANDLING (DAY / NIGHT MODE)
// ============================================================
function initTheme() {
  // Default to light mode as requested ("copiler er ui ta ektu light kore deu")
  const savedTheme = localStorage.getItem("bangla_compiler_theme") || "light";
  applyTheme(savedTheme);

  if (btnThemeToggle) {
    btnThemeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
      const newTheme = currentTheme === "light" ? "dark" : "light";
      applyTheme(newTheme);
      localStorage.setItem("bangla_compiler_theme", newTheme);
    });
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  if (theme === "light") {
    if (themeIcon) themeIcon.textContent = "🌙";
    if (themeText) themeText.textContent = "রাত মোড";
    if (btnThemeToggle) btnThemeToggle.title = "ডার্ক / রাত মোডে পরিবর্তন করুন";
  } else {
    if (themeIcon) themeIcon.textContent = "☀️";
    if (themeText) themeText.textContent = "দিন মোড";
    if (btnThemeToggle) btnThemeToggle.title = "লাইট / দিন মোডে পরিবর্তন করুন";
  }
}

// ============================================================
// 2. VIRTUAL BANGLA KEYBOARD CHIPS
// ============================================================
function renderChips() {
  chipsContainer.innerHTML = "";
  KEYBOARD_CHIPS.forEach(chip => {
    const el = document.createElement("button");
    el.className = `chip ${chip.type}`;
    el.textContent = chip.label;
    el.type = "button";
    el.title = `ইনসার্ট করুন: ${chip.label}`;
    el.addEventListener("click", () => {
      insertAtCursor(chip.insert, chip.offset);
    });
    chipsContainer.appendChild(el);
  });
}

function insertAtCursor(text, offset) {
  const start = codeEditor.selectionStart;
  const end = codeEditor.selectionEnd;
  const value = codeEditor.value;

  codeEditor.value = value.substring(0, start) + text + value.substring(end);
  const newPos = offset !== undefined ? start + offset : start + text.length;
  codeEditor.selectionStart = newPos;
  codeEditor.selectionEnd = newPos;
  codeEditor.focus();
  updateEditorStats();
  updateLineNumbers();
}

// ============================================================
// 3. EDITOR LISTENERS & CONTROLS
// ============================================================
function setupEditorEvents() {
  codeEditor.addEventListener("input", () => {
    updateEditorStats();
    updateLineNumbers();
  });

  codeEditor.addEventListener("scroll", () => {
    lineNumbers.scrollTop = codeEditor.scrollTop;
  });

  codeEditor.addEventListener("keyup", updateEditorStats);
  codeEditor.addEventListener("click", updateEditorStats);

  // Tab key handling (insert 4 spaces) & Ctrl+Enter to Run
  codeEditor.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      e.preventDefault();
      insertAtCursor("    ");
    } else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      executeCode(true); // Explicit Run
    }
  });

  // Clear button resets editor and output state (NO AUTO RUN)
  btnClear.addEventListener("click", () => {
    codeEditor.value = "";
    updateEditorStats();
    updateLineNumbers();
    clearOutputState();
    codeEditor.focus();
  });

  // Reset button restores full demo code (NO AUTO RUN)
  btnReset.addEventListener("click", () => {
    if (samplePrograms["full_demo"]) {
      codeEditor.value = samplePrograms["full_demo"].code;
      exampleSelect.value = "full_demo";
      updateEditorStats();
      updateLineNumbers();
      clearOutputState();
    }
  });

  // Explicit Run & Compile buttons
  btnRun.addEventListener("click", () => executeCode(true));
  btnCompile.addEventListener("click", () => executeCode(false));

  btnCopyPython.addEventListener("click", () => {
    const text = pythonCodeView.textContent;
    if (!text || text.startsWith("#")) return;
    navigator.clipboard.writeText(text).then(() => {
      const origText = btnCopyPython.textContent;
      btnCopyPython.textContent = "✅ কপি হয়েছে!";
      setTimeout(() => btnCopyPython.textContent = origText, 2000);
    });
  });

  tokenFilter.addEventListener("input", filterTokens);

  btnAstTreeView.addEventListener("click", () => {
    btnAstTreeView.classList.add("active");
    btnAstTextView.classList.remove("active");
    astTreeContainer.classList.remove("hidden");
    astTextContainer.classList.add("hidden");
  });

  btnAstTextView.addEventListener("click", () => {
    btnAstTextView.classList.add("active");
    btnAstTreeView.classList.remove("active");
    astTextContainer.classList.remove("hidden");
    astTreeContainer.classList.add("hidden");
  });
}

function updateLineNumbers() {
  const lines = codeEditor.value.split("\n").length;
  let numbers = "";
  for (let i = 1; i <= Math.max(lines, 1); i++) {
    numbers += i + "\n";
  }
  lineNumbers.textContent = numbers;
}

function updateEditorStats() {
  const text = codeEditor.value;
  const start = codeEditor.selectionStart;
  const lines = text.substring(0, start).split("\n");
  const line = lines.length;
  const col = lines[lines.length - 1].length + 1;

  cursorPos.textContent = `লাইন ${toBanglaNum(line)}, কলাম ${toBanglaNum(col)}`;
  charCount.textContent = `${toBanglaNum(text.length)} অক্ষর`;
}

function toBanglaNum(num) {
  const bn = ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"];
  return String(num).replace(/[0-9]/g, d => bn[d]);
}

// Clear Output State (Reset terminal and inspector to waiting state)
function clearOutputState() {
  hideErrors();
  timeBadge.classList.add("hidden");
  timeBadge.textContent = "⚡ 0 ms";
  terminalOutput.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">▶</div>
      <div class="empty-text">কোড রান করতে উপরের <strong>'চালাও (Run)'</strong> বাটনে ক্লিক করুন অথবা <strong>Ctrl + Enter</strong> চাপুন।</div>
    </div>
  `;
  tokensTableBody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">কম্পাইল করার পর টোকেনসমূহ এখানে দৃশ্যমান হবে।</td></tr>`;
  tokenCount.textContent = "০";
  tokenMetaPill.textContent = "মোট ০টি টোকেন";
  astTreeContainer.innerHTML = '<div class="empty-state text-muted">সিনট্যাক্স ট্রি দেখতে কোড কম্পাইল বা রান করুন।</div>';
  astTextContainer.textContent = "";
  symbolsTableBody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">কোনো সিম্বল পাওয়া যায়নি।</td></tr>`;
  functionsClassesContainer.innerHTML = `<div class="text-muted text-center p-2">কোনো ফাংশন বা ক্লাস ডিফাইন করা হয়নি।</div>`;
  tacContainer.innerHTML = '<div class="empty-state text-muted">কম্পাইল করার পর থ্রি-অ্যাড্রেস কোড এখানে দেখা যাবে।</div>';
  pythonCodeView.textContent = "# কোড কম্পাইল করার পর জেনারেটেড পাইথন কোড এখানে আসবে";
  switchTab("tab-output");
}

// ============================================================
// 4. TAB & MODAL SWITCHING
// ============================================================
function setupTabEvents() {
  tabButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      switchTab(tabId);
    });
  });
}

function switchTab(tabId) {
  tabButtons.forEach(b => b.classList.toggle("active", b.getAttribute("data-tab") === tabId));
  tabPanes.forEach(p => p.classList.toggle("active", p.id === tabId));
}

function setupModalEvents() {
  btnCheatsheet.addEventListener("click", () => cheatsheetModal.classList.remove("hidden"));
  btnCloseModal.addEventListener("click", () => cheatsheetModal.classList.add("hidden"));
  cheatsheetModal.addEventListener("click", (e) => {
    if (e.target === cheatsheetModal) cheatsheetModal.classList.add("hidden");
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cheatsheetModal.classList.add("hidden");
  });
}

// ============================================================
// 5. EXAMPLES LOADING (NO AUTO-RUN)
// ============================================================
async function loadExamples() {
  try {
    const res = await fetch("/api/examples");
    if (res.ok) {
      samplePrograms = await res.json();

      // Dropdown selection loads code WITHOUT executing automatically
      exampleSelect.addEventListener("change", (e) => {
        const key = e.target.value;
        if (samplePrograms[key]) {
          codeEditor.value = samplePrograms[key].code;
          updateEditorStats();
          updateLineNumbers();
          clearOutputState(); // Clean slate, waits for user to click Run!
        }
      });

      // Initial load: Fill editor but DO NOT execute automatically!
      if (samplePrograms["full_demo"]) {
        codeEditor.value = samplePrograms["full_demo"].code;
        updateEditorStats();
        updateLineNumbers();
        clearOutputState(); // Clean slate, waits for user to click Run!
      }
    }
  } catch (err) {
    console.warn("Could not load examples from server:", err);
  }
}

// ============================================================
// 6. CODE EXECUTION / COMPILATION
// ============================================================
async function executeCode(runExecution = true) {
  const source = codeEditor.value;
  const endpoint = runExecution ? "/api/run" : "/api/compile";

  btnRun.disabled = true;
  btnCompile.disabled = true;
  const originalRunText = btnRun.innerHTML;
  btnRun.innerHTML = runExecution ? "⏳ চলছে..." : "⏳ কম্পাইল হচ্ছে...";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ source })
    });

    const data = await res.json();
    currentCompiledData = data;
    renderCompilerResults(data, runExecution);
  } catch (err) {
    showErrors([`সার্ভার সংযোগ ত্রুটি: ${err.message}`]);
  } finally {
    btnRun.disabled = false;
    btnCompile.disabled = false;
    btnRun.innerHTML = originalRunText;
  }
}

// Render Results to UI
function renderCompilerResults(data, wasExecuted) {
  // 1. Errors
  if (data.errors && data.errors.length > 0) {
    showErrors(data.errors);
  } else {
    hideErrors();
  }

  // 2. Terminal Output
  if (wasExecuted) {
    timeBadge.textContent = `⚡ ${data.elapsed_ms} ms`;
    timeBadge.classList.remove("hidden");
    if (data.output) {
      terminalOutput.textContent = data.output;
    } else if (data.errors && data.errors.length > 0) {
      terminalOutput.textContent = "কম্পাইলেশন ব্যর্থ হয়েছে। উপরের এরর বক্সটি দেখুন।";
    } else {
      terminalOutput.textContent = "(প্রোগ্রামটি সফলভাবে সম্পন্ন হয়েছে, কোনো আউটপুট ছিল না)";
    }
    switchTab("tab-output");
  } else {
    switchTab("tab-tokens");
  }

  // 3. Tokens Tab
  renderTokens(data.tokens || []);

  // 4. AST Tab
  renderAST(data.ast_tree, data.ast_text);

  // 5. Semantic & Symbols Tab
  renderSemantic(data.symbols || [], data.functions || [], data.classes || []);

  // 6. TAC Tab
  renderTAC(data.tac || []);

  // 7. Python Code Tab
  pythonCodeView.textContent = data.python_code || "# কোনো পাইথন কোড তৈরি করা যায়নি";
}

function showErrors(errors) {
  errorList.innerHTML = "";
  errors.forEach(err => {
    const li = document.createElement("li");
    li.textContent = `• ${err}`;
    errorList.appendChild(li);
  });
  errorAlert.classList.remove("hidden");
}

function hideErrors() {
  errorAlert.classList.add("hidden");
  errorList.innerHTML = "";
}

// Render Tokens
function renderTokens(tokens) {
  tokenCount.textContent = toBanglaNum(tokens.length);
  tokenMetaPill.textContent = `মোট ${toBanglaNum(tokens.length)}টি টোকেন পাওয়া গেছে`;
  
  tokensTableBody.innerHTML = "";
  if (tokens.length === 0) {
    tokensTableBody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">কোনো টোকেন পাওয়া যায়নি।</td></tr>`;
    return;
  }

  tokens.forEach((t, i) => {
    const tr = document.createElement("tr");
    tr.dataset.kind = t.kind;
    tr.dataset.lexeme = t.lexeme;

    let badgeClass = "token-badge";
    if (t.kind.startsWith("TYPE_") || ["LET", "IF", "ELSE", "WHILE", "FUNCTION", "CLASS", "PRINT"].includes(t.kind)) {
      badgeClass += " kw";
    } else if (["INT", "FLOAT", "STRING", "TRUE", "FALSE"].includes(t.kind)) {
      badgeClass += " literal";
    }

    tr.innerHTML = `
      <td class="text-muted">${i + 1}</td>
      <td><span class="${badgeClass}">${t.kind}</span></td>
      <td><code>${escapeHtml(t.lexeme)}</code></td>
      <td>${t.line}</td>
      <td>${t.col}</td>
      <td>${t.value !== null ? escapeHtml(t.value) : '-'}</td>
    `;
    tokensTableBody.appendChild(tr);
  });
}

function filterTokens() {
  const query = tokenFilter.value.toLowerCase().trim();
  const rows = tokensTableBody.querySelectorAll("tr");
  rows.forEach(tr => {
    const kind = (tr.dataset.kind || "").toLowerCase();
    const lexeme = (tr.dataset.lexeme || "").toLowerCase();
    if (!query || kind.includes(query) || lexeme.includes(query)) {
      tr.style.display = "";
    } else {
      tr.style.display = "none";
    }
  });
}

// Render AST
function renderAST(astTree, astText) {
  astTextContainer.textContent = astText || "AST খালি।";

  astTreeContainer.innerHTML = "";
  if (!astTree) {
    astTreeContainer.innerHTML = '<div class="empty-state text-muted">কোনো সিনট্যাক্স ট্রি তৈরি হয়নি।</div>';
    return;
  }

  const rootEl = createTreeNodeElement(astTree);
  astTreeContainer.appendChild(rootEl);
}

function createTreeNodeElement(node) {
  const nodeEl = document.createElement("div");
  nodeEl.className = "tree-node";

  const labelEl = document.createElement("span");
  labelEl.className = "tree-label";

  const badgeClass = `badge-${node.badge || 'block'}`;
  labelEl.innerHTML = `
    <span class="node-badge ${badgeClass}">${node.badge || 'node'}</span>
    <strong>${escapeHtml(node.name)}</strong>
    ${node.detail ? `<span class="text-muted">(${escapeHtml(node.detail)})</span>` : ''}
  `;

  nodeEl.appendChild(labelEl);

  if (node.children && node.children.length > 0) {
    node.children.forEach(child => {
      nodeEl.appendChild(createTreeNodeElement(child));
    });
  }

  return nodeEl;
}

// Render Semantic Tab
function renderSemantic(symbols, functions, classes) {
  symbolsTableBody.innerHTML = "";
  if (symbols.length === 0) {
    symbolsTableBody.innerHTML = `<tr><td colspan="3" class="text-center text-muted">কোনো ভেরিয়েবল ডিফাইন করা হয়নি।</td></tr>`;
  } else {
    symbols.forEach(s => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${escapeHtml(s.name)}</strong></td>
        <td><span class="token-badge">${escapeHtml(s.type)}</span></td>
        <td><span class="info-pill">${escapeHtml(s.scope)}</span></td>
      `;
      symbolsTableBody.appendChild(tr);
    });
  }

  functionsClassesContainer.innerHTML = "";
  if (functions.length === 0 && classes.length === 0) {
    functionsClassesContainer.innerHTML = `<div class="text-muted text-center p-2">কোনো ফাংশন বা ক্লাস পাওয়া যায়নি।</div>`;
    return;
  }

  functions.forEach(fn => {
    const card = document.createElement("div");
    card.className = "fn-card";
    card.innerHTML = `
      <div><span class="fn-name">ফাংশন ${escapeHtml(fn.name)}</span> (${escapeHtml(fn.params.join(", "))}) ➔ <span class="token-badge">${escapeHtml(fn.return_type)}</span></div>
    `;
    functionsClassesContainer.appendChild(card);
  });

  classes.forEach(c => {
    const card = document.createElement("div");
    card.className = "class-card";
    card.innerHTML = `
      <div style="margin-bottom: 4px;"><strong>ক্লাস ${escapeHtml(c.name)}</strong></div>
      <div class="text-muted" style="font-size: 11.5px;">ফিল্ড: ${c.fields.join(", ") || "নেই"}</div>
      <div class="text-muted" style="font-size: 11.5px;">মেথড: ${c.methods.join("(), ") || "নেই"}()</div>
    `;
    functionsClassesContainer.appendChild(card);
  });
}

// Render TAC
function renderTAC(tac) {
  tacContainer.innerHTML = "";
  if (tac.length === 0) {
    tacContainer.innerHTML = '<div class="empty-state text-muted">কোনো TAC ইনস্ট্রাকশন তৈরি হয়নি।</div>';
    return;
  }

  tac.forEach((line, i) => {
    const div = document.createElement("div");
    div.className = "tac-line";
    div.innerHTML = `
      <span class="tac-num">${String(i).padStart(3, '0')}:</span>
      <span class="tac-code">${escapeHtml(line)}</span>
    `;
    tacContainer.appendChild(div);
  });
}

// Helper to Escape HTML
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
