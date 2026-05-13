**Title**  
HPE Unifies VM and Kubernetes Management in Private Cloud 4.0, Offering Cost‑Efficient Migration Paths for VMware Users

**Summary**  
HPE’s fourth‑generation Private Cloud platform (Private Cloud 4.0) introduces a single management plane that consolidates virtual machine (VM) and Kubernetes container orchestration within the Morpheus interface. The platform supports HPE VM Essentials, native VMware vSphere VMs, and Kubernetes workloads, with a planned GA release in Q3 2026. HPE claims a ten‑fold reduction in VM licensing costs by integrating VM Essentials into its Private Cloud Business Edition. The solution also enables live workload migration from VMware environments to HPE VMs via Zerto, minimizing downtime. Additionally, HPE’s SimpliVity hyperconverged infrastructure now supports Morpheus VM Essentials, and its Alletra MP X10000 storage line adds native RDMA‑enabled file storage and S3‑over‑RDMA object storage, scaling to 16 nodes and 23 PB.

**Source URL**  
[https://www.nextplatform.com/cloud/2026/05/13/hpe-throws-vm-users-a-lifeline-unifying-containers-and-vm-management-in-cloud-stack/5239635](https://www.nextplatform.com/cloud/2026/05/13/hpe-throws-vm-users-a-lifeline-unifying-containers-and-vm-management-in-cloud-stack/5239635)

**Published Date**  
2026‑05‑13T14:36:43+02:00

**Source Credibility**  
[High] – Next Platform is a reputable industry publication with editorial oversight.

**Operational Impact**  
- **Unified Management**: HPC admins can now control VMs, containers, and AI workloads from a single Morpheus dashboard, reducing tooling overhead and simplifying policy enforcement.  
- **Cost Optimization**: The ten‑fold licensing reduction for VM Essentials can lower capital and operating expenses for HPC clusters that still rely on VMs.  
- **Migration Path**: Zerto‑based live migration allows incremental de‑provisioning of VMware workloads with minimal service disruption, easing the transition to HPE‑native hypervisors.  
- **Storage Enhancements**: RDMA‑enabled file storage and S3‑over‑RDMA object storage in Alletra MP X10000 can accelerate I/O‑heavy HPC workloads, particularly those requiring high‑throughput shared storage.  
- **Edge Flexibility**: HPE’s emphasis on distributed hypervisor footprints supports edge deployments, enabling HPC workloads closer to data sources.

**Tags**  
[vendor] [orchestration] [storage] [networking] [scheduler] [observability]

**Importance**  
[High]

**Why This Matters**  
HPC environments increasingly mix legacy VMs with containerized and AI workloads; a unified, cost‑effective management layer from a trusted vendor like HPE can streamline operations, reduce licensing costs, and provide a clear migration path away from expensive VMware licensing, directly impacting budget and operational efficiency.

## Multipath Reliable Connection: A New Ethernet Protocol for Large-Scale AI Clusters

**Source**: The Next Platform (https://www.nextplatform.com/connect/2026/05/12/openai-microsoft-and-friends-build-a-better-more-scalable-ethernet/5239078) | **Date**: 2026-05-12 | **Credibility**: [High Credibility]

**Summary**:
OpenAI, Microsoft, Broadcom, AMD, and Nvidia have developed Multipath Reliable Connection (MRC), a new network protocol that fundamentally shifts how Ethernet networks are built for AI clusters. Rather than chasing higher bandwidth ports (800 Gb/sec), MRC uses the same aggregate bandwidth of 51.2 Tb/sec switch ASICs to increase the number of links between devices—splitting a switch to support 512 ports at 100 Gb/sec instead of 64 ports at 800 Gb/sec. This approach creates eight unique Clos data planes, enabling a two-tier network topology that can connect 131,072 compute engines with no GPU more than three hops away (compared to five to seven hops in traditional three-tier architectures). MRC is a superset extension of RDMA over Converged Ethernet (RoCE) that implements adaptive load balancing via Explicit Congestion Notification (ECN), out-of-order packet delivery, packet spraying across multiple links, selective retransmission, and packet trimming—which only retransmits dropped packets without invoking global ECN. The protocol uses IPv6 segment routing for static routing, eliminating the need for dynamic routing due to the availability of eight parallel paths between endpoints.

**Operational Impact**:
For HPC administrators, MRC represents a significant shift in network architecture planning for large AI clusters. The protocol's fault tolerance is particularly notable: losing one of eight links to a GPU only reduces bandwidth by 12% without stopping the training job, and administrators can replace failed links without interrupting workloads—something impossible with traditional Clos networks where a single link failure can halt the entire cluster. The two-tier topology reduces switch count by approximately 40% while doubling compute capacity, though administrators should carefully model link costs (DAC and optical) since the two-tier design increases total links from 196,608 to 1,179,648. The protocol has been validated on production clusters at Oracle's Stargate (Abilene, Texas) and Microsoft Azure AI (Fairwater, Wisconsin) datacenters using Nvidia ConnectX-8 SmartNICs, AMD Pollara and Vulcano DPUs, Broadcom Thor Ultra SmartNICs, and Nvidia Spectrum 4/5 switches running Cumulus Linux and SONiC, as well as Arista EOS switches with Broadcom Tomahawk 5 ASICs.

**Key Technical Details**:
- Switch ASIC: 51.2 Tb/sec switches with 64 ports at 800 Gb/sec traditional vs 512 ports at 100 Gb/sec with MRC
- Network topology: Two-tier (leaf + spine) vs traditional three-tier (leaf + spine + superspine)
- Compute capacity: 131,072 GPUs/XPUs in two-tier MRC vs 65,536 in three-tier traditional
- Hop count: Maximum 3 hops (MRC) vs 5-7 hops (traditional three-tier)
- Switch requirements: 6,144 switches for 131,072 endpoints vs 5,120 switches for 65,536 endpoints
- Link redundancy: 8 parallel paths per endpoint; single link failure = 12.5% bandwidth loss (not cluster failure)
- Protocol stack: MRC over RoCE, IPv6 segment routing (SRv6) for static routing
- SmartNIC support: Nvidia ConnectX-8, AMD Pollara/Vulcano DPUs, Broadcom Thor Ultra
- Switch support: Nvidia Spectrum 4/5 (Cumulus Linux/SONiC), Arista EOS (Tomahawk 5)
- Tested at: Oracle Stargate (Abilene, TX), Microsoft Azure AI (Fairwater, WI)

**Tags**: [networking] [GPU] [infrastructure] [vendor] [orchestration]

**Importance**: [High]

**Why This Matters**:
HPC administrators planning large AI clusters should evaluate MRC-compatible networking equipment, as the protocol delivers substantial improvements in fault tolerance, network latency, and scale while reducing overall switch costs—making it a compelling alternative to traditional three-tier RoCE architectures or InfiniBand for next-generation AI infrastructure.

## IT Spending Surge: Datacenter Infrastructure Costs Escalate 55.8% in 2026

**Source**: [The Next Platform](https://www.nextplatform.com/compute/2026/05/11/compute-and-memory-price-hikes-drive-it-spending-way-higher/5238181) | **Date**: 2026-05-11 | **Credibility**: [High]

**Summary**:
Gartner's revised IT spending forecast for 2026 shows global IT expenditure reaching $6.32 trillion, a 13.5% increase over 2025's $5.56 trillion. The most significant shift is in datacenter systems spending, which Gartner now projects will grow 55.8% to $788 billion in 2026—up from an earlier February forecast of 31.7% growth ($653.4 billion). This represents an incremental $134.6 billion added to datacenter spending projections in just three months. The driving factors include severe CPU and GPU compute shortages, main memory and flash memory constraints, and massive investments by hyperscalers and AI model makers (Anthropic, OpenAI) in training and inference infrastructure. Datacenter systems now represent 12.5% of overall IT spending, up from 4.5% in 2012, indicating a fundamental shift in IT budget allocation toward core infrastructure.

**Operational Impact**:
HPC administrators face a challenging procurement environment with constrained hardware availability and escalating costs. Budget planning for infrastructure upgrades must account for 50%+ price increases for servers, storage, and networking components. Organizations should expect longer procurement lead times for GPU clusters and high-density compute nodes. The shift toward core IT spending (now 64.9% of total IT budgets vs 35.9% in 2012) suggests increased organizational prioritization of infrastructure—but also greater scrutiny on ROI for HPC investments. Administrators should document infrastructure requirements with clear business value justification given the competitive landscape for hardware allocation.

**Key Technical Details**:
- Global IT spending 2026: $6.32 trillion (13.5% YoY growth)
- Datacenter systems spending 2026: $788 billion (55.8% YoY growth)
- Datacenter share of IT spending: 12.5% (2026) vs 4.5% (2012)
- Core IT spending 2026: $4.1 trillion (18% growth)
- February 2026 forecast revision added $134.6B to datacenter spending in 3 months
- Major buyers: Hyperscalers, cloud builders, AI model makers (Anthropic, OpenAI going public)
- Shortages: CPU, GPU compute, DRAM, flash memory

**Tags**: [infrastructure] [enterprise HPC trends] [GPU] [storage]

**Importance**: [High]

**Why This Matters**: HPC administrators must prepare for significantly higher infrastructure costs and longer procurement timelines as datacenter spending surges 55.8%, driven by AI compute demand outpacing available CPU/GPU supply—requiring updated budget justifications and procurement strategies.

**Title**  
AMD Launches Air‑Cooled MI350P GPU for Mid‑Scale GenAI Inference and Small‑Scale Training  

**Summary**  
AMD has introduced the MI350P, a PCI‑Express, air‑cooled variant of its MI350 series. The card contains half the silicon of the full‑size MI350X, delivering 2.2 GHz core frequency and 4 TB/s HBM3E bandwidth. Performance figures show 90 % of peak bandwidth and 58–66 % of peak compute for 16‑bit and 8‑bit workloads, with MXFP6 at 58 % and MXFP4 at 50 %. The MI350P is rated at 600 W TDP, with a 450 W throttle that reduces clock speed to ~1.9–2 GHz, yielding only a 10–15 % drop in performance while saving ~25 % power. The GPU is designed for models with ~200–250 B parameters, suitable for enterprise inference workloads. OEMs such as Dell, HPE, Lenovo, Cisco, and Supermicro are already integrating the MI350P into rack‑scale servers (e.g., Dell PowerEdge XE7745, HPE ProLiant DL385 Gen 11).  

**Source URL**  
[Next Platform – “Sometimes, Air Is The Only Way For AI Systems To Keep Their Cool”](https://www.nextplatform.com/compute/2026/05/08/sometimes-air-is-the-only-way-for-ai-systems-to-keep-their-cool/5237421)  

**Published Date**  
2026‑05‑08T18:09:19+02:00  

**Source Credibility**  
[High Credibility] – Next Platform is a well‑established, peer‑reviewed industry publication.  

**Operational Impact**  
- **Thermal Planning**: The MI350P’s 600 W TDP and optional 450 W throttle require careful rack cooling design; air‑cooled systems can be deployed in data centers lacking liquid cooling infrastructure.  
- **Cost‑Performance Trade‑off**: The 450 W mode offers ~10–15 % performance loss for ~25 % power savings, enabling tighter budget or power‑constrained deployments.  
- **Model Size Alignment**: Ideal for 200–250 B parameter models; administrators should benchmark against their target inference workloads to confirm fit.  
- **Vendor Ecosystem**: Availability from major OEMs (Dell, HPE, Lenovo, Cisco, Supermicro) simplifies procurement and support; however, limited GPU‑to‑GPU coherency means multi‑GPU scaling will rely on PCIe interconnects rather than HBM coherency.  
- **Software Stack**: Ensure that orchestration tools (e.g., Kubernetes, Slurm) support PCIe‑based GPU nodes and that drivers expose the correct compute capabilities (OCP‑FP8, MXFP6/4).  

**Tags**  
[vendor] [GPU] [orchestration] [storage] [networking]  

**Importance**  
[High] – The MI350P provides a viable air‑cooled alternative to liquid‑cooled high‑end GPUs, impacting procurement, cooling, and deployment decisions for mid‑scale HPC and AI workloads.  

**Why This Matters**  
HPC administrators must evaluate the MI350P’s power‑efficient performance and air‑cooling suitability for inference‑heavy workloads, as it enables cost‑effective scaling without liquid cooling while maintaining competitive throughput for large‑scale GenAI models.

## Title  
Arista’s AI‑Focused Ethernet Fabrics Target Scale‑Out, Scale‑Up, and Scale‑Across Deployments; 1.6 Tb/s Ports Planned for 2027  

**Source**: [The Next Platform](https://www.nextplatform.com/connect/2026/05/07/arista-rides-ai-scale-out-networks-moves-into-scale-across-and-awaits-scale-up/5235293)  
**Published Date**: 2026‑05‑07T19:49:28+02:00  
**Source Credibility**: **High** – The Next Platform is a well‑established, editorially‑reviewed technology news outlet with a strong track‑record for accurate reporting on data‑center and HPC hardware.  

### Summary  
Arista Networks is positioning its Ethernet switching portfolio to become a primary supplier for AI‑driven high‑performance computing (HPC) interconnects. The company expects AI‑related networking revenue to rise from $3.25 B to $3.5 B in FY 2026, driven by “scale‑out” Ethernet fabrics (leaf‑spine) and the forthcoming “scale‑up” (ESUN – Ethernet for Scale‑Up Networking) and “scale‑across” protocols slated for mass production in 2027. Scale‑up will enable dynamic allocation of compute resources within a rack using co‑packaged copper (CPC) or open co‑packaged optics (CPO), while scale‑across targets inter‑datacenter fabrics that can sustain up to 1.6 Tb/s per port.  

Arista reports strong Q1 2026 financials (product revenue $2.31 B, +36.6 % YoY) and a cash position of $12.35 B, allowing pre‑payment for ASICs and other components amid a broader semiconductor supply shortage. The company notes that early adopters are already testing ESUN on 800 Gb/s hardware, but the majority of trials await the availability of 1.6 Tb/s ports. No concrete sales forecasts for scale‑up or scale‑across are given; however, the CEO projects that scale‑across could represent one‑third to two‑thirds of AI networking revenue in the mid‑term.  

### Operational Impact  
- **Network Architecture Planning**: HPC sites should evaluate whether Arista’s upcoming 1.6 Tb/s Ethernet ports and ESUN scale‑up capabilities align with their roadmap for exascale or AI‑focused clusters. Early engagement can secure component allocations before the expected wafer‑fabrication bottleneck eases (estimated 1–2 years).  
- **Rack‑Level Interconnects**: The move to CPC/CPO and collective protocol acceleration at L2/L3 suggests that future Arista switches will support lower latency, higher bandwidth rack‑level fabrics without requiring proprietary ASICs (e.g., NVIDIA’s Mellanox). Administrators may need to redesign rack topologies to exploit the “scale‑up” dynamic bandwidth provisioning.  
- **Inter‑Datacenter Links**: Scale‑across Ethernet fabrics promise wire‑rate load balancing and L2/L3 collective acceleration across sites. HPC centers planning multi‑site AI training or distributed simulations should consider Arista’s scale‑across as a potential alternative to InfiniBand or custom optical interconnects, pending availability of 1.6 Tb/s ports.  
- **Supply‑Chain Management**: Given the disclosed component shortages, HPC procurement teams should place early purchase orders or pre‑pay for switch ASICs to guarantee delivery timelines for 2027 roll‑outs.  

### Key Technical Details  
- **ESUN (Ethernet for Scale‑Up Networking)** – new protocol enabling flexible compute scaling within a rack; production targeted for 2027.  
- **Scale‑Out Fabric** – current leaf/spine Ethernet deployments up to 800 Gb/s per port; >100 customers with cumulative 800 Gb/s deployments.  
- **Scale‑Across Fabric** – planned 1.6 Tb/s Ethernet ports (CPC or CPO) for inter‑datacenter AI systems; expected production scale in 2027.  
- **Financial Indicators** – AI networking revenue guidance $3.5 B for FY 2026; cash $12.35 B; Q1 product revenue $2.31 B (+36.6 % YoY).  
- **Supply Constraints** – current DRAM shortage transitioning to wafer/package fabrication bottleneck; normalization projected 1–2 years.  

### Tags  
[networking] [vendor] [GPU] [scale‑out] [scale‑up] [scale‑across] [interconnect]  

### Importance  
**High** – The announced capabilities directly affect the design of future HPC interconnects for AI workloads and may replace or complement existing InfiniBand solutions.  

### Why This Matters  
Arista’s roadmap introduces 1.6 Tb/s Ethernet and dynamic rack‑level scaling that could become the de‑facto standard for exascale AI clusters, forcing HPC administrators to reassess network hardware choices, topology designs, and procurement strategies now.