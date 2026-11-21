[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Kuyukbot1/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Kuyukbot1/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# Saturday 21 November 2026: 42 stories, 6 continents, one front page and a map

Bounty: [news-image-20261121 — "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121)

One 1024×1024 front page drawn in code (`draw.py`, Pillow) summing up the
world's news of Saturday 21 November 2026: 13 illustrated feature cards, a
world map with numbered pins matching the cards, a 29-item ALSO ON list, and
a sources footer. Every story happened or was first reported on 21 November
2026 (stories first reported after the previous day's entry was built and
carried in Saturday's morning papers count, as in the 19/20 Nov entries);
disputed claims are attributed, never stated as fact.

## The 13 features

1. **US · Iran war** — Trump: Iran wants a deal, but not one "acceptable" to him; Araghchi says Tehran still hopes diplomacy can end the war.
2. **Gulf · Iran war** — Saudi-led coalition downs Houthi missiles; Kuwait and Bahrain face new Iranian attacks after the Qeshm strike.
3. **Europe · Espionage** — Denmark expels Russia's defence attache over an alleged plot to kill rapper Kyivstoner.
4. **Europe · Ukraine war** — Russian missile hits Poland as allies drill; eight killed in strikes on Ukraine after the Crimean Bridge attack.
5. **Europe · Justice** — Paris court jails three police over the racist beating of music producer Michel Zecler.
6. **Global · Markets** — Anthropic falls 9% the day after its record IPO.
7. **Asia · Health** — India launches its first home-grown H5N1 chicken vaccine (1–2 rupees a dose).
8. **Asia · Markets** — NSE becomes the world's 5th-largest listed exchange, passing Nasdaq and HKEX.
9. **Oceania · Sport** — Jaiswal and Rahul's 130-run stand puts India on top in Wellington.
10. **Middle East · Iraq** — Iraqi forces move into Kataib Hezbollah's stronghold, Jurf al-Sakhar.
11. **Global · Culture** — GTA VI rakes in $3.79bn in first-day sales.
12. **Global · Diplomacy** — Two veto powers block Grynspan's bid for UN chief in an informal poll.
13. **Africa · Justice** — Kenya's courts face a backlog of 580,000 cases.

## Also on Saturday 21 November (29)

Nvidia's Huang to testify at a Senate hearing; EU approves a €1bn Ukraine
military package and releases a record €7.9bn payment; EU ambassadors set to
clear final Ukraine accession clusters; Israeli airstrike on Bureij camp;
WHO chief demands unrestricted aid entry to Gaza; Pezeshkian calls for energy
subsidy reform; US targets Iran's ship-to-ship transfers; Trump defends
Putin ties and says AI data centres must stay in the US; Melania Trump says
her Christmas wish is another ceasefire; Trump says close to a Mexico deal;
Chile–Philippines free-trade pact at APEC; Sensex rallies 898 pts to
83,919.71; Supreme Court rejects Tamil Nadu's Cauvery plea; Indian man jailed
19+ years in a plot to kill a Sikh leader; Nepal PM to visit India 22–23
Nov; cheetah at Kuno gives birth to four cubs; Japanese forces to use Indian
facilities for live-fire drills; DGCA show-cause notice to SpiceJet; foreign
investors pump a record ₹1.01 lakh crore in November; Cyclone Akvan weakens
into a deep depression; COP31 talks spill into overtime; Hazlewood hints at
quitting if Cummins loses the captaincy; Kenya report warns gangs could
destabilise the 2027 election; Tanzania promises a new constitution by 2029;
US Treasury presses Singapore and Malaysia on Iran sanctions; rights groups
seek action after the ICJ Rohingya ruling; UN warns global hunger is growing;
five Cambodians caught crossing the Thai border through a possible minefield.

Sources: Reuters, AP, AFP, BBC, Al Jazeera, Le Monde, NDTV, ANI, PIB.
Full story-by-story sourcing in `../RESEARCH_21NOV.md`.

## How to run

```sh
python3 draw.py            # redraws entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

`main.ts` (Node 22, stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`; it is deterministic — two runs produce
byte-identical output.
