/**
 * Water Quality Analytics Dashboard
 * Handles Chart.js visualizations and data loading
 */

class AnalyticsDashboard {
    constructor() {
        this.charts = {
            trends: null,
            qualityPie: null,
            userStats: null
        };
        this.init();
    }

    async init() {
        console.log('Initializing Analytics Dashboard...');
        
        try {
            // Load all data in parallel for better performance
            await Promise.all([
                this.loadStatistics(),
                this.loadTrendsChart(),
                this.loadQualityDistribution()
            ]);
            
            // Load role-specific analytics
            if (this.userCanViewLocationInsights()) {
                await this.loadLocationInsights();
            }
            
            if (this.userIsAdmin()) {
                await this.loadUserStatistics();
            }
            
            console.log('Analytics Dashboard initialized successfully');
        } catch (error) {
            console.error('Error initializing dashboard:', error);
            this.showError('Failed to load dashboard data');
        }
    }

    // Role checking methods
    userCanViewLocationInsights() {
        return ['researcher', 'government', 'admin'].includes(window.currentUserRole);
    }

    userIsAdmin() {
        return window.currentUserRole === 'admin';
    }

    // Statistics Cards
    async loadStatistics() {
        try {
            const response = await fetch('/analytics/api/statistics');
            if (!response.ok) throw new Error('Failed to fetch statistics');
            
            const data = await response.json();
            
            // Update statistics cards
            document.getElementById('total-readings').textContent = data.total_readings.toLocaleString();
            document.getElementById('excellent-readings').textContent = data.excellent_readings.toLocaleString();
            document.getElementById('avg-ph').textContent = data.avg_ph.toFixed(2);
            document.getElementById('active-locations').textContent = data.active_locations.toLocaleString();
            
        } catch (error) {
            console.error('Error loading statistics:', error);
            this.showErrorInCard('total-readings', 'Failed to load');
        }
    }

