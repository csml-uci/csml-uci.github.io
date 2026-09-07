---
title: "Impact of Solid Propellant Microstructure on Effective Behavior: a Data-Driven Perspective"
short_name: "Solid Propellants"
image: "/images/research/solid-propellant.png"
order: 1
active: true
team_members:
  - "Lorenzo Canton"
funding:
  - "Air Force Office of Scientific Research (AFOSR), Aug 2026 – Jun 2030"
  - "Preceding project: Data-Driven Homogenization of Solid Propellants, AFOSR, Dec 2023 – Jun 2025"
description: |
  This research uses interpretable machine learning and mesoscale simulations to identify the microstructural features that govern the effective thermomechanical behavior of solid rocket propellants.
---

## Abstract

This research seeks to elucidate the relationships between microstructural features at the mesoscale and the effective thermomechanical behavior of solid rocket propellants through a novel data-driven multiscale modeling framework. Conventional approaches to microstructural homogenization, including theoretical and phenomenological models, often depend on restrictive assumptions that limit their applicability to complex, heterogeneous materials, while direct numerical simulations, though accurate, are computationally intractable for large-scale applications. Even advanced surrogate models trained on simulation data face limitations in generalizability and interpretability, as identical microstructural parameters can yield markedly different effective responses due to uncharacterized microstructural variability. The central hypothesis of this work is that interpretable, low-dimensional features governing the effective behavior of heterogeneous materials can be discovered via machine learning models trained on high-fidelity simulation data. To this end, we integrate mesoscale finite element simulations of representative volume elements with symmetry-preserving neural network architectures conditioned on latent representations extracted from microstructural images. Interpretability is achieved through a combination of spatial attribution techniques and correlation analysis between latent variables and physical descriptors such as porosity, inclusion morphology, and distribution metrics. The resulting framework yields computationally efficient, physically informed surrogate constitutive models capable of predicting the behavior of solid propellants across a broad design space, generating new knowledge on the core features of a microstructure that dictate its effective behavior, while also enabling scalable, high-fidelity simulations at the engineering scale.

## Related publications

- H. Logarzo, G. Capuano, and J. J. Rimoli, *Smart constitutive laws: Inelastic homogenization through machine learning*, Computer Methods in Applied Mechanics and Engineering (2021). [Details](/publications/#logarzo2021j)
- K. Garanger, J. Kraus, and J. J. Rimoli, *Symmetry-enforcing neural networks with applications to constitutive modeling*, Extreme Mechanics Letters (2024). [Details](/publications/#garanger2024j)
- K. A. Hart and J. J. Rimoli, *Generation of statistically representative microstructures with direct grain geometry control*, Computer Methods in Applied Mechanics and Engineering (2020). [Details](/publications/#hart2020j)
