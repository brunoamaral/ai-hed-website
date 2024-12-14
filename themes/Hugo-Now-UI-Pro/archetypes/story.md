---
categories: 
  - 
date: {{ .Date }}
description: ""
draft: false
resources: 
- src: images/
  name: "header"
- src: "gallery/*.jpg"
  name: gallery-:counter
  title: gallery-title-:counter
slug:
subtitle: 
tags: 
  - 
title: {{ replace .Name "-" " " | title }}
options:
  hideFooter: false
  hideSubscribeForm: true
  showHeader: true
  unlisted: false
scripts:
  - 
---