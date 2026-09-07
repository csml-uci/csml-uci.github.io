---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
author: "{{ .Site.Params.pi_name }}"
categories: ["news"]         # e.g. "publications", "funding", "awards", "people"
# image: "/images/news/{{ .File.ContentBaseName }}.jpg"
---

Write the news item here. The first paragraph is used as the summary on the home page.
