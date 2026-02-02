// charts.js - Enhanced chart functionality for Healing Horizons

class HealingCharts {
    constructor() {
        this.charts = new Map();
        this.init();
    }

    init() {
        // Initialize all charts on page
        this.initializeMoodChart();
        this.initializeProgressChart();
        this.initializeRecoveryChart();
        this.initializeActivityChart();
        this.initializeRadarChart();
    }

    initializeMoodChart() {
        const ctx = document.getElementById('moodChart');
        if (!ctx) return;

        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(244, 63, 94, 0.3)');
        gradient.addColorStop(1, 'rgba(244, 63, 94, 0.05)');

        const chart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
                datasets: [{
                    label: 'Mood Score',
                    data: [3, 4, 5, 6, 5, 7, 8, 9],
                    borderColor: '#f43f5e',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#f43f5e',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f1f5f9',
                        bodyColor: '#f1f5f9',
                        borderColor: '#f43f5e',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                let label = 'Mood: ';
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y + '/10';
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '/10';
                            },
                            color: '#64748b'
                        },
                        title: {
                            display: true,
                            text: 'Mood Score',
                            color: '#64748b'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#64748b'
                        },
                        title: {
                            display: true,
                            text: 'Weeks of Healing',
                            color: '#64748b'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animations: {
                    tension: {
                        duration: 1000,
                        easing: 'easeInOutQuart'
                    }
                }
            }
        });

        this.charts.set('mood', chart);
    }

    initializeProgressChart() {
        const ctx = document.getElementById('progressChart');
        if (!ctx) return;

        const chart = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [
                    {
                        label: 'Self-Care',
                        data: [4, 5, 7, 8],
                        backgroundColor: 'rgba(244, 63, 94, 0.8)',
                        borderColor: '#f43f5e',
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    },
                    {
                        label: 'Social Activity',
                        data: [3, 4, 6, 7],
                        backgroundColor: 'rgba(139, 92, 246, 0.8)',
                        borderColor: '#8b5cf6',
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    },
                    {
                        label: 'Productivity',
                        data: [5, 6, 7, 8],
                        backgroundColor: 'rgba(59, 130, 246, 0.8)',
                        borderColor: '#3b82f6',
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#64748b',
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f1f5f9',
                        bodyColor: '#f1f5f9',
                        borderColor: '#f43f5e',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '/10';
                            },
                            color: '#64748b'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#64748b'
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });

        this.charts.set('progress', chart);
    }

    initializeRecoveryChart() {
        const ctx = document.getElementById('recoveryChart');
        if (!ctx) return;

        const chart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: Array.from({length: 30}, (_, i) => `Day ${i + 1}`),
                datasets: [
                    {
                        label: 'Emotional Healing',
                        data: this.generateRecoveryData(30, 0.2),
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Self-Discovery',
                        data: this.generateRecoveryData(30, 0.3),
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#64748b'
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });

        this.charts.set('recovery', chart);
    }

    initializeActivityChart() {
        const ctx = document.getElementById('activityChart');
        if (!ctx) return;

        const chart = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Journaling', 'Meditation', 'Exercise', 'Social', 'Therapy', 'Self-Care'],
                datasets: [{
                    data: [25, 15, 20, 15, 10, 15],
                    backgroundColor: [
                        '#f43f5e',
                        '#8b5cf6',
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#ec4899'
                    ],
                    borderColor: '#ffffff',
                    borderWidth: 3,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#64748b',
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                },
                cutout: '65%',
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });

        this.charts.set('activity', chart);
    }

    initializeRadarChart() {
        const ctx = document.getElementById('radarChart');
        if (!ctx) return;

        const chart = new Chart(ctx.getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['Emotional', 'Social', 'Physical', 'Mental', 'Spiritual', 'Practical'],
                datasets: [
                    {
                        label: 'Current',
                        data: [7, 6, 8, 7, 5, 6],
                        backgroundColor: 'rgba(244, 63, 94, 0.2)',
                        borderColor: '#f43f5e',
                        borderWidth: 2,
                        pointBackgroundColor: '#f43f5e',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    },
                    {
                        label: 'Target',
                        data: [9, 8, 9, 8, 7, 8],
                        backgroundColor: 'rgba(139, 92, 246, 0.2)',
                        borderColor: '#8b5cf6',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointBackgroundColor: '#8b5cf6',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#64748b'
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 10,
                        ticks: {
                            stepSize: 2,
                            color: '#64748b'
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        angleLines: {
                            color: 'rgba(0,0,0,0.1)'
                        },
                        pointLabels: {
                            color: '#64748b',
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    }
                }
            }
        });

        this.charts.set('radar', chart);
    }

    generateRecoveryData(days, volatility) {
        const data = [];
        let current = 10;
        
        for (let i = 0; i < days; i++) {
            // General upward trend with some volatility
            const change = (Math.random() * 5 - 2.5) * volatility;
            current = Math.max(10, Math.min(100, current + change));
            
            // Ensure overall upward trend
            if (i > 7) current += 0.5;
            if (i > 14) current += 0.8;
            if (i > 21) current += 1;
            
            data.push(Math.round(current));
        }
        
        return data;
    }

    updateChart(chartName, newData) {
        const chart = this.charts.get(chartName);
        if (chart) {
            chart.data.datasets[0].data = newData;
            chart.update();
        }
    }

    animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value + '%';
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    exportChart(chartName, format = 'png') {
        const chart = this.charts.get(chartName);
        if (chart) {
            const link = document.createElement('a');
            link.download = `${chartName}-chart.${format}`;
            link.href = chart.toBase64Image();
            link.click();
        }
    }

    destroyAll() {
        this.charts.forEach(chart => chart.destroy());
        this.charts.clear();
    }

    resizeAll() {
        this.charts.forEach(chart => chart.resize());
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.healingCharts = new HealingCharts();
    
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            window.healingCharts.resizeAll();
        }, 250);
    });
    
    // Animate progress numbers
    const progressElements = document.querySelectorAll('.progress-number');
    progressElements.forEach(element => {
        const target = parseInt(element.dataset.target || element.textContent);
        window.healingCharts.animateValue(element, 0, target, 2000);
    });
});

