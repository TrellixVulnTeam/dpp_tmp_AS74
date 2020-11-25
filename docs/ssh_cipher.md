## Cipher Suite

**Aktueller Stand:**

In Linux Red Hat sind folgende Cipher Suite deaktiviert. Diese können jedoch für einzelne Anwendung durch eine explizite Konfiguration aktiviert werden:
- DH mit Parametern < 1024 Bit
- RSA mit Schlüsselgröße < 1024 Bit
- Kamelie
- ARIA
- SEED
- IDEA
- Integrity-only cipher suites
- TLS-CBC-Modus-Verschlüsselungssuites mit SHA-384 HMAC
- AES-CCM8
- Alle ECC-Kurven, die mit TLS 1.3 inkompatibel sind, einschließlich secp256k1
- IKEv1 (seit RHEL 8)

<br>
In der nachfolgenden Tabelle werden drei Ebenen vorgestellt, die in der darauffolgenden Tabelle die Cipher Suites zeigt, die hierfür aktiv sind. 
<br><br>

| Default (Standard) | Legacy (Red Hat Enterprise Linux 5 oder früher) | Future (Zukunft sicher) |
|--|--|--|
| Die standardmäßige systemweite Richtlinienebene bietet sichere Einstellungen für aktuelle Bedrohungen. Es ermöglicht die Protokolle TLS 1.2 und 1.3 sowie IKEv2 und SSH2. Protokolle. Die RSA-Schlüssel und Diffie-Hellman-Parameter werden nur akzeptiert, wenn diese mindestens 2048 Bit lang sind. | In der nachfolgenden Tabelle werden drei Ebenen vorgestellt, die in der darauffolgenden Tabelle die Cipher Suites zeigt, die hierfür aktiv sind. Diese Richtlinie gewährleistet maximale Kompatibilität mit Red Hat Enterprise Linux 5 und früher. Aufgrund einer erhöhten Angriffsfläche ist die Richtlinie weniger sicher. Zusätzlich zu den Algorithmen und Protokollen auf DEFAULT-Ebene umfasst sie Unterstützung für die Protokolle TLS 1.0 und 1.1. Die Algorithmen DSA, 3DES und RC4 sind erlaubt, während RSA-Schlüssel und Diffie-Hellman Parameter nur akzeptiert werden, wenn diese mindestens 1023 Bit lang sind. | Ein konservatives Sicherheitsniveau, von dem angenommen wird, dass es allen kurzfristigen künftigen Angriffen standhält. Diese Stufe erlaubt nicht die Verwendung von SHA-1 in Signaturalgorithmen. Die RSA-Schlüssel und Diffie-Hellman-Parameter werden hierbei nur akzeptiert, wenn diese mindestens 3072 Bit lang sind. |

<br>

|  | Legacy | Default | Future |
|--|--|--|--|
| IKEv1 | no | no | no |
| 3DES | yes | no | no |
| RC4 | yes | no | no |
| DH | min. 1024-bit | min. 2048-bit | min. 3072-bit |
| RSA | min. 1024-bit | min. 2048-bit | min. 3072-bit |
| DSA | yes | no | no |
| TLS v1.0 | yes | no | no |
| TLS v1.1 | yes | no | no |
| SHA-1 in digital signatures| yes | yes | no |
| CBC mode ciphers | yes | yes | no |
| Symetric ciphers with keys <256 bits | yes | yes | no |
| SHA-1 and SHA-224 signatures in certificates | yes | yes | no |