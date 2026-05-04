# Makefile for Spectral Causality JMLR paper

TEX = spectral_causality
PDF = $(TEX).pdf
BIB = references.bib

.PHONY: all clean pptx

all: $(PDF) pptx

$(PDF): $(TEX).tex $(BIB)
	pdflatex -interaction=nonstopmode $(TEX).tex
	bibtex $(TEX)
	pdflatex -interaction=nonstopmode $(TEX).tex
	pdflatex -interaction=nonstopmode $(TEX).tex

pptx: spectral_causality_figures.pptx

spectral_causality_figures.pptx: generate_figures_pptx.py figures/*.png
	python3 generate_figures_pptx.py

clean:
	rm -f *.aux *.log *.bbl *.blg *.fls *.fdb_latexmk *.out *.toc \
	      *.synctex.gz *.pdf *.pptx

archive: $(PDF) pptx
	tar czf spectral_causality_jmlr.tar.gz \
	    $(TEX).tex $(BIB) jmlr2e.sty Makefile \
	    generate_figures_pptx.py \
	    figures/ \
	    $(PDF) spectral_causality_figures.pptx
	@echo "Created spectral_causality_jmlr.tar.gz"
