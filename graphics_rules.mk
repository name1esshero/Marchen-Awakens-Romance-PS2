# Generated editable texture workspace and non-destructive mod-build staging.
GRAPHICS_DIR ?= graphics
GRAPHICS_OVERRIDES_DIR ?= build/graphics-overrides
GRAPHICS_COMPOSE_FIT ?= contain
GRAPHICS_COMPOSE_ALPHA_THRESHOLD ?= 1

.PHONY: graphics-export graphics-audit graphics-stage graphics-rebuild graphics-compose

graphics-export: prepare-assets
	python3 tools/graphics.py export extracted/assets $(GRAPHICS_DIR)

graphics-audit: graphics-export
	python3 tools/graphics.py audit extracted/assets $(GRAPHICS_DIR)

graphics-stage: graphics-export
	python3 tools/graphics.py build extracted/assets $(GRAPHICS_DIR) --overrides-dir $(GRAPHICS_OVERRIDES_DIR)

graphics-rebuild: graphics-stage

# Deterministically place a transparent generated PNG layer on a recovered TGA.
# Set the paths and optional regions on the make command line; Japanese bases
# are inputs only and the output should normally use the sibling _eng.tga name.
graphics-compose:
	python3 tools/graphics_compose.py --base "$(GRAPHICS_COMPOSE_BASE)" --overlay "$(GRAPHICS_COMPOSE_OVERLAY)" --output "$(GRAPHICS_COMPOSE_OUTPUT)" --fit $(GRAPHICS_COMPOSE_FIT) --alpha-threshold $(GRAPHICS_COMPOSE_ALPHA_THRESHOLD) $(if $(strip $(GRAPHICS_COMPOSE_REGION)),--region $(GRAPHICS_COMPOSE_REGION),) $(if $(strip $(GRAPHICS_COMPOSE_CLEAR_REGION)),--clear-region $(GRAPHICS_COMPOSE_CLEAR_REGION),) $(if $(filter 1,$(GRAPHICS_COMPOSE_REPLACE)),--replace,)

# The normal mod-image recipe consumes the generated texture overrides.
build-mod-disc: graphics-stage
