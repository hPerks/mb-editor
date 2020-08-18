import tkinter as tk
import tkinter.ttk as ttk


class StyledApp(tk.Tk):
    colors = ['#2f2f2f', '#3f3f3f', '#ddaa00', '#ffdb66', '#dbdbdb', '#2f2f2f', '#525252']

    class Entry(tk.Entry):
        def __init__(self, parent, **config):
            defaults = dict(
                justify=tk.CENTER,
                relief='flat',
                font=('Roboto', 12),
                background=StyledApp.colors[1],
                readonlybackground=StyledApp.colors[1],
                insertbackground=StyledApp.colors[4],
                foreground=StyledApp.colors[4],
                highlightthickness=0,
            )
            defaults.update(**config)
            super().__init__(parent, **defaults)

    class Text(tk.Text):
        def __init__(self, parent, **config):
            defaults = dict(
                relief='flat',
                font=('Monaco', 10),
                background=StyledApp.colors[1],
                foreground=StyledApp.colors[4],
                highlightthickness=0,
            )
            defaults.update(**config)
            super().__init__(parent, **defaults)

    def __init__(self):
        super().__init__()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=self.colors[0])
        self.style.configure('TLabel', background=self.colors[0], foreground=self.colors[4], font=('Roboto', 12, 'bold'))
        self.style.configure('TButton', relief='flat', background=self.colors[2], foreground=self.colors[5], font=('Roboto', 12, 'bold'))

        self.style.element_create('Plain.Notebook.tab', 'from', 'default')
        self.style.layout(
            'TNotebook.tab', [(
                'Plain.Notebook.tab', {
                    'sticky': 'news',
                    'children': [(
                        'Notebook.padding', {
                            'sticky': 'news',
                            'side': 'top', 'children': [(
                                'Notebook.focus', {
                                    'sticky': 'news',
                                    'side': 'top', 'children': [(
                                        'Notebook.label', {'side': 'top', 'sticky': ''}
                                    )]
                                }
                            )]
                        }
                    )]
                }
            )]
        )

        self.style.configure('TNotebook', background=self.colors[0], borderwidth=0, relief='flat')
        self.style.configure('TNotebook.Tab', background=self.colors[0], foreground=self.colors[4], borderwidth=0, relief='flat', font=('Roboto', 10))
        self.style.map('TNotebook.Tab', background=[('selected', self.colors[0])])
        self.style.map('TButton', background=[('active', self.colors[3])])

        self.configure(background=self.colors[0])
