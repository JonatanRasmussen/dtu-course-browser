// Results Display Module
const ResultsDisplay = {
    render(data) {
        if (AppState.allRecommendations.length === 0) {
            document.getElementById('results').innerHTML =
                '<div class="results"><p>No recommendations found matching your criteria.</p></div>';
            return;
        }

        let html = '<div class="results">';

        // Header
        html += '<h2>Course Recommendations</h2>';
        html += '<div class="info-box">';
        html += `<strong>Based on courses:</strong> ${data.input_courses.join(', ')}<br>`;

        if (Object.keys(data.filters_applied).length > 0) {
            html += '<strong>Filters applied:</strong> ';
            html += Object.entries(data.filters_applied)
                .map(([k, v]) => `${k}: ${v.join(', ')}`)
                .join(' | ');
        } else {
            html += '<strong>No filters applied</strong>';
        }

        html += `<br><strong>Total matches:</strong> ${AppState.allRecommendations.length >= 100 ? '100+' : AppState.allRecommendations.length}`;
        html += '</div>';

        // View toggle
        html += '<div class="view-toggle-container">';
        html += '<span style="margin-right: 10px; font-weight: bold;">View Mode:</span>';
        html += `<button id="view-carousel" class="view-toggle-btn ${AppState.currentViewMode === 'carousel' ? 'active' : ''}"
                         onclick="ResultsDisplay.switchViewMode('carousel')">🎠 Carousel View</button>`;
        html += `<button id="view-scroll" class="view-toggle-btn ${AppState.currentViewMode === 'scroll' ? 'active' : ''}"
                         onclick="ResultsDisplay.switchViewMode('scroll')">📜 Scroll List View</button>`;
        html += '</div>';

        // Carousel container
        html += `<div id="carouselView" style="display: ${AppState.currentViewMode === 'carousel' ? 'block' : 'none'};">`;
        html += CarouselView.generateHTML();
        html += '</div>';

        // Scroll list container
        html += `<div id="scrollView" style="display: ${AppState.currentViewMode === 'scroll' ? 'block' : 'none'};">`;
        html += ScrollListView.generateHTML(true);
        html += '</div>';

        html += '</div>';

        document.getElementById('results').innerHTML = html;

        if (AppState.currentViewMode === 'carousel') {
            CarouselView.init();
        }
    },

    switchViewMode(mode) {
        if (mode !== 'carousel' && mode !== 'scroll') return;

        AppState.currentViewMode = mode;

        document.getElementById('view-carousel').classList.remove('active');
        document.getElementById('view-scroll').classList.remove('active');
        document.getElementById(`view-${mode}`).classList.add('active');

        const carouselView = document.getElementById('carouselView');
        const scrollView = document.getElementById('scrollView');

        if (mode === 'carousel') {
            carouselView.style.display = 'block';
            scrollView.style.display = 'none';
            CarouselView.init();
        } else {
            carouselView.style.display = 'none';
            scrollView.style.display = 'block';
            try {
                window.removeEventListener('resize', CarouselView.handleResize);
            } catch (e) { }
        }
    }
};

// Carousel View
const CarouselView = {
    state: {
        currentIndex: 0,
        itemsPerView: 3
    },

    generateHTML() {
        let html = '<div class="carousel-container">';
        html += '<div class="carousel-wrapper">';
        html += '<button class="carousel-button carousel-button-prev" onclick="CarouselView.move(-1)">&#10094;</button>';
        html += '<div class="carousel-track" id="carouselTrack">';

        AppState.allRecommendations.forEach((course, index) => {
            html += `
                <div class="carousel-item">
                    <div class="course-card">
                        <div class="course-header">
                            <span class="course-id">${index + 1}. ${course.course_id}</span>
                            <span class="similarity-score">${course.similarity}</span>
                        </div>
                        <div class="course-name">${course.name}</div>
                        <div class="course-meta">
                            📚 ${course.ects} ECTS | 🏛️ ${course.institute}
                        </div>
                        <div class="course-description">${course.description || 'No description available'}</div>
                        <a href="https://kurser.dtu.dk/course/${course.course_id}"
                           target="_blank"
                           rel="noopener noreferrer"
                           class="course-link">Visit Official Page</a>
                    </div>
                </div>
            `;
        });

        html += '</div>';
        html += '<button class="carousel-button carousel-button-next" onclick="CarouselView.move(1)">&#10095;</button>';
        html += '</div>';
        html += '<div class="carousel-dots" id="carouselDots"></div>';
        html += '<div class="carousel-counter" id="carouselCounter"></div>';
        html += '</div>';

        return html;
    },

    init() {
        this.state.currentIndex = 0;
        this.updateItemsPerView();
        this.createDots();
        this.update();
        window.addEventListener('resize', this.handleResize.bind(this));
    },

    updateItemsPerView() {
        const width = window.innerWidth;
        if (width <= 600) {
            this.state.itemsPerView = 1;
        } else if (width <= 900) {
            this.state.itemsPerView = 2;
        } else {
            this.state.itemsPerView = 3;
        }
    },

    handleResize() {
        const oldItemsPerView = this.state.itemsPerView;
        this.updateItemsPerView();
        if (oldItemsPerView !== this.state.itemsPerView) {
            this.state.currentIndex = 0;
            this.createDots();
            this.update();
        }
    },

    createDots() {
        const dotsContainer = document.getElementById('carouselDots');
        if (!dotsContainer) return;

        const totalPages = Math.ceil(AppState.allRecommendations.length / this.state.itemsPerView);
        let html = '';

        for (let i = 0; i < totalPages; i++) {
            html += `<div class="carousel-dot ${i === 0 ? 'active' : ''}"
                          onclick="CarouselView.goToPage(${i})"></div>`;
        }

        dotsContainer.innerHTML = html;
    },

    move(direction) {
        const totalPages = Math.ceil(AppState.allRecommendations.length / this.state.itemsPerView);
        this.state.currentIndex += direction;

        if (this.state.currentIndex < 0) {
            this.state.currentIndex = 0;
        } else if (this.state.currentIndex >= totalPages) {
            this.state.currentIndex = totalPages - 1;
        }

        this.update();
    },

    goToPage(pageIndex) {
        this.state.currentIndex = pageIndex;
        this.update();
    },

    update() {
        const track = document.getElementById('carouselTrack');
        const dots = document.querySelectorAll('.carousel-dot');
        const counter = document.getElementById('carouselCounter');

        if (!track) return;

        const itemWidth = 100 / this.state.itemsPerView;
        const translateX = -(this.state.currentIndex * itemWidth * this.state.itemsPerView);
        track.style.transform = `translateX(${translateX}%)`;

        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.state.currentIndex);
        });

        const startItem = this.state.currentIndex * this.state.itemsPerView + 1;
        const endItem = Math.min((this.state.currentIndex + 1) * this.state.itemsPerView,
            AppState.allRecommendations.length);

        if (counter) {
            counter.textContent = `Showing ${startItem}-${endItem} of ${AppState.allRecommendations.length}`;
        }

        const prevBtn = document.querySelector('.carousel-button-prev');
        const nextBtn = document.querySelector('.carousel-button-next');
        const totalPages = Math.ceil(AppState.allRecommendations.length / this.state.itemsPerView);

        if (prevBtn) {
            prevBtn.disabled = this.state.currentIndex === 0;
        }
        if (nextBtn) {
            nextBtn.disabled = this.state.currentIndex >= totalPages - 1;
        }
    }
};

