// Main Application State and Coordination
const AppState = {
    selectedCourses: new Set(),
    allRecommendations: [],
    displayedCount: 0,
    currentViewMode: 'scroll', // 'carousel' or 'scroll'
    DISPLAY_INCREMENT: 10,

    getSelectedFilters() {
        let filters = {};
        let selected = [];
        let checkboxes = document.querySelectorAll('input[name="course_type"]:checked');
        checkboxes.forEach(cb => selected.push(cb.value));
        if (selected.length > 0) {
            filters['course_type'] = selected;
        }
        return filters;
    },

    getRecommendations() {
        const filters = this.getSelectedFilters();
        const activeTab = document.querySelector('.tab-content.active').id;
        let courseIds = Array.from(this.selectedCourses);

        if (courseIds.length === 0) {
            this.showError('Please select at least one course');
            return;
        }

        const btn = document.getElementById('submitBtn');
        btn.disabled = true;
        btn.textContent = 'Loading...';
        document.getElementById('results').innerHTML = '<p class="loading">Generating recommendations...</p>';

        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                course_ids: courseIds,
                n_recommendations: 100,
                filters: filters
            })
        })
            .then(response => response.json())
            .then(data => {
                btn.disabled = false;
                btn.textContent = 'Get Recommendations';
                if (data.success) {
                    this.allRecommendations = data.recommendations;
                    this.displayedCount = 0;
                    ResultsDisplay.render(data);
                } else {
                    this.showError(data.error);
                }
            })
            .catch(error => {
                btn.disabled = false;
                btn.textContent = 'Get Recommendations';
                this.showError('Error: ' + error);
            });
    },

    showError(message) {
        document.getElementById('results').innerHTML =
            `<div class="error"><strong>Error:</strong> ${message}</div>`;
    }
};

// Event Listeners
document.addEventListener('click', function (e) {
    if (!e.target.closest('.search-container')) {
        document.getElementById('autocompleteResults').classList.remove('show');
    }
});

document.addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && e.target.id === 'courseSearch') {
        e.preventDefault();
        const firstResult = document.querySelector('.autocomplete-item');
        if (firstResult) {
            firstResult.click();
        }
    }
});

document.addEventListener('keydown', function (e) {
    const resultsVisible = document.getElementById('carouselTrack') !== null;
    if (!resultsVisible) return;

    if (e.key === 'ArrowLeft') {
        CarouselView.move(-1);
    } else if (e.key === 'ArrowRight') {
        CarouselView.move(1);
    }
});