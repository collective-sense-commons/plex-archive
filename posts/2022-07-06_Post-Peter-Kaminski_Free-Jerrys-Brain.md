---
title: "Free Jerrys Brain?"
author: "Peter Kaminski"
issue_slug: "2022-07-06"
tags: ['Tools and Platforms']
---

# Free Jerrys Brain?

**Author:** [[Peter Kaminski]]
**Issue:** [2022-07-06](https://plex.collectivesensecommons.org/2022-07-06/)

---

## Free Jerry's Brain?
by **Peter Kaminski**

*Serving as an update, of sorts, on the **Free Jerry's Brain** project.*

In [ogm] Town Square, [spirit asked](https://chat.collectivesensecommons.org/agora/pl/mt4cuxrrs3bb3q3cbb7xp719ac),

Hi! Was wondering if there are any developments on getting “[Jerry’s Brain](https://jerrysbrain.com/)” into a more open format (than [the brain](https://thebrain.com/) format) to work as a “sourdough starter” for other mapping projects? 🙂Yes, we have the data in Jerry's Brain available in a more open format. Thanks to code (“**MemeBrane**”) developed by the “Free Jerry's Brain” group, and deployment by **@maparent,** the data is stored in a PostgreSQL database.

The [MemeBrane server](https://memebrane.conversence.com/brain/jerry/thought/32f9fc36-6963-9ee0-9b44-a89112919e29/) at  shows a human-readable preview of the data for each thought; the same can be retrieved programmatically by setting Accept: application/json.

It “wouldn't be hard” (ymmv) to export the data from Postgres to any other reasonable format.

The next step, which *can* be hard (ymmv), is to write code / create visualizations that uses the data as “sourdough starter”.

The data is loaded into the database in two ways:

- importing a saved export (as Jerry says, an export that is 1.5 years old for the current load)
- individual thoughts are updated from the WebBrain source when they are loaded through the MemeBrane web interface (in this mode, the database works as a read-through cache, with a [TTL](https://en.wikipedia.org/wiki/Time_to_live) for individual thoughts of 24 hours)

So, if you're reading JSON through MemeBrane thought-by-thought, you'll see fresh thoughts every time.

If you did a database dump, you'd have a mix of current and old thoughts.

**spirit** continued,

It’s almost as if someone would have to rewrite the code for the Brain software or something similar. Has anyone attempted this?

Also I wonder could the data be imported into the mind mapping software **@jonathansand** is creating? Or too incompatible?**@bentleydavis** made a fairly straightforward HTML5+JS front-end for MemeBrane, [Brainy McBrainface](https://mcbrain.netlify.app/), which made it look more like Jerry's Brain. It's pretty interesting, but not powerful enough to replace TheBrain.

[Zsolt Viczián](https://twitter.com/zsviczian) is creating [ExcaliBrain](https://github.com/zsviczian/excalibrain), which creates a TheBrain-link interface within Obsidian.  In some ways, I think it's even more powerful than TheBrain.  It's great work, but still early and kinda creaky (no insult intended, it's amazing what he's doing).

You could probably import Jerry's Brain into Jonathan's [Seriously](https://apps.apple.com/eg/app/seriously/id1508392202), although Seriously is top-down mindmap rather than a directed graph.  (This might count as “too incompatible”.)  Also, Jerry's Brain is hundreds of thousands of nodes; Seriously might run into CPU, memory, or user interface scaling issues.

Similarly, you could import TheBrain into e.g., [Kumu](https://kumu.io/).  I don't think the Kumu interface would really replace TheBrain's, and again, there are possible scaling issues.

I've imported small exports of TheBrain into small websites with internal navigation; they work well for what they are, but they're read-only, of course.  (See [https://climatesites.net/](https://climatesites.net/) and the sites linked from there; they are exports from TheBrain.)

I've also imported small exports of TheBrain into [TiddlyWiki](https://tiddlywiki.com/) (and could do Massive Wiki); those would be read/write, but they wouldn't natively have the graphical interface of TheBrain. This might be a pro or a con, depending on the user, but admittedly, it would not replace TheBrain.

*Stay tuned for more as it happens. Contact [Pete](mailto:kaminski@istori.com) or [Jerry](mailto:sociate@gmail.com) for more info. Thank you for the prompting question, spirit!*

---

**Related:**
- [[Peter Kaminski]] (author)
- [[2022]] (year)
- Topics: [[Tools and Platforms]]

