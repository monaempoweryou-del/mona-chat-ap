/**
 * Renova Builders — Google Ads Full Account Audit Script
 * Paste into: Google Ads → Tools & Settings → Bulk Actions → Scripts → + New
 * Authorize → Run
 * Results delivered to: monaempoweryou@gmail.com
 */

var EMAIL_RECIPIENT = 'monaempoweryou@gmail.com';
var DATE_RANGE = 'LAST_90_DAYS';
var CLIENT_NAME = 'Renova Builders';

function main() {
  var report = [];
  report.push('=== ' + CLIENT_NAME + ' — FULL PPC AUDIT ===');
  report.push('Date range: Last 90 days');
  report.push('Generated: ' + new Date().toLocaleString());
  report.push('');

  report = report.concat(getAccountSummary());
  report.push('');
  report = report.concat(getCampaignData());
  report.push('');
  report = report.concat(getKeywordData());
  report.push('');
  report = report.concat(getSearchTermData());
  report.push('');
  report = report.concat(getAdData());
  report.push('');
  report = report.concat(getConversionData());
  report.push('');
  report = report.concat(getAuditFlags());

  var body = report.join('\n');
  MailApp.sendEmail(EMAIL_RECIPIENT, CLIENT_NAME + ' — Full PPC Audit (' + new Date().toDateString() + ')', body);
  Logger.log('Audit complete. Report sent to ' + EMAIL_RECIPIENT);
}

function getAccountSummary() {
  var lines = ['--- ACCOUNT SUMMARY ---'];
  try {
    var stats = AdsApp.currentAccount().getStatsFor(DATE_RANGE);
    lines.push('Account name: ' + AdsApp.currentAccount().getName());
    lines.push('Customer ID:  ' + AdsApp.currentAccount().getCustomerId());
    lines.push('Currency:     ' + AdsApp.currentAccount().getCurrencyCode());
    lines.push('');
    lines.push('Impressions:  ' + stats.getImpressions());
    lines.push('Clicks:       ' + stats.getClicks());
    lines.push('CTR:          ' + (stats.getCtr() * 100).toFixed(2) + '%');
    lines.push('Avg CPC:      $' + stats.getAverageCpc().toFixed(2));
    lines.push('Total spend:  $' + stats.getCost().toFixed(2));
    lines.push('Conversions:  ' + stats.getConversions());
    var cpa = stats.getConversions() > 0 ? (stats.getCost() / stats.getConversions()).toFixed(2) : 'N/A';
    lines.push('Cost/Conv:    $' + cpa);
    lines.push('Conv rate:    ' + (stats.getConversionRate() * 100).toFixed(2) + '%');
  } catch(e) {
    lines.push('ERROR reading account summary: ' + e.message);
  }
  return lines;
}

function getCampaignData() {
  var lines = ['--- CAMPAIGNS ---'];
  try {
    var campaigns = AdsApp.campaigns().get();
    var count = 0;
    while (campaigns.hasNext()) {
      var c = campaigns.next();
      var stats = c.getStatsFor(DATE_RANGE);
      var budget = c.getBudget();
      count++;
      lines.push('');
      lines.push('Campaign: ' + c.getName());
      lines.push('  Status:       ' + c.isEnabled() ? 'ENABLED' : (c.isPaused() ? 'PAUSED' : 'REMOVED'));
      lines.push('  Type:         ' + c.getAdvertisingChannelType());
      lines.push('  Daily budget: $' + budget.getAmount().toFixed(2));
      lines.push('  Impressions:  ' + stats.getImpressions());
      lines.push('  Clicks:       ' + stats.getClicks());
      lines.push('  CTR:          ' + (stats.getCtr() * 100).toFixed(2) + '%');
      lines.push('  Avg CPC:      $' + stats.getAverageCpc().toFixed(2));
      lines.push('  Spend:        $' + stats.getCost().toFixed(2));
      lines.push('  Conversions:  ' + stats.getConversions());
      var cpa = stats.getConversions() > 0 ? '$' + (stats.getCost() / stats.getConversions()).toFixed(2) : 'N/A';
      lines.push('  Cost/Conv:    ' + cpa);
    }
    if (count === 0) lines.push('No campaigns found.');
    lines.push('');
    lines.push('Total campaigns: ' + count);
  } catch(e) {
    lines.push('ERROR reading campaigns: ' + e.message);
  }
  return lines;
}

function getKeywordData() {
  var lines = ['--- KEYWORDS (top 50 by spend) ---'];
  try {
    var keywords = AdsApp.keywords()
      .orderBy('Cost DESC')
      .withLimit(50)
      .get();

    var count = 0;
    while (keywords.hasNext()) {
      var kw = keywords.next();
      var stats = kw.getStatsFor(DATE_RANGE);
      count++;
      var qs = 'N/A';
      try { qs = kw.getQualityScore(); } catch(e) {}
      lines.push('');
      lines.push('Keyword: [' + kw.getMatchType() + '] ' + kw.getText());
      lines.push('  Campaign:    ' + kw.getCampaign().getName());
      lines.push('  Ad Group:    ' + kw.getAdGroup().getName());
      lines.push('  Status:      ' + (kw.isEnabled() ? 'ENABLED' : 'PAUSED'));
      lines.push('  Quality Score: ' + qs);
      lines.push('  Impressions: ' + stats.getImpressions());
      lines.push('  Clicks:      ' + stats.getClicks());
      lines.push('  CTR:         ' + (stats.getCtr() * 100).toFixed(2) + '%');
      lines.push('  Avg CPC:     $' + stats.getAverageCpc().toFixed(2));
      lines.push('  Spend:       $' + stats.getCost().toFixed(2));
      lines.push('  Conversions: ' + stats.getConversions());
    }
    if (count === 0) lines.push('No keywords found.');
    lines.push('');
    lines.push('Keywords shown: ' + count);
  } catch(e) {
    lines.push('ERROR reading keywords: ' + e.message);
  }
  return lines;
}

