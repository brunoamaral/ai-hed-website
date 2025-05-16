---
title: "Training Materials for Teachers"
layout: "page"
slug: "overview"
summary: "Learn how to adopt AI in teaching through seven detailed guideline chapters."
url: /resources/training-materials-for-teachers/
---

<div class="container">
  <div class="row">
    <div class="col-lg-10 mx-auto">
      <h1 class="mb-4">Guidelines for Adopting AI in Teaching</h1>
      <p class="lead mb-5">These comprehensive guidelines help higher education teachers integrate AI effectively and responsibly into their courses. Explore each chapter to develop your understanding and skills.</p>
      <div class="form-row align-items-center mb-4">
        <div class="col">
          <div class="input-group">
            <input id="chapter-search" type="text" class="form-control" placeholder="Search chapters…">
          </div>
        </div>
        <div class="col-auto">
          <a href="/downloads/AI-HED_WP3_Guidelines_course_development_final_Feb14_2025.pdf" class="btn btn-lg btn-success font-weight-bold text-title">
            <i class="fas fa-file-pdf"></i>&nbsp; Download PDF
          </a>
        </div>
      </div>
      <div class="list-group mb-5">
        <a href="/resources/training-materials-for-teachers/objectives/" class="list-group-item list-group-item-action chapter-item" data-slug="objectives">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 1: Objectives</h5>
          </div>
          <p class="mb-1">Understanding the aims and scope of these guidelines for AI in academic education.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/impact/" class="list-group-item list-group-item-action chapter-item" data-slug="impact">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 2: The Impact of AI on Academic Education</h5>
          </div>
          <p class="mb-1">Exploring how AI is changing higher education and required teaching skills.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/pedagogical-approaches/" class="list-group-item list-group-item-action chapter-item" data-slug="pedagogical-approaches">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 3: Pedagogical Approaches</h5>
          </div>
          <p class="mb-1">Human-centered approaches to adopting AI in academic education.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/principles/" class="list-group-item list-group-item-action chapter-item" data-slug="principles">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 4: Principles of Course Design</h5>
          </div>
          <p class="mb-1">Key principles for integrating AI into your course design with a focus on constructive alignment.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/designing-courses/" class="list-group-item list-group-item-action chapter-item" data-slug="designing-courses">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 5: Designing Courses</h5>
          </div>
          <p class="mb-1">Didactical scenarios, teaching methods, assessment and grading approaches with AI.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/legal-compliance/" class="list-group-item list-group-item-action chapter-item" data-slug="legal-compliance">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 6: Legal Compliance and Ethical Responsibility</h5>
          </div>
          <p class="mb-1">Ensuring ethical and legally compliant use of AI in teaching and learning.</p>
        </a>
        <a href="/resources/training-materials-for-teachers/recommended-ai-tools/" class="list-group-item list-group-item-action chapter-item" data-slug="recommended-ai-tools">
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1">Chapter 7: Recommended AI Tools</h5>
          </div>
          <p class="mb-1">Curated list of AI tools recommended for teaching and learning.</p>
        </a>
      </div>
      <div class="card mb-5">
        <div class="card-body bg-light">
          <h3>Download Complete Guidelines</h3>
          <p>You can also download the complete guidelines as a PDF document for offline reference.</p>
          <a href="/downloads/AI-HED_WP3_Guidelines_course_development_final_Feb14_2025.pdf" class="btn btn-success">
            <i class="fas fa-file-pdf"></i> Download PDF
          </a>
        </div>
      </div>
      <div class="alert alert-info">
        <p><strong>About these guidelines:</strong></p>
        <p>These guidelines were developed in work package 3 of the AI-HED project. The author expresses gratitude and appreciation to all experts and members of the AI-HED project who have contributed to this document.</p>
        <p class="mb-0"><strong>Author:</strong> Dietmar Paier, UAS BFI Vienna</p>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('chapter-search');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      const query = e.target.value.toLowerCase();
      const chapterItems = document.querySelectorAll('.chapter-item');
      
      let matchFound = false;
      
      chapterItems.forEach(function(item) {
        const title = item.querySelector('h5').textContent.toLowerCase();
        const summary = item.querySelector('p').textContent.toLowerCase();
        
        if (title.includes(query) || summary.includes(query)) {
          item.style.display = '';
          matchFound = true;
        } else {
          item.style.display = 'none';
        }
      });
      
      // Handle no results
      const noResultsEl = document.getElementById('no-results');
      if (!matchFound && query) {
        if (!noResultsEl) {
          const alert = document.createElement('div');
          alert.id = 'no-results';
          alert.className = 'alert alert-warning mt-3';
          alert.textContent = 'No chapters found. Try different keywords.';
          document.querySelector('.list-group').after(alert);
        }
      } else if (noResultsEl) {
        noResultsEl.remove();
      }
    });
  }
});
</script>