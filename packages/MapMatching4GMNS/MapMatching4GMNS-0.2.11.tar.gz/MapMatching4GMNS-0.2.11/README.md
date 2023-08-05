# MapMatching2GMNS

Please send your comments to [xzhou74@asu.edu](mailto:xzhou74@asu.edu) if you
have any suggestions and questions.

Based on input network and given GPS trajectory data, the map-matching program
of MapMatching4GMNS aims to find the most likely route in terms of node sequence
in the underlying network, with the following data flow chart.

Test Python Script:
<https://github.com/xiaomo123zk/MapMatching4GMNS-0.2/tree/main/MapMatching4GMNS.ipynb>

[GMNS: General Modeling Network Specification
(GMNS)](https://github.com/zephyr-data-specs/GMNS)

## Installation

MapMatching4GMNS has been released on
[PyPI](https://test.pypi.org/project/MapMatching4GMNS/), and can be installed
using

\$ pip install MapMatching4GMNS

If you need a specific version of MapMatching4GMNS, say, 0.2.9,

\$ pip **install** MapMatching4GMNS==0.2.9 --upgrade

## Dependency: An environment that needs to be installed in advance for the code to run normally

**Windows Users**  
You do not need to install Microsoft Visual C++ Redistributable for Visual
Studio; only copy the missing dependency libraries from the
Dependent_libraries_missing_in_windows_system folder to your computer
path(C:\\Windows\\System32).  
Note: If your windows system has existed some dependencies in the
C:\\Windows\\System32, you only need to copy the dependency libraries that are
not.

## Getting Started

### Download the Test Data Set

A sample data set with six different networks are provided. You can manually
retrieve each individual test network from
[here](https://github.com/asu-trans-ai-lab/osm_test_data_set//datasets/map_matchindata).from
MapMatching4GMNS import \*

\# first, **check** your operation system.

\# **If** you run the code **on** windows system without installed C++
environment,

\# **some** necessary dependency libraries need **to** be copied.

\# **If** an error occurs: Permission denied: 'C:/Windows/System32/\*.dll',

\# you need **to** manually copy the dependency library from
https://github.com/xiaomo123zk/MapMatching4GMNS-0.2/tree/main/Dependent_libraries_missing_in_windows_system

\#First, download the **input data** of the test: node.csv, link.csv and
trace.csv from Github.

MapMatching4GMNS.download_sample_data_sets_from\_network()

\#If the online download fails**,** Please download manually the **input**
**data** **from**
<https://github.com/asu-trans-ai-lab/osm_test_data_set/map_matching/>.

\#Second, **call** the mapmatching4gmns library **to** calculate **and**
**output** the result **in** the **current** directory.

MapMatching4GMNS.map\_match()

## The calculation process of MapMatching2GMNS

1.  **Data flow**

| **Input files** | **Output files**      |
|-----------------|-----------------------|
| node.csv        | intput_agent.csv      |
| link.csv        | agent.csv             |
| trace.csv       | agent_performance.csv |

1.  **Read standard GMNS network files** node and link files

2.  **Read GPS trace.csv** file Note: the M2G program will convert trace.csv to
    input_agent.csv for visualization in NeXTA.

3.  **Construct 2d grid system** to speed up the indexing of GSP points to the
    network. For example, a 10x10 grid for a network of 100 K nodes could lead
    to 1K nodes in each cell.

4.  **Identify the related subarea** for the traversed cells by each GPS trace,
    so only a small subset of the network will be loaded in the resulting
    shortest path algorithm.

5.  **Identify the origin and destination** nodes in the grid for each GPS
    trace, in case, the GPS trace does not start from or end at a node inside
    the network (in this case, the boundary origin and destination nodes will be
    identified). The OD node identification is important to run the following
    shortest path algorithm.

6.  **Estimate link cost** to calculate a generalized weight/cost for each link
    in the cell, that is, the distance from nearly GPS points to a link inside
    the cell.

7.  Use **likely path finding algorithm** selects the least cost path with the
    smallest generalized cumulative cost from the beginning to the end of the
    GPS trace.

8.  **Identify matched timestamps** of each node in the likely path

9.  **Output agent file** with **map-matched node sequence** and time sequence

10. **Output link performance** with **estimated link travel time and delay**
    based on free-flow travel time of each link along the GPS matched routes

11. **Input file description**

    **File node.csv** gives essential node information of the underlying
    (subarea) network in GMNS format, including node_id, x_coord and y_coord.

**File link.csv** provides essential link information of the underlying
(subarea) network, including link_id, from_node_id and to_node_id.

**Input trace file** as

The agent id is GPS trace id, x_coord and y_coord should be consistent to the
network coordinate defined in node.csv and link.cvs. Fields hh mm and ss
correspond the hour, minute and second for the related GPS timestamp. We use
separate columns directly to avoid confusion caused by different time coding
formats.

<https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>

1.  **Output file description**

>   **File agent.csv** describes the most-likely path for each agent based on
    input trajectories.

![](media/caec124ffd9a88d841b924a0dda3d3b7.png)

>   **File agent_performance.csv**.

![](media/211a0e9e0dbea63be67ee32304c6a17c.png)

The first visualization tool **NeXTA**: the original input_agent.csv and
resulting agent.csv can be visualized through NeXTA.

1.  Load the network node.csv and click on the following 4 buttons or menu check
    box.

1.  The original GPS trace is shown in green and the map-matched route in the
    network is displayed in purple. The user can use the scroll wheel of the
    mouse to zoom in the focused area.

The first visualization tool **QGIS**: the original input_agent.csv and
resulting agent.csv, link_performance.csv can be visualized through QGIS**.**

>   Note: The QGIS is a free and open source geographic information system. You
>   need to install QGIS on your computer in advance. The official download
>   address is <https://qgis.org/en/site/forusers/download.html>.

1.  Double click the QGIS.qgz in the "release" folder, which is the QGIS
    project, where the node, link, agent, trace, and background map have been
    loaded in QGIS.

![](media/467df57df4bad617baa567f88fe7b79f.png)

1.  The original GPS trace is shown in red point, the node is shown in purple
    point, and the agent is shown in continuous red curve.

![](media/14f8cb054120946e92fae6a1b819c1b5.png)

1.  The link_performance.csv is loaded in QGIS as the layer, and the map-matched
    route in the network is displayed in a continuous red curve, as the topo
    main road. The user can use the scroll wheel of the mouse to zoom in the
    focused area.

The process is shown in the figure below:

![](media/708d0b3f8db3cfd491182d58fe54b956.png)
![](media/9c9d1b3422fe793bb64c89fb4c625ebb.png)

![](media/609bda211a703f1a9491a69db8ec4097.png)

![](media/93d63af8ecb6e6bd5847ee84c53bb7e2.png)

**Reference:**

This code is implemented based on a published paper in Journal of Transportation
Research Part C:

Estimating the most likely space–time paths, dwell times and path uncertainties
from vehicle trajectory data: A time geographic method

<https://www.sciencedirect.com/science/article/pii/S0968090X15003150>