    // Trends Chart (Line Chart)
    async loadTrendsChart() {
        try {
            const response = await fetch('/analytics/api/water-quality-trends');
            if (!response.ok) throw new Error('Failed to fetch trends data');
            
            const data = await response.json();
            
            // Hide loading spinner
            document.getElementById('trends-loading').style.display = 'none';
            
            const ctx = document.getElementById('trendsChart').getContext('2d');
            this.charts.trends = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates.map(date => new Date(date).toLocaleDateString()),
                    datasets: [
                        {
                            label: 'pH Level',
                            data: data.ph_values,
                            borderColor: '#e74a3b',
                            backgroundColor: 'rgba(231, 74, 59, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true,
                            yAxisID: 'y'
                        },
                        {
                            label: 'Dissolved Oxygen (mg/L)',
                            data: data.do_values,
                            borderColor: '#36b9cc',
                            backgroundColor: 'rgba(54, 185, 204, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true,
                            yAxisID: 'y1'
                        },
                        {
                            label: 'Turbidity (NTU)',
                            data: data.turbidity_values,
                            borderColor: '#f6c23e',
                            backgroundColor: 'rgba(246, 194, 62, 0.1)',
                            borderWidth: 2,
                            tension: 0.4,
                            fill: true,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Water Quality Trends Over Time'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    label += context.parsed.y.toFixed(2);
                                    return label;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Date'
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                            title: {
                                display: true,
                                text: 'pH Level'
                            },
                            min: 0,
                            max: 14,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            title: {
                                display: true,
                                text: 'DO & Turbidity'
                            },
                            grid: {
                                drawOnChartArea: false
                            }
                        }
                    }
                }
            });
            
        } catch (error) {
            console.error('Error loading trends chart:', error);
            document.getElementById('trends-loading').innerHTML = 
                '<div class="text-danger">Failed to load trends data</div>';
        }
    }

    // Quality Distribution (Pie Chart)
    async loadQualityDistribution() {
        try {
            const response = await fetch('/analytics/api/quality-distribution');
            if (!response.ok) throw new Error('Failed to fetch quality distribution');
            
            const data = await response.json();
            
            // Hide loading spinner
            document.getElementById('distribution-loading').style.display = 'none';
            
            const ctx = document.getElementById('qualityPieChart').getContext('2d');
            this.charts.qualityPie = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: data.colors,
                        hoverBackgroundColor: data.colors.map(color => this.lightenColor(color, 20)),
                        hoverBorderColor: "rgba(234, 236, 244, 1)",
                        borderWidth: 2,
                        hoverOffset: 15
                    }],
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${value} readings (${percentage}%)`;
                                }
                            }
                        }
                    },
                    cutout: '60%'
                }
            });
            
        } catch (error) {
            console.error('Error loading quality distribution:', error);
            document.getElementById('distribution-loading').innerHTML = 
                '<div class="text-danger">Failed to load distribution data</div>';
        }
    }

    // Location Insights (Researcher+ only)
    async loadLocationInsights() {
        try {
            const response = await fetch('/analytics/api/location-insights');
            if (!response.ok) throw new Error('Failed to fetch location insights');
            
            const locations = await response.json();
            
            // Hide loading spinner and show table
            document.getElementById('locations-loading').style.display = 'none';
            document.getElementById('locations-table').style.display = 'block';
            
            const tableBody = document.getElementById('locationInsightsBody');
            tableBody.innerHTML = locations.map(location => `
                <tr>
                    <td><strong>${this.escapeHtml(location.location)}</strong></td>
                    <td>
                        <span class="badge ${this.getPHBadgeClass(location.avg_ph)}">
                            ${location.avg_ph.toFixed(2)}
                        </span>
                    </td>
                    <td>${location.avg_do.toFixed(2)} mg/L</td>
                    <td>${location.avg_turbidity.toFixed(2)} NTU</td>
                    <td><span class="badge bg-secondary">${location.reading_count}</span></td>
                    <td>${new Date(location.last_reading).toLocaleDateString()}</td>
                </tr>
            `).join('');
            
        } catch (error) {
            console.error('Error loading location insights:', error);
            document.getElementById('locations-loading').innerHTML = 
                '<div class="text-danger">Failed to load location insights</div>';
        }
    }

    // User Statistics (Admin only)
    async loadUserStatistics() {
        try {
            const response = await fetch('/analytics/api/user-statistics');
            if (!response.ok) throw new Error('Failed to fetch user statistics');
            
            const userStats = await response.json();
            
            // Hide loading spinner
            document.getElementById('users-loading').style.display = 'none';
            
            const ctx = document.getElementById('userStatsChart').getContext('2d');
            this.charts.userStats = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: userStats.map(stat => {
                        const roleNames = {
                            'community': 'Community',
                            'researcher': 'Researcher',
                            'government': 'Government',
                            'admin': 'Admin'
                        };
                        return roleNames[stat.role] || stat.role;
                    }),
                    datasets: [{
                        label: 'Number of Users',
                        data: userStats.map(stat => stat.user_count),
                        backgroundColor: [
                            'rgba(54, 185, 204, 0.8)',
                            'rgba(78, 115, 223, 0.8)',
                            'rgba(231, 74, 59, 0.8)',
                            'rgba(246, 194, 62, 0.8)'
                        ],
                        borderColor: [
                            'rgb(54, 185, 204)',
                            'rgb(78, 115, 223)',
                            'rgb(231, 74, 59)',
                            'rgb(246, 194, 62)'
                        ],
                        borderWidth: 2,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'User Distribution by Role'
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Users'
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'User Roles'
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
            
        } catch (error) {
            console.error('Error loading user statistics:', error);
            document.getElementById('users-loading').innerHTML = 
                '<div class="text-danger">Failed to load user statistics</div>';
        }
    }

    // Utility Methods
    getPHBadgeClass(phValue) {
        if (phValue >= 6.5 && phValue <= 8.5) return 'bg-success';
        if (phValue >= 6.0 && phValue <= 9.0) return 'bg-warning';
        return 'bg-danger';
    }

    lightenColor(color, percent) {
        // Simple color lightening for hover effects
        const num = parseInt(color.replace("#", ""), 16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) + amt;
        const G = (num >> 8 & 0x00FF) + amt;
        const B = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
            (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
            (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1);
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    showError(message) {
        // Create a temporary error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger alert-dismissible fade show';
        errorDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container-fluid').prepend(errorDiv);
    }

    showErrorInCard(cardId, message) {
        document.getElementById(cardId).innerHTML = 
            `<span class="text-danger">${message}</span>`;
    }

    // Cleanup method (for page navigation)
    destroy() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
    }
}

// Initialize dashboard when page loads
let analyticsDashboard;

document.addEventListener('DOMContentLoaded', function() {
    analyticsDashboard = new AnalyticsDashboard();
});

// Cleanup before page unload (optional)
window.addEventListener('beforeunload', function() {
    if (analyticsDashboard) {
        analyticsDashboard.destroy();
    }
});