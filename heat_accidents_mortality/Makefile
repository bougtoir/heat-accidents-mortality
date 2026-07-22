PY = python3
S  = scripts

.PHONY: all us japan figures clean data_us data_jp

all: us japan figures

## --- data building (downloads public sources into data/raw) ---
data_us:
	$(PY) $(S)/build_fars.py
	$(PY) $(S)/build_temperature.py
	$(PY) $(S)/build_controls.py
	$(PY) $(S)/build_cdc_heat.py

data_jp:
	$(PY) $(S)/build_japan.py

## --- analysis ---
us: data_us
	$(PY) $(S)/analyze_us.py

japan: data_jp
	$(PY) $(S)/analyze_japan.py

## --- figures + manuscript ---
figures:
	$(PY) $(S)/figures_us.py
	$(PY) $(S)/figures_japan.py

manuscript:
	$(PY) $(S)/make_manuscript.py

test:
	$(PY) -m pytest -q tests

clean:
	rm -f data/processed/*.csv output/*.txt output/figures/*
