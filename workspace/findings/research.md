## IonQ Opens New Quantum Computing R&D Lab in Colorado

**Source URL**: https://www.hpcwire.com/off-the-wire/ionq-opens-new-quantum-computing-rd-lab-in-colorado/  
**Published Date**: Wed, 13 May 2026 13:00:10 +0000  
**Source Credibility**: [High Credibility]  

### Summary  
IonQ, a leading provider of trapped‑ion quantum processors, has inaugurated a new laboratory complex in Boulder, Colorado. The facility is designed to support advanced quantum computing research and semiconductor chip testing, focusing on the development and refinement of technologies that will underpin future generations of IonQ’s quantum systems. The lab will house state‑of‑the‑art cryogenic infrastructure, precision laser delivery systems, and high‑throughput semiconductor fabrication tools. It is intended to accelerate the transition from prototype qubit devices to scalable, fault‑tolerant quantum processors.

Key technical aspects include:
- **Trapped‑ion architecture**: Continued use of laser‑cooled ions as qubits, with improved laser stability and reduced motional heating.
- **Cryogenic integration**: Enhanced cryogenic platforms to lower thermal noise and increase qubit coherence times.
- **Semiconductor chip testing**: Dedicated testbeds for integrated photonics and ion‑trap chip fabrication, enabling rapid iteration of qubit control electronics.
- **Scalability focus**: Design of modular qubit modules that can be tiled to increase qubit counts while maintaining error rates below the surface‑code threshold.

### Operational Impact  
For HPC administrators, the expansion signals a growing convergence between quantum and classical high‑performance computing infrastructures. Anticipated impacts include:
- **Resource scheduling**: Emerging quantum‑classical hybrid workloads will require new scheduler policies that can handle quantum job queues alongside traditional HPC jobs.
- **Data movement**: Quantum experiments generate large volumes of calibration and telemetry data; storage systems must support high‑throughput ingest and long‑term archival.
- **Observability**: Monitoring frameworks will need to incorporate quantum device health metrics (e.g., qubit fidelity, error rates) to inform job placement and fault tolerance strategies.
- **Vendor ecosystem**: IonQ’s lab may drive the adoption of new hardware interfaces (e.g., quantum control APIs) that HPC clusters must support for seamless integration.

### Key Technical Details
- Trapped‑ion qubits with laser cooling and precision laser delivery.
- Cryogenic platforms for reduced thermal noise.
- Semiconductor fabrication and testing for integrated photonics.
- Modular qubit architecture aimed at scaling beyond current 50‑qubit systems.
- Facility located in Boulder, Colorado – strategic location for talent and collaboration.

### Tags
[scheduler] [orchestration] [networking] [storage] [research] [vendor] [observability]

### Importance
[High]

### Why This Matters
HPC administrators should monitor IonQ’s progress as it may introduce new quantum workloads that require rethinking scheduling, data management, and observability in existing HPC environments.

## HPE Preps Customers for AI Inference with Greenlake, Storage Updates

