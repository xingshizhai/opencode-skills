#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char *TAG = "hello_world";

// Default LED pin (adjust for your board)
// ESP32-DevKitC: GPIO2
// ESP32-S3-DevKitC: GPIO48 (RGB LED) or GPIO2
// ESP32-C3-DevKitC: GPIO8 (RGB LED)
#define LED_PIN 2

void app_main(void)
{
    ESP_LOGI(TAG, "Hello from ESP32!");
    printf("ESP32 Hello World!\n");
    
    // Configure LED pin
    gpio_reset_pin(LED_PIN);
    gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);
    
    int led_state = 0;
    
    while (1) {
        // Toggle LED
        led_state = !led_state;
        gpio_set_level(LED_PIN, led_state);
        
        // Print message
        ESP_LOGI(TAG, "LED state: %s", led_state ? "ON" : "OFF");
        printf("LED toggled: %d\n", led_state);
        
        // Wait 1 second
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}