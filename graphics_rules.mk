# Generated editable texture workspace and non-destructive mod-build staging.
GRAPHICS_DIR ?= graphics
GRAPHICS_OVERRIDES_DIR ?= build/graphics-overrides

.PHONY: graphics-export graphics-audit graphics-stage graphics-rebuild

graphics-export: prepare-assets
	python3 tools/graphics.py export extracted/assets $(GRAPHICS_DIR)

graphics-audit: graphics-export
	python3 tools/graphics.py audit extracted/assets $(GRAPHICS_DIR)

graphics-stage: graphics-export
	python3 tools/graphics.py build extracted/assets $(GRAPHICS_DIR) --overrides-dir $(GRAPHICS_OVERRIDES_DIR)

graphics-rebuild: graphics-stage

# The normal mod-image recipe consumes the generated texture overrides.
build-mod-disc: graphics-stage
