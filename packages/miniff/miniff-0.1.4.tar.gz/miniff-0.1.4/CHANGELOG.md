# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

+ Gateways to most common workflows through ``python -m miniff jobs.yml``, ``ml_util.fit(...)``, and others.
+ Introduce descriptor fidelity as a part of the machine-learning potential.
+ ``ScalarFunctionWrapper`` as atomic dynamics interface.
+ More functional forms of descriptors.

### Fixed

+ API reference in docs
+ Switched to pytest, warning fixes, misc.

## [0.1.3] - 2021-04-07

### Added

+ Potential kernel infrastructure in ``potentials`` and ``_potentials``. From now on, each potential kernel "knows" the kernel type it computes by means
  of the ``potentials.PotentialKernel`` class. Added the support of "non-resolving" potentials which provide total energy only rather than individual
  energy contributions.
+ ``ewald`` module, ``potentials.ewald_*_potential_family`` and ``potentials.ewald_charge_wrapper_potential_family`` for computing non-local Coulomb
  interactions (also using neural networks or any other intermediate potentials computing charge).
+ Computing angular distribution functions through ``kernel.NeighborWrapper.adf``.

### Fixed

+ Determining neighbors in ``kernel.NeighborWrapper`` is now automated based on cutoff arguments. That said, no need to specify the ``x`` argument 
  (neighbor counts).
+ Reworked and added more workflow scenarios in ``ml_util``. From now on, arbitrary dataset errors can be tracked at the same time (not only train and
  test).
+ Package versions, tests, misc.

### Removed

+ Class ``ml.SequentialSoleEnergyNN``. From now on ``torch.nn.Sequential`` and other standard torch modules can be used directly. The default
  configuration of former ``ml.SequentialSoleEnergyNN`` is now found in ``ml_utils.behler_nn`` returning ``torch.nn.Sequential``.
+ ``examples`` is no longer the part of the package. Tutorials in the documentation replace them.
+ ``ArrayWithUnits`` was removed. All tensors and numerical values now exist without units context and it is the user's responsibility to be units-aware,
  especially when saving and loading data across different runs.

## [0.1.2] - 2021-03-09

### Fixed

+ Pinning of the patch version number of the packages, i.e., the dependencies of miniff, has been removed. Not fixing the patch version number facilitates receiving bug fixes for individual packages by requirements.txt/env.yml and update the environment during the installation. The overall consistency is still maintained as the major and minor version numbers continue to remain fixed.

## [0.1.1] - 2021-02-23

### Fixed

+ Updated the installation section in the README to capture the single command installation via pip. Users who wish to install and use miniff can use `pip install miniff` instead of setting up a development environment explicitly.

## [0.1.0] - 2021-02-15

### Added

+ Initial development version