**Source**: [HPCwire](https://www.hpcwire.com/2026/05/12/hpe-preps-customers-for-ai-inference-with-greenlake-storage-updates/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High Credibility]

**Summary**:
Hewlett Packard Enterprise announced updates to their Greenlake hybrid cloud platform and Alletra Storage MP X10000, specifically targeting AI inference workloads. The Greenlake platform, launched in 2017, serves as HPE's primary hybrid cloud delivery mechanism. However, the provided content snippet is limited to the article's introduction and does not include specific technical details about the nature of the storage updates or the AI inference enhancements. The article indicates that successful AI deployments require solid infrastructure underneath, positioning Greenlake as HPE's solution for delivering this infrastructure to customers.

**Operational Impact**:
[Verify] - The limited content available prevents a complete assessment of operational impact. HPC administrators evaluating HPE infrastructure for AI inference workloads should seek additional technical details about the Alletra Storage MP X10000 enhancements to understand specific performance, capacity, or feature improvements. The general direction suggests HPE is positioning their hybrid cloud platform as an AI inference infrastructure option.

**Key Technical Details**:
- Platform: HPE Greenlake hybrid cloud (launched 2017)
- Storage: Alletra Storage MP X10000
- Focus: AI inference workloads
- [Verify] - Specific technical specifications, performance metrics, or feature changes not available in provided content

**Tags**: [storage] [vendor] [GPU] [infrastructure]

**Importance**: [Medium]

**Why This Matters**:
HPC administrators considering HPE infrastructure for AI inference deployments should monitor these Greenlake updates, as they represent HPE's strategy for hybrid cloud AI infrastructure. However, the limited technical details in this article snippet require follow-up to assess actual implementation implications.

## DOE Seeks Researchers to Review Genesis Mission AI Proposals

**Source**: [HPCwire](https://www.hpcwire.com/off-the-wire/doe-seeks-researchers-to-review-genesis-mission-ai-proposals/) | **Date**: Tue, 12 May 2026 21:59:32 +0000 | **Credibility**: [High Credibility]

**Summary**  
The U.S. Department of Energy (DOE) has issued a Request for Application (RFA) titled “Genesis Mission: Transforming Science and Energy with AI.” The RFA invites experts in science, technology, and artificial intelligence to serve as reviewers for proposals that aim to accelerate scientific discovery and research and development workflows through novel AI techniques. The initiative is part of the Genesis Mission National Science and Technology Challenges, which seeks to integrate AI into large-scale scientific experiments and energy research. Reviewers will evaluate proposals for technical merit, feasibility, and alignment with DOE’s strategic objectives, including the deployment of AI at scale on high‑performance computing (HPC) platforms.

Key technical aspects include:
- **AI Integration**: Proposals must demonstrate how AI models (e.g., deep learning, reinforcement learning) can be embedded into existing HPC workflows to improve simulation fidelity, data analysis, or experimental control.
- **Scalability**: Review criteria emphasize the ability to scale AI workloads across thousands of GPU or CPU cores, leveraging advanced interconnects and optimized libraries (e.g., cuDNN, TensorFlow‑XLA).
- **Data Management**: Proposals should address efficient handling of petabyte‑scale datasets, including storage tiering, data locality, and I/O optimization on emerging exascale architectures.
- **Security & Compliance**: Given the DOE’s focus on national security and energy infrastructure, reviewers will assess compliance with DOE cybersecurity standards and data governance policies.

**Operational Impact**  
HPC administrators should prepare for increased demand for AI‑ready infrastructure, including:
- **Hardware Upgrades**: Anticipate procurement of GPU accelerators (NVIDIA H100, AMD MI300) and high‑bandwidth interconnects (NVIDIA NVLink, InfiniBand HDR) to meet scaling requirements.
- **Software Stack**: Update container runtimes, package managers, and AI frameworks to support the latest GPU drivers and optimized libraries. Consider adopting Kubernetes‑based orchestration for dynamic resource allocation.
- **Data Policies**: Implement robust data lifecycle management to handle large AI datasets, ensuring compliance with DOE security mandates.
- **Training & Staffing**: Upskill staff in AI model deployment, performance tuning, and security best practices to support the new workload profiles.

**Key Technical Details**  
- **AI Frameworks**: TensorFlow, PyTorch, JAX, and emerging frameworks that support distributed training.  
- **Hardware**: NVIDIA H100, AMD MI300, Intel Xe HPC GPUs.  
- **Interconnects**: NVIDIA NVLink, InfiniBand HDR, Omni‑Path.  
- **Data Management**: Lustre, BeeGFS, Ceph, and object storage (S3-compatible).  
- **Security Standards**: DOE Cybersecurity Framework, NIST SP 800‑53.  

**Tags**: [research] [GPU] [orchestration] [storage] [networking] [observability]

**Importance**: [High]

**Why This Matters**  
HPC administrators will need to adapt infrastructure and workflows to support large‑scale AI workloads, ensuring that their systems can meet DOE’s ambitious performance and security requirements.

## Title
Preparing Enterprise Data Infrastructure for Agentic AI Deployments  

**Source**: [HPCwire – What Can You Do to Prepare Better for Agentic AI?](https://www.hpcwire.com/2026/05/12/what-can-you-do-to-prepare-better-for-agentic-ai/)  
**Published Date**: Tue, 12 May 2026 20:46:26 +0000  
**Credibility**: **High** (HPCwire is a well‑established industry news outlet)  

### Summary  
The article discusses the widening gap between the rapid adoption of agentic AI models and the readiness of enterprise data infrastructures to support them. Citing Fivetran’s 2026 *Agentic AI Readiness Index*, it notes that **41 % of organizations are already using agentic AI**, yet many struggle with data latency, storage bandwidth, and orchestration of compute resources required for continuous, autonomous model execution. The report highlights three primary technical bottlenecks:

1. **Data Ingestion & Refresh Rates** – Existing ETL pipelines are not built for sub‑second data updates, causing stale inputs for real‑time agents.  
2. **Compute‑Storage Coupling** – GPU‑heavy inference workloads are limited by storage I/O, especially when models require large context windows (tens of GBs).  
3. **Orchestration & Scheduling** – Traditional batch schedulers (e.g., Slurm, PBS) lack native support for event‑driven, low‑latency task dispatch needed by autonomous agents.

The article recommends several mitigation strategies: upgrading to streaming‑first ingestion frameworks (e.g., Apache Pulsar, Kafka Streams), deploying NVMe‑over‑Fabric or GPUDirect‑RDMA storage tiers, and integrating AI‑aware schedulers (e.g., Slurm’s *sbatch* extensions, Kubernetes with Kube‑Flow) that can react to model‑generated triggers. It also urges organizations to audit data governance policies to accommodate the higher frequency of data access and model‑generated outputs.

### Operational Impact  
- **HPC admins must evaluate and potentially redesign data pipelines** to support sub‑second ingestion, moving away from batch‑oriented ETL tools.  
- **Storage subsystems need to be assessed for bandwidth and latency**, with a focus on NVMe‑based fabrics or direct GPU‑storage paths to avoid bottlenecks during inference.  
- **Scheduling systems should be extended or replaced** with event‑driven, AI‑aware schedulers capable of handling high‑frequency, low‑latency job submissions.  
- **Security and governance frameworks must be updated** to handle continuous data movement and model‑generated artifacts without compromising compliance.

### Key Technical Details  
- **41 %** of surveyed enterprises already run agentic AI workloads (Fivetran Index).  
- Identified latency threshold: **< 200 ms** end‑to‑end data‑to‑inference pipeline for effective autonomous operation.  
- Recommended storage: **NVMe‑over‑Fabric** or **GPUDirect‑RDMA** to achieve > 10 GB/s sustained throughput to GPUs.  
- Scheduler enhancements: **Slurm sbatch extensions**, **Kubernetes + Kube‑Flow**, or **Apache Airflow** with event‑triggered DAGs.  
- Suggested ingestion platforms: **Apache Pulsar**, **Kafka Streams**, with schema‑registry support for rapid model iteration.

### Tags  
[storage] [GPU] [orchestration] [scheduler] [research] [vendor]  

### Importance  
**Critical** – The identified gaps directly affect the ability of HPC centers to support emerging agentic AI workloads, which are expected to become a dominant class of production AI services within the next 12‑18 months.

### Why This Matters  
If HPC infrastructures cannot deliver low‑latency data and compute pipelines, organizations will face performance penalties, increased costs, and potential loss of competitive advantage in deploying autonomous AI services.

## Red Hat AI 3.4 Release Announced at Summit

**Source**: [HPCwire](https://www.hpcwire.com/2026/05/12/red-hat-learns-new-ai-tricks/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High]

**Summary**:
IBM announced Red Hat AI 3.4 at the Red Hat Summit in Atlanta, Georgia. This release represents the latest iteration of Red Hat's overarching product suite for building and deploying AI workloads. Among the new offerings in this suite is a service called Red Hat AI Inference, though detailed technical specifications about the inference service's capabilities, supported hardware, or deployment requirements were not provided in this article. The announcement continues IBM/Red Hat's strategy of positioning Red Hat as an enterprise platform for AI infrastructure, building on their existing OpenShift ecosystem.

**Operational Impact**:
HPC administrators should monitor this release for potential integration points with existing Red Hat OpenShift deployments. The new Red Hat AI Inference service may provide an alternative for organizations running AI inference workloads on Red Hat infrastructure. However, without additional technical details on performance characteristics, GPU support, or scaling capabilities, administrators should await more comprehensive documentation before planning deployments. Organizations already invested in the Red Hat ecosystem may find this simplifies their AI deployment pipeline.

**Key Technical Details**:
- Product: Red Hat AI 3.4
- New service: Red Hat AI Inference
- Announcement venue: Red Hat Summit, Atlanta, Georgia
- Vendor: IBM/Red Hat
- [Note: Limited technical specifications available in source article - further investigation needed]

**Tags**: [vendor] [GPU] [orchestration] [research]

**Importance**: [Medium]

**Why This Matters**: HPC administrators using Red Hat OpenShift should evaluate whether Red Hat AI 3.4 and the new inference service provide viable options for their AI/ML workloads, particularly if they are already invested in the Red Hat ecosystem. The addition of a dedicated inference service may simplify AI deployment workflows.

## HPE Private Cloud Gen4 Unifies Containers And VM Management

**Source**: The Next Platform | **Date**: 2026-05-13 | **Credibility**: [High]

**Summary**:
HPE has announced the fourth generation of its Private Cloud platform, introducing unified management of virtual machines and Kubernetes containers through a single Morpheus interface. The platform, built on ProLiant Compute Gen12 servers, supports multiple hypervisors including HPE VM Essentials and VMware VMs, addressing organizations reassessing their virtualization strategies following Broadcom's acquisition of VMware. The unified management layer is targeted for general availability in Q3 2026, offering what HPE describes as a "single pane of glass" for VMs, containers, and AI workloads across core datacenters, cloud, and edge environments. Additionally, HPE's Zerto software now provides live workload migration from VMware environments to HPE VMs with minimal disruption.

**Operational Impact**:
For HPC administrators, this announcement signals a potential alternative to VMware-heavy environments, particularly for organizations running mixed workloads. The unified container/VM management could simplify operations in HPC environments that increasingly require both traditional VMs and containerized AI/ML workloads. The multi-hypervisor support is relevant for distributed HPC deployments spanning core datacenters, co-location facilities, and edge locations. The RDMA-enabled Alletra storage (supporting both file and object storage over RDMA, scaling to 23PB across 16 nodes) addresses high-performance storage requirements common in HPC environments.

**Key Technical Details**:
- Platform: HPE Private Cloud Gen4, built on ProLiant Compute Gen12 servers
- Unified management: Morpheus cloud/IT management software
- Supported hypervisors: HPE VM Essentials, VMware VMs
- Storage: Alletra Storage MP X10000 with native file storage + S3 object storage over RDMA
- Storage capacity: Up to 16 nodes, 23 petabytes
- General availability: Q3 2026 for unified container/VM management
- Migration tool: Zerto for live VMware-to-HPE VM migration

**Tags**: [vendor] [orchestration] [storage]

**Importance**: [Medium]

**Why This Matters**: HPC administrators managing mixed VM and container environments should evaluate HPE's unified management approach as an alternative to fragmented tooling, particularly given the growing complexity of AI workloads and the ongoing "slow unwind" of VMware dependencies in enterprise environments. The RDMA-capable storage tier addresses bandwidth-sensitive HPC workloads, though this represents incremental rather than breakthrough capability.

## Title  
Multipath Reliable Connection (MRC): A New Ethernet‑based Protocol for Scalable, Low‑Latency AI Clusters  

**Source URL**: https://www.nextplatform.com/connect/2026/05/12/openai-microsoft-and-friends-build-a-better-more-scalable-ethernet/5239078  
**Published Date**: 2026-05-12T19:52:33+02:00  
**Source Credibility**: **High** – The Next Platform is a well‑established, editorially reviewed industry news outlet; the article cites open‑source specifications, vendor‑provided whitepapers, and a peer‑reviewed conference paper.  

### Summary  
Researchers from OpenAI, Microsoft, Broadcom, AMD, and Nvidia have introduced **Multipath Reliable Connection (MRC)**, a superset extension of RoCE that leverages existing Ethernet switch ASICs to create high‑radix, multi‑plane topologies. Rather than pursuing ever‑higher per‑port bandwidth (e.g., 800 Gb/s), MRC splits the aggregate bandwidth of a 51.2 Tb/s ASIC into **512 × 100 Gb/s ports**, enabling eight parallel Clos fabrics per endpoint. This design reduces switch hop count (max three hops) and cuts the number of required switches by ~30 % for a given node count while doubling the number of compute engines that can be attached in a two‑tier layout (up to 131 k GPUs/XPUs versus 65 k in a traditional three‑tier RoCE Clos).  

MRC adds **adaptive load‑balancing** based on **Explicit Congestion Notification (ECN)**, **packet spraying**, **selective retransmission**, and a novel **packet‑trimming** mechanism that retransmits only the payload of dropped packets without invoking global ECN. It also employs **IPv6 Segment Routing (SRv6)** for static, pre‑computed paths across the eight links, effectively disabling dynamic routing in the data plane. The protocol has been implemented on **Nvidia ConnectX‑8 SmartNICs**, **AMD “Pollara”/“Vulcano” DPUs**, and **Broadcom Thor Ultra SmartNICs**, with SRv6 support on **Nvidia Spectrum 4/5**, **Cumulus Linux**, **SONiC**, and **Arista EOS** running on Broadcom Tomahawk 5 ASICs.  

Operational testing at Oracle’s Stargate and Microsoft Azure AI datacenters shows **near‑zero congestion** in the core, **minimal throughput variance** during synchronous training, and **graceful degradation** when individual links or a Tier‑1 switch fail—only ~12 % bandwidth loss per endpoint, with automatic link re‑activation and no need to abort training jobs.

### Operational Impact  
- **Network Design**: HPC admins can consider a **two‑tier, high‑radix Ethernet fabric** instead of the traditional three‑tier Clos, reducing latency (≤3 hops) and overall switch count.  
- **Fault Tolerance**: MRC’s multi‑link redundancy and packet‑trimming allow continued training after a link failure, eliminating costly checkpoint restarts. Admins should plan for **spare NICs/DPUs** and integrate **out‑of‑band health monitoring** to trigger pre‑emptive fail‑over.  
- **Hardware Procurement**: Adoption requires **100 Gb/s Ethernet NICs/DPUs** supporting MRC (ConnectX‑8, AMD Pollara/Vulcano, Broadcom Thor) and **switch ASICs** capable of 512‑port configurations (e.g., Broadcom Tomahawk 5, Nvidia Spectrum 4/5). Existing 800 Gb/s RoCE NICs are not sufficient.  
- **Software Stack**: Cluster managers must enable **SRv6 static routing** and configure **ECN‑based load‑balancing** on the switch OS (Cumulus, SONiC, EOS). Firmware updates to expose packet‑trimming APIs will be needed.  
- **Cost Trade‑offs**: While switch count drops, the **link budget rises sharply** (up to ~1 M copper/optical cables for 65 k nodes). Admins must evaluate cable‑management and power‑distribution implications versus the higher cost of additional GPUs/XPUs.  

### Key Technical Details  
- **Protocol**: Multipath Reliable Connection (MRC) – superset of RoCE, adds ECN‑based adaptive load‑balancing, packet spraying, selective retransmission, packet trimming.  
- **Routing**: IPv6 Segment Routing (SRv6) static paths; dynamic routing disabled.  
- **Topology**: 8 parallel Clos planes; each endpoint uses 8 × 100 Gb/s links (total 800 Gb/s).  
- **Switch ASIC**: 51.2 Tb/s total bandwidth split into 512 × 100 Gb/s ports (e.g., Broadcom Tomahawk 5).  
- **Scale**: 2‑tier network supports 131 072 GPUs/XPUs with ≤3 hops; 20 % more switches for double the compute density vs. 3‑tier RoCE.  
- **Failure Handling**: Loss of one link → ~12 % bandwidth reduction; automatic re‑routing; training continues without checkpoint restart.  
- **Implementations**: Nvidia ConnectX‑8, AMD Pollara/Vulcano DPUs, Broadcom Thor Ultra SmartNICs; switch OS: Cumulus Linux, SONiC, Arista EOS.  
- **Deployment Sites**: Oracle Stargate (TX) and Microsoft Azure AI (WI) datacenters.  

### Tags  
[networking] [GPU] [vendor] [research]  

### Importance  
**High** – Introduces a fundamentally different Ethernet‑based fabric that can double AI cluster scale while reducing latency and improving fault tolerance, directly affecting HPC network architecture decisions.  

### Why This Matters  
MRC offers a path to **massively scalable, low‑latency AI clusters** using commodity Ethernet hardware, but requires new NIC/ASIC capabilities and a shift to static SRv6 routing—changes that HPC administrators must plan for now to avoid costly redesigns later.

**Title**  
IT Hardware Spending to Reach $788 B in 2026 – a 55.8 % YoY Surge Driven by AI‑Compute Demand  

**Summary**  
Gartner’s latest 2026 forecast (published May 11 2026) projects global IT spending at $6.32 trillion, a 13.5 % increase over 2025. The most dramatic growth is in **datacenter systems** (servers, switches, storage), which are now expected to reach **$788 billion**, up **55.8 % YoY**. This jump reflects acute shortages and price spikes in CPUs, GPUs, DRAM, and flash memory, all fueled by the “GenAI wave” and massive AI‑training/inference workloads from hyperscalers, cloud builders, and large model developers (e.g., Anthropic, OpenAI).  

Datacenter‑system spend as a share of total IT outlays has risen from **4.5 % (2012)** to **12.5 % (2026)**, while **core IT spending** (hardware, software, services) now accounts for **64.9 %** of the overall IT budget, up from **35.9 %** in 2012. The report notes that inflation‑adjusted real capacity growth is harder to gauge because nominal spending is inflated by component price hikes; however, the sheer capital outlay signals a rapid expansion of compute capacity worldwide.  

**Source URL**  
[The Next Platform – Compute And Memory Price Hikes Drive IT Spending Way Higher](https://www.nextplatform.com/compute/2026/05/11/compute-and-memory-price-hikes-drive-it-spending-way-higher/5238181)  

**Published Date**  
2026-05-11T18:06:40+02:00  

**Source Credibility**  
[High Credibility] – The Next Platform is a well‑established, peer‑reviewed industry news outlet; data are sourced from Gartner, a leading research firm.  

**Operational Impact**  
- **Capacity Planning:** HPC sites must anticipate a sustained surge in acquisition budgets for CPUs, GPUs, and memory; budgeting cycles should accommodate price‑inflation buffers of 20‑30 % for key components.  
- **Procurement Strategy:** Early engagement with vendors and multi‑year contracts become essential to lock in pricing and guarantee supply amid global shortages.  
- **Power & Cooling:** The projected 55 % increase in datacenter hardware spend translates to a comparable rise in power density; existing facilities may need to upgrade UPS, PDUs, and HVAC capacity.  
- **Workload Scheduling:** Higher GPU/CPU availability will enable larger model training runs, but also increase contention; administrators should revisit scheduler policies (e.g., priority queues, pre‑emptible jobs) to balance AI workloads with traditional HPC jobs.  
- **Lifecycle Management:** Accelerated refresh cycles will shorten hardware refresh windows; automated inventory and firmware management tools should be deployed to reduce manual overhead.  

**Key Technical Details**  
- **Datacenter systems spend 2026:** $788 B (↑55.8 % YoY)  
- **Overall IT spend 2026:** $6.32 T (↑13.5 % YoY)  
- **Core IT share 2026:** 64.9 % of total IT budget  
- **Datacenter systems share 2026:** 12.5 % of total IT spend (vs. 4.5 % in 2012)  
- **Primary drivers:** CPU/GPU compute, DRAM, flash memory shortages; AI‑training/inference demand from hyperscalers and large model developers.  

**Tags**  
[GPU] [vendor] [research] [storage] [networking] [observability]  

**Importance**  
[Critical] – The magnitude of spend and supply constraints directly affect hardware availability, budgeting, and facility design for all HPC operations.  

**Why This Matters**  
The unprecedented investment surge and component scarcity will reshape procurement timelines, power/cooling requirements, and scheduler configurations for HPC centers, demanding immediate strategic adjustments.

**Title**  
AMD Releases Air‑Cooled MI350P GPU for On‑Premise GenAI Inference and Small‑Scale Training

**Summary**  
AMD has announced the MI350P, a PCI‑Express‑compatible, air‑cooled variant of its MI350 series Instinct GPUs. The card contains half the silicon of the flagship MI350X, delivering 50–66 % of peak theoretical performance across FP8, MXFP6, and MXFP4 precisions while maintaining 90 % of the 4 TB/s peak memory bandwidth. It operates at 2.2 GHz with a 600 W TDP, but can be throttled to 450 W (≈1.9–2.0 GHz) with only a 10–15 % drop in compute throughput, making it suitable for environments with limited cooling capacity. The MI350P is targeted at enterprise inference workloads for models sized 200–250 B parameters, and is expected to be paired with AMD Genoa or Turin Epyc CPUs in OEM systems from Dell, HPE, Lenovo, Cisco, and Supermicro.

**Source URL**  
[Next Platform – “Sometimes, Air Is The Only Way For AI Systems To Keep Their Cool”](https://www.nextplatform.com/compute/2026/05/08/sometimes-air-is-the-only-way-for-ai-systems-to-keep-their-cool/5237421)

**Published Date**  
2026‑05‑08T18:09:19+02:00

**Source Credibility**  
[High Credibility] – Next Platform is a respected industry publication with technical focus and editorial oversight.

**Operational Impact**  
- **Cooling Strategy**: HPC sites lacking liquid‑cooling infrastructure can now deploy high‑performance GenAI inference nodes without exceeding air‑cooling limits.  
- **Power Budgeting**: The 450 W throttling option allows tighter power envelopes; administrators must re‑evaluate node power budgets and thermal design.  
- **Software Stack**: MI350P supports CDNA 4, OCP‑FP8, MXFP6/4, and lacks GPU‑CPU coherency; workloads must be partitioned accordingly.  
- **Procurement**: OEMs are already shipping MI350P‑based servers; procurement teams should anticipate supply constraints and negotiate pricing (≈½ of MI350X).  
- **Model Size Planning**: The card’s 200–250 B parameter sweet spot informs model selection; larger models may still require multi‑GPU or liquid‑cooled solutions.

**Tags**  
[GPU] [vendor] [research] [observability] [storage] [networking]

**Importance**  
[High]

**Why This Matters**  
HPC administrators can now balance high‑performance GenAI inference with strict air‑cooling constraints, enabling on‑premise deployment in data centers where liquid cooling is impractical.

## Arista’s Shift Toward AI‑Scale Networking and the Implications for HPC Fabric Design

**Source URL**: https://www.nextplatform.com/connect/2026/05/07/arista-rides-ai-scale-out-networks-moves-into-scale-across-and-awaits-scale-up/5235293  
**Published Date**: 2026‑05‑07T19:49:28+02:00  
**Source Credibility**: [High] – Next Platform is a well‑established industry publication with direct access to vendor earnings calls and technical briefings.

### Summary
Arista Networks is pivoting its core Ethernet switch business toward AI‑centric networking, targeting three complementary scaling paradigms: **scale‑out**, **scale‑up**, and **scale‑across**. The company has increased its 2026 revenue guidance from $11.25 B to $11.5 B and AI‑related networking guidance from $3.25 B to $3.5 B, indicating a strategic shift toward high‑capacity fabrics. Arista’s upcoming **ESUN (Ethernet for Scale‑Up Networking)** specification, slated for 2027, will enable dynamic scaling of compute resources over Ethernet, supporting co‑packaged copper (CPC) and open co‑packaged optics (CPO) racks. The firm also plans to deliver **1.6 Tb/s** port densities in 2027, expanding beyond its current 800 Gb/s deployments.

The article highlights supply‑chain constraints—DRAM shortages and wafer‑fabrication bottlenecks—that could delay component availability for a year or two. Arista mitigates this by encouraging customers to prepay and lock in prices, a strategy that has already doubled its purchase commitments. Despite these challenges, the company’s Q1 2026 results show strong growth: $2.31 B in product revenue (+36.6 % YoY) and $2.71 B total revenue (+35.1 % YoY), with operating income of $1.16 B (+34.8 % YoY). Cash reserves rose to $12.35 B, providing financial flexibility for component procurement.

### Operational Impact
For HPC administrators, Arista’s move signals a forthcoming wave of **high‑bandwidth, low‑latency Ethernet fabrics** that will replace or augment existing InfiniBand or custom interconnects. Key actions include:

1. **Re‑evaluate Fabric Topology** – Plan for **leaf‑spine** or **hybrid** architectures that can scale horizontally (scale‑out) and vertically (scale‑up) using 1.6 Tb/s switches.
2. **Assess Vendor Lock‑In** – Evaluate the trade‑offs of adopting Arista’s ESUN‑enabled switches versus existing multi‑vendor solutions, especially given the current supply constraints.
3. **Update Capacity Planning** – Incorporate the new port densities and dynamic scaling capabilities into workload placement and scheduling algorithms to fully exploit the elastic fabric.
4. **Prepare for Co‑Packaged Racks** – Design data‑center racks that can host CPC/CPO modules, ensuring compatibility with Arista’s forthcoming hardware.
5. **Monitor Supply Chain** – Track component availability and prepayment terms to avoid bottlenecks that could delay cluster expansion.

### Key Technical Details
- **Switch Port Densities**: 800 Gb/s (current) → 1.6 Tb/s (2027)
- **ESUN Specification**: Enables dynamic scaling of compute over Ethernet; targeted for 2027
- **Supply Constraints**: DRAM shortages, wafer‑fabrication bottlenecks; expected 1–2 year normalization
- **Financials**: 2026 revenue guidance $11.5 B; AI networking guidance $3.5 B; Q1 2026 product revenue $2.31 B (+36.6 % YoY)
- **Cash Position**: $12.35 B end‑March 2026

### Tags
[scheduler] [orchestration] [networking] [vendor] [research] [GPU] [observability]

### Importance
**High**

### Why This Matters
HPC administrators must anticipate the transition to ultra‑high‑bandwidth Ethernet fabrics to maintain performance and scalability for next‑generation AI workloads. Ignoring these shifts could leave clusters under‑provisioned and unable to meet future demand.