function getSearchTermData() {
  var lines = ['--- SEARCH TERMS (top 50 by impressions) ---'];
  try {
    var report = AdsApp.report(
      'SELECT Query, Impressions, Clicks, Ctr, AverageCpc, Cost, Conversions, ConversionRate ' +
      'FROM SEARCH_QUERY_PERFORMANCE_REPORT ' +
      'WHERE Impressions > 0 ' +
      'DURING ' + DATE_RANGE + ' ' +
      'ORDER BY Impressions DESC ' +
      'LIMIT 50'
    );
    var rows = report.rows();
    var count = 0;
    while (rows.hasNext()) {
      var row = rows.next();
      count++;
      lines.push(
        row['Query'] + ' | ' +
        'Impr: ' + row['Impressions'] + ' | ' +
        'Clicks: ' + row['Clicks'] + ' | ' +
        'CTR: ' + (parseFloat(row['Ctr']) * 100).toFixed(1) + '% | ' +
        'CPC: $' + parseFloat(row['AverageCpc']).toFixed(2) + ' | ' +
        'Cost: $' + parseFloat(row['Cost']).toFixed(2) + ' | ' +
        'Conv: ' + row['Conversions']
      );
    }
    if (count === 0) lines.push('No search terms found.');
    lines.push('');
    lines.push('Search terms shown: ' + count);
  } catch(e) {
    lines.push('ERROR reading search terms: ' + e.message);
  }
  return lines;
}

function getAdData() {
  var lines = ['--- ADS (top performing by clicks) ---'];
  try {
    var ads = AdsApp.ads()
      .orderBy('Clicks DESC')
      .withLimit(20)
      .get();
    var count = 0;
    while (ads.hasNext()) {
      var ad = ads.next();
      var stats = ad.getStatsFor(DATE_RANGE);
      count++;
      lines.push('');
      lines.push('Ad #' + count + ' — ' + ad.getCampaign().getName() + ' / ' + ad.getAdGroup().getName());
      try {
        var rsa = ad.asResponsiveSearchAd();
        var headlines = rsa.getHeadlines();
        lines.push('  Type: Responsive Search Ad');
        lines.push('  Headlines: ' + headlines.slice(0, 3).map(function(h) { return h.text; }).join(' | '));
      } catch(e) {
        lines.push('  Type: ' + ad.getType());
      }
      lines.push('  Status:      ' + (ad.isEnabled() ? 'ENABLED' : 'PAUSED'));
      lines.push('  Impressions: ' + stats.getImpressions());
      lines.push('  Clicks:      ' + stats.getClicks());
      lines.push('  CTR:         ' + (stats.getCtr() * 100).toFixed(2) + '%');
      lines.push('  Conversions: ' + stats.getConversions());
    }
    if (count === 0) lines.push('No ads found.');
  } catch(e) {
    lines.push('ERROR reading ads: ' + e.message);
  }
  return lines;
}

function getConversionData() {
  var lines = ['--- CONVERSION TRACKING ---'];
  try {
    var convActions = AdsApp.conversionActions().get();
    var count = 0;
    while (convActions.hasNext()) {
      var ca = convActions.next();
      count++;
      lines.push('Action: ' + ca.getName());
      lines.push('  Category: ' + ca.getCategory());
      lines.push('  Status:   ' + ca.isEnabled());
      lines.push('  Count:    ' + ca.getCountingType());
    }
    if (count === 0) {
      lines.push('WARNING: No conversion actions found. Conversion tracking may not be set up.');
      lines.push('This is a critical gap — without conversion tracking, bidding optimization is impossible.');
    }
  } catch(e) {
    lines.push('Conversion action check: ' + e.message);
    lines.push('Manual check required — go to Tools > Conversions in Google Ads.');
  }
  return lines;
}

function getAuditFlags() {
  var lines = ['--- AUDIT FLAGS ---'];
  var flags = [];

  try {
    // Flag 1: No conversions
    var acctStats = AdsApp.currentAccount().getStatsFor(DATE_RANGE);
    if (acctStats.getConversions() === 0) {
      flags.push('CRITICAL: Zero conversions in 90 days. Conversion tracking likely not set up or broken.');
    }

    // Flag 2: High spend, low CTR
    if (acctStats.getCost() > 100 && acctStats.getCtr() < 0.02) {
      flags.push('WARNING: CTR below 2% with significant spend. Ad relevance or targeting issue.');
    }

    // Flag 3: Low quality scores
    var lowQsCount = 0;
    var kwIter = AdsApp.keywords().get();
    while (kwIter.hasNext()) {
      var kw = kwIter.next();
      try {
        var qs = kw.getQualityScore();
        if (qs !== null && qs < 5) lowQsCount++;
      } catch(e) {}
    }
    if (lowQsCount > 0) {
      flags.push('WARNING: ' + lowQsCount + ' keywords with Quality Score below 5. Wasted spend risk.');
    }

    // Flag 4: Broad match with no negatives check
    var broadCount = 0;
    var kwIter2 = AdsApp.keywords().withCondition("KeywordMatchType = BROAD").get();
    while (kwIter2.hasNext()) { kwIter2.next(); broadCount++; }
    if (broadCount > 10) {
      flags.push('WARNING: ' + broadCount + ' broad match keywords. Review search terms for irrelevant traffic.');
    }

    if (flags.length === 0) {
      lines.push('No critical flags detected. Detailed review recommended.');
    } else {
      flags.forEach(function(f) { lines.push(f); });
    }
  } catch(e) {
    lines.push('Could not run automated flags: ' + e.message);
  }

  return lines;
}
