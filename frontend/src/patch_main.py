import sys

def patch_main_js(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update Imports (Add 'ai')
    old_imports = "import { auth, clients, tracking, proposals, email, documents, gem, voice, safeJ } from './services/api.js';"
    new_imports = "import { auth, clients, tracking, proposals, email, documents, gem, ai, voice, safeJ } from './services/api.js';"
    content = content.replace(old_imports, new_imports)
    
    # 2. Update nextQ Prompt (detailed JSON)
    # We use a very specific marker for Phase 5 to avoid collision
    old_prompt_marker = 'turnPrompt = `PHASE 5 (Closure): Summarize all requirements in a professional Markdown Table format.'
    new_prompt_content = """turnPrompt = `PHASE 5 (Closure): Summarize all requirements in a professional Markdown Table format.
            MANDATORY: Use EXACT wording for the last sentence of your response: "Thank you! I have captured your requirements. A Fristine Solutions Architect will now review this to finalize your formal proposal within 24–48 hours."
            MANDATORY STEP 2: Write the exact keyword: REQUIREMENTS_COMPLETE 
            MANDATORY STEP 3: Provide the full ULTRA-DETAILED JSON summary block. 
            
            CRITICAL RULES:
            1. The "detailed_analysis" field MUST be a deep technical breakdown (5-8 paragraphs) of how Zoho solves their specific business challenges.
            2. "must_have" and "pain_points" MUST be granular technical items (e.g. "Real-time SAP S/4HANA OData Sync" instead of "Integrations").
            
            JSON SCHEMA: {
              "business_overview": "Summary", "detailed_analysis": "Long-form technical rationale", "departments": [], "current_tools": [], "pain_points": [], 
              "must_have": [], "nice_to_have": [], "automation_opportunities": [], "integrations": [], 
              "success_metrics": [], "zoho_products": [], "user_count": 0, "industry": "", "summary": "", "timeline": ""
            }`;"""
    
    # Locate the old block starting with old_prompt_marker and ending with '};'
    start_idx = content.find(old_prompt_marker)
    if start_idx != -1:
        end_idx = content.find('`;', start_idx) + 2
        content = content[:start_idx] + new_prompt_content + content[end_idx:]

    # 3. Update Helpers (mdToHtml / sleep) at the bottom
    old_helpers = """function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function mdToHtml(text) {
    return text
        .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
        .replace(/\\*(.+?)\\*/g, '<em>$1</em>')
        .replace(/\\n/g, '<br>');
}"""
    
    new_helpers = """function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function mdToHtml(md) {
    if (!md) return '';
    let h = md.replace(/\\n\\n+/g, '</p><p>').replace(/\\n/g, '<br/>');
    h = h.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
    h = h.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
    h = h.replace(/^- (.*?)$/gm, '<li>$1</li>');
    h = h.replace(/(<li>[\\s\\S]*?<\/li>)/g, '<ul>$1</ul>');
    h = h.replace(/<\\/ul>\\s*<ul>/g, ''); 
    return h;
}"""
    content = content.replace(old_helpers, new_helpers)
    
    # 4. Redesign showReqSummary
    # This matches the START of the current showReqSummary and goes to where buildSolution begins.
    old_func_start = "function showReqSummary() {"
    new_func_impl = r"""function showReqSummary() {
    if (callingMode) {
        callingMode = false;
        toggleCallingMode();
    }
    const r = reqs || { summary: 'Ready to proceed.', must_have: [] };
    setStg(2, 'done'); setStg(3, 'act'); setPhase('Reviewing Requirements…');
    saveConversationMemory();

    const makeList = (arr) => (arr || []).map(i => `<li>${i}</li>`).join('');
    const products = r.zoho_products || [];
    const productChips = products.length ? products.map(p => `
        <span style="background:rgba(26,79,214,.08);color:#1A4FD6;border:1px solid rgba(26,79,214,.2);border-radius:20px;padding:4px 12px;font-size:11px;font-weight:600;display:inline-flex;align-items:center;gap:4px">
            <svg viewBox="0 0 16 16" width="12" height="12" fill="none"><path d="M4 8l3 3 5-5" stroke="#1A4FD6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            ${p}
        </span>`).join(' ') : '';

    const htmlIntro = `
    <div class="reqcard-full">
      <div class="reqcard-intro">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
            <div style="display:flex;align-items:center;gap:10px">
                <div style="width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,var(--green),#10b981);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(16,185,129,0.2)">
                    <svg viewBox="0 0 16 16" width="18" height="18" fill="none"><path d="M4 8l3 3 5-5" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <strong style="font-size:16px;color:var(--navy);letter-spacing:-0.4px">High-Fidelity Discovery Report</strong>
            </div>
            <div style="font-size:11px;font-weight:700;color:var(--primary);text-transform:uppercase;letter-spacing:1px;background:rgba(59,130,246,0.1);padding:4px 10px;border-radius:20px">Draft Verified</div>
        </div>
        <p style="font-size:13.5px;color:var(--slate);line-height:1.6;margin-bottom:0">We have mapped your requirements to the <strong>Fristine CCMS Framework</strong>.</p>
      </div>`;

    const htmlBoxHead = `
      <div class="reqcard-box">
        <div class="reqcard-title">
          <svg viewBox="0 0 20 20" width="18" height="18" fill="none"><rect x="4" y="3" width="12" height="15" rx="2" stroke="#fff" stroke-width="1.5"/><path d="M8 7h4M8 10h4M8 13h2" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>
          Technical Specification — ${cli?.company || 'Project Alpha'}
        </div>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:20px;padding:20px;background:#fff;border-bottom:1px solid var(--brd)">
            <div><div class="reqs-label">Target Industry</div><div style="font-size:14px;font-weight:700;color:var(--navy)">${r.industry || 'N/A'}</div></div>
            <div><div class="reqs-label">Scaled User Base</div><div style="font-size:14px;font-weight:700;color:var(--navy)">${r.user_count || 0} Users</div></div>
            <div><div class="reqs-label">Go-Live Milestone</div><div style="font-size:14px;font-weight:700;color:var(--primary)">${r.timeline || 'TBD'}</div></div>
        </div>`;

    const analysis = r.detailed_analysis ? `
        <div class="reqs-section" style="background:#f8fafc">
            <div class="reqs-label" style="color:var(--primary)">Strategic Technical Analysis</div>
            <div class="reqs-text" style="font-size:14px;line-height:1.8;color:var(--navy);font-weight:450">${mdToHtml(r.detailed_analysis)}</div>
        </div>` : '';

    const details = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--brd)">
            <div class="reqs-section" style="background:#fff;margin:0"><div class="reqs-label">Core Pain Points</div><ul class="reqs-list">${makeList(r.pain_points)}</ul></div>
            <div class="reqs-section" style="background:#fff;margin:0"><div class="reqs-label">Architectural Must-Haves</div><ul class="reqs-list">${makeList(r.must_have)}</ul></div>
        </div>

        <div class="reqs-section">
            <div class="reqs-label">Proposed Stack Componentry</div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">${productChips}</div>
        </div>

        <div class="reqs-actions">
          <button class="reqs-btn-confirm" id="confirmProposal">
            <svg viewBox="0 0 16 16" width="16" height="16" fill="none"><path d="M4 8l3 3 5-5" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Approve & Generate Proposal
          </button>
          <div style="display:flex;gap:8px;width:100%">
              <button class="reqs-btn-clarify" id="clarifyBtn" style="flex:1">Refine</button>
              <button class="reqs-btn-wrong" id="wrongBtn">Restart</button>
          </div>
        </div>
      </div>
    </div>`;

    addAg(htmlIntro + htmlBoxHead + analysis + details, { noEscape: true });

    setTimeout(() => {
        document.getElementById('confirmProposal')?.addEventListener('click', () => buildSolution());
        document.getElementById('clarifyBtn')?.addEventListener('click', () => {
            discoveryComplete = false;
            addAg("Of course! What changes would you like?");
            document.getElementById('msgIn').focus();
        });
        document.getElementById('wrongBtn')?.addEventListener('click', () => {
            discoveryComplete = false; reqs = null;
            addAg("No problem at all — let's start fresh.");
            document.getElementById('msgIn').focus();
        });
    }, 100);
}"""

    # Replace the existing showReqSummary block
    # We find where it starts and where the NEXT function starts
    start_func = content.find(old_func_start)
    if start_func != -1:
        # The next function usually starts with 'async function buildSolution()'
        end_func = content.find('async function buildSolution()', start_func)
        if end_func != -1:
            content = content[:start_func] + new_func_impl + "\n\n" + content[end_func:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    patch_main_js(sys.argv[1])
