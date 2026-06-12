/**
 * Renova Builders — Growth Diagnostics v1
 * Paste into: Google Ads → Tools & Settings → Bulk Actions → Scripts → + New
 * Authorize → Run
 * Output delivered to: monaempoweryou@gmail.com
 *
 * PURPOSE: Identify device, location, timing, and landing page opportunities.
 * Produces preliminary growth signals and scaling forecast framework.
 *
 * ⚠ CONVERSION DATA CAVEAT:
 * Conversion columns are UNRELIABLE until tracking is fixed.
 * Use CLICKS and CTR as primary performance indicators during transition.
 * Re-run this script 4 weeks after conversion tracking cleanup for clean data.
 *
 * Sections:
 * 1. Device performance breakdown
 * 2. Geographic breakdown (top cities/regions)
 * 3. Ad schedule (day of week + hour of day)
 * 4. Landing page distribution
 * 5. Call signal analysis
 * 6. Growth signals + scaling forecast framework
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';
var DATE_RANGE = 'LAST_30_DAYS';
var ACCOUNT_SPEND_30D = 4688.87;   // from execution package — update if different
var CONFIRMED_PHONE_LEADS_30D = 8; // Phone Website (5) + Phone number button click (3)

function main() {
  var out = [];
  out.push('═══════════════════════════════════════════════════════════');
  out.push('  RENOVA BUILDERS — GROWTH DIAGNOSTICS');
  out.push('═══════════════════════════════════════════════════════════');
  out.push('Generated: ' + new Date().toLocaleString());
  out.push('Period: Last 30 Days');
  out.push('Account: ' + AdsApp.currentAccount().getName() + ' (' + AdsApp.currentAccount().getCustomerId() + ')');
  out.push('');
  out.push('CONVERSION DATA STATUS: UNRELIABLE — tracking polluted until page view actions are demoted.');
  out.push('Impression and click data is clean. Conversion columns are for reference only.');
  out.push('Re-run this script 4 weeks after fixing conversion tracking for clean forecasts.');
  out.push('');

  out = out.concat(section1_DeviceBreakdown());
  out.push('');
  out = out.concat(section2_GeoBreakdown());
  out.push('');
  out = out.concat(section3_AdSchedule());
  out.push('');
  out = out.concat(section4_LandingPages());
  out.push('');
  out = out.concat(section5_CallSignals());
  out.push('');
  out = out.concat(section6_GrowthSignals());

  MailApp.sendEmail(
    EMAIL_RECIPIENT,
    'Renova Growth Diagnostics ' + new Date().toDateString(),
    out.join('\n')
  );
  Logger.log('Growth diagnostics complete. Sent to ' + EMAIL_RECIPIENT);
}

// ─── 1. DEVICE PERFORMANCE BREAKDOWN ──────────────────────────────────────────

function section1_DeviceBreakdown() {
  var lines = ['━━━ 1. DEVICE PERFORMANCE BREAKDOWN ━━━'];
  lines.push('Identifies whether mobile or desktop is driving qualified traffic.');
  lines.push('Home services buyers often research on mobile, convert on desktop.');
  lines.push('');
  try {
    var report = AdsApp.report(
      'SELECT Device, Impressions, Clicks, Ctr, AverageCpc, Cost, Conversions ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS'
    );
    var rows = report.rows();
    var devices = {};
    while (rows.hasNext()) {
      var row = rows.next();
      var d = row['Device'];
      if (!devices[d]) devices[d] = { impr: 0, clicks: 0, cost: 0, conv: 0 };
      devices[d].impr  += parseInt((row['Impressions'] || '0').replace(/,/g,'')) || 0;
      devices[d].clicks += parseInt((row['Clicks']     || '0').replace(/,/g,'')) || 0;
      devices[d].cost  += parseFloat(row['Cost'])        || 0;
      devices[d].conv  += parseFloat(row['Conversions']) || 0;
    }

    var totalClicks = Object.keys(devices).reduce(function(s, k) { return s + devices[k].clicks; }, 0);
    var totalCost   = Object.keys(devices).reduce(function(s, k) { return s + devices[k].cost;   }, 0);

    Object.keys(devices).sort(function(a, b) {
      return devices[b].clicks - devices[a].clicks;
    }).forEach(function(device) {
      var d = devices[device];
      var ctr  = d.impr > 0   ? (d.clicks / d.impr * 100).toFixed(1) : '0.0';
      var cpc  = d.clicks > 0 ? (d.cost / d.clicks).toFixed(2)        : '0.00';
      var pctC = totalClicks > 0 ? (d.clicks / totalClicks * 100).toFixed(0) : '0';
      var pctS = totalCost   > 0 ? (d.cost   / totalCost   * 100).toFixed(0) : '0';
      lines.push('  ' + device);
      lines.push('    Impressions: ' + d.impr.toLocaleString());
      lines.push('    Clicks: ' + d.clicks.toLocaleString() + ' (' + pctC + '% of total)');
      lines.push('    CTR: ' + ctr + '%');
      lines.push('    Avg CPC: $' + cpc);
      lines.push('    Spend: $' + d.cost.toFixed(2) + ' (' + pctS + '% of total)');
      lines.push('');
    });

    // Device insights
    var desktop = devices['DESKTOP'] || { impr: 0, clicks: 0, cost: 0 };
    var mobile  = devices['MOBILE']  || { impr: 0, clicks: 0, cost: 0 };
    if (desktop.impr > 0 && mobile.impr > 0) {
      var desktopCtr = (desktop.clicks / desktop.impr * 100);
      var mobileCtr  = (mobile.clicks  / mobile.impr  * 100);
      var ctrRatio   = desktopCtr > 0 ? (mobileCtr / desktopCtr).toFixed(2) : 'N/A';
      lines.push('DEVICE INSIGHT:');
      lines.push('  Desktop CTR: ' + desktopCtr.toFixed(1) + '% | Mobile CTR: ' + mobileCtr.toFixed(1) + '% | Ratio: ' + ctrRatio + 'x');
      if (mobileCtr < desktopCtr * 0.5) {
        lines.push('  FLAG: Mobile CTR is less than 50% of Desktop CTR.');
        lines.push('  Mobile ad copy or landing page experience may be underperforming.');
        lines.push('  Recommendation: Review mobile ad copy, add mobile call extension, check page load speed on mobile.');
      } else {
        lines.push('  Mobile and desktop CTR are reasonably aligned. No immediate device-level issue detected.');
      }
    }
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 2. GEOGRAPHIC BREAKDOWN ──────────────────────────────────────────────────

function section2_GeoBreakdown() {
  var lines = ['━━━ 2. GEOGRAPHIC BREAKDOWN — Top Locations ━━━'];
  lines.push('Identifies which cities and regions are generating traffic.');
  lines.push('Renova serves Bay Area. Non-Bay Area impressions = geo targeting leak = wasted spend.');
  lines.push('');
  try {
    var report = AdsApp.report(
      'SELECT CityName, RegionName, Impressions, Clicks, Ctr, AverageCpc, Cost, Conversions ' +
      'FROM GEO_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS ' +
      'LIMIT 0,200'
    );
    var rows = report.rows();
    var geos = [];
    while (rows.hasNext()) {
      var row = rows.next();
      var impr   = parseInt((row['Impressions'] || '0').replace(/,/g,'')) || 0;
      var clicks = parseInt((row['Clicks']      || '0').replace(/,/g,'')) || 0;
      var cost   = parseFloat(row['Cost']) || 0;
      geos.push({
        city:   row['CityName']   || 'Unknown',
        region: row['RegionName'] || 'Unknown',
        impr: impr, clicks: clicks, cost: cost,
        ctr:  impr > 0   ? (clicks / impr * 100).toFixed(1)  : '0.0',
        cpc:  clicks > 0 ? (cost   / clicks).toFixed(2)       : '0.00'
      });
    }
    geos.sort(function(a, b) { return b.clicks - a.clicks; });

    var bayAreaKeywords = [
      'san francisco', 'oakland', 'san jose', 'berkeley', 'fremont',
      'hayward', 'concord', 'walnut creek', 'pleasanton', 'livermore',
      'dublin', 'san ramon', 'danville', 'orinda', 'lafayette',
      'palo alto', 'mountain view', 'sunnyvale', 'santa clara', 'san mateo',
      'redwood city', 'milpitas', 'saratoga', 'los altos', 'los gatos',
      'cupertino', 'campbell', 'marin', 'novato', 'san rafael',
      'daly city', 'south san francisco', 'burlingame', 'castro valley',
      'union city', 'newark', 'alameda', 'emeryville', 'richmond',
      'el cerrito', 'san leandro', 'napa', 'vallejo', 'petaluma',
      'california'
    ];
    function isBayArea(geo) {
      var combined = (geo.city + ' ' + geo.region).toLowerCase();
      for (var i = 0; i < bayAreaKeywords.length; i++) {
        if (combined.indexOf(bayAreaKeywords[i]) !== -1) return true;
      }
      return false;
    }

    var bayArea = [], outside = [];
    geos.forEach(function(g) {
      if (isBayArea(g)) bayArea.push(g); else outside.push(g);
    });

    var bayClicks    = bayArea.reduce(function(s, g) { return s + g.clicks; }, 0);
    var outsideClicks = outside.reduce(function(s, g) { return s + g.clicks; }, 0);
    var baySpend     = bayArea.reduce(function(s, g) { return s + g.cost; }, 0);
    var outsideSpend = outside.reduce(function(s, g) { return s + g.cost; }, 0);

    lines.push('TOP BAY AREA LOCATIONS (top 20 by clicks):');
    bayArea.slice(0, 20).forEach(function(g) {
      lines.push('  ' + g.city + ', ' + g.region + ' — ' + g.clicks + ' clicks | ' + g.impr + ' impr | CTR ' + g.ctr + '% | $' + g.cpc + ' CPC | $' + g.cost.toFixed(2) + ' spend');
    });

    lines.push('');
    lines.push('BAY AREA total: ' + bayClicks + ' clicks | $' + baySpend.toFixed(2) + ' spend');
    lines.push('');

    if (outside.length > 0) {
      lines.push('OUTSIDE SERVICE AREA (potential geo targeting leak):');
      outside.slice(0, 15).forEach(function(g) {
        lines.push('  !! ' + g.city + ', ' + g.region + ' — ' + g.clicks + ' clicks | $' + g.cost.toFixed(2) + ' spend');
      });
      lines.push('');
      lines.push('Out-of-area total: ' + outsideClicks + ' clicks | $' + outsideSpend.toFixed(2) + ' spend');
      if (outsideSpend > 100) {
        lines.push('FLAG: $' + outsideSpend.toFixed(2) + ' spent outside service area — requires geo targeting review.');
        lines.push('Recommendation: Verify campaign geo targets are set to Bay Area only, not "presence or interest".');
        lines.push('Change geo targeting option to "Presence: People in or regularly in your targeted locations".');
        lines.push('AUTHORIZED: Geo targeting corrections do not require budget approval.');
      }
    } else {
      lines.push('No out-of-area traffic detected. Geo targeting appears correctly configured.');
    }
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 3. AD SCHEDULE — DAY + HOUR ──────────────────────────────────────────────

function section3_AdSchedule() {
  var lines = ['━━━ 3. AD SCHEDULE ANALYSIS ━━━'];
  lines.push('Shows when buyers are searching. Identifies peak periods for bid adjustments.');
  lines.push('');
  try {
    // Day of week
    var dowReport = AdsApp.report(
      'SELECT DayOfWeek, Impressions, Clicks, Ctr, AverageCpc, Cost ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS'
    );
    var dow = {};
    var dowRows = dowReport.rows();
    while (dowRows.hasNext()) {
      var row = dowRows.next();
      var day = row['DayOfWeek'];
      if (!dow[day]) dow[day] = { impr: 0, clicks: 0, cost: 0 };
      dow[day].impr   += parseInt((row['Impressions'] || '0').replace(/,/g,'')) || 0;
      dow[day].clicks += parseInt((row['Clicks']      || '0').replace(/,/g,'')) || 0;
      dow[day].cost   += parseFloat(row['Cost']) || 0;
    }

    var dayOrder = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY'];
    lines.push('DAY OF WEEK:');
    lines.push('  Day       | Clicks | Spend   | CTR  | Avg CPC');
    dayOrder.forEach(function(day) {
      var d = dow[day] || { impr: 0, clicks: 0, cost: 0 };
      var ctr = d.impr > 0   ? (d.clicks / d.impr * 100).toFixed(1) : '0.0';
      var cpc = d.clicks > 0 ? (d.cost   / d.clicks).toFixed(2)      : '0.00';
      lines.push('  ' + day.substring(0, 3) + '       | ' + d.clicks + '   | $' + d.cost.toFixed(2) + ' | ' + ctr + '% | $' + cpc);
    });

    // Hour of day
    var hourReport = AdsApp.report(
      'SELECT HourOfDay, Impressions, Clicks, Ctr, AverageCpc, Cost ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'DURING LAST_30_DAYS'
    );
    var hours = {};
    var hourRows = hourReport.rows();
    while (hourRows.hasNext()) {
      var row2 = hourRows.next();
      var hour = parseInt(row2['HourOfDay']) || 0;
      if (!hours[hour]) hours[hour] = { impr: 0, clicks: 0, cost: 0 };
      hours[hour].impr   += parseInt((row2['Impressions'] || '0').replace(/,/g,'')) || 0;
      hours[hour].clicks += parseInt((row2['Clicks']      || '0').replace(/,/g,'')) || 0;
      hours[hour].cost   += parseFloat(row2['Cost']) || 0;
    }

    lines.push('');
    lines.push('HOUR OF DAY (Pacific Time):');
    var peakHours = [];
    var avgClicks = 0;
    var hourKeys = Object.keys(hours).map(Number);
    hourKeys.forEach(function(h) { avgClicks += hours[h].clicks; });
    avgClicks = avgClicks / 24;

    hourKeys.sort(function(a, b) { return a - b; }).forEach(function(hour) {
      var h = hours[hour] || { impr: 0, clicks: 0, cost: 0 };
      var label = hour < 10 ? '0' + hour : '' + hour;
      var ampm  = hour < 12 ? 'AM' : 'PM';
      var displayHour = hour === 0 ? 12 : (hour > 12 ? hour - 12 : hour);
      var ctr  = h.impr > 0   ? (h.clicks / h.impr * 100).toFixed(1) : '0.0';
      var cpc  = h.clicks > 0 ? (h.cost   / h.clicks).toFixed(2)      : '0.00';
      var peak = h.clicks > avgClicks * 1.3 ? ' ← PEAK' : '';
      if (h.clicks > avgClicks * 1.3) peakHours.push(displayHour + ampm);
      lines.push('  ' + displayHour + ampm + ' | ' + h.clicks + ' clicks | $' + h.cost.toFixed(2) + ' | CTR ' + ctr + '%' + peak);
    });

    lines.push('');
    if (peakHours.length > 0) {
      lines.push('PEAK SEARCH HOURS (30%+ above average): ' + peakHours.join(', '));
      lines.push('Recommendation: These are the highest-intent search windows. Ensure budget is not exhausted before these hours.');
    }
    lines.push('');
    lines.push('SCHEDULING OPPORTUNITY: If budget is limited, concentrate it on peak hours/days.');
    lines.push('Requires approval: ad schedule bid adjustments are a bid-level change.');

  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 4. LANDING PAGE DISTRIBUTION ─────────────────────────────────────────────

function section4_LandingPages() {
  var lines = ['━━━ 4. LANDING PAGE DISTRIBUTION ━━━'];
  lines.push('Shows which pages are receiving ad traffic.');
  lines.push('Concentrated traffic to one page = opportunity (optimize that page) + risk (single point of failure).');
  lines.push('');
  try {
    var report = AdsApp.report(
      'SELECT FinalUrl, Impressions, Clicks, Ctr, AverageCpc, Cost ' +
      'FROM URL_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS ' +
      'LIMIT 0,100'
    );
    var rows = report.rows();
    var pages = [];
    while (rows.hasNext()) {
      var row = rows.next();
      var clicks = parseInt((row['Clicks'] || '0').replace(/,/g,'')) || 0;
      var impr   = parseInt((row['Impressions'] || '0').replace(/,/g,'')) || 0;
      var cost   = parseFloat(row['Cost']) || 0;
      pages.push({
        url: row['FinalUrl'],
        impr: impr, clicks: clicks, cost: cost,
        ctr: impr > 0   ? (clicks / impr * 100).toFixed(1) : '0.0',
        cpc: clicks > 0 ? (cost   / clicks).toFixed(2)      : '0.00'
      });
    }
    pages.sort(function(a, b) { return b.clicks - a.clicks; });

    var totalClicks = pages.reduce(function(s, p) { return s + p.clicks; }, 0);

    if (pages.length === 0) {
      lines.push('No URL performance data returned. Final URLs may not be tracked or report unavailable.');
    } else {
      lines.push('Landing pages receiving traffic (top 20):');
      lines.push('');
      pages.slice(0, 20).forEach(function(p, i) {
        var pct = totalClicks > 0 ? (p.clicks / totalClicks * 100).toFixed(0) : '0';
        lines.push('  ' + (i + 1) + '. ' + p.url);
        lines.push('     Clicks: ' + p.clicks + ' (' + pct + '% of total) | CTR: ' + p.ctr + '% | CPC: $' + p.cpc + ' | Spend: $' + p.cost.toFixed(2));
      });

      lines.push('');
      if (pages.length > 0 && pages[0].clicks / totalClicks > 0.7) {
        lines.push('FLAG: ' + Math.round(pages[0].clicks / totalClicks * 100) + '% of all clicks going to one landing page.');
        lines.push('  → If this is the home page: consider creating service-specific landing pages.');
        lines.push('    Kitchen remodel searches should land on a kitchen-specific page, not the home page.');
        lines.push('    Relevant landing pages typically 2-3x the conversion rate of generic pages.');
        lines.push('  AUTHORIZED: Landing page review and copy recommendations do not require budget approval.');
      }
    }
  } catch(e) {
    lines.push('ERROR: ' + e.message);
  }
  return lines;
}

// ─── 5. CALL SIGNAL ANALYSIS ──────────────────────────────────────────────────

function section5_CallSignals() {
  var lines = ['━━━ 5. CALL SIGNAL ANALYSIS ━━━'];
  lines.push('Phone calls are currently the only verified real lead signal in the account.');
  lines.push('8 phone signals confirmed (30d): Phone Website (5) + Phone number button click (3).');
  lines.push('');

  try {
    // Call extension performance
    var report = AdsApp.report(
      'SELECT CampaignName, PhoneCallDuration, PhoneImpressions, PhoneCalls, PhoneThroughRate ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'WHERE PhoneImpressions > 0 ' +
      'DURING LAST_30_DAYS ' +
      'LIMIT 0,50'
    );
    var rows = report.rows();
    var calls = [];
    var hasCalls = false;
    while (rows.hasNext()) {
      var row = rows.next();
      var phoneCalls = parseInt((row['PhoneCalls'] || '0').replace(/,/g,'')) || 0;
      var phoneImpr  = parseInt((row['PhoneImpressions'] || '0').replace(/,/g,'')) || 0;
      if (phoneImpr > 0) {
        hasCalls = true;
        calls.push({
          campaign:    row['CampaignName'],
          calls:       phoneCalls,
          impressions: phoneImpr,
          ctr:         phoneImpr > 0 ? (phoneCalls / phoneImpr * 100).toFixed(2) : '0.00',
          avgDuration: row['PhoneCallDuration'] || 'N/A'
        });
      }
    }

    if (!hasCalls) {
      lines.push('No call extension impression data returned from report.');
      lines.push('This may mean call extensions are not set up on all campaigns, or data is in a different report.');
    } else {
      lines.push('Call extension performance by campaign:');
      calls.sort(function(a, b) { return b.calls - a.calls; });
      calls.forEach(function(c) {
        lines.push('  Campaign: ' + c.campaign);
        lines.push('  Phone impressions: ' + c.impressions + ' | Calls: ' + c.calls + ' | Call-through rate: ' + c.ctr + '%');
        if (c.avgDuration !== 'N/A') lines.push('  Avg call duration: ' + c.avgDuration + ' seconds');
        lines.push('');
      });
    }

  } catch(e) {
    lines.push('Call extension report error: ' + e.message);
    lines.push('This report requires call extensions to be active on campaigns.');
  }

  lines.push('CALL TRACKING RECOMMENDATIONS:');
  lines.push('  1. Verify Google call forwarding number is active on all ads');
  lines.push('  2. Confirm minimum call duration threshold is set (recommend 60 seconds)');
  lines.push('     → Conversions > call action > Edit > set minimum call duration to 60s');
  lines.push('     → Calls under 60s are likely wrong numbers, not qualified leads');
  lines.push('  3. Install call tracking on the Renova website directly (e.g., CallRail or Google Tag)');
  lines.push('     → This will capture calls from both ads AND organic traffic');
  lines.push('  AUTHORIZED: Call duration threshold changes do not affect spend.');

  return lines;
}

// ─── 6. GROWTH SIGNALS + SCALING FORECAST ─────────────────────────────────────

function section6_GrowthSignals() {
  var lines = ['━━━ 6. GROWTH SIGNALS + SCALING FORECAST FRAMEWORK ━━━'];
  lines.push('');
  lines.push('Current account snapshot (30 days, from confirmed data):');

  try {
    // Pull fresh account totals
    var report = AdsApp.report(
      'SELECT Impressions, Clicks, Ctr, AverageCpc, Cost, SearchImpressionShare, ' +
      'SearchBudgetLostImpressionShare, SearchRankLostImpressionShare ' +
      'FROM CAMPAIGN_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING LAST_30_DAYS'
    );
    var rows = report.rows();
    var totals = { impr: 0, clicks: 0, cost: 0, isData: [] };
    while (rows.hasNext()) {
      var row = rows.next();
      totals.impr   += parseInt((row['Impressions'] || '0').replace(/,/g,'')) || 0;
      totals.clicks += parseInt((row['Clicks']      || '0').replace(/,/g,'')) || 0;
      totals.cost   += parseFloat(row['Cost']) || 0;
      var is = parseFloat(row['SearchImpressionShare']) || 0;
      var budgetLost = parseFloat(row['SearchBudgetLostImpressionShare']) || 0;
      var rankLost   = parseFloat(row['SearchRankLostImpressionShare'])   || 0;
      if (is > 0) {
        totals.isData.push({
          is: is, budgetLost: budgetLost, rankLost: rankLost,
          cost: parseFloat(row['Cost']) || 0
        });
      }
    }

    var avgCpc          = totals.clicks > 0 ? totals.cost / totals.clicks : 0;
    var confirmedLeads  = CONFIRMED_PHONE_LEADS_30D;
    var cplConfirmed    = confirmedLeads > 0 ? totals.cost / confirmedLeads : 0;
    var clickToLeadRate = totals.clicks > 0 ? (confirmedLeads / totals.clicks * 100) : 0;

    lines.push('  Total impressions (30d): ' + totals.impr.toLocaleString());
    lines.push('  Total clicks (30d): ' + totals.clicks.toLocaleString());
    lines.push('  Total spend (30d): $' + totals.cost.toFixed(2));
    lines.push('  Average CPC: $' + avgCpc.toFixed(2));
    lines.push('');
    lines.push('  Confirmed real phone leads (30d): ' + confirmedLeads);
    lines.push('  Current CPL (phone leads only): $' + cplConfirmed.toFixed(0));
    lines.push('  Current click-to-lead rate: ' + clickToLeadRate.toFixed(2) + '%');
    lines.push('  Industry benchmark for home services: 1.0% - 3.0% click-to-lead');
    lines.push('');

    if (clickToLeadRate < 0.5) {
      lines.push('FLAG: Click-to-lead rate is critically low (' + clickToLeadRate.toFixed(2) + '%).');
      lines.push('Possible causes (in priority order):');
      lines.push('  1. Call tracking is undercounting leads (form submits not tracked, calls not captured)');
      lines.push('  2. Landing page is not converting visitors into contacts');
      lines.push('  3. Traffic quality is poor (broad match + wrong intent)');
      lines.push('  4. Phone number is not prominently displayed on mobile');
      lines.push('');
    }

    // Impression share analysis
    if (totals.isData.length > 0) {
      var avgIS          = totals.isData.reduce(function(s, d) { return s + d.is; }, 0) / totals.isData.length;
      var avgBudgetLost  = totals.isData.reduce(function(s, d) { return s + d.budgetLost; }, 0) / totals.isData.length;
      var avgRankLost    = totals.isData.reduce(function(s, d) { return s + d.rankLost; }, 0) / totals.isData.length;
      lines.push('IMPRESSION SHARE (active campaigns avg):');
      lines.push('  Current IS: ' + (avgIS * 100).toFixed(0) + '%');
      lines.push('  Lost to budget: ' + (avgBudgetLost * 100).toFixed(0) + '%');
      lines.push('  Lost to rank: ' + (avgRankLost * 100).toFixed(0) + '%');
      lines.push('');
      if (avgBudgetLost > 0.2) {
        lines.push('  BUDGET LIMIT SIGNAL: ' + (avgBudgetLost * 100).toFixed(0) + '% of impressions lost to budget cap.');
        lines.push('  This means increasing budget would directly capture more market share.');
        lines.push('  Impressions available at current CPC: ' + Math.round(totals.impr / (1 - avgBudgetLost)).toLocaleString() + ' (vs current ' + totals.impr.toLocaleString() + ')');
      }
      if (avgRankLost > 0.3) {
        lines.push('  RANK SIGNAL: ' + (avgRankLost * 100).toFixed(0) + '% of impressions lost to ad rank.');
        lines.push('  Ad rank is driven by bid × Quality Score. Improving ad relevance can recover this without spending more.');
      }
    }

    lines.push('');
    lines.push('━━━ SCALING FORECAST (preliminary — update after tracking is clean) ━━━');
    lines.push('');
    lines.push('IMPORTANT: These forecasts use confirmed phone leads only (8/month).');
    lines.push('True lead volume is likely higher once form submissions are properly tracked.');
    lines.push('Re-run this script after 4 weeks of clean data for validated forecasts.');
    lines.push('');

    // Scenario modeling
    var scenarios = [
      { label: 'Current state (baseline)', spend: totals.cost, ctr: clickToLeadRate, note: 'Conversion tracking polluted — actual rate unknown' },
      { label: 'After tracking fix only (est)', spend: totals.cost, ctr: clickToLeadRate * 3, note: 'Est. 3x improvement as form submits become visible' },
      { label: 'After tracking + negatives (est)', spend: totals.cost * 0.95, ctr: clickToLeadRate * 3.5, note: 'Minor spend reduction from cleaner traffic' },
      { label: '+50% spend (est, post-fix)', spend: totals.cost * 1.5, ctr: clickToLeadRate * 3.5, note: 'Budget increase after foundation is clean' },
      { label: '+100% spend (est, post-fix)', spend: totals.cost * 2.0, ctr: clickToLeadRate * 3.5, note: 'Scale scenario — requires IS data to validate capacity' },
    ];

    scenarios.forEach(function(s) {
      var estLeads = s.ctr > 0 ? Math.round(totals.clicks * (s.spend / totals.cost) * (s.ctr / 100)) : confirmedLeads;
      var estCpl   = estLeads > 0 ? s.spend / estLeads : 0;
      lines.push('  Scenario: ' + s.label);
      lines.push('  Monthly spend: $' + s.spend.toFixed(0));
      lines.push('  Est. leads/month: ' + estLeads);
      lines.push('  Est. CPL: $' + estCpl.toFixed(0));
      lines.push('  Note: ' + s.note);
      lines.push('');
    });

    lines.push('REVENUE CONTEXT (for Renova to validate):');
    lines.push('  Typical close rate for home remodeling: 20-35%');
    lines.push('  Typical project value (bathroom): $15,000 - $40,000');
    lines.push('  Typical project value (kitchen): $25,000 - $75,000');
    lines.push('  Typical project value (full home remodel): $100,000+');
    lines.push('  At 30 leads/month × 25% close rate = 7-8 projects/month');
    lines.push('  At $20,000 avg project value = $140,000-160,000 monthly revenue from PPC alone');
    lines.push('');
    lines.push('  !! This is the growth model. The account has the volume.');
    lines.push('  The problem is measurement and optimization, not market demand.');
    lines.push('  Fix measurement. Fix targeting. The revenue follows.');

  } catch(e) {
    lines.push('ERROR in growth signals: ' + e.message);
  }

  lines.push('');
  lines.push('━━━ HIGHEST-OPPORTUNITY SERVICE LINES ━━━');
  lines.push('Based on search term data and campaign structure. To be validated with clean conversion data.');
  lines.push('');
  lines.push('  1. BATHROOM REMODEL — highest campaign investment ($130/day allocated across 3 campaigns)');
  lines.push('     Status: Active traffic in "Leads Service base--13". Dedicated campaigns need structural repair.');
  lines.push('     Search volume: Confirmed. "bathroom remodel", "walk in shower", "bathroom renovation" all present.');
  lines.push('     Opportunity: Dedicated bathroom campaign with proper ads + relevant landing page.');
  lines.push('');
  lines.push('  2. KITCHEN REMODEL — second highest investment ($55-140/day across 3 campaigns)');
  lines.push('     Status: Kitchen Search campaign (REVIEW) — structure intact, not serving.');
  lines.push('     Search volume: Confirmed. "kitchen remodel", "kitchen renovation" in active search terms.');
  lines.push('     Opportunity: Diagnose why Kitchen Search campaign has 0 impressions and repair.');
  lines.push('');
  lines.push('  3. FULL HOME REMODEL — "full home remodel" campaign is KEEP, generating spend');
  lines.push('     Status: Active at $65.39/day. MAXIMIZE_CONVERSIONS on polluted data.');
  lines.push('     Opportunity: Post-tracking-fix, this campaign should retrain and improve CPL.');
  lines.push('');
  lines.push('  4. ADUs / ADDITIONS — not confirmed in current campaign structure');
  lines.push('     Opportunity: High-value service with less competition. Consider after foundation is clean.');
  lines.push('');
  lines.push('  5. OUTDOOR / DECK / PATIO — campaigns paused (all ad groups off)');
  lines.push('     Status: Requires Maor approval to evaluate revival.');
  lines.push('     Note: "Outdoor Kitchen" and "Deck Patio Pavers" campaigns exist but are dead.');

  lines.push('');
  lines.push('━━━ NEXT STEPS WHEN TRACKING IS CLEAN ━━━');
  lines.push('  Week 4 (post-fix): Run this script again. The CPL number will tell you everything.');
  lines.push('  If CPL < $300: Scale aggressively. Increase budget to saturation point.');
  lines.push('  If CPL $300-600: Optimize before scaling. Fix landing page, improve ad copy.');
  lines.push('  If CPL > $600: Structural problem. Investigate landing page + call tracking first.');

  return lines;
}
