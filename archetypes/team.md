---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
# Roles that get their own section on the team page: "PhD Student", "MS Student",
# "Undergraduate Student", "Postdoc", "Project Scientist", "Research Scientist",
# "Visiting Scholar". Any other role is listed under "Other Members".
role: "PhD Student"
status: "current"            # "current" or "alumni"
year_joined: {{ now.Year }}
# image: "/images/team/{{ .File.ContentBaseName }}.jpg"   # square JPG in static/images/team/
email: ""
# website: "https://..."
# github: "username"
# scholar: "GoogleScholarID"
interests:
  - ""
# For alumni, add:
# year_left: 2030
# current_position: "Assistant Professor at ..."
# thesis_title: "..."
---