// Chart utilities
const ChartUtils = {
    // Create a gradient for chart backgrounds
    createGradient(ctx, color1, color2, direction = 'vertical') {
        let gradient;
        
        if (direction === 'vertical') {
            gradient = ctx.createLinearGradient(0, 0, 0, 400);
        } else {
            gradient = ctx.createLinearGradient(0, 0, 400, 0);
        }
        
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        
        return gradient;
    },

    // Generate random data for testing
    generateRandomData(count, min, max) {
        return Array.from({length: count}, () => 
            Math.floor(Math.random() * (max - min + 1)) + min
        );
    },

    // Calculate average of data array
    calculateAverage(data) {
        return data.reduce((a, b) => a + b, 0) / data.length;
    },

    // Format percentage for display
    formatPercentage(value, total) {
        return ((value / total) * 100).toFixed(1) + '%';
    },

    // Get color based on value
    getColorForValue(value, max = 10) {
        const percentage = value / max;
        
        if (percentage < 0.3) return '#ef4444'; // Red
        if (percentage < 0.6) return '#f59e0b'; // Yellow
        if (percentage < 0.8) return '#10b981'; // Green
        return '#8b5cf6'; // Purple
    },

    // Create sparkline chart
    createSparkline(canvas, data, color = '#f43f5e') {
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const max = Math.max(...data);
        const min = Math.min(...data);
        
        ctx.clearRect(0, 0, width, height);
        
        // Draw line
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.lineJoin = 'round';
        ctx.lineCap = 'round';
        
        data.forEach((value, index) => {
            const x = (index / (data.length - 1)) * width;
            const y = height - ((value - min) / (max - min)) * height;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Draw area under line
        ctx.beginPath();
        ctx.moveTo(0, height);
        data.forEach((value, index) => {
            const x = (index / (data.length - 1)) * width;
            const y = height - ((value - min) / (max - min)) * height;
            ctx.lineTo(x, y);
        });
        ctx.lineTo(width, height);
        ctx.closePath();
        
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, color + '20');
        gradient.addColorStop(1, color + '05');
        ctx.fillStyle = gradient;
        ctx.fill();
    }
};

// Make utilities available globally
window.ChartUtils = ChartUtils;