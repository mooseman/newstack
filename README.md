
** Newstack -  a toy proof-of-concept for the Internet network stack re-done from scratch.  **  


Introduction

The traditional seven-layer OSI model (and the four- or five-layer TCP/IP stack often taught in practice) succeeded in its era by providing a modular approach to networking. However, the design can feel “clunky” by modern standards: layering redundancies, historical artifacts, and the late-in-the-game addition of security features have all contributed to a stack that is powerful, but not always elegant. With today’s computing paradigms—cloud computing, edge computing, mobile-first networking, and strong emphasis on end-to-end security—there’s an opportunity to conceive of a fresh, streamlined architecture.

The question is: if we started from a clean slate, with no baggage from legacy protocols, how might we completely re-design the stack to be (1) secure by default, (2) minimalist with as few layers as possible, (3) flexible in adapting to new technologies, and (4) elegantly structured?

Below is a conceptual approach to such a design.

High-Level Goals for a New Design

    Security by Default: Every communication channel should be cryptographically secure and authenticated from the start. No separate or bolted-on security layers—encryption, integrity checks, and authentication are integral at the core level.

    Minimalism in Layering: Instead of seven layers, aim for a smaller number—possibly three conceptual layers:
        Unified Link/Network Layer
        Session/Transport/Security Layer
        Application/Service Layer

    Or even consider a two-layer approach if certain responsibilities can be collapsed (e.g., secure transport and routing combined into a single "foundation" layer, with an application layer on top).

    Flexibility and Extensibility: The design should allow incremental adoption of new link technologies, new addressing schemes, and new transport semantics without forcing a wholesale redesign. A well-defined abstraction boundary allows innovation below and above without breaking everything else.

    Elegant, Unified Addressing and Naming: Instead of juggling IP addresses, DNS names, MAC addresses, and various ephemeral identifiers, adopt a unified, cryptographic naming system that can serve as the stable bedrock for secure routing and identification.

    Context-Aware Services: Allow the application layer to specify transport needs (latency-sensitive, loss-tolerant, multi-path support, etc.) through a simplified API that the transport layer can fulfill dynamically, rather than hard-coding multiple transport protocols.

Conceptual Redesign

Layer 1: The Foundation Layer (Physical + Link + Network Unified)

    Responsibilities:
        Physical Transmission & Media Abstraction: Abstract away cables, fiber, wireless frequencies, and optical links.
        Data Link Reliability & Framing: Basic error detection and possibly limited local correction, but keep complexity low.
        Routing & Forwarding Using Self-Certifying Addresses: Instead of IP addresses, use self-certifying identifiers (SCIDs). An SCID might be derived from a public key, ensuring that each address is intrinsically tied to a cryptographic identity. This simplifies authentication and eliminates the need for a separate PKI system at higher layers.
        Name-Based Forwarding & Late Binding: Rather than rigid host-based addresses, consider content- or identity-based routing paradigms (e.g., Named Data Networking concepts). Routers forward based on names or secure identifiers, enabling more flexible network architectures (e.g., content caching, multi-path forwarding).

    Security Integration:
        All packets at this layer carry cryptographic signatures that routers can verify efficiently. This prevents large classes of spoofing and certain denial-of-service attacks at the fundamental level.
        Basic encryption of payload headers can be optional at this layer. However, due to performance reasons, full payload encryption might be delegated to the next layer.

    Outcome: The Foundation Layer provides a uniform abstraction of “secure, addressable endpoints” on a global scale. It reduces the complexity of having separate MAC, IP, and ARP layers. Endpoints and services are named with cryptographic identities, and routing is flexible and policy-driven.

