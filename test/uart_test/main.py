
import machine
import time

def main(uart_bus):

    while True:
        if uart_bus.any():
            print(uart_bus.readall())
        time.sleep_ms(100)


if __name__ == '__main__':
    print("Starting uart test program")
    uart_bus = machine.UART(1, baudrate=9600, parity=None, stop=1)
    main(uart_bus)
    uart_bus.deinit()
