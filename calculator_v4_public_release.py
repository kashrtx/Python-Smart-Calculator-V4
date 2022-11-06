import PySimpleGUI as sg
import speech_recognition as sr
from math import sqrt

"""
--------------------------------------------------------------------------------
Smart Python Calculator V4 Final Release (Public Release)
--------------------------------------------------------------------------------
By: Kaushal Bhingaradia
Date: November 06, 2022

Description: Hello, and Welcome to Smart Python Calculator V4! The calculator is
now an interactive GUI instead of a CMD terminal, where you can can input from 
the GUI  buttons, keyboard input (click the box where the numbers output), and 
from voice recognition (using the MIC button). 
________________________________________________________________________________
"""

# initialize variables
result = ''
answer = ''
char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '**',
        'sqrt', '/', '(', ')', '.']

# settings for buttons
wht = {'size': (7, 2), 'font': ('Times New Roman', 24),
       'button_color': ("black", "#FFFFFF")}
rd = {'size': (7, 2), 'font': ('Times New Roman', 24),
      'button_color': ("black", "#FFCCCB")}
ylw = {'size': (65, 4), 'font': ('Times New Roman', 24),
       'button_color': ("black", "#FFCC00"), 'focus': True}
prple = {'size': (7, 2), 'font': ('Times New Roman', 24),
         'button_color': ("black", "#CBC3E3")}
grn = {'size': (4, 1), 'font': ('Times New Roman', 24),
       'button_color': ("black", "#00FF00")}

# each list is a row that corresponds to the GUI
layout = [
    [sg.Text('By: Kaushal Bhingaradia 2022')],
    [sg.Multiline(size=(65, 4), key='OUTPUT'), sg.Button('MIC', **grn)],
    [sg.Button('0', **wht), sg.Button('Clear', **rd), sg.Button('.', **wht),
     sg.Button('+', **prple)],
    [sg.Button('7', **wht), sg.Button('8', **wht), sg.Button('9', **wht),
     sg.Button('-', **prple)],
    [sg.Button('4', **wht), sg.Button('5', **wht), sg.Button('6', **wht),
     sg.Button('*', **prple)],
    [sg.Button('1', **wht), sg.Button('2', **wht), sg.Button('3', **wht),
     sg.Button('/', **prple)],
    [sg.Button('**', **prple), sg.Button('sqrt', **prple),
     sg.Button('(', **prple), sg.Button(')', **prple)],
    [sg.Button('=', **ylw)]

]

# create window
window = sg.Window('Smart Python Calculator V4 (Final Release)',
                   icon='app.ico', layout=layout, background_color="#ADD8E6",
                   size=(600, 740))


# Use microphone to get/store text and process it for calculations.
def voice_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, 5)
        try:

            text = r.recognize_google(audio, language='en-US').lower()

            # This is the filter for the voice recognition
            #  Ensures that the proper operators are calculated and
            # certain terms avoided

            if 'square root' in text:
                text = text.replace('square root', '(')
                text += ')**(0.5)'
            if 'sqrt' in text:
                text = text.replace('sqrt', '(')
                text += ')**(0.5)'
            if '√' in text:
                text = text.replace('√', '(')
                text += ')**(0.5)'
            if 'times' in text:
                text = text.replace('times', '*')
            if 'divided' in text:
                text = text.replace('divided', '/')
            if 'ratio' in text:
                text = text.replace('ratio', '/')
            if 'ratioed' in text:
                text = text.replace('ratioed', '/')
            if 'multiplied' in text:
                text = text.replace('multiplied', '*')
            if 'thousand' in text:
                text = text.replace('thousand', '*10**3')
            if 'million' in text:
                text = text.replace('million', '*10**6')
            if 'billion' in text:
                text = text.replace('billion', '*10**9')
            if 'power' in text:
                text = text.replace('power', '**')
            if '^' in text:
                text = text.replace('^', '**')
            if 'remainder' in text:
                text = text.replace('remainder', '%')
            if 'modulus' in text:
                text = text.replace('modulus', '%')
            if 'integer division' in text:
                text = text.replace('integer division', '//')
            if 'plus' in text:
                text = text.replace('plus', '+')
            if 'sum' in text:
                text = text.replace('sum', '+')
            if 'some' in text:
                text = text.replace('some', '+')
            if 'subtracted' in text:
                text = text.replace('subtracted', '-')
            if 'minus' in text:
                text = text.replace('minus', '-')
            if 'too' in text:
                text = text.replace('too', '')
            if 'to' in text:
                text = text.replace('to', '')
            if 'the' in text:
                text = text.replace('the', '')
            if 'by' in text:
                text = text.replace('by', '')
            if 'of' in text:
                text = text.replace('of', '')
            if ',' in text:
                text = text.replace(',', '')
            if 'five' in text:
                text = text.replace('five', '5')
            if 'point' in text:
                text = text.replace('point', '.')
            if 'decimal' in text:
                text = text.replace('decimal', '.')
            # this should be dead last cause it can break operator names that
            # have a in it.
            if 'a' in text:
                text = text.replace('a', '')

            # get rid of anything except numbers
            for words in text:
                if words.isalpha():
                    text = words.replace(words, '')

            # return the processed text
            return text.strip()

        except sr.UnknownValueError:
            sg.Popup('Error: Did not recognize what was said!',
                     keep_on_top=True)
        except sr.WaitTimeoutError:
            sg.Popup('Error: Voice Recognition Timeout!', keep_on_top=True)
        except sr.RequestError as e:
            sg.Popup(f"Error: Could not request results from Google Speech "
                     f"Recognition service; {e}", keep_on_top=True)


# events
while True:
    event, values = window.read()
    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    else:
        # input by keyboard is first priority
        if values['OUTPUT']:
            result = values['OUTPUT'].strip()
        # check buttons pressed as 2nd
        if event in char:
            result += event.strip()
            window['OUTPUT'].Update(result)

        # Clear the calculations
    if event == 'Clear':
        result = ''
        window['OUTPUT'].Update(result)

    if event == '=':
        try:
            answer = eval(result)
            answer = str(round(float(answer), 3))
            result = answer.strip()
            window['OUTPUT'].Update(result)
        except NameError:
            result = ''
            window['OUTPUT'].Update(result)
        except SyntaxError:
            result = ''
            window['OUTPUT'].Update(result)
        except ZeroDivisionError:
            result = ''
            window['OUTPUT'].Update(result)
            sg.Popup('Error: Cannot divide by 0!', keep_on_top=True)
        except OverflowError:
            result = ''
            window['OUTPUT'].Update(result)
            sg.Popup('Error: Calculated result is too large!', keep_on_top=True)
        except TypeError:
            result = ''
            window['OUTPUT'].Update(result)
            sg.Popup('Error: Forgot to add operator next to '
                     'parentheses!', keep_on_top=True)
        except AttributeError:
            result = ''
            window['OUTPUT'].Update(result)

    if event == 'MIC':
        try:
            result += voice_recognition()
            window['OUTPUT'].Update(result)
        except TypeError:
            sg.Popup('Error: Data Type Error!', keep_on_top=True)
        except sr.WaitTimeoutError:
            sg.Popup('Error: Voice Recognition Timeout!', keep_on_top=True)

window.close()
