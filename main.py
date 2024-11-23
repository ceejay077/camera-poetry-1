#!/usr/bin/python3

import time
import signal
import os
from datetime import datetime
import cv2
from gpiozero import LED, Button
from dotenv import load_dotenv
from openai import OpenAI
import replicate
from typing import Optional

# Type hints and class for thermal printer
class AdafruitThermal:
    def __init__(self, serial_port: str, baud_rate: int, timeout: int = 5):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        
    def justify(self, alignment: str) -> None:
        # Implementation would go here
        pass
        
    def println(self, text: Optional[str] = None) -> None:
        # Implementation would go here
        pass
        
    def setLineHeight(self, height: Optional[int] = None) -> None:
        # Implementation would go here
        pass

class PoetryCamera:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client with modern client configuration
        self.openai_client = OpenAI()
        
        # Initialize hardware
        self.printer = AdafruitThermal('/dev/serial0', 9600, timeout=5)
        self.shutter_button = Button(16)
        self.power_button = Button(26, hold_time=2)
        self.led = LED(20)
        
        # Camera settings
        self.camera_index = 0
        self.image_path = '/home/carolynz/CamTest/images/image.jpg'
        
        # Configure prompts
        self.system_prompt = """You are a poet. You specialize in elegant and emotionally impactful poems. 
        You are careful to use subtlety and write in a modern vernacular style. 
        Use high-school level English but MFA-level craft. 
        Your poems are literary but easy to relate to and understand. 
        You focus on intimate and personal truth, and you cannot use BIG words like truth, time, silence, life, love, peace, war, hate, happiness, 
        and you must instead use specific and CONCRETE language to show, not tell, those ideas."""
        
        self.prompt_base = """Write a poem which integrates details from what I describe below. 
        Use the specified poem format. The references to the source material must be subtle yet clear. 
        Focus on a unique and elegant poem and use specific ideas and details.
        You must keep vocabulary simple and use understated point of view."""
        
        self.poem_format = "8 line free verse"
        
        # Set up button handlers
        self.setup_buttons()

    def take_photo(self) -> bool:
        """Take a photo using OpenCV."""
        self.led.blink()
        
        try:
            camera = cv2.VideoCapture(self.camera_index)
            ret, frame = camera.read()
            
            if ret:
                cv2.imwrite(self.image_path, frame)
                print('----- SUCCESS: image saved locally')
                return True
            else:
                print('----- ERROR: Could not capture image.')
                return False
        finally:
            camera.release()
            self.led.off()

    async def generate_caption(self) -> str:
        """Generate image caption using Replicate API."""
        return await replicate.async_run(
            "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
            input={
                "image": open(self.image_path, "rb"),
                "caption": True,
            }
        )

    async def generate_poem(self, image_caption: str) -> str:
        """Generate poem using OpenAI API."""
        prompt = self._generate_prompt(image_caption)
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content

    def _generate_prompt(self, image_description: str) -> str:
        """Generate the complete prompt for the poem."""
        prompt_parts = [
            self.prompt_base,
            f"Poem format: {self.poem_format}",
            f"Scene description: {image_description}"
        ]
        return "\n\n".join(prompt_parts)

    def print_header(self) -> None:
        """Print the receipt header."""
        now = datetime.now()
        self.printer.justify('C')
        self.printer.println('\n')
        self.printer.println(now.strftime('%b %-d, %Y'))
        self.printer.println(now.strftime('%-I:%M %p'))
        
        self.printer.setLineHeight(56)
        self.printer.println()
        self.printer.setLineHeight()
        
        self.printer.println("`'. .'`'. .'`'. .'`'. .'`'. .'`")
        self.printer.println("   `     `     `     `     `   ")

    def print_poem(self, poem: str) -> None:
        """Print the poem with proper formatting."""
        self.printer.justify('L')
        # Assuming wrap_text is imported or defined elsewhere
        self.printer.println(self._wrap_text(poem, 32))

    def print_footer(self) -> None:
        """Print the receipt footer."""
        self.printer.justify('C')
        self.printer.println("   .     .     .     .     .   ")
        self.printer.println("_.` `._.` `._.` `._.` `._.` `._")
        self.printer.println('\n')
        self.printer.println(' This poem was written by AI.')
        self.printer.println()
        self.printer.println('Explore the archives at')
        self.printer.println('poetry.camera')
        self.printer.println('\n\n\n\n')

    def _wrap_text(self, text: str, width: int) -> str:
        """Wrap text to specified width."""
        # Implementation would go here - you might want to use textwrap from standard library
        # or import your existing wrap_text function
        from textwrap import fill
        return fill(text, width=width)

    async def take_photo_and_print_poem(self) -> None:
        """Main function to take photo and generate/print poem."""
        if self.take_photo():
            self.print_header()
            
            caption = await self.generate_caption()
            poem = await self.generate_poem(caption)
            
            print('--------POEM BELOW-------')
            print(poem)
            print('------------------')
            
            self.print_poem(poem)
            self.print_footer()

    def shutdown(self) -> None:
        """Safely shutdown the system."""
        print('shutdown button held for 2s')
        print('shutting down now')
        self.led.off()
        os.system('sudo shutdown -h now')

    def setup_buttons(self) -> None:
        """Set up button handlers."""
        self.shutter_button.when_pressed = self.take_photo_and_print_poem
        self.power_button.when_held = self.shutdown

    def handle_keyboard_interrupt(self, sig, frame) -> None:
        """Handle Ctrl+C gracefully."""
        print('Ctrl+C received, stopping script')
        self.led.off()
        os.kill(os.getpid(), signal.SIGUSR1)

def main():
    """Main entry point for the application."""
    poetry_camera = PoetryCamera()
    
    # Set up signal handler
    signal.signal(signal.SIGINT, poetry_camera.handle_keyboard_interrupt)
    
    # Keep the script running
    signal.pause()

if __name__ == "__main__":
    main()