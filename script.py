import serial
from pynput import keyboard
import time

ARDUINO_PORT = 'COM4'
BAUD_RATE = 9600

ser = None

def on_press(key):
    """Called whenever a key is pressed"""
    try:
        # Only process keys that have a 'char' attribute (printable characters)
        if hasattr(key, 'char') and key.char:
            key_char = key.char
            print(f"Key pressed: {key_char}")
            
            # Send to Arduino
            if ser and ser.is_open:
                ser.write(key_char.encode())
                
                # Read response from Arduino
                time.sleep(0.05)
                while ser.in_waiting:
                    response = ser.readline().decode().strip()
                    if response:
                        print(f"Arduino: {response}")
        else:
            # Silently ignore special keys (backspace, ctrl, shift, etc.)
            pass
    
    except Exception as e:
        print(f"Error handling key: {e}")

def on_release(key):
    """Called when a key is released"""
    if key == keyboard.Key.esc:
        print("\nESC pressed - Exiting...")
        return False

def main():
    global ser
    
    print("Connecting to Arduino...")
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Connected to Arduino on {ARDUINO_PORT}")
        
        time.sleep(0.5)
        while ser.in_waiting:
            print(ser.readline().decode().strip())
        
        print("\n=== Motor Control Active ===")
        print("Press any key to activate motor")
        print("Press ESC to exit\n")
        
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        
        print("Keyboard listener stopped")
    
    except serial.SerialException as e:
        print(f"Error: Could not connect to Arduino on {ARDUINO_PORT}")
        print(f"Details: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    main()