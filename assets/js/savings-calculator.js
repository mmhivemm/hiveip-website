/* Savings calculator — printing cost only.
   Compares Hive IP in-factory printing against the legacy packaging-supplier
   route. Hive IP bills on the codes covered by an active promotional campaign;
   every pack produced can carry a code at no extra cost.

   Internal pricing constants below are used only to compute the percentage
   saving rendered to the user. They are not displayed and are kept here as
   anonymous numeric values rather than commented rate cards.

   Legacy comparator: midpoint of the publicly-known £3,000–£5,000/m range
   for packaging-supplier printing — industry knowledge, fine to use as the
   reference point.
*/
(function () {
  'use strict';

  // Internal pricing constants (not displayed)
  var BASE_RATE     = 900;     // per million, for the first BASE_LIMIT millions of any campaign
  var BASE_LIMIT    = 20;      // millions
  var DECAY_FACTOR  = 0.95;    // each additional million is this proportion of the previous
  var LEGACY_RATE   = 4000;    // per million, industry midpoint comparator

  function $(sel) { return document.querySelector(sel); }

  var els = {
    campaigns:    $('#calc-campaigns'),
    campaignSize: $('#calc-campaign-size'),
    savingsPct:   $('#calc-savings-pct')
  };
  if (!els.campaigns || !els.campaignSize || !els.savingsPct) return;

  /* Hive cost for a given total volume (millions) of codes covered by
     campaigns across the year. Discount compounds across the full year's
     volume — additional campaigns extend the same curve rather than
     resetting it.
       - First BASE_LIMIT millions are flat at BASE_RATE per million.
       - The (BASE_LIMIT+1)th million costs BASE_RATE * DECAY_FACTOR.
       - The (BASE_LIMIT+2)th million costs the previous rate * DECAY_FACTOR.
       - Etc. (geometric decay)
       - Fractional partial millions are charged proportionally at the next-step rate.
  */
  function hiveCostForVolume(totalM) {
    if (totalM <= 0) return 0;
    if (totalM <= BASE_LIMIT) return totalM * BASE_RATE;

    var cost      = BASE_LIMIT * BASE_RATE;
    var remaining = totalM - BASE_LIMIT;
    var rate      = BASE_RATE;

    while (remaining >= 1) {
      rate = rate * DECAY_FACTOR;
      cost += rate;
      remaining -= 1;
    }
    if (remaining > 0) {
      rate = rate * DECAY_FACTOR;
      cost += rate * remaining;
    }
    return cost;
  }

  function update() {
    var campaigns = Math.max(0, parseInt(els.campaigns.value, 10) || 0);
    var sizeM     = Math.max(0, parseFloat(els.campaignSize.value) || 0);

    // Apply the compound discount across the year's total covered volume,
    // not per individual campaign — running more campaigns at the same size
    // pushes further down the decay curve.
    var totalCoveredM = campaigns * sizeM;
    var legacyTotal   = totalCoveredM * LEGACY_RATE;
    var hiveTotal     = hiveCostForVolume(totalCoveredM);

    var pct = 0;
    if (legacyTotal > 0) {
      pct = ((legacyTotal - hiveTotal) / legacyTotal) * 100;
    }
    els.savingsPct.textContent = Math.round(pct) + '%';
  }

  ['input', 'change'].forEach(function (evt) {
    [els.campaigns, els.campaignSize].forEach(function (el) {
      el.addEventListener(evt, update);
    });
  });

  update();
})();
