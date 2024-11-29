---
authors:
  - bruno-amaral
date: {{ .Date }}
description: ""
draft: false
resources: 
- src: images/
  name: "header"
- src:
  name: slide-1
slug:
subtitle: 
tags: 
  - 
categories: 
  - 
title: "{{ replace (getenv "SLUG") "-" " " | title }}"

options:
  unlisted: false
  showHeader: true
  hideFooter: false
  hideSubscribeForm: false
  header:
scripts:
  -
---
