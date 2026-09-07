---
title: "Energetic Mesh Smoothing"
short_name: "Mesh Smoothing"
image: "/images/research/mesh-smoothing.jpg"
order: 4
active: true
team_members:
  - "Kevin Garanger"
  - "Alejandro Mota (Sandia National Laboratories)"
  - "James W. Foulk III (Sandia National Laboratories)"
funding:
  - "Sandia National Laboratories, Mar 2024 – Sep 2026"
description: |
  Finite element meshes of complex geometries often contain badly shaped elements. In collaboration with Sandia National Laboratories, this project treats mesh improvement as an energy minimization problem, in which every element is pulled toward an ideal shape by a pseudo-strain energy that grows without bound as the element degenerates.
---

## Abstract

This project treats mesh improvement as an energy minimization problem. Each element of a finite element mesh is paired with an ideal reference element, and a hyperelastic pseudo-strain energy penalizes both its distortion and its change of volume, so that general-purpose finite element solvers can be used to smooth the mesh. A family of pseudo-energy densities inspired by the Seth–Hill generalized strains can be tuned to penalize disproportionately the worst elements in a mesh, which are the ones most detrimental to simulation stability, and grows without bound as an element degenerates, so that element inversion is impossible by construction. The same energy drives discrete topological operations, such as element swaps and edge splits and collapses, and accommodates spatially varying size fields and anisotropic adaptation through a modified metric. On three-dimensional meshes containing highly distorted elements, the method substantially improves mesh quality and consistently outperforms established smoothing techniques from the Cubit meshing library.

## Related publications

- K. Garanger, A. Mota, J. W. Foulk III, and J. J. Rimoli, *Variational mesh smoothing via pseudo-strain energy minimization*, Computer Methods in Applied Mechanics and Engineering 458, 119033 (2026). [Details](/publications/#garanger2026j)
