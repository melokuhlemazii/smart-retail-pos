/**
 * Chart Configuration and Initialization
 * Used in Sales Reports module
 */

// Color palette for charts
const chartColors = {
    primary: '#3B82F6',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#EF4444',
    purple: '#8B5CF6',
    pink: '#EC4899',
};

// Daily Sales Chart
function initializeDailySalesChart() {
    const ctx = document.getElementById('dailySalesChart');
    if (!ctx) return;

    // Build query string from filter params
    const params = new URLSearchParams({
        start_date: filterParams.start_date,
        end_date: filterParams.end_date,
        cashier_id: filterParams.cashier_id || '',
        category: filterParams.category || '',
        chart_type: 'daily'
    });

    fetch(`/sales_reports_data?${params}`)
        .then(response => response.json())
        .then(data => {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Daily Sales (R)',
                        data: data.data,
                        backgroundColor: chartColors.success,
                        borderColor: chartColors.success,
                        borderWidth: 2,
                        borderRadius: 5,
                        hoverBackgroundColor: '#059669'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 15,
                                font: { size: 12, weight: 'bold' }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return 'R ' + parseFloat(context.parsed.y).toLocaleString('en-ZA', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return 'R ' + value.toLocaleString('en-ZA', {maximumFractionDigits: 0});
                                }
                            },
                            title: {
                                display: true,
                                text: 'Amount (Rands)'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading daily sales chart:', error));
}

// Category Distribution Chart (Pie)
function initializeCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    const params = new URLSearchParams({
        start_date: filterParams.start_date,
        end_date: filterParams.end_date,
        cashier_id: filterParams.cashier_id || '',
        category: filterParams.category || '',
        chart_type: 'category'
    });

    fetch(`/sales_reports_data?${params}`)
        .then(response => response.json())
        .then(data => {
            const backgroundColors = [
                '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6',
                '#EC4899', '#14B8A6', '#6366F1', '#F97316', '#06B6D4'
            ];

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: backgroundColors.slice(0, data.labels.length),
                        borderColor: '#FFFFFF',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                usePointStyle: true,
                                padding: 15,
                                font: { size: 12, weight: 'bold' }
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return 'R ' + parseFloat(context.parsed).toLocaleString('en-ZA', {minimumFractionDigits: 2, maximumFractionDigits: 2});
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading category chart:', error));
}

// Top Products Chart
function initializeProductsChart() {
    const ctx = document.getElementById('productsChart');
    if (!ctx) return;

    const params = new URLSearchParams({
        start_date: filterParams.start_date,
        end_date: filterParams.end_date,
        cashier_id: filterParams.cashier_id || '',
        category: filterParams.category || '',
        chart_type: 'products'
    });

    fetch(`/sales_reports_data?${params}`)
        .then(response => response.json())
        .then(data => {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Quantity Sold',
                        data: data.data,
                        backgroundColor: chartColors.purple,
                        borderColor: chartColors.purple,
                        borderWidth: 2,
                        borderRadius: 5,
                        hoverBackgroundColor: '#7C3AED'
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 15,
                                font: { size: 12, weight: 'bold' }
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + ' units';
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error loading products chart:', error));
}

// Utility function to format currency
function formatCurrency(value) {
    return 'R ' + parseFloat(value).toLocaleString('en-ZA', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-ZA', {year: 'numeric', month: 'short', day: 'numeric'});
}
