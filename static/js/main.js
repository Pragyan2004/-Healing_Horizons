// 2026 Healing Horizons - Main JavaScript

class HealingHorizonsApp {
    constructor() {
        this.initializeComponents();
        this.setupEventListeners();
        this.initializeAnimations();
    }

    initializeComponents() {
        // Initialize markdown rendering
        this.initializeMarkdown();

        // Initialize charts if on dashboard
        if (document.getElementById('moodChart')) {
            this.initializeCharts();
        }

        // Initialize theme
        this.initializeTheme();
    }

    setupEventListeners() {
        // Form submission with loading animation
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                if (form.classList.contains('needs-validation')) {
                    if (!form.checkValidity()) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }

                // Show loading overlay
                if (!form.classList.contains('no-loading')) {
                    this.showLoadingOverlay();
                }
            });
        });

        // Mood selector
        document.querySelectorAll('.mood-selector .mood-option').forEach(option => {
            option.addEventListener('click', (e) => {
                document.querySelectorAll('.mood-option').forEach(opt => {
                    opt.classList.remove('active');
                });
                e.currentTarget.classList.add('active');
                document.getElementById('moodInput').value =
                    e.currentTarget.dataset.mood;
            });
        });

        // Textarea auto-resize
        document.querySelectorAll('textarea.auto-resize').forEach(textarea => {
            textarea.addEventListener('input', function () {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        });

        // Copy to clipboard
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const text = e.currentTarget.dataset.text;
                try {
                    await navigator.clipboard.writeText(text);
                    this.showToast('Copied to clipboard!', 'success');
                } catch (err) {
                    this.showToast('Failed to copy', 'error');
                }
            });
        });
    }

    initializeMarkdown() {
        // Configure marked.js
        marked.setOptions({
            breaks: true,
            gfm: true,
            headerIds: true,
            highlight: function (code, lang) {
                if (window.hljs) {
                    return hljs.highlightAuto(code).value;
                }
                return code;
            }
        });

        // Convert all markdown content
        document.querySelectorAll('.markdown-content').forEach(element => {
            const text = element.textContent;
            element.innerHTML = marked.parse(text);
        });
    }

    initializeCharts() {
        // Mood Chart
        const moodCtx = document.getElementById('moodChart');
        if (moodCtx) {
            new Chart(moodCtx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Mood Score',
                        data: [4, 6, 5, 7, 6, 8, 7],
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#f43f5e',
                        pointBorderColor: '#fff',
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(255, 255, 255, 0.9)',
                            titleColor: '#1e293b',
                            bodyColor: '#1e293b',
                            borderColor: '#e2e8f0',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 10,
                            grid: { color: 'rgba(0,0,0,0.03)' },
                            ticks: { font: { family: 'Inter' } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { font: { family: 'Inter' } }
                        }
                    }
                }
            });
        }

        // Recovery Progress
        const progressCtx = document.getElementById('progressChart');
        if (progressCtx) {
            new Chart(progressCtx.getContext('2d'), {
                type: 'radar',
                data: {
                    labels: ['Emotional', 'Social', 'Physical', 'Mental', 'Spiritual'],
                    datasets: [{
                        label: 'Current',
                        data: [7, 6, 8, 7, 5],
                        backgroundColor: 'rgba(244, 63, 94, 0.2)',
                        borderColor: '#f43f5e',
                        borderWidth: 3,
                        pointBackgroundColor: '#f43f5e'
                    }, {
                        label: 'Target',
                        data: [9, 8, 9, 8, 7],
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        borderColor: '#8b5cf6',
                        borderWidth: 2,
                        borderDash: [5, 5]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 10,
                            ticks: { display: false },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            angleLines: { color: 'rgba(0,0,0,0.05)' }
                        }
                    },
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }
    }

    initializeTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', theme);
    }

    initializeAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-slide-up-fade');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.glass-card, .feature-card, .testimonial-card').forEach(el => {
            observer.observe(el);
        });
    }

    showLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'fixed inset-0 bg-white/80 backdrop-blur-sm z-[200] flex items-center justify-center animate-fade-in';
        overlay.innerHTML = `
            <div class="text-center p-8 glass-card border-none shadow-2xl">
                <div class="w-16 h-16 border-4 border-rose-100 border-t-rose-600 rounded-full animate-spin mx-auto mb-6"></div>
                <h2 class="text-2xl font-bold gradient-text mb-2">Healing Horizons AI</h2>
                <p class="text-slate-600 animate-pulse">Analyzing your journey with empathy...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast-message bg-white border-l-4 ${type === 'success' ? 'border-green-500' : 'border-rose-500'} shadow-xl rounded-lg p-4 min-w-[300px] animate-slide-in-right flex items-center mb-3`;
        toast.innerHTML = `
            <div class="mr-3">
                <i class="fas ${type === 'success' ? 'fa-check-circle text-green-500' : 'fa-exclamation-circle text-rose-500'} text-xl"></i>
            </div>
            <div>
                <p class="text-sm font-medium text-slate-800">${message}</p>
            </div>
            <button onclick="this.parentElement.remove()" class="ml-auto text-slate-400 hover:text-slate-600">
                <i class="fas fa-times"></i>
            </button>
        `;

        container.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-x-full');
            toast.style.transition = 'all 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    }

    // Analyze Journal Entry
    async analyzeJournalEntry() {
        const textarea = document.querySelector('textarea[name="content"]');
        const content = textarea.value.trim();

        if (content.length < 5) {
            this.showToast('Please write a bit more first...', 'info');
            return;
        }

        this.showLoadingOverlay();

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]')?.value
                },
                body: JSON.stringify({ text: content })
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();

            // Map simple mood to UI mood
            const moodMap = {
                'improving': 'hopeful',
                'struggling': 'sad',
                'neutral': 'neutral'
            };

            const predictedMood = moodMap[data.mood] || 'neutral';

            // Select the mood
            const moodRadio = document.querySelector(`input[name="mood"][value="${predictedMood}"]`);
            if (moodRadio) {
                moodRadio.click(); // This will trigger the visual update
                this.showToast(`Mood detected: ${predictedMood}`, 'success');
            }

            // Show suggestions modal or toast
            this.showAnalysisResult(data);

        } catch (error) {
            console.error(error);
            this.showToast('Could not analyze text. Try again.', 'error');
        } finally {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.remove();
        }
    }

    showAnalysisResult(data) {
        // Create a modal to show results
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 bg-black/50 z-[150] flex items-center justify-center animate-fade-in px-4';
        modal.innerHTML = `
            <div class="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl animate-scale-in relative">
                <button onclick="this.closest('.fixed').remove()" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600">
                    <i class="fas fa-times text-xl"></i>
                </button>
                
                <div class="text-center mb-6">
                    <div class="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-magic text-2xl text-indigo-600"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-800">AI Insight</h3>
                    <p class="text-indigo-600 font-medium mt-1 uppercase tracking-wide text-xs">Mood: ${data.mood}</p>
                </div>
                
                <div class="space-y-4 mb-8">
                    <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                        <h4 class="font-bold text-slate-700 mb-2"><i class="fas fa-lightbulb text-yellow-500 mr-2"></i>Suggestion</h4>
                        <ul class="space-y-2 text-slate-600 text-sm">
                            ${data.next_steps.map(step => `<li class="flex items-start"><i class="fas fa-check text-green-500 mt-1 mr-2"></i>${step}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                
                <button onclick="this.closest('.fixed').remove()" class="btn-primary w-full py-3 rounded-xl">
                    Got it
                </button>
            </div>
        `;
        document.body.appendChild(modal);
    }

    exportJournal() {
        const entries = document.querySelectorAll('.journal-entry');
        if (entries.length === 0) {
            this.showToast('No entries to export', 'error');
            return;
        }

        const data = {
            metadata: {
                appName: 'Healing Horizons',
                exportedAt: new Date().toLocaleString(),
                totalEntries: entries.length
            },
            history: Array.from(entries).map(entry => ({
                date: entry.querySelector('.text-sm')?.textContent || '',
                mood: entry.querySelector('.font-medium')?.textContent || '',
                content: entry.querySelector('p')?.textContent.trim() || ''
            }))
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `healing-horizons-journal-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showToast('Journal exported successfully!');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.healingApp = new HealingHorizonsApp();
});