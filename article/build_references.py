"""
Build a working APA 7 reference list and BibTeX file from LITERATURE_MATRIX.csv.

The script fetches metadata from Crossref for entries with a DOI. Entries
without a DOI (books, legislation, standards) are added manually at the end.

    python build_references.py

Outputs:
    REFERENCES_APA.md
    REFERENCES.bib
"""

import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(HERE, "LITERATURE_MATRIX.csv")
OUT_APA = os.path.join(HERE, "REFERENCES_APA.md")
OUT_BIB = os.path.join(HERE, "REFERENCES.bib")
UA = "RCC-GeoDB-ReferenceBuilder/1.0 (mailto:research@example.org)"

AUTHOR_OVERRIDES = {
    "10.1080/01944369408975579": [{"family": "Budić", "given": "Zorica D."}],
    "10.2307/977254": [{"family": "Nedović-Budić", "given": "Zorica"},
                        {"family": "Godschalk", "given": "David R."}],
    "10.1002/j.1681-4835.2004.tb00117.x": [{"family": "Ndou", "given": "Valentina"}],
    "10.1007/978-3-031-88653-9_61": [
        {"family": "Hijazi", "given": "Ihab H."},
        {"family": "Qanazi", "given": "Saleh"},
        {"family": "El Meouche", "given": "Rani"},
    ],
    "10.1680/muen.13.00008": [
        {"family": "Yıldırım", "given": "Volkan"},
        {"family": "Yomralıoğlu", "given": "Tahsin"},
        {"family": "Nişancı", "given": "Recep"},
        {"family": "İnan", "given": "Halilibrahim"},
    ],
    "10.3846/ijspm.2018.445": [
        {"family": "Kaganova", "given": "Olga"},
        {"family": "Telgarsky", "given": "Jeffrey"},
    ],
    "10.1080/14498596.2011.567438": [
        {"family": "Grus", "given": "L."},
        {"family": "Crompvoets", "given": "J."},
        {"family": "Bregt", "given": "A. K."},
        {"family": "van Loenen", "given": "B."},
        {"family": "Delgado Fernandez", "given": "Tatiana"},
        {"family": "Vandenbroucke", "given": "D."},
    ],
    "10.1787/e57ce301-en": [{"family": "OECD", "given": ""}],
    "10.1016/j.jmse.2021.03.003": [
        {"family": "Deng", "given": "Tianhu"},
        {"family": "Zhang", "given": "Keren"},
        {"family": "Shen", "given": "Zuo-Jun M."},
    ],
}

TITLE_FIXES = {
    "10.2307/25148625": "Design science in information systems research",
    "10.25300/MISQ/2013/37.2.01": "Positioning and presenting design science research for maximum impact",
    "10.3846/ijspm.2018.445": "Management of capital assets by local governments: An assessment and benchmarking survey",
}

JOURNAL_FIXES = {
    "10.1002/j.1681-4835.2006.tb00176.x": "The Electronic Journal of Information Systems in Developing Countries",
    "10.1002/j.1681-4835.2004.tb00117.x": "The Electronic Journal of Information Systems in Developing Countries",
}

YEAR_OVERRIDES = {
    "10.1080/24749508.2024.2373489": 2024,
}

SKIP_DOIS = {
    "10.1080/24749508.2024.2373489",
    "10.1016/j.jmse.2021.03.003",
}


def clean(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def initials(given):
    if not given:
        return ""
    parts = re.split(r"\s+", given.strip())
    out = []
    for part in parts:
        if not part:
            continue
        if "-" in part:
            out.append("-".join(p[0].upper() + "." for p in part.split("-") if p))
        else:
            out.append(part[0].upper() + ".")
    return " ".join(out)


def apa_authors(authors):
    names = []
    for a in authors:
        family = clean(a.get("family", ""))
        given = initials(a.get("given", ""))
        if family:
            names.append(f"{family}, {given}".strip().rstrip(","))
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]}, & {names[1]}"
    return ", ".join(names[:-1]) + ", & " + names[-1]


