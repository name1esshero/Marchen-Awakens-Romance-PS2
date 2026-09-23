# Editable video streams recovered from MOVIE.AFS.
MOVIES_DIR ?= movies

.PHONY: movies-export movies-audit

movies-export: prepare-assets
	python3 tools/movies.py export extracted/assets $(MOVIES_DIR)

movies-audit: movies-export
	python3 tools/movies.py audit extracted/assets $(MOVIES_DIR)

# A changed movie source flows through the ordinary relocated archive builder.
build-mod-disc: movies-audit
asset-census: movies-audit
