/**
 * Renova Builders — PPC Execution Package Generator v1
 * Paste into: Google Ads → Tools & Settings → Bulk Actions → Scripts → + New
 * Authorize → Run
 * Output delivered to: monaempoweryou@gmail.com
 *
 * AUTHORIZED SCOPE (June 12, 2026 Executive Order):
 * 1. Campaign inventory with Keep/Repair/Review/Pause disposition
 * 2. Conversion tracking status + exact repair steps
 * 3. Negative keyword draft from actual search term data
 * 4. Dead campaign recovery recommendations
 * 5. Ad approval audit
 * 6. Execution-ready change list (execute-now vs. approval-required)
 *
 * NOT AUTHORIZED (excluded from this package):
 * Budget changes | Bid strategy changes | New campaigns | Pausing active spend campaigns
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';
var DATE_RANGE = 'LAST_30_DAYS';

// ─── NEGATIVE KEYWORD PATTERN LIBRARY ─────────────────────────────────────────
// Terms that are irrelevant for a home remodeling contractor.
// Matched against actual search queries pulled from the account.
var NEGATIVE_PATTERNS = [
  // Job-seeking
  ' job', 'jobs', 'career', 'careers', 'hiring', 'salary', 'employment',
  'apprentice', 'work for us', 'trade school',
  // DIY / educational
  'how to', 'diy ', 'tutorial', 'yourself', 'step by step', 'can i do',
  'guide to', 'training', 'certification', 'license course', 'school',
  // Material / product purchase
  'buy ', 'purchase', 'wholesale', 'home depot', 'lowes', "lowe's",
  'supply store', 'supplier', 'tile store', 'cabinet store', 'hardware store',
  // Rental
  'rent ', 'rental', ' lease', 'leasing',
  // Unrelated trades (Renova is a remodeling contractor)
  'plumber', 'plumbing', 'electrician', 'electrical', 'roofer', 'roofing',
  'landscap', 'mover', 'moving company', 'tree service', 'pest control',
  'hvac', 'air conditioning', 'solar panel', 'garage door repair',
  // Informational / price research (high impression, low purchase intent)
  'average cost', 'how much does', 'cost calculator', 'estimate calculator',
  'price of ', 'is it worth', 'pros and cons',
  // Service types Renova does not offer
  'new construction', 'custom home builder', 'home builder',
  'commercial contractor', 'commercial remodel',
  // Complaint / review navigation
  'complaint', 'bbb ', 'yelp ', 'angie', 'thumbtack', 'homeadvisor',
  'nextdoor', 'facebook review',
  // Permit / inspection only
  'permit only', 'inspection only', 'city permit',
];

function main() {
  var out = [];
  out.push('═══════════════════════════════════════════════════════════');
  out.push('  RENOVA BUILDERS — PPC EXECUTION PACKAGE');
  out.push('═══════════════════════════════════════════════════════════');
  out.push('Generated: ' + new Date().toLocaleString());
  out.push('Period: Last 30 Days');
  out.push('Account: ' + AdsApp.currentAccount().getName() +
           ' (' + AdsApp.currentAccount().getCustomerId() + ')');
  out.push('');
  out.push('AUTHORIZED SCOPE: Measurement | Targeting | Structural cleanup');
  out.push('NOT AUTHORIZED: Budgets | Bids | New campaigns | Pausing active spend');
  out.push('');

  out = out.concat(section1_ConversionAudit());
  out.push('');
  out = out.concat(section2_CampaignInventory());
  out.push('');
  out = out.concat(section3_NegativeKeywords());
  out.push('');
  out = out.concat(section4_AdApproval());
  out.push('');
  out = out.concat(section5_ExecutionList());

  MailApp.sendEmail(
    EMAIL_RECIPIENT,
    'Renova PPC — Execution Package ' + new Date().toDateString(),
    out.join('\n')
  );
  Logger.log('Execution package complete. Sent to ' + EMAIL_RECIPIENT);
}

// ─── 1. CONVERSION TRACKING AUDIT ─────────────────────────────────────────────

function section1_ConversionAudit() {
  var lines = ['━━━ 1. CONVERSION TRACKING AUDIT ━━━'];
  lines.push('Root issue: Smart Bidding is training on polluted conversion data.');
  lines.push('This must be fixed before any performance evaluation or bid strategy change.');
  lines.push('');

  try {
    var report = AdsApp.report(
      'SELECT ConversionTypeName, Conversions ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS'
    );
    var rows = report.rows();
    var actions = {};
    while (rows.hasNext()) {
      var row = rows.next();
      var name = row['ConversionTypeName'];
      if (!name || name === '--') continue;
      var convs = parseFloat(row['Conversions']) || 0;
      if (!actions[name]) actions[name] = 0;
      actions[name] += convs;
    }

    var keys = Object.keys(actions);
    var totalConv = keys.reduce(function(s, k) { return s + actions[k]; }, 0);
    lines.push('Conversion actions detected: ' + keys.length);
    lines.push('Total 30-day conversions: ' + totalConv.toFixed(0));
    lines.push('');

    keys.forEach(function(name) {
      var count = actions[name];
      var nameLower = name.toLowerCase();
      var verdict, requiredAction, authorized;

      if (nameLower.indexOf('page') !== -1 || nameLower.indexOf('view') !== -1 ||
          nameLower.indexOf('session') !== -1 || nameLower.indexOf('scroll') !== -1) {
        verdict = 'INVALID — Page view event. This is not a lead.';
        requiredAction = 'Demote to Secondary action. Do NOT delete — deletion breaks historical data.';
        authorized = 'YES — safe to execute immediately (no spend impact)';
      } else if (nameLower.indexOf('phone') !== -1 || nameLower.indexOf('call') !== -1) {
        verdict = 'VALID — Phone engagement. Real lead signal.';
        requiredAction = 'Keep as Primary. Verify tag is firing on click, not page load.';
        authorized = 'YES — verify only, no changes needed if confirmed';
      } else if (nameLower.indexOf('form') !== -1 || nameLower.indexOf('submit') !== -1 ||
                 nameLower.indexOf('quote') !== -1 || nameLower.indexOf('qoute') !== -1 ||
                 nameLower.indexOf('request') !== -1 || nameLower.indexOf('contact') !== -1) {
        verdict = 'UNVERIFIED — Name suggests form/quote but may be page visit. Check tag type.';
        requiredAction = 'Open action in Conversions UI. If tag trigger = URL match / page visit → demote to Secondary. If trigger = form submit / click → keep Primary.';
        authorized = 'VERIFY FIRST — classification determines action';
      } else {
        verdict = 'UNVERIFIED — Cannot classify from name alone.';
        requiredAction = 'Manual review required. Check tag trigger in Conversions UI.';
        authorized = 'VERIFY FIRST';
      }

      lines.push('  Action: "' + name + '"');
      lines.push('  30-day conversions: ' + count.toFixed(0));
      lines.push('  Verdict: ' + verdict);
      lines.push('  Action required: ' + requiredAction);
      lines.push('  Execute without approval: ' + authorized);
      lines.push('');
    });

    if (totalConv > 12759) {
      lines.push('CONFIRMED POLLUTION: ' + totalConv.toFixed(0) + ' conversions vs 12,759 clicks.');
      lines.push('Conversions exceed clicks. Smart Bidding is chasing page views at $0.37 CPC.');
      lines.push('Every MAXIMIZE_CONVERSIONS campaign is misdirected until this is fixed.');
      lines.push('');
    }

    lines.push('REPAIR SEQUENCE (exact steps):');
    lines.push('  Step 1: Tools > Measurement > Conversions');
    lines.push('  Step 2: Open each action. Check "Optimization" column — Primary vs Secondary.');
    lines.push('  Step 3: For page view actions → click action → "Edit settings" → set to Secondary');
    lines.push('  Step 4: For quote/contact actions → verify trigger type before changing anything');
    lines.push('  Step 5: For phone actions → confirm Primary. No changes if already set correctly.');
    lines.push('  Step 6: After fix, allow 14-28 days recalibration. Do NOT evaluate campaigns during this window.');
    lines.push('  AUTHORIZED: Steps 1-5 have zero spend impact. Execute on approval.');

  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 2. CAMPAIGN INVENTORY ─────────────────────────────────────────────────────

function section2_CampaignInventory() {
  var lines = ['━━━ 2. CAMPAIGN INVENTORY — Keep / Repair / Review / Pause ━━━'];
  lines.push('');
  lines.push('KEEP   — Active spend, healthy structure. Do not touch until measurement is clean.');
  lines.push('REPAIR — Active or salvageable. Specific structural fix needed.');
  lines.push('REVIEW — Zero impressions but structure intact. Reassess post-measurement fix.');
  lines.push('PAUSE  — Structurally broken or empty. No path to impressions without rebuild.');
  lines.push('         [PAUSE actions require Maor approval before execution]');
  lines.push('');

  try {
    var campaigns = AdsApp.campaigns().get();
    var keep = [], repair = [], review = [], pauseList = [];

    while (campaigns.hasNext()) {
      var c = campaigns.next();
      var stats = c.getStatsFor(DATE_RANGE);
      var impr = stats.getImpressions();
      var spend = stats.getCost();
      var name = c.getName();
      var bidding = c.getBiddingStrategyType();
      var budget = c.getBudget().getAmount();

      // Count structure
      var agTotal = 0, agEnabled = 0, agPaused = 0;
      var agIter = c.adGroups().get();
      while (agIter.hasNext()) {
        var ag = agIter.next(); agTotal++;
        if (ag.isEnabled()) agEnabled++; else if (ag.isPaused()) agPaused++;
      }

      var kwTotal = 0, kwEnabled = 0;
      var kwIter = c.keywords().get();
      while (kwIter.hasNext()) {
        var kw = kwIter.next(); kwTotal++;
        if (kw.isEnabled()) kwEnabled++;
      }

      var adTotal = 0, adEnabled = 0;
      var adIter = c.ads().get();
      while (adIter.hasNext()) {
        var ad = adIter.next(); adTotal++;
        if (ad.isEnabled()) adEnabled++;
      }

      var entry = {
        name: name, bidding: bidding, budget: budget,
        impressions: impr, spend: spend,
        agTotal: agTotal, agEnabled: agEnabled, agPaused: agPaused,
        kwTotal: kwTotal, kwEnabled: kwEnabled,
        adTotal: adTotal, adEnabled: adEnabled,
        disposition: '', rootCause: '', nextAction: ''
      };

      if (impr > 0) {
        entry.disposition = 'KEEP';
        entry.rootCause = 'Active. Generating impressions and spend.';
        entry.nextAction = 'Monitor only until conversion tracking is fixed. No structural changes.';
        keep.push(entry);
      } else if (agTotal === 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'No ad groups. Campaign has no structure whatsoever.';
        entry.nextAction = 'Pause and archive. No recovery path without full rebuild.';
        pauseList.push(entry);
      } else if (kwTotal === 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'No keywords. Search campaign with no targeting.';
        entry.nextAction = 'Pause and archive. No recovery path without adding keywords.';
        pauseList.push(entry);
      } else if (adTotal === 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'No ads. Nothing to serve even if keywords match.';
        entry.nextAction = 'Pause and archive. No recovery path without adding ads.';
        pauseList.push(entry);
      } else if (agEnabled === 0 && agPaused > 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'All ' + agTotal + ' ad groups are paused. No path to auction.';
        entry.nextAction = 'Pause campaign. Investigate why ad groups were paused before any revival.';
        pauseList.push(entry);
      } else if (kwEnabled === 0 && kwTotal > 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'All ' + kwTotal + ' keywords paused. No search targeting active.';
        entry.nextAction = 'Pause campaign. Review keyword strategy before revival.';
        pauseList.push(entry);
      } else if (adEnabled === 0 && adTotal > 0) {
        entry.disposition = 'PAUSE';
        entry.rootCause = 'All ' + adTotal + ' ads paused or removed. Nothing to serve.';
        entry.nextAction = 'Pause campaign. Ads need revival or replacement.';
        pauseList.push(entry);
      } else if (agEnabled > 0 && kwEnabled > 0 && adEnabled > 0) {
        entry.disposition = 'REVIEW';
        entry.rootCause = 'Structure intact (' + agEnabled + ' ad groups, ' + kwEnabled + ' keywords, ' + adEnabled + ' ads) but zero impressions.';
        entry.nextAction = 'Check: (1) bids vs first-page CPC, (2) geo targeting, (3) budget exhaustion, (4) ad quality. Do not pause until root cause confirmed.';
        review.push(entry);
      } else {
        entry.disposition = 'REPAIR';
        entry.rootCause = 'Partial structure: ' + agEnabled + '/' + agTotal + ' ad groups enabled, ' + kwEnabled + '/' + kwTotal + ' keywords, ' + adEnabled + '/' + adTotal + ' ads.';
        entry.nextAction = 'Enable paused elements if they are valid. Remove if they are incomplete.';
        repair.push(entry);
      }
    }

    function printGroup(label, arr, approvalNote) {
      lines.push(label + ' (' + arr.length + ' campaigns)' + (approvalNote ? ' — ' + approvalNote : '') + ':');
      if (arr.length === 0) { lines.push('  None.'); lines.push(''); return; }
      arr.forEach(function(e) {
        lines.push('');
        lines.push('  ▸ ' + e.name);
        lines.push('    Disposition: ' + e.disposition);
        lines.push('    Root cause: ' + e.rootCause);
        lines.push('    Next action: ' + e.nextAction);
        lines.push('    Bidding: ' + e.bidding + ' | Budget: $' + e.budget.toFixed(2) + '/day | 30d Spend: $' + e.spend.toFixed(2));
        lines.push('    Structure: ' + e.agEnabled + '/' + e.agTotal + ' ad groups | ' +
                   e.kwEnabled + '/' + e.kwTotal + ' keywords | ' + e.adEnabled + '/' + e.adTotal + ' ads');
      });
      lines.push('');
    }

    printGroup('KEEP', keep);
    printGroup('REVIEW — structure intact, diagnose before touching', review);
    printGroup('REPAIR — partial structure', repair);
    printGroup('PAUSE RECOMMENDED', pauseList, 'requires Maor approval');

    var pauseBudget = pauseList.reduce(function(s, e) { return s + e.budget; }, 0);
    var pauseSpend = pauseList.reduce(function(s, e) { return s + e.spend; }, 0);
    lines.push('INVENTORY SUMMARY:');
    lines.push('  KEEP: ' + keep.length + ' | REVIEW: ' + review.length +
               ' | REPAIR: ' + repair.length + ' | PAUSE: ' + pauseList.length);
    lines.push('  Pause candidates: $' + pauseBudget.toFixed(2) + '/day allocated | $' +
               pauseSpend.toFixed(2) + ' actual 30d spend');
    lines.push('  Note: Most PAUSE candidates have $0 actual spend — pausing is account hygiene, not spend reduction.');

  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 3. NEGATIVE KEYWORD DRAFT ─────────────────────────────────────────────────

function section3_NegativeKeywords() {
  var lines = ['━━━ 3. NEGATIVE KEYWORD DRAFT ━━━'];
  lines.push('Built from actual search query data. Pattern-matched against irrelevant terms');
  lines.push('for a home remodeling contractor. Review before uploading.');
  lines.push('');

  try {
    var report = AdsApp.report(
      'SELECT Query, CampaignName, Impressions, Clicks, Cost, Conversions ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS ' +
      'LIMIT 0,2500'
    );
    var rows = report.rows();
    var allTerms = [];
    while (rows.hasNext()) {
      var row = rows.next();
      allTerms.push({
        query: row['Query'],
        queryLower: row['Query'].toLowerCase(),
        campaign: row['CampaignName'],
        impressions: parseInt((row['Impressions'] || '0').replace(/,/g, '')) || 0,
        clicks: parseInt((row['Clicks'] || '0').replace(/,/g, '')) || 0,
        cost: parseFloat(row['Cost']) || 0,
        conv: parseFloat(row['Conversions']) || 0
      });
    }

    // Sort by impressions descending
    allTerms.sort(function(a, b) { return b.impressions - a.impressions; });

    // Pattern match
    var confirmed = [];   // Matched to a negative pattern
    var highWaste = [];   // High impressions, zero clicks, not pattern-matched
    var totalImprFlagged = 0, totalCostFlagged = 0;

    allTerms.forEach(function(t) {
      var matchedPattern = null;
      for (var i = 0; i < NEGATIVE_PATTERNS.length; i++) {
        if (t.queryLower.indexOf(NEGATIVE_PATTERNS[i]) !== -1) {
          matchedPattern = NEGATIVE_PATTERNS[i].trim();
          break;
        }
      }
      if (matchedPattern) {
        confirmed.push({ term: t.query, impr: t.impressions, clicks: t.clicks, cost: t.cost, pattern: matchedPattern, campaign: t.campaign });
        totalImprFlagged += t.impressions;
        totalCostFlagged += t.cost;
      } else if (t.impressions >= 50 && t.clicks === 0) {
        highWaste.push({ term: t.query, impr: t.impressions, campaign: t.campaign });
      }
    });

    lines.push('Total search terms analyzed: ' + allTerms.length);
    lines.push('Pattern-matched negative candidates: ' + confirmed.length);
    lines.push('Impressions recoverable by adding these negatives: ' + totalImprFlagged);
    lines.push('Spend recoverable: $' + totalCostFlagged.toFixed(2));
    lines.push('');

    if (confirmed.length > 0) {
      lines.push('CONFIRMED NEGATIVE CANDIDATES (sorted by impressions):');
      lines.push('[Format: Rank. "Query" | Impressions | Clicks | Spend | Pattern matched | Campaign]');
      lines.push('');
      confirmed.sort(function(a, b) { return b.impr - a.impr; });
      confirmed.forEach(function(f, i) {
        lines.push((i + 1) + '. "' + f.term + '"' +
                   ' | ' + f.impr + ' impr | ' + f.clicks + ' clicks | $' + f.cost.toFixed(2) +
                   ' | pattern: "' + f.pattern + '"' +
                   ' | ' + f.campaign);
      });
    } else {
      lines.push('No pattern-matched irrelevant terms found. Manual search term review required.');
    }

    lines.push('');
    if (highWaste.length > 0) {
      lines.push('HIGH-IMPRESSION ZERO-CLICK TERMS — needs manual classification:');
      lines.push('These generate impressions but zero engagement. May indicate wrong match type, wrong audience, or irrelevant query.');
      highWaste.slice(0, 25).forEach(function(f, i) {
        lines.push('  ' + (i + 1) + '. "' + f.term + '" | ' + f.impr + ' impr | 0 clicks | ' + f.campaign);
      });
      if (highWaste.length > 25) lines.push('  ... and ' + (highWaste.length - 25) + ' more.');
    }

    lines.push('');
    lines.push('UPLOAD INSTRUCTIONS:');
    lines.push('  For clear pattern terms (e.g., "jobs", "diy", "how to"):');
    lines.push('    → Add as [PHRASE] match at account-level negative keyword list');
    lines.push('    → Tools > Shared library > Negative keyword lists > + New list');
    lines.push('  For specific one-off queries:');
    lines.push('    → Add as [EXACT] match at campaign level');
    lines.push('  AUTHORIZED: Adding negatives does not change bids or budgets. Safe to execute.');

  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 4. AD APPROVAL AUDIT ─────────────────────────────────────────────────────

function section4_AdApproval() {
  var lines = ['━━━ 4. AD APPROVAL AUDIT ━━━'];
  lines.push('Checks all enabled and paused ads for policy status.');
  lines.push('');

  try {
    var adIter = AdsApp.ads().get();
    var statusCounts = {};
    var issues = [];
    var total = 0;

    while (adIter.hasNext()) {
      var ad = adIter.next();
      total++;
      var status = ad.getApprovalStatus();
      var campName = ad.getAdGroup().getCampaign().getName();
      var agName = ad.getAdGroup().getName();
      if (!statusCounts[status]) statusCounts[status] = 0;
      statusCounts[status]++;
      if (status !== 'APPROVED' && status !== 'APPROVED_LIMITED') {
        var stats = ad.getStatsFor(DATE_RANGE);
        issues.push({
          camp: campName, ag: agName, status: status,
          impr: stats.getImpressions(), clicks: stats.getClicks()
        });
      }
    }

    lines.push('Ads audited: ' + total);
    lines.push('');
    lines.push('Approval status breakdown:');
    Object.keys(statusCounts).forEach(function(s) {
      lines.push('  ' + s + ': ' + statusCounts[s] + ' ad(s)');
    });
    lines.push('');

    if (issues.length === 0) {
      lines.push('All ads in approved or approved-limited status. No action required.');
    } else {
      lines.push('NON-APPROVED ADS (' + issues.length + ') — require attention:');
      lines.push('');
      issues.forEach(function(i) {
        lines.push('  Campaign: ' + i.camp);
        lines.push('  Ad Group: ' + i.ag);
        lines.push('  Status: ' + i.status);
        lines.push('  30d Performance: ' + i.impr + ' impressions | ' + i.clicks + ' clicks');
        lines.push('');
      });
      lines.push('ACTION: For each disapproved ad:');
      lines.push('  → Navigate to the ad in the UI');
      lines.push('  → Click "Why is this ad disapproved?" to see the policy reason');
      lines.push('  → Fix the policy violation and resubmit');
      lines.push('  AUTHORIZED: Fixing policy violations and resubmitting is safe to execute.');
    }

    lines.push('');
    lines.push('NOTE: APPROVED_LIMITED means the ad runs but is restricted in some contexts.');
    lines.push('Common reasons: alcohol, gambling, political content. If none apply, investigate.');

  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 5. EXECUTION LIST ─────────────────────────────────────────────────────────

function section5_ExecutionList() {
  var lines = ['━━━ 5. EXECUTION-READY CHANGE LIST ━━━'];
  lines.push('');
  lines.push('A. EXECUTE NOW — Authorized per June 12, 2026 Executive Order');
  lines.push('   (No spend impact. No structural changes. Safe to execute immediately.)');
  lines.push('');
  lines.push('   A1. FIX CONVERSION TRACKING');
  lines.push('       Where: Tools > Measurement > Conversions');
  lines.push('       Action: Demote page view actions to Secondary (see Section 1 for exact list)');
  lines.push('       Impact: Stops Smart Bidding from training on page views');
  lines.push('       Risk: None. Reversible at any time.');
  lines.push('');
  lines.push('   A2. UPLOAD NEGATIVE KEYWORDS');
  lines.push('       Where: Tools > Shared library > Negative keyword lists');
  lines.push('       Action: Add pattern-matched irrelevant terms from Section 3');
  lines.push('       Impact: Removes irrelevant impressions and clicks');
  lines.push('       Risk: Low. Each negative is individually removable if too aggressive.');
  lines.push('');
  lines.push('   A3. FIX DISAPPROVED ADS');
  lines.push('       Where: Ads & assets (navigate to each non-approved ad in Section 4)');
  lines.push('       Action: Fix policy violation, resubmit for review');
  lines.push('       Impact: Restores ad eligibility in blocked campaigns');
  lines.push('       Risk: None.');
  lines.push('');
  lines.push('────────────────────────────────────────────────────────');
  lines.push('');
  lines.push('B. REQUIRES MAOR APPROVAL — Do not execute without sign-off');
  lines.push('');
  lines.push('   B1. PAUSE DEAD CAMPAIGNS');
  lines.push('       Scope: Campaigns with no structure or all elements paused (see Section 2)');
  lines.push('       Impact: Account hygiene. Dead campaigns have $0 actual spend — pausing is');
  lines.push('               cleanup only. Budget allocation numbers will look cleaner.');
  lines.push('       Reason for approval: Structural change to account architecture.');
  lines.push('       Exception: "Renova Leads-Search" — confirmed empty, $100/day budget.');
  lines.push('                  Recommend prioritizing this one pause for approval.');
  lines.push('');
  lines.push('   B2. BID STRATEGY REVISION');
  lines.push('       Scope: Switch active campaigns from MAXIMIZE_CONVERSIONS → MAXIMIZE_CLICKS');
  lines.push('       Timing: Not before 14-28 days after conversion tracking is fixed');
  lines.push('       Reason: Smart Bidding needs clean conversion data to recalibrate.');
  lines.push('               Switching strategy before recalibration wastes the reset period.');
  lines.push('       Reason for approval: Bid strategy change per executive order restriction.');
  lines.push('');
  lines.push('   B3. KEYWORD BID REPAIRS (REVIEW campaigns)');
  lines.push('       Scope: Campaigns with intact structure but $0.01 bids (see Section 2 REVIEW)');
  lines.push('       Action: Raise CPC bids to exceed first-page CPC estimate per keyword');
  lines.push('       Impact: Activates campaigns that are currently below auction floor');
  lines.push('       Reason for approval: Bid increase = potential spend increase.');
  lines.push('');
  lines.push('   B4. STRUCTURAL REBUILDS');
  lines.push('       Scope: Campaigns in REPAIR category (partial structure)');
  lines.push('       Action: New ad copy, keyword restructuring, ad group reorganization');
  lines.push('       Timing: Not before measurement is confirmed clean');
  lines.push('       Reason for approval: Major structural changes per executive order.');
  lines.push('');
  lines.push('────────────────────────────────────────────────────────');
  lines.push('');
  lines.push('RECOMMENDED EXECUTION SEQUENCE:');
  lines.push('  Week 1:   Execute A1 + A2 + A3 (conversion fix, negatives, ad fixes)');
  lines.push('  Week 2-4: Smart Bidding recalibration window. Monitor spend only. No changes.');
  lines.push('  Week 4:   Pull fresh performance report. Submit B1 for approval (campaign pauses).');
  lines.push('  Week 5:   After B1 approved and executed, submit B2 (bid strategy) for approval.');
  lines.push('  Week 6+:  Assess B3 and B4 based on clean data from weeks 1-5.');
  lines.push('');
  lines.push('Every step after A3 depends on clean conversion data from A1.');
  lines.push('Do not evaluate campaign performance or make optimization decisions during weeks 2-4.');
  return lines;
}
