## Title
IonQ Opens New Quantum Computing R&D Lab in Boulder, Colorado  

**Source URL**: https://www.hpcwire.com/off-the-wire/ionq-opens-new-quantum-computing-rd-lab-in-colorado/  
**Published Date**: Wed, 13 May 2026 13:00:10 +0000  
**Source Credibility**: **High** – HPCwire is a well‑established, editorially‑reviewed news outlet for high‑performance computing.  

### Summary
IonQ announced the launch of a dedicated laboratory complex in Boulder, Colorado, designed to support advanced quantum‑computing research and semiconductor chip testing. The facility will house state‑of‑the‑art trapped‑ion quantum processors, custom control electronics, and a suite of metrology tools for silicon‑based quantum chip fabrication. According to the release, the lab will enable tighter integration between IonQ’s hardware development and software stack, accelerating the rollout of next‑generation quantum systems that target error‑corrected logical qubits.

The new R&D site is expected to serve both internal engineering teams and external academic collaborators, providing access to high‑fidelity quantum hardware for algorithm development and benchmarking. IonQ also indicated plans to co‑locate a high‑speed networking testbed (10 GbE and emerging 400 GbE links) to evaluate quantum‑classical hybrid workloads that will run on conventional HPC clusters alongside quantum accelerators.

### Operational Impact
- **Hybrid Workload Integration**: HPC administrators should anticipate the need to provision low‑latency, high‑bandwidth interconnects between classical compute nodes and quantum accelerators for co‑execution of quantum‑classical algorithms. Existing InfiniBand fabrics may require tuning or augmentation with dedicated quantum‑ready ports.
- **Scheduling & Resource Management**: The emergence of quantum resources will likely drive extensions to job schedulers (e.g., Slurm) to handle quantum device reservations, queue policies, and co‑allocation with GPU/CPU resources. Admins may need to evaluate upcoming scheduler plugins or APIs that support quantum job descriptors.
- **Security & Access Controls**: Quantum hardware access will involve sensitive intellectual property; administrators must implement fine‑grained authentication (e.g., LDAP + MFA) and possibly hardware‑level isolation (PCIe pass‑through, SR‑IOV) to protect both quantum and classical assets.
- **Observability**: Monitoring quantum device health (coherence times, error rates) will require new telemetry pipelines. Existing HPC monitoring stacks (Prometheus, Grafana) will need custom exporters to ingest quantum metrics for capacity planning.

### Key Technical Details
- Facility location: Boulder, Colorado (new laboratory suite)
- Focus areas: Trapped‑ion quantum processors, semiconductor quantum chip testing, high‑speed networking (10 GbE & 400 GbE testbed)
- Intended use: Development of error‑corrected logical qubits, hybrid quantum‑classical workload benchmarking
- Collaboration model: Open to academic partners; on‑site access to quantum hardware
- Timeline: Facility announced May 2026; operational rollout expected later in 2026 (exact dates not disclosed)

### Tags
[research] [vendor] [GPU] [orchestration] [scheduler] [networking] [observability]  

### Importance
**High** – Introduces a new class of quantum resources that will intersect with existing HPC environments, prompting changes to scheduling, networking, and monitoring practices.

### Why This Matters
The lab signals accelerated deployment of quantum accelerators that will need to be integrated into conventional HPC clusters, requiring administrators to adapt scheduling, networking, and observability tooling to support hybrid quantum‑classical workloads.

## HPE Preps Customers for AI Inference with Greenlake, Storage Updates

