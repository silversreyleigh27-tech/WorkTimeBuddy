
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.timepicker import TimePicker  # This is not a default widget, will simulate via TextInput for now
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window

from datetime import datetime, timedelta
import pytz

class TimeCalcLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(TimeCalcLayout, self).__init__(orientation='vertical', **kwargs)
        
        self.time_input = TextInput(hint_text='Enter time (HH:MM)', multiline=False, size_hint=(1, 0.1))
        self.add_widget(self.time_input)
        
        self.direction_spinner = Spinner(
            text='Start → End',
            values=['Start → End', 'End → Start'],
            size_hint=(1, 0.1)
        )
        self.add_widget(self.direction_spinner)

        self.zone_toggle = ToggleButton(text='Time Zone: IST', size_hint=(1, 0.1))
        self.zone_toggle.bind(on_press=self.toggle_zone)
        self.add_widget(self.zone_toggle)
        self.timezone = 'Asia/Kolkata'

        self.format_toggle = ToggleButton(text='Format: 24-Hour', size_hint=(1, 0.1))
        self.format_toggle.bind(on_press=self.toggle_format)
        self.add_widget(self.format_toggle)
        self.format_12 = False

        self.calc_btn = Button(text='Calculate', size_hint=(1, 0.1))
        self.calc_btn.bind(on_press=self.calculate)
        self.add_widget(self.calc_btn)

        self.result = Label(text='', size_hint=(1, 0.2))
        self.add_widget(self.result)

    def toggle_zone(self, instance):
        if self.timezone == 'Asia/Kolkata':
            self.timezone = 'Australia/Sydney'
            self.zone_toggle.text = 'Time Zone: AEST'
        else:
            self.timezone = 'Asia/Kolkata'
            self.zone_toggle.text = 'Time Zone: IST'

    def toggle_format(self, instance):
        self.format_12 = not self.format_12
        self.format_toggle.text = 'Format: 12-Hour' if self.format_12 else 'Format: 24-Hour'

    def calculate(self, instance):
        try:
            tz = pytz.timezone(self.timezone)
            input_time = datetime.strptime(self.time_input.text.strip(), '%H:%M')
            now = datetime.now(tz)
            input_time = tz.localize(datetime(now.year, now.month, now.day, input_time.hour, input_time.minute))

            delta = timedelta(hours=9, minutes=9)

            if self.direction_spinner.text == 'Start → End':
                result_time = input_time + delta
            else:
                result_time = input_time - delta

            if self.format_12:
                fmt = '%I:%M %p'
            else:
                fmt = '%H:%M'

            self.result.text = f'Result: {result_time.strftime(fmt)} ({self.zone_toggle.text.split(": ")[1]})'
        except Exception as e:
            self.result.text = 'Invalid input. Please enter in HH:MM format.'

class TimeCalcApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return TimeCalcLayout()

if __name__ == '__main__':
    TimeCalcApp().run()
