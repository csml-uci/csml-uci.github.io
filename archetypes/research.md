---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
short_name: ""
image: "/images/research/{{ .File.ContentBaseName }}.jpg"
order: 1                     # position on the research page (1 = first)
active: true                 # false moves it to "Past Projects"
team_members:
  - ""
funding:
  - ""
description: |
  One-paragraph summary shown on the home page and the research list.
---

## Overview

Full description of the project.
