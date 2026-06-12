/**
 * Renova Builders — Diagnostic Deep Dive v2
 * Paste into: Google Ads → Tools & Settings → Bulk Actions → Scripts → + New
 * Authorize → Run
 * Results delivered to: monaempoweryou@gmail.com
 *
 * Covers:
 * 1. Conversion action audit — what is actually being tracked and counted
 * 2. Campaign bidding strategy + type — all 15 campaigns confirmed
 * 3. Dead campaign root cause — why each zero-impression campaign is inactive
 * 4. Keyword bid diagnostic — bids vs. first-page CPC estimates
 * 5. Ad approval status — any disapproved or under-review ads
 * 6. Fixed search term report — actual queries triggering the ads
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';
var DATE_RANGE = 'LAST_30_DAYS';

function main() {
  var report = [];
  report.push('=== RENOVA BUILDERS — DIAGNOSTIC DEEP DIVE ===');
  report.push('Generated: ' + new Date().toLocaleString());
  report.push('Period: Last 30 Days');
  report.push('Account: ' + AdsApp.currentAccount().getName() + ' (' + AdsApp.currentAccount().getCustomerId() + ')');
  report.push('');

  report = report.concat(getConversionActionAudit());
  report.push('');
  report = report.concat(getCampaignBiddingAndType());
  report.push('');
  report = report.concat(getDeadCampaignDiagnostic());
  report.push('');
  report = report.concat(getKeywordBidDiagnostic());
  report.push('');
  report = report.concat(getAdApprovalStatus());
  report.push('');
  report = report.concat(getSearchTermReport());

  var body = report.join('\n');
  MailApp.sendEmail(
    EMAIL_RECIPIENT,
    'Renova — Diagnostic Deep Dive (' + new Date().toDateString() + ')',
    body
  );
  Logger.log('Diagnostic complete. Sent to ' + EMAIL_RECIPIENT);
}

// ─── 1. CONVERSION ACTION AUDIT ───────────────────────────────────────────────

function getConversionActionAudit() {
  var lines = ['--- 1. CONVERSION ACTION AUDIT ---'];
  try {
    // ConversionTypeName is a segment. Do NOT combine with ConversionRate or
    // CostPerConversion — they are incompatible and will cause a query error.
    var report = AdsApp.report(
      'SELECT CampaignName, ConversionTypeName, Conversions ' +
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
    var found = Object.keys(actions);
    if (found.length === 0) {
      lines.push('No conversion actions returned for this period.');
      lines.push('ACTION REQUIRED: Go to Tools & Settings > Measurement > Conversions to inspect setup.');
    } else {
      lines.push('Conversion actions found (' + found.length + '):');
      found.forEach(function(name) {
        lines.push('  Action: "' + name + '"');
        lines.push('  Total conversions (30d): ' + actions[name].toFixed(0));
        lines.push('');
      });
      var totalConv = found.reduce(function(sum, n) { return sum + actions[n]; }, 0);
      lines.push('Total conversions across all actions: ' + totalConv.toFixed(0));
      lines.push('Total account clicks (30d): 12,759');
      lines.push('');
      if (totalConv > 12759) {
        lines.push('FLAG: Conversions (' + totalConv.toFixed(0) + ') exceed total clicks (12,759).');
        lines.push('This confirms the conversion event fires multiple times per session.');
        lines.push('The named action(s) above are almost certainly NOT tracking form submissions or phone calls.');
        lines.push('They are likely tracking a micro-event: page scroll, page view, session start, or similar.');
        lines.push('Conversion data is unreliable. All CPA and conversion-based decisions are invalid until fixed.');
      }
    }
  } catch(e) {
    lines.push('ERROR querying conversion actions: ' + e.message);
  }
  return lines;
}

// ─── 2. CAMPAIGN BIDDING STRATEGY + TYPE ──────────────────────────────────────

function getCampaignBiddingAndType() {
  var lines = ['--- 2. CAMPAIGN BIDDING STRATEGY + TYPE (ALL CAMPAIGNS) ---'];
  try {
    var campaigns = AdsApp.campaigns().get();
    var active = [], dead = [];
    while (campaigns.hasNext()) {
      var c = campaigns.next();
      var stats = c.getStatsFor(DATE_RANGE);
      var impr = stats.getImpressions();
      var entry = {
        name: c.getName(),
        type: c.getAdvertisingChannelType(),
        bidding: c.getBiddingStrategyType(),
        budget: c.getBudget().getAmount(),
        impressions: impr,
        spend: stats.getCost()
      };
      if (impr > 0) active.push(entry); else dead.push(entry);
    }

    lines.push('');
    lines.push('ACTIVE (have impressions):');
    active.forEach(function(e) {
      lines.push('  Campaign: ' + e.name);
      lines.push('  Channel: ' + e.type + ' | Bidding: ' + e.bidding + ' | Budget: $' + e.budget.toFixed(2) + '/day');
      lines.push('  Impressions: ' + e.impressions + ' | Spend: $' + e.spend.toFixed(2));
      lines.push('');
    });

    lines.push('ZERO IMPRESSIONS (enabled but inactive):');
    dead.forEach(function(e) {
      lines.push('  Campaign: ' + e.name);
      lines.push('  Channel: ' + e.type + ' | Bidding: ' + e.bidding + ' | Budget: $' + e.budget.toFixed(2) + '/day');
      lines.push('');
    });
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 3. DEAD CAMPAIGN ROOT CAUSE ──────────────────────────────────────────────

function getDeadCampaignDiagnostic() {
  var lines = ['--- 3. DEAD CAMPAIGN ROOT CAUSE DIAGNOSTIC ---'];
  lines.push('Checking ad groups, keywords, and ads within each zero-impression campaign.');
  lines.push('');
  try {
    var campaigns = AdsApp.campaigns().get();
    var deadCount = 0;
    while (campaigns.hasNext()) {
      var c = campaigns.next();
      var stats = c.getStatsFor(DATE_RANGE);
      if (stats.getImpressions() > 0) continue;
      deadCount++;

      lines.push('CAMPAIGN: ' + c.getName());

      // Ad group check
      var agIter = c.adGroups().get();
      var agTotal = 0, agEnabled = 0, agPaused = 0;
      while (agIter.hasNext()) {
        var ag = agIter.next();
        agTotal++;
        if (ag.isEnabled()) agEnabled++;
        else if (ag.isPaused()) agPaused++;
      }
      lines.push('  Ad Groups: ' + agTotal + ' total | ' + agEnabled + ' enabled | ' + agPaused + ' paused');
      if (agTotal === 0)      lines.push('  >> ROOT CAUSE: No ad groups — campaign has no structure');
      else if (agEnabled === 0) lines.push('  >> ROOT CAUSE: All ad groups are paused or removed');

      // Keyword check
      var kwIter = c.keywords().get();
      var kwTotal = 0, kwEnabled = 0, kwPaused = 0;
      while (kwIter.hasNext()) {
        var kw = kwIter.next();
        kwTotal++;
        if (kw.isEnabled()) kwEnabled++;
        else if (kw.isPaused()) kwPaused++;
      }
      lines.push('  Keywords: ' + kwTotal + ' total | ' + kwEnabled + ' enabled | ' + kwPaused + ' paused');
      if (kwTotal === 0)       lines.push('  >> ROOT CAUSE: No keywords — nothing to match searches against');
      else if (kwEnabled === 0) lines.push('  >> ROOT CAUSE: All keywords are paused');

      // Ad check
      var adIter = c.ads().get();
      var adTotal = 0, adEnabled = 0;
      while (adIter.hasNext()) {
        var ad = adIter.next();
        adTotal++;
        if (ad.isEnabled()) adEnabled++;
      }
      lines.push('  Ads: ' + adTotal + ' total | ' + adEnabled + ' enabled');
      if (adTotal === 0)       lines.push('  >> ROOT CAUSE: No ads — nothing to serve');
      else if (adEnabled === 0) lines.push('  >> ROOT CAUSE: All ads are paused or removed');

      // If everything looks enabled, flag for bid/approval investigation
      if (agEnabled > 0 && kwEnabled > 0 && adEnabled > 0) {
        lines.push('  >> Structure appears intact. Root cause likely: bids too low, geo targeting issue,');
        lines.push('     ad disapproval, or Quality Score suppression. See sections 4 and 5 below.');
      }

      lines.push('');
    }
    lines.push('Total dead campaigns diagnosed: ' + deadCount);
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 4. KEYWORD BID DIAGNOSTIC ────────────────────────────────────────────────

function getKeywordBidDiagnostic() {
  var lines = ['--- 4. KEYWORD BID DIAGNOSTIC (Enabled Keywords, Zero Impressions) ---'];
  lines.push('Shows max CPC bid vs. first-page CPC estimate. If bid < first-page CPC, keyword is not entering auction.');
  lines.push('Note: Smart bidding campaigns show no manual bid — check bidding strategy instead.');
  lines.push('');
  try {
    var report = AdsApp.report(
      'SELECT CampaignName, AdGroupName, Criteria, KeywordMatchType, Status, ' +
      'CpcBid, FirstPageCpc, TopOfPageCpc, QualityScore, Impressions ' +
      'FROM KEYWORDS_PERFORMANCE_REPORT ' +
      'WHERE Status = ENABLED AND Impressions = 0 ' +
      'DURING LAST_30_DAYS ' +
      'ORDER BY CampaignName ASC ' +
      'LIMIT 0,200'
    );
    var rows = report.rows();
    var count = 0, lowBidCount = 0;
    var currentCampaign = '';
    while (rows.hasNext()) {
      var row = rows.next();
      count++;
      var camp = row['CampaignName'];
      if (camp !== currentCampaign) {
        lines.push('Campaign: ' + camp);
        currentCampaign = camp;
      }
      var fpCpc = parseFloat(row['FirstPageCpc']) || 0;
      var cpcBid = parseFloat(row['CpcBid']) || 0;
      var qs = row['QualityScore'] || 'N/A';
      var bidNote = '';
      if (fpCpc > 0 && cpcBid > 0 && cpcBid < fpCpc) {
        bidNote = ' !! BID TOO LOW — First Page: $' + fpCpc.toFixed(2) + ', Current Bid: $' + cpcBid.toFixed(2);
        lowBidCount++;
      } else if (cpcBid === 0 && fpCpc > 0) {
        bidNote = ' (Smart bidding — no manual bid set; first-page est: $' + fpCpc.toFixed(2) + ')';
      }
      lines.push('  [' + row['KeywordMatchType'] + '] ' + row['Criteria'] +
                 ' | QS: ' + qs + ' | CPC Bid: $' + cpcBid.toFixed(2) + bidNote);
    }
    if (count === 0) lines.push('No enabled zero-impression keywords returned by report.');
    lines.push('');
    lines.push('Zero-impression enabled keywords shown: ' + count);
    lines.push('Keywords with bid below first-page CPC: ' + lowBidCount);
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 5. AD APPROVAL STATUS ────────────────────────────────────────────────────

function getAdApprovalStatus() {
  var lines = ['--- 5. AD APPROVAL STATUS (All Ads) ---'];
  try {
    var report = AdsApp.report(
      'SELECT CampaignName, AdGroupName, CreativeApprovalStatus, Impressions, Clicks ' +
      'FROM AD_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS ' +
      'ORDER BY CampaignName ASC ' +
      'LIMIT 0,200'
    );
    var rows = report.rows();
    var statusCounts = {};
    var issues = [];
    while (rows.hasNext()) {
      var row = rows.next();
      var status = row['CreativeApprovalStatus'];
      if (!statusCounts[status]) statusCounts[status] = 0;
      statusCounts[status]++;
      if (status !== 'APPROVED' && status !== 'APPROVED_LIMITED') {
        issues.push('  ' + row['CampaignName'] + ' / ' + row['AdGroupName'] +
                    ' — ' + status +
                    ' | Impressions: ' + row['Impressions'] +
                    ' | Clicks: ' + row['Clicks']);
      }
    }
    lines.push('Status summary:');
    Object.keys(statusCounts).forEach(function(s) {
      lines.push('  ' + s + ': ' + statusCounts[s] + ' ad(s)');
    });
    if (issues.length > 0) {
      lines.push('');
      lines.push('Ads NOT in approved status (' + issues.length + '):');
      issues.forEach(function(i) { lines.push(i); });
    } else {
      lines.push('All ads are in approved or approved-limited status.');
    }
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 6. SEARCH TERM REPORT (FIXED) ────────────────────────────────────────────

function getSearchTermReport() {
  var lines = ['--- 6. SEARCH TERMS (Top 50 by Impressions, Last 30 Days) ---'];
  lines.push('Fix applied: LIMIT now uses "LIMIT 0,50" format required by AWQL parser.');
  lines.push('');
  try {
    var report = AdsApp.report(
      'SELECT Query, CampaignName, AdGroupName, Impressions, Clicks, Ctr, ' +
      'AverageCpc, Cost, Conversions ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS ' +
      'ORDER BY Impressions DESC ' +
      'LIMIT 0,50'
    );
    var rows = report.rows();
    var count = 0;
    while (rows.hasNext()) {
      var row = rows.next();
      count++;
      lines.push(
        count + '. "' + row['Query'] + '"' +
        ' [' + row['CampaignName'] + ' / ' + row['AdGroupName'] + ']' +
        ' | Impr: ' + row['Impressions'] +
        ' | Clicks: ' + row['Clicks'] +
        ' | CTR: ' + (parseFloat(row['Ctr']) * 100).toFixed(1) + '%' +
        ' | CPC: $' + parseFloat(row['AverageCpc']).toFixed(2) +
        ' | Cost: $' + parseFloat(row['Cost']).toFixed(2) +
        ' | Conv: ' + row['Conversions']
      );
    }
    if (count === 0) lines.push('No search terms with impressions found for this period.');
    lines.push('');
    lines.push('Search terms shown: ' + count);
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}
