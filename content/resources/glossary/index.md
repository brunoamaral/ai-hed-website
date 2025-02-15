---
title: Glossary
subtitle: Guides, Use Cases, and Other Teaching Tools
date: 2025-02-13T15:11:28Z 
draft: false
categories: 

disable_comments: true
summary: " "
description:
aliases:

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

### To Be Available Soon

<div class="row">
<div class="col-10 offset-1">
{{< csv2table path="glossary.csv" outputFormat="html" caption="">}}
</div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
	var waitForFilters = setInterval(function () {
		if (typeof applyTableFilters === "function") {
			clearInterval(waitForFilters);
			applyTableFilters({
				tableSelector: "table.database-table",
				facetColumns: [],
				searchColumns: ["Concept"],
				searchPlaceholder: "Search concepts ..."
			});
		}
	}, 50);
});
</script>