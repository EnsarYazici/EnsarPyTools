from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import requests

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Username')
        self.password = TextInput(hint_text='Password', password=True)
        self.login_button = Button(text='Login')
        self.use_button = Button(text='Use', disabled=True)
        
        self.login_button.bind(on_press=self.login)
        self.use_button.bind(on_press=self.use)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_button)
        layout.add_widget(self.use_button)
        
        return layout
    
    def login(self, instance):
        response = requests.post('http://localhost:8000/login', json={
            'username': self.username.text,
            'password': self.password.text
        })
        
        if response.status_code == 200:
            self.use_button.disabled = False
            self.usage_count = response.json()['usage_count']
        else:
            self.use_button.disabled = True
    
    def use(self, instance):
        response = requests.post('http://localhost:8000/use', json={
            'username': self.username.text
        })
        
        if response.status_code == 200:
            self.usage_count -= 1
            if self.usage_count <= 0:
                self.use_button.disabled = True
        else:
            self.use_button.disabled = True

if __name__ == '__main__':
    MyApp().run()