**Source**: [HPCwire](https://www.hpcwire.com/2026/05/12/hpe-preps-customers-for-ai-inference-with-greenlake-storage-updates/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High Credibility]

**Summary**:
Hewlett Packard Enterprise announced updates to its Greenlake hybrid cloud platform aimed at preparing customers for AI inference workloads. The updates include enhancements to the Alletra Storage MP X10000 system. Greenlake, launched in 2017, serves as HPE's hybrid cloud delivery model, offering infrastructure-as-a-service capabilities. The article emphasizes that successful AI deployments require solid underlying infrastructure, positioning Greenlake as the foundation for HPE's AI strategy. However, the article provides limited technical specifics regarding the exact nature of the storage enhancements or performance metrics.

**Operational Impact**:
HPC administrators evaluating HPE infrastructure for AI inference workloads should consider Greenlake as a potential platform for hybrid cloud AI deployment. The Alletra Storage MP X10000 enhancements appear targeted at addressing the storage demands of inference workloads, which typically require low-latency access to model weights and data. Administrators should request detailed technical specifications from HPE regarding IOPS, throughput, and latency improvements to properly evaluate these updates against their inference requirements. The hybrid cloud model may appeal to organizations balancing on-premises security requirements with cloud-like operational flexibility.

**Key Technical Details**:
- Platform: HPE Greenlake (hybrid cloud, launched 2017)
- Storage: Alletra Storage MP X10000
- Focus: AI inference infrastructure
- Vendor: Hewlett Packard Enterprise
- Announcement date: May 12, 2026

**Tags**: [vendor] [storage] [GPU] [orchestration]

**Importance**: [Medium]

**Why This Matters**: HPC administrators should monitor HPE's Greenlake platform developments as they represent an increasingly common path for deploying AI inference at scale, particularly in enterprise environments requiring hybrid cloud deployment models. The Alletra Storage MP X10000 enhancements may offer improved storage characteristics for inference workloads, but further technical details are needed to assess operational impact.

## DOE Seeks Researchers to Review Genesis Mission AI Proposals

**Source**: [HPCwire](https://www.hpcwire.com/off-the-wire/doe-seeks-researchers-to-review-genesis-mission-ai-proposals/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High]

**Summary**:
The Department of Energy is soliciting expert reviewers for the "Genesis Mission: Transforming Science and Energy with AI" Request for Application (RFA). This initiative seeks researchers with expertise in science, technology, and artificial intelligence to evaluate proposals addressing the Genesis Mission National Science and Technology Challenges. The program aims to accelerate scientific discovery and research and development workflows through novel AI approaches. This represents a significant federal investment in AI-driven scientific computing, building on DOE's existing leadership in high-performance computing through facilities like Oak Ridge, Lawrence Livermore, and Argonne national laboratories.

**Operational Impact**:
This announcement has **limited direct operational impact** for HPC administrators in the near term. The request is for proposal reviewers, not system operators or developers. However, the Genesis Mission RFA outcomes will shape future AI workloads that HPC facilities will need to support. Administrators should monitor which proposals receive funding, as these will likely define emerging AI + science workload patterns that may influence procurement decisions, GPU cluster requirements, and software stack investments over the next 3-5 years.

**Key Technical Details**:
- Program: Genesis Mission: Transforming Science and Energy with AI
- Focus: National Science and Technology Challenges in scientific discovery and R&D workflows
- Reviewer requirements: Expertise in science, technology, and AI
- Agency: U.S. Department of Energy (DOE)
- Publication: HPCwire Off the Wire

**Tags**: [research] [GPU] [AI]

**Importance**: [Medium]

**Why This Matters**:
HPC administrators should track the Genesis Mission because funded proposals will likely drive future AI-focused workload requirements at DOE facilities, potentially influencing broader industry trends in AI-enabled scientific computing infrastructure.

## What Can You Do to Prepare Better for Agentic AI?

**Source**: [HPCwire](https://www.hpcwire.com/2026/05/12/what-can-you-do-to-prepare-better-for-agentic-ai/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High Credibility]

**Summary**:
HPCwire reports on the growing gap between enterprise data infrastructure readiness and the rapid deployment of agentic AI systems. Citing Fivetran's 2026 Agentic AI Readiness Index, the article highlights that while 41% of organizations have already deployed agentic AI in some capacity, enterprise data infrastructure is struggling to keep pace with these new workloads. The piece suggests that infrastructure readiness has become a critical bottleneck in the agentic AI race, potentially limiting the effectiveness of AI agents that require real-time data access, low-latency pipelines, and robust orchestration capabilities.

**Operational Impact**:
For HPC administrators, this finding signals a need to evaluate whether existing data pipelines, storage systems, and orchestration frameworks can support agentic AI workloads. Agentic AI systems differ from traditional batch AI workloads in that they require continuous data flow, real-time inference capabilities, and dynamic resource allocation. Administrators should assess: (1) data pipeline latency between sources and compute, (2) storage throughput for concurrent read/write operations, and (3) scheduler flexibility for handling autonomous agent tasks that may spawn additional sub-tasks. The 41% adoption rate suggests this is no longer a future concern but an operational reality.

**Key Technical Details**:
- **Adoption metric**: 41% of organizations already using agentic AI (Fivetran 2026 Readiness Index)
- **Primary concern**: Enterprise data infrastructure unable to keep pace with agentic AI deployment
- **Infrastructure requirements**: Real-time data pipelines, low-latency access, dynamic orchestration

**Tags**: [orchestration] [infrastructure] [AI/ML] [data management]

**Importance**: [Medium]

**Why This Matters**: HPC administrators need to proactively evaluate infrastructure readiness for agentic AI workloads, as the high adoption rate (41%) indicates these workloads are already entering production environments, requiring different data pipeline and orchestration characteristics than traditional HPC or batch AI jobs.

## Red Hat AI 3.4 Announced with New Inference Service

**Source**: [HPCwire](https://www.hpcwire.com/2026/05/12/red-hat-learns-new-ai-tricks/) | **Date**: Tue, 12 May 2026 | **Credibility**: [High]

**Summary**:
IBM announced Red Hat AI 3.4 at the Red Hat Summit in Atlanta, Georgia this week. This release represents the latest iteration of Red Hat's overarching product suite for building and deploying AI workloads. The announcement includes a new service called Red Hat AI Inference, though specific technical details about the service's architecture, capabilities, or GPU orchestration features are not available in the preview content. The article indicates more detailed coverage exists behind the linked source. This announcement continues IBM/Red Hat's integration of enterprise AI capabilities into their open hybrid cloud platform, building on their previous AI/ML offerings.

**Operational Impact**:
[Content truncated - unable to fully assess operational impact from available preview. Further investigation needed to determine specific features, GPU support, cluster management capabilities, or integration requirements for Red Hat AI Inference service.]

**Key Technical Details**:
- Product: Red Hat AI 3.4
- New service: Red Hat AI Inference
- Event: Red Hat Summit 2026, Atlanta, Georgia
- Vendor: IBM/Red Hat
- [Verify] - Full technical specifications not available in preview content

**Tags**: [vendor] [GPU] [orchestration] [research]

**Importance**: [Medium]

**Why This Matters**:
HPC administrators should monitor this announcement as Red Hat AI Inference represents another option for AI workload management in enterprise HPC environments. The integration with Red Hat's existing infrastructure (RHEL, OpenShift, RHODS) could provide streamlined paths for AI inference deployment, but technical details are needed to assess operational impact.

## Title  
HPE Private Cloud 4th Gen Unifies VM, Kubernetes, and AI Management – Implications for HPC Environments  

**Source URL**: https://www.nextplatform.com/cloud/2026/05/13/hpe-throws-vm-users-a-lifeline-unifying-containers-and-vm-management-in-cloud-stack/5239635  
**Published Date**: 2026-05-13T14:36:43+02:00  
**Source Credibility**: **High** – The Next Platform is a well‑established, editorially‑reviewed outlet covering enterprise compute and HPC.  

### Summary  
HPE announced the fourth generation of its Private Cloud platform, built on Gen12 ProLiant servers, that delivers a single‑pane‑of‑glass management layer for virtual machines (VMs), Kubernetes containers, and AI workloads. The platform integrates HPE VM Essential (a hypervisor‑agnostic VM stack) with the Morpheus cloud‑IT management suite, allowing administrators to operate VMs—including VMware‑based instances—and containers from one console. General availability is slated for Q3 2026.  

Key technical additions include: (1) support for multiple hypervisors (HPE VM Essential, VMware vSphere, and future options) to match diverse edge and data‑center footprints; (2) live‑migration tooling via Zerto that moves workloads from VMware environments to HPE VMs with minimal disruption; (3) an upgraded storage offering—Alletra Storage MP X10000—providing native file storage with RDMA, alongside existing S3‑over‑RDMA object storage, scaling to 16 nodes and 23 PB. The platform also bundles SimpliVity hyper‑converged infrastructure with Morpheus VM Essentials, extending the unified model to HCI deployments.  

The announcement comes amid a “slow unwind” from VMware after Broadcom’s acquisition, with 86 % of surveyed enterprises reducing VMware footprints and 72 % migrating workloads to public clouds. HPE positions its unified stack as a cost‑effective, less‑fragmented alternative for organizations seeking to retain on‑premise or hybrid workloads, including AI inference at the edge.

### Operational Impact  
- **Unified Management**: HPC admins can now provision, monitor, and schedule both VM‑based and container‑based jobs from a single Morpheus interface, reducing the operational overhead of maintaining separate orchestration stacks (e.g., Slurm for VMs, Kubernetes for containers).  
- **Hypervisor Flexibility**: The ability to run multiple hypervisors under one management plane enables gradual migration from legacy VMware clusters without immediate re‑platforming, preserving existing workloads while testing HPE VM Essential or other hypervisors.  
- **Live Migration**: Zerto‑enabled migration provides a low‑downtime path to move HPC workloads off VMware into HPE’s stack, useful for disaster‑recovery drills or consolidating compute resources.  
- **Edge & AI Support**: RDMA‑enabled file storage and native object storage improve data‑movement performance for AI training/inference workloads that are increasingly distributed to edge sites.  
- **Licensing Cost Reduction**: HPE claims a 10‑fold reduction in VM license costs versus traditional VMware licensing, potentially freeing budget for additional compute or storage capacity.  

**Action Items for HPC Administrators**  
1. Evaluate Morpheus integration with existing HPC schedulers (e.g., Slurm, PBS) to determine API compatibility for job submission and accounting.  
2. Pilot HPE VM Essential on a test node to benchmark VM launch latency and I/O performance against current VMware/vSphere setups.  
3. Assess Zerto live‑migration for a subset of non‑production workloads to validate migration time and data integrity.  
4. Review Alletra MP X10000 RDMA file‑system performance for AI data pipelines; compare against current parallel file systems (e.g., Lustre, GPFS).  

### Tags  
[scheduler] [orchestration] [vendor] [GPU] [storage] [edge] [AI] [virtualization]  

### Importance  
**High** – The convergence of VM and container management directly affects HPC workload orchestration, licensing economics, and edge AI deployment strategies.  

### Why This Matters  
HPE’s unified stack could simplify HPC environment management, lower licensing costs, and provide the performance‑critical storage needed for AI‑driven HPC workloads, while offering a practical migration path away from costly VMware dependencies.

## Title  
Multipath Reliable Connection (MRC): A New Ethernet‑Based Protocol for Scalable, Low‑Latency AI Clusters  

**Source URL**: https://www.nextplatform.com/connect/2026/05/12/openai-microsoft-and-friends-build-a-better-more-scalable-ethernet/5239078  
**Published Date**: 2026-05-12T19:52:33+02:00  
**Source Credibility**: **High** – The Next Platform is a well‑established, editorially reviewed technology news outlet with a strong track record on HPC and data‑center reporting.  

### Summary  
Researchers from OpenAI, Microsoft, Broadcom, AMD, and Nvidia have introduced **Multipath Reliable Connection (MRC)**, a network protocol that sits atop existing Ethernet switch ASICs and extends the RDMA over Converged Ethernet (RoCE) stack. MRC adopts concepts from the Ultra Ethernet specification (Ultra Ethernet Consortium, July 2023) to deliver InfiniBand‑class latency while retaining Ethernet compatibility. The protocol uses **explicit congestion notification (ECN)**‑based adaptive load balancing, **packet spraying** across up to eight parallel links per endpoint, **selective retransmission**, and a novel **packet‑trimming** mechanism that retransmits only the payload of dropped packets without invoking global ECN.  

MRC is paired with **IPv6 Segment Routing (SRv6)** to provide static, pre‑computed paths across the multiple links, effectively disabling dynamic routing in the data plane. By re‑architecting switch ASICs to expose a higher radix (e.g., 512 × 100 Gb/s ports instead of 64 × 800 Gb/s), a two‑tier topology can replace the traditional three‑tier Clos network, halving the number of switch hops (max 3 vs. 5‑7) and doubling the number of compute endpoints (e.g., 131 k GPUs/XPUs vs. 65 k) for the same aggregate bandwidth. The design trades a modest 20 % increase in switch count for a 2‑3× reduction in optical link budget and a dramatic improvement in fault tolerance: loss of a single link reduces bandwidth by only ~12 % and the system continues training without a global checkpoint restart.  

The protocol has already been deployed on Nvidia ConnectX‑8 SmartNICs, AMD “Pollara”/“Vulcano” DPUs, Broadcom Thor Ultra SmartNICs, and on Nvidia Spectrum 4/5 as well as Arista EOS switches running Cumulus Linux or SONiC. Testbeds at Oracle’s Stargate and Microsoft Azure AI datacenters report **near‑zero congestion** in the core and **stable throughput** across shared workloads.  

### Operational Impact  
- **Network Architecture Redesign**: HPC sites can replace three‑tier RoCE/InfiniBand fabrics with a flatter two‑tier MRC fabric, reducing latency (fewer hops) and simplifying cabling.  
- **Switch Procurement**: Procurement teams should evaluate high‑radix Ethernet ASICs (e.g., 512‑port 100 Gb/s) and verify firmware support for MRC extensions (packet trimming, SRv6 static routing).  
- **NIC/Firmware Updates**: Existing RoCE NICs must be upgraded or flashed to firmware that implements MRC (ConnectX‑8, AMD DPUs, Broadcom Thor). Verify driver compatibility with the OS stack (Linux kernel ≥ 6.8, Mellanox OFED 5.10+).  
- **Fault‑Tolerance Procedures**: Administrators can relax checkpoint frequency for link‑failure scenarios, but must still maintain per‑node checkpointing for GPU/XPU crashes. Implement out‑of‑band health monitoring to predict compute‑engine failures and trigger graceful fail‑over to spare nodes.  
- **Capacity Planning**: While switch count rises ~20 %, link count grows >5×; budgeting for DAC and optical transceivers is essential. Conduct a cost‑benefit analysis comparing link‑budget vs. GPU cost (GPU ≈ $10k–$15k each).  
- **Observability**: Enable telemetry for packet‑trimming events and ECN counters on switches/NICs to detect congestion hotspots. Existing telemetry stacks (Prometheus + node_exporter, NVIDIA DCGM) will need new MRC‑specific metrics.  

### Key Technical Details  
- **Protocol**: Multipath Reliable Connection (MRC), superset of RoCE v2.  
- **Core Features**: ECN‑based adaptive load balancing, packet spraying across 8 links, selective retransmission, packet trimming, SRv6 static routing.  
- **Switch ASIC Re‑use**: 51.2 Tb/s ASIC split into 512 × 100 Gb/s ports (high radix).  
- **Topology**: Two‑tier Clos with 8 parallel data planes; example scaling to 131 072 GPUs/XPUs with ≤3 hops.  
- **Hardware Implementations**: Nvidia ConnectX‑8 SmartNICs, AMD “Pollara”/“Vulcano” DPUs, Broadcom Thor Ultra SmartNICs; Nvidia Spectrum 4/5, Arista EOS (Broadcom Tomahawk 5) running Cumulus Linux or SONiC.  
- **Performance Claims**: “Essentially no congestion” in core; throughput variance eliminated for synchronous training; fault‑tolerant link loss reduces impact to ~12 % bandwidth per endpoint.  
- **Deployment Sites**: Oracle Stargate (Abilene, TX) and Microsoft Azure AI (Fairwater, WI).  

### Tags  
[scheduler] [orchestration] [networking] [GPU] [vendor] [research]  

### Importance  
**High** – The protocol directly affects network design, cost, and reliability for large‑scale AI/HPC clusters, and its adoption would require substantial changes to existing fabric deployments.  

### Why This Matters  
MRC promises InfiniBand‑level latency and fault tolerance using commodity Ethernet hardware, enabling HPC administrators to build larger, cheaper, and more resilient AI clusters without the traditional three‑tier Clos complexity.

## Title
IT Spending Surge in 2026 Driven by CPU/GPU and Memory Shortages – Implications for HPC Infrastructure  

**Source URL**: https://www.nextplatform.com/compute/2026/05/11/compute-and-memory-price-hikes-drive-it-spending-way-higher/5238181  
**Published Date**: 2026-05-11T18:06:40+02:00  
**Source Credibility**: **High** (The Next Platform is a well‑established, editorially‑driven technology news outlet; data cited from Gartner, a reputable market‑research firm)  

### Summary  
Gartner’s latest forecast shows global IT spending reaching **$6.32 trillion in 2026**, a 13.5 % year‑over‑year increase, driven primarily by soaring demand and price inflation for CPUs, GPUs, DRAM, and flash memory. The most striking shift is in **datacenter systems spending**, which Gartner now expects to climb **55.8 % to $788 billion** in 2026—up from a previously projected 31.7 % growth. This jump represents an additional **$134.6 billion** over the prior three‑month forecast, roughly equivalent to the total datacenter spend of 2012‑2013 combined (nominal terms).  

The analysis highlights that **datacenter hardware now accounts for 12.5 % of total IT spend**, up from 4.5 % in 2012, while “core IT” (hardware, software, services) will represent **64.9 % of the overall IT budget** by 2026, up from 35.9 % in 2012. The surge is attributed to massive AI‑training and inference workloads being deployed by hyperscalers, cloud builders, and AI model developers (e.g., Anthropic, OpenAI). Inflation‑adjusted figures suggest real capacity growth is outpacing price increases, but the nominal cost pressure remains a critical factor for procurement.  

### Operational Impact  
- **Budget Planning**: HPC centers must anticipate substantially higher capital expenditures for compute nodes, GPU accelerators, and high‑bandwidth memory to stay competitive in the AI/ML space.  
- **Capacity Forecasting**: The rapid growth in datacenter spend signals accelerated deployment of large‑scale GPU clusters; administrators should reassess scaling models and plan for higher power, cooling, and floor‑space requirements.  
- **Procurement Strategy**: With component shortages and price spikes, long‑lead‑time contracts, multi‑vendor sourcing, and inventory buffering become essential to avoid project delays.  
- **Lifecycle Management**: Faster refresh cycles may be required as newer GPU/CPU architectures become cost‑effective only after price normalization; administrators should design modular systems to simplify upgrades.  
- **Energy & Sustainability**: The projected increase in datacenter power draw will pressure existing facilities; evaluating energy‑efficient scheduling (e.g., power‑aware Slurm plugins) and renewable‑energy procurement will be increasingly important.  

### Key Technical Details  
- **Datacenter systems spend 2026**: $788 B (55.8 % YoY growth)  
- **Overall IT spend 2026**: $6.32 T (13.5 % YoY growth)  
- **Core IT share 2026**: 64.9 % of total IT budget  
- **Datacenter hardware share 2026**: 12.5 % of total IT spend (vs. 4.5 % in 2012)  
- **Primary drivers**: AI training/inference demand, hyperscaler expansion, GPU/CPU/DRAM/Flash shortages  
- **Inflation‑adjusted capacity**: Real capacity growth outpaces nominal spend, but price pressure remains high  

### Tags  
[scheduler] [orchestration] [GPU] [vendor] [research] [storage] [networking]  

### Importance  
**Critical** – The magnitude of spend and component scarcity directly affect HPC acquisition cycles, system design, and operational budgets.  

### Why This Matters  
HPC administrators must adapt procurement, capacity planning, and energy management strategies now to cope with unprecedented cost and supply pressures on the compute and memory subsystems that underpin AI‑intensive workloads.

## AMD Introduces MI350P Air-Cooled GPU for Enterprise AI Workloads

**Source**: The Next Platform | **Date**: 2026-05-08 | **Credibility**: [High]

**Summary**:
AMD has launched the MI350P, a half-capacity variant of the MI350X GPU designed specifically for air-cooled server environments. The MI350P uses a PCIe form factor that fits into standard server chassis, targeting enterprises that cannot deploy liquid cooling infrastructure or require on-premise AI capabilities in thermally-constrained datacenters. The GPU features 12 HBM3E memory stacks (half the MI350X configuration), operates at 2.2 GHz with a 600W TDP (throttleable to 450W), and implements the CDNA 4 architecture with support for OCP-FP8, MXFP6, and MXFP4 precision formats. AMD has been notably transparent about delivered performance metrics, showing the MI350P achieves approximately 90% of peak memory bandwidth (4 TB/sec) and 58-66% of peak compute on 16-bit and 8-bit math operations in their benchmarks. The device is positioned for models with 200-250 billion parameters, suitable for enterprise inference and smaller training workloads.

**Operational Impact**:
For HPC administrators, the MI350P addresses a critical gap for organizations with air-cooled infrastructure who need GPU acceleration for AI inference and smaller model training. The 450W throttling option provides flexibility for datacenters with limited thermal headroom, potentially reducing performance by only 10-15% while cutting power consumption by 25%. Administrators should note that unlike the MI350X OAM form factor, the MI350P cannot support memory coherency across GPUs or between GPUs and CPUs—each GPU operates standalone. This limitation affects how AI frameworks and orchestration tools should be configured. The lack of multi-GPU coherency means this GPU is best suited for inference workloads or single-node training rather than distributed training scenarios. Availability is expected to be constrained given ongoing GPU supply challenges.

**Key Technical Details**:
- Architecture: CDNA 4 (debuted June 2025)
- Memory: 12 HBM3E stacks (half of MI350X)
- Clock: 2.2 GHz (throttleable to ~1.9-2.0 GHz at 450W)
- TDP: 600W standard, 450W reduced mode
- Memory bandwidth: 4 TB/sec peak (90% delivered in tests)
- Compute delivery: 58-66% of peak on FP16/FP8, 50% on MXFP4
- Target workload: 200-250 billion parameter models
- Coherency: Standalone only (no multi-GPU or GPU-CPU coherency)
- OEMs: Dell (XE7745, R7725), HPE (ProLiant DL385 Gen11, DL345 Gen12), Lenovo (ThinkSystem SR675/I v3), Cisco (C845a M8, X Series 580p, UC245 M8), Supermicro (multiple AS models)

**Tags**: [GPU] [vendor] [orchestration] [infrastructure]

**Importance**: Medium

**Why This Matters**: HPC administrators managing air-cooled infrastructure now have an official AMD GPU option for enterprise AI inference, but must account for the lack of multi-GPU coherency when designing workloads and orchestration strategies—this GPU is optimized for standalone inference or single-node workloads, not distributed training at scale.

## Title
Arista’s AI‑Focused Ethernet Fabrics: Scale‑Out, Scale‑Across, and Upcoming Scale‑Up (ESUN) Roadmap  

**Source URL**: https://www.nextplatform.com/connect/2026/05/07/arista-rides-ai-scale-out-networks-moves-into-scale-across-and-awaits-scale-up/5235293  
**Published Date**: 2026-05-07T19:49:28+02:00  
**Source Credibility**: **High** – The Next Platform is a well‑established, editorially‑reviewed source for data‑center and HPC technology news.  

### Summary
Arista Networks is positioning its Ethernet switching portfolio to become the primary networking substrate for large‑scale generative‑AI (GenAI) deployments. The company reports a strong Q1 2026 financial performance (product revenue $2.31 B, +36.6 % YoY) and has raised its 2026 AI‑related networking revenue guidance to $3.5 B. The growth is driven by “scale‑out” Ethernet fabrics (leaf‑spine) that already support 800 Gb/s per port and are being expanded toward 1.6 Tb/s per port in 2027.  

A new “scale‑up” protocol, **ESUN (Ethernet for Scale‑Up Networking)**, is slated for introduction in 2027. ESUN will enable dynamic, high‑bandwidth interconnects within AI racks, supporting co‑packaged copper (CPC) and open co‑packaged optics (CPO) to accelerate collective operations and memory‑side networking. Arista also emphasizes “scale‑across” Ethernet fabrics that interconnect multiple datacenters, targeting 1/3 – 2/3 of future AI networking revenue. Supply‑chain constraints (DRAM, ASIC wafer fab) are expected to persist for 12‑24 months, prompting customers to pre‑pay for components.  

### Operational Impact
- **Network Fabric Planning**: HPC admins should evaluate whether existing 800 Gb/s leaf‑spine fabrics meet upcoming AI workloads or if a migration path to 1.6 Tb/s ports (expected 2027) is required.  
- **Rack‑Level Interconnect**: The ESUN protocol will affect intra‑rack topology; administrators may need to redesign rack designs to incorporate CPC/CPO modules and ensure firmware support for collective and memory‑acceleration features.  
- **Supply‑Chain Awareness**: Anticipate lead‑time extensions for Arista ASICs and related optics; incorporate component pre‑order or alternative vendor strategies into procurement cycles.  
- **Performance Tuning**: ESUN’s “scale‑up” capabilities promise wire‑rate L2/L3 load balancing and collective acceleration. Administrators must plan for driver/OS stack updates (e.g., Mellanox/ROCE, OpenFabrics) to expose these features to MPI/PMI layers.  
- **Monitoring & Observability**: New telemetry (port‑level 1.6 Tb/s utilization, ESUN state) will be required; integrate Arista CloudVision or equivalent APIs into existing monitoring frameworks (Prometheus, Grafana).  

### Key Technical Details
- Current production Ethernet fabric: 800 Gb/s per port, >100 customers, 1.6 Tb/s target for 2027.  
- ESUN (Ethernet for Scale‑Up Networking) launch: 2027‑2028, focusing on AI rack interconnects, CPC/CPO optics.  
- Scale‑across Ethernet fabrics: projected to drive 33‑66 % of AI networking revenue; no specific port speed disclosed.  
- Supply‑chain constraints: DRAM shortage (few quarters), wafer/package fab shortage (1‑2 years).  
- Financials: Q1 2026 product revenue $2.31 B (+36.6 % YoY), AI networking guidance $3.5 B for 2026.  

### Tags
[networking] [GPU] [vendor] [observability] [scale‑out] [scale‑up] [scale‑across]  

### Importance
**High** – The shift to 1.6 Tb/s Ethernet and the introduction of ESUN directly affect network bandwidth, latency, and topology choices for AI‑heavy HPC clusters.  

### Why This Matters
HPC administrators must prepare for a near‑term transition to higher‑speed Ethernet fabrics and new rack‑level interconnect protocols to sustain AI workload scaling, while navigating prolonged component lead times.