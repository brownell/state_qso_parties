// Texas QSO Party Results Lookup - JavaScript
console.log("js has loaded")
document.addEventListener('DOMContentLoaded', function() {
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
        const year = yearSelect.value.trim();
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
    // TODO PDF final reort
    showFinalReportBtn.addEventListener('click', async function() {
        const year = yearSelect.value.trim();

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
            const response = await fetch(`/api/final_report/${year}`);
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
        year = result.year;
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
                    <p>Place ${result.rank}
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
        html += '<div class="result-group"><h4>Station Information</h4>';
        html += `<div class="result-item"><div class="result-label">Callsign:</div><div class="result-value">${result.callsign}</div></div>`;
        if (result.name) {
            html += `<div class="result-item"><div class="result-label">Operator Name:</div><div class="result-value">${result.name}</div></div>`;
        }
        // if (result.overlay) {
        //     html += `<div class="result-item"><div class="result-label">Overlay:</div><div class="result-value">${result.overlay}</div></div>`;
        // }
        if (result.dx_entity != result.callsign) {
            html += `<div class="result-item"><div class="result-label">Station Location:</div><div class="result-value">${result.dx_entity}</div></div>`;
        } else {
            html += `<div class="result-item"><div class="result-label">Station Location:</div><div class="result-value">${result.category_location}</div></div>`;
        }
        html += `<div class="result-item"><div class="result-label">Station Type:</div><div class="result-value">${result.category_station}</div></div>`;
        html += `<div class="result-item"><div class="result-label">Station Type:</div><div class="result-value">${result.category_station}</div></div>`;
        html += `<div class="result-item"><div class="result-label">Mode:</div><div class="result-value">${result.category_mode}</div></div>`;
        html += `<div class="result-item"><div class="result-label">Power Level:</div><div class="result-value">${result.category_power}</div></div>`;
        html += '</div>';

        // Score Summary
        html += '<div class="result-group"><h4>Score Summary</h4>';
        html += `<div class="result-item"><div class="result-label">Final Score:</div><div class="result-value ">${result.final_score.toLocaleString()}</div></div>`;
        if (result.claimed_score) {
            html += `<div class="result-item"><div class="result-label">Claimed Score:</div><div class="result-value">${result.claimed_score.toLocaleString()}</div></div>`;
        }
        if (result.cab_bonus_points > 0 || result.mtb_bonus_points > 0) {
            html += `<div class="result-item"><div class="result-label">Score Before Bonus Added</div><div class="result-value">${result.score_wo_bonus}</div></div>`;
        }
        if (result.cab_bonus_points > 0) {
            html += `<div class="result-item"><div class="result-label">County Activation Bonus Points</div><div class="result-value">${result.cab_bonus_points}</div></div>`;
        }
        if (result.mtb_bonus_points > 0) {
            html += `<div class="result-item"><div class="result-label">Mobile Tracking Bonus Points</div><div class="result-value">${result.cab_bonus_points}</div></div>`;
        }
        html += `<div class="result-item"><div class="result-label">QSO Points:</div><div class="result-value">${result.qso_points.toLocaleString()}</div></div>`;
        html += `<div class="result-item"><div class="result-label">Total Multipliers:</div><div class="result-value">${result.total_multipliers.toLocaleString}</div></div>`;

        // if (result.worked_n5lcc && result.worked_n5lcc !== 'N/A') {
        //     hasBonuses = true;
        //     bonusesHTML += renderResultItem('Worked N5LCC', result.worked_n5lcc ? 'Yes' : 'No');
        //     if (result.num_n5lcc_contacts > 0) {
        //         bonusesHTML += renderResultItem('N5LCC Contacts', result.num_n5lcc_contacts);
        //     }
        // }

        // QSO Statistics
        html += '<div class="result-group"><h4>QSO Statistics</h4>';
        html += '<p>To see which QSO were not scored, see the section of messages below.</p>'
        html += `<div class="result-item"><div class="result-label">Total QSOs:</div><div class="result-value ">${result.total_qsos.toLocaleString()}</div></div>`;
        html += `<div class="result-item"><div class="result-label">Valid QSOs:</div><div class="result-value ">${result.valid_qsos.toLocaleString()}</div></div>`;
        if (result.cw_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">CW QSOs:</div><div class="result-value ">${result.cw_qsos.toLocaleString()}</div></div>`; }
        if (result.ph_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">Phone QSOs:</div><div class="result-value ">${result.ph_qsos.toLocaleString()}</div></div>`; }
        if (result.rt_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">RTTY QSOs:</div><div class="result-value ">${result.rt_qsos.toLocaleString()}</div></div>`; }
        if (result.dg_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">Other Digital QSOs:</div><div class="result-value ">${result.dg_qsos.toLocaleString()}</div></div>`; }
        html += '</div>';

        if (result.uniques > 0) {
        html += `<div class="result-item"><div class="result-label">Uniques (points awarded):</div><div class="result-value ">${result.uniques.toLocaleString()}</div></div>`; }
        
        if (result.nils > 0) {
        html += `<div class="result-item"><div class="result-label">Not In Log (no points):</div><div class="result-value ">${result.nils.toLocaleString()}</div></div>`; }
        html += '</div>';
        
        if (result.busteds > 0) {
        html += `<div class="result-item"><div class="result-label"Busted Callsign (no points):</div><div class="result-value ">${result.busteds.toLocaleString()}</div></div>`; }
        html += '</div>';
        
        if (result.dup_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">Duplicate QSOs (no points):</div><div class="result-value ">${result.dup_qsos.toLocaleString()}</div></div>`; }
        html += '</div>';
        
        if (result.invalid_exchange_qso > 0) {
        html += `<div class="result-item"><div class="result-label">QSOs With Invalid Exchange:</div><div class="result-value ">${result.invalid_exchange_qso.toLocaleString()}</div></div>`; }
        html += '</div>';
        
        if (result.other_bad_qsos > 0) {
        html += `<div class="result-item"><div class="result-label">Other Bad Qsos (no points):</div><div class="result-value ">${result.other_bad_qsos.toLocaleString()}</div></div>`; }
        html += '</div>';

        // // Multipliers
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
        
        // Counties worked (for NON-LA stations)
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

        // QSOs by Band
        if (result.qsos_by_band && result.qsos_by_band.length > 0) {
            html += '<div class="result-group">';
            html += '<h4>QSOs by Band</h4>';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Band</th><th>Count</th></tr></thead>';
            html += '<tbody>';
            for (const [key, value] of Object.entries(result.qsos_by_band)) {
                console.log(`by mode  ${key}: ${value}`);
                if (value > 0) {
                    html += `<tr><td>${key}</td><td>${value}</td></tr>`;
                }
            }
            html += '</tbody></table>';
            html += '</div>';
        }

        // QSOs by Mode
        if (result.qsos_by_mode) {
            html += '<div class="result-group">';
            html += '<h4>QSOs by Mode</h4>';
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
            html += '<div class="result-group">';
            html += '<h4>QSOs by Hour</h4>';
            html += '<table class="result-table">';
            html += '<thead><tr><th>Hour (1400 April 4 through 0200 April 5)</th><th>Count</th></tr></thead>';
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


        // Bands Worked
        if (result.bands_worked && result.bands_worked.length > 0) {
            html += '<div class="result-group">';
            html += '<h4>Bands Worked</h4>';
            html += '<div class="result-list">';
            result.bands_worked.forEach(band => {
                html += `<span class="result-list-item">${band}m</span>`;
            });
            html += '</div>';
            html += '</div>';
        }

        // errors and warnings
        if (result.errors && result.errors.length > 0) {
            html += '<div class="result-group">';
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

// TODO pdf final report
function printFinalReport() {
    document.body.classList.add('print-final-report');
    window.print();
    document.body.classList.remove('print-final-report');
}