Layer 2: The Secure Transport/Session Layer

    Responsibilities:
        End-to-End Encryption and Authentication: By the time data reaches this layer, endpoints establish a secure session with strong encryption (like a next-generation variant of TLS, but built natively into the stack).
        Stateful Multiplexing and Transport Options: Instead of having separate protocols like TCP, UDP, and QUIC, have a single, flexible transport core that can be tuned via parameters. For example:
            Reliability toggles (fully reliable, partially reliable, best-effort)
            Congestion control schemes selectable by the application (or negotiable)
            Latency or bandwidth optimization modes
            Multipath support by default, leveraging the SCID-based routing below
        Session Management: Sessions (like QUIC connections or TLS sessions) are first-class citizens. Negotiation of cipher suites, transport parameters, and flow control behavior occurs here. Sessions are tied to identities (SCIDs) from the foundation layer, ensuring no separate naming complexity.

    Security Integration:
        Mandatory encryption for all user data. Clear-text transmission is not even an option.
        Key exchange and authentication integrated into the session establishment.
        Ephemeral keys to ensure forward secrecy.

    Outcome: The Secure Transport/Session Layer provides an application-neutral, secure, and flexible transport service. Applications simply request a session with certain properties and get a secure, tuned data stream or datagram service. This collapses the complexity of multiple separate transport protocols and add-on security layers into one elegant system.

Layer 3: The Application/Service Interface Layer

    Responsibilities:
        Service Discovery and Binding: Applications can request connections by referring to service identifiers (which map to SCIDs under the hood). The system can handle dynamic service resolution, caching, and load balancing at this layer.
        Data Framing and Semantics: Applications may want to exchange discrete messages, streams, or complex objects. The interface layer helps package data in a way that can be efficiently handed down to the secure transport.
        Policy Expression: Applications can specify policies (e.g., “low latency is critical, accept partial reliability,” or “high reliability, no data loss, streaming mode”).
        Advanced Features: Built-in support for content negotiation, compression, and even application-layer encryption/hashing for domain-specific purposes. However, these features are optional and sit atop a secure foundation.

    Security Integration:
        Authentication and authorization hooks integrated at the application level, but they build upon the cryptographic identities already established by lower layers. No need to reinvent the wheel.
        Fine-grained access control lists (ACLs) or capability tokens can be negotiated as part of session setup.

    Outcome: The Application/Service Interface Layer is a clean, well-defined API boundary. Developers interact with a secure, abstract transport without worrying about how addresses are assigned or how keys are negotiated. The complexity is hidden below, enabling easy adaptation to future technologies or protocols.

Key Architectural Innovations

    Self-Certifying Addresses (SCIDs):
    By making addresses inherently cryptographic, many trust and identity problems vanish. Instead of DNS + IP + ARP, you have one stable naming mechanism that also ensures authenticity.

    Unified Routing & Link Abstraction:
    Combine the physical, data link, and network layers into a single “foundation” that simply delivers named secure endpoints. Differences in physical media, packet framing, and path selection are hidden behind a stable interface.

    Single, Configurable Transport Mechanism:
    Instead of a proliferation of transport protocols, have one flexible “session protocol” that can be specialized using parameters. This prevents fragmentation and complexity.

    Security Integrated from the Ground Up:
    Encryption and authentication are not an afterthought. Every connection is secure by design, simplifying the mental model and making eavesdropping or tampering much harder.

    Minimal Layer Count and Crisp Boundaries:
    With three main conceptual layers (Foundation, Transport/Session, Application Interface) or even a two-layer model if the application interface is considered just an API atop transport, the design is simpler, more understandable, and more elegant.

Comparisons and Inspirations

    QUIC: QUIC integrates security (TLS 1.3) with transport and reduces round trips. Our proposal takes this philosophy even further by building the equivalent of QUIC’s secure transport into the very core of the stack, rather than layering it over IP.

    Named Data Networking (NDN): NDN’s approach to using names as first-class network addresses can inspire the foundation layer. By routing on content names (or SCIDs), the network can optimize itself for various forwarding strategies, caching, and multi-path routing.

    Self-Certifying File Systems (e.g., SFS): Borrowing the concept of names that embed public keys ensures authenticity of endpoints and content without complex PKI.

Conclusion

This proposed redesign is admittedly ambitious and not fully backward-compatible with today’s installed base. Yet, if we could reinvent the stack from scratch, we would strive for:

    Far fewer conceptual layers (e.g., three).
    Security embedded at every step.
    Unified naming and addressing for simpler, more secure routing.
    A single, flexible transport/session mechanism that replaces a slew of legacy protocols.
    A clean and elegant application interface that abstracts away all the underlying complexity.

Such a design would be more elegant, inherently secure, and better prepared for future evolutions of network technology than the historically layered and sometimes “clunky” stacks we rely on today.

