# preCICE configuration validation rules

This checker in development for the coupling library preCICE.

Currently, through the preCICE native command `precice-tools check`, syntax and basic setup mistakes will get checked.

Our checker assumes that this command has been executed beforehand and returned without an error.
Cases that get handled beforehand do _not_ get checked by this logical checker.
Instead, we try to find _logical_ mistakes in the configuration file, which adhere to the defined syntax of
preCICE, but will lead to errors when actually running the simulation.

Here you will find an overview over all logical errors, which we refer to as 'rules', which currently get handled by our
preCICE config checker.
Our rules have been sorted into three categories of _severity_:

- `error`: These rules should be adhered to, in order to guarantee (a flawless) execution of the coupled simulation.
- `warning`: Rules in this category do not necessarily cause errors during the simulation, yet should be inspected to
  ensure the intended outcome.
- `debug`: These rules are simply hints and do not get checked or printed by default.
  Usually they do not represent mistakes but are meant to help find the most hidden bugs 🪲

Rules with `TODO` before their names have not yet been implemented but will be soon.

## Rules with severity `error`

### (1) Missing coupling-scheme

If a preCICE config.xml is missing a coupling-scheme (or a multi-coupling-scheme), then no data gets exchanged between
participants.

Since preCICE is a tool for running coupled simulations between multiple participants, not defining a coupling-scheme is
an error.

### (2) `TODO` Participant not part of a coupling-scheme

A participant needs to be part of at least one coupling scheme.

Otherwise, the participant does not exchange data and is not part of a coupled simulation, which is an error.

### (3) Participant needs to be part of an m2n exchange

In order for the two solvers to exchange data between them,
their participants have to be connected through an m2n node in the config.xml.

Otherwise, they are not partaking in the coupled simulation.

#### Participant not part of an m2n exchange

A participant needs to be part of at least one m2n data exchange to exchange data.

#### `Duplicate m2n exchange

A participant can be part of more than one m2n exchange, but an exchange between two participants is only allowed to be
defined once.

### (4) `TODO` Read- and write-data are only valid on a participants own meshes or if explicitly requested

If a participant wants to read-/write-data from or to a mesh, then he needs to know the correct positions to do so.

He knows these coordinates if the mesh is his own (`provide-mesh`) or he explicitly states that he knows them from a
received mesh (with `direct-access="true"`).

If neither is satisfied, the participant has no permission to read from or write to the mesh.

### (5) `TODO` Participant reads from/writes to mesh, but nobody writes to/reads from it

If a participant reads data from a mesh, then someone should write it beforehand.<br>
Similarly, if a participant writes data to a mesh, then someone should read from it later on.

### (6) Missing exchange

A coupling-scheme needs to have at least one exchange element. Otherwise, it is redundant.

### Compositional coupling deadlock

Participants can be "connected" through coupling-schemes.
When using `serial` couplings, the `second` participant waits for the `first`.

This means that when more than two participants get coupled in pairs of two, a circular dependency can
evolve, in which `X` waits for `Y`, `Y` waits for `Z` and `Z` for `X`, leading to a deadlock.

## Rules with severity `warning`

### (1) `TODO` Coupling-scheme without mapping

To ensure that exchanged data between one participant and its mesh to another participant and its mesh, the mapping has
to be defined.
If the mapping does not get defined, it is not certain that the meshes “fit together” and data gets exchanged
correctly.

It is possible, however, that meshes fit together naturally.

### (2) Data rules

A data element in a preCICE needs to be mentioned at many locations to finally allow it to be utilized by one or more
participants.
After declaration, data has to be:

- used in a mesh
- written by a participant
- read by a participant (or read through other means, e.g., of immediate export)
- exchanged in a coupling-scheme, if it gets written and read by different participants-

All other cases get checked here (minus the ones that get handled by `precice-tools check`).

Using, reading or writing data without the respective other tags is not as severe an error, as this data element is
likely not used in the simulation yet, due to multiple tags missing.

For the exact implementation, see `rules/data_use_read_write.py`.

#### Data gets used in a mesh, read and written by different participants, but not exchanged

The data element does not get exchanged between the participants which are accessing the data.

#### Data gets used but not written or read

The data element gets used in a mesh, but no participant is reading or writing it.

#### Data gets used and read, but not written

The data element gets used in a mesh and read by a participant (or other ways of acquiring the data), but no participant
is writing the data.

#### Data gets used and written, but not read

The data element gets used in a mesh and written by a participant, but nobody is reading it (or acquiring the data
through other means).

#### Data does not get used, read or written

The data element gets declared but not used in a mesh, read or written by any participant.

### (3) `TODO` Unused mesh

A participant can provide a mesh to another participant, who receives it but does not use it.
This means that the mesh is not used in any coupling scheme.

This does not necessarily cause the simulation to malfunction or misbehave.

## Rules with severity `debug`

### (1) `TODO` Disjoint simulations

A simulation between participants A and B and a second one between participants C and D can run simultaneously, but will
deteriorate the readability of the preCICE-config and will make it more prone to errors.

In most cases, however, running multiple “disjoint simulations” simultaneously is intended.   