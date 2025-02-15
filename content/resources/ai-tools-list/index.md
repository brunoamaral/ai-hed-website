---
title: List of AI Tools
subtitle: Guides, Use Cases, and Other Teaching Tools
date: 2025-02-13T15:11:28Z 
draft: false
categories: 
type: "page"
disable_comments: true
summary: " "
description:
aliases:
layout: page
resources:
  - src: microsoft-365-hC_796Wu-VY-unsplash.jpg
    name: "header"
options:
  header: small
  headerHeight:
  unlisted: false
  showHeader: true
  hideSubscribeForm: false
  disable_sharebuttons: true
  hideShareButtons: true
  navbar: navbar navbar-expand-lg bg-white fixed-top font-weight-bold
  hide_date_reading_time: true

---


<div class="row">
<div class="col-10 offset-1">
{{< ai-tools path="tools.csv" caption="tools" outputFormat="html" caption="">}}
</div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
	// Find all tables with the class "database-table"
	var tables = document.querySelectorAll("table.database-table");

	tables.forEach(function (table) {
		// Find header cells and determine indices for Category, Tool, and Description
		var headerCells = table.querySelectorAll("thead th");
		var categoryIndex = -1, toolIndex = -1, descriptionIndex = -1;
		headerCells.forEach(function (th, index) {
			var headerText = th.textContent.trim().toLowerCase();
			if (headerText === "category") {
				categoryIndex = index;
			} else if (headerText === "tool") {
				toolIndex = index;
			} else if (headerText === "description") {
				descriptionIndex = index;
			}
		});

		// Collect unique categories if the Category column exists
		var rows = table.querySelectorAll("tbody tr");
		var categories = new Set();
		if (categoryIndex !== -1) {
			rows.forEach(function (row) {
				var cells = row.querySelectorAll("td");
				if (cells[categoryIndex]) {
					var cat = cells[categoryIndex].textContent.trim();
					if (cat !== "") {
						categories.add(cat);
					}
				}
			});
		}
		var categoryArray = Array.from(categories).sort();

		// Create a container for the filters using Bootstrap classes
		var filterContainer = document.createElement("div");
		filterContainer.className = "mb-3 d-flex align-items-center";

		// Create a text input filter for Tool and Description columns
		var searchInput = document.createElement("input");
		searchInput.type = "text";
		searchInput.className = "form-control";
		searchInput.placeholder = "Search Tool and Description...";
		filterContainer.appendChild(searchInput);

		// If a Category column exists, create a dropdown filter
		var categorySelect = null;
		if (categoryIndex !== -1) {
			categorySelect = document.createElement("select");
			categorySelect.className = "form-control mr-3";
			var defaultOption = document.createElement("option");
			defaultOption.value = "";
			defaultOption.textContent = "All Categories";
			categorySelect.appendChild(defaultOption);
			categoryArray.forEach(function (cat) {
				var option = document.createElement("option");
				option.value = cat;
				option.textContent = cat;
				categorySelect.appendChild(option);
			});
			filterContainer.appendChild(categorySelect);
		}

		// Insert the filter container above the table
		table.parentNode.insertBefore(filterContainer, table);

		// Filter function applies both category and text filters
		function filterRows() {
			var selectedCategory = categorySelect ? categorySelect.value : "";
			var searchText = searchInput.value.trim().toLowerCase();

			rows.forEach(function (row) {
				var cells = row.querySelectorAll("td");
				var rowCategory = (categoryIndex !== -1 && cells[categoryIndex]) ? cells[categoryIndex].textContent.trim() : "";
				var rowTool = (toolIndex !== -1 && cells[toolIndex]) ? cells[toolIndex].textContent.trim().toLowerCase() : "";
				var rowDescription = (descriptionIndex !== -1 && cells[descriptionIndex]) ? cells[descriptionIndex].textContent.trim().toLowerCase() : "";

				// Check category filter: if selected, row must match exactly
				var passesCategory = (selectedCategory === "" || rowCategory === selectedCategory);
				// Check search filter: if non-empty, at least one column must include the search term
				var passesSearch = (searchText === "" || rowTool.indexOf(searchText) !== -1 || rowDescription.indexOf(searchText) !== -1);

				// Only show the row if both conditions pass
				row.style.display = (passesCategory && passesSearch) ? "" : "none";
			});
		}

		// Listen for changes on both the dropdown and the text input
		if (categorySelect) {
			categorySelect.addEventListener("change", filterRows);
		}
		searchInput.addEventListener("input", filterRows);
	});
});
</script>