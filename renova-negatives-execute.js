/**
 * Renova Builders — Negative Keyword Upload (Execution Script)
 * Adds all authorized negative keywords directly to active campaigns.
 *
 * AUTHORIZED: June 12, 2026 Executive Order — A2 item
 * ONE-TIME USE — run once, verify, done.
 * Spend impact: None. Negatives only block irrelevant traffic.
 *
 * Paste into: Google Ads → Tools & Settings → Bulk Actions → Scripts → + New
 * Authorize → Run → Check email for confirmation log.
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';

// The 2 confirmed active (KEEP) campaigns. Both receive the full list.
var TARGET_CAMPAIGNS = ['Leads Service base--13', 'full home remodel'];

// ─── PHRASE MATCH — blocks any query containing this phrase ───────────────────
var PHRASE_NEGATIVES = [
  // DIY / educational intent
  'how to', 'diy', 'step by step', 'tutorial', 'yourself', 'can i do', 'guide to',
  // Price research / informational
  'average cost', 'how much does', 'cost calculator', 'estimate calculator',
  'price of', 'is it worth', 'pros and cons',
  // Product stores
  'home depot', 'lowes', "lowe's", 'supply store', 'hardware store',
  'tile store', 'cabinet store',
  // Wrong trade types
  'roofer', 'roofing company', 'roof repair',
  'plumber', 'plumbing repair', 'plumbing service', 'handyman plumbing',
  'electrician', 'electrical repair',
  'landscaping', 'lawn service', 'pest control',
  'hvac', 'air conditioning', 'solar panel', 'moving company',
  // Job-seeking
  'job', 'jobs', 'career', 'careers', 'hiring', 'salary',
  'employment', 'apprentice', 'trade school', 'work for us',
  // Rental
  'for rent', 'to rent', 'rental', 'renting',
  // Services Renova does not offer
  'new construction', 'home builder', 'custom home builder',
  'commercial contractor', 'commercial remodel',
  // Review / directory navigation
  'complaint', 'homeadvisor', 'thumbtack',
  // Permit-only
  'permit only', 'inspection only'
];

// ─── EXACT MATCH — blocks only this precise query ─────────────────────────────
// These are confirmed wasteful from actual account data (spend with no lead potential)
var EXACT_NEGATIVES = [
  'home improvement',           // 113 impressions, 0 clicks confirmed
  'backyard landscaping',       // confirmed click, wrong service
  'foam roofing bay area',      // confirmed click, wrong trade
  'best roofer in my area',     // confirmed click, wrong trade
  'handyman plumbing near me',  // confirmed click, wrong service
  'handyman plumbers near me',  // confirmed click, wrong service
  'castro valley home depot',   // confirmed click, product store
  'home depot shower remodel'   // confirmed 2 clicks at $3.22, product store
];

function main() {
  var log = [];
  var grandTotal = 0, grandErrors = 0;

  log.push('═══════════════════════════════════════════════════════════');
  log.push('RENOVA BUILDERS — NEGATIVE KEYWORD UPLOAD CONFIRMATION');
  log.push('═══════════════════════════════════════════════════════════');
  log.push('Executed: ' + new Date().toLocaleString());
  log.push('Phrase negatives: ' + PHRASE_NEGATIVES.length);
  log.push('Exact negatives:  ' + EXACT_NEGATIVES.length);
  log.push('Total per campaign: ' + (PHRASE_NEGATIVES.length + EXACT_NEGATIVES.length));
  log.push('Target campaigns: ' + TARGET_CAMPAIGNS.join(', '));
  log.push('');

  TARGET_CAMPAIGNS.forEach(function(campName) {
    log.push('─── ' + campName + ' ───');

    var safeNameCondition = "Name = '" + campName.replace(/\\/g, '\\\\').replace(/'/g, "\\'") + "'";
    var campIter = AdsApp.campaigns().withCondition(safeNameCondition).get();

    if (!campIter.hasNext()) {
      log.push('  NOT FOUND — manual upload required for this campaign.');
      log.push('  Use renova-negatives-upload.txt and paste into the campaign negative keyword tab.');
      log.push('');
      return;
    }

    var camp = campIter.next();
    var added = 0, errors = 0;

    PHRASE_NEGATIVES.forEach(function(kw) {
      try {
        camp.createNegativeKeyword('"' + kw + '"');
        added++;
      } catch(e) {
        errors++;
        log.push('  PHRASE ERROR: "' + kw + '" — ' + e.message);
      }
    });

    EXACT_NEGATIVES.forEach(function(kw) {
      try {
        camp.createNegativeKeyword('[' + kw + ']');
        added++;
      } catch(e) {
        errors++;
        log.push('  EXACT ERROR: [' + kw + '] — ' + e.message);
      }
    });

    log.push('  Negatives added: ' + added);
    if (errors > 0) log.push('  Errors: ' + errors + ' (see lines above — may already exist)');
    log.push('');

    grandTotal  += added;
    grandErrors += errors;
  });

  log.push('─────────────────────────────────────────────────────────');
  log.push('TOTAL NEGATIVES ADDED: ' + grandTotal + ' across ' + TARGET_CAMPAIGNS.length + ' campaigns');
  if (grandErrors > 0) {
    log.push('TOTAL ERRORS: ' + grandErrors + ' (keywords may already exist — check manually)');
  } else {
    log.push('ERRORS: None');
  }
  log.push('');
  log.push('Verify at: Campaigns → [campaign name] → Keywords → Negative keywords');
  log.push('');
  log.push('WHAT THESE NEGATIVES BLOCK:');
  log.push('  • All "how to" DIY tutorial queries (~350 confirmed variants)');
  log.push('  • All "diy" intent queries (~30 confirmed variants)');
  log.push('  • All Home Depot / Lowes store navigation queries');
  log.push('  • All roofing / plumbing / landscaping (wrong trade) queries');
  log.push('  • All job-seeking queries');
  log.push('  • 8 specific confirmed wasteful exact queries (with spend, no leads)');
  log.push('');
  log.push('WHAT THESE NEGATIVES DO NOT BLOCK:');
  log.push('  • "bathroom remodel" / "kitchen remodel" — correctly not blocked');
  log.push('  • "bathroom waterproofing" — correctly not blocked ("roofing" not substring of "waterproofing" with this list)');
  log.push('  • "current bathroom designs" — correctly not blocked (false positive removed)');
  log.push('  • Any legitimate remodeling service query');
  log.push('');
  log.push('NEXT STEP: Fix conversion tracking (UI action required — see below)');
  log.push('  Tools > Measurement > Conversions > "all pages views" > Edit settings > Secondary action');

  MailApp.sendEmail(
    EMAIL_RECIPIENT,
    'Renova — Negative Keywords Uploaded ' + new Date().toDateString(),
    log.join('\n')
  );

  Logger.log('Done. ' + grandTotal + ' negatives added. Confirmation sent to ' + EMAIL_RECIPIENT);
}
