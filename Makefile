.DEFAULT_GOAL := build-boot
EE_GCC := .tools/ee-gcc2.96/bin/ee-gcc
BOOT_SOURCES := $(wildcard preserved/boot/*.hex) preserved/boot/layout.json

.PHONY: test inventory verify-camera verify-reference build-boot verify-boot setup-ee verify-ee verify-source-only export-assets prepare-assets build-disc build-mod-disc compare-disc verify-disc

test:
	python3 -m unittest discover -s tests -v
	clang++ -std=c++17 -fsyntax-only candidates/camera_accessors.cpp
	clang++ -std=c++98 -fsyntax-only candidates/ee_camera/probe.cpp

inventory:
	sha256sum -c config/reference.sha256
	python3 tools/bootstrap.py baserom.iso --extract extracted

verify-reference:
	sha256sum -c config/reference.sha256

build/camera_accessors.o: asm/camera_accessors.s
	mkdir -p build
	clang -target mipsel-none-elf -march=mips3 -mabi=32 -c $< -o $@

verify-camera: build/camera_accessors.o
	sha256sum -c config/boot.sha256
	python3 tools/compare_sections.py 'extracted/SLPM_661.56;1' $< config/camera_sections.txt

build-boot: build/SLPM_661.56

build/SLPM_661.56: $(BOOT_SOURCES) build/camera_accessors.o tools/reconstruct_elf.py tools/bootstrap.py
	python3 tools/reconstruct_elf.py build preserved/boot build/camera_accessors.o $@

verify-boot: build-boot verify-camera
	cmp 'extracted/SLPM_661.56;1' build/SLPM_661.56
	@echo 'PASS: full boot ELF is byte-identical (bootstrap reconstruction, not full decompilation)'

verify-source-only:
	python3 tools/check_source_only.py

# Explicit asset research workflow. The output workspace is ignored/reference-derived;
# builds consume that workspace, never the baserom directly.
export-assets:
	python3 tools/assets.py export baserom.iso extracted/assets

prepare-assets:
	python3 tools/assets.py prepare extracted/assets

build-disc:
	python3 tools/assets.py build extracted/assets build/assets-rebuilt.iso

build-mod-disc:
	python3 tools/assets.py build extracted/assets build/assets-modded.iso --relocate --translations localization/messages.json

compare-disc:
	python3 tools/compare_disc.py build/assets-rebuilt.iso

verify-disc: build-disc compare-disc

setup-ee:
	python3 tools/setup_ee_compiler.py

build/ee_camera.o: candidates/ee_camera/probe.cpp candidates/ee_camera/CCamera.h $(EE_GCC) tools/run_ee_probe.py config/ee_compiler.json
	python3 tools/run_ee_probe.py --output $@

build/SLPM_661.56.ee-probe: $(BOOT_SOURCES) build/ee_camera.o tools/reconstruct_elf.py tools/bootstrap.py
	python3 tools/reconstruct_elf.py build preserved/boot build/ee_camera.o $@

verify-ee: build/SLPM_661.56.ee-probe
	sha256sum -c config/boot.sha256
	python3 tools/compare_sections.py 'extracted/SLPM_661.56;1' build/ee_camera.o config/camera_sections.txt
	cmp 'extracted/SLPM_661.56;1' build/SLPM_661.56.ee-probe
	@echo 'PASS: EE GCC candidate sections and full probe ELF match; class/source authenticity remains open'
