---
title: "Bits and Pieces - SnapStack"
author: "Peter Kaminski"
issue_slug: "2025-09-03"
tags: ['Tools and Platforms', 'Web3, DAOs, and Distributed Governance']
---

# Bits and Pieces - SnapStack

**Author:** [[Peter Kaminski]]
**Issue:** [2025-09-03](https://plex.collectivesensecommons.org/2025-09-03/)

---

## Bits and Pieces - SnapStack
by **Peter Kaminski**

Hey, I’m excited to tell you about a new project I’m working on, **SnapStack.** In the Massive Wiki - MarkPub universe, it will provide an alternative to Git for **sharing** and **versioning** files. If it sounds interesting and you want to follow along, send me an email: [kaminski@istori.com](mailto:kaminski@istori.com).

(In “Massive Wiki”, the word “Massive” is inspired by an acronym, “MaSVF”. The word “Wiki” represents naming and easy linking between pages, as well as the “wiki culture” of collaborative writing. MaSVF stands for **Ma **rkdown, **S** hared, **V** ersioned, **F** iles.)

SnapStack will be a light collection of workflows and collaborative agreements for a small, cohesive team, say 3-10 people, to use. It will use IPFS as a decentralized, immutable storage commons, IPNS for a canonical pointer to the most recent version of the wiki / vault / repository being worked on, and some lightweight versioning, in a version chain. The workflows are straightforward enough that you could just use a checklist to run through them as you pull and push new versions, but I expect we’ll build some lightweight software to automate the workflows.

A mostly non-technical explanation of IPFS: It’s like there’s a magical interplanetary disk drive, and you can use any of various gateways to access it. You give your local gateway a “content ID” (a CID), and it magically retrieves and gives you the corresponding file.

Underneath, it’s decentralized / distributed. Your local gateway node connects to a variety of other nodes around the solar system, and they all exchange a distributed hash table of who’s got which file. When you request a file that your local node doesn’t have, it asks around if anyone else has seen that file (by ID), until someone says, sure, here you go. Then you get the file. Kinda like interlibrary loan, but with many more books.

(Small tweak, the files are actually handled in chunks, usually around 256KB, and your gateway might get chunks of the file from different servers.)

Content-addressed storage is key. Files are identified by cryptographic hashes of their content rather than location-based addresses. This ensures content integrity and enables the decentralized model.

A “cryptographic hash” is another magical thing. It’s a bit of math that any computer can run when it looks at a file, which produces a unique ID from the contents of the file. So there’s a perfect 1:1 correspondence between the ID and the file or any exact copy of the file. But if the file changes even one little bit, the math generates a different ID!

---

**Related:**
- [[Peter Kaminski]] (author)
- [[2025]] (year)
- Topics: [[Tools and Platforms]], [[Web3, DAOs, and Distributed Governance]]

