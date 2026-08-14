// Louisiana QSO Party Log Upload - JavaScript

// Display results
function displayResults(result) {
    const html = generateResultsHTML(result);
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
}

// Generate HTML for results
function generateResultsHTML(result) {
    let html = '';

    // Station Information
    html += '<div class="result-group">';
    html += '<h4>Station Information</h4>';
    html += renderResultItem('Callsign', result.callsign, true);
    if (result.name && result.name !== 'N/A') {
        html += renderResultItem('Operator Name', result.name);
    }
    html += renderResultItem('Location Type', result.location_type);
    html += renderResultItem('Exchange', result.exchange);

    if (result.overlay && result.overlay !== 'N/A' && result.overlay !== null) {
        html += renderResultItem('Overlay', result.overlay);
    }
    html += renderResultItem('Mode Category', result.mode_category);
    html += renderResultItem('Power Level', result.power_level);
    html += '</div>';

    // Score Summary
    html += '<div class="result-group">';
    html += '<h4>Score Summary</h4>';
    html += renderResultItem('Final Score', result.final_score.toLocaleString(), true);
    html += renderResultItem('QSO Points', result.qso_points.toLocaleString());
    html += renderResultItem('Total Multipliers', result.total_multipliers);
    if (result.claimed_score && result.claimed_score !== 'N/A') {
        html += renderResultItem('Claimed Score', result.claimed_score.toLocaleString());
    }
    html += '</div>';

    // QSO Statistics
    html += '<div class="result-group">';
    html += '<h4>QSO Statistics</h4>';
    html += renderResultItem('Total QSOs', result.total_qsos);
    html += renderResultItem('Valid QSOs', result.valid_qsos);
    html += '</div>';

    // QSOs by Band
    if (result.qsos_by_band && result.qsos_by_band.length > 0) {
        html += '<div class="result-group">';
        html += '<h4>QSOs by Band</h4>';
        html += '<table class="result-table">';
        html += '<thead><tr><th>Band</th><th>Count</th></tr></thead>';
        html += '<tbody>';
        result.qsos_by_band.forEach(item => {
            if (item.count > 0) {
                html += `<tr><td>${item.band}m</td><td>${item.count}</td></tr>`;
            }
        });
        html += '</tbody></table>';
        html += '</div>';
    }

    // QSOs by Mode
    if (result.qsos_by_mode && result.qsos_by_mode.length > 0) {
        html += '<div class="result-group">';
        html += '<h4>QSOs by Mode</h4>';
        html += '<table class="result-table">';
        html += '<thead><tr><th>Mode</th><th>Count</th></tr></thead>';
        html += '<tbody>';
        result.qsos_by_mode.forEach(item => {
            if (item.count > 0) {
                html += `<tr><td>${item.mode}</td><td>${item.count}</td></tr>`;
            }
        });
        html += '</tbody></table>';
        html += '</div>';
    }

    // QSOs by Hour
    if (result.qsos_by_hour && result.qsos_by_hour.length > 0) {
        html += '<div class="result-group">';
        html += '<h4>QSOs by Hour</h4>';
        html += '<table class="result-table">';
        html += '<thead><tr><th>Hour</th><th>Count</th></tr></thead>';
        html += '<tbody>';
        result.qsos_by_hour.forEach(item => {
            if (item.count > 0) {
                html += `<tr><td>Hour ${item.hour + 1}</td><td>${item.count}</td></tr>`;
            }
        });
        html += '</tbody></table>';
        html += '</div>';
    }

    // Multipliers
    html += '<div class="result-group">';
    html += '<h4>Multipliers</h4>';
    
    // Counties worked (for NON-LA stations)
    if (result.counties_worked && result.counties_worked.length > 0) {
        html += renderResultItem('Counties Worked', result.counties_worked_multiplier);
        html += '<div class="result-list">';
        result.counties_worked.forEach(county => {
            html += `<span class="result-list-item">${county}</span>`;
        });
        html += '</div>';
    }

    // States worked (for LA stations)
    if (result.states_worked && result.states_worked.length > 0) {
        html += renderResultItem('States Worked', result.states_worked_multiplier);
        html += '<div class="result-list">';
        result.states_worked.forEach(state => {
            html += `<span class="result-list-item">${state}</span>`;
        });
        html += '</div>';
    }

    // Provinces worked (for LA stations)
    if (result.provinces_worked && result.provinces_worked.length > 0) {
        html += renderResultItem('Provinces Worked', result.provinces_worked_multiplier);
        html += '<div class="result-list">';
        result.provinces_worked.forEach(province => {
            html += `<span class="result-list-item">${province}</span>`;
        });
        html += '</div>';
    }

    // DX worked (for LA stations)
    if (result.dx_worked && result.dx_worked.length > 0) {
        html += renderResultItem('DX Worked', result.dx_worked_multiplier);
        html += '<div class="result-list">';
        result.dx_worked.forEach(dx => {
            html += `<span class="result-list-item">${dx}</span>`;
        });
        html += '</div>';
    }

    html += '</div>';

    // Bonuses
    let hasBonuses = false;
    let bonusesHTML = '<div class="result-group">';
    bonusesHTML += '<h4>Bonuses</h4>';

    if (result.worked_n5lcc && result.worked_n5lcc !== 'N/A') {
        hasBonuses = true;
        bonusesHTML += renderResultItem('Worked N5LCC', result.worked_n5lcc ? 'Yes' : 'No');
        if (result.num_n5lcc_contacts > 0) {
            bonusesHTML += renderResultItem('N5LCC Contacts', result.num_n5lcc_contacts);
        }
    }

    if (result.counties_activated && result.counties_activated.length > 0) {
        hasBonuses = true;
        bonusesHTML += renderResultItem('Counties Activated (Rover)', result.counties_activated.length);
        bonusesHTML += '<div class="result-list">';
        result.counties_activated.forEach(county => {
            bonusesHTML += `<span class="result-list-item">${county}</span>`;
        });
        bonusesHTML += '</div>';
    }

    if (result.rover_bonus_points > 0) {
        hasBonuses = true;
        bonusesHTML += renderResultItem('Rover Bonus Points', result.rover_bonus_points.toLocaleString());
    }

    bonusesHTML += '</div>';

    if (hasBonuses) {
        html += bonusesHTML;
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

    return html;
}


// Helper function to render a result item
function renderResultItem(label, value, highlight = false) {
    const highlightClass = highlight ? ' highlight' : '';
    return `
        <div class="result-item">
            <div class="result-label">${label}:</div>
            <div class="result-value${highlightClass}">${value}</div>
        </div>
    `;
}


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const clearBtn = document.getElementById('clearBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const messageBox = document.getElementById('messageBox');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    const statsHeader = document.getElementById('statsHeader');
    const fileInput = document.getElementById('logfile');
    const textArea = document.getElementById('log_text');

    // Prevent using both file upload and paste
    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            textArea.value = '';
            textArea.disabled = true;
        } else {
            textArea.disabled = false;
        }
    });

    textArea.addEventListener('input', function() {
        if (this.value.trim()) {
            fileInput.disabled = true;
        } else {
            fileInput.disabled = false;
        }
    });

    // Clear form
    clearBtn.addEventListener('click', function() {
        form.reset();
        fileInput.disabled = false;
        textArea.disabled = false;
        hideMessage();
        hideResults();
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous results
        hideMessage();
        hideResults();
        
        // Show loading indicator
        showLoading();
        
        // Prepare form data
        const formData = new FormData(form);
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Hide loading indicator
            hideLoading();
            
            if (data.success) {
                // Show success message
                showMessage(data.message, 'success');
                
                // Display results
                displayResults(data.result);
                
                // Scroll to results
                setTimeout(() => {
                    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 300);
            } else {
                // Show error message
                let errorMsg = data.error || 'Validation failed';
                if (data.errors && data.errors.length > 0) {
                    errorMsg += '<ul>';
                    data.errors.forEach(err => {
                        errorMsg += `<li>${err}</li>`;
                    });
                    errorMsg += '</ul>';
                }
                showMessage(errorMsg, 'error');
            }
            
        } catch (error) {
            hideLoading();
            showMessage('Error communicating with server: ' + error.message, 'error');
        }
    });

    // Show loading indicator
    function showLoading() {
        loadingIndicator.style.display = 'block';
        submitBtn.disabled = true;
    }

    // Hide loading indicator
    function hideLoading() {
        loadingIndicator.style.display = 'none';
        submitBtn.disabled = false;
    }

    // Show message
    function showMessage(message, type) {
        messageBox.innerHTML = message;
        messageBox.className = 'message-box ' + type;
        messageBox.style.display = 'block';
    }

    // Hide message
    function hideMessage() {
        messageBox.style.display = 'none';
    }

    // Hide results
    function hideResults() {
        resultsSection.style.display = 'none';
    }

});
