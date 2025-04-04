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

### (7) Compositional coupling deadlock

Participants can be "connected" through coupling-schemes.
When using `serial` couplings, the `second` participant waits for the `first`.

This means that when more than two participants get coupled in pairs of two, a circular dependency can
evolve, in which `X` waits for `Y`, `Y` waits for `Z` and `Z` for `X`, leading to a deadlock.

### (8) Mappings

Mappings are a central component of preCICE configs. They define how data is exchanged between two participants. 
It gets specified by a participant (here "Parent") and defines how data from Parent's mesh gets mapped to a different 
participants mesh (here "Stranger"), or vice versa.

A mapping has a type (specified in `<mapping:type .../>`), a direction (`read` or `write`), an origin-mesh (specified 
by tag `from="..."`), a destination mesh (specified by tag `to="..."`) and a constraint (`consistent`, `conservative`, 
`scaled-consistent-surface` or `scaled-consistent-volume`).

The combination of direction and constraint will be referred to as "format" here.

There are two main kinds of mappings: regular mappings and "just-in-time" (JIT) mappings. For JIT mappings, Parent can
directly access Stranger's mesh, meaning there is no need to define a mesh of Parent to map the values from Stranger's 
mesh to.

#### JIT mapping without permission

A JIT mapping is only valid, if Parent receives Stranger's mesh with the attribute `api-access="true"`.

#### JIT mapping has a wrong type

For JIT mappings, only the types `nearest-neighbor`, `rbf-pum-direct` and `rbf` are supported.

#### JIT mapping has a wrong format

For JIT mappings, only the formats `write-conservative` and `read-consistent` are supported.
A `read-conservative` mapping can be achieved by switching the direction to `write` and moving the mapping from Parent
to Stranger. This also works to achieve a `write-consistent` mapping.

#### JIT mapping is in the wrong direction

If the direction is `read`, then the JIT mapping needs to have the tag `from="..."`. If it instead has the tag `to="..."`, 
then direction and tag don't fit and the mapping is in the wrong direction.

Similarly, a JIT `write`-mapping needs to have the tag `to="..."`, otherwise its direction is wrong.

#### JIT mapping is in the wrong direction and has a wrong format

This comprises both "JIT mapping has a wrong format" and "JIT mapping is in the wrong direction".

#### JIT mapping is missing data processing

Parent declares a read-mapping, but does not read from the corresponding mesh, i.e., Parent has no `read-data` element,
that reads from Stranger's mesh specified in the mapping.

Similarly, if Parent declares a write-mapping, a `write-data` element should exist, that writes data to Stranger's mesh 
as specified in the mapping.

#### Mapping is in the wrong direction

For a "regular" mapping, the direction `read` means, that Parent wants to read data from Stranger's mesh. 
For this to work, data from Stranger's mesh has to be mapped to Parent's mesh. 
This means, the `from="..."`-mesh has to be by Stranger and the `to="..."`-mesh has to be by Parent.
If the from-mesh is _not_ by Stranger and the to-mesh not by Parent, then the direction is wrong. 

Similarly, a `write`-mapping means that Parent wants to write data to Stranger's mesh. 
For this to work, data from Parent's mesh has to be mapped to Stranger's mesh.
This means, the `from="..."`-mesh has to be by Parent and the `to="..."`-mesh has to be by Parent.
Otherwise, the direction of the mapping is wrong.

#### Mapping between parallel participants has a wrong format

Participants which are coupled with a parallel coupling-scheme 
(i.e., coupling-schemes of types `parallel-explicit`, `parallel-implicit` and `multi`) face the same format restrictions
as JIT mappings: Only the formats `read-consistent` and `write-conservative` are supported.

#### Mapping is missing data processing

Parent declares a read-mapping, but does not read from the corresponding mesh, i.e., Parent has no `read-data` element, 
that reads from Parent's own mesh as specified in the mapping.

Similarly, if Parent declares a write-mapping, a `write-data` element should exist, writing to Parent's mesh as 
specified in the mapping.

#### Participants of mapping have no m2n exchange

A mapping between two participants only specifies how to map data between their meshes, but does not exchange it.
In order for the data-exchange to work, both participants have to exchange data via an M2N exchange.

#### Participants of mapping have no coupling-scheme

In order for the exchange to work, both participants have to exchange data via a coupling-scheme.

#### Participants of mapping have no data-exchange

Even if both participants share a common coupling scheme, it is not guaranteed, that they exchange data in it via an
`<exchange data="..." from="..." to="..."/>` tag. 

#### Participants of mapping have no correct data-exchange

Even if both participants share a common coupling scheme with a data-exchange, it is not guaranteed that they 
exchange data in correctly via an `<exchange data="..." mesh="..." from="..." to="..." />` tag.

For any mapping, the participants specifying the `to="..."`- and `from="..."`-meshes in the mapping have to be the
`to="..."`- and `from="..."`-participants in the exchange.
The mesh used in the exchange should be Stranger's mesh, 
otherwise, there exists no correct data-exchange between the participants.

#### Mesh in mapping is not provided by any participant

A mesh in a mapping does not get provided by any participant.

#### Mesh in mapping gets provided by multiple participants

A mesh in a mapping gets provided by multiple participants.

#### Mapping is between the same participant

Both meshes in the mapping get provided by the same participant.

## Rules with severity `warning`

### (1) `TODO` Coupling-scheme without mapping

To ensure that exchanged data between one participant and its mesh to another participant and its mesh, a mapping has
to be defined.


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