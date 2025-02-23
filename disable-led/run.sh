#!/bin/bash

disable_leds() {
    echo "Disabling Raspberry Pi LEDs..."
    echo 0 | tee /sys/class/leds/led1/brightness
    echo 0 | tee /sys/class/leds/led0/brightness
    echo "dtparam=pwr_led_trigger=none" >> /boot/config.txt
    echo "dtparam=pwr_led_activelow=off" >> /boot/config.txt
    echo "dtparam=act_led_trigger=none" >> /boot/config.txt
    echo "dtparam=act_led_activelow=off" >> /boot/config.txt
}

enable_leds() {
    echo "Restoring LED settings..."
    echo 1 | tee /sys/class/leds/led1/brightness
    echo 1 | tee /sys/class/leds/led0/brightness
    sed -i '/dtparam=pwr_led_trigger=none/d' /boot/config.txt
    sed -i '/dtparam=pwr_led_activelow=off/d' /boot/config.txt
    sed -i '/dtparam=act_led_trigger=none/d' /boot/config.txt
    sed -i '/dtparam=act_led_activelow=off/d' /boot/config.txt
    echo "LED settings restored. Reboot may be required."
}

trap enable_leds EXIT  # When the add-on stops, turn LEDs back on.

disable_leds
sleep infinity  # Keeps the add-on running.
