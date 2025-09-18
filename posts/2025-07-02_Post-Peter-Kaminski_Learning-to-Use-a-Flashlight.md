---
title: "Learning to Use a Flashlight"
author: "Peter Kaminski"
issue_slug: "2025-07-02"
tags: []
---

# Learning to Use a Flashlight

**Author:** [[Peter Kaminski]]
**Issue:** [2025-07-02](https://plex.collectivesensecommons.org/2025-07-02/)

---

## Learning to Use a Flashlight
by **Peter Kaminski**

I like learning curves. There, I said it. You’re probably not surprised if you know me.

I wanted to tell you, I found a new learning curve! In sort of a surprising place: pocket flashlights.

But let’s back up a bit, first.

Growing up in the 1960s and 1970s, tinkering with electrical and electronic circuits was one of my experimental hobbies. And flashlights—or at least, the circuits for them—were pretty much the simplest thing you could build with your toy electrical set. A small incandescent bulb, and two wires, going to each end of a battery. To make it fancy, you could add a switch in the middle of one of the wires, and turn your little “flashlight” on and off. Super fun, not complex at all.

Back then, the biggest, brightest flashlight was for professionals—police officers, construction people working at night, firefighters, farmers. Maglite flashlights, big heavy things, with 2, 3, 4, even 6 “D” batteries. A 4D-cell Maglite with an incandescent bulb would put out 100 lumens—as bright as 100 candles shining all in one place. Fancy ones would have krypton or xenon bulbs, to make them a tad brighter.

Good news for gadget geeks: flashlights have gotten fancy! Any decent flashlight will now put out 100 lumens, and even tiny pocket ones can put out 1,000 lumens or more! Humans perceive brightness roughly logarithmically, so 1,000 lumens looks only 2-4x as bright as 100, but with improvements in batteries, LEDS, and optics, flashlights today are comparatively tiny and last much longer on a charge than the venerable old Maglites.

Interestingly to me, a fancy gadget pocket flashlight is now a little electronic marvel. Even the fanciest ones still look more or less like a Maglite, a metal tube with a bulb on one end and a button somewhere on it, just shrunk down to fit in the palm of your hand.

However, the button is *not* a physical part of the battery-light circuit anymore. It’s an electronic button that sends a signal to a thumbnail-sized computer, say an [ATtiny16](https://www.microchip.com/en-us/product/attiny1616) microcontroller or similar, inside the metal tube! The ATtiny16 is roughly 10x more powerful than a first-generation IBM PC. Yikes! If you’re old enough to remember pundits saying there would be computers everywhere, here’s an example.

The software in the flashlight handles the UI (user interface), the operation of the LED(s), tracking the voltage of the battery and the temperature of the flashlight, etc. The first software systems were proprietary to the manufacturer, but lucky for us, a developer named ToyKeeper developed an open source software, [Andúril 2](https://github.com/ToyKeeper/anduril), for ATtiny flashlights.

[ToyKeeper writes](https://www.patreon.com/toykeeper/about),

A few years back, I decided to see if I could flip an industry—convert it to free software and get manufacturers to collaborate with the community for mutual benefit. Gotta do something to stay busy, right? The weird thing is, it actually seems to be working. We’ve now got at least ten companies making lights with open-source code, listening to the people instead of treating us as just consumers. It’s a new way of doing business.(As an aside, **Anduril 2** the flashlight software has nothing to do with Palmer Luckey’s **Anduril** the military technology company, except that their names are inspired by Tolkien’s sword.)

ToyKeeper has a vibrant community helping by using and providing feedback for the software, so the software has grown into a capable and polished flashlight controller, with a finely-tuned UI. And with a number of flashlight manufacturers adopting the software and the UI, it’s become a lovely commons which benefits users and manufacturers alike.

For better or worse, the UI is complicated. **Hello, learning curve!** There are two main modes, “simple” and “advanced”—but even the simple mode can be a little daunting. Advanced mode is frankly complex.

The complexity is driven by the fact that the only input is a single button, and the only output is the flashlight’s LED(s).

I’ve been really enjoying learning the Anduril UI. Part of it is that it’s learning something in an entirely new realm—clicks and flashes. So not only is it memorizing and committing to muscle memory, it’s in a domain where I haven’t done that before. (I guess something like a Casio watch has some similarities, but Anduril complexity is way above Casio’s, so much that it feels completely new.)

To give you an idea, here are state diagrams that document how to get to different modes and sub-modes. The numbers show how many clicks, while “C” means all clicks, and “H” means hold the last click. So in question and answer posts, you’ll see things like “it’s 3C to get to battery check mode” or “3H to get to the strobe modes, and then 2C to switch between the modes”.

*[Image not included in the current archive. Images may be included in the future.]*

*[Image not included in the current archive. Images may be included in the future.]*

My first Anduril 2 light is the lovely [Wurkkos TS10 SG](https://wurkkos.com/collections/ts10-famliy). Some of the things I like about it:

- it’s tiny
- with Anduril, you can configure an *incredibly* low standby mode
- it’s hard to figure out how to use well—learning curves ftw!

Here are a bunch of random things I’ve learned about the new fancy flashlights:

- they’re fun
- the dramatic difference between a very low floor and very bright ceiling brightness means you’ll temporarily blind yourself if you’re not careful when you’re looking down the barrel of the flashlight
- Claude and ChatGPT can tell you all about the Anduril 2 UI and how to get to different modes (what other “sekrit” stuff do they know about?!?)
- cool kids never have their flashlight all the way off anymore, just in moonlight or standby mode (with weeks of battery life in that mode)
- flashlights are sized to fit the battery they’re built around; a 14500 battery is the same shape as a AA, so it makes a small palm-sized light; an 18650 battery is bigger, and makes a large palm-sized light
- on batteries, the numbers refer to dimensions: 14500 means 14mm diameter x 50mm length, and 18650 means 18mm diameter x 65mm length.
- some 14500 flashlights (but not all) are “dual-fuel”—they can take either a regular AA battery, or a rechargeable and higher-voltage 14500
- good communities of enthusiasts and help: [r/flashlight](https://reddit.com/r/flashlight) and [Budget Light Forum](https://budgetlightforum.com/) (ToyKeeper’s home turf)
- favorite reviewer: [zeroair](https://zeroair.org/)
- watch for sales, they’re always rotating sale prices

If you’re in the market for a good light, the Wurkkos TS10 SG is a great place to start, **if** you don’t mind a flashlight that’s hard to figure out. On the other hand, seriously, don’t buy it if you don’t like learning curves.

A more practical beauty is the [Olight Baton 4](https://www.olight.com/store/baton-4-powerful-edc-flashlight) (with or without the “Premium” charging case). Very solid, high quality light, with a simple, perfect easy-to-use UI.

An honorable mention goes to these sort-of [generic clip lights](https://www.amazon.com/dp/B0DFWD4C5R). Their UI is okay, not great, but they’re very practical for dog walking, jogging, or biking. 

But not as much fun as an Anduril 2 light! 🙂🔦

---

**Related:**
- [[Peter Kaminski]] (author)
- [[2025]] (year)
- Topics: 

