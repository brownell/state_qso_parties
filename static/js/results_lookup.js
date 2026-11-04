// Texas QSO Party Results Lookup - JavaScript
console.log("js has loaded")
document.addEventListener('DOMContentLoaded', function() {
    
    console.log("DOMContentLoaded")
    const yearSelect = document.getElementById('year');
    const callsignInput = document.getElementById('callsign');
    const showIndividualBtn = document.getElementById('showIndividualBtn');
    const showFinalReportBtn = document.getElementById('showFinalReportBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const messageBox = document.getElementById('messageBox');
    const individualResults = document.getElementById('individualResults');
    const finalReport = document.getElementById('finalReport');
    // const statsH3 = document.getElementById('statsH3');

    // Auto-uppercase callsign
    callsignInput.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });

    // Show individual results
    showIndividualBtn.addEventListener('click', async function() {
        year = 2026;
        const callsign = callsignInput.value.trim().toUpperCase();
        // statsH3.innerText = `Score & Statistics for ${year} Texas QSO Party`;
        if (!year) {
            showMessage('Please select a contest year', 'error');
            return;
        }
        if (!callsign) {
            showMessage('Please enter your callsign', 'error');
            return;
        }
        await loadIndividualResults(year, callsign);
    });

    // Show final report
    showFinalReportBtn.addEventListener('click', async function() {
        const year = 2026;

        if (!year) {
            showMessage('Please select a contest year', 'error');
            return;
        }
        await loadFinalReport(year);
    });

    // Load individual results
    async function loadIndividualResults(year, callsign) {
        hideMessage();
        hideResults();
        showLoading();

        try {
            const response = await fetch('/api/individual_results', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    year: 2026,
                    callsign: callsign
                })
            });

            const data = await response.json();
            hideLoading();
            if (data.success) {
                displayIndividualResults(data.result);
                scrollToResults();
            } else {
                showMessage(data.error || 'Results not found', 'error');
            }

        } catch (error) {
            hideLoading();
            showMessage('Error loading results: ' + error.message, 'error');
        }
    }

    // Load final report
    async function loadFinalReport(year) {
        hideMessage();
        hideResults();
        showLoading();

        try {
            const response = await fetch(`/api/final_report/2026.pdf`);
            const data = await response.json();

            hideLoading();

            if (data.success) {
                displayFinalReport(data.html);
                scrollToResults();
            } else {
                showMessage(data.error || 'Final report not found', 'error');
            }

        } catch (error) {
            hideLoading();
            showMessage('Error loading final report: ' + error.message, 'error');
        }
    }

    // Display individual results
    function displayIndividualResults(result) {
        // Generate certificate
        const certificateHTML = generateCertificate(result);
        document.getElementById('certificateContent').innerHTML = certificateHTML;

        // Generate statistics (reuse existing format function from upload.js)
        const statisticsHTML = generateStatisticsHTML(result);
        document.getElementById('statisticsContent').innerHTML = statisticsHTML;
        year = 2026;
        document.getElementById('statsH3').innerHTML = `Your Statistics for ${year} Texas QSO Party`;


        // Show individual results section
        individualResults.style.display = 'block';
        finalReport.style.display = 'none';
    }

    // Display final report
    function displayFinalReport(html) {
        document.getElementById('finalReportContent').innerHTML = html;

        // Show final report section
        finalReport.style.display = 'block';
        individualResults.style.display = 'none';
    }

    // Generate certificate HTML
    function generateCertificate(result) {
// TODO club might be string 'None'

        if (result.category_rank == 1) {
            rank = `FIRST PLACE in Category`
        } else if (result.category_rank == 2) {
            rank = `SECOND PLACE in Category`
        } else if (result.category_rank == 3) {
            rank = `THIRD PLACE in Category`
        } else  if (result.category_rank == '') {
            rank = 'Not calculated'
        } else {
            rank = `Rank in Category: # ${result.category_rank}`
        }

        return `
            <div class="certificate">
                <div class="certificate-header">
                <div class="certificate-title">${result.year} Texas QSO Party</div>
                    <div class="certificate-org">Texas DX Society</div>
                    <div class="certificate-subtitle">Takes DX Society pleasure in awarding this Certificate of Merit to</div>
                </div>

                <div class="certificate-body">
                    <div class="certificate-callsign">${result.callsign}</div>
                    <div class="certificate-name">${result.name || ''}</div>
                    <div class="certificate-club">${result.club|| ''}</div>
                </div>

                <div class="certificate-score">
                    <strong>Final Score: ${result.final_score.toLocaleString()}</strong>
                </div>

                <div class="certificate-rankings">
                    <h2>${result.cat}</h2>
                    <h2>${rank}</h2>
                </div>
                <div class="certificate-footer-container">
                    <div class="certificate-footer">
                        <div class="certificate-signature">
                            <img src="/static/images/signatures.png" class="signature" alt="Signatures">
                        </div>
                        <img src="/static/images/alligator_logo.png" class="certificate-logo" alt="Louisianba QSP Party">
                    </div>

                </div>
            </div>
        `;
    }

    // Generate statistics HTML (adapted from upload.js)
    function generateStatisticsHTML(result) {
        let html = '';

        // Station Information
        html += `<div class="section-sub-header"><h4>Station Information</h4></div>`
        // Data in this sub-section
        html += `<dl class="result-group">`;
        html += `<dt>Callsign:</dt><dd>${result.callsign}</dd>`;
        if (result.name) {
            html += `<dt>Operator Name:</dt><dd>${result.name}</dd>`
        };
        if (result.dxcc_entity && result.dxcc_entity != result.callsign) {
                 html += `<dt>Location:</dt><dd>${result.dxcc_entity}</dd>`
        } else if (result.location) {
            html += `<dt>Location:</dt><dd>${result.location}</dd>`    
        }
        if (result.category_station) {html += `<dt>Station Type:</dt><dd>${result.category_station}</dd>`
        }
        if (result.category_mode) {html += `<dt>Mode:</dt><dd>${result.category_mode}</dd>`
        }
        if (result.category_power) {html += `<dt>Powere:</dt><dd>${result.category_power}</dd>`
        }
        html += `</dl>`

        // Score Summary
        html += `<div class="section-sub-header"><h4>Score Summary</h4></div>`
        // Data in this sub-section
        html += `<dl class="result-group">`;
        
        if (result.final_score) {html += `<dt>Final Score:</dt><dd>${result.final_score.toLocaleString()}</dd>`
        }
        if (result.claimed_score) {html += `<dt>Claimed Score:</dt><dd>${result.claimed_score.toLocaleString()}</dd>`
        }
        if (result.cab_mobile_points > 0) {html += `<dt>County Activation Bonus:</dt><dd>${result.cab_mobile_points.toLocaleString()}</dd>`
        }
        if (result.mtb_mobile_points > 0) {html += `<dt>Mobile Tracking Bonus:</dt><dd>${result.cab_mobile_points.toLocaleString()}</dd>`
        }
        if (result.qso_points > 0) {html += `<dt>Points for QSOs:</dt><dd>${result.qso_points.toLocaleString()}</dd>`
        }
        if (result.total_multipliers> 0) {html += `<dt>Multipliers:</dt><dd>${result.cab_mobile_points.toLocaleString()}</dd>`
        }
        
        html += `</dl>`

        // QSO Statistics
        html += `<div class="section-sub-header"><h4>QSO Statistics</h4></div>`
        html += '<p class="section-sub-header">To see which QSO were not scored, see the section of messages below.</p>'
        // Data in this sub-section
        html += `<dl class="result-group">`;
        
        if (result.total_qsos) {html += `<dt>QSOs in Log File:</dt><dd>${result.total_qsos.toLocaleString()}</dd>`
        }
        if (result.scored_qsos) {html += `<dt>Scored QSOs:</dt><dd>${result.scored_qsos}</dd>`
        }
        if (result.category_station) {html += `<dt>Station Type:</dt><dd>${result.category_station.toLocaleString()}</dd>`
        }
        if (result.cw_qsos) {html += `<dt>CW QSOs:</dt><dd>${result.cw_qsos.toLocaleString()}</dd>`
        }
        if (result.ph_qsos) {html += `<dt>Phone (SSB or FM) QSOs:</dt><dd>${result.ph_qsos.toLocaleString()}</dd>`
        }
        if (result.rt_qsos) {html += `<dt>RTTY QSOs:</dt><dd>${result.rt_qsos.toLocaleString()}</dd>`
        }
        if (result.dg_qsos) {html += `<dt>Other Digital QSOs:</dt><dd>${result.dg_qsos.toLocaleString()}</dd>`
        }
        if (result.uniques) {html += `<dt>Uniques:</dt><dd>${result.uniques.toLocaleString()}</dd>`
        }
        if (result.nils) {html += `<dt>Not In Log (NIL) QSOs:</dt><dd>${result.nils}</dd>`
        }
        if (result.busteds) {html += `<dt>Busted QSOs:</dt><dd>${result.busteds}</dd>`
        }
        if (result.dup_qsos) {html += `<dt>Duplicate QSOs:</dt><dd>${result.dup_qsos}</dd>`
        }
        if (result.invalid_exchange_qso) {html += `<dt>QSOs with Invalid Exchange):</dt><dd>${result.invalid_exchange_qso}</dd>`
        }
        if (result.nils) {html += `<dt>Not In Log (NIL):</dt><dd>${result.nils}</dd>`
        }
        if (result.other_invalid_qsos) {html += `<dt>Other Invalid QSOs:</dt><dd>${result.other_invalid_qsos}</dd>`
        }
        
        html += `</dl>`

        // // Bonuses - leaaving in for future use
        // html += '<div class="result-group">';
        // html += '<h4>Multipliers</h4>';
        // html += '<table class="result-table">';
        // html += '<thead><tr><th>Multiplier Type</th><th>Count</th></tr></thead>';
        // html += '<tbody>';
        // html += `<tr><td>Total Multipliers</td><td>${result.total_multipliers}</td></tr>`;        
        // html += '</tbody></table>';
        // html += '</div>';

        // counties activated for 
        if (result.category_station == 'MOB' && result.counties_activated && result.counties_activated.length > 0) {
            html += renderResultItem('Counties Activated', result.counties_activated.length);
            html += '<div class="result-list">';
            result.counties_activated.forEach(county => {
                html += `<span class="result-list-item">${county}</span>`;
            });
            html += '</div>';
        }
        
        // QSOs by Band
        if (result.qsos_by_band) {
            html += `<div class="section-sub-header"><h4>QSOs by Band</h4></div>`
            html += '<div class="result-group2">';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Band</th><th>Count</th></tr></thead>';
            html += '<tbody>';
            for (const [key, value] of Object.entries(result.qsos_by_band)) {
                // console.log(`by mode  ${key}: ${value}`);
                if (value > 0) {
                    html += `<tr><td>${key}</td><td>${value}</td></tr>`;
                }
            }
            html += '</tbody></table>';
            html += '</div>';
        }

        // QSOs by Mode
        if (result.qsos_by_mode) {
            html += `<div class="section-sub-header"><h4>QSOs by Mode</h4></div>`
            html += '<div class="result-group2">';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Mode</th><th>Count</th></tr></thead>';
            html += '<tbody>';
            for (const [key, value] of Object.entries(result.qsos_by_mode)) {
                console.log(`by mode  ${key}: ${value}`);
                if (value > 0) {
                    html += `<tr><td>${key}</td><td>${value}</td></tr>`;
                }
            }
            html += '</tbody></table>';
            html += '</div>';
        }

        // QSOs by Hour
        if (result.qsos_by_hour) {
            html += `<div class="section-sub-header"><h4>QSOs by Hour</h4></div>`
            html += '<div class="result-group2">';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Hour (1400Z on 9/19 until 0200Z on 9/20 and 1400Z until 2000Z 2/20)</th><th>Count</th></tr></thead>';
            html += '<tbody>';
            for (const [key, value] of Object.entries(result['qsos_by_hour'])) {
                let temp = key;
                if (key > 2400) {
                    temp = key - 2400;
                }
                if (value > 0) {
                    html += `<tr><td>${temp}</td><td>${value}</td></tr>`;
                }
            }
            html += '</tbody></table>';
            html += '</div>';
        }

         // Counties worked (for NON-state stations)
        if (result.counties_worked && result.counties_worked.length > 0) {
            html += renderResultItem('Counties Worked', result.counties_worked.length);
            html += '<div class="result-list">';
            result.counties_worked.forEach(county => {
                html += `<span class="result-list-item">${county}</span>`;
            });
            html += '</div>';
        }

        // States worked (for LA stations)
        if (result.states_worked && result.states_worked.length > 0) {
            html += renderResultItem('States Worked', result.states_worked.length);
            html += '<div class="result-list">';
            result.states_worked.forEach(state => {
                html += `<span class="result-list-item">${state}</span>`;
            });
            html += '</div>';
        }

        // Provinces worked (for LA stations)
        if (result.provinces_worked && result.provinces_worked.length > 0) {
            html += renderResultItem('Provinces Worked', result.provinces_worked.length);
            html += '<div class="result-list">';
            result.provinces_worked.forEach(province => {
                html += `<span class="result-list-item">${province}</span>`;
            });
            html += '</div>';
        }

        // DX worked (for LA stations)
        if (result.dx_worked && result.dx_worked.length > 0) {
            html += renderResultItem('DX Worked', result.dx_worked.length);
            html += '<div class="result-list">';
            result.dx_worked.forEach(dx => {
                html += `<span class="result-list-item">${dx}</span>`;
            });
            html += '</div>';
        }

        // errors and warnings
        if (result.errors && result.errors.length > 0) {
            html += '<div class="result-group2">';
            html += '<h4>Errors</h4>';
            html += '<ul class="error-list">';
            result.errors.forEach(error => {
                html += `<li class="error-list-item">${error}</li>`;
            });
            html += '</ul>';
            html += '</div>';
        }

        if (result.warnings && result.warnings.length > 0) {
            html += '<div class="result-group">';
            html += '<h4>QSOS with ERRORS - Not scored</h4>';
            html += '<ul class="warning-list">';
            result.warnings.forEach(warning => {
                html += `<li class="warning-list-item">${warning}</li>`;
            });
            html += '</ul>';
            html += '</div>';
        }

        return html;
    }

    // Helper functions
    // Function to render a result item
    function renderResultItem(label, value, highlight = false) {
        const highlightClass = highlight ? ' highlight' : '';
        return `
            <div class="result-item, worked">
                <div class="result-label">${label}:<span>  </span></div>
                <div class="result-value${highlightClass}">${value}</div>
            </div>
        `;
    }
    function showLoading() {
        loadingIndicator.style.display = 'block';
        showIndividualBtn.disabled = true;
        showFinalReportBtn.disabled = true;
    }

    function hideLoading() {
        loadingIndicator.style.display = 'none';
        showIndividualBtn.disabled = false;
        showFinalReportBtn.disabled = false;
    }

    function showMessage(message, type) {
        messageBox.innerHTML = message;
        messageBox.className = 'message-box ' + type;
        messageBox.style.display = 'block';
    }

    function hideMessage() {
        messageBox.style.display = 'none';
    }

    function hideResults() {
        individualResults.style.display = 'none';
        finalReport.style.display = 'none';
    }

    function scrollToResults() {
        setTimeout(() => {
            if (individualResults.style.display === 'block') {
                individualResults.scrollIntoView({ behavior: 'smooth' });
            } else if (finalReport.style.display === 'block') {
                finalReport.scrollIntoView({ behavior: 'smooth' });
            }
        }, 300);
    }
});

// Print functions
function printCertificate() {
    document.body.classList.add('print-certificate');
    window.print();
    document.body.classList.remove('print-certificate');
}

function printStatistics() {
    document.body.classList.add('print-statistics');
    window.print();
    document.body.classList.remove('print-statistics');
}
