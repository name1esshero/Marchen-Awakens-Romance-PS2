.PHONY: test inventory verify-camera verify-reference

test:
	python3 -m unittest discover -s tests -v
	clang++ -std=c++17 -fsyntax-only candidates/camera_accessors.cpp

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
