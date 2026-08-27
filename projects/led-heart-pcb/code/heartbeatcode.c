#define F_CPU 3333333UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdint.h>

// -----------------------------------------------------
// ATtiny1616 pin assignments
// -----------------------------------------------------

#define DATA_PIN   PIN0_bm     // PB0 -> SER
#define CLK_PIN    PIN1_bm     // PB1 -> SRCLK
#define LATCH_PIN  PIN2_bm     // PB2 -> RCLK


// -----------------------------------------------------
// GPIO initialization
// -----------------------------------------------------

void gpio_init(void)
{
    // PB0, PB1, PB2 are outputs
    PORTB.DIRSET = DATA_PIN | CLK_PIN | LATCH_PIN;

    // Start all three signals LOW
    PORTB.OUTCLR = DATA_PIN | CLK_PIN | LATCH_PIN;
}


// -----------------------------------------------------
// Send one bit to the shift registers
// -----------------------------------------------------

void shift_bit(uint8_t bit)
{
    // Set DATA line
    if (bit)
    {
        PORTB.OUTSET = DATA_PIN;
    }
    else
    {
        PORTB.OUTCLR = DATA_PIN;
    }

    // Pulse shift clock
    PORTB.OUTSET = CLK_PIN;
    PORTB.OUTCLR = CLK_PIN;
}


// -----------------------------------------------------
// Send 16 bits to U2 + U3
// -----------------------------------------------------

void write_leds(uint16_t pattern)
{
    // Keep LATCH low while loading data
    PORTB.OUTCLR = LATCH_PIN;

    // Send bit 15 first -> bit 0 last
    for (int8_t i = 15; i >= 0; i--)
    {
        shift_bit((pattern >> i) & 0x01);
    }

    // Pulse LATCH
    // All 16 LED outputs update simultaneously
    PORTB.OUTSET = LATCH_PIN;
    PORTB.OUTCLR = LATCH_PIN;
}


// -----------------------------------------------------
// Turn all LEDs off
// -----------------------------------------------------

void leds_off(void)
{
    write_leds(0x0000);
}


// -----------------------------------------------------
// Turn all LEDs on
// -----------------------------------------------------

void leds_on(void)
{
    write_leds(0xFFFF);
}


// -----------------------------------------------------
// Software brightness control
//
// brightness:
// 0   = off
// 255 = full brightness
// -----------------------------------------------------

void show_brightness(uint16_t pattern,
                     uint8_t brightness,
                     uint16_t duration_ms)
{
    /*
     * Software PWM.
     *
     * Each PWM cycle is approximately 2 ms:
     * 1 ms ON/OFF portions scaled by brightness.
     */

    uint16_t cycles = duration_ms / 2;

    for (uint16_t c = 0; c < cycles; c++)
    {
        // ON portion
        if (brightness > 0)
        {
            write_leds(pattern);

            for (uint8_t i = 0; i < brightness / 16; i++)
            {
                _delay_us(100);
            }
        }

        // OFF portion
        write_leds(0x0000);

        for (uint8_t i = 0; i < (255 - brightness) / 16; i++)
        {
            _delay_us(100);
        }
    }
}


// -----------------------------------------------------
// Fade brightness upward
// -----------------------------------------------------

void fade_up(uint16_t pattern, uint8_t speed)
{
    for (uint16_t brightness = 0;
         brightness <= 255;
         brightness += 5)
    {
        show_brightness(
            pattern,
            (uint8_t)brightness,
            speed
        );
    }
}


// -----------------------------------------------------
// Fade brightness downward
// -----------------------------------------------------

void fade_down(uint16_t pattern, uint8_t speed)
{
    for (int16_t brightness = 255;
         brightness >= 0;
         brightness -= 5)
    {
        show_brightness(
            pattern,
            (uint8_t)brightness,
            speed
        );
    }
}


// -----------------------------------------------------
// Heartbeat animation
// -----------------------------------------------------

void heartbeat(void)
{
    const uint16_t HEART = 0xFFFF;

    // -----------------------------------------
    // First beat: strong
    // "BUM"
    // -----------------------------------------

    fade_up(HEART, 2);

    show_brightness(HEART, 255, 80);

    fade_down(HEART, 2);


    // Very short gap between heart contractions
    _delay_ms(90);


    // -----------------------------------------
    // Second beat: slightly weaker
    // "bum"
    // -----------------------------------------

    for (uint8_t brightness = 0;
         brightness <= 190;
         brightness += 10)
    {
        show_brightness(
            HEART,
            brightness,
            2
        );
    }

    show_brightness(
        HEART,
        190,
        60
    );

    for (int16_t brightness = 190;
         brightness >= 0;
         brightness -= 10)
    {
        show_brightness(
            HEART,
            (uint8_t)brightness,
            2
        );
    }


    // Pause before next heartbeat
    leds_off();
    _delay_ms(650);
}


// -----------------------------------------------------
// Main
// -----------------------------------------------------

int main(void)
{
    gpio_init();

    leds_off();

    _delay_ms(500);

    while (1)
    {
        heartbeat();
    }
}
