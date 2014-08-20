"""latexout.py

Module for saving all the information about a StarSystem to a LaTeX file for
processing towards a nicely formatted PDF file.
"""

#from ..starsystem import StarSystem

class LatexWriter:
    def __init__(self, starsystem, filename='starsystem.tex'):
        self.starsystem = starsystem
        self.filename = filename

    def write(self):
        # Open the file
        file = open(self.filename, 'w')

        # Write the preamble
        file.write(self.preamble())

        # Write the title page, ToC and first chapter
        file.write(self.title())

        # Write stellar system and star properties
        file.write(self.starsystemprop())

        file.write(self.starprop())

        # Write the overviews
        file.write(self.overviews())

        # Write the end of document
        file.write(self.end())
        # Close the file
        file.close()

    def preamble(self):
        preambulum = """\documentclass[a4paper,12pt,twoside]{scrreprt}

\\usepackage[T1]{fontenc}
\\usepackage[latin1]{inputenc}
\\usepackage[inner=35mm,outer=25mm,top=30mm,bottom=30mm]{geometry}
\\usepackage{float}
\\usepackage[hidelinks]{hyperref}
\\usepackage{booktabs}
\\usepackage{multirow}
\\usepackage[figuresright]{rotating} % For sideways tables
\\usepackage{pdflscape} % For rotation in the PDF
\setkomafont{sectioning}{\\bfseries}

% Activate the following two for nicer fonts
%\\usepackage{charter}
%\\usepackage[bitstream-charter]{mathdesign}

\\usepackage{scrlayer-scrpage}
\pagestyle{scrheadings}

\setcounter{tocdepth}{1}

"""
        return preambulum

    def title(self):
        titelus = """
\\begin{document}
\\title{CAS: Computer-Assisted Starsystem}
\subtitle{A GURPS Star System}
\\author{The Guy in Front of The Computer}
\date{\\today}
\maketitle

\\tableofcontents
\clearpage

\chapter{Summary}
\section{General Description}
% Give a general description, such as the one you could hand out to your players

\section{GM Notes}
% Enter here the GM Notes

"""
        return titelus

    def starsystemprop(self):
        str = """\chapter{The Star System}
\section{Star System Properties}
"""
        numstar = len(self.starsystem.stars)
        str += "Number of stars: {}\\\\ \n".format(numstar)
        age = self.starsystem.getAge()
        str += "Stellar age: {} billion years \n\n".format(age)

        # Only put table (about the properties of the stellar system) if
        # necessary (i.e. more than one star)
        if numstar > 1:
            str += """\\begin{table}[H]
\centering
\\begin{tabular}{"""
            str += 'l' * numstar
            str += "}\n\\toprule \n"
            if numstar == 2:
                header = "Pair A--B \\\\ \n"
            else:
                header = "Pair A--B & Pair A--C \\\\ \n"
            str += "Property & " + header
            str += "\midrule\n"
            # Extract orbit and eccentricities
            oecc = self.starsystem.getOrbits()
            orb = ''
            ecc = ''
            for o, e in oecc:
                orb += ' & {:8.2f}'.format(round(o, 2))
                ecc += ' & {:8.2f}'.format(round(e, 2))
            str += "Orbital Separation [AU] " + orb + ' \\\\ \n'
            str += "Orbital Eccentricity    " + ecc + ' \\\\ \n'
            str += "Orbital Period [d]      "
            for per in self.starsystem.getPeriod():
                str += ' & {:7.1f} '.format(round(per, 1))
            str += " \\\\ \n"
            str += "\\bottomrule\n\end{tabular} \n\end{table}\n\n"
        return str

    def starprop(self):
        str = """\section{Star Properties}
% Number of data columns = Number of stars
\\begin{table}[H]
\centering
\\begin{tabular}{"""
        numstar = len(self.starsystem.stars)
        str += 'l' * (numstar + 1) + '}\n'
        str += '\\toprule\n'
        str += 'Property '
        letters = ['A', 'B', 'C']
        for nst in range(numstar):
            str += '& Star ' + letters[nst] + ' '
        str += '\\\\ \n\midrule\n'

        sequence = 'Sequence   '
        mass = 'Mass       '
        temp = 'Temperature'
        lum = 'Luminosity '
        rad = 'Radius     '
        inner = 'Inner Limit'
        outer = 'Outer Limit'
        snowline = 'Snow line  '
        if numstar > 1:
            fzinner = 'FZ Inner   '
            fzouter = 'FZ Outer   '
        for star in self.starsystem.stars:
            sequence += ' & ' + star.getSequence()
            mass += ' & {:7.2f}'.format(star.getMass())
            temp += ' & {:7.0f}'.format(star.getTemp())
            lum += ' & {:7.4f}'.format(star.getLuminosity())
            rad += ' & {:7.5f}'.format(star.getRadius())
            inner += ' & {:7.2f}'.format(star.getOrbitlimits()[0])
            outer += ' & {:6.1f} '.format(star.getOrbitlimits()[1])
            snowline += ' & {:7.2f}'.format(star.getSnowline())
            if numstar > 1:
                fzinner += ' & {:6.1f} '.format(star.getForbidden()[0])
                fzouter += ' & {:6.1f} '.format(star.getForbidden()[1])
        #for string in [sequence, mass, temp, lum, rad, inner, outer, snowline]:
        #    string += '\\\\ \n'
        eol = ' \\\\ \n'
        sequence += eol
        mass += eol
        temp += eol
        lum += eol
        rad += eol
        inner += eol
        outer += eol
        snowline += eol
        if numstar > 1:
            fzinner += eol
            fzouter += eol

        str += sequence + mass + temp + lum + rad + inner + outer + snowline
        if numstar > 1:
            str += fzinner + fzouter
        str += '\\bottomrule\n\end{tabular} \n\end{table} \n\n'

        return str


    def overviews(self):
        # Gather number of planet systems
        # For each planet system:
        #  - List orbits and occupants
        #  - List terrestrial planet details
        #  - List Moons and Moonlets
        #  - List Asteroid Belts
        str = ''
        letters = ['A', 'B', 'C']
        for star in self.starsystem.stars:
            idx = self.starsystem.stars.index(star)
            lettr = letters[idx]
            ps = star.planetsystem
            oc = ps.getOrbitcontents()
            types = [pl.type() for key, pl in oc.items()]

            title = 'Overview -- Planet System ' + lettr
            str += '\chapter{' + title + '}\n'
            str += '\section{Summary}\n% A small amount of short sentences describing the general feel of this planet system.\n\n'
            str += '\section{Description}\n% A more in-depth description of the planet system.\n\n'
            str += '\section{GM Notes}\n% Notes about the planet system and eventual adventures that can be undertaken.\n\n'
            str += '\\begin{landscape}\n\section{List of Orbits and their Occupants}\n\\begin{table}[H]\n\\begin{tabular}{llllrrrrrrrrr}\n'
            str += '\\toprule\n'
            str += '\multirow{2}{*}{Name} & \multirow{2}{*}{Type} & \multirow{2}{*}{Size} & \multirow{2}{*}{World} & Orbit & O Per. & \multirow{2}{*}{Ecc.} & R$_\mathrm{min}$ & R$_\mathrm{max}$ & \multirow{2}{*}{Moons} & \multirow{2}{*}{Moonlets} & BB Temp. \\\\ \n'
            str += '\cmidrule(lr){5-5} \cmidrule(lr){6-6} \cmidrule(lr){8-8} \cmidrule(lr){9-9} \cmidrule(lr){12-12}\n'
            str += '& & & & \multicolumn{1}{c}{AU} & \multicolumn{1}{c}{Year} & & \multicolumn{1}{c}{AU} & \multicolumn{1}{c}{AU} & & & \multicolumn{1}{c}{K} \\\\ \n'
            str += '\midrule\n'
            planetcounter = 0
            for skey in sorted(oc):
                planetcounter += 1
                str += '<{}-{}> & '.format(lettr, planetcounter)
                str += '{} & '.format(oc[skey].type())
                str += '{} & '.format(oc[skey].getSize())
                str += '{} & '.format(oc[skey].getType())
                str += '{:.2f} & '.format(oc[skey].getOrbit())
                str += '{:.2f} & '.format(oc[skey].getPeriod())
                str += '{:.2f} & '.format(oc[skey].getEcc())
                str += '{:.2f} & '.format(oc[skey].getMinMax()[0])
                str += '{:.2f} & '.format(oc[skey].getMinMax()[1])
                str += '{} & '.format(oc[skey].numMoons())
                str += '{} & '.format(oc[skey].numMoonlets())
                str += '{:.0f}'.format(oc[skey].getBBTemp())
                str += '\\\\ \n'
            str += '\\bottomrule\n\end{tabular}\n\end{table}\n\n'


            sectable = '\\begin{table}[H]\n'
            sectable += '\\begin{tabular}{lrrr}\n'
            sectable += '\\toprule\n'
            sectable += 'Planet & TTE$^1$ & Rot. Per. [d]  & Ax. Tilt [$^\circ$] \\\\ \n'
            sectable += '\midrule\n'
            planetcounter = 0
            secondtable = False
            if 'Terrestrial' in types:
                secondtable = True
            for skey in sorted(oc):
                planetcounter += 1
                if oc[skey].type() is not 'Terrestrial':
                    continue
                sectable += '<{}-{}> & '.format(lettr, planetcounter)
                sectable += '{:.0f} & '.format(oc[skey].getTTE())
                sectable += '{:.2f} & '.format(oc[skey].getRotation())
                sectable += '{}'.format(oc[skey].getAxialTilt())
                sectable += '\\\\ \n'
            sectable += '\\bottomrule\n\end{tabular}\n\n'
            sectable += '\\footnotesize\n'
            sectable += '$^1$ Total Tidal Effect\n\end{table}\n\n'

            if secondtable is True:
                str += sectable

            str += '\end{landscape}\n\n'
        return str


    def end(self):
        return "\n\n\\end{document}"
