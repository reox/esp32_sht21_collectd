BOARD := /dev/ttyUSB0
BAUD := 115200
AMPY := ampy -p ${BOARD} -b ${BAUD}

IMAGE := esp32-20181110-v1.9.4-683-gd94aa577a.bin


.PHONY: upload getconfig shell flash

upload:
	${AMPY} put main.py
	${AMPY} put bmp280.py
	${AMPY} put sht21.py
	${AMPY} put weather.py
	${AMPY} put collectd.py
	${AMPY} put boot.py
	${AMPY} reset

getconfig:
	${AMPY} get config.py > config.py

shell:
	screen ${BOARD} ${BAUD}

flash: ${IMAGE}
	esptool --chip esp32 --port ${BOARD} write_flash -z 0x1000 $<
