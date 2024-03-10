# Foreword

The [*Security Protocols and Data Models (SPDM)*](#security-protocols-and-data-models) Working Group of the [DMTF](#dmtf) prepared the *Security Protocol and Data Model (SPDM) Specification* (DSP0274).  DMTF is a not-for-profit association of industry members that promotes enterprise and systems management and interoperability.  For information about the DMTF, see [DMTF](https://www.dmtf.org/ "https://www.dmtf.org/").

This version supersedes version 1.2 and its errata versions. For a list of the changes, see [ANNEX E (informative) change log](#annex-e-informative-change-log).

# Introduction

The *Security Protocol and Data Model (SPDM) Specification* defines [*messages*](#message), data objects, and sequences for performing message exchanges over a variety of transport and physical media.  The description of message exchanges includes [*authentication*](#authentication) and provisioning of hardware identities, measurement for firmware identities, session key exchange protocols to enable confidentiality with integrity-protected data communication, and other related capabilities.  The SPDM enables efficient access to low-level security capabilities and operations.  Other mechanisms, including non-DMTF-defined mechanisms, can use the SPDM.

## Advice

The authors recommend readers visit tutorial and education materials under [Security Protocols and Data Models](https://www.dmtf.org/standards/spdm) and [Platform Management Communications Infrastructure (PMCI)](https://www.dmtf.org/standards/pmci) on the DMTF website prior to or during the reading of this specification to help understand this specification.

## Conventions

The following conventions apply to all SPDM specifications.

### Document conventions

* Document titles appear in *italics*.
* The first occurrence of each important term appears in *italics* with a link to its definition.
* ABNF rules appear in a monospaced font.

### Reserved and unassigned values

Unless otherwise specified, any reserved, unspecified, or unassigned values in enumerations or other numeric ranges are reserved for future definition by the DMTF.

Unless otherwise specified, field values marked as Reserved shall be written as zero (`0`), ignored when read, not modified, and not interpreted as an error if not zero, and used in transcript hash calculations as is.

### Byte ordering

Unless otherwise specified, for all SPDM specifications [*byte*](#byte) ordering of multi-byte numeric fields or multi-byte bit fields is *little endian* (that is, the lowest byte offset holds the least significant byte, and higher offsets hold the more significant bytes).

#### Hash byte order

For fields or values containing a digest or hash, SPDM preserves the byte order of the digest as the specification of a given hash algorithm defines. SPDM views these digests, simply, as a string of octets where the first byte is the leftmost byte of the digest, the second byte is the second leftmost byte, the third byte is the third leftmost byte, and this pattern continues until the last byte of the digest. Thus, the byte order for SPDM digests or hashes is: the first byte is placed at the lowest offset in the field or value, the second byte is placed at the second lowest offset, the third byte is placed at the third lowest offset in the field or value and this pattern continues until the last byte.

For example, in [FIPS 180-4](#ref-fips-sha2), a SHA 256 hash is the concatenation of eight 32-bit words where each word is in *big endian* order, but the order of words does not have any endianness associated with it. SPDM simply views this 256-bit digest as a string of octets that is 32 bytes in size where the first byte is the value at H<sub>0</sub>[31:24] of the final digest, the second byte is the value at H<sub>0</sub>[23:16], the third byte is the value at H<sub>0</sub>[15:8], the fourth byte is the value at H<sub>0</sub>[7:0], the fifth bytes is the value at H<sub>1</sub>[31:24], and this pattern continues until the last byte, which is the value at H<sub>7</sub>[7:0], where the FIPS 180-4 specification defines H<sub>0</sub>, H<sub>1</sub>, and H<sub>7</sub>.

#### Encoded ASN.1 byte order

For fields or values containing DER, CER, or BER encoded data, SPDM preserves the byte order as described in [X.690](#ref_asn1) specification. SPDM views a DER, CER, or BER encoded data as simply a string of octets where the first byte is the leftmost byte of Figure 1 or Figure 2 in the [X.690](#ref_asn1) specification, the second byte is the second leftmost byte, the third byte is the third leftmost byte, and this pattern continues until the last byte. The first byte is also called either the Identifier octet or the Leading identifier octet. The X.690 specification defines Figure 1, Figure 2, and identifier octets. When populating a DER, CER, or BER encoded data in SPDM fields, the first byte is placed in the lowest address, the second byte is placed in the second lowest offset, the third byte is placed in the third lowest offset in the field or value and this pattern continues until the last byte.

#### Octet string byte order

A string of octets is conventionally written from left to right. Also by convention, byte zero of the octet string shall be the leftmost byte of the octet, byte 1 of the octet string shall be the second leftmost byte of the octet, and this pattern shall continue until the very last byte. When placing an octet string into an SPDM field, the i<sup>th</sup> byte of the octet string shall be placed in the i<sup>th</sup> offset of that field.

For example, if placing an octet stream consisting of "0xAA 0xCB 0x9F 0xD8" into `DMTFSpecMeasurementValue` field, then offset 0 (the lowest offset) of `DMTFSpecMeasurementValue` will contain 0xAA, offset 1 of `DMTFSpecMeasurementValue` will contain 0xCB, offset 2 of `DMTFSpecMeasurementValue` will contain 0x9F, and offset 3 of `DMTFSpecMeasurementValue` will contain 0xD8.

#### Signature byte order

For fields or values containing a signature, SPDM attempts to preserve the byte order of the signature as the specification of a given signature algorithm defines. Most signature specifications define a string of octets as the format of the signature, and others may explicitly state the endianness such as in the specification for [Edwards-Curve Digital Signature Algorithm](#rfc8032). Unless otherwise specified, the byte order of a signature for a given signature algorithm shall be [octet string byte order](#octet-string-byte-order).

##### ECDSA signatures byte order

[FIPS PUB 186-5](#ref-ecdsa) defines `r`, `s`, and ECDSA signature to be `(r, s)`, where `r` and `s` are just integers. For ECDSA signatures, excluding SM2, in SPDM, the signature shall be the concatenation of `r` and `s`. The size of `r` shall be the size of the selected curve. Likewise, the size of `s` shall be the size of the selected curve. See `BaseAsymAlgo` in `NEGOTIATE_ALGORITHMS` for the size of `r` and `s`. The byte order for `r` and `s` shall be big-endian order.  When placing ECDSA signatures into an SPDM signature field, `r` shall come first, followed by `s`.

##### SM2 signatures byte order

[GB/T 32918.2-2016](#ref_gbt32918_2_2016) defines `r` and `s` and SM2 signatures to be `(r, s)`, where `r` and `s` are just integers. The size of `r` and `s` shall each be 32 bytes. To form an SM2 signature, `r` and `s` shall be converted to an octet stream according to GB/T 32918.2-2016 and [GB/T 32918.1-2016](#ref_gbt32918_1_2016) with a target length of 32 bytes. Let the resulting octet string of `r` and `s` be called `SM2_R` and `SM2_S` respectively. The final SM2 signature shall be the concatenation of `SM2_R` and `SM2_S`. When placing SM2 signatures into an SPDM signature field, the SM2 signature byte order shall be [octet string byte order](#octet-string-byte-order).

### Sizes and lengths

Unless otherwise specified, all sizes and lengths are in units of bytes.

### SPDM data type conventions

#### SPDM data types

[Table 1 &mdash; SPDM data types](#table-spdm-data-types) lists the abbreviations and descriptions for common data types that SPDM message fields and data structure definitions use.  These definitions follow [DSP0240](#dsp0240).

<a id="table-spdm-data-types"></a>**Table 1 &mdash; SPDM data types**

| Data type    | Interpretation                                                |
|:-------------|:--------------------------------------------------------------|
| `ver8`       | Eight-bit encoding of the SPDM version number. [Version encoding](#version-encoding) defines the encoding of the version number. |
| `bitfield8`  | Byte with 8-bit fields.                                   |
| `bitfield16` | Two-byte word with 16-bit fields.                             |

#### Integers

Unless noted otherwise, integers shall be unsigned.

### Version encoding

The `SPDMVersion` field represents the version of the specification through a combination of *Major* and *Minor* nibbles, encoded as follows:

| Version | Matches | Incremented when |
|:--------|:--------|:-----------------|
| Major   | Major version field in the `SPDMVersion` field in the SPDM message header. | Protocol modification breaks backward compatibility. |
| Minor   | Minor version field in the `SPDMVersion` field in the SPDM message header. | Protocol modification maintains backward compatibility. |

EXAMPLE:

Version 3.7 → `0x37`

Version 1.0 → `0x10`

Version 1.2 → `0x12`

An [*endpoint*](#endpoint) that supports Version 1.2 can interoperate with an older endpoint that supports Version 1.0 or other previous minor versions. Whether an endpoint supports inter-operation with previous minor versions of the SPDM specification is an implementation-specific decision.

An endpoint that supports Version 1.2 only and an endpoint that supports Version 3.7 only are not interoperable and shall not attempt to communicate beyond `GET_VERSION`.

This specification considers two minor versions to be interoperable when it is possible for an implementation that is conformant to a higher minor version number to also communicate with an implementation that is conformant to a lower minor version number with minimal differences in operation. In such a case, the following rules apply:

* Both endpoints shall use the same lower version number in the `SPDMVersion` field for all messages.
* Functionality shall be limited to what the lower minor version of the SPDM specification defines.
* Computations and other operations between different minor versions of the Secured Messages using SPDM specification should remain the same, unless security issues of lower minor versions are fixed in higher minor versions and the fixes require change in computations or other operations. These differences are dependent on the value in the `SPDMVersion` field in the message.
* In a newer minor version of the SPDM specification, a given message can be longer, bit fields and enumerations can contain new values, and reserved fields can gain functionality. Existing numeric and bit fields retain their existing definitions.
* Errata versions (indicated by a non-zero value in the `UpdateVersionNumber` field for the `GET_VERSION` request and `VERSION` response messages) clarify existing behaviors in the SPDM specification. They maintain bitwise compatibility with the base version, except as required to fix security vulnerabilities or to correct mistakes from the base version.

For details on the version agreement process, see [GET_VERSION request and VERSION response messages](#get_version-request-and-version-response-messages). The detailed version encoding that the `VERSION` response message returns contains an additional byte that indicates specification bug fixes or development versions. See [Table 9 &mdash; Successful VERSION response message format](#table-successful-version-response-message-format).

### Notations

SPDM specifications use the following notations:

| Notation                                         | Description                              |
|:-------------------------------------------------|:-----------------------------------------|
| `Concatenate()` | The concatenation function `Concatenate(a, b, ..., z)`, where the first entry occupies the least-significant bits and the last entry occupies the most-significant bits. |
| `M:N` | In field descriptions, this notation typically represents a range of byte offsets starting from byte `M` and continuing to and including byte `N` (`M ≤ N`).<br/><br/>The lowest offset is on the left.  The highest offset is on the right. |
| `[4]` | Square brackets around a number typically indicate a bit offset.<br/><br/>Bit offsets are zero-based values.  That is, the least significant bit (`[LSb]`) offset = 0. |
| `[M:N]` | A range of bit offsets where M is greater than or equal to N.<br/><br/>The most significant bit is on the left, and the least significant bit is on the right. |
| `1b` | A lowercase `b` after a number consisting of `0`s and `1`s indicates that the number is in binary format. |
| `0x12A` | Hexadecimal, as indicated by the leading `0x`. |
| `N+`    | Variable-length byte range that starts at byte offset N. |
| `{ Payload }` | Used mostly in figures, this notation indicates that the payload specified in the enclosing curly brackets is encrypted and/or authenticated by the keys derived from one or more major secrets. The specific secret used is described throughout this specification. For example, `{ HEARTBEAT }` shows that the Heartbeat message is encrypted and/or authenticated by the keys derived from one or more major secrets. |
| <!-- markdownlint-disable MD033 --> <code>{ Payload }::[[S<sub>X</sub>]]</code> | Used mostly in figures, this notation indicates that the payload specified in the enclosing curly brackets is encrypted and/or authenticated by the keys derived from major Secret X.<br/><br/>For example, <code>{ HEARTBEAT }::[[S<sub>2</sub>]]</code> shows that the Heartbeat message is encrypted and/or authenticated by the keys derived from major secret <code>S<sub>2</sub></code>. |
| `[${message_name}]`.`${field_name}` | Used to indicate a field in a message. <br/><ul><li>`${message_name}` is the name of the request or response message.</li><li>`${field_name}` is the name of the field in the request or response message. An asterisk (`*`) instead of a field name means all fields in that message except for any conditional fields that are empty (as for example `KEY_EXCHANGE`.`OpaqueData`).</li></ul> |
<!--markdownlint-enable MD033 -->

### Text or string encoding

When a value is indicated as a text or string data type, the encoding for the text or string shall be an array of contiguous [*bytes*](#byte) whose values are ordered. The first byte of the array resides at the lowest offset, and the last byte of the array is at the highest offset. The order of characters in the array shall be such that the leftmost character of the string is placed at the first byte in the array, the second leftmost character is placed in the second byte, and so forth until the last character is placed in the last byte.

Each byte in the array shall be the numeric value that represents that character, as [ASCII &mdash; ISO/IEC 646:1991](#ascii) defines.

[Table 2 &mdash; "spdm" encoding example](#table-spdm-encoding-example) shows an encoding example of the string "spdm":

<a id="table-spdm-encoding-example"></a>**Table 2 &mdash; "spdm" encoding example**

| Offset | Character | Value  |
|:-------|:----------|:-------|
| 0      | s         | `0x73` |
| 1      | p         | `0x70` |
| 2      | d         | `0x64` |
| 3      | m         | `0x6D` |

### Deprecated material

Deprecated material is not recommended for use in new development efforts. Existing and new implementations can use this material, but they shall move to the favored approach as soon as possible. Implementations can implement any deprecated elements as required by this document to achieve backward compatibility. Although implementations can use deprecated elements, they are directed to use the favored elements instead.

The following typographical convention indicates deprecated material:

---------------------------

DEPRECATED

Deprecated material appears here.

DEPRECATED

---------------------------

In places where this typographical convention cannot be used (for example, in tables or figures), the "DEPRECATED" label is used alone.

### Other conventions

Unless otherwise specified, all figures are informative.

# Scope

This specification describes how to use messages, data objects, and sequences to exchange messages between two devices over a variety of transports and physical media.  This specification contains the message exchanges, sequence diagrams, message formats, and other relevant semantics for such message exchanges, including authentication of hardware identities and firmware measurements.

Other specifications define the mapping of these messages to different transports and physical media.  This specification provides information to enable security policy enforcement but does not specify individual policy decisions.

# Normative references

The following documents are indispensable for the application of this specification.  For dated or versioned references, only the edition cited, including any corrigenda or DMTF update versions, applies.  For references without date or version, the latest published edition of the referenced document (including any corrigenda or DMTF update versions) applies.

* <a id="iso-iec-directives"></a>[*ISO/IEC Directives, Part 2, Principles and rules for the structure and drafting of ISO and IEC documents - 2021 (9th edition)*](https://www.iso.org/sites/directives/current/part2/index.xhtml "https://www.iso.org/sites/directives/current/part2/index.xhtml")
* <a id="dsp0004"></a>DMTF DSP0004, *Common Information Model (CIM) Metamodel*, [https://www.dmtf.org/sites/default/files/standards/documents/DSP0004_3.0.1.pdf](https://www.dmtf.org/sites/default/files/standards/documents/DSP0004_3.0.1.pdf "https://www.dmtf.org/sites/default/files/standards/documents/DSP0004_3.0.1.pdf")
* <a id="dsp0223"></a>DMTF DSP0223, *Generic Operations*, [https://www.dmtf.org/sites/default/files/standards/documents/DSP0223_1.0.1.pdf](https://www.dmtf.org/sites/default/files/standards/documents/DSP0223_1.0.1.pdf "https://www.dmtf.org/sites/default/files/standards/documents/DSP0223_1.0.1.pdf")
* <a id="dsp0236"></a>DMTF DSP0236, *MCTP Base Specification 1.3.0*, [https://dmtf.org/sites/default/files/standards/documents/DSP0236_1.3.0.pdf](https://dmtf.org/sites/default/files/standards/documents/DSP0236_1.3.0.pdf "https://dmtf.org/sites/default/files/standards/documents/DSP0236_1.3.0.pdf")
* <a id="dsp0239"></a>DMTF DSP0239, *MCTP IDs and Codes 1.6.0*, [https://www.dmtf.org/sites/default/files/standards/documents/DSP0239_1.6.0.pdf](https://www.dmtf.org/sites/default/files/standards/documents/DSP0239_1.6.0.pdf "https://www.dmtf.org/sites/default/files/standards/documents/DSP0239_1.6.0.pdf")
* <a id="dsp0240"></a>DMTF DSP0240, *Platform Level Data Model (PLDM) Base Specification*, [https://www.dmtf.org/sites/default/files/standards/documents/DSP0240_1.0.0.pdf](https://www.dmtf.org/sites/default/files/standards/documents/DSP0240_1.0.0.pdf "https://www.dmtf.org/sites/default/files/standards/documents/DSP0240_1.0.0.pdf")
* <a id="dsp0275"></a>DMTF DSP0275, *Security Protocol and Data Model (SPDM) over MCTP Binding Specification*, [https://www.dmtf.org/dsp/DSP0275](https://www.dmtf.org/dsp/DSP0275 "https://www.dmtf.org/dsp/DSP0275")
* <a id="dsp1001"></a>DMTF DSP1001, *Management Profile Usage Guide*, [https://www.dmtf.org/sites/default/files/standards/documents/DSP1001_1.2.0.pdf](https://www.dmtf.org/sites/default/files/standards/documents/DSP1001_1.2.0.pdf "https://www.dmtf.org/sites/default/files/standards/documents/DSP1001_1.2.0.pdf")
* <a id="ietf_dtlsv1_3"></a>IETF RFC 9147, [*The Datagram Transport Layer Security (DTLS) Protocol Version 1.3*](https://datatracker.ietf.org/doc/html/rfc9147 "https://datatracker.ietf.org/doc/html/rfc9147"), April 2022
* <a id="rfc2986"></a>IETF RFC 2986, [*PKCS #10: Certification Request Syntax Specification*](https://tools.ietf.org/html/rfc2986 "https://tools.ietf.org/html/rfc2986"), November 2000
* <a id="ietf-rfc4716"></a>IETF RFC 4716, [*The Secure Shell (SSH) Public Key File Format*](https://tools.ietf.org/html/rfc4716 "https://tools.ietf.org/html/rfc4716"), November 2006
* <a id="ref_IETF_RFC5234"></a>IETF RFC 5234, [*Augmented BNF for Syntax Specifications: ABNF*](https://tools.ietf.org/html/rfc5234 "https://tools.ietf.org/html/rfc5234"), January 2008
* <a id="ref_x509"></a>IETF RFC 5280, [*Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile*](https://tools.ietf.org/html/rfc5280 "https://tools.ietf.org/html/rfc5280"), May 2008
* <a id="ietf-rfc7250"></a>IETF RFC 7250, [*Using Raw Public Keys in Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)*](https://tools.ietf.org/html/rfc7250 "https://tools.ietf.org/html/rfc7250"), June 2014
* <a id="ref_IETF_RFC7919"></a>IETF RFC 7919, [*Negotiated Finite Field Diffie-Hellman Ephemeral Parameters for Transport Layer Security (TLS)*](https://tools.ietf.org/html/rfc7919 "https://tools.ietf.org/html/rfc7919"), August 2016
* <a id="rfc8017"></a>IETF RFC 8017, [*PKCS #1: RSA Cryptography Specifications Version 2.2*](https://tools.ietf.org/html/rfc8017), November, 2016
* <a id="rfc8032"></a>IETF RFC 8032, [*Edwards-Curve Digital Signature Algorithm (EdDSA)*](https://tools.ietf.org/html/rfc8032), January 2017
* <a id="ref_IETF_RFC8446"></a>IETF RFC 8446, [*The Transport Layer Security (TLS) Protocol Version 1.3*](https://tools.ietf.org/html/rfc8446 "https://tools.ietf.org/html/rfc8446"), August 2018
* <a id="USB-authentication"></a>[*USB Authentication Specification Rev 1.0 with ECN and Errata through January 7, 2019*](https://www.usb.org/document-library/usb-authentication-specification-rev-10-ecn-and-errata-through-january-7-2019 "https://www.usb.org/document-library/usb-authentication-specification-rev-10-ecn-and-errata-through-january-7-2019")
* <a id="TCG-algorithm-registry"></a>[*TCG Algorithm Registry, Family "2.0", Level 00 Revision 01.32*](https://trustedcomputinggroup.org/resource/tcg-algorithm-registry/ "https://trustedcomputinggroup.org/resource/tcg-algorithm-registry/"), June 25, 2020
* <a id="gcm"></a>NIST Special Publication 800-38D, [*Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC*](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf"), November 2007
* <a id="chachapoly"></a>IETF RFC 8439, [*ChaCha20 and Poly1305 for IETF Protocols*](https://tools.ietf.org/html/rfc8439 "https://tools.ietf.org/html/rfc8439"), June 2018
* <a id="rfc8998"></a>IETF RFC 8998, [*ShangMi (SM) Cipher Suites for TLS 1.3*](https://tools.ietf.org/html/rfc8998), March 2021
* <a id="ref_gbt32918_1_2016"></a>GB/T 32918.1-2016, *Information security technology—Public key cryptographic algorithm SM2 based on elliptic curves—Part 1: General*, August 2016
* <a id="ref_gbt32918_2_2016"></a>GB/T 32918.2-2016, *Information security technology—Public key cryptographic algorithm SM2 based on elliptic curves—Part 2: Digital signature algorithm*, August 2016
* <a id="ref_gbt32918_3_2016"></a>GB/T 32918.3-2016, *Information security technology—Public key cryptographic algorithm SM2 based on elliptic curves—Part 3: Key exchange protocol*, August 2016
* <a id="ref_gbt32918_4_2016"></a>GB/T 32918.4-2016, *Information security technology—Public key cryptographic algorithm SM2 based on elliptic curves—Part 4: Public key encryption algorithm*, August 2016
* <a id="ref_gbt32918_5_2016"></a>GB/T 32918.5-2016, *Information security technology—Public key cryptographic algorithm SM2 based on elliptic curves—Part 5: Parameter definition*, August 2016
* <a id="ref_gbt32905_2016"></a>GB/T 32905-2016, *Information security technology—SM3 cryptographic hash algorithm*, August 2016
* <a id="ref_gbt32907_2016"></a>GB/T 32907-2016, *Information security technology—SM4 block cipher algorithm*, August 2016
* <a id="ref_asn1"></a>**ASN.1 &mdash; ISO-822-1-4, DER &mdash; ISO-8825-1**
  * [ITU-T X.680, X.681, X.682, X.683, X.690](https://www.itu.int/rec/T-REC-X.680-X.693-201508-S/en "https://www.itu.int/rec/T-REC-X.680-X.693-201508-S/en"), 08/2015
* <a id="ascii"></a>**[ASCII &mdash; ISO/IEC 646:1991](https://www.iso.org/standard/4777.html "https://www.iso.org/standard/4777.html")**, 09/1991
* <a id="ref-ecdsa"></a>**ECDSA**
  * Section 6, The Elliptic Curve Digital Signature Algorithm (ECDSA) in [FIPS PUB 186-5 Digital Signature Standard (DSS)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf")
  * [NIST SP 800-186 Recommendations for Discrete Logarithm-based Cryptography: Elliptic Curve Domain Parameters](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-186.pdf")
  * IETF RFC 6979, [Deterministic Usage of the Digital Signature Algorithm (DSA) and Elliptic Curve Digital Signature Algorithm (ECDSA)](https://tools.ietf.org/html/rfc6979), August 2013
* <a id="ref-fips-sha2"></a>**SHA2-256**, **SHA2-384**, and **SHA2-512**
  * [FIPS PUB 180-4 Secure Hash Standard (SHS)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf")
* <a id="SHA3-256"></a><a id="SHA3-384"></a><a id="SHA3-512"></a>**SHA3-256**, **SHA3-384**, and **SHA3-512**
  * [FIPS PUB 202 SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf")

# Terms and definitions

In this document, some terms have a specific meaning beyond the normal English meaning.  This clause defines those terms.

The terms "shall" ("required"), "shall not", "should" ("recommended"), "should not" ("not recommended"), "may", "need not" ("not required"), "can" and "cannot" in this document are to be interpreted as described in [ISO/IEC Directives, Part 2](#iso-iec-directives), Clause 7.  The terms in parentheses are alternatives for the preceding term, for use in exceptional cases when the preceding term cannot be used for linguistic reasons.  Note that [ISO/IEC Directives, Part 2](#iso-iec-directives), Clause 7 specifies additional alternatives. Occurrences of such additional alternatives shall be interpreted in their normal English meaning.

The terms "clause", "subclause", "paragraph", and "annex" in this document are to be interpreted as described in [ISO/IEC Directives, Part 2](#iso-iec-directives), Clause 6.

The terms "normative" and "informative" in this document are to be interpreted as described in [ISO/IEC Directives, Part 2](#iso-iec-directives), Clause 3.  In this document, clauses, subclauses, and annexes labeled "(informative)" do not contain normative content. Notes and examples are always informative elements.

The terms that [DSP0004](#dsp0004), [DSP0223](#dsp0223), [DSP0236](#dsp0236), [DSP0239](#dsp0239), [DSP0275](#dsp0275), and [DSP1001](#dsp1001) define also apply to this document.

This specification uses these terms:

| Term | Definition |
|:-----|:-----------|
| <a id="alias-certificate"></a>alias certificate | Certificate that is dynamically generated by the [*component*](#component) or component firmware. |
| <a id="application-data-term"></a>application data | Data that is specific to the application and whose definition and format is outside the scope of this specification. Application data usually exists at the application layer, which is, in general, the layer above SPDM and the transport layer. Examples of data that could be application data include: messages carried as DMTF MCTP payloads; Internet traffic; PCIe transaction layer packets (TLPs); camera images and video (MIPI CSI-2 packets);  video display stream (MIPI DSI-2 packets); and touchscreen data (MIPI I3C Touch). |
| <a id="authentication-initiator"></a>authentication initiator | Endpoint that initiates the authentication process by challenging another endpoint. |
| <a id="authentication"></a>authentication | Process of determining whether an entity is who or what it claims to be. |
| <a id="byte"></a>byte | Eight-bit quantity.  Also known as an *octet*. |
| <a id="certificate-authority"></a>certificate authority (CA) | Trusted entity that issues certificates. |
| <a id="certificate-chain"></a>certificate chain | Typically a series of two or more certificates.  Each certificate is signed by the preceding certificate in the chain. |
| <a id="certificate"></a>certificate | Digital form of identification that provides information about an entity and certifies ownership of a particular asymmetric key-pair. |
| <a id="component"></a>component | Physical device, contained in a single package. A "component" may also refer to a functional block implemented in hardware, firmware, and/or software. |
| <a id="device-certificate"></a>device certificate | Certificate that contains information that identifies the component. Can be a leaf certificate or an [*intermediate certificate*](#intermediate-certificate). |
| <a id="device"></a>device | Physical entity such as a network controller or a fan. |
| <a id="distributed-management-task-force"></a>DMTF | Formerly known as the Distributed Management Task Force, the DMTF creates open manageability standards that span diverse emerging and traditional information technology (IT) infrastructures, including cloud, virtualization, network, servers, and storage.  Member companies and alliance partners worldwide collaborate on standards to improve the interoperable management of IT. |
| <a id="encap-req"></a>encapsulated request | A request embedded into an `ENCAPSULATED_REQUEST` or `ENCAPSULATED_RESPONSE_ACK` response message to allow the Responder to issue a request to a Requester. See [GET_ENCAPSULATED_REQUEST request and ENCAPSULATED_REQUEST response messages](#get_encapsulated_request-request-and-encapsulated_request-response-messages). |
| <a id="generic-cert"/>generic certificate | A certificate, for use in certificate slots 1 or greater, that has minimal SPDM requirements to allow for numerous use cases that the vendor, standards body, or user defines. |
| <a id="endpoint"></a>endpoint | Logical entity that communicates with other endpoints over one or more transport protocols. |
| <a id="event-notifier"></a> event notifier | An SPDM endpoint that is capable of sending asynchronous notifications using SPDM event mechanisms. See [Event mechanism](#event-mechanism). |
| <a id="event-recipient"></a> event recipient | An SPDM endpoint that is capable of receiving asynchronous notifications using SPDM event mechanisms. See [Event mechanism](#event-mechanism). |
| <a id="intermediate-certificate"></a>intermediate certificate | Certificate that is neither a root certificate nor a leaf certificate. |
| <a id="invasive-debug-mode"></a>invasive debug mode | A device mode that enables debug access that might expose or allow modification of firmware, hardware, or settings that can access (read or write) security keys, states, and contexts of the device. A device should not be trusted when it is operating in this mode. |
| <a id="large-spdm-message"></a>large SPDM message | An SPDM message that is greater than the `DataTransferSize` of the receiving SPDM endpoint or greater than the transmit buffer size of the sending SPDM endpoint. |
| <a id="large-spdm-request-message"></a>large SPDM request message | A large SPDM message that is an SPDM request. |
| <a id="large-spdm-response-message"></a>large SPDM response message | A large SPDM message that is an SPDM response. |
| <a id="leaf-certificate-term"></a>leaf certificate | Last certificate in a certificate chain. A leaf certificate is synonymous with an end entity certificate as [RFC 5280](#ref_x509) describes. |
| <a id="measurement"></a>measurement | Representation of hardware/firmware/software or configuration data on an endpoint. |
| <a id="message"></a>message | See [SPDM message](#spdm-message). |
| <a id="message-body"></a>message body | Portion of an SPDM message that carries additional data. |
| <a id="message-transcript"></a>message transcript | The concatenation of a sequence of messages in the order in which they are sent and received by an endpoint. The final message included in the message transcript may be truncated to allow inclusion of a signature in that message which is computed over the message transcript. If an endpoint is communicating with multiple peer endpoints concurrently, the message transcripts for the peers are accumulated separately and independently. |
| <a id="monotonically-increasing"></a>monotonically increasing | This specification uses the term *monotonically increasing* to describe an integer field where the value of each instance of the field in a series increases from a lower starting point to a higher ending point without repeating values. For instance, a *monotonically increasing* field may contain the values 1, 3, 4, 7, and 9. |
| <a id="msb"></a>most significant byte (MSB) | Highest-order [*byte*](#byte) in a number consisting of multiple bytes. |
| <a id="negotiated-state"></a>Negotiated State | Set of parameters that represents the state of the communication between a corresponding pair of Requester and Responder at the successful completion of the `NEGOTIATE_ALGORITHMS` messages.<br/><br/>These parameters may include values provided in `VERSION`, `CAPABILITIES`, and `ALGORITHMS` messages.<br/><br/>Additionally, they may include parameters associated with the transport layer.<br/><br/>They may include other values deemed necessary by the Requester or Responder to continue or preserve communication with each other. |
| <a id="nibble"></a>nibble | Computer term for a four-bit aggregation, or half of a byte. |
| <a id="non-invasive-debug-mode"></a>non-invasive debug mode | A device mode that enables debug access that does not expose or allow modification of security-critical firmware, hardware, or settings. |
| <a id="nonce"></a>nonce | Number that is unpredictable to entities other than its generator.  The probability of the same number occurring more than once is negligible. A nonce may be generated by combining a random number of at least 64 bits, optionally concatenated with a monotonically increasing counter of size suitable for the application. |
| <a id="opaque-data"></a>opaque data | Opaque data fields transfer data that is outside the scope of this specification. The semantics and usage of this data are implementation specific and are also outside the scope of this specification. |
| <a id="payload"></a>payload | Information-bearing fields of a message.  These fields are separate from the transport fields and elements, such as address fields, framing bits, and checksums, that transport the message from one point to another. |
| <a id="physical-transport-binding"></a>physical transport binding | Specifications that define how a base messaging protocol is implemented on a particular physical transport type and medium, such as SMBus/I<sup>2</sup>C or PCI Express™ Vendor Defined Messaging. |
| <a id="platform-management-component-intercommunication"></a>Platform Management Component Intercommunication (PMCI) | Working group under the DMTF that defines standardized communication protocols, low-level data models, and transport definitions that support communications with and between management controllers and management devices that form a platform management subsystem within a managed computer system. |
| <a id="record">record</a> | A unit or chunk of data that is either encrypted and/or authenticated. |
| <a id="requester"></a>Requester | Original transmitter, or source, of an SPDM request message.  It is also the ultimate receiver, or destination, of an SPDM response message. A Requester is the sender of the `GET_VERSION` request and remains the requester for the remainder of that connection.|
| <a id="reset"></a>Reset | This term is used to denote a Reset or restart of a device that runs the Requester or Responder code, which typically leads to the loss of all volatile state on the device. |
| <a id="responder"></a>Responder | Ultimate receiver, or destination, of an SPDM request message.  It is also the original transmitter, or source of an SPDM response message. |
| <a id="root-certificate"></a>root certificate | First certificate in a certificate chain, which acts as the trust anchor and is typically self-signed. |
| <a id="secure-session"></a>secure session | Provides either encryption or message authentication or both for communicating data over a transport. |
| <a id="security-protocols-and-data-models"></a>Security Protocols and Data Models (SPDM) WG| Working group under the DMTF that defines standards to enable security for platforms, whether for the control plane, data plane, or other infrastructure. |
| <a id="sequentially-decreasing"></a>sequentially decreasing | This specification uses the term *sequentially decreasing* to describe an integer field where the value of each instance of the field in a series decrements from a higher starting point to a lower ending point without skipping or repeating values. For instance, a *sequentially decreasing* field may contain the values 255, 254, 253, 252, and 251. |
| <a id="sequentially-increasing"></a>sequentially increasing | This specification uses the term *sequentially increasing* to describe an integer field where the value of each instance of the field in a series increments from a lower starting point to a higher ending point without skipping or repeating values. For instance, a *sequentially increasing* field may contain the values 1, 2, 3, 4, and 5. |
| <a id="session-keys"></a>session keys | Any secrets, derived cryptographic keys, or any cryptographic information bound to a session. |
| <a id="sse"></a>Session-Secrets-Exchange | Any SPDM request and their corresponding response that initiates a session and provides initial cryptographic exchange. Examples of such requests are `KEY_EXCHANGE` and `PSK_EXCHANGE`. |
| <a id="ssf"></a>Session-Secrets-Finish | This term denotes any SPDM request and its corresponding response that finalizes a session setup and provides the final exchange of cryptographic or other information before application data can be securely transmitted. Examples of such requests are `FINISH` and `PSK_FINISH`. |
| <a id="spdm-message-payload"></a>SPDM message payload | Portion of the message body of an SPDM message.  This portion of the message is separate from those fields and elements that identify the SPDM version, the SPDM request and response codes, and the two parameters. |
| <a id="spdm-message"></a>SPDM message | Unit of communication in SPDM communications. See [Generic SPDM message format](#generic-spdm-message-format). |
| <a id="spdm-request-message"></a>SPDM request message | Message that is sent to an endpoint to request a specific SPDM operation.  A corresponding SPDM response message acknowledges receipt of an SPDM request message. |
| <a id="spdm-response-message"></a>SPDM response message | Message that is sent in response to a specific SPDM request message.  This message includes a `Response Code` field that indicates whether the request completed normally. |
| <a id="trusted-computing-base"></a>trusted computing base (TCB) | Set of all hardware, firmware, and/or software components that are critical to its security, in the sense that bugs or vulnerabilities occurring inside the TCB might jeopardize the security properties of the entire system.  By contrast, parts of a computer system outside the TCB shall not be able to misbehave in a way that would leak any more privileges than are granted to them in accordance with the security policy.<br/><br/>Reference: [https://en.wikipedia.org/wiki/Trusted_computing_base](https://en.wikipedia.org/wiki/Trusted_computing_base "https://en.wikipedia.org/wiki/Trusted_computing_base") |
| <a id="trusted environment"></a>trusted environment | An environment where the operator is assured of no unauthorized interference in operations. |

# Symbols and abbreviated terms

The abbreviations that [DSP0004](#dsp0004), [DSP0223](#dsp0223), and [DSP1001](#dsp1001) define apply to this document.

The following additional abbreviations are used in this document.

| Abbreviation | Definition |
|:-------------|:-----------|
| <a id="aead"></a>AEAD | Authenticated Encryption with Associated Data       |
| <a id="ca"></a>CA     | [*certificate authority*](#certificate-authority)   |
| <a id="dmtf"></a>DMTF | Formerly the *Distributed Management Task Force*    |
| <a id="ecc"></a>ECC   | Elliptic-curve cryptography                         |
| <a id="ecc"></a>ECDSA | Elliptic-curve Digital Signature Algorithm          |
| <a id="kdf"></a>KDF   | Key Derivation Function                             |
| <a id="mac"></a>MAC   | Message Authentication Code                         |
| <a id="msb"></a>MSB   | [*most significant byte*](#msb)                     |
| <a id="oid"></a>OID   | Object identifier                                   |
| <a id="pmci"></a>PMCI | [*Platform Management Component Intercommunication*](#platform-management-component-intercommunication)                           |
| <a id="rma"></a>RMA   | Return Merchandise Authorization                    |
| <a id="rsa"></a>RSA   | Rivest–Shamir–Adleman                               |
| <a id="spdm"></a>SPDM | Security Protocol and Data Model                    |
| <a id="tcb"></a>TCB   | [*trusted computing base*](#trusted-computing-base) |
| <a id="vca"></a>VCA   | Version-Capabilities-Algorithms                     |

# SPDM message exchanges

The message exchanges that this specification defines are between two endpoints and are performed and exchanged through sending and receiving of [*SPDM*](#spdm) messages that [*SPDM messages*](#spdm-messages) defines.  The SPDM message exchanges are defined in a generic fashion that allows the messages to be communicated across different physical mediums and over different transport protocols.

The specification-defined message exchanges enable Requesters to:

* Discover and negotiate the security capabilities of a Responder.
* Authenticate or provision an identity of a Responder.
* Retrieve the measurements of a Responder.
* Securely establish cryptographic [*session keys*](#session-keys) to construct a secure communication channel for the transmission or reception of [*application data*](#application-data-term).
* Receive notifications of selectable events when certain scenarios transpire.

These message exchange capabilities are built on top of well-known and established security practices across the computing industry.  The following clauses provide a brief overview of each message exchange capability.  Some message exchange capabilities are based on the security model that the [*USB Authentication Specification Rev 1.0 with ECN and Errata through January 7, 2019*](#USB-authentication) defines.

## Security capability discovery and negotiation

This specification defines a mechanism for a Requester to discover the security capabilities of a Responder.  For example, an endpoint could support multiple cryptographic hash functions that this specification defines.  Furthermore, the specification defines a mechanism for a Requester and Responder to select a common set of cryptographic algorithms to use for all subsequent message exchanges before another negotiation is initiated by the Requester, if an overlapping set of cryptographic algorithms exists that both endpoints support.

## Identity authentication

In this specification, the authenticity of a Responder is determined by digital signatures using well-established techniques based on public key cryptography.  A Responder proves its identity by generating digital signatures using a private key, and the signatures can be cryptographically verified by the Requester using the public key associated with that private key.

At a high level, the authentication of the identity of a Responder involves these processes:

* [Identity provisioning](#identity-provisioning)
* [Runtime authentication](#runtime-authentication)

### Identity provisioning

Identity provisioning is the process that device vendors follow during or after hardware manufacturing to equip a device with a secure identifier. In the context of this specification, this secure identifier consists of an asymmetric key pair and, [optionally](#raw-public-keys), a certificate to bind the key pair to a particular instance of a device and associate it with additional metadata. The specifics of key generation and provisioning are outside the scope of this specification. However, as the security of the SPDM protocol depends on device identities that cannot be easily modified, removed, or copied, it is strongly recommended that identity keys are unique per device and generated using cryptographically strong random seeds.

#### Certificate models

If trust in a device public key is established through a certificate, the certificate is typically part of a [*certificate chain*](#certificate-chain). The certificate chain has a [*root certificate*](#root-certificate) (`RootCert`) as its root and a [*leaf certificate*](#leaf-certificate-term) as the last certificate in it. The `RootCert` is generated by a trusted root [*certificate authority (CA)*](#certificate-authority) and certifies the certificate containing the device public key either directly or indirectly through a number of intermediate CAs. [*Authentication initiators*](#authentication-initiator) use the `RootCert` to verify the validity of device certificate chains.

The certificate chain should contain at least one certificate that includes hardware identity information, regardless of the certificate model that is in use. The [Hardware identity OID](#hardware-identity-oid) should be used to indicate which certificate conveys the hardware identity. Though existing deployments might not include the [Hardware identity OID](#hardware-identity-oid) in a certificate, it is strongly recommended that new deployments include this information. The public/private key pair associated with a hardware identity certificate is constant on the instance of the device, regardless of the version of firmware running on the device.

SPDM defines multiple overarching formats for certificate chains, referred to as certificate chain models. While the details of each certificate chain model vary, all of them follow the general format of connecting from a [*root certificate*](#root-certificate) (`RootCert`) to a [*leaf certificate*](#leaf-certificate-term), possibly through one or more [*intermediate certificates*](#intermediate-certificate).

A Responder can use one or more of the certificate chain models. A Requester should be capable of performing [Runtime authentication](#runtime-authentication) on a certificate chain that conforms to any of the models.

[Figure 1 &mdash; SPDM certificate chain models](#figure-spdm-certificate-chain-models) shows the SPDM certificate chain models:

<a id="figure-spdm-certificate-chain-models"></a>**Figure 1 &mdash; SPDM certificate chain models**

<!--markdownlint-disable MD033 -->
<img src="SPDMSpecification_files/Figure-CertificateChainModels.svg" title="Figure 1 &mdash; SPDM certificate chain models" alt="Figure 1 &mdash; SPDM certificate chain models" width="500" height="600">
<!--markdownlint-enable MD033 -->

##### Device certificate model

When the device certificate (`DeviceCert`) model is in use, the leaf certificate is a Device Certificate, which contains the public key that corresponds to the device private key. Through the certificate chain, the root CA indirectly endorses the device public key in the Device Certificate. In this model, the Device Certificate should contain the [Hardware identity OID](#hardware-identity-oid).

##### Alias certificate model

When the alias certificate (`AliasCert`) model is in use, the leaf certificate is an Alias Certificate, in which case there may be one or more intermediate `AliasCert` certificates between the Device Certificate and the leaf Alias Certificate. In the `AliasCert` model, the device private key signs the next level Alias Certificate, and then the private key associated with the public key in each Alias Intermediate CA signs the Alias Certificate below it. When the `AliasCert` model is in use, the Device Certificate is referred to as a Device Certificate CA, indicating that the certificate both contains device hardware identity information and functions as a certificate authority to sign an additional certificate. In this model, the Device Certificate CA should contain the [Hardware identity OID](#hardware-identity-oid).

A device that implements the `AliasCert` model might factor some mutable information, such as the measurement of a firmware image, into the derivation of the public/private key pairs for the intermediate and leaf alias certificates. Therefore, the asymmetric public/private key pairs for each Alias Certificate should be treated as mutable.

Through the certificate chain, the root CA indirectly endorses the device public key in the Device Certificate. When the `AliasCert` model is in use, the Alias Certificates are endorsed by the device private key, meaning that the Alias Certificates are also indirectly endorsed by the root CA.

When the `AliasCert` model is used, the device creates and endorses one or more certificates. The certificates from the root certificate to the Device Certificate are considered immutable because the Responder cannot change them, as they can only be changed through the `SET_CERTIFICATE` command or an equivalent capability. The certificates below the Device Certificate can be created on the device and are mutable certificates in that they can change when the device state changes, such as a device [*reset*](#reset). The [Mutable certificate OID](#mutable-certificate-oid) should be used to indicate mutable certificates.

In addition, when the `AliasCert` model is used, one or more Alias Certificates can contain firmware identity information. Other standards bodies might define the format of the firmware identity information. Such definitions are outside the scope of this specification.

Note that a signature algorithm used with a mutable alias certificate can insert random data during signing, which would cause the digest of the certificate chain to change each time it is regenerated. An implementer can use a mechanism that is outside the scope of this specification to ensure that such a signature does not change between instances of `DIGESTS` and `CERTIFICATE` responses.

##### Generic certificate model

With the support of [multiple asymmetric keys](#multiple-asymmetric-key-support), the need for another certificate model arises to accommodate varying use cases that `DeviceCert` and `AliasCert` models cannot fulfill. Thus, the generic certificate model offers the greatest flexibility to the device manufacturer, a manufacturer in the supply chain, and the users of the SPDM endpoint.

As [Figure 1 &mdash; SPDM certificate chain models](#figure-spdm-certificate-chain-models) illustrates, much like the other certificate models, the generic certificate model, too, is composed of a chain of certificates starting with the root and ending with the leaf. The root CA, too, either directly certifies the leaf certificate or indirectly certifies the leaf certificate (`GenericCert`) through one or more intermediate certificate authorities.  In other words, this model is the most flexible (or least restrictive) of the certificate models in this specification. The main difference between this model and the other models is that SPDM shall not impose any requirements on the contents of each certificate in the chain in a generic certificate model other than the key pair and related information associated in the leaf certificate.

For example, in a device certificate model, the leaf certificate can contain elements that specifically identify the device and device manufacturer, whereas the generic certificate model has no such requirement nor any concept of a device certificate.

As such, the generic certificate model applies to certificates in slots greater than slot 0. A model in a certificate slot in this specification is either a `DeviceCert`, `AliasCert`, or `GenericCert` model.

The contents and use cases for the certificates of a generic certificate model, other than the associated key pair and related information in the leaf certificate, are outside the scope of this specification. Typically, the users of the SPDM endpoint, the device manufacturer, or standards define the contents and use cases of a generic certificate model.

### Raw public keys

Instead of using certificate chains, the vendor can provision the raw public key of the Responder to the Requester in a trusted environment; for example, during the secure manufacturing process. In this case, trust of the public key of the Responder is established without the need for a certificate-based public key infrastructure.

The format of the provisioned public key is outside the scope of this specification. Vendors can use proprietary formats or public key formats that other standards define, such as [RFC 7250](#ietf-rfc7250) and [RFC 4716](#ietf-rfc4716).

### Runtime authentication

Runtime authentication is the process by which an authentication initiator, or Requester, interacts with a Responder in a running system.  The authentication initiator can retrieve the certificate chains from the Responder and send a unique challenge to the Responder.  The Responder uses the private key associated with the leaf certificate to sign the challenge.  The authentication initiator verifies the signature by using the public key associated with the leaf certificate of the Responder and any intermediate public keys within the certificate chain by using the root certificate as the trusted anchor.

If the public key of the Responder was provisioned to the Requester in a trusted environment, the authentication initiator sends a unique challenge to the Responder. The Responder signs the challenge with the private key. The authentication initiator verifies the signature by using the public key of the Responder. Device identification can be handled using the [GET_ENDPOINT_INFO request and ENDPOINT_INFO response messages](#get_endpoint_info-request-and-endpoint_info-response-messages) or the transport layer (which is outside the scope of this specification).

## Firmware and configuration measurement

A measurement is a representation of firmware/software or configuration data on an endpoint. A measurement is typically either a cryptographic hash value of the data or the raw data itself.  The endpoint optionally binds a measurement with the endpoint identity through the use of digital signatures. This binding enables an authentication initiator to establish the identity and measurement of the firmware/software or configuration running on the endpoint.

## Secure sessions

Many devices exchange data that might require protection with other devices. In this specification, this data that is being exchanged is generically referred to as application data. The protocol of the application data usually exists at a higher layer, and as such it is outside the scope of this specification.  The protocol of the application data usually allows for encrypted and/or authenticated data transfer.

This specification provides a method to perform a cryptographic key exchange such that the protocol of the application data can use the exchanged keys to provide a secure channel of communication by using encryption and message authentication.  This cryptographic key exchange provides either Responder-only authentication or mutual authentication, both of which can be considered equivalent to [Runtime authentication](#runtime-authentication).  For more details, see the [Session](#session) clause.

Finally, many SPDM requests and their corresponding responses can also be afforded the same protection. For more details, see [Table 6 &mdash; SPDM request and response messages validity](#table-spdm-request-and-response-messages-validity) and the [SPDM request and response code issuance allowance](#spdm-request-and-response-code-issuance-allowance) clause.

[Figure 2 &mdash; SPDM messaging protocol flow](#figure-spdm-messaging-protocol-flow) gives a very high-level view of when the [*secure session*](#secure-session) starts.

## Mutual authentication overview

The ability of a Responder to verify the authenticity of the Requester is called mutual authentication. Several mechanisms in this specification are detailed to provide mutual authentication capabilities. The cryptographic means to verify the identity of the Requester is the same as verifying the identity of the Responder. The [Identity provisioning](#identity-provisioning) clause discusses identity in regards to the Responder but the details also apply to the Requester.

In general, when this specification states requirements or recommendations for Responders in the context of identity, those same rules also apply to Requesters in the context of mutual authentication. The various clauses in this specification provide more details.

## Multiple asymmetric key support

An SPDM endpoint can use more than one asymmetric key pair for a negotiated asymmetric algorithm. This enables cryptographic isolation between different use cases which potentially increases the security posture of the SPDM endpoint and its corresponding SPDM connections. For example, an SPDM Responder can choose which key-pairs to use in a `CHALLENGE` request and which key pairs to use in a `GET_MEASUREMENTS` request. The SPDM Responder permits the `CHALLENGE` and `GET_MEASUREMENTS` requests to use the same key-pair for signing operations.

Additionally, a Responder can allow the Requester to select the use cases to associate with each asymmetric key pair. The Responder can, also, allow the Requester to request the generation of a new key pair.

To facilitate the use of multiple asymmetric keys, the ability to uniquely identify each key pair is essential. To achieve this, a unique key pair number, called `KeyPairID`, identifies each asymmetric key pair. Additionally, one or more leaf certificates can bind to the same asymmetric key pair.

## Custom environments

A fixed or predetermined environment is an environment where certain characteristics of the environment are fixed or known before the SPDM endpoints communicate with each other. In many cases, these characteristics are determined even before the environment can operate such as during the design phase. An example of a such an environment is when two specific endpoints can only communicate with each other. These environments may forfeit certain SPDM features such as interoperability. However, the security posture and guarantees of these environments are outside the scope of this specification.

## Notification overview

To aid an SPDM endpoint in enforcing its security policy requirements in an efficient, reliable, and timely manner, the [SPDM event mechanism](#event-mechanism) provides a method to asynchronously deliver a notification to or receive a notification from the interested SPDM endpoint. This mechanism allows an interested SPDM endpoint to choose only the event types it wants to receive. For more details, see [Event mechanism](#event-mechanism).

# SPDM messaging protocol

The SPDM messaging protocol defines a request-response messaging model between two endpoints to perform the message exchanges outlined in [SPDM message exchanges](#spdm-message-exchanges).  Each [*SPDM request message*](#spdm-request-message) shall be responded to with an SPDM response message as this specification defines unless this specification states otherwise.

[Figure 2 &mdash; SPDM messaging protocol flow](#figure-spdm-messaging-protocol-flow)  is an example of a high-level request-response flow diagram for SPDM. An endpoint that acts as the [*Requester*](#requester) sends an SPDM request message to another endpoint that acts as the [*Responder*](#responder), and the Responder returns an SPDM response message to the Requester.

<a id="figure-spdm-messaging-protocol-flow"></a>**Figure 2 &mdash; SPDM messaging protocol flow**

<!--markdownlint-disable MD033 -->
<img src="SPDMSpecification_files/spdm-message-protocol-flow-example.svg" title="Figure 2 &mdash; SPDM messaging protocol flow" alt="Figure 2 &mdash; SPDM messaging protocol flow" width="500" height="600">
<!--markdownlint-enable MD033 -->

All SPDM request-response messages share a common data format that consists of a four-[*byte*](#byte) message header and zero or more bytes message [*payload*](#payload) that is message-dependent.  The following clauses describe the common message format and [SPDM messages'](#spdm-messages) details for each of the request and response messages.

The Requester shall issue `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS` request messages before issuing any other request messages.  The responses to `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS` can be saved by the Requester so that after Reset the Requester can skip these requests.

## SPDM connection model

In SPDM, communication between a pair of SPDM endpoints starts when one endpoint sends a `GET_VERSION` request to another SPDM endpoint. The SPDM endpoint that starts the communication is called the Requester. The endpoint receiving the `GET_VERSION` and providing the `VERSION` response is called a Responder. The communication between a pair of Requester and Responder is called a connection. One or more connections can exist between a Requester and Responder. Different connections might exist over the same transport or over different transports. When there are multiple connections over the same transport, the transport is responsible for providing mechanisms for SPDM endpoints to distinguish between one or more connections. When the transport does not provide such a mechanism, there shall be one connection between the Requester and Responder over that connection.

SPDM endpoints can be both a Requester and Responder. As a Requester, an SPDM endpoint can communicate with one or more Responders. Likewise, as a Responder, an SPDM endpoint can respond to multiple Requesters. The SPDM connection model considers each of these communications to be a separate connection. For example, a pair of SPDM endpoints can be both Requester and Responder to each other. Thus, the SPDM connection model considers this to be two separate connections.

Within a connection, the Requester remains the Requester for the remainder of the connection. Likewise, the Responder remains the Responder for the remainder of the connection. However, under certain scenarios allowed by SPDM, a Responder can send a request to a Requester and, likewise, a Requester might provide a response to a Responder. These cases are limited and this specification explicitly defines these cases. In such scenarios, when a Requester provides a response, the Requester shall abide by all requirements in this specification as if they are a Responder for that request. Similarly, when a Responder sends a request, the Responder shall abide by all requirements in this specification as if they are a Requester for that request.

Within a connection, the Requester can establish one or more secure sessions. These secure sessions are considered to be part of the same connection. Secure sessions can terminate and additional sessions can be established at any time. A `GET_VERSION` can reset the connection and all context associated with that connection including, but not limited to, information such as session keys and session IDs. However, this is not considered a termination of the connection. A connection can terminate due to external events such as a device reset or an error-handling strategy implemented on an SPDM endpoint, but such scenarios are outside the scope of this specification. Connections can be terminated using mechanisms outside the scope of this specification.

## SPDM bits-to-bytes mapping

All SPDM fields, regardless of size or endianness, map the highest numeric bits to the highest numerically assigned byte in sequentially decreasing order down to and including the least numerically assigned byte of that field. The following two figures illustrate this mapping.

[Figure 3 &mdash; One-byte field bit map](#figure-one-byte-bit-map) shows the one-byte field bit map:

<a id="figure-one-byte-bit-map"></a>**Figure 3 &mdash; One-byte field bit map**

![Figure 3 &mdash; One-byte field bit map](SPDMSpecification_files/single-byte-bit-map.svg)

[Figure 4 &mdash; Two-byte field bit map](#figure-multi-byte-bit-map) shows the two-byte field bit map:

<a id="figure-multi-byte-bit-map"></a>**Figure 4 &mdash; Two-byte field bit map**

![Figure 4 &mdash; Two-byte field bit map](SPDMSpecification_files/multi-byte-bit-map.svg)

## Generic SPDM message format

[Table 3 &mdash; Generic SPDM message field definitions](#table-generic-spdm-message-field-definitions) defines the fields that constitute a generic SPDM message, including the message header and payload:

<a id="table-generic-spdm-message-field-definitions"></a>**Table 3 &mdash; Generic SPDM message field definitions**

| Byte offset | Bit offset | Size (bits) | Field                 | Description          |
|:------------|:-----------|:------------|:----------------------|:---------------------|
| 0      | [7:4] | 4            | SPDM Major Version    | Shall be the major version of the SPDM Specification.  An endpoint shall not communicate by using an incompatible SPDM version value.  See [Version encoding](#version-encoding). |
| 0      | [3:0] | 4            | SPDM Minor Version    | Shall be the minor version of the SPDM Specification.  A specification with a given minor version extends a specification with a lower minor version as long as they share the major version.  See [Version encoding](#version-encoding). |
| 1      | [7:0] | 8            | Request Response Code | Shall be the request message code or response code, which [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes) and [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes) enumerate. `0x00` through `0x7F` represent response codes and `0x80` through `0xFF` represent request codes. In request messages, this field is considered the request code. In response messages, this field is considered the response code. |
| 2      | [7:0] | 8            | Param1                | Shall be the first one-byte parameter.  The contents of the parameter are specific to the `Request Response Code`. |
| 3      | [7:0] | 8            | Param2                | Shall be the second one-byte parameter.  The contents of the parameter are specific to the `Request Response Code`. |
| 4      | See the description. | Variable              | [*SPDM message payload*](#spdm-message-payload) | Shall be zero or more bytes that are specific to the `Request Response Code`. |

### SPDM version

The `SPDMVersion` field, present as the first field in all SPDM messages, indicates the version of the SPDM specification that the format of an SPDM message adheres to. The format of this field shall be the same as byte 0 in [Table 3 &mdash; Generic SPDM message field definitions](#table-generic-spdm-message-field-definitions). The value of this field shall be the same value as the version of this specification except for `GET_VERSION` and `VERSION` messages.

For example, if the version of this specification is 1.2, the value of `SPDMVersion` is `0x12`, which also corresponds to an `SPDM Major Version` of 1 and an `SPDM Minor Version` of 2. See [Version encoding](#version-encoding) for more examples.

The version of this specification can be found on the title page and in the footer of the other pages in this document.

The `SPDMVersion` for the version of this specification shall be `0x13`.

The `SPDMversionString` shall be a string formed by concatenating the major version, a period ("."), and the minor version. For example, if the version of this specification is 1.2.3, then `SPDMversionString` is `"1.2"`.

## SPDM request codes

[Table 4 &mdash; SPDM request codes](#table-spdm-request-codes) defines the SPDM request codes. The **Implementation requirement** column indicates requirements on the Requester.

All SPDM-compatible implementations shall use [SPDM request codes](#table-spdm-request-codes).

If an `ERROR` response is sent for unsupported request codes, the `ErrorCode` shall be `UnsupportedRequest`.

<a id="table-spdm-request-codes"></a>**Table 4 &mdash; SPDM request codes**

| Request                       | Code value | Implementation requirement | Message format |
|:------------------------------|:-----------|:---------------------------|:-----------    |
| GET_DIGESTS                   | 0x81       | Optional                   | [Table 34 &mdash; GET_DIGESTS request message format](#table-get-digests-request-message-format) |
| GET_CERTIFICATE               | 0x82       | Optional                   | [Table 38 &mdash; GET_CERTIFICATE request message format](#table-get-certificate-request-message-format) |
| CHALLENGE                     | 0x83       | Optional                   | [Table 44 &mdash; CHALLENGE request message format](#table-challenge-request-message-format) |
| GET_VERSION                   | 0x84       | Required                   | [Table 8 &mdash; GET_VERSION request message format](#table-get-version-request-message-format) |
| CHUNK_SEND                    | 0x85       | Optional                   | [Table 96 &mdash; CHUNK_SEND request format](#table-chunk-send-request-format-table) |
| CHUNK_GET                     | 0x86       | Optional                   | [Table 100 &mdash; CHUNK_GET request format](#table-chunk-get-request-format) |
| GET_ENDPOINT_INFO             | 0x87       | Optional                   | [Table 119 &mdash; GET_ENDPOINT_INFO request format](#table-get-endpoint-info-message-format) |
| GET_MEASUREMENTS              | 0xE0       | Optional                   | [Table 49 &mdash; GET_MEASUREMENTS request message format](#table-get-measurements-request-message-format) |
| GET_CAPABILITIES              | 0xE1       | Required                   | [Table 11 &mdash; GET_CAPABILITIES request message format](#table-get-capabilities-request-message-format) |
| GET_SUPPORTED_EVENT_TYPES     | 0xE2       | Optional                   | [Table 109 &mdash; GET_SUPPORTED_EVENT_TYPES request message format](#table-event-3) |
| NEGOTIATE_ALGORITHMS          | 0xE3       | Required                   | [Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format](#table-negotiate-algorithms-request-message-format) |
| KEY_EXCHANGE                  | 0xE4       | Optional                   | [Table 69 &mdash; KEY_EXCHANGE request message format](#table-key-exchange-request-message-format) |
| FINISH                        | 0xE5       | Optional                   | [Table 72 &mdash; FINISH request message format](#table-finish-request-message-format) |
| PSK_EXCHANGE                  | 0xE6       | Optional                   | [Table 74 &mdash; PSK_EXCHANGE request message format](#table-psk-exchange-request-message-format) |
| PSK_FINISH                    | 0xE7       | Optional                   | [Table 76 &mdash; PSK_FINISH request message format](#table-psk-finish-request-message-format) |
| HEARTBEAT                     | 0xE8       | Optional                   | [Table 78 &mdash; HEARTBEAT request message format](#table-heartbeat-request-message-format) |
| KEY_UPDATE                    | 0xE9       | Optional                   | [Table 80 &mdash; KEY_UPDATE request message format](#table-key-update-request-message-format) |
| GET_ENCAPSULATED_REQUEST      | 0xEA       | Optional                   | [Table 83 &mdash; GET_ENCAPSULATED_REQUEST request message format](#table-get-encapsulated-request-request-message-format) |
| DELIVER_ENCAPSULATED_RESPONSE | 0xEB       | Optional                   | [Table 85 &mdash; DELIVER_ENCAPSULATED_RESPONSE request message format](#table-deliver-encapsulated-response-request-message-format) |
| END_SESSION                   | 0xEC       | Optional                   | [Table 87 &mdash; END_SESSION request message format](#table-end-session-request-message-format) |
| GET_CSR                       | 0xED       | Optional                   | [Table 90 &mdash; GET_CSR request message format](#table-get-csr-request-message-format) |
| SET_CERTIFICATE               | 0xEE       | Optional                   | [Table 93 &mdash; SET_CERTIFICATE request message format](#table-set-certificate-request-message-format) |
| GET_MEASUREMENT_EXTENSION_LOG | 0xEF       | Optional                   | [Table 126 &mdash; GET_MEASUREMENT_EXTENSION_LOG message format](#table-get-measurement-extension-log-message-format) |
| SUBSCRIBE_EVENT_TYPES         | 0xF0       | Optional                   | [Table 113 &mdash; SUBSCRIBE_EVENT_TYPES request message format](#table-event-5) |
| SEND_EVENT                    | 0xF1       | Optional                   | [Table 116 &mdash; SEND_EVENT request message format](#table-event-7) |
| GET_KEY_PAIR_INFO             | 0xFC       | Optional                   | [Table 102 &mdash; GET_KEY_PAIR_INFO request message format](#table-gkpi) |
| SET_KEY_PAIR_INFO             | 0xFD       | Optional                   | [Table 106 &mdash; SET_KEY_PAIR_INFO request message format](#table-skpi) |
| VENDOR_DEFINED_REQUEST        | 0xFE       | Optional                   | [Table 57 &mdash; VENDOR_DEFINED_REQUEST request message format](#table-vendor-defined-request-request-message-format) |
| RESPOND_IF_READY              | 0xFF       | Required                   | [Table 56 &mdash; RESPOND_IF_READY request message format](#table-respond-if-ready-request-message-format) |
| Reserved                      | All other values  |                     | SPDM implementations compatible with this version shall not use the reserved request codes. |

## SPDM response codes

The `Request Response Code` field in the SPDM response message shall specify the appropriate response code for a request.  All SPDM-compatible implementations shall use [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).

On a successful completion of an SPDM operation, the specified response message shall be returned.  Upon an unsuccessful completion of an SPDM operation, the `ERROR` response message should be returned.

[Table 5 &mdash; SPDM response codes](#table-spdm-response-codes) defines the response codes for SPDM.  The **Implementation requirement** column indicates requirements on the Responder.

<a id="table-spdm-response-codes"></a>**Table 5 &mdash; SPDM response codes**

| Response                  | Value  | Implementation requirement | Message format |
|:--------------------------|:-------|:---------------------------|:-------        |
| DIGESTS                   | 0x01   | Optional                   | [Table 35 &mdash; Successful DIGESTS response message format](#table-successful-digests-response-message-format) |
| CERTIFICATE               | 0x02   | Optional                   | [Table 40 &mdash; Successful CERTIFICATE response message format](#table-successful-certificate-response-message-format) |
| CHALLENGE_AUTH            | 0x03   | Optional                   | [Table 45 &mdash; Successful CHALLENGE_AUTH response message format](#table-successful-challenge-auth-response-message-format) |
| VERSION                   | 0x04   | Required                   | [Table 9 &mdash; Successful VERSION response message format](#table-successful-version-response-message-format) |
| CHUNK_SEND_ACK            | 0x05   | Optional                   | [Table 98 &mdash; CHUNK_SEND_ACK response message format](#table-chunk-send-ack-response-message-format) |
| CHUNK_RESPONSE            | 0x06   | Optional                   | [Table 101 &mdash; CHUNK_RESPONSE response format](#table-chunk-response-response-format) |
| ENDPOINT_INFO             | 0x07   | Optional                   | [Table 122 &mdash; ENDPOINT_INFO response format](#table-endpoint-info-response-message-format) |
| MEASUREMENTS              | 0x60   | Optional                   | [Table 52 &mdash; Successful MEASUREMENTS response message format](#table-successful-get-measurements-response-message-format) |
| CAPABILITIES              | 0x61   | Required                   | [Table 12 &mdash; Successful CAPABILITIES response message format](#table-successful-capabilities-response-message-format) |
| SUPPORTED_EVENT_TYPES     | 0x62   | Optional                   | [Table 110 &mdash; SUPPORTED_EVENT_TYPES response message format](#table-event-4) |
| ALGORITHMS                | 0x63   | Required                   | [Table 21 &mdash; Successful ALGORITHMS response message format](#table-successful-algorithms-response-message-format) |
| KEY_EXCHANGE_RSP          | 0x64   | Optional                   | [Table 71 &mdash; Successful KEY_EXCHANGE_RSP response message format](#table-successful-key-exchange-rsp-response-message-format) |
| FINISH_RSP                | 0x65   | Optional                   | [Table 73 &mdash; Successful FINISH_RSP response message format](#table-successful-finish-rsp-response-message-format) |
| PSK_EXCHANGE_RSP          | 0x66   | Optional                   | [Table 75 &mdash; PSK_EXCHANGE_RSP response message format](#table-psk-exchange-rsp-response-message-format) |
| PSK_FINISH_RSP            | 0x67   | Optional                   | [Table 77 &mdash; Successful PSK_FINISH_RSP response message format](#table-successful-psk-finish-rsp-response-message-format) |
| HEARTBEAT_ACK             | 0x68   | Optional                   | [Table 79 &mdash; HEARTBEAT_ACK response message format](#table-heartbeat-ack-response-message-format) |
| KEY_UPDATE_ACK            | 0x69   | Optional                   | [Table 81 &mdash; KEY_UPDATE_ACK response message format](#table-key-update-ack-response-message-format) |
| ENCAPSULATED_REQUEST      | 0x6A   | Optional                   | [Table 84 &mdash; ENCAPSULATED_REQUEST response message format](#table-encapsulated-request-response-message-format) |
| ENCAPSULATED_RESPONSE_ACK | 0x6B   | Optional                   | [Table 86 &mdash; ENCAPSULATED_RESPONSE_ACK response message format](#table-encapsulated-response-ack-response-message-format) |
| END_SESSION_ACK           | 0x6C   | Optional                   | [Table 89 &mdash; END_SESSION_ACK response message format](#table-end-session-ack-response-message-format) |
| CSR                       | 0x6D   | Optional                   | [Table 92 &mdash; CSR response message format](#table-csr-response-message-format) |
| SET_CERTIFICATE_RSP       | 0x6E   | Optional                   | [Table 95 &mdash; Successful SET_CERTIFICATE_RSP response message format](#table-set-certificate-rsp-response-message-format) |
| MEASUREMENT_EXTENSION_LOG | 0x6F   | Optional                   | [Table 127 &mdash; Successful MEASUREMENT_EXTENSION_LOG message format](#table-measurement-extension-log-message-format) |
| SUBSCRIBE_EVENT_TYPES_ACK | 0x70   | Optional                   | [Table 114 &mdash; SUBSCRIBE_EVENT_TYPES_ACK response message format](#table-event-6)|
| EVENT_ACK                 | 0x71   | Optional                   | [Table 118 &mdash; EVENT_ACK response message format](#table-event-1)|
| KEY_PAIR_INFO             | 0x7C   | Optional                   | [Table 103 &mdash; KEY_PAIR_INFO response message format](#table-kpi) |
| SET_KEY_PAIR_INFO_ACK     | 0x7D   | Optional                   | [Table 108 &mdash; SET_KEY_PAIR_INFO_ACK response message format](#table-skpia) |
| VENDOR_DEFINED_RESPONSE   | 0x7E   | Optional                   | [Table 67 &mdash; VENDOR_DEFINED_RESPONSE response message format](#table-vendor-defined-response-response-message-format) |
| ERROR                     | 0x7F   | Required                   | [Table 57 &mdash; ERROR response message format](#table-error-response-message-format) |
| Reserved                  | All other values  |                 | SPDM implementations compatible with this version shall not use the reserved response codes. |

## SPDM request and response code issuance allowance

[Table 6 &mdash; SPDM request and response messages validity](#table-spdm-request-and-response-messages-validity) describes the conditions under which a request and response can be issued.

The **Session** column describes whether the respective request and response can be sent in a session. If the value is *"Allowed"*, the issuer of the request and response shall be able to send it in a secure session, thereby affording them the protection of a secure session. If the **Session** column value is *"Prohibited"*, the issuer shall be prohibited from sending the respective request and response in a secure session.

The **Outside of a session** column indicates which requests and responses are allowed to be sent free and independent of a session, thereby lacking the protection of a secure session. An *"Allowed"* in this column indicates that the respective request and response shall be able to be sent outside the context of a secure session. Likewise, a *"Prohibited"* in this column shall prohibit the issuer from sending the respective request or response outside the context of a session.

A request and its corresponding response can have an *"Allowed"* value in both the **Session** and **Outside of a session** columns, in which case they can be sent and received in both scenarios but might have additional restrictions. For details, see the respective request and response clauses.

A request and its corresponding response that has an *"Allowed"* value in the **Session** and *"Prohibited"* in the **Outside of a session** columns are commands used by the session.  These commands only operate on the session that they were sent under, which is outside the scope of this specification.  The session ID is implicit from the session used to transmit the commands.

Finally, the **Session phases** column describes which phases of a session the respective request and response shall be issued when they are allowed to be issued in a session.

If, during the session handshake phase, an unexpected request is received using a valid session ID, the Responder shall either send an `ERROR` message in the session with `ErrorCode=UnexpectedRequest` or silently discard the request.

`Vendor-defined` shall indicate whether a VENDOR_DEFINED_REQUEST and VENDOR_DEFINED_RESPONSE is *"Allowed"* or *"Prohibited"* for use in the **Session**, **Outside of a session**, and the applicable **Session phases**.

For details, see the [Session](#session) clause.

<a id="table-spdm-request-and-response-messages-validity"></a>**Table 6 &mdash; SPDM request and response messages validity**

| Request                         | Response                         | Outside of a session | Session              | Session phases    |
|:--------------------------------|:---------------------------------|:---------------------|:-----------          |:------------------|
| GET_MEASUREMENTS                | MEASUREMENTS                     | Allowed              | Allowed              | Application Phase |
| FINISH                          | FINISH_RSP                       | Conditional (**)     | Allowed              | Session Handshake |
| PSK_FINISH                      | PSK_FINISH_RSP                   | Prohibited           | Allowed              | Session Handshake |
| HEARTBEAT                       | HEARTBEAT_ACK                    | Prohibited           | Allowed              | Application Phase |
| KEY_UPDATE                      | KEY_UPDATE_ACK                   | Prohibited           | Allowed              | Application Phase |
| END_SESSION                     | END_SESSION_ACK                  | Prohibited           | Allowed              | Application Phase |
| Not Applicable                  | ERROR                            | Allowed              | Allowed              | All Phases        |
| GET_ENCAPSULATED_REQUEST        | ENCAPSULATED_REQUEST             | Allowed              | Allowed              | All Phases        |
| DELIVER_ENCAPSULATED_RESPONSE   | ENCAPSULATED_RESPONSE_ACK        | Allowed              | Allowed              | All Phases        |
| VENDOR_DEFINED_REQUEST          | VENDOR_DEFINED_RESPONSE          | Vendor-defined       | Vendor-defined       | Vendor-defined    |
| CHUNK_SEND                      | CHUNK_SEND_ACK                   | Allowed              | Allowed              | All Phases        |
| CHUNK_GET                       | CHUNK_RESPONSE                   | Allowed              | Allowed              | All Phases        |
| GET_ENDPOINT_INFO               | ENDPOINT_INFO                    | Allowed              | Allowed              | Application Phase |
| GET_CSR                         | CSR                              | Allowed              | Allowed              | Application Phase |
| SET_CERTIFICATE                 | SET_CERTIFICATE_RSP              | Allowed              | Allowed              | Application Phase |
| GET_DIGESTS                     | DIGESTS                          | Allowed              | Allowed              | Application Phase |
| GET_CERTIFICATE                 | CERTIFICATE                      | Allowed              | Allowed              | Application Phase |
| GET_KEY_PAIR_INFO               | KEY_PAIR_INFO                    | Allowed              | Allowed              | Application Phase |
| SET_KEY_PAIR_INFO               | SET_KEY_PAIR_INFO_ACK            | Allowed              | Allowed              | Application Phase |
| GET_MEASUREMENT_EXTENSION_LOG   | MEASUREMENT_EXTENSION_LOG        | Allowed              | Allowed              | Application Phase |
| GET_SUPPORTED_EVENT_TYPES       | SUPPORTED_EVENT_TYPES            | Prohibited           | Allowed              | Application Phase |
| SUBSCRIBE_EVENT_TYPES           | SUBSCRIBE_EVENT_TYPES_ACK        | Prohibited           | Allowed              | Application Phase |
| SEND_EVENT                      | EVENT_ACK                        | Prohibited           | Allowed              | Application Phase |
| RESPOND_IF_READY                | Response to Original Request (*) | Allowed (*)          | Allowed (*)          | All Phases (*)    |
| All others                      | All others                       | Allowed              | Prohibited           | Not Applicable    |

(*) [See RESPOND_IF_READY request description for details](#respond_if_ready-request-message-format)
(**) Prohibited when `HANDSHAKE_IN_THE_CLEAR_CAP` = `0`, Allowed when `HANDSHAKE_IN_THE_CLEAR_CAP` = `1`.

## Concurrent SPDM message processing

This clause describes the specifications and requirements for handling concurrent overlapping SPDM request messages.

If an endpoint can act as both a Responder and Requester, it shall be able to send request messages and response messages independently.

## Requirements for Requesters

A Requester shall not have multiple outstanding requests to the same Responder within a connection, with the following exceptions:

* As the [GET_VERSION request and VERSION response messages](#get_version-request-and-version-response-messages) clause describes, a Requester can issue a `GET_VERSION` to a Responder to reset the connection at any time, even if the Requester has existing outstanding requests to the same Responder.
* In the [large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism), a single large SPDM request message and a single `CHUNK_SEND` request can be outstanding at the same time.

An outstanding request is a request where the request message has begun transmission, the corresponding response has not been fully received, and the request is not a retry as described in [Timing Requirements](#timing-requirements).

If the Requester has sent a request to a Responder and wants to send a subsequent request to the same Responder, then the Requester shall wait to send the subsequent request until after the Requester completes one of the following actions:

* Receives the response from the Responder for the outstanding request.
* Times out waiting for a response.
* Receives an indication from the transport layer that transmission of the request message failed.
* The Requester encounters an internal error or Reset.
* The Requester sends a `GET_VERSION` to reinitialize the session.

A Requester might send simultaneous request messages to different Responders.

## Requirements for Responders

A Responder is not required to process more than one request message at a time, even across connections, with the following exceptions:

* As the [GET_VERSION request and VERSION response messages](#get_version-request-and-version-response-messages) clause describes, a Requester can issue a `GET_VERSION` to a Responder to reset a connection at any time, even if the Requester has existing outstanding requests to the same Responder.
* In the [large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism), a single large SPDM request message and a single `CHUNK_SEND` request can be outstanding at the same time.
* Retries can be issued multiple times to the same Responder, as [Timing requirements](#timing-requirements) defines.

A Responder that is not ready to accept a new request message or process more than one outstanding request at a time from the same Requester shall either respond with an `ERROR` message of `ErrorCode=Busy` or silently discard the request message.

If a Responder is working on a request message from a Requester, the Responder can respond with an `ERROR` message of `ErrorCode=Busy`.

If a Responder enables simultaneous communications with multiple Requesters, the Responder is expected to distinguish the Requesters by using mechanisms that are outside the scope of this specification.

## Transcript and transcript hash calculation rules

The transcript is a concatenation of the prescribed full messages or message fields in order. In the case where a message is transferred in chunks, only the complete message that is built by the concatenation of chunk payloads shall be added to the transcript. Consequently, the transcript hash is the hash of the transcript using the negotiated hash algorithm (`BaseHashSel` or `ExtHashSel` of `ALGORITHMS`). For messages that are encrypted, the plaintext messages are used in the transcript. Where a transcript indicates that the hash of the specified certificate chain is used, the hash of the certificate chain is calculated over the specified certificate chain, as [Table 33 &mdash; Certificate chain format](#table-certificate-chain-format) describes. Messages that contribute to a transcript may be optional and/or conditional and will only contribute to a transcript if issued. Such messages are identified by the text "if issued" in the transcript definition. For a given message, if it does not have the "if issued" text in the transcript definition, then it is required to be present in the transcript. When an endpoint calculates the transcript hash over a series of messages, the endpoint shall ensure both the existence and the order of the messages as specified by each transcript hash calculation rule.

# SPDM messages

SPDM messages can be divided into the following categories that support different aspects of security exchanges between a Requester and Responder:

* [Capability discovery and negotiation](#capability-discovery-and-negotiation)
* [Responder identity authentication](#responder-identity-authentication)
* [Measurement](#firmware-and-other-measurements)
* [Key agreement for secure-channel establishment](#key_exchange-request-and-key_exchange_rsp-response-messages)

## Capability discovery and negotiation

All Requesters and Responders shall support `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS`.

[Figure 5 &mdash; Capability discovery and negotiation flow](#figure-capability-discovery-and-negotiation-flow) shows the high-level request-response flow and sequence for the capability discovery and negotiation:

<a id="figure-capability-discovery-and-negotiation-flow"></a>**Figure 5 &mdash; Capability discovery and negotiation flow**

![Figure 5 &mdash; Capability discovery and negotiation flow](SPDMSpecification_files/Figure-CapabilityDiscoveryAndNegotiationFlow.svg)

### Negotiated state preamble

<a id="vca-def"></a>The [*`VCA` (Version-Capabilities-Algorithms)*](#vca) shall be the concatenation of messages `GET_VERSION`, `VERSION`, `GET_CAPABILITIES`, `CAPABILITIES`, `NEGOTIATE_ALGORITHMS`, and `ALGORITHMS` last exchanged between the Requester and the Responder.

If the two endpoints do not support session key establishment with the PSK (Pre-Shared Key) option, or if the two endpoints support PSK but the negotiated capabilities and algorithms are not provisioned to both endpoints alongside the PSK, then the Requester shall issue `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS` to construct `VCA`.

If the Responder supports caching the negotiated state (`CACHE_CAP=1`), the Requester might not issue `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS`. In this case, the Requester and the Responder shall store the most recent `VCA` as part of the Negotiated State.

If the two endpoints support session key establishment with the PSK and if the negotiated capabilities and algorithms (the `C` and `A` of `VCA`) are provisioned to both endpoints alongside the PSK, then the Requester shall not issue `GET_CAPABILITIES` and `NEGOTIATE_ALGORITHMS`.

## GET_VERSION request and VERSION response messages

This request message shall retrieve the SPDM version of an endpoint. [Table 8 &mdash; GET_VERSION request message format](#table-get-version-request-message-format) shows the `GET_VERSION` request message format and [Table 9 &mdash; Successful VERSION response message format](#table-successful-version-response-message-format) shows the `VERSION` response message format.

In all future SPDM versions, the `GET_VERSION` and `VERSION` response messages will be backward compatible with all earlier versions.

The Requester shall begin the discovery process by sending a `GET_VERSION` request message with the value of the `SPDMVersion` field set to `0x10`. All Responders shall always support the `GET_VERSION` request message with major version `0x1` and provide a `VERSION` response containing all supported versions, as [Table 8 &mdash; GET_VERSION request message format](#table-get-version-request-message-format) describes.

The Requester shall consult the `VERSION` response to select a common supported version, which should be the latest supported common version.  The Requester shall use the selected version in all future communication of other requests.  A Requester shall not issue other requests until it receives a successful `VERSION` response and identifies a common version that both sides support.  A Responder shall not respond to the `GET_VERSION` request message with an `ERROR` message except for `ErrorCode`s specified in this clause. The selected version shall be the version in the `SPDMVersion` field of the Request (other than `GET_VERSION`) immediately following the `GET_VERSION` request. If the Requester uses a version other than the selected version in a Request, the Responder should either return an `ERROR` message of `ErrorCode=VersionMismatch` or silently discard the Request.

A Requester can issue a `GET_VERSION` request message to a Responder at any time, which serves as an exception to [Requirements for Requesters](#requirements-for-requesters) to allow for scenarios where a Requester is required to restart the protocol due to an internal error or Reset.

After receiving a valid `GET_VERSION` request, the Responder shall invalidate state and data associated with all previous requests from the same Requester.  All active sessions between the Requester and the Responder are terminated, and information (such as session keys and session IDs) for those sessions should not be used anymore.  Additionally, this message shall clear the previously [*Negotiated State*](#negotiated-state), if any, in both the Requester and its corresponding Responder. An invalid `GET_VERSION` request that results in the Responder returning an error to the Requester shall not affect the connection state.  The `ERROR` message resulting from an invalid `GET_VERSION` request shall have the value of the `SPDMVersion` field set to `0x10`.

After sending the `VERSION` response for a `GET_VERSION` request, if the Responder completes a runtime code or configuration change for its hardware or firmware measurement and the change has taken effect, then the Responder shall either silently discard any request received outside of a session or respond with an `ERROR` message of `ErrorCode=RequestResynch` to any request received outside of a session, until a `GET_VERSION` request is received. For requests received within a session, the Responder shall follow the selected session policy that the Requester selects in [Table 70 &mdash; Session policy](#table-terminate-config) at the time of session establishment.

[Figure 6 &mdash; Discovering the common major version](#figure-discovering-the-common-major-version) shows the process:

<a id="figure-discovering-the-common-major-version"></a>**Figure 6 &mdash; Discovering the common major version**

![Figure 6 &mdash; Discovering the common major version](SPDMSpecification_files/Figure-DiscoveringCommonMajorVersion.svg)

[Table 8 &mdash; GET_VERSION request message format](#table-get-version-request-message-format) shows the `GET_VERSION` request message format:

<a id="table-get-version-request-message-format"></a>**Table 8 &mdash; GET_VERSION request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | SPDMVersion         | 1            | Shall be `0x10` (V1.0). |
| 1      | RequestResponseCode | 1            | Shall be `0x84`=`GET_VERSION`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2      | Param1              | 1            | Reserved.            |
| 3      | Param2              | 1            | Reserved.            |

[Table 9 &mdash; Successful VERSION response message format](#table-successful-version-response-message-format) shows the successful `VERSION` response message format:

<a id="table-successful-version-response-message-format"></a>**Table 9 &mdash; Successful VERSION response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | SPDMVersion             | 1            | Shall be `0x10` (V1.0). |
| 1      | RequestResponseCode     | 1            | Shall be `0x04`=`VERSION`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2      | Param1                  | 1            | Reserved.            |
| 3      | Param2                  | 1            | Reserved.            |
| 4      | Reserved                | 1            | Reserved.            |
| 5      | VersionNumberEntryCount | 1            | Number of version entries present in this table (=n). |
| 6      | VersionNumberEntry1:n   | 2 \* n         | 16-bit version entry. See [Table 10 &mdash; VersionNumberEntry definition](#table-versionnumberentry-definition). Each entry should be unique. |

[Table 10 &mdash; VersionNumberEntry definition](#table-versionnumberentry-definition) shows the `VersionNumberEntry` definition. See [Version encoding](#version-encoding) for more details.

<a id="table-versionnumberentry-definition"></a>**Table 10 &mdash; VersionNumberEntry definition**

| Bit offset | Field               | Description                        |
|:-----------|:--------------------|:-----------------------------------|
| [15:12] | MajorVersion        | Shall be the version of the specification having changes that are incompatible with one or more functions in earlier major versions of the specification. |
| [11:8]  | MinorVersion        | Shall be the version of the specification having changes that are compatible with functions in earlier minor versions of this major version specification. |
| [7:4]   | UpdateVersionNumber | Shall be the version of the specification with editorial updates and errata fixes.  Informational; ignore when checking versions for interoperability. |
| [3:0]   | Alpha               | Shall be the pre-release work-in-progress version of the specification.  Because the `Alpha` value represents an in-development version of the specification, versions that share the same major and minor version numbers but have different `Alpha` versions might not be fully interoperable.  Released versions shall have an `Alpha` value of zero (`0`). |

## GET_CAPABILITIES request and CAPABILITIES response messages

This request message shall retrieve the SPDM capabilities of an endpoint.

[Table 11 &mdash; GET_CAPABILITIES request message format](#table-get-capabilities-request-message-format) shows the `GET_CAPABILITIES` request message format.

[Table 12 &mdash; Successful CAPABILITIES response message format](#table-successful-capabilities-response-message-format) shows the `CAPABILITIES` response message format.

[Table 13 &mdash; Flag fields definitions for the Requester](#table-flag-fields-definitions-for-the-requester) shows the flag fields definitions for the Requester.

Likewise, [Table 14 &mdash; Flag fields definitions for the Responder](#table-flag-fields-definitions-for-the-responder) shows the flag fields definitions for the Responder.

To properly support transferring of SPDM messages, the Requester and Responder shall indicate two buffer sizes:

* One for receiving a single SPDM transfer called `DataTransferSize`
* One for indicating their maximum internal buffer size for processing a single assembled received SPDM message called `MaxSPDMmsgSize`

Additionally, the Requester and Responder can have a transmit buffer. The transmit buffer size is not communicated to the other SPDM endpoint, but it can be less than the `DataTransferSize` of the receiving SPDM endpoint.

Both the Requester and Responder shall support a minimum size for both the transmit and receive buffer to successfully transfer SPDM messages. The minimum size is referred to as `MinDataTransferSize.` For this version of the specification, the `MinDataTransferSize` shall be 42. This value is the size, in bytes, of the SPDM message with the largest size from this list, assuming all fields are present:

* `GET_VERSION`
* `VERSION` assuming no versions returned contain `Alpha` versions in `VersionNumberEntry` and version entries are not duplicated.
* `GET_CAPABILITIES`
* `CAPABILITIES` with `Param1` in the `GET_CAPABILITIES` request set to 0.
* `CHUNK_SEND` using the size of the SPDM Header for the size of the `SPDMchunk` field.
* `CHUNK_SEND_ACK` using the maximum size of `ERROR` message for the size of the `ResponseToLargeRequest` field.
* `CHUNK_GET`
* `CHUNK_RESPONSE` using the size of SPDM Header for the size of the `SPDMchunk` field.
* `ERROR` using the maximum size for the `ExtendedErrorData`

The `GET_CAPABILITIES` request with Extended capabilities (Bit 0 of `Param1` set to a value of 1) is only allowed if both the Requester and Responder support the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism) (`CHUNK_CAP=1`). If the `GET_CAPABILITIES` request sets Bit 0 of `Param1` to a value of 1, then the Responder shall use the value for `DataTransferSize` and `MaxSPDMmsgSize` from the request for the transmission of the `CAPABILITIES` response. A Responder can report that it needs to transmit the response in smaller transfers by sending an `ERROR` message of `ErrorCode=LargeResponse`. If the `GET_CAPABILITIES` request sets Bit 0 of `Param1` to a value of 1 and the Responder does not support the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism) (`CHUNK_CAP=0`), the Responder shall send an `ERROR` message of `ErrorCode=InvalidRequest`.

<a id="table-get-capabilities-request-message-format"></a>**Table 11 &mdash; GET_CAPABILITIES request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0     | SPDMVersion         | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1     | RequestResponseCode | 1            | Shall be `0xE1`=`GET_CAPABILITIES`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2     | Param1              | 1            | Shall be the extended capabilities to include in the response. <ul><li>Bit 0. If set in the requests, the Responder shall include the Supported Algorithms Block in its `CAPABILITIES` response if it supports this extended capability. If the Requester does not support the Large SPDM message transfer mechanism (`CHUNK_CAP=0`), this bit shall be 0.</li><li>All other values reserved.</li></ul> |
| 3     | Param2              | 1            | Reserved.            |
| 4     | Reserved            | 1            | Reserved.            |
| 5     | CTExponent          | 1            | Shall be exponent of base 2, which is used to calculate `CT`.<br/><br/>See [Table 7 &mdash; Timing specification for SPDM messages](#table-timing-specification-for-spdm-messages).<br/><br/>The equation for `CT` shall be 2<sup>`CTExponent`</sup> microseconds (µs).<br/><br/>For example, if `CTExponent` is 10, `CT` is 2<sup>10</sup> = 1024 µs. |
| 6     | Reserved            | 2            | Reserved.            |
| 8     | Flags               | 4            | See [Table 13 &mdash; Flag fields definitions for the Requester](#table-flag-fields-definitions-for-the-requester). |
| 12    | DataTransferSize    | 4            | This field shall indicate the maximum buffer size, in bytes, of the Requester for receiving a single and complete SPDM message whose message size is less than or equal to the value in this field. The value of this field shall be equal to or greater than `MinDataTransferSize`. The `DataTransferSize` shall exclude transport headers, encryption headers, and [MAC](#mac). This field helps the sender of the SPDM message know whether or not it needs to utilize the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism). |
| 16    | MaxSPDMmsgSize      | 4            | If the Requester supports the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism), this field shall indicate the maximum size, in bytes, of the internal buffer of a Requester used to reassemble a single and complete [Large SPDM message](#large-spdm-message). This field shall be greater than or equal to `DataTransferSize`. This buffer size is most helpful when transferring a Large SPDM message in multiple chunks because it tells the sender whether or not there is enough memory for the fully reassembled SPDM message.<br/><br/>If the Requester does not support the Large SPDM message transfer mechanism, this field shall be equal to the `DataTransferSize` of the Requester. |

<a id="table-successful-capabilities-response-message-format"></a>**Table 12 &mdash; Successful CAPABILITIES response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0     | SPDMVersion         | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1     | RequestResponseCode | 1            | Shall be `0x61`=`CAPABILITIES`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2     | Param1              | 1            | Shall be the extended capabilities included in the response. <ul><li>Bit 0. If the request message sets the Supported Algorithms extended capability bit and the Responder supports this extended capability, then the Responder shall set this bit in the response and shall include the Supported Algorithms Block in its `CAPABILITIES` response. If the Responder does not support this extended capability or does not support the Large SPDM message transfer mechanism (`CHUNK_CAP=0`), this bit shall be 0.</li><li>All other values reserved.</li></ul> |
| 3     | Param2              | 1            | Reserved.            |
| 4     | Reserved            | 1            | Reserved.            |
| 5     | CTExponent          | 1            | Shall be the exponent of base 2, which used to calculate `CT`.<br/><br/>See [Table 7 &mdash; Timing specification for SPDM messages](#table-timing-specification-for-spdm-messages).<br/><br/>The equation for `CT` shall be 2<sup>`CTExponent`</sup> microseconds (µs).<br/><br/>For example, if `CTExponent` is 10, `CT` is 2<sup>10</sup> = 1024 µs. |
| 6     | Reserved            | 2            | Reserved.            |
| 8     | Flags               | 4            | See [Table 14 &mdash; Flag fields definitions for the Responder](#table-flag-fields-definitions-for-the-responder). |
| 12    | DataTransferSize    | 4            | This field shall indicate the maximum buffer size, in bytes, of the Responder for receiving a single and complete SPDM message whose message size is less than or equal to the value in this field. The value of this field shall be equal to or greater than `MinDataTransferSize`. The `DataTransferSize` shall exclude transport headers, encryption headers, and [MAC](#mac). This field helps the sender of the SPDM message know whether or not it needs to utilize the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism). |
| 16    | MaxSPDMmsgSize      | 4            | If the Responder supports the [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism), this field shall indicate the maximum size, in bytes, of the internal buffer of a Responder used to reassemble a single and complete [Large SPDM message](#large-spdm-message). This field shall be greater than or equal to `DataTransferSize`. This buffer size is most helpful when transferring a Large SPDM message in multiple chunks because it tells the sender whether or not there is enough memory for the fully reassembled SPDM message.<br/><br/>If the Responder does not support the Large SPDM message transfer mechanism, this field shall be equal to the `DataTransferSize` of the Responder. |
| 20    | SupportedAlgorithms | AlgSize or 0 | If present, this field shall be `AlgSize` in size and the format of the field shall be as described in [Supported algorithms block](#supported-algorithms-block). If Bit 0 of `Param1` does not indicate that the Supported Algorithm extended capability is included in this response, then this field shall be absent. |

As described in other parts of this specification, a Requester or Responder can reverse roles or take on both roles for certain SPDM messages and flows. Thus, an SPDM endpoint cannot send a Large SPDM message that exceeds the `MaxSPDMmsgSize` of the receiving SPDM endpoint. Specifically, a requesting SPDM endpoint shall not send a request that exceeds the size of `MaxSPDMmsgSize` of the responding SPDM endpoint. Likewise, a responding SPDM endpoint shall not send a response that exceeds the size of `MaxSPDMmsgSize` of the requesting SPDM endpoint. If the size of a response message exceeds the size of the `MaxSPDMmsgSize` of the requesting SPDM endpoint, the responding SPDM endpoint shall respond with an `ERROR` message of `ErrorCode=ResponseTooLarge`. If the size of a request message exceeds the size of the `MaxSPDMmsgSize` of the responding SPDM endpoint, the responding SPDM endpoint shall either respond with an `ERROR` message of `ErrorCode=RequestTooLarge` or silently discard the request. Additionally, an SPDM endpoint is expected to provide graceful error handling (for example, buffer overflow/underflow protection) in the event that it receives an SPDM message that exceeds its `MaxSPDMmsgSize`.

[Table 13 &mdash; Flag fields definitions for the Requester](#table-flag-fields-definitions-for-the-requester) shows the flag fields definitions for the Requester.

Unless otherwise stated, if a Requester indicates support for a capability associated with an SPDM request or response message, it means the Requester can receive the corresponding request and produce a successful response. In other words, the Requester is acting as a Responder to that SPDM request associated with that capability. For example, if a Requester sets the `CERT_CAP` bit to `1`, the Requester can receive a `GET_CERTIFICATE` request and send back a successful `CERTIFICATE` response message.

`AlgSize` is the size of the [Supported algorithms block](#supported-algorithms-block). If the Supported Algorithms Block is not included in the response, then the `SupportedAlgorithms` field shall be absent.

<a id="table-flag-fields-definitions-for-the-requester"></a>**Table 13 &mdash; Flag fields definitions for the Requester**

| Byte offset | Bit offset | Field            | Description                |
|:------------|:-----------|:-----------------|:---------------------------|
| 0     | 0             | Reserved        | Reserved.            |
| 0     | 1             | CERT_CAP        | If set, Requester shall support `DIGESTS` and `CERTIFICATE` response messages. Shall be `0b` if the Requester does not support asymmetric algorithms. |
| 0     | 2             | CHAL_CAP        | **DEPRECATED:** If set, Requester shall support `CHALLENGE_AUTH` response message. |
| 0     | [5:3]         | Reserved        | Reserved.            |
| 0     | 6             | ENCRYPT_CAP     | If set, Requester shall support message encryption in a secure session. If set, when the Requester chooses to start a secure session, the Requester shall send one of the Session-Secrets-Exchange request messages supported by the Responder. |
| 0     | 7             | MAC_CAP         | If set, Requester shall support message authentication in a secure session. If set, when the Requester chooses to start a secure session, the Requester shall send one of the Session-Secrets-Exchange request messages supported by the Responder. `MAC_CAP` is not the same as the `HMAC` in the `RequesterVerifyData` or `ResponderVerifyData` fields of Session-Secrets-Exchange and Session-Secrets-Finish messages. |
| 1     | 0             | MUT_AUTH_CAP    | If set, Requester shall support mutual authentication.  |
| 1     | 1             | KEY_EX_CAP      | If set, Requester shall support `KEY_EXCHANGE` request message. If set, `ENCRYPT_CAP` or `MAC_CAP` shall be set. |
| 1     | [3:2]         | PSK_CAP         | Pre-Shared Key capabilities of the Requester.<ul><li>`00b`. Requester shall not support Pre-Shared Key capabilities.</li><li>`01b`. Requester shall support Pre-Shared Key </li><li>`10b` and `11b`. Reserved.</li></ul>If supported, `ENCRYPT_CAP` or `MAC_CAP` shall be set. |
| 1     | 4             | ENCAP_CAP       | If set, Requester shall support `GET_ENCAPSULATED_REQUEST`, `ENCAPSULATED_REQUEST`, `DELIVER_ENCAPSULATED_RESPONSE`, and `ENCAPSULATED_RESPONSE_ACK` messages. Additionally, the transport may require the Requester to support these messages.<br/><br/>`ENCAP_CAP` was previously deprecated because [Basic mutual authentication](#basic-mutual-authentication) is deprecated. Deprecation is removed since some messages, such as `KEY_UPDATE`, do not require mutual authentication but still require `ENCAP_CAP`. |
| 1     | 5             | HBEAT_CAP       | If set, Requester shall support `HEARTBEAT` messages. |
| 1     | 6             | KEY_UPD_CAP     | If set, Requester shall support `KEY_UPDATE` messages. |
| 1     | 7             | HANDSHAKE_IN_THE_CLEAR_CAP  | If set, the Requester can support a Responder that can only send and receive all SPDM messages exchanged during the Session Handshake Phase in the clear (such as without encryption and message authentication). Application data is encrypted and/or authenticated using the negotiated cryptographic algorithms as normal. Setting this bit leads to changes in the contents of certain SPDM messages, as discussed in other parts of this specification.<br/><br/>If this bit is cleared, the Requester signals that it requires encryption and/or message authentication of SPDM messages exchanged during the Session Handshake Phase.<br/><br/>If the Requester supports Pre-Shared Keys (`PSK_CAP` is `01b`) and does not support asymmetric key exchange (`KEY_EX_CAP` is `0b`), then this bit shall be zero. If the Requester does not support encryption and message authentication, then this bit shall be zero.<br/><br/>In other words, this bit indicates whether `MAC_CAP` and `ENCRYPT_CAP` is involved accordingly in the handshake phase of a secure session or both encryption and message authentication capabilities are disabled in the session handshake phase of a secure session.  |
| 2     | 0             | PUB_KEY_ID_CAP  | If set, the public key of the Requester was provisioned to the Responder. The transport layer is responsible for identifying the Responder. In this case, the `CERT_CAP` and `MULTI_KEY_CAP` of the Requester shall be `0`. |
| 2     | 1             | CHUNK_CAP       | If set, Requester shall support [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism) messages.|
| 2     | [5:2]         | Reserved        | Reserved.            |
| 2     | [7:6]         | EP_INFO_CAP     | The `ENDPOINT_INFO` response capabilities of the Requester.<br/><ul><li>`00b`. The Requester does not support `ENDPOINT_INFO` response capabilities.</li><li>`01b`. The Requester supports the `ENDPOINT_INFO` response but cannot perform signature generation for this response.</li><li>`10b`. The Requester supports the `ENDPOINT_INFO` response and can generate signatures for this response.</li><li>`11b`. Reserved.</li></ul> |
| 3     | 0             | Reserved        | Reserved.            |
| 3     | 1             | EVENT_CAP       | If set, the Requester is an [Event Notifier](#event-notifier). See [Event mechanism](#event-mechanism) for details. |
| 3     | [3:2]         | MULTI_KEY_CAP   | Shall be the Multiple Asymmetric Key capabilities of the Requester.<ul><li>`00b`.  Requester shall not support `Multiple Asymmetric Key` capabilities. </li><li>`01b`.  Requester shall only support `Multiple Asymmetric Key` capabilities.</li><li>`10b`.  Requester shall support `Multiple Asymmetric Key` capabilities, and Responder can use `RequesterMultiKeyConnSel` as [Multiple Asymmetric Key Negotiation](#multiple-asymmetric-key-negotiation) describes. </li><li>`11b`.  Reserved. </li></ul>If set to `01b` or `10b`, the Requester shall support more than one key pair for at least one asymmetric algorithm for use in Requester authentication such as in mutual authentication. In the case of mutual authentication, these are the key pairs belonging to the Requester. |
| 3     | [7:4]         | Reserved        | Reserved.            |

---------------------------

[Table 14 &mdash; Flag fields definitions for the Responder](#table-flag-fields-definitions-for-the-responder) shows the flag fields definitions for the Responder.

Unless otherwise stated, if a Responder indicates support for a capability associated with an SPDM request or response message, it means the Responder can receive the corresponding request and produce a successful response. For example, if a Responder sets the `CERT_CAP` bit to `1`, the Responder can receive a `GET_CERTIFICATE` request and send back a successful `CERTIFICATE` response message.

<a id="table-flag-fields-definitions-for-the-responder"></a>**Table 14 &mdash; Flag fields definitions for the Responder**

| Byte offset | Bit offset | Field                        | Description                |
|:------------|:-----------|:-----------------------------|:---------------------------|
| 0     | 0             | CACHE_CAP                   | If set, the Responder shall support the ability to cache the [*Negotiated State*](#negotiated-state) across a Reset.  This allows the Requester to skip reissuing the `GET_VERSION`, `GET_CAPABILITIES`, and `NEGOTIATE_ALGORITHMS` requests after a Reset.  The Responder shall cache the selected cryptographic algorithms as one of the parameters of the Negotiated State.  If the Requester chooses to skip issuing these requests after the Reset, the Requester shall also cache the same selected cryptographic algorithms. |
| 0     | 1             | CERT_CAP                    | If set, Responder shall support `DIGESTS` and `CERTIFICATE` response messages. Shall be `0b` if the Responder does not support asymmetric algorithms. |
| 0     | 2             | CHAL_CAP                    | If set, Responder shall support `CHALLENGE_AUTH` response message. |
| 0     | [4:3]           | MEAS_CAP                    | `MEASUREMENTS` response capabilities of the Responder.<ul><li>`00b`. The Responder shall not support `MEASUREMENTS` response capabilities.</li><li>`01b`. The Responder shall support `MEASUREMENTS` response but cannot perform signature generation for this response.</li><li>`10b`. The Responder shall support `MEASUREMENTS` response and can generate signatures for this response.</li><li>`11b`. Reserved. </li></ul> Note that, apart from affecting `MEASUREMENTS`, this capability also affects Param2 of `CHALLENGE`, Param1 of `KEY_EXCHANGE`, Param1 of `PSK_EXCHANGE`, and the MeasurementSummaryHash field of `KEY_EXCHANGE_RSP`, `CHALLENGE_AUTH`, and `PSK_EXCHANGE_RSP`. See the respective request and response clauses for further details. |
| 0     | 5             | MEAS_FRESH_CAP              | <ul><li>`0`. As part of `MEASUREMENTS` response message, the Responder may return `MEASUREMENTS` that were computed during the last Responder's Reset.</li><li>`1`. The Responder shall support recomputing all `MEASUREMENTS` without requiring a Reset and shall always return fresh `MEASUREMENTS` as part of `MEASUREMENTS` response message.</li></ul> |
| 0     | 6             | ENCRYPT_CAP                 | If set, Responder shall support message encryption in a secure session. If set, `PSK_CAP` or `KEY_EX_CAP` shall be set accordingly to indicate support. |
| 0     | 7             | MAC_CAP                     | If set, Responder shall support message authentication in a secure session. If set, `PSK_CAP` or `KEY_EX_CAP` shall be set accordingly to indicate support. `MAC_CAP` is not the same as the `HMAC` in the `RequesterVerifyData` or `ResponderVerifyData` fields of Session-Secrets-Exchange and Session-Secrets-Finish messages. |
| 1     | 0             | MUT_AUTH_CAP                | If set, Responder shall support mutual authentication. |
| 1     | 1             | KEY_EX_CAP                  | If set, Responder shall support `KEY_EXCHANGE_RSP` response message. If set, `ENCRYPT_CAP` or `MAC_CAP` shall be set. |
| 1     | [3:2]           | PSK_CAP                     | `Pre-Shared Key` capabilities of the Responder.<ul><li>`00b`.  Responder shall not support `Pre-Shared Key` capabilities.</li><li>`01b`.  Responder shall support `Pre-Shared Key` but does not provide ResponderContext for session key derivation.</li><li>`10b`.  Responder shall support `Pre-Shared Key` and provides ResponderContext for session key derivation. </li><li>`11b`.  Reserved.</li></ul>If supported, `ENCRYPT_CAP` or `MAC_CAP` shall be set. |
| 1     | 4             | ENCAP_CAP                   | If set, Responder shall support `GET_ENCAPSULATED_REQUEST`, `ENCAPSULATED_REQUEST`, `DELIVER_ENCAPSULATED_RESPONSE`, and `ENCAPSULATED_RESPONSE_ACK` messages. Additionally, the transport may require the Responder to support these messages.<br/><br/>`ENCAP_CAP` was previously deprecated because [Basic mutual authentication](#basic-mutual-authentication) is deprecated. Deprecation is removed since some messages, such as `KEY_UPDATE`, do not require mutual authentication but still require `ENCAP_CAP`. |
| 1     | 5             | HBEAT_CAP                   | If set, Responder shall support `HEARTBEAT` messages. |
| 1     | 6             | KEY_UPD_CAP                 | If set, Responder shall support `KEY_UPDATE` messages. |
| 1     | 7             | HANDSHAKE_IN_THE_CLEAR_CAP  | If set, the Responder can only send and receive messages without encryption and message authentication during the Session Handshake Phase. If set, `KEY_EX_CAP` shall also be set. Setting this bit leads to changes in the contents of certain SPDM messages, as discussed in other parts of this specification.<br/><br/>If the Responder supports Pre-Shared Keys (`PSK_CAP` is `01b`) and does not support asymmetric key exchange (`KEY_EX_CAP` is `0b`), then this bit shall be zero. If the Responder does not support encryption and message authentication, then this bit shall be zero.<br/><br/>In other words, this bit indicates whether message authentication and/or encryption (`MAC_CAP` and `ENCRYPT_CAP`) are used in the handshake phase of a secure session. |
| 2     | 0             | PUB_KEY_ID_CAP              | If set, the public key of the Responder was provisioned to the Requester. The transport layer is responsible for identifying the Requester. In this case, the `CERT_CAP`, `ALIAS_CERT_CAP`, and `MULTI_KEY_CAP` of the Responder shall be `0`. |
| 2     | 1             | CHUNK_CAP                   | If set, Responder shall support [Large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism) messages. |
| 2     | 2             | ALIAS_CERT_CAP              | If set, the Responder shall use the `AliasCert` model. See [Identity provisioning](#identity-provisioning) for details. |
| 2     | 3             | SET_CERT_CAP                | If set, Responder shall support `SET_CERTIFICATE_RSP` response messages. |
| 2     | 4             | CSR_CAP                     | If set, Responder shall support `CSR` response messages. If this bit is set, `SET_CERT_CAP` shall be set. |
| 2     | 5             | CERT_INSTALL_RESET_CAP      | If set, Responder may return an `ERROR` message of `ErrorCode=ResetRequired` to complete a certificate provisioning request. If this bit is set, `SET_CERT_CAP` shall be set and `CSR_CAP` can be set. |
| 2     | [7:6]         | EP_INFO_CAP                 | The `ENDPOINT_INFO` response capabilities of the Responder.<br/><ul><li>`00b`. The Responder shall not support `ENDPOINT_INFO` response capabilities.</li><li>`01b`. The Responder shall support the `ENDPOINT_INFO` response but cannot perform signature generation for this response.</li><li>`10b`. The Responder shall support the `ENDPOINT_INFO` response and can generate signatures for this response.</li><li>`11b`. Reserved.</li></ul> |
| 3     | 0             | MEL_CAP                     | If set, Responder shall support `MEASUREMENT_EXTENSION_LOG` response message. |
| 3     | 1             | EVENT_CAP                   | If set, the Responder is an [Event Notifier](#event-notifier). See [Event mechanism](#event-mechanism) for details. |
| 3     | [3:2]         | MULTI_KEY_CAP               | Shall be the Multiple Asymmetric Key capabilities of the Responder.<ul><li>`00b`.  Responder shall not support `Multiple Asymmetric Key` capabilities. </li><li>`01b`.  Responder shall only support `Multiple Asymmetric Key` capabilities.</li><li>`10b`.  Responder shall support `Multiple Asymmetric Key` capabilities, and Requester can use `ResponderMultiKeyConn` as [Multiple Asymmetric Key Negotiation](#multiple-asymmetric-key-negotiation) describes. </li><li>`11b`.  Reserved. </li></ul>If set to `01b` or `10b`, the Responder shall support more than one key pair for at least one asymmetric algorithm for the SPDM connection to use in Responder authentication. |
| 3     | 4             | GET_KEY_PAIR_INFO_CAP       | If set, Responder shall support `KEY_PAIR_INFO` response messages. If the Responder sets `MULTI_KEY_CAP`, this bit shall also be set. |
| 3     | 5             | SET_KEY_PAIR_INFO_CAP       | If set, Responder shall support `SET_KEY_PAIR_INFO_ACK` response message. |
| 3     | [7:6]         | Reserved                    | Reserved. |

In the case where an SPDM implementation incorrectly returns an illegal combination of capability flags as they are defined by this specification (for example, `ENCRYPT_CAP` is set but both `KEY_EX_CAP` and `PSK_CAP` are cleared), the following guidance is provided: If a Responder detects an illegal capability flag combination reported by the Requester, it shall issue an `ERROR` message of `ErrorCode=InvalidRequest`.

### Supported algorithms block

The Supported Algorithms Block reports all options from the `ALGORITHMS` response that are supported by the Responder. The Supported Algorithms Block shall conform to the [Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format](#table-negotiate-algorithms-request-message-format), including all fields from `Param1` through the end of the message, inclusive. When constructing the Supported Algorithms Block, the Responder shall follow all requirements for the Requester, and shall set all bits and values that reflect algorithms that the Responder supports.

## NEGOTIATE_ALGORITHMS request and ALGORITHMS response messages

This request message shall negotiate cryptographic algorithms. In SPDM, the Requester issues `NEGOTIATE_ALGORITHMS` to indicate which cryptographic algorithm(s) it supports for each type of cryptographic operation, and the Responder selects one algorithm of each type using the `ALGORITHMS` response message. The selected algorithms shall be used for all relevant cryptographic operations for the duration of the connection. The criteria a Responder uses to determine which algorithm to select when more than one are supported by both endpoints are outside the scope of this specification.

[Figure 7 &mdash; Hashing algorithm selection: Example 1](#figure-hashing-algorithm-selection-example-1) illustrates how two endpoints negotiate a base hashing algorithm. Endpoint A issues a `NEGOTIATE_ALGORITHMS` request message, and endpoint B returns a selected mutually supported algorithm in the `ALGORITHMS` response.

<a id="figure-hashing-algorithm-selection-example-1"></a>**Figure 7 &mdash; Hashing algorithm selection: Example 1**

![Figure 7 &mdash; Hashing algorithm selection: Example 1](SPDMSpecification_files/Figure-HashingAlgorithmSelectionExample1.svg)

If the Requester and Responder support no common algorithms of a particular type, the Responder shall issue an `ALGORITHMS` response message with all appropriate selection field values set to zero to indicate that no selection was made. The Responder should respond to all subsequent requests by this Requester with an `ERROR` message of `ErrorCode=RequestResynch`. The Responder may continue to operate with limited functionality for operations that do not require negotiated cryptographic algorithms.

A Requester shall not issue a `NEGOTIATE_ALGORITHMS` request message until it receives a successful `CAPABILITIES` response message.

After a Requester issues a `NEGOTIATE_ALGORITHMS` request, it shall not issue any other SPDM requests, with the exception of `GET_VERSION`, until it receives a successful `ALGORITHMS` response message.

For each algorithm type, a Responder shall not select both an SPDM-enumerated algorithm and an extended algorithm.

The SPDM protocol accounts for the possibility that both endpoints issue `NEGOTIATE_ALGORITHMS` request messages independently of each other.  In this case, the endpoint A Requester and endpoint B Responder communication pair might select a different algorithm from the one selected by the endpoint B Requester and endpoint A Responder communication pair.

[Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format](#table-negotiate-algorithms-request-message-format) shows the `NEGOTIATE_ALGORITHMS` request message format.

<a id="table-negotiate-algorithms-request-message-format"></a>**Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0                        | SPDMVersion               | 1               | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1                        | RequestResponseCode       | 1               | Shall be `0xE3`=`NEGOTIATE_ALGORITHMS`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2                        | Param1                    | 1               | Shall be the number of algorithm structure tables in this request using `ReqAlgStruct`. |
| 3                        | Param2                    | 1               | Reserved. |
| 4                        | Length                    | 2               | Shall be the length of the entire request message, in bytes. Length shall be less than or equal to 128 bytes. |
| 6                        | MeasurementSpecification  | 1               | Bit mask.  The [Measurement specification field format table](#table-ms-bit-format) defines the format for this field.  For each defined measurement specification a Requester supports, the Requester can set the appropriate bits. |
| 7                        | OtherParamsSupport        | 1               | Shall be the selection bit mask.<br/><br/>Bit [3:0] - See [Opaque Data Format Support and Selection Table](#table-odfs-selection)<br/>Bit [4] - This field shall be the `ResponderMultiKeyConn` field as [Multiple Asymmetric Key Negotiation](#multiple-asymmetric-key-negotiation) describes.<br/>Bit [7:5] - Reserved. |
| 8                        | BaseAsymAlgo              | 4               | Shall be the bit mask listing Requester-supported SPDM-enumerated asymmetric key signature algorithms for the purpose of signature verification. If the Requester does not support any request/response pair that requires signature verification, this value shall be set to zero. If the Requester will not send any requests that require a signature, this value should be set to zero. Let `SigLen` be the size of the signature in bytes.<ul><li>Byte 0 Bit 0. [TPM_ALG_RSASSA_2048](#signature-algorithm-references) where `SigLen`=256.</li><li>Byte 0 Bit 1. [TPM_ALG_RSAPSS_2048](#signature-algorithm-references) where `SigLen`=256.</li><li>Byte 0 Bit 2. [TPM_ALG_RSASSA_3072](#signature-algorithm-references) where `SigLen`=384.</li><li>Byte 0 Bit 3. [TPM_ALG_RSAPSS_3072](#signature-algorithm-references) where `SigLen`=384.</li><li>Byte 0 Bit 4. [TPM_ALG_ECDSA_ECC_NIST_P256](#signature-algorithm-references) where `SigLen`=64 (32-byte r followed by 32-byte s).</li><li>Byte 0 Bit 5. [TPM_ALG_RSASSA_4096](#signature-algorithm-references) where `SigLen`=512.</li><li>Byte 0 Bit 6. [TPM_ALG_RSAPSS_4096](#signature-algorithm-references) where `SigLen`=512.</li><li>Byte 0 Bit 7. [TPM_ALG_ECDSA_ECC_NIST_P384](#signature-algorithm-references) where `SigLen`=96 (48-byte r followed by 48-byte s).</li><li>Byte 1 Bit 0. [TPM_ALG_ECDSA_ECC_NIST_P521](#signature-algorithm-references) where `SigLen`=132 (66-byte r followed by 66-byte s).</li><li>Byte 1 Bit 1. [TPM_ALG_SM2_ECC_SM2_P256](#signature-algorithm-references) where `SigLen`=64 (32-byte `SM2_R` followed by 32-byte `SM2_S`).</li><li>Byte 1 Bit 2. [EdDSA ed25519](#signature-algorithm-references) where `SigLen`=64 (32-byte R followed by 32-byte S).</li><li>Byte 1 Bit 3. [EdDSA ed448](#signature-algorithm-references) where `SigLen`=114 (57-byte R followed by 57-byte S).</li><li>All other values reserved.</li></ul> |
| 12                       | BaseHashAlgo              | 4               | Shall be the bit mask listing Requester-supported SPDM-enumerated cryptographic hashing algorithms. If the Requester does not support any request/response pair that requires hashing operations, this value shall be set to zero.<ul><li>Byte 0 Bit 0. [TPM_ALG_SHA_256](#TCG-algorithm-registry)</li><li>Byte 0 Bit 1. [TPM_ALG_SHA_384](#TCG-algorithm-registry)</li><li>Byte 0 Bit 2. [TPM_ALG_SHA_512](#TCG-algorithm-registry)</li><li>Byte 0 Bit 3. [TPM_ALG_SHA3_256](#TCG-algorithm-registry)</li><li>Byte 0 Bit 4. [TPM_ALG_SHA3_384](#TCG-algorithm-registry)</li><li>Byte 0 Bit 5. [TPM_ALG_SHA3_512](#TCG-algorithm-registry)</li><li>Byte 0 Bit 6. [TPM_ALG_SM3_256](#TCG-algorithm-registry)</li><li>All other values reserved.</li></ul> |
| 16                       | Reserved                  | 12              | Reserved. |
| 28                       | ExtAsymCount              | 1               | Shall be the number of Requester-supported extended asymmetric key signature algorithms (=A) for the purpose of signature verification. `A` + `E` + `ExtAlgCount2` + `ExtAlgCount3` + `ExtAlgCount4` + `ExtAlgCount5` shall be less than or equal to 20. If the Requester does not support any request/response pair that requires signature verification, this value shall be set to zero. |
| 29                       | ExtHashCount              | 1               | Shall be the number of Requester-supported extended hashing algorithms (=E). `A` + `E` + `ExtAlgCount2` + `ExtAlgCount3` + `ExtAlgCount4` + `ExtAlgCount5` shall be less than or equal to 20. If the Requester does not support any request/response pair that requires hashing operations, this value shall be set to zero. |
| 30                       | Reserved                  | 1               | Reserved. |
| 31                       | MELspecification          | 1               | Shall be the bit mask.  The [Measurement Extension Log specification field format table](#table-me-bit-format) defines the format for this field. The Requester shall set the corresponding bit for each supported measurement extension log (MEL) specification. |
| 32                       | ExtAsym                   | 4 \* `A`        | Shall be the list of Requester-supported extended asymmetric key signature algorithms for the purpose of signature verification.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |
| 32 + 4 \* `A`            | ExtHash                   | 4 \* `E`        | Shall be the list of the extended hashing algorithms supported by Requester.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |
| 32 + 4 \* `A` + 4 \* `E` | ReqAlgStruct              | `AlgStructSize` | See the `AlgStructure` request field. |

`AlgStructSize` is the sum of the size of the following algorithm structure tables. The algorithm structure table shall be present only if the Requester supports that `AlgType`. `AlgType` shall monotonically increase for subsequent entries.

[Table 16 &mdash; Algorithm request structure](#table-algorithm-request-structure) shows the Algorithm request structure:

<a id="table-algorithm-request-structure"></a>**Table 16 &mdash; Algorithm request structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1      | Shall be the type of algorithm.<ul><li>0x00 and 0x01. Reserved.</li><li>0x02. DHE.</li><li>0x03.  `AEADCipherSuite`.</li><li>0x04. `ReqBaseAsymAlg`.</li><li>0x05. `KeySchedule`.</li><li>All other values reserved.</li></ul> |
| 1      | AlgCount           | 1      | Shall be the Requester-supported fixed algorithms.<ul><li>Bit [7:4]. Number of bytes required to describe Requester-supported SPDM-enumerated fixed algorithms (=FixedAlgCount). `FixedAlgCount` + 2 shall be a multiple of 4.</li><li>Bit [3:0]. Number of Requester-supported extended algorithms (=`ExtAlgCount`).</li></ul> |
| 2      | AlgSupported       | `FixedAlgCount` | Shall be the bit mask listing Requester-supported SPDM-enumerated algorithms. |
| 2 + FixedAlgCount  | AlgExternal | 4 \* `ExtAlgCount` | Shall be the list of Requester-supported extended algorithms.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

The following tables describe the Algorithm request structures mapped to their respective types:

* [Table 17 &mdash; DHE structure](#table-dhe-structure)
* [Table 18 &mdash; AEAD structure](#table-aead-structure)
* [Table 19 &mdash; ReqBaseAsymAlg structure](#table-reqbaseasymalg-structure)
* [Table 20 &mdash; KeySchedule structure](#table-keyschedule-structure)

<a id="table-dhe-structure"></a>**Table 17 &mdash; DHE structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1            | Shall be `0x02`=`DHE` |
| 1      | AlgCount           | 1            | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Number of Requester-supported extended DHE groups (=`ExtAlgCount2`).</li></ul> |
| 2      | AlgSupported       | 2            | Shall be the bit mask listing Requester-supported SPDM-enumerated Diffie-Hellman Ephemeral (DHE) groups. Values in parentheses specify the size of the corresponding public values associated with each group.<ul><li>Byte 0 Bit 0. [ffdhe2048](#ref_IETF_RFC7919) (D = 256).</li><li>Byte 0 Bit 1. [ffdhe3072](#ref_IETF_RFC7919) (D = 384).</li><li>Byte 0 Bit 2. [ffdhe4096](#ref_IETF_RFC7919) (D = 512).</li><li>Byte 0 Bit 3. [secp256r1](#ref_IETF_RFC8446) (D = 64, C = 32).</li><li>Byte 0 Bit 4. [secp384r1](#ref_IETF_RFC8446) (D = 96, C = 48).</li><li>Byte 0 Bit 5. [secp521r1](#ref_IETF_RFC8446) (D = 132, C = 66).</li><li>Byte 0 Bit 6. [SM2_P256 (Part 3 and Part 5 of GB/T 32918 specification)](#ref_gbt32918_3_2016) (D = 64, C = 32).</li><li>All other values reserved.</li></ul> |
| 4      | AlgExternal        | 4 \* `ExtAlgCount2` | Shall be the list of Requester-supported extended DHE groups.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-aead-structure"></a>**Table 18 &mdash; AEAD structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1            | Shall be the `0x03`=`AEAD` |
| 1      | AlgCount           | 1            | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Number of Requester-supported extended [*AEAD*](#aead) algorithms (=`ExtAlgCount3`).</li></ul> |
| 2      | AlgSupported       | 2            | Shall be the bit mask listing Requester-supported SPDM-enumerated AEAD algorithms.<ul><li>Byte 0 Bit 0. [AES-128-GCM](#gcm). 128-bit key; 96-bit IV (initialization vector); tag size is specified by transport layer.</li><li>Byte 0 Bit 1. [AES-256-GCM](#gcm). 256-bit key; 96-bit IV; tag size is specified by transport layer.</li><li>Byte 0 Bit 2. [CHACHA20_POLY1305](#chachapoly). 256-bit key; 96-bit IV; 128-bit tag.</li><li>Byte 0 Bit 3. [AEAD_SM4_GCM](#rfc8998). 128-bit key; 96-bit IV; tag size is specified by transport layer.</li><li>All other values reserved.</li></ul> |
| 4      | AlgExternal        | 4 \* `ExtAlgCount3` | Shall be the list of Requester-supported extended AEAD algorithms.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-reqbaseasymalg-structure"></a>**Table 19 &mdash; ReqBaseAsymAlg structure**

| Byte offset | Field            | Size (bytes)      | Description                |
|:------------|:-----------------|:-------------     |:---------------------------|
| 0           | AlgType          | 1                 | Shall be `0x04`=`ReqBaseAsymAlg` |
| 1           | AlgCount         | 1                 | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Number of Requester-supported extended asymmetric key signature algorithms for the purpose of signature generation (=`ExtAlgCount4`).</li></ul> |
| 2           | AlgSupported     | 2                 | Shall be the bit mask listing Requester-supported SPDM-enumerated asymmetric key signature algorithms for the purpose of signature generation. If the Requester does not support any request/response pair that requires signature generation, this value shall be set to zero.<ul><li>Byte 0 Bit 0. [TPM_ALG_RSASSA_2048](#signature-algorithm-references).</li><li>Byte 0 Bit 1. [TPM_ALG_RSAPSS_2048](#signature-algorithm-references).</li><li>Byte 0 Bit 2. [TPM_ALG_RSASSA_3072](#signature-algorithm-references).</li><li>Byte 0 Bit 3. [TPM_ALG_RSAPSS_3072](#signature-algorithm-references).</li><li>Byte 0 Bit 4. [TPM_ALG_ECDSA_ECC_NIST_P256](#signature-algorithm-references).</li><li>Byte 0 Bit 5. [TPM_ALG_RSASSA_4096](#signature-algorithm-references).</li><li>Byte 0 Bit 6. [TPM_ALG_RSAPSS_4096](#signature-algorithm-references).</li><li>Byte 0 Bit 7. [TPM_ALG_ECDSA_ECC_NIST_P384](#signature-algorithm-references).</li><li>Byte 1 Bit 0. [TPM_ALG_ECDSA_ECC_NIST_P521](#signature-algorithm-references).</li><li>Byte 1 Bit 1. [TPM_ALG_SM2_ECC_SM2_P256](#signature-algorithm-references).</li><li>Byte 1 Bit 2. [EdDSA ed25519](#signature-algorithm-references).</li><li>Byte 1 Bit 3. [EdDSA ed448](#signature-algorithm-references).</li><li>All other values reserved.</li></ul>For details of `SigLen` for each algorithm, see [Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format](#table-negotiate-algorithms-request-message-format). |
| 4           | AlgExternal      | 4 \* `ExtAlgCount4` | Shall be the list of Requester-supported extended asymmetric key signature algorithms for the purpose of signature generation.  [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-keyschedule-structure"></a>**Table 20 &mdash; KeySchedule structure**

| Byte offset | Field              | Size (bytes)      | Description                |
|:------------|:-----------------  |:-------------     |:---------------------------|
| 0           | AlgType            | 1                 | Shall be `0x05`=`KeySchedule` |
| 1           | AlgCount           | 1                 | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Number of Requester-supported extended key schedule algorithms (=`ExtAlgCount5`).</li></ul> |
| 2           | AlgSupported       | 2                 | Shall be the bit mask listing Requester-supported SPDM-enumerated key schedule algorithms.<ul><li>Byte 0 Bit 0. SPDM Key Schedule.</li><li>All other values reserved.</li></ul> |
| 4           | AlgExternal        | 4 \* `ExtAlgCount5` | Shall be the list of Requester-supported extended key schedule algorithms. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

[Table 21 &mdash; ALGORITHMS response message format](#table-successful-algorithms-response-message-format) shows the `ALGORITHMS` response message format.

<a id="table-successful-algorithms-response-message-format"></a>**Table 21 &mdash; Successful ALGORITHMS response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0                          | SPDMVersion                  | 1               | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1                          | RequestResponseCode          | 1               | Shall be `0x63`=`ALGORITHMS`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2                          | Param1                       | 1               | Shall be the number of algorithm structure tables in this response using `RespAlgStruct`. |
| 3                          | Param2                       | 1               | Reserved. |
| 4                          | Length                       | 2               | Shall be the length of the response message, in bytes. |
| 6                          | MeasurementSpecificationSel  | 1               | Bit mask.  The Responder shall select one of the measurement specifications supported by the Requester and Responder.  Thus, no more than one bit shall be set. The [Measurement specification field format table](#table-ms-bit-format) defines the format for this field. |
| 7                          | OtherParamsSelection         | 1               | Shall be the selected Parameter Bit Mask. The Responder shall select one of the opaque data formats supported by the Requester. Thus, no more than one bit shall be set for the opaque data format.<ul><li>Bit [3:0]. See [Opaque Data Format Support and Selection Table](#table-odfs-selection).</li><li>Bit 4 - This field shall be the `RequesterMultiKeyConnSel` as [Multiple Asymmetric Key Negotiation](#multiple-asymmetric-key-negotiation) describes.</li><li>Bit [7:5]. Reserved.</li></ul> |
| 8                          | MeasurementHashAlgo          | 4               | Shall be the bit mask indicating the SPDM-enumerated hashing algorithms used for measurements.<ul><li>Byte 0 Bit 0. Raw Bit Stream Only.</li><li>Byte 0 Bit 1. [TPM_ALG_SHA_256](#TCG-algorithm-registry).</li><li>Byte 0 Bit 2. [TPM_ALG_SHA_384](#TCG-algorithm-registry).</li><li>Byte 0 Bit 3. [TPM_ALG_SHA_512](#TCG-algorithm-registry).</li><li>Byte 0 Bit 4. [TPM_ALG_SHA3_256](#TCG-algorithm-registry).</li><li>Byte 0 Bit 5. [TPM_ALG_SHA3_384](#TCG-algorithm-registry).</li><li>Byte 0 Bit 6. [TPM_ALG_SHA3_512](#TCG-algorithm-registry).</li><li>Byte 0 Bit 7. [TPM_ALG_SM3_256](#TCG-algorithm-registry).</li><li>If the Responder supports measurements (`MEAS_CAP=01b` or `MEAS_CAP=10b` in its `CAPABILITIES` response) and if `MeasurementSpecificationSel` is non-zero, then exactly one bit in this bit field shall be set. Otherwise, the Responder shall set this field to `0`.</li><li>All other values reserved.</li></ul>A Responder shall select bit 0 only if it supports raw bit streams as the only form of measurement; otherwise, the Responder shall select one of the other bits. |
| 12                         | BaseAsymSel                  | 4               | Shall be the bit mask indicating the SPDM-enumerated asymmetric key signature algorithm selected for the purpose of signature generation. If the Responder does not support any request/response pair that requires signature generation, this value shall be set to zero. The Responder shall set no more than one bit. |
| 16                         | BaseHashSel                  | 4               | Shall be the bit mask indicating the SPDM-enumerated hashing algorithm selected. If the Responder does not support any request/response pair that requires hashing operations, this value shall be set to zero. The Responder shall set no more than one bit. |
| 20                         | Reserved                     | 11              | Reserved. |
| 31                         | MELspecificationSel          | 1               | Shall be the bit mask indicating MEL.  The Responder shall select one of the MEL specifications supported by the Requester and Responder. No more than one bit shall be set. The [Measurement Extension Log specification field format table](#table-me-bit-format) defines the format for this field. |
| 32                         | ExtAsymSelCount              | 1               | Shall be the number of extended asymmetric key signature algorithms selected for the purpose of signature generation. Shall be either `0` or `1` (=A'). If the Responder does not support any request/response pair that requires signature generation, this value shall be set to zero. |
| 33                         | ExtHashSelCount              | 1               | Shall be the number of extended hashing algorithms selected.  Shall be either `0` or `1` (=E'). If the Responder does not support any request/response pair that requires hashing operations, this value shall be set to zero. |
| 34                         | Reserved                     | 2               | Reserved. |
| 36                         | ExtAsymSel                   | 4 \* `A'`       | Shall be the extended asymmetric key signature algorithm selected for the purpose of signature generation. The Responder shall use this asymmetric signature algorithm for all subsequent applicable response messages to the Requester.  The [extended algorithm field format table](#table-extended-algorithm-field-format) describes the format of this field. |
| 36 + 4 \* `A'`             | ExtHashSel                   | 4 \* `E'`       | Shall be the extended hashing algorithm selected.  The Responder shall use this hashing algorithm during all subsequent response messages to the Requester.  The Requester shall use this hashing algorithm during all subsequent applicable request messages to the Responder.  The [extended algorithm field format table](#table-extended-algorithm-field-format) describes the format of this field. |
| 36 + 4 \* `A'` + 4 \* `E'` | RespAlgStruct                | `AlgStructSize` | See [Table 22 &mdash; Response AlgStructure field format](#table-response-algstructure-field-format). |

`AlgStructSize` is the sum of the sizes of all the algorithm structure tables, as the following tables show.  An algorithm structure table needs to be present only if the Responder supports that `AlgType`. `AlgType` shall monotonically increase for subsequent entries.

<a id="table-response-algstructure-field-format"></a>**Table 22 &mdash; Response AlgStructure field format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0                   | AlgType            | 1                 | Shall be the type of algorithm.<ul><li>0x00 and 0x01. Reserved.</li><li>0x02. DHE.</li><li>0x03. `AEADCipherSuite`.</li><li>0x04. `ReqBaseAsymAlg`.</li><li>0x05. `KeySchedule`.</li><li>All other values reserved.</li></ul> |
| 1                   | AlgCount           | 1                 | Shall be the bit mask listing Responder-supported fixed algorithm requested by the Requester.<ul><li>Bit [7:4]. Number of bytes required to describe Requester-supported SPDM-enumerated fixed algorithms (=FixedAlgCount). `FixedAlgCount` + 2 shall be a multiple of 4.</li><li>Bit [3:0]. Number of Requester-supported, Responder-selected, extended algorithms (=`ExtAlgCount'`). This value shall be either 0 or 1.</li></ul> |
| 2                   | AlgSupported       | `FixedAlgCount`   | Shall be the bit mask for indicating a Requester-supported, Responder-selected, SPDM-enumerated algorithm. Responder shall set at most one bit to 1. |
| 2 + `FixedAlgCount` | AlgExternal        | 4 \* `ExtAlgCount'` | If present: shall be a Requester-supported, Responder-selected, extended algorithm.  Responder shall select at most one extended algorithm. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

The following tables describe the algorithm types and their associated fixed fields:

* [Table 23 &mdash; DHE structure](#table-dhe-structure-2)
* [Table 24 &mdash; AEAD structure](#table-aead-structure-2)
* [Table 25 &mdash; ReqBaseAsymAlg structure](#table-reqbaseasymalg-structure-2)
* [Table 26 &mdash; KeySchedule structure](#table-keyschedule-structure-2)
* [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format)

<a id="table-dhe-structure-2"></a>**Table 23 &mdash; DHE structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1                  | Shall be `0x02`=`DHE` |
| 1      | AlgCount           | 1                  | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Shall be the number of Requester-supported, Responder-selected, extended DHE groups (=`ExtAlgCount2'`). This value shall be either 0 or 1.</li></ul> |
| 2      | AlgSupported       | 2                  | Shall be the bit mask for indicating a Requester-supported, Responder-selected, SPDM-enumerated DHE group. Values in parentheses specify the size of the corresponding public values associated with each group.<ul><li> Byte 0 Bit 0. [ffdhe2048](#ref_IETF_RFC7919) (D = 256).</li><li>Byte 0 Bit 1. [ffdhe3072](#ref_IETF_RFC7919) (D = 384).</li><li>Byte 0 Bit 2. [ffdhe4096](#ref_IETF_RFC7919) (D = 512).</li><li>Byte 0 Bit 3. [secp256r1](#ref_IETF_RFC8446) (D = 64, C = 32)</li><li>Byte 0 Bit 4. [secp384r1](#ref_IETF_RFC8446) (D = 96, C = 48).</li><li>Byte 0 Bit 5. [secp521r1](#ref_IETF_RFC8446) (D = 132, C = 66).</li><li>Byte 0 Bit 6. [SM2_P256 (Part 3 and Part 5 of GB/T 32918)](#ref_gbt32918_3_2016) (D = 64, C = 32).</li><li>All other values reserved.</li></ul> |
| 4      | AlgExternal        | 4 \* `ExtAlgCount2'` | If present: shall be a Requester-supported, Responder-selected, extended DHE algorithm. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-aead-structure-2"></a>**Table 24 &mdash; AEAD structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1                  | Shall be `0x03`=`AEAD` |
| 1      | AlgCount           | 1                  | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Shall be the number of Requester-supported, Responder-selected, extended AEAD algorithms (=`ExtAlgCount3'`). This value shall be either 0 or 1. |
| 2      | AlgSupported       | 2                  | Shall be the bit mask for indicating a Requester-supported, Responder-selected, SPDM-enumerated AEAD algorithm.<ul><li>Byte 0 Bit 0. [AES-128-GCM](#TCG-algorithm-registry).</li><li>Byte 0 Bit 1. [AES-256-GCM](#TCG-algorithm-registry).</li><li>Byte 0 Bit 2. [CHACHA20_POLY1305](#TCG-algorithm-registry).</li><li>Byte 0 Bit 3. [AEAD_SM4_GCM](#rfc8998).</li><li>All other values reserved.</li></ul> |
| 4      | AlgExternal        | 4 \* `ExtAlgCount3'` | If present: shall be a Requester-supported, Responder-selected, extended AEAD algorithm. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-reqbaseasymalg-structure-2"></a>**Table 25 &mdash; ReqBaseAsymAlg structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1                  | Shall be `0x04`=`ReqBaseAsymAlg` |
| 1      | AlgCount           | 1                  | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Number of Requester-supported, Responder-selected, extended asymmetric key signature algorithms (=`ExtAlgCount4'`) for the purpose of signature verification. This value shall be either 0 or 1.</li></ul> |
| 2      | AlgSupported       | 2                  | Shall be the bit mask for indicating a Requester-supported, Responder-selected, SPDM-enumerated asymmetric key signature algorithm for the purpose of signature verification. If the Responder does not support any request/response pair that requires signature verification, this value shall be set to zero. If the Responder will not send any messages that require a signature, this value should be set to zero.<ul><li>Byte 0 Bit 0. [TPM_ALG_RSASSA_2048](#TCG-algorithm-registry).</li><li>Byte 0 Bit 1. [TPM_ALG_RSAPSS_2048](#TCG-algorithm-registry).</li><li>Byte 0 Bit 2. [TPM_ALG_RSASSA_3072](#TCG-algorithm-registry).</li><li>Byte 0 Bit 3. [TPM_ALG_RSAPSS_3072](#TCG-algorithm-registry).</li><li>Byte 0 Bit 4. [TPM_ALG_ECDSA_ECC_NIST_P256](#TCG-algorithm-registry).</li><li>Byte 0 Bit 5. [TPM_ALG_RSASSA_4096](#TCG-algorithm-registry).</li><li>Byte 0 Bit 6. [TPM_ALG_RSAPSS_4096](#TCG-algorithm-registry).</li><li>Byte 0 Bit 7. [TPM_ALG_ECDSA_ECC_NIST_P384](#TCG-algorithm-registry).</li><li>Byte 1 Bit 0. [TPM_ALG_ECDSA_ECC_NIST_P521](#TCG-algorithm-registry).</li><li>Byte 1 Bit 1. [TPM_ALG_SM2_ECC_SM2_P256](#TCG-algorithm-registry).</li><li>Byte 1 Bit 2. [EdDSA ed25519](#rfc8032).</li><li>Byte 1 Bit 3. [EdDSA ed448](#rfc8032).</li><li>All other values reserved.</li></ul>For details of `SigLen` for each algorithm, see [Table 15 &mdash; NEGOTIATE_ALGORITHMS request message format](#table-negotiate-algorithms-request-message-format). |
| 4      | AlgExternal        | 4 \* `ExtAlgCount4'` | If present: shall be a Requester-supported, Responder-selected extended asymmetric key signature algorithm for the purpose of signature verification. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-keyschedule-structure-2"></a>**Table 26 &mdash; KeySchedule structure**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | AlgType            | 1                  | Shall be `0x05`=`KeySchedule`    |
| 1      | AlgCount           | 1                  | <ul><li>Bit [7:4]. Shall be a value of 2.</li><li>Bit [3:0]. Shall be the number of Requester-supported, Responder-selected, extended key schedule algorithms (=`ExtAlgCount5'`).  This value shall be either 0 or 1.</li></ul> |
| 2      | AlgSupported       | 2                  | Shall be the bit mask for indicating a Requester-supported, Responder-selected, SPDM-enumerated key schedule algorithm.<ul><li>Byte 0 Bit 0. SPDM key schedule.</li><li>All other values reserved.</li></ul> |
| 4      | AlgExternal        | 4 \* `ExtAlgCount5'` | If present: shall be a Requester-supported, Responder-selected, extended key schedule algorithm. [Table 27 &mdash; Extended Algorithm field format](#table-extended-algorithm-field-format) describes the format of this field. |

<a id="table-extended-algorithm-field-format"></a>**Table 27 &mdash; Extended Algorithm field format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | Registry ID   | 1 | Shall represent the registry or standards body.  The **ID** column of [Table 60 &mdash; Registry or standards body ID](#table-registry-or-standards-body-id) describes the value of this field. |
| 1      | Reserved      | 1 | Reserved.  |
| 2      | Algorithm ID  | 2 | Shall indicate the desired algorithm.  The registry or standards body owns the value of this field.  See [Table 60 &mdash; Registry or standards body ID](#table-registry-or-standards-body-id). At present, DMTF does not define any algorithms for use in extended algorithms fields. |

<a id="table-odfs-selection"></a>**Table 28 &mdash; Opaque Data Format Support and Selection**

| Bit offset | Field          | Description |
|:-----------|:---------------|:------------|
| 0          | OpaqueDataFmt0 | If set, this bit shall indicate that the format for all `OpaqueData` fields in this specification is defined by the device vendor or other standards body. |
| 1          | OpaqueDataFmt1 | If set, this bit shall indicate that the format for all `OpaqueData` fields in this specification is defined by the [General opaque data format](#general-opaque-data-format).
| [3:2]      | Reserved       | Reserved. |

The Opaque Data Format Selection Table shows the bit definition for the format of the Opaque data fields. A Requester may set more than one bit in the table to indicate each supported format. A Responder shall select no more than one of the bits supported by the Requester in this table. If the Requester or the Responder does not set a bit, then all `OpaqueData` fields in this specification shall be absent by setting the respective `OpaqueDataLength` field to a value of zero.

<a id="table-ms-bit-format"></a>**Table 29 &mdash; Measurement Specification Field Format**

| Bit offset | Field        | Description |
|:-----------|:-------      |:------------|
| 0          | DMTFmeasSpec | This bit shall indicate a DMTF-defined measurement specification. [Table 54 &mdash; DMTF measurement specification format](#table-dmtf-measurement-specification-format) defines the format for this measurement specification. |
| [1:7]      | Reserved     | Reserved |

The Measurement Specification Field Format Table describes the field format for Measurement specification related fields. The selected measurement specification (`MeasurementSpecificationSel`) is used in the `MEASUREMENTS` response. See [Measurement block](#measurement-block) and `GET_MEASUREMENTS` for details.

<a id="table-me-bit-format"></a>**Table 30 &mdash; Measurement Extension Log Specification Field Format**

| Bit offset | Field        | Description |
|:-----------|:-------      |:------------|
| 0          | DMTFmelSpec  | This bit indicates a DMTF-defined measurement extension log specification. Refer to the [DMTF Measurement Extension Log Format](#dmtf-measurement-extension-log-format) clause for details. If the Requester supports the DMTF-defined measurement extension log specification, it shall set this bit to 1 in `MELspecification`. If the Responder selects the DMTF-defined measurement extension log specification for constructing the MEL, it shall set this bit to 1 in `MELspecificationSel`. |
| [1:7]      | Reserved     | Reserved    |

The Measurement Extension Log Specification Field Format Table describes the field format for MEL specification related fields. The selected MEL specification (`MELspecificationSel`) is used in construction of the MEL.

### Connection behavior after VCA

With the successful completion of the `ALGORITHMS` message, all the parameters of the SPDM connection have been determined. Thus, all SPDM message exchanges after the VCA messages shall comply with the selected parameters in the `ALGORITHMS` message, with the exception of `GET_VERSION` and `VERSION` messages, or unless otherwise stated in this specification. To explain this behavior, suppose a Responder supports both RSA and ECDSA asymmetric algorithms. For an SPDM connection, the Responder selects the `TPM_ALG_RSASSA_2048` asymmetric algorithm in `BaseAsymSel` and the `TPM_ALG_SHA_256` hash algorithm in `BaseHashSel`. If the Requester on that same connection issues `GET_DIGESTS`, the Responder returns `TPM_ALG_SHA_256` digests only for those populated slots that can provide a `TPM_ALG_RSASSA_2048` signature for a `CHALLENGE_AUTH` response. The Responder would violate this requirement if it returns one or more digests of populated slots that perform ECDSA signatures or if it uses a different hash algorithm to create the digests.

Unless otherwise stated in this specification, and with the exception of `GET_VERSION`, if a Requester issues a request that violates one or more of the negotiated or selected parameters of a given connection, the Responder shall either silently discard the request or return an `ERROR` message with an appropriate error code.

## Responder identity authentication

This clause describes request messages and response messages associated with the identity of the Responder's authentication operations. The `GET_DIGESTS` and `GET_CERTIFICATE` messages shall be supported by a Responder that returns `CERT_CAP=1` in its `CAPABILITIES` response message. The `CHALLENGE` message that this clause defines shall be supported by a Responder that returns `CHAL_CAP=1` in its `CAPABILITIES` response message. The `GET_DIGESTS` and `GET_CERTIFICATE` messages are not applicable if the public key of the Responder was provisioned to the Requester in a trusted environment.

[Figure 8 &mdash; Responder authentication: Example certificate retrieval flow](#figure-responder-authentication-example-certificate-retrieval-flow) shows the high-level request-response message flow and sequence for [*certificate*](#certificate) retrieval.

<a id="figure-responder-authentication-example-certificate-retrieval-flow"></a>**Figure 8 &mdash; Responder authentication: Example certificate retrieval flow**

![Figure 8 &mdash; Responder authentication: Example certificate retrieval flow](SPDMSpecification_files/Figure-EndpointAuthenticationExampleCertificateRetrievalFlow.svg)

The `GET_DIGESTS` request message and `DIGESTS` response message can optimize the amount of data required to be transferred from the Responder to the Requester, due to the potentially large size of a certificate chain.  The cryptographic hash values of every certificate chain stored on an endpoint are returned with the `DIGESTS` response message, enabling the Requester to compare these values to previously retrieved and cached certificate chain hash values and detect any changes to the certificate chains stored on the device before issuing a `GET_CERTIFICATE` request message.

For the runtime challenge-response flow, the signature field in the `CHALLENGE_AUTH` response message payload shall be signed by using the private key associated with the leaf certificate over the hash of the message transcript. See [Table 47 &mdash; Request ordering and message transcript computation rules for M1/M2](#table-m1-construction).

This ensures cryptographic binding between a specific request message from a specific Requester and a specific response message from a specific Responder, which enables the Requester to detect the presence of an active adversary attempting to downgrade cryptographic algorithms or SPDM versions.

Furthermore, a Requester-generated [*nonce*](#nonce) protects the challenge-response from replay attacks, whereas a Responder-generated nonce prevents the Responder from signing over arbitrary data that the Requester dictates.  The message transcript generation for the signature computation is restarted as of the most recent `GET_VERSION` request received.

## Requester identity authentication

If a Requester supports mutual authentication, it shall comply with all requirements placed on a Responder as specified in [Responder identity authentication](#responder-identity-authentication).

If a Responder supports mutual authentication, it shall comply with all requirements placed on a Requester as specified in [Responder identity authentication](#responder-identity-authentication). The preceding two statements essentially describe a role reversal.

### Certificates and certificate chains

Each SPDM endpoint that supports identity authentication using certificates shall carry at least one complete certificate chain.  A certificate chain contains an ordered list of certificates, presented as the binary (byte) concatenation of the fields that [Table 33 &mdash; Certificate chain format](#table-certificate-chain-format) shows. In the context of this specification, a complete certificate chain is one where: (i) the first certificate either is signed by a Root Certificate (a certificate that specifies a trust anchor) or is a Root Certificate itself, (ii) each subsequent certificate is signed by the preceding certificate, and (iii) the final certificate contains the public key used to authenticate the SPDM endpoint. The final certificate is called the [*leaf certificate*](#leaf-certificate-term).

If an SPDM endpoint does not support multiple asymmetric keys (`MULTI_KEY_CAP=0`), the SPDM endpoint shall contain a single public-private key pair per supported algorithm for its leaf certificates, regardless of how many certificate chains are stored on the device. The Responder selects a single asymmetric key signature algorithm per Requester regardless of the value of `MULTI_KEY_CAP` field.

Certificate chains are stored in logical locations called *slots*.  Each supported slot shall either be empty or contain one complete certificate chain.  A device shall not contain more than eight slots. Slots are numbered 0 through 7 inclusive.  Slot 0 is populated by default.  If a device uses the `DeviceCert` model (`ALIAS_CERT_CAP=0b` in its `CAPABILITIES` response) and if `MULTI_KEY_CAP` is not set, then the certificate chain in every populated slot shall use the `DeviceCert` model. If a device uses the `AliasCert` model (`ALIAS_CERT_CAP=1b` in its `CAPABILITIES` response) and if `MULTI_KEY_CAP` is not set, then the certificate chain in every populated slot shall use the `AliasCert` model.

If the `MULTI_KEY_CAP` is set, the certificate model for each populated certificate slot can be different. Multiple asymmetric key support allows the use of the generic certificate model. The use of the `GenericCert` model shall be prohibited when `MULTI_KEY_CAP` is not set.

In all cases, the certificate model for slot 0 shall be either the device certificate model or the alias certificate model.

Additional slots may be populated through the supply chain such as by a platform integrator or by an end user such as an IT administrator.  A slot mask identifies the certificate chains in the eight slots. Similarly, if the Requester supports mutual authentication and if `MULTI_KEY_CONN_REQ` is not set, a Requester device shall use either the `DeviceCert` model or the `AliasCert` model and the certificate chain in every populated slot shall use the same model. Note that the Requester does not have capability flags to indicate the certificate model.

If an endpoint supports certificates, then Slot 0 is the default certificate chain slot. Slot 0 shall contain a valid certificate chain unless the device has not yet had a certificate chain provisioned and is in a trusted environment.

Each certificate in a chain shall be in ASN.1 DER-encoded [X.509](#ref_x509) v3 format as [RFC 5280](#ref_x509) defines.  The ASN.1 DER encoding of each individual certificate can be analyzed to determine its length.

To allow for flexibility in supporting multiple certificate models, the minimum number of certificates within a certificate chain shall be one and a chain shall contain a leaf certificate.

The leaf certificate in the device certificate model shall be the `DeviceCert` leaf certificate. The leaf certificate in an alias certificate model shall be the `AliasCert` leaf certificate. In a generic certificate model, the leaf certificate shall be the `GenericCert` leaf certificate. When `MULTI_KEY_CAP` is not set and a certificate chain consists of a single certificate, that certificate can only be a `DeviceCert` leaf certificate. When `MULTI_KEY_CAP` is set and a certificate chain consists of a single certificate, that certificate is either a `DeviceCert` or a `GenericCert` leaf certificate.

[Table 33 &mdash; Certificate chain format](#table-certificate-chain-format) describes the certificate chain format:

<a id="table-certificate-chain-format"></a>**Table 33 &mdash; Certificate chain format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | Length       | 2            | Shall be the total length of the certificate chain, in bytes, including all fields in this table.  This field is little endian. |
| 2      | Reserved     | 2            | Reserved. |
| 4      | RootHash     | `H`            | Shall be the digest of the Root Certificate. Note that the Root Certificate is ASN.1 DER-encoded for this digest. This field shall be in [hash byte order](#hash-byte-order). `H` is the output size, in bytes, of the hash algorithm selected by the most recent `ALGORITHMS` response. |
| 4 + `H`  | Certificates | `Length` - (4 + `H`) | Shall be a [complete](#certificates-and-certificate-chains) certificate chain consisting of one or more ASN.1 DER-encoded [X.509](#ref_x509) v3 certificates. This field shall be in [Encoded ASN.1 byte order](#encoded-asn1-byte-order). |

## GET_CERTIFICATE request and CERTIFICATE response messages

This request message shall retrieve the certificate chain from the specified slot number.

[Table 38 &mdash; GET_CERTIFICATE request message format](#table-get-certificate-request-message-format) shows the `GET_CERTIFICATE` request message format.

[GET_CERTIFICATE request attributes](#table-certificate-request-attributes) shows the `GET_CERTIFICATE` request attributes.

[Table 40 &mdash; Successful CERTIFICATE response message format](#table-successful-certificate-response-message-format) shows the `CERTIFICATE` response message format.

[Table 141 &mdash; CERTIFICATE response attributes](#table-craf) shows the `CERTIFICATE` response attributes.

The Requester sends one or more `GET_CERTIFICATE` requests to retrieve the certificate chain of the Responder.

<a id="table-get-certificate-request-message-format"></a>**Table 38 &mdash; GET_CERTIFICATE request message format**

| Byte offset | Field               | Size (bytes) | Description                |
|:------------|:--------------------|:-------------|:---------------------------|
| 0           | SPDMVersion         | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1           | RequestResponseCode | 1            | Shall be `0x82`=`GET_CERTIFICATE`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2           | Param1              | 1            | Bit [7:4]. Reserved. </br></br> Bit [3:0]. Shall be the `SlotID`.  Slot number of the Responder certificate chain to read.  The value in this field shall be between 0 and 7 inclusive. |
| 3           | Param2              | 1            | Request attributes.<br/>See [GET_CERTIFICATE request attributes](#table-certificate-request-attributes). |
| 4           | Offset              | 2            | Shall be the offset in bytes from the start of the certificate chain to where the read request message begins. The Responder shall send its certificate chain starting from this offset. For the first `GET_CERTIFICATE` request for a given slot, the Requester shall set this field to 0. For subsequent requests, `Offset` is set to the next portion of the certificate in that slot. |
| 6           | Length              | 2            | Shall be the length of certificate chain data, in bytes, to be returned in the corresponding response. This field is an unsigned 16-bit integer. |

<a id="table-certificate-request-attributes"></a>**Table 39 &mdash; GET_CERTIFICATE request attributes**

| Bit offset | Field            | Description                                           |
|:-----------|:-----------------|:------------------------------------------------------|
| 0          | SlotSizeRequested| When `SlotSizeRequested=1b` in the `GET_CERTIFICATE` request, the Responder shall return the number of bytes available for certificate chain storage in the `RemainderLength` field of the response. When `SlotSizeRequested=1b`, the `Offset` and `Length` fields in the `GET_CERTIFICATE` request shall be ignored by the Responder. |
| [7:1]      | Reserved         | Reserved. |

<a id="table-successful-certificate-response-message-format"></a>**Table 40 &mdash; Successful CERTIFICATE response message format**

| Byte offset | Field               | Size (bytes)         | Description                |
|:------------|:-----------------   |:-------------        |:---------------------------|
| 0           | SPDMVersion         | 1                    | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1           | RequestResponseCode | 1                    | Shall be `0x02`=`CERTIFICATE`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2           | Param1              | 1                    | Bit [7:4]. Reserved. </br></br> Bit [3:0]. Shall be the `SlotID`. Slot number of the certificate chain returned. |
| 3           | Param2              | 1                    | The format of this field shall be the format that [Table 141 &mdash; CERTIFICATE response attributes](#table-craf) defines. |
| 4           | PortionLength       | 2                    | Shall be the number of bytes of this portion of the certificate chain.  This should be less than or equal to `Length` received as part of the request.  For example, the Responder might set this field to a value less than `Length` received as part of the request due to limitations on the transmit buffer of the Responder. If the requested `Length` field is `0` then this field shall be set to 0. If `SlotSizeRequested=1b` in the request, this field shall be set to zero. |
| 6           | RemainderLength     | 2                    | Shall be the number of bytes of the certificate chain that have not been sent yet, after the current response.  For the last response, this field shall be 0 as an indication to the Requester that the entire certificate chain has been sent. If the requested `Length` field is `0` and `SlotSizeRequested=0b` in the request, then this field shall return the actual size of the certificate chain in the slot. See [Table 39 &mdash; GET_CERTIFICATE request attributes](#table-certificate-request-attributes) for more detail. |
| 8           | CertChain           | `PortionLength` or 0 | Shall be the requested contents of the target certificate chain, as described in [Certificates and certificate chains](#certificates-and-certificate-chains). If `SlotSizeRequested=1b` in the request, this field shall be absent. If the requested `Length` field is `0`, then this field shall be absent.|

<a id="table-craf"></a>**Table 41 &mdash; CERTIFICATE response attributes**

| Bit offset     | Field           | Description |
|:---------      |:-----           |:----  |
| [2:0]          | CertificateInfo | The value of this field shall be the certificate model of the slot. The format of this field shall be the format of the `CertModel` field that the [certificate info table](#table-cert-info) defines. |
| All other bits | Reserved        | Reserved. |

[Figure 9 &mdash; Responder cannot return full length data flow](#figure-responder-cannot-return-full-length-data-flow) shows the high-level request-response message flow when the Responder cannot return the entire data requested by the Requester in the first response.

<a id="figure-responder-cannot-return-full-length-data-flow"></a>**Figure 9 &mdash; Responder cannot return full length data flow**

![Figure 9 &mdash; Responder cannot return full length data flow](SPDMSpecification_files/Figure-RequestedInfoTooLong-Protocol.svg)

Endpoints that support the [large SPDM message transfer mechanism](#large-spdm-message-transfer-mechanism) message set shall use the large SPDM message transfer mechanism messages to manage the transfer of the requested certificate chain when the `CERTIFICATE` response is larger than either the `DataTransferSize` of the Requester or the transmit buffer of the Responder. Specifically:

* If the Requester sets `Offset` to `0` and `Length` to `0xFFFF` in the `GET_CERTIFICATE` request, the Responder shall set `PortionLength` equal to the size of the complete certificate chain stored in the requested slot, shall set `RemainderLength` to `0`, and shall store the contents of the complete certificate chain in `CertChain` in the `CERTIFICATE` response. Then the Responder shall fragment and return this response message in chunks, as per the clauses presented in [`CHUNK_GET` request and `CHUNK_RESPONSE` response message](#chunk_get-request-and-chunk_response-response-message). In this case, the Responder shall not return a partial certificate chain.

By setting `SlotSizeRequested=1b` in the request attributes, the Requester can query the size of the Responder's certificate slot. The Requester should query the slot size before any action that uses slot storage, because the Responder might change the value of the slot size based on other actions.

### Mutual authentication requirements for GET_CERTIFICATE and CERTIFICATE messages

If the Requester supports mutual authentication, the requirements placed on the Responder in [GET_CERTIFICATE request and CERTIFICATE response messages](#get_certificate-request-and-certificate-response-messages) clause shall also apply to the Requester. If the Responder supports mutual authentication, the requirements placed on the Requester in the [GET_CERTIFICATE request and CERTIFICATE response messages](#get_certificate-request-and-certificate-response-messages) clauses shall also apply to the Responder. The preceding two sentences essentially describe a role reversal.

## KEY_EXCHANGE request and KEY_EXCHANGE_RSP response messages

This request message shall initiate a handshake between Requester and Responder intended to authenticate the Responder (or, optionally, both parties), negotiate cryptographic parameters (in addition to those negotiated in the last `NEGOTIATE_ALGORITHMS`/`ALGORITHMS` exchange), and establish shared keying material.<br/><br/>[Table 69 &mdash; KEY_EXCHANGE request message format](#table-key-exchange-request-message-format) shows the `KEY_EXCHANGE` request message format, and [Table 71 &mdash; Successful KEY_EXCHANGE_RSP response message format](#table-successful-key-exchange-rsp-response-message-format) shows the `KEY_EXCHANGE_RSP` response message format. The handshake is completed by the successful exchange of the `FINISH` request and `FINISH_RSP` response messages presented in the next clause. The handshake depends on the tight coupling between these two request/response message pairs.

The Requester-Responder pair can support two modes of handshakes. If `HANDSHAKE_IN_THE_CLEAR_CAP` is set in both the Requester and the Responder, all SPDM messages exchanged during the Session Handshake Phase are sent in the clear (outside of a secure session). Otherwise both the Requester and the Responder use encryption and/or message authentication during the Session Handshake Phase using the Handshake secret derived at the completion of the `KEY_EXCHANGE_RSP` message for subsequent message communication until the completion of the `FINISH_RSP` message.

[Figure 15 &mdash; Responder authentication key exchange example](#figure-responder-authentication-key-exchange-example) shows an example of a Responder authentication key exchange:

<a id="figure-responder-authentication-key-exchange-example"></a>**Figure 15 &mdash; Responder authentication key exchange example**

![Figure 15 &mdash; Responder authentication key exchange example](SPDMSpecification_files/Figure_Responder-Only_Authentication_flow.svg)

[Figure 16 &mdash; Responder authentication multiple key exchange example](#figure-responder-authentication-multiple-key-exchange-example) shows an example of multiple sessions using two independent sets of root session keys that coexist at the same time. When `HANDSHAKE_IN_THE_CLEAR_CAP`=`0` for both Requester and Responder, the specification does not require a specific temporal relationship between the second `KEY_EXCHANGE` request message and the first `FINISH_RSP` response message. However, to simplify implementation, a Responder might respond with an `ERROR` message of `ErrorCode=Busy` to the second `KEY_EXCHANGE` request message until the first `FINISH_RSP` response message is complete. If the handshake is performed in the clear (that is, if `HANDSHAKE_IN_THE_CLEAR_CAP`=`1` for both Requester and Responder), a Requester shall not send a second `KEY_EXCHANGE` request message until the first `FINISH_RSP` response message is received. A Responder shall respond with an `ERROR` message of `ErrorCode=UnexpectedRequest` if it receives a second `KEY_EXCHANGE` request message before the first `FINISH` request is received.

<a id="figure-responder-authentication-multiple-key-exchange-example"></a>**Figure 16 &mdash; Responder authentication multiple key exchange example**

![Figure 16 &mdash; Responder authentication multiple key exchange example](SPDMSpecification_files/Figure-SPDM-messaging-multisession-protocol-flow.svg)

The handshake includes an ephemeral Diffie-Hellman (DHE) key exchange in which the Requester and Responder each generate an ephemeral (that is, temporary) Diffie-Hellman key pair and exchange the public keys of those key pairs in the `ExchangeData` fields of the `KEY_EXCHANGE` request message and `KEY_EXCHANGE_RSP` response message. The Responder generates a DHE secret by using the private key of the DHE key pair of the Responder and the public key of the DHE key pair of the Requester provided in the `KEY_EXCHANGE` request message. Similarly, the Requester generates a DHE secret by using the private key of the DHE key pair of the Requester and the public key of the DHE key pair of the Responder provided in the `KEY_EXCHANGE_RSP` response message. The DHE secrets are computed as specified in clause 7.4 of [RFC 8446](#ref_IETF_RFC8446). Assuming that the public keys were received correctly, both the Requester and Responder generate identical DHE secrets from which session secrets are generated.

Diffie-Hellman group parameters are determined by the DHE group in use, which is selected in the most recent `ALGORITHMS` response. The contents of the `ExchangeData` field are computed as specified in clause 4.2.8 of [RFC 8446](#ref_IETF_RFC8446). Specifically, if the DHE key exchange is based on finite-fields (FFDHE), the `ExchangeData` field in `KEY_EXCHANGE` and `KEY_EXCHANGE_RSP` shall contain the computed public value (Y = g^X mod p) for the specified group (see [Table 17 &mdash; DHE structure](#table-dhe-structure) for group definitions) encoded as a big-endian integer and padded to the left with zeros to the size of p in bytes. If the key exchange is based on elliptic curves (ECDHE), the `ExchangeData` field in `KEY_EXCHANGE` and `KEY_EXCHANGE_RSP` shall contain the serialization of X and Y, which are the binary representations of the x and y values respectively in network byte order, padded on the left by zeros if necessary. The size of each number representation occupies as many octets as are implied by the curve parameters selected. Specifically, X is [0: C - 1] and Y is [C : D - 1], where C and D are determined by the group (see [Table 17 &mdash; DHE structure](#table-dhe-structure)).

For SM2_P256 key exchange, the identifiers ID<sub>A</sub> and ID<sub>B</sub> that the [GB/T 32918.3-2016](#ref_gbt32918_3_2016) specification defines are needed to derive the shared secret. If this algorithm is selected, the ID for the Requester (that is, ID<sub>A</sub>) shall be the concatenation of "Requester-KEP-dmtf-spdm-v" and `SPDMversionString`. Likewise, the ID for the Responder (that is, ID<sub>B</sub>) shall be the concatenation of "Responder-KEP-dmtf-spdm-v" and `SPDMversionString`.

A Requester should generate a new DHE key pair for each `KEY_EXCHANGE` request message that the Requester sends. A Responder should generate a new DHE key pair for each `KEY_EXCHANGE_RSP` response message that the Responder sends.

<a id="table-key-exchange-request-message-format"></a>**Table 69 &mdash; KEY_EXCHANGE request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0        | SPDMVersion         | 1                  | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1        | RequestResponseCode | 1                  | Shall be `0xE4`=`KEY_EXCHANGE`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2        | Param1              | 1                  | Shall be the type of measurement summary hash requested:<br/><br/>`0x0`: No measurement summary hash requested.<br/><br/>`0x1`: TCB measurements only.<br/><br/>`0xFF`: All measurements.<br/><br/>All other values reserved.<br/><br/>If a Responder does not support measurements (`MEAS_CAP=00b` in its `CAPABILITIES` response), the Requester shall set this value to `0x0`. |
| 3        | Param2              | 1                  | Shall be the `SlotID`.  Slot number of the Responder certificate chain that shall be used for authentication. If the public key of the Responder was provisioned to the Requester in a trusted environment, the value in this field shall be `0xFF`; otherwise it shall be between 0 and 7 inclusive. |
| 4        | ReqSessionID        | 2                  | Shall be the two-byte Requester contribution to allow construction of a unique four-byte session ID between a Requester-Responder pair. The final session ID (SessionID) = Concatenate(ReqSessionID, RspSessionID). |
| 6        | SessionPolicy       | 1                  | Shall be the session policy as [Table 70 &mdash; Session policy](#table-terminate-config) defines. |
| 7        | Reserved            | 1                  | Reserved. |
| 8        | RandomData          | 32                 | Shall be the Requester-provided random data. |
| 40       | ExchangeData        | D                  | Shall be the DHE public information generated by the Requester. If the DHE group selected in the most recent `ALGORITHMS` response is finite-field-based (FFDHE), the `ExchangeData` represents the computed public value. If the selected DHE group is elliptic-curve-based (ECDHE), the `ExchangeData` represents the X and Y values in network byte order. Specifically, X is [0: C - 1] and Y is [C : D - 1]. In both cases the size of D (and C for ECDHE) is derived from the selected DHE group, as described in [Table 23 &mdash; DHE structure](#table-dhe-structure-2). |
| 40 + `D` | OpaqueDataLength    | 2                  | Shall be the size of the `OpaqueData` field that follows in bytes. The value should not be greater than 1024 bytes. Shall be `0` if no `OpaqueData` is provided. |
| 42 + `D` | OpaqueData          | `OpaqueDataLength` | If present, shall be the `OpaqueData` sent by the Requester. Used to indicate any parameters that the Requester wishes to pass to the Responder as part of key exchange. If present, this field shall conform to the selected opaque data format in `OtherParamsSelection`. |

<a id="table-terminate-config"></a>**Table 70 &mdash; Session policy**

| Bit offset | Field             | Description                |
|:-----------|:----------------- |:---------------------------|
| 0          | TerminationPolicy | This field specifies the behavior of the Responder when the Responder completes a runtime code or configuration update that affects the hardware or firmware measurement of the Responder. The Requester selects the value. If not set, the Responder shall terminate the session when the runtime update has taken effect. If set, the Responder shall decide whether to terminate or continue with the session based on its own policy. A policy example is one where the Responder terminates the session whenever an update to configuration or runtime code changes the security version of the firmware that manages SPDM sessions. The policy of the Responder is outside the scope of this specification.<br/><br/>To terminate a session, the Responder shall either respond with an `ERROR` message of `ErrorCode=RequestResynch` to any SPDM request received within the session or silently discard any request received within the session until a `GET_VERSION` request is received. |
| 1          | EventAllPolicy    | If set, the Responder shall subscribe the Requester to all events the Responder supports. Upon successfully entering the application phase of a session, the Responder may immediately send events.<br/><br/>If `EVENT_CAP` is not set in `CAPABILITIES`, the Responder shall either respond with an `ERROR` message of `ErrorCode=InvalidRequest` or silently discard the request. |
| [7:2]      | Reserved          | Reserved |

<a id="table-successful-key-exchange-rsp-response-message-format"></a>**Table 71 &mdash; Successful KEY_EXCHANGE_RSP response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0                                          | SPDMVersion             | 1                  | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1                                          | RequestResponseCode     | 1                  | Shall be `0x64`=`KEY_EXCHANGE_RSP`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2                                          | Param1                  | 1                  | Shall be HeartbeatPeriod.<br/><br/>The value of this field shall be zero if Heartbeat is not supported by one of the endpoints. Otherwise, the value shall be in units of seconds. Zero is a legal value if Heartbeat is supported, and this means that a heartbeat is not desired on this session. |
| 3                                          | Param2                  | 1                  | Reserved. |
| 4                                          | RspSessionID            | 2                  | Shall be the two-byte Responder contribution to allow construction of a unique four-byte session ID between a Requester-Responder pair. The final session ID = Concatenate(ReqSessionID, RspSessionID). |
| 6                                          | MutAuthRequested        | 1                  | Bit 0. If set, the Responder is requesting to authenticate the Requester ([Session-based mutual authentication](#session-based-mutual-authentication)) without using the encapsulated request flow.<br/><br/>Bit 1. If set, Responder is requesting Session-based mutual authentication with the encapsulated request flow.<br/><br/>Bit 2. If set, Responder is requesting Session-based mutual authentication with an implicit `GET_DIGESTS` request. The Responder and Requester shall follow the optimized encapsulated request flow.<br/><br/> Bit [7:3]. Reserved.<br/><br/>At most one bit of Bit 0, Bit 1, or Bit 2 shall be set.<br/><br/>For encapsulated request flow and the optimized encapsulated request flow details, see the [GET_ENCAPSULATED_REQUEST request and ENCAPSULATED_REQUEST response messages](#get_encapsulated_request-request-and-encapsulated_request-response-messages) clause. |
| 7                                          | SlotIDParam             | 1                  | Bit [7:4]. Reserved.<br/><br/>Bit [3:0]. Shall be the `SlotID`. Slot number of the Requester certificate chain that shall be used for mutual authentication, if `MutAuthRequested` Bit 0 is set. If the public key of the Requester was provisioned to the Responder through other means, the value in this field shall be `0xF`; otherwise it shall be between 0 and 7 inclusive. All other values reserved.<br/><br/>For any other value of `MutAuthRequested`, this field shall be set to `0` and ignored by the Requester. |
| 8                                          | RandomData              | 32                 | Shall be the Responder-provided random data. |
| 40                                         | ExchangeData            | D                  | Shall be the DHE public information generated by the Responder. If the DHE group selected in the most recent `ALGORITHMS` response is finite-field-based (FFDHE), the `ExchangeData` represents the computed public value. If the selected DHE group is elliptic-curve-based (ECDHE), the `ExchangeData` represents the X and Y values in network byte order. Specifically, X is [0: C - 1] and Y is [C : D - 1]. In both cases the size of D (and C for ECDHE) is derived from the selected DHE group, as described in [Table 23 &mdash; DHE structure](#table-dhe-structure-2). |
| 40 + `D`                                     | MeasurementSummaryHash  | `MSHLength` = `H` or 0         | If the Responder does not support measurements (`MEAS_CAP=00b` in its `CAPABILITIES` response) or requested `Param1`=`0x0`, this field shall be absent.<br/><br/>If the requested `Param1`=`0x1`, this field shall be the combined hash of measurements of all measurable components considered to be in the TCB required to generate this response, computed as `hash(Concatenate(MeasurementBlock[0], MeasurementBlock[1], ...))`, where `MeasurementBlock[x]` denotes a measurement of an element in the TCB and `hash` is the negotiated base hashing algorithm. Measurements are concatenated in ascending order based on their measurement index as [Table 53 &mdash; Measurement block format](#table-measurement-block-format) describes.<br/><br/>If the requested `Param1`=`0x1` and if there are no measurable components in the TCB required to generate this response, this field shall be `0`.<br/><br/>If requested `Param1`=`0xFF`, this field shall be computed as `hash(Concatenate(MeasurementBlock[0], MeasurementBlock[1], ..., MeasurementBlock[n]))` of all supported measurements available in the measurement index range `0x01`-`0xFE`, concatenated in ascending index order. Indices with no associated measurements shall not be included in the hash calculation. See the [Measurement index assignments](#measurement-index-assignments) clause.<br/><br/>If the Responder supports both raw bit stream and digest representations for a given measurement index, the Responder shall use the digest form.<br/><br/>This field shall be in [hash byte order](#hash-byte-order). |
| 40 + `D` + `MSHLength`                                 | OpaqueDataLength        | 2                  | Shall be the size of the `OpaqueData` field that follows in bytes. The value should not be greater than 1024 bytes. Shall be `0` if no `OpaqueData` is provided. |
| 42 + `D` + `MSHLength`                                 | OpaqueData              | `OpaqueDataLength` | If present, shall be the `OpaqueData` sent by the Responder. Used to indicate any parameters that the Responder wishes to pass to the Requester as part of key exchange. If present, this field shall conform to the selected opaque data format in `OtherParamsSelection`. |
| 42 + `D` + `MSHLength` + `OpaqueDataLength`            | Signature               | `SigLen`           | Shall be the `Signature` over the transcript. `SigLen` is the size of the asymmetric signing algorithm output the Responder selected via the last `ALGORITHMS` response message to the Requester. The [Transcript for KEY_EXCHANGE_RSP signature](#definition_th_ke_resp) defines the construction of the transcript. |
| 42 + `D` + `MSHLength` + `OpaqueDataLength` + `SigLen` | ResponderVerifyData     | `H` or 0             | Conditional field.<br/><br/>If the Session Handshake Phase is encrypted and/or message authenticated, this field shall be of length H and shall equal the HMAC of the transcript hash, using `finished_key` as the secret key and using the negotiated hash algorithm as the hash function. The transcript hash shall be the hash of the transcript for `KEY_EXCHANGE_RSP` HMAC as [Transcript for KEY_EXCHANGE_RSP HMAC](#definition_th_ke_resp_vf) shows. The `finished_key` shall be derived from the Response Direction Handshake Secret and is described in [Finished_key derivation](#finished_key-derivation). HMAC is described in [RFC 2104](https://tools.ietf.org/html/rfc2104).<br/><br/>If both the Requester and Responder set `HANDSHAKE_IN_THE_CLEAR_CAP` to 1, this field shall be absent. |

### Session-based mutual authentication

Mutual authentication for `KEY_EXCHANGE` occurs in the session handshake phase of a session.

To perform authentication of a Requester, the Responder sets the appropriate bit in the `MutAuthRequested` field of the `KEY_EXCHANGE_RSP` message. When either Bit 1 or Bit 2 of `MutAuthRequested` are set, the encapsulated request flow or the optimized encapsulated request flow shall be used accordingly to enable the Responder to obtain the certificate chains and certificate chain digests of the Requester. For flow details and illustrations, see [GET_ENCAPSULATED_REQUEST request and ENCAPSULATED_REQUEST response messages](#get_encapsulated_request-request-and-encapsulated_request-response-messages).

When either bit 1 or bit 2 of `MutAuthRequested` are set, the only allowed messages in this phase of the session shall be `GET_DIGESTS`, `DIGESTS`, `GET_CERTIFICATE`, `CERTIFICATE`, and `ERROR`. If the Requester receives other requests during this flow, the Requester can respond with an `ERROR` message of `ErrorCode=UnexpectedRequest` and shall terminate the session.

If Bit 0 of `MutAuthRequested` is set, then mutual authentication shall be performed without exchanging any messages between `KEY_EXCHANGE_RSP` and `FINISH` request. This is useful for Responders that have obtained a Requester's certificate chains in a previous interaction.

#### Specify Requester certificate for session-based mutual authentication

The SPDM key exchange protocol is optimized to perform key exchange with the least number of messages exchanged. For Responder-only authentication and for mutual authentication where the Responder has obtained the certificate chains of the Requester in a previous interaction, key exchange is carried out with two request/response message pairs (`KEY_EXCHANGE` and `KEY_EXCHANGE_RSP`; `FINISH` and `FINISH_RSP`). In other cases where mutual authentication is desired, additional [encapsulated messages](#get_encapsulated_request-request-and-encapsulated_request-response-messages) are exchanged between `KEY_EXCHANGE_RSP` and `FINISH` to enable the Responder to obtain the certificate chains and certificate chain digests of the Requester. However, in all cases the certificate chain (or raw public key) the Requester should authenticate against is specified by the Responder via the `SlotID` field in `KEY_EXCHANGE_RSP`, which precedes the aforementioned encapsulated messages. This means that a Responder has no way of knowing in advance which `SlotID` value to use when authenticating a Requester whose certificates it has not obtained in a previous interaction, other than the default (Slot 0).

To address this case, the Responder explicitly designates the certificate chain to be used via the final `ENCAPSULATED_RESPONSE_ACK` request issued inside the encapsulated request flow. Specifically, if either Bit 1 or 2 in `MutAuthRequested` is set to `1`, the Responder shall use an `ENCAPSULATED_RESPONSE_ACK` request with `Param2`=`0x02` and a 1-byte-long `Encapsulated Request` field containing the `SlotID` value. The Requester shall use the certificate chain corresponding to the slot specified in the `Encapsulated Request` field.

If Bit 0 of `MutAuthRequested` is set, then no encapsulated messages are exchanged after `KEY_EXCHANGE_RSP` and the certificate chain of the Requester is determined by the value of `SlotIDParam` in `KEY_EXCHANGE_RSP`.

## FINISH request and FINISH_RSP response messages

This request message shall complete the handshake between Requester and Responder initiated by a `KEY_EXCHANGE` request. The purpose of the `FINISH` request and `FINISH_RSP` response messages is to provide key confirmation, bind the identity of each party to the exchanged keys and protect the entire handshake against manipulation by an active attacker. Upon receiving a `FINISH` request, the Responder shall ensure the session and the corresponding session ID were created through a `KEY_EXCHANGE` request and corresponding `KEY_EXCHANGE_RSP` response. [Table 72 &mdash; FINISH request message format](#table-finish-request-message-format) shows the `FINISH` request message format and [Table 73 &mdash; Successful FINISH_RSP response message format](#table-successful-finish-rsp-response-message-format) shows the `FINISH_RSP` response message format.

<a id="table-finish-request-message-format"></a>**Table 72 &mdash; FINISH request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0          | SPDMVersion          | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1          | RequestResponseCode  | 1            | Shall be `0xE5`=`FINISH`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2          | Param1               | 1            | Bit 0. If set, the Signature field is included. This bit shall be set when Session-based mutual authentication occurs. All other bits reserved. |
| 3          | Param2               | 1            | Shall be the `SlotID`. Only valid if `Param1`=`0x01`, otherwise reserved.  Slot number of the Requester certificate chain that shall be used for authentication. If the public key of the Requester was provisioned to the Responder in a trusted environment, the value in this field shall be `0xFF`; otherwise it shall be between 0 and 7 inclusive. |
| 4          | Signature            | SigLen       | Shall be the `Signature` over the transcript. `SigLen` is the size of the asymmetric signing algorithm (`ReqBaseAsymAlg`) output the Responder selected via the last `ALGORITHMS` response message to the Requester. If `Param1`=`0x00`, `SigLen` is zero and this field shall be absent. [Transcript for FINISH signature, mutual authentication](#definition_th_fi_req_mut) defines the construction of the transcript, signature generation, and verification. |
| 4 + `SigLen` | RequesterVerifyData  | H            | Shall be an HMAC of the transcript hash using the `finished_key` as the secret key and using the negotiated hash algorithm as the hash function. For mutual authentication, the transcript hash shall be the hash of the transcript for `FINISH` HMAC, mutual authentication as the [transcript for FINISH HMAC, mutual authentication](#definition_th_fi_req_vf_mut) shows. Otherwise, it shall be the hash of the transcript for `FINISH` HMAC, Responder-only authentication as the [transcript for FINISH HMAC, Responder-only authentication](#definition_th_fi_req_vf) shows. The `finished_key` shall be derived from Request Direction Handshake Secret and is described in [Finished_key derivation](#finished_key-derivation). HMAC is described in [RFC 2104](https://tools.ietf.org/html/rfc2104). |

If the handshake is performed in the clear (that is, if `HANDSHAKE_IN_THE_CLEAR_CAP`=`1` for both Requester and Responder), and if either Bit 1 or Bit 2 in `KEY_EXCHANGE_RSP`.`MutAuthRequested` is set, then upon receiving `FINISH` the Responder shall confirm that the value in `FINISH`.`Param2` matches the value that the Responder specified in the final `ENCAPSULATED_RESPONSE_ACK`.`EncapsulatedRequest`.

<a id="table-successful-finish-rsp-response-message-format"></a>**Table 73 &mdash; Successful FINISH_RSP response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | SPDMVersion          | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1      | RequestResponseCode  | 1            | Shall be `0x65`=`FINISH_RSP`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2      | Param1               | 1            | Reserved. |
| 3      | Param2               | 1            | Reserved. |
| 4      | ResponderVerifyData  | `H` or 0       | Conditional field.<br/><br/>If the Session Handshake Phase is encrypted and/or message authenticated (that is, if either the Requester or the Responder set `HANDSHAKE_IN_THE_CLEAR_CAP` to 0), this field shall be absent.<br/><br/>If both the Requester and Responder support `HANDSHAKE_IN_THE_CLEAR_CAP` field, this field shall be of length H and shall equal the HMAC of the transcript hash using `finished_key` as the secret key and using the negotiated hash algorithm as the hash function. For Session-based mutual authentication, the transcript hash shall be the hash of the transcript for `FINISH_RSP` HMAC, as the [transcript for FINISH_RSP HMAC, mutual authentication](#definition_th_fi_res_vf_mut) shows. Otherwise, the transcript hash shall be the hash of the transcript for `FINISH_RSP` HMAC, Responder-only authentication as the [transcript for FINISH_RSP HMAC, Responder-only authentication](#definition_th_fi_res_vf) shows.  The `finished_key` shall be derived from Response Direction Handshake Secret and is described in [Finished_key derivation](#finished_key-derivation). HMAC is described in [RFC 2104](https://tools.ietf.org/html/rfc2104). |

### Transcript and transcript hash calculation rules for KEY_EXCHANGE

[Transcript for KEY_EXCHANGE_RSP signature](#definition_th_ke_resp) shows the transcript for the `KEY_EXCHANGE_RSP` signature:

<a id="definition_th_ke_resp"></a>**Transcript for KEY_EXCHANGE_RSP signature**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*` except the `Signature` and `ResponderVerifyData` fields.

The Responder shall generate the `KEY_EXCHANGE_RSP` signature from:

```C
SPDMsign(PrivKey, transcript, "key_exchange_rsp signing");
```

where

* `SPDMsign` is described by the [Signature generation](#signature-generation) clause.
* `PrivKey` shall be the private key of the Responder associated with the leaf certificate stored in `SlotID` in `KEY_EXCHANGE`. If the public key of the Responder was provisioned to the Requester, then `PrivKey` shall be the associated private key.
* `transcript` shall be the concatenation of the messages for a `KEY_EXCHANGE_RSP` signature.

The leaf certificate of the Responder shall be the one indicated by `SlotID` in `Param2` of `KEY_EXCHANGE` request.

Likewise, the Requester shall verify the `KEY_EXCHANGE_RSP` signature using `SPDMsignatureVerify(PubKey, signature, transcript, "key_exchange_rsp signing")`, where `transcript` is the concatenation of the messages for a `KEY_EXCHANGE_RSP` signature and `PubKey` is the public key of the leaf certificate of the Responder. The leaf certificate of the Responder shall be the one indicated by `SlotID` in `Param2` of `KEY_EXCHANGE` request. `SPDMsignatureVerify` is described in [Signature verification](#signature-verification). A successful verification shall be when `SPDMsignatureVerify` returns `success`.

[Transcript for KEY_EXCHANGE_RSP HMAC](#definition_th_ke_resp_vf) shows the transcript for `KEY_EXCHANGE_RSP` HMAC:

<a id="definition_th_ke_resp_vf"></a>**Transcript for `KEY_EXCHANGE_RSP` HMAC**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*` except the `ResponderVerifyData` field.

[Transcript for FINISH signature, mutual authentication](#definition_th_fi_req_mut) shows the transcript for the `FINISH` signature with mutual authentication:

<a id="definition_th_fi_req_mut"></a>**Transcript for `FINISH` signature, mutual authentication**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*`
1. `[DIGESTS].*` (if encapsulated `DIGEST` is issued and `MULTI_KEY_CONN_REQ` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `FINISH`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[FINISH]`.`SPDM Header Fields`

The Requester shall generate the `FINISH` signature from `SPDMsign(PrivKey, transcript, "finish signing")`, where `transcript` is the concatenation of the messages for `FINISH` signature and the `PrivKey` is the private key of the leaf certificate of the Requester. The leaf certificate of the Requester shall be the one indicated in `SlotID` in `Param2` of `FINISH` request. `SPDMsign` is described in [Signature generation](#signature-generation).

Likewise, the Responder shall verify the `FINISH` signature using `SPDMsignatureVerify(PubKey, signature, transcript, "finish signing")`, where `transcript` is the concatenation of the messages for a `FINISH` signature and the `PubKey` is the public key of the leaf certificate of the Requester. The leaf certificate of the Requester shall be the one indicated in `SlotID` in `Param2` of the `FINISH` request. `SPDMsignatureVerify` is described in [Signature verification](#signature-verification). A successful verification is when `SPDMsignatureVerify` returns `success`.

[Transcript for FINISH HMAC, Responder-only authentication](#definition_th_fi_req_vf) shows the transcript for `FINISH` HMAC with Responder-only authentication:

<a id="definition_th_fi_req_vf"></a>**Transcript for `FINISH` HMAC, Responder-only authentication**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*`
1. `[FINISH]`.`SPDM Header Fields`

[Transcript for FINISH HMAC, mutual authentication](#definition_th_fi_req_vf_mut) shows the transcript for `FINISH` HMAC with mutual authentication:

<a id="definition_th_fi_req_vf_mut"></a>**Transcript for `FINISH` HMAC, mutual authentication**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*`
1. `[DIGESTS].*` (if encapsulated `DIGEST` is issued and `MULTI_KEY_CONN_REQ` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `FINISH`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[FINISH]`.`SPDM Header Fields`
1. `[FINISH]`.`Signature`

[Transcript for FINISH_RSP HMAC, Responder-only authentication](#definition_th_fi_res_vf) shows the transcript for `FINISH_RSP` HMAC with Responder-only authentication:

<a id="definition_th_fi_res_vf"></a>**Transcript for `FINISH_RSP` HMAC, Responder-only authentication**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*`
1. `[FINISH]`.`*`
1. `[FINISH_RSP]`.`SPDM Header fields`

[Transcript for FINISH_RSP HMAC, mutual authentication](#definition_th_fi_res_vf_mut) shows the transcript for `FINISH_RSP` HMAC with mutual authentication:

<a id="definition_th_fi_res_vf_mut"></a>**Transcript for `FINISH_RSP` HMAC, mutual authentication**

1. `VCA`
1. `[DIGESTS].*` (if issued and `MULTI_KEY_CONN_RSP` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `KEY_EXCHANGE`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[KEY_EXCHANGE]`.`*`
1. `[KEY_EXCHANGE_RSP]`.`*`
1. `[DIGESTS].*` (if encapsulated `DIGEST` is issued and `MULTI_KEY_CONN_REQ` is true).
1. Hash of the specified certificate chain in DER format (that is, `Param2` of `FINISH`) or hash of the public key in its provisioned format, if a certificate is not used.
1. `[FINISH]`.`*`
1. `[FINISH_RSP]`.`SPDM Header fields`

When multiple session keys are being established between the same Requester-Responder pair, the `Signature` over the transcript during `FINISH` request is computed using only the corresponding `KEY_EXCHANGE`, `KEY_EXCHANGE_RSP`, and `FINISH` request parameters.

For additional rules, see [general ordering rules](#general-ordering-rules).

## PSK_EXCHANGE request and PSK_EXCHANGE_RSP response messages

The Pre-Shared Key (PSK) key exchange scheme provides an option for a Requester and a Responder to perform session key establishment with symmetric-key cryptography. This option is especially useful for endpoints that do not support asymmetric-key cryptography or certificate processing. This option can also be leveraged to expedite session key establishment even if asymmetric-key cryptography is supported.

This option requires the Requester and Responder to have prior knowledge of a common PSK before the handshake. Essentially, the PSK serves as a mutual authentication credential and as the base of session key establishment. As such, only the two endpoints and potentially a trusted third party that provisions the PSK to the two endpoints know the value of the PSK. For these same reasons, the `HANDSHAKE_IN_THE_CLEAR_CAP` is not applicable in a PSK key exchange. Thus, for PSK-based session establishment, both the Responder and the Requester shall ignore the `HANDSHAKE_IN_THE_CLEAR_CAP` bit.

A Requester can pair with multiple Responders. Likewise, a Responder can pair with multiple Requesters. A Requester-Responder pair can be provisioned with one or more PSKs. An endpoint can act as a Requester to one device and simultaneously a Responder to another device. If both endpoints can act as Requester or Responder, then the endpoints shall use different PSKs for each role. It is the responsibility of the transport layer to identify the peer and establish communication between the two endpoints before the PSK-based session key exchange starts.

The PSK can be provisioned in a trusted environment, for example, during the secure manufacturing process. In an untrusted environment, the PSK can be agreed upon between the two endpoints using a secure protocol. The mechanism for PSK provisioning is outside the scope of this specification. The size of the provisioned PSK is determined by the security strength requirements of the application, but it should be at least 128 bits. It is recommended to be at least 256 bits in order to resist dictionary attacks, particularly when the Requester and Responder cannot both contribute sufficient entropy during the exchange.

Two message pairs are defined for this option:

* `PSK_EXCHANGE`/`PSK_EXCHANGE_RSP`
* `PSK_FINISH`/`PSK_FINISH_RSP`

The `PSK_EXCHANGE` message carries three responsibilities:

1. Prompts the Responder to retrieve the specific PSK.
1. Exchanges contextual information between the Requester and the Responder.
1. Proves to the Requester that the Responder knows the correct PSK and has derived the correct session keys.

[Figure 17 &mdash; PSK_EXCHANGE: Example](#figure-preshared-key-exchange-example) shows an example of the `PSK_EXCHANGE` message:

<a id="figure-preshared-key-exchange-example"></a>**Figure 17 &mdash; PSK_EXCHANGE: Example**

![Figure 17 &mdash; PSK_EXCHANGE: Example](SPDMSpecification_files/Figure_PreSharedSecret_flow.svg)

<a id="table-psk-exchange-request-message-format"></a>**Table 74 &mdash; PSK_EXCHANGE request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0              | SPDMVersion         | 1                  | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1              | RequestResponseCode | 1                  | Shall be `0xE6`=`PSK_EXCHANGE`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2              | Param1              | 1                  | Shall be the type of measurement summary hash requested:<br/><br/>`0x0`: No measurement summary hash requested.<br/><br/>`0x1`: TCB measurements only.<br/><br/>`0xFF`: All measurements.<br/><br/>All other values reserved.<br/><br/>If a Responder does not support measurements (`MEAS_CAP=00b` in its `CAPABILITIES` response), the Requester shall set this value to `0x0`. |
| 3              | Param2              | 1                  | Shall be the session policy. See [Table 70 &mdash; Session policy](#table-terminate-config). |
| 4              | ReqSessionID        | 2                  | Shall be the two-byte Requester contribution to allow construction of a unique four-byte session ID between a Requester-Responder pair. The final session ID = Concatenate(ReqSessionID, RspSessionID). |
| 6              | P                   | 2                  | Shall be the length of `PSKHint` in bytes. |
| 8              | R                   | 2                  | Shall be the length of `RequesterContext` in bytes. |
| 10             | OpaqueDataLength    | 2                  | Shall be the size of the `OpaqueData` field that follows in bytes. The value should not be greater than 1024 bytes. Shall be `0` if no `OpaqueData` is provided. |
| 12             | PSKHint             | `P`                | Shall be the information required by the Responder to retrieve the PSK. Optional. |
| 12 + `P`       | RequesterContext    | `R`                | Shall be the context of the Requester. Shall include a nonce or non-repeating counter of at least 32 bytes and, optionally, relevant information contributed by the Requester. |
| 12 + `P` + `R` | OpaqueData          | `OpaqueDataLength` | Optional. If present, the `OpaqueData` sent by the Requester is used to indicate any parameters that the Requester wishes to pass to the Responder as part of PSK-based key exchange. If present, this field shall conform to the selected opaque data format in `OtherParamsSelection`. |

The field `PSKHint` is optional. It is absent if P is set to 0. It is introduced to address two scenarios:

* The Responder is provisioned with multiple PSKs and stores them in secure storage. The Requester uses `PSKHint` as an identifier to specify which PSK will be used in this particular session.
* The Responder does not store the actual value of the PSK but can derive the PSK using `PSKHint`. For example, if the Responder has an immutable UDS (Unique Device Secret) in fuses, then during provisioning a PSK can be derived from the UDS (or a derivative value) and a non-secret salt known by the Requester. During session key establishment, the salt value is sent to the Responder in `PSKHint` of `PSK_EXCHANGE`. This mechanism allows the Responder to support any number of PSKs without consuming secure storage.

The `RequesterContext` is the contribution of the Requester to session key derivation. It shall contain a nonce or non-repeating counter to ensure that the derived session keys are ephemeral to mitigate against replay attacks. If a non-repeating counter is used, the counter shall not be reset for the lifetime of the device. The `RequesterContext` can also contain other information from the Requester.

Upon receiving a `PSK_EXCHANGE` request, the Responder:

1. Generates PSK from `PSKHint`, if necessary.
1. Generates `ResponderContext`, if supported.
1. Derives the `finished_key` of the Responder by following the [key schedule](#key-schedule).
1. Constructs the `PSK_EXCHANGE_RSP` response message and sends it to the Requester.

<a id="table-psk-exchange-rsp-response-message-format"></a>**Table 75 &mdash; PSK_EXCHANGE_RSP response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0                                   | SPDMVersion             | 1                  | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1                                   | RequestResponseCode     | 1                  | Shall be `0x66`=`PSK_EXCHANGE_RSP`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2                                   | Param1                  | 1                  | Shall be HeartbeatPeriod.<br/><br/>The value of this field shall be zero if Heartbeat is not supported by one of the endpoints. Otherwise, the value shall be in units of seconds. Zero is a legal value if Heartbeat is supported, and this means that a heartbeat is not desired on this session. |
| 3                                   | Param2                  | 1                  | Reserved. |
| 4                                   | RspSessionID            | 2                  | Shall be the two-byte Responder contribution to allow construction of a unique four-byte session ID between a Requester-Responder pair. The final session ID (SessionID) = Concatenate(ReqSessionID, RspSessionID). |
| 6                                   | Reserved                | 2                  | Reserved. |
| 8                                   |  Q                       | 2                  | Shall be the length of ResponderContext in bytes. |
| 10                                  | OpaqueDataLength        | 2                  | Shall be the size of the `OpaqueData` field that follows in bytes. The value should not be greater than 1024 bytes. Shall be `0` if no `OpaqueData` is provided. |
| 12                                  | MeasurementSummaryHash  | `MSHLength`= `H` or 0       | If the Responder does not support measurements (`MEAS_CAP=00b` in its `CAPABILITIES` response) or requested `Param1`=`0x0`, this field shall be absent.<br/><br/>If the requested `Param1`=`0x1`, this field shall be the combined hash of measurements of all measurable components considered to be in the TCB required to generate this response, computed as `hash(Concatenate(MeasurementBlock[0], MeasurementBlock[1], ...))`, where `MeasurementBlock[x]` denotes a measurement of an element in the TCB and `hash` is the negotiated base hashing algorithm. Measurements are concatenated in ascending order based on their measurement index as [Table 53 &mdash; Measurement block format](#table-measurement-block-format) describes.<br/><br/>If the requested `Param1`=`0x1` and if there are no measurable components in the TCB required to generate this response, this field shall be `0`.<br/><br/>If requested `Param1`=`0xFF`, this field shall be computed as `hash(Concatenate(MeasurementBlock[0], MeasurementBlock[1], ..., MeasurementBlock[n]))` of all supported measurements available in the measurement index range `0x01`-`0xFE`, concatenated in ascending index order. Indices with no associated measurements shall not be included in the hash calculation. See the [Measurement index assignments](#measurement-index-assignments) clause.<br/><br/>If the Responder supports both raw bit stream and digest representations for a given measurement index, the Responder shall use the digest form.<br/><br/>This field shall be in [hash byte order](#hash-byte-order). |
| 12 + `MSHLength`                            | ResponderContext        | `Q`                | Shall be the context of the Responder. Optional. If present, shall include a nonce and/or information contributed by the Responder. |
| 12 + `MSHLength` + `Q`                      | OpaqueData              | `OpaqueDataLength` | Optional. If present, the `OpaqueData` sent by the Responder is used to indicate any parameters that the Responder wishes to pass to the Requester as part of PSK-based key exchange. If present, this field shall conform to the selected opaque data format in `OtherParamsSelection`. |
| 12 + `MSHLength` + `Q` + `OpaqueDataLength` | ResponderVerifyData     | `H`                | Shall be the data to be verified by the Requester using the `finished_key` of the Responder. |

The `ResponderContext` is the contribution of the Responder to session key derivation. It should contain a nonce or non-repeating counter and other information from the Responder. If a non-repeating counter is used, the counter shall not be reset for the lifetime of the device. Because the Responder can be a constrained device that cannot generate a nonce, `ResponderContext` is optional. However, the Responder is required to use `ResponderContext` if it can generate a nonce.

Note that the nonce in `ResponderContext` is critical for anti-replay. If a nonce is not present in `ResponderContext`, then the Responder is not challenging the Requester for real-time knowledge of the PSK. Such a session is subject to replay attacks&mdash;that is, a person-in-the-middle attacker could record and replay prior `PSK_EXCHANGE` and `PSK_FINISH` messages and set up a session with the Responder. But the bogus session would not leak secrets, so long as the PSK and session keys of the prior replayed session are not compromised.

If `ResponderContext` is absent, such as when `PSK_CAP` in the `CAPABILITIES` of the Responder is `01b`, the Requester shall not send `PSK_FINISH`, because the session keys are solely determined by the Requester and the Session immediately enters the Application Phase.  If and only if the `ResponderContext` is present in the response, such as when `PSK_CAP` in the `CAPABILITIES` of the Responder is `10b`, the Requester shall send `PSK_FINISH` with `RequesterVerifyData` to prove that it has derived correct session keys.

To calculate `ResponderVerifyData`, the Responder calculates an HMAC. The HMAC key is the `finished_key` of the Responder. The data is the hash of the concatenation of all messages sent up to this point between the Requester and the Responder. For messages that are encrypted, the plaintext messages are used in calculating the hash.

```raw
1. [GET_VERSION].*
2. [VERSION].*
3. [GET_CAPABILITIES].* (if issued)
4. [CAPABILITIES].* (if issued)
5. [NEGOTIATE_ALGORITHMS].* (if issued)
6. [ALGORITHMS].* (if issued)
7. [PSK_EXCHANGE].*
8. [PSK_EXCHANGE_RSP].* except the ResponderVerifyData field
```

Note that, even if `CERTIFICATE` and Responder-signed response messages (such as `CHALLENGE_AUTH`) were issued, these messages would not be included in the data for calculating `ResponderVerifyData`. In other words, the identity of the signer of the response messages is not bound to the identity of the sender of `PSK_EXCHANGE_RSP`. Therefore, to mitigate Responder identity impersonation, if the Requester has received a response with a signature and if there is no cryptographic binding between the signer of the Responder-signed response and the sender of `PSK_EXCHANGE_RSP`, then the Requester should not issue `PSK_EXCHANGE`. The method of cryptographic binding between the signer of the Responder-signed response and the sender of `PSK_EXCHANGE_RSP` is outside the scope of this specification.

Upon receiving `PSK_EXCHANGE_RSP`, the Requester:

1. Derives the `finished_key` of the Responder by following the [key schedule](#key-schedule).
1. Verifies `ResponderVerifyData` by calculating the HMAC in the same manner as the Responder. If verification fails, the Requester terminates the session.
1. If the Responder contributes to session key derivation, such as when the `ResponderContext` field is present in the `PSK_EXCHANGE_RSP` response, it constructs the `PSK_FINISH` request and sends it to the Responder.

If a successful `PSK_EXCHANGE_RSP` has been received by the Requester, and the `PSK_CAP` of the Responder is `10b`, and the `ResponderContext` field is present in the `PSK_EXCHANGE_RSP` response then, for the session ID created by the `PSK_EXCHANGE` and `PSK_EXCHANGE_RSP` messages, the next request shall be `PSK_FINISH`.

## PSK_FINISH request and PSK_FINISH_RSP response messages

These messages shall complete the mutually-authenticated handshake between Requester and Responder initiated by a `PSK_EXCHANGE` request. The `PSK_FINISH` request proves to the Responder that the Requester knows the PSK and has derived the correct session keys. This is achieved by an HMAC value calculated with the `finished_key` of the Requester and messages of this session. The Requester shall send `PSK_FINISH` only if `ResponderContext` is present in `PSK_EXCHANGE_RSP`. Upon receiving a `PSK_FINISH` request, the Responder shall ensure the session and the corresponding session ID were created through a `PSK_EXCHANGE` request and corresponding `PSK_EXCHANGE_RSP` response.

[Table 76 &mdash; PSK_FINISH request message format](#table-psk-finish-request-message-format) describes the `PSK_FINISH` request message format:

<a id="table-psk-finish-request-message-format"></a>**Table 76 &mdash; PSK_FINISH request message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | SPDMVersion         | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1      | RequestResponseCode | 1            | Shall be `0xE7`=`PSK_FINISH`. See [Table 4 &mdash; SPDM request codes](#table-spdm-request-codes).  |
| 2      | Param1              | 1            | Reserved. |
| 3      | Param2              | 1            | Reserved. |
| 4      | RequesterVerifyData | `H`          | Shall be the data to be verified by the Responder using the `finished_key` of the Requester. |

To calculate `RequesterVerifyData`, the Requester calculates an HMAC. The key is the `finished_key` of the Requester, as described in the [Key schedule](#key-schedule) clause. The data is the hash of the concatenation of all messages sent so far between the Requester and the Responder. For messages that are encrypted, the plaintext messages are used in calculating the hash.

```raw
1. [GET_VERSION].*
2. [VERSION].*
3. [GET_CAPABILITIES].* (if issued)
4. [CAPABILITIES].* (if issued)
5. [NEGOTIATE_ALGORITHMS].* (if issued)
6. [ALGORITHMS].* (if issued)
7. [PSK_EXCHANGE].*
8. [PSK_EXCHANGE_RSP].*
9. [PSK_FINISH].* except the RequesterVerifyData field
```

For additional rules, see [general ordering rules](#general-ordering-rules).

Upon receiving the `PSK_FINISH` request, the Responder derives the `finished_key` of the Requester and calculates the HMAC independently in the same manner and verifies that the result matches `RequesterVerifyData`. If verification is successful, the Responder constructs the `PSK_FINISH_RSP` response and sends it to the Requester. Otherwise, the Responder sends the Requester an `ERROR` message of `ErrorCode=InvalidRequest`.

[Table 77 &mdash; Successful PSK_FINISH_RSP response message format](#table-successful-psk-finish-rsp-response-message-format) describes the successful `PSK_FINISH_RSP` response message format:

<a id="table-successful-psk-finish-rsp-response-message-format"></a>**Table 77 &mdash; Successful PSK_FINISH_RSP response message format**

| Byte offset | Field            | Size (bytes) | Description                |
|:------------|:-----------------|:-------------|:---------------------------|
| 0      | SPDMVersion         | 1            | Shall be the `SPDMVersion` as described in [SPDM version](#spdm-version). |
| 1      | RequestResponseCode | 1            | Shall be `0x67`=`PSK_FINISH_RSP`. See [Table 5 &mdash; SPDM response codes](#table-spdm-response-codes).  |
| 2      | Param1              | 1            | Reserved. |
| 3      | Param2              | 1            | Reserved. |
