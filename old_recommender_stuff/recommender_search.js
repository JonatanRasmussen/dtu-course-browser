// Course Search Module
const CourseSearch = {
    searchTimeout: null,

    switchTab(tabName) {
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        event.target.classList.add('active');
        document.getElementById('tab-' + tabName).classList.add('active');

        if (tabName === 'search') {
            document.getElementById('bulkText').value = '';
            document.getElementById('extractedCourses').classList.add('hidden');
        } else {
            AppState.selectedCourses.clear();
            this.updateBasketDisplay();
            document.getElementById('courseSearch').value = '';
            document.getElementById('autocompleteResults').classList.remove('show');
        }
    },

    search() {
        const query = document.getElementById('courseSearch').value;

        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }

        if (query.length < 2) {
            document.getElementById('autocompleteResults').classList.remove('show');
            return;
        }

        this.searchTimeout = setTimeout(() => {
            fetch(`/search_courses?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.displayAutocompleteResults(data.results);
                    }
                })
                .catch(error => console.error('Search error:', error));
        }, 300);
    },

    displayAutocompleteResults(results) {
        const container = document.getElementById('autocompleteResults');

        if (results.length === 0) {
            container.innerHTML = '<div style="padding: 10px; color: #999;">No courses found</div>';
            container.classList.add('show');
            return;
        }

        let html = '';
        results.forEach(course => {
            if (AppState.selectedCourses.has(course.course_id)) {
                return;
            }

            html += `
                <div class="autocomplete-item" onclick="CourseSearch.addToBasket('${course.course_id}', '${course.name.replace(/'/g, "\\'")}')">
                    <div class="autocomplete-item-id">${course.course_id}</div>
                    <div class="autocomplete-item-name">${course.name}</div>
                </div>
            `;
        });

        container.innerHTML = html || '<div style="padding: 10px; color: #999;">All matching courses already selected</div>';
        container.classList.add('show');
    },

    addToBasket(courseId, courseName) {
        AppState.selectedCourses.add(courseId);
        this.updateBasketDisplay();
        document.getElementById('courseSearch').value = '';
        document.getElementById('autocompleteResults').classList.remove('show');
    },

    removeFromBasket(courseId) {
        AppState.selectedCourses.delete(courseId);
        this.updateBasketDisplay();
    },

    updateBasketDisplay() {
        const basket = document.getElementById('courseBasket');

        if (AppState.selectedCourses.size === 0) {
            basket.className = 'course-basket empty';
            basket.innerHTML = 'Click courses from search results to add them here';
            return;
        }

        basket.className = 'course-basket';
        let html = '';
        AppState.selectedCourses.forEach(courseId => {
            html += `
                <span class="basket-item">
                    ${courseId}
                    <span class="basket-item-remove" onclick="CourseSearch.removeFromBasket('${courseId}')">✕</span>
                </span>
            `;
        });
        basket.innerHTML = html;
    },

    extractCourses() {
        const text = document.getElementById('bulkText').value;

        if (!text.trim()) {
            AppState.showError('Please paste some text containing course codes');
            return;
        }

        fetch('/extract_courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.displayExtractedCourses(data.courses);
                } else {
                    AppState.showError(data.error);
                }
            })
            .catch(error => AppState.showError('Error: ' + error));
    },

    displayExtractedCourses(courses) {
        const container = document.getElementById('extractedCourses');

        if (courses.length === 0) {
            container.innerHTML = '<div style="padding: 10px; color: #c62828;">No valid course codes found in the text.</div>';
            container.classList.remove('hidden');
            return;
        }

        AppState.selectedCourses.clear();
        courses.forEach(course => AppState.selectedCourses.add(course.course_id));

        let html = `<div style="font-weight: bold; margin-bottom: 10px;">Found ${courses.length} course(s):</div>`;
        courses.forEach(course => {
            html += `<div class="extracted-course-item">✓ ${course.course_id} - ${course.name}</div>`;
        });

        container.innerHTML = html;
        container.classList.remove('hidden');
    }
};