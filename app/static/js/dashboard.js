// Enhanced Water Quality Dashboard with Advanced Features
class EnhancedWaterQualityDashboard {
    constructor() {
        this.readings = [];
        this.filteredReadings = [];
        this.currentSort = { field: 'timestamp', direction: 'desc' };
        this.init();
    }

    async init() {
        await this.loadUserReadings();
        this.setupEventListeners();
        this.setupRealTimeFilters();
    }

    // Load user's water readings
    async loadUserReadings() {
        try {
            this.showLoading();
            const response = await fetch('/api/water/readings');
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.readings = data.readings || [];
            this.filteredReadings = [...this.readings];
            
            this.updateDashboardStats();
            this.displayReadingsTable();
            this.setupSearchAndFilters();
            
        } catch (error) {
            console.error('Error loading readings:', error);
            this.showError(`Failed to load data: ${error.message}`);
        }
    }

    // Update dashboard statistics
    updateDashboardStats() {
        const totalReadings = document.getElementById('totalReadings');
        const latestPh = document.getElementById('latestPh');
        const latestTurbidity = document.getElementById('latestTurbidity');
        const latestOxygen = document.getElementById('latestOxygen');

        totalReadings.textContent = this.readings.length;
        
        if (this.readings.length > 0) {
            const latest = this.readings[0];
            latestPh.textContent = latest.ph_level ? latest.ph_level.toFixed(1) : '-';
            latestTurbidity.textContent = latest.turbidity_ntu ? latest.turbidity_ntu.toFixed(1) : '-';
            latestOxygen.textContent = latest.dissolved_oxygen ? latest.dissolved_oxygen.toFixed(1) : '-';
        }
        
        this.updateReadingCount();
    }

    // Display readings table
    displayReadingsTable() {
        const container = document.getElementById('readingsTable');
        
        if (this.filteredReadings.length === 0) {
            container.innerHTML = this.getEmptyStateHTML();
            return;
        }

        container.innerHTML = this.generateTableHTML();
        this.setupTableInteractions();
    }

    getEmptyStateHTML() {
        return `
            <div class="text-center py-5">
                <i class="bi bi-inbox display-1 text-muted"></i>
                <h4 class="text-muted mt-3">No water quality readings found</h4>
                <p class="text-muted mb-3">Add your first reading using the form above!</p>
                <button class="btn btn-primary" onclick="document.getElementById('location_name').focus()">
                    <i class="bi bi-plus-circle"></i> Add First Reading
                </button>
            </div>
        `;
    }

    generateTableHTML() {
        return `
            <div class="table-responsive">
                <table class="table table-hover table-striped" id="readingsTableElement">
                    <thead class="table-dark">
                        <tr>
                            <th class="sortable" data-field="location_name">
                                <i class="bi bi-geo-alt"></i> Location 
                                ${this.getSortIcon('location_name')}
                            </th>
                            <th class="sortable" data-field="ph_level">
                                <i class="bi bi-speedometer2"></i> pH
                                ${this.getSortIcon('ph_level')}
                            </th>
                            <th class="sortable" data-field="turbidity_ntu">
                                <i class="bi bi-eye"></i> Turbidity
                                ${this.getSortIcon('turbidity_ntu')}
                            </th>
                            <th class="sortable" data-field="dissolved_oxygen">
                                <i class="bi bi-wind"></i> Oxygen
                                ${this.getSortIcon('dissolved_oxygen')}
                            </th>
                            <th class="sortable" data-field="temperature_c">
                                <i class="bi bi-thermometer"></i> Temp
                                ${this.getSortIcon('temperature_c')}
                            </th>
                            <th class="sortable" data-field="timestamp">
                                <i class="bi bi-calendar"></i> Date
                                ${this.getSortIcon('timestamp')}
                            </th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.filteredReadings.map(reading => this.getTableRowHTML(reading)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    getTableRowHTML(reading) {
        const status = this.getWaterQualityStatus(reading);
        const statusBadge = this.getStatusBadge(status);
        
        return `
            <tr data-reading-id="${reading.id}">
                <td class="fw-bold">${reading.location_name}</td>
                <td>
                    ${reading.ph_level ? `
                        <span class="${this.getParameterClass(reading.ph_level, 'ph')}">
                            ${reading.ph_level.toFixed(1)}
                        </span>
                    ` : '-'}
                </td>
                <td>
                    ${reading.turbidity_ntu ? `
                        <span class="${this.getParameterClass(reading.turbidity_ntu, 'turbidity')}">
                            ${reading.turbidity_ntu.toFixed(1)} NTU
                        </span>
                    ` : '-'}
                </td>
                <td>
                    ${reading.dissolved_oxygen ? `
                        <span class="${this.getParameterClass(reading.dissolved_oxygen, 'oxygen')}">
                            ${reading.dissolved_oxygen.toFixed(1)} mg/L
                        </span>
                    ` : '-'}
                </td>
                <td>${reading.temperature_c ? reading.temperature_c + '°C' : '-'}</td>
                <td>${new Date(reading.timestamp).toLocaleDateString()}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="dashboard.viewReading(${reading.id})" 
                                title="View Details">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="dashboard.editReading(${reading.id})" 
                                title="Edit Reading">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="dashboard.deleteReading(${reading.id})" 
                                title="Delete Reading">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }

