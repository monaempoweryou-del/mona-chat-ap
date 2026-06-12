/**
 * Renova Builders — Weekly Performance Monitor
 * Runs every Monday. Sends executive report to monaempoweryou@gmail.com.
 *
 * Covers:
 *   1. Lead volume (phone clicks) — week-over-week
 *   2. Spend vs $5,000/month cap
 *   3. Top 10 search terms this week (new negative candidates flagged)
 *   4. Campaign health (impressions, clicks, CPL)
 *   5. Anomaly alerts (spend spikes, zero-impression days, CPL outliers)
 *
 * SETUP: Google Ads → Tools → Bulk Actions → Scripts → + New
 *   Paste → Authorize → Save → Schedule: Weekly, Monday 8:00 AM
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';
var SPEND_CAP_MONTHLY = 5000;
var KEEP_CAMPAIGNS = ['Leads Service base--13', 'full home remodel'];

// Keywords that indicate irrelevant traffic — flag as negative candidates
var NEGATIVE_SIGNALS = [
  'diy', 'how to', 'tutorial', 'step by step', 'yourself',
  'average cost', 'how much', 'cost calculator', 'price of', 'pros and cons',
  'home depot', 'lowes', 'hardware store', 'supply store',
  'roofer', 'roofing', 'plumber', 'plumbing', 'electrician', 'landscaping',
  'lawn', 'pest', 'hvac', 'air conditioning', 'solar', 'moving',
  'job', 'career', 'hiring', 'salary', 'employment', 'apprentice',
  'for rent', 'to rent', 'rental', 'renting',
  'new construction', 'home builder', 'commercial',
  'homeadvisor', 'thumbtack', 'angie', 'complaint',
  'permit only', 'inspection only'
];

function main() {
  var log = [];
  var alerts = [];
  var today = new Date();
  var weekLabel = 'Week of ' + today.toDateString();

  log.push('═══════════════════════════════════════════════════════════════');
  log.push('RENOVA BUILDERS — WEEKLY PERFORMANCE MONITOR');
  log.push(weekLabel);
  log.push('═══════════════════════════════════════════════════════════════');
  log.push('');

  section1_SpendVsCap(log, alerts);
  log.push('');
  section2_CampaignHealth(log, alerts);
  log.push('');
  section3_LeadSignals(log, alerts);
  log.push('');
  section4_SearchTermReview(log, alerts);
  log.push('');
  section5_Anomalies(log, alerts);
  log.push('');

  // Alert summary at top (prepend)
  var header = [];
  if (alerts.length > 0) {
    header.push('⚠ ALERTS THIS WEEK (' + alerts.length + '):');
    alerts.forEach(function(a) { header.push('  • ' + a); });
    header.push('');
  } else {
    header.push('✓ NO ALERTS — Account operating normally.');
    header.push('');
  }

  var fullLog = header.concat(log);
  fullLog.push('───────────────────────────────────────────────────────────────');
  fullLog.push('NEXT STEPS:');
  fullLog.push('  • Review any flagged negative keyword candidates above');
  fullLog.push('  • Add confirmed negatives to renova-negatives-execute.js and re-run');
  fullLog.push('  • Review any anomaly alerts with Nataly if spend impact > $50');
  fullLog.push('  • If monthly spend on pace > $4,500 → flag to Maor before cap hit');
  fullLog.push('');
  fullLog.push('Monitor script: renova-weekly-monitor.js | Branch: claude/nova-image-preview-ri1q4z');

  var subject = alerts.length > 0
    ? 'ALERT: Renova Weekly Monitor — ' + alerts.length + ' item(s) need attention — ' + today.toDateString()
    : 'Renova Weekly Monitor — All Clear — ' + today.toDateString();

  MailApp.sendEmail(EMAIL_RECIPIENT, subject, fullLog.join('\n'));
  Logger.log('Weekly monitor complete. ' + alerts.length + ' alerts. Report sent to ' + EMAIL_RECIPIENT);
}

// ─── SECTION 1: Spend vs Monthly Cap ─────────────────────────────────────────
function section1_SpendVsCap(log, alerts) {
  log.push('─── 1. SPEND VS MONTHLY CAP ───');

  try {
    var thisWeekSpend = 0;
    var last30Spend = 0;

    KEEP_CAMPAIGNS.forEach(function(campName) {
      var iter = AdsApp.campaigns()
        .withCondition("Name = '" + campName.replace(/'/g, "\\'") + "'")
        .get();
      if (iter.hasNext()) {
        var c = iter.next();
        thisWeekSpend += c.getStatsFor('LAST_7_DAYS').getCost();
        last30Spend   += c.getStatsFor('LAST_30_DAYS').getCost();
      }
    });

    var dailyRate    = thisWeekSpend / 7;
    var projectedMo  = dailyRate * 30.4;
    var capPct       = (projectedMo / SPEND_CAP_MONTHLY * 100).toFixed(0);

    log.push('  Last 7 days:       $' + thisWeekSpend.toFixed(2));
    log.push('  Last 30 days:      $' + last30Spend.toFixed(2));
    log.push('  Daily rate (7d):   $' + dailyRate.toFixed(2) + '/day');
    log.push('  Projected monthly: $' + projectedMo.toFixed(2) + ' (' + capPct + '% of $5,000 cap)');

    if (projectedMo > 4500) {
      alerts.push('SPEND ALERT: Projected monthly $' + projectedMo.toFixed(0) + ' approaching $5,000 cap. Review with Maor.');
    }
    if (projectedMo > 5000) {
      alerts.push('CRITICAL: Projected monthly spend EXCEEDS $5,000 cap. Immediate review required.');
    }
  } catch(e) {
    log.push('  ERROR: ' + e.message);
  }
}

// ─── SECTION 2: Campaign Health ───────────────────────────────────────────────
function section2_CampaignHealth(log, alerts) {
  log.push('─── 2. CAMPAIGN HEALTH (KEEP CAMPAIGNS) ───');

  try {
    KEEP_CAMPAIGNS.forEach(function(campName) {
      var iter = AdsApp.campaigns()
        .withCondition("Name = '" + campName.replace(/'/g, "\\'") + "'")
        .get();

      if (!iter.hasNext()) {
        log.push('  ' + campName + ': NOT FOUND');
        alerts.push('Campaign not found: "' + campName + '" — verify campaign name.');
        return;
      }

      var c     = iter.next();
      var s7    = c.getStatsFor('LAST_7_DAYS');
      var s30   = c.getStatsFor('LAST_30_DAYS');

      var impr7    = s7.getImpressions();
      var clicks7  = s7.getClicks();
      var cost7    = s7.getCost();
      var conv7    = s7.getConversions();
      var impr30   = s30.getImpressions();
      var clicks30 = s30.getClicks();
      var cost30   = s30.getCost();
      var ctr7     = impr7 > 0 ? (clicks7 / impr7 * 100).toFixed(2) : '0.00';
      var cpc7     = clicks7 > 0 ? (cost7 / clicks7).toFixed(2) : '0.00';

      log.push('  ── ' + campName + ' ──');
      log.push('    7-day:  ' + impr7 + ' impr | ' + clicks7 + ' clicks | ' + ctr7 + '% CTR | $' + cpc7 + ' CPC | $' + cost7.toFixed(2) + ' spend | ' + conv7 + ' conv');
      log.push('    30-day: ' + impr30 + ' impr | ' + clicks30 + ' clicks | $' + cost30.toFixed(2) + ' spend');

      if (impr7 === 0) {
        alerts.push(campName + ': ZERO impressions this week. Campaign may be paused or budget depleted.');
      }
      if (cost7 > (cost30 / 4) * 1.5) {
        alerts.push(campName + ': Spend spike this week ($' + cost7.toFixed(2) + ' vs avg $' + (cost30/4).toFixed(2) + '/week). Review search terms.');
      }
    });
  } catch(e) {
    log.push('  ERROR: ' + e.message);
  }
}

// ─── SECTION 3: Lead Signals (Phone Clicks) ──────────────────────────────────
function section3_LeadSignals(log, alerts) {
  log.push('─── 3. LEAD SIGNALS (PHONE + CONVERSION DATA) ───');

  try {
    var report7 = AdsApp.report(
      'SELECT CampaignName, Clicks, Cost, Conversions, ConversionRate ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_7_DAYS'
    );

    var report30 = AdsApp.report(
      'SELECT CampaignName, Clicks, Cost, Conversions, ConversionRate ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS'
    );

    var totals7  = { clicks: 0, cost: 0, conv: 0 };
    var totals30 = { clicks: 0, cost: 0, conv: 0 };

    var rows7 = report7.rows();
    while (rows7.hasNext()) {
      var r = rows7.next();
      if (KEEP_CAMPAIGNS.indexOf(r['CampaignName']) !== -1) {
        totals7.clicks += parseInt(r['Clicks'].replace(/,/g, '')) || 0;
        totals7.cost   += parseFloat(r['Cost'].replace(/,/g, '')) || 0;
        totals7.conv   += parseFloat(r['Conversions'].replace(/,/g, '')) || 0;
      }
    }

    var rows30 = report30.rows();
    while (rows30.hasNext()) {
      var r = rows30.next();
      if (KEEP_CAMPAIGNS.indexOf(r['CampaignName']) !== -1) {
        totals30.clicks += parseInt(r['Clicks'].replace(/,/g, '')) || 0;
        totals30.cost   += parseFloat(r['Cost'].replace(/,/g, '')) || 0;
        totals30.conv   += parseFloat(r['Conversions'].replace(/,/g, '')) || 0;
      }
    }

    var cpConv7  = totals7.conv > 0  ? '$' + (totals7.cost / totals7.conv).toFixed(2)   : 'N/A';
    var cpConv30 = totals30.conv > 0 ? '$' + (totals30.cost / totals30.conv).toFixed(2)  : 'N/A';

    log.push('  7-day:  ' + totals7.clicks + ' clicks | ' + totals7.conv.toFixed(1) + ' conv | ' + cpConv7 + ' cost/conv | $' + totals7.cost.toFixed(2) + ' spend');
    log.push('  30-day: ' + totals30.clicks + ' clicks | ' + totals30.conv.toFixed(1) + ' conv | ' + cpConv30 + ' cost/conv | $' + totals30.cost.toFixed(2) + ' spend');
    log.push('');
    log.push('  NOTE: Conversion counts include ALL primary conversion actions.');
    log.push('  If "all pages views" has NOT been demoted to Secondary yet,');
    log.push('  these numbers are inflated and not reflective of actual leads.');
    log.push('  ACTION REQUIRED: Demote page view events to Secondary in Google Ads UI.');

    if (totals7.conv > totals7.clicks) {
      alerts.push('Conversion pollution detected: ' + totals7.conv.toFixed(0) + ' conversions > ' + totals7.clicks + ' clicks. Page view tracking still primary. Fix conversion settings immediately.');
    }
  } catch(e) {
    log.push('  ERROR: ' + e.message);
  }
}

// ─── SECTION 4: Search Term Review — New Negative Candidates ─────────────────
function section4_SearchTermReview(log, alerts) {
  log.push('─── 4. SEARCH TERM REVIEW — NEW NEGATIVE CANDIDATES ───');

  try {
    var report = AdsApp.report(
      'SELECT Query, CampaignName, Impressions, Clicks, Cost, Conversions ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_7_DAYS ' +
      'LIMIT 0,1000'
    );

    var rows = report.rows();
    var terms = [];
    while (rows.hasNext()) {
      var r = rows.next();
      terms.push({
        query:   r['Query'],
        camp:    r['CampaignName'],
        impr:    parseInt(r['Impressions'].replace(/,/g, '')) || 0,
        clicks:  parseInt(r['Clicks'].replace(/,/g, '')) || 0,
        cost:    parseFloat(r['Cost'].replace(/,/g, '')) || 0,
        conv:    parseFloat(r['Conversions'].replace(/,/g, '')) || 0
      });
    }

    // Sort by impressions desc
    terms.sort(function(a, b) { return b.impr - a.impr; });

    // Flag negative candidates
    var candidates = [];
    terms.forEach(function(t) {
      var q = t.query.toLowerCase();
      NEGATIVE_SIGNALS.forEach(function(signal) {
        if (q.indexOf(signal) !== -1 && t.conv === 0) {
          candidates.push(t);
        }
      });
    });

    // Dedupe
    var seen = {};
    candidates = candidates.filter(function(t) {
      if (seen[t.query]) return false;
      seen[t.query] = true;
      return true;
    });

    log.push('  Total search terms this week: ' + terms.length);
    log.push('  Negative keyword candidates (matching signals, 0 conv): ' + candidates.length);
    log.push('');

    if (candidates.length > 0) {
      log.push('  TOP CANDIDATES TO ADD AS NEGATIVES:');
      candidates.slice(0, 15).forEach(function(t) {
        log.push('    [' + t.impr + ' impr | ' + t.clicks + ' click | $' + t.cost.toFixed(2) + '] "' + t.query + '"');
      });
      if (candidates.length > 15) {
        log.push('  ... and ' + (candidates.length - 15) + ' more. Review full search term report for complete list.');
      }
      if (candidates.length >= 5) {
        alerts.push(candidates.length + ' new negative keyword candidates found this week. Review Section 4 and add confirmed negatives.');
      }
    } else {
      log.push('  No new negative candidates this week. Existing negatives holding.');
    }

    // Top 10 clean terms (no negative signals, with clicks)
    var clean = terms.filter(function(t) {
      var q = t.query.toLowerCase();
      var flagged = NEGATIVE_SIGNALS.some(function(s) { return q.indexOf(s) !== -1; });
      return !flagged && t.clicks > 0;
    }).slice(0, 10);

    if (clean.length > 0) {
      log.push('');
      log.push('  TOP 10 CLEAN TERMS (good traffic this week):');
      clean.forEach(function(t) {
        log.push('    [' + t.impr + ' impr | ' + t.clicks + ' click | $' + t.cost.toFixed(2) + '] "' + t.query + '"');
      });
    }
  } catch(e) {
    log.push('  ERROR: ' + e.message);
  }
}

// ─── SECTION 5: Anomaly Detection ─────────────────────────────────────────────
function section5_Anomalies(log, alerts) {
  log.push('─── 5. ANOMALY DETECTION ───');

  try {
    var anomalies = [];

    KEEP_CAMPAIGNS.forEach(function(campName) {
      var iter = AdsApp.campaigns()
        .withCondition("Name = '" + campName.replace(/'/g, "\\'") + "'")
        .get();
      if (!iter.hasNext()) return;

      var c   = iter.next();
      var s7  = c.getStatsFor('LAST_7_DAYS');
      var s30 = c.getStatsFor('LAST_30_DAYS');

      var impr7  = s7.getImpressions();
      var cost7  = s7.getCost();
      var cost30 = s30.getCost();
      var avgWeeklySpend = cost30 / 4;

      // Spend spike: this week > 150% of avg weekly
      if (avgWeeklySpend > 0 && cost7 > avgWeeklySpend * 1.5) {
        anomalies.push(campName + ': Spend spike — $' + cost7.toFixed(2) + ' this week vs $' + avgWeeklySpend.toFixed(2) + ' weekly avg (+' + ((cost7/avgWeeklySpend - 1)*100).toFixed(0) + '%)');
      }

      // Spend drop: this week < 50% of avg weekly (but not zero — zero handled separately)
      if (avgWeeklySpend > 0 && cost7 < avgWeeklySpend * 0.5 && cost7 > 0) {
        anomalies.push(campName + ': Spend drop — $' + cost7.toFixed(2) + ' this week vs $' + avgWeeklySpend.toFixed(2) + ' weekly avg. Budget issue or ad disapproval?');
      }

      // Zero impressions
      if (impr7 === 0 && cost30 > 0) {
        anomalies.push(campName + ': ZERO impressions this week despite recent spend history. Investigate immediately.');
      }
    });

    if (anomalies.length > 0) {
      log.push('  ANOMALIES DETECTED:');
      anomalies.forEach(function(a) {
        log.push('  ⚠ ' + a);
        alerts.push(a);
      });
    } else {
      log.push('  No anomalies detected. Campaigns operating within normal range.');
    }

    // Check for any newly active campaigns (not in KEEP list but spending)
    var campIter = AdsApp.campaigns().withCondition('Status = ENABLED').get();
    while (campIter.hasNext()) {
      var c = campIter.next();
      var name = c.getName();
      if (KEEP_CAMPAIGNS.indexOf(name) !== -1) continue;
      var spend7 = c.getStatsFor('LAST_7_DAYS').getCost();
      if (spend7 > 1) {
        var msg = 'Unexpected spend: "' + name + '" is enabled and spent $' + spend7.toFixed(2) + ' this week — not in KEEP list.';
        log.push('  ⚠ ' + msg);
        alerts.push(msg);
      }
    }
  } catch(e) {
    log.push('  ERROR: ' + e.message);
  }
}