def bib_authors(authors):
    names = []
    for a in authors:
        family = clean(a.get("family", ""))
        given = clean(a.get("given", ""))
        if family:
            names.append(f"{family}, {given}".strip().rstrip(","))
    return " and ".join(names)


def fetch_crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))["message"]
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code == 429:
                time.sleep(2 + attempt * 2)
                continue
            raise
    raise last


def main():
    with open(MATRIX, encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    apa = []
    bib = []
    seen_dois = set()

    for row in rows:
        doi = (row.get("doi") or "").strip()
        if not doi or doi in seen_dois or doi in SKIP_DOIS:
            continue
        seen_dois.add(doi)
        if doi in SKIP_DOIS:
            continue
        try:
            m = fetch_crossref(doi)
        except Exception as exc:
            print(f"WARN: {doi}: {exc}", file=sys.stderr)
            continue

        authors = AUTHOR_OVERRIDES.get(doi, m.get("author", []))
        year = YEAR_OVERRIDES.get(
            doi,
            (m.get("published-print") or m.get("issued") or {})
            .get("date-parts", [[None]])[0][0],
        )
        title = TITLE_FIXES.get(doi, clean((m.get("title") or [""])[0])).rstrip(".")
        journal = JOURNAL_FIXES.get(doi, clean((m.get("container-title") or [""])[0]))
        volume = clean(m.get("volume", ""))
        issue = clean(m.get("issue", ""))
        pages = clean(m.get("page", ""))
        doi_url = "https://doi.org/" + doi

        author_apa = apa_authors(authors)
        if journal:
            source = f"*{journal}*"
            if volume:
                source += f", {volume}"
                if issue:
                    source += f"({issue})"
            if pages:
                source += f", {pages}"
            entry = f"{author_apa} ({year}). {title}. {source}. {doi_url}"
        else:
            entry = f"{author_apa} ({year}). {title}. {doi_url}"
        apa.append(entry)

        key = re.sub(r"[^A-Za-z0-9]", "", (authors[0].get("family", "ref") if authors else "ref")).lower()
        key += str(year) if year else ""
        if not key:
            key = "ref" + row["id"]
        # avoid duplicate keys
        base = key
        n = 2
        while any(b.startswith("@" ) and "{" + key + "," in b for b in bib):
            key = base + chr(ord("a") + n)
            n += 1

        bib_entry = [
            f"@article{{{key},",
            f"  author = {{{bib_authors(authors)}}},",
            f"  title = {{{title}}},",
        ]
        if journal:
            bib_entry.append(f"  journal = {{{journal}}},")
        if year:
            bib_entry.append(f"  year = {{{year}}},")
        if volume:
            bib_entry.append(f"  volume = {{{volume}}},")
        if issue:
            bib_entry.append(f"  number = {{{issue}}},")
        if pages:
            bib_entry.append(f"  pages = {{{pages}}},")
        bib_entry.append(f"  doi = {{{doi}}},")
        bib_entry.append("}")
        bib.append("\n".join(bib_entry))
        time.sleep(0.1)

    manual_apa = [
        "Deng, T., Zhang, K., & Shen, Z.-J. M. (2021). A systematic review of a digital twin city: A new pattern of urban governance toward smart cities. *Journal of Management Science and Engineering*, 6(2), 125–134. https://doi.org/10.1016/j.jmse.2021.03.003",
        "Rajshahi City Corporation. (n.d.). *Home*. http://erajshahi.portal.gov.bd/",
        "Faridatul, M. I., Islam, M., Joy, M. J. H., Wakil, M. A., Rahman, M. M., & Sarker, D. (2024). Impact of greenery and waterbody on the cooling of city’s environment: A case of Rajshahi City. *Geology, Ecology, and Landscapes*, 9(3), 1065–1086. https://doi.org/10.1080/24749508.2024.2373489",
        "Local Government (City Corporation) Act, 2009. (Bangladesh).",
        "Right to Information Act, 2009. (Bangladesh).",
        "Government of Bangladesh. (2021). *Smart Bangladesh Vision 2041*. Dhaka: Government of Bangladesh.",
        "International Organization for Standardization. (2014). *ISO 55000:2014 Asset management — Overview, principles and terminology*. Geneva: ISO.",
        "Institute of Public Works Engineering Australasia. (2020). *International Infrastructure Management Manual (IIMM)*. Sydney: IPWEA.",
        "Lipsky, M. (1980). *Street-level bureaucracy: Dilemmas of the individual in public services*. New York: Russell Sage Foundation.",
        "Moore, M. H. (1995). *Creating public value: Strategic management in government*. Cambridge, MA: Harvard University Press.",
        "Scott, J. C. (1998). *Seeing like a state: How certain schemes to improve the human condition have failed*. New Haven, CT: Yale University Press.",
    ]

    with open(OUT_APA, "w", encoding="utf-8") as handle:
        handle.write("# References (working APA 7 list)\n\n")
        handle.write("Generated from `LITERATURE_MATRIX.csv` and Crossref metadata. "
                     "Check every entry against the publisher record before submission.\n\n")
        for entry in apa + manual_apa:
            handle.write(f"- {entry}\n")

    manual_bib = [
        "@article{deng2021, author={Deng, Tianhu and Zhang, Keren and Shen, Zuo-Jun M.}, title={A Systematic Review of a Digital Twin City: A New Pattern of Urban Governance Toward Smart Cities}, journal={Journal of Management Science and Engineering}, volume={6}, number={2}, pages={125--134}, year={2021}, doi={10.1016/j.jmse.2021.03.003}}",
        "@misc{rcc_nd, author={{Rajshahi City Corporation}}, title={Home}, howpublished={\\url{http://erajshahi.portal.gov.bd/}}, year={n.d.}}",
        "@article{faridatul2024, author={Faridatul, Mst Ilme and Islam, Muhaiminul and Joy, Md. Jahid Hasan and Wakil, Md. Abdul and Rahman, Md. Mostafizur and Sarker, Dulal}, title={Impact of Greenery and Waterbody on the Cooling of City’s Environment: A Case of Rajshahi City}, journal={Geology, Ecology, and Landscapes}, volume={9}, number={3}, pages={1065--1086}, year={2024}, doi={10.1080/24749508.2024.2373489}}",
        "@book{scott1998, author={Scott, James C.}, title={Seeing Like a State: How Certain Schemes to Improve the Human Condition Have Failed}, publisher={Yale University Press}, address={New Haven, CT}, year={1998}}",
        "@book{moore1995, author={Moore, Mark H.}, title={Creating Public Value: Strategic Management in Government}, publisher={Harvard University Press}, address={Cambridge, MA}, year={1995}}",
        "@book{lipsky1980, author={Lipsky, Michael}, title={Street-Level Bureaucracy: Dilemmas of the Individual in Public Services}, publisher={Russell Sage Foundation}, address={New York}, year={1980}}",
        "@misc{bd_citycorporation2009, title={Local Government (City Corporation) Act, 2009}, year={2009}, country={Bangladesh}}",
        "@misc{bd_rti2009, title={Right to Information Act, 2009}, year={2009}, country={Bangladesh}}",
        "@misc{bd_smart2041, title={Smart Bangladesh Vision 2041}, year={2021}, organization={Government of Bangladesh}}",
        "@misc{iso55000, title={ISO 55000:2014 Asset Management — Overview, Principles and Terminology}, year={2014}, organization={International Organization for Standardization}}",
        "@book{iimm2020, title={International Infrastructure Management Manual}, year={2020}, organization={Institute of Public Works Engineering Australasia}}",
    ]

    with open(OUT_BIB, "w", encoding="utf-8") as handle:
        handle.write("\n\n".join(bib + manual_bib) + "\n")

    print(f"Wrote {OUT_APA} ({len(apa) + len(manual_apa)} entries)")
    print(f"Wrote {OUT_BIB} ({len(bib) + len(manual_bib)} entries)")


if __name__ == "__main__":
    main()