    getParameterClass(value, type) {
        const thresholds = {
            ph: { good: [6.5, 8.5], fair: [6.0, 9.0] },
            turbidity: { good: [0, 5], fair: [5, 10] },
            oxygen: { good: [5, Infinity], fair: [3, 5] }
        };
        
        const threshold = thresholds[type];
        if (!threshold) return '';
        
        if (value >= threshold.good[0] && value <= threshold.good[1]) return 'text-success fw-bold';
        if (value >= threshold.fair[0] && value <= threshold.fair[1]) return 'text-warning fw-bold';
        return 'text-danger fw-bold';
    }

    getSortIcon(field) {
        if (this.currentSort.field !== field) {
            return '<i class="bi bi-arrow-down-up text-muted"></i>';
        }
        return this.currentSort.direction === 'asc' ? 
            '<i class="bi bi-arrow-up"></i>' : 
            '<i class="bi bi-arrow-down"></i>';
    }

    // Setup event listeners
    setupEventListeners() {
        // Add reading form
        const form = document.getElementById('addReadingForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleAddReading(e));
        }
    }

    // Search and filtering
    setupSearchAndFilters() {
        const searchInput = document.getElementById('searchInput');
        const parameterFilter = document.getElementById('parameterFilter');
        const dateFilter = document.getElementById('dateFilter');

        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => this.applyFilters(), 300);
        });

        parameterFilter.addEventListener('change', () => this.applyFilters());
        dateFilter.addEventListener('change', () => this.applyFilters());
    }

    applyFilters() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const parameterFilter = document.getElementById('parameterFilter').value;
        const dateFilter = document.getElementById('dateFilter').value;

        this.filteredReadings = this.readings.filter(reading => {
            return this.matchesSearch(reading, searchTerm) &&
                   this.matchesParameter(reading, parameterFilter) &&
                   this.matchesDate(reading, dateFilter);
        });

        this.sortReadings();
        this.displayReadingsTable();
        this.updateReadingCount();
    }

    matchesSearch(reading, searchTerm) {
        if (!searchTerm) return true;
        return reading.location_name.toLowerCase().includes(searchTerm);
    }

    matchesParameter(reading, parameterFilter) {
        if (!parameterFilter) return true;
        return reading[parameterFilter] != null;
    }

    matchesDate(reading, dateFilter) {
        if (!dateFilter) return true;
        const daysAgo = parseInt(dateFilter);
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - daysAgo);
        return new Date(reading.timestamp) >= cutoffDate;
    }

    // Sorting functionality
    setupTableInteractions() {
        const sortableHeaders = document.querySelectorAll('.sortable');
        sortableHeaders.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const field = header.dataset.field;
                this.sortReadingsByField(field);
            });
        });
    }

    sortReadingsByField(field) {
        if (this.currentSort.field === field) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.field = field;
            this.currentSort.direction = 'asc';
        }
        this.sortReadings();
        this.displayReadingsTable();
    }

    sortReadings() {
        this.filteredReadings.sort((a, b) => {
            let aValue = a[this.currentSort.field];
            let bValue = b[this.currentSort.field];

            if (aValue == null) aValue = this.currentSort.direction === 'asc' ? Infinity : -Infinity;
            if (bValue == null) bValue = this.currentSort.direction === 'asc' ? Infinity : -Infinity;

            if (this.currentSort.direction === 'asc') {
                return aValue > bValue ? 1 : -1;
            } else {
                return aValue < bValue ? 1 : -1;
            }
        });
    }

    // Add new reading
    async handleAddReading(e) {
        e.preventDefault();
        
        const form = e.target;
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;

        try {
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Adding...';
            submitButton.disabled = true;

            const formData = {
                location_name: document.getElementById('location_name').value,
                ph_level: document.getElementById('ph_level').value ? parseFloat(document.getElementById('ph_level').value) : null,
                turbidity_ntu: document.getElementById('turbidity_ntu').value ? parseFloat(document.getElementById('turbidity_ntu').value) : null,
                dissolved_oxygen: document.getElementById('dissolved_oxygen').value ? parseFloat(document.getElementById('dissolved_oxygen').value) : null,
                temperature_c: document.getElementById('temperature_c').value ? parseFloat(document.getElementById('temperature_c').value) : null,
                conductivity_us: document.getElementById('conductivity_us').value ? parseFloat(document.getElementById('conductivity_us').value) : null
            };

            const response = await fetch('/api/water/reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Water quality reading added successfully!');
                form.reset();
                await this.loadUserReadings();
            } else {
                throw new Error(data.error || 'Failed to add reading');
            }
        } catch (error) {
            this.showError(`Failed to add reading: ${error.message}`);
        } finally {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    }

    // Delete reading - FIXED VERSION
    async deleteReading(readingId) {
        if (!confirm('Are you sure you want to delete this water quality reading? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`/api/water/reading/${readingId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccess('Reading deleted successfully!');
                await this.loadUserReadings();
            } else {
                throw new Error(data.error || 'Failed to delete reading');
            }
        } catch (error) {
            this.showError(`Failed to delete reading: ${error.message}`);
        }
    }

    // View and edit operations
    viewReading(readingId) {
        const reading = this.readings.find(r => r.id === readingId);
        if (reading) {
            this.showReadingDetails(reading);
        }
    }

    editReading(readingId) {
        const reading = this.readings.find(r => r.id === readingId);
        if (reading) {
            this.populateEditForm(reading);
        }
    }

    showReadingDetails(reading) {
        const status = this.getWaterQualityStatus(reading);
        const modalContent = `
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title"><i class="bi bi-droplet"></i> Reading Details</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <h6>Location: ${reading.location_name}</h6>
                <div class="row mt-3">
                    <div class="col-6">
                        <strong>pH Level:</strong> ${reading.ph_level || 'N/A'}
                    </div>
                    <div class="col-6">
                        <strong>Turbidity:</strong> ${reading.turbidity_ntu ? reading.turbidity_ntu + ' NTU' : 'N/A'}
                    </div>
                    <div class="col-6">
                        <strong>Dissolved Oxygen:</strong> ${reading.dissolved_oxygen ? reading.dissolved_oxygen + ' mg/L' : 'N/A'}
                    </div>
                    <div class="col-6">
                        <strong>Temperature:</strong> ${reading.temperature_c ? reading.temperature_c + '°C' : 'N/A'}
                    </div>
                    <div class="col-12 mt-2">
                        <strong>Status:</strong> ${this.getStatusBadge(status)}
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
        `;
        
        this.showCustomModal(modalContent);
    }

    populateEditForm(reading) {
        document.getElementById('location_name').value = reading.location_name;
        if (reading.ph_level) document.getElementById('ph_level').value = reading.ph_level;
        if (reading.turbidity_ntu) document.getElementById('turbidity_ntu').value = reading.turbidity_ntu;
        if (reading.dissolved_oxygen) document.getElementById('dissolved_oxygen').value = reading.dissolved_oxygen;
        if (reading.temperature_c) document.getElementById('temperature_c').value = reading.temperature_c;
        if (reading.conductivity_us) document.getElementById('conductivity_us').value = reading.conductivity_us;
        
        document.getElementById('location_name').scrollIntoView({ behavior: 'smooth' });
    }

    showCustomModal(content) {
        let modal = document.getElementById('customModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'customModal';
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        ${content}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        } else {
            modal.querySelector('.modal-content').innerHTML = content;
        }
        
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    // Utility methods
    setupRealTimeFilters() {
        const clearButton = document.createElement('button');
        clearButton.className = 'btn btn-outline-secondary btn-sm mt-2';
        clearButton.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Clear Filters';
        clearButton.onclick = () => this.clearFilters();
        
        const filterCard = document.querySelector('.card-body .row');
        if (filterCard) {
            filterCard.parentNode.appendChild(clearButton);
        }
    }

    clearFilters() {
        document.getElementById('searchInput').value = '';
        document.getElementById('parameterFilter').value = '';
        document.getElementById('dateFilter').value = '';
        this.applyFilters();
    }

    showLoading() {
        const container = document.getElementById('readingsTable');
        container.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 text-muted">Loading your water quality data...</p>
            </div>
        `;
    }

    showSuccess(message) {
        document.getElementById('successMessage').textContent = message;
        const modal = new bootstrap.Modal(document.getElementById('successModal'));
        modal.show();
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        const modal = new bootstrap.Modal(document.getElementById('errorModal'));
        modal.show();
    }

    // Water quality assessment
    getWaterQualityStatus(reading) {
        let score = 0;
        let parameters = 0;

        if (reading.ph_level && reading.ph_level >= 6.5 && reading.ph_level <= 8.5) {
            score += 1;
            parameters += 1;
        }
        
        if (reading.turbidity_ntu && reading.turbidity_ntu < 5) {
            score += 1;
            parameters += 1;
        }
        
        if (reading.dissolved_oxygen && reading.dissolved_oxygen > 5) {
            score += 1;
            parameters += 1;
        }

        if (parameters === 0) return 'unknown';
        
        const percentage = (score / parameters) * 100;
        if (percentage >= 80) return 'excellent';
        if (percentage >= 60) return 'good';
        if (percentage >= 40) return 'fair';
        return 'poor';
    }

    getStatusBadge(status) {
        const badges = {
            excellent: '<span class="badge bg-success"><i class="bi bi-award"></i> Excellent</span>',
            good: '<span class="badge bg-info"><i class="bi bi-check-circle"></i> Good</span>',
            fair: '<span class="badge bg-warning"><i class="bi bi-exclamation-triangle"></i> Fair</span>',
            poor: '<span class="badge bg-danger"><i class="bi bi-x-circle"></i> Poor</span>',
            unknown: '<span class="badge bg-secondary"><i class="bi bi-question-circle"></i> Unknown</span>'
        };
        return badges[status] || badges.unknown;
    }

    updateReadingCount() {
        const count = this.filteredReadings.length;
        const total = this.readings.length;
        const badge = document.getElementById('readingCount');
        
        if (count === total) {
            badge.textContent = `${count} reading${count !== 1 ? 's' : ''}`;
            badge.className = 'badge bg-primary fs-6';
        } else {
            badge.textContent = `${count} of ${total} reading${total !== 1 ? 's' : ''}`;
            badge.className = 'badge bg-warning fs-6';
        }
    }
}

// Initialize dashboard when DOM is loaded
let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Enhanced Water Quality Dashboard...');
    dashboard = new EnhancedWaterQualityDashboard();
});