// Scroll List View
const ScrollListView = {
    generateHTML(initialLoad = true) {
        let html = '<div class="scroll-list-container">';
        html += '<div class="scroll-list" id="scrollList">';

        const endIndex = initialLoad ?
            Math.min(AppState.DISPLAY_INCREMENT, AppState.allRecommendations.length) :
            AppState.displayedCount;

        const coursesToShow = AppState.allRecommendations.slice(0, endIndex);

        coursesToShow.forEach((course, index) => {
            html += `
                <div class="course-card">
                    <div class="course-header">
                        <span class="course-id">${index + 1}. ${course.course_id}</span>
                        <span class="similarity-score">Similarity: ${course.similarity}</span>
                    </div>
                    <div class="course-name"><strong>${course.name}</strong></div>
                    <div class="course-meta">
                        📚 ECTS: ${course.ects} | 🏛️ Institute: ${course.institute}
                    </div>
                    <div class="course-description">${course.description || 'No description available'}</div>
                    <a href="https://kurser.dtu.dk/course/${course.course_id}"
                       target="_blank"
                       rel="noopener noreferrer"
                       class="course-link">View Course Details</a>
                </div>
            `;
        });

        html += '</div>';

        if (endIndex < AppState.allRecommendations.length) {
            html += `
                <button onclick="ScrollListView.loadMore()" class="btn-load-more">
                    Load More (${AppState.allRecommendations.length - endIndex} remaining)
                </button>
            `;
        } else if (AppState.allRecommendations.length > AppState.DISPLAY_INCREMENT) {
            html += '<div style="text-align: center; padding: 20px; color: #666;">All recommendations displayed</div>';
        }

        html += '</div>';

        if (initialLoad) {
            AppState.displayedCount = endIndex;
        }

        return html;
    },

    loadMore() {
        const endIndex = Math.min(
            AppState.displayedCount + AppState.DISPLAY_INCREMENT,
            AppState.allRecommendations.length
        );

        const coursesToAdd = AppState.allRecommendations.slice(AppState.displayedCount, endIndex);

        let html = '';
        coursesToAdd.forEach((course, index) => {
            const actualIndex = AppState.displayedCount + index + 1;
            html += `
                <div class="course-card">
                    <div class="course-header">
                        <span class="course-id">${actualIndex}. ${course.course_id}</span>
                        <span class="similarity-score">Similarity: ${course.similarity}</span>
                    </div>
                    <div class="course-name"><strong>${course.name}</strong></div>
                    <div class="course-meta">
                        📚 ECTS: ${course.ects} | 🏛️ Institute: ${course.institute}
                    </div>
                    <div class="course-description">${course.description || 'No description available'}</div>
                    <a href="https://kurser.dtu.dk/course/${course.course_id}"
                       target="_blank"
                       rel="noopener noreferrer"
                       class="course-link">View Course Details</a>
                </div>
            `;
        });

        const scrollView = document.getElementById('scrollView');
        const oldButton = scrollView.querySelector('.btn-load-more');
        if (oldButton) {
            oldButton.remove();
        }

        const scrollList = document.getElementById('scrollList');
        scrollList.insertAdjacentHTML('beforeend', html);

        AppState.displayedCount = endIndex;

        if (AppState.displayedCount < AppState.allRecommendations.length) {
            const newButton = document.createElement('button');
            newButton.className = 'btn-load-more';
            newButton.onclick = () => this.loadMore();
            newButton.textContent = `Load More (${AppState.allRecommendations.length - AppState.displayedCount} remaining)`;
            scrollView.querySelector('.scroll-list-container').appendChild(newButton);
        } else {
            const endMessage = document.createElement('div');
            endMessage.style.cssText = 'text-align: center; padding: 20px; color: #666;';
            endMessage.textContent = 'All recommendations displayed';
            scrollView.querySelector('.scroll-list-container').appendChild(endMessage);
        }
    }
};