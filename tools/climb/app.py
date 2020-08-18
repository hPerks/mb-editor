import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import job
import style
from amble.utils import path


class App(style.StyledApp):
    version = '1.1'

    def __init__(self):
        super().__init__()

        self.title('CLIMB v{}'.format(self.version))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self)

        self.label_title = ttk.Label(self.frame, text='CLIMB v{}'.format(self.version), font=('Roboto', 24, 'bold'), foreground='#da0', justify=tk.CENTER)

        self.tabs = ttk.Notebook(self.frame)
        self.tab_install = ttk.Frame(self.tabs)
        self.tab_bundle = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_install, text='Install')
        self.tabs.add(self.tab_bundle, text='Bundle')

        self.label_source_zip = ttk.Label(self.tab_install, text='Install from:', justify=tk.CENTER)
        self.entry_source_zip = self.Entry(self.tab_install)
        self.button_source_zip = ttk.Button(self.tab_install, text='Browse', command=self.press_button_source_zip)

        self.label_arrow_install = ttk.Label(self.tab_install, text='\u21e9', justify=tk.CENTER, font=('Roboto', 36))

        self.label_missions_dir = ttk.Label(self.tab_install, text='Missions folder:')
        self.entry_missions_dir = self.Entry(self.tab_install)
        self.entry_missions_dir.insert(0, '~/data/missions/custom')
        self.entry_missions_dir.xview(tk.END)
        self.button_missions_dir = ttk.Button(self.tab_install, text='Browse', command=self.press_button_missions_dir)

        self.button_install = ttk.Button(self.tab_install, text='Install!', command=self.press_button_install)

        self.label_mission_file = ttk.Label(self.tab_bundle, text='Your mission:', justify=tk.CENTER)
        self.entry_mission_file = self.Entry(self.tab_bundle)
        self.button_mission_file = ttk.Button(self.tab_bundle, text='Browse', command=self.press_button_mission_file)

        self.label_arrow_bundle = ttk.Label(self.tab_bundle, text='\u21e9', justify=tk.CENTER, font=('Roboto', 36))

        self.label_dest_dir = ttk.Label(self.tab_bundle, text='Destination:')
        self.entry_dest_dir = self.Entry(self.tab_bundle)
        self.button_dest_dir = ttk.Button(self.tab_bundle, text='Browse', command=self.press_button_dest_dir)

        self.button_bundle = ttk.Button(self.tab_bundle, text='Bundle!', command=self.press_button_bundle)

        self.frame_status = ttk.Frame(self.frame)
        self.scrollbar_status_v = ttk.Scrollbar(self.frame_status, orient='vertical')
        self.text_status = self.Text(self.frame_status, state='disabled', width=0, height=0, yscrollcommand=self.scrollbar_status_v.set)

        self.label_credits = ttk.Label(self.frame, text='made with \u2665 by hPerks, using AMBLE (github.com/omaitzen/amble)', font=('Roboto', 10), foreground='#525252')

        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.grid_columnconfigure(0, weight=1, uniform='joj')
        self.frame.grid_columnconfigure(1, weight=1, uniform='joj')

        self.label_title.grid(row=0, column=0, columnspan=2, pady=(18, 12))

        self.tabs.grid(row=1, column=0, padx=(12, 6), pady=(12, 12))

        self.tab_install.grid_columnconfigure(0, weight=1, uniform='hoh sis')
        self.tab_install.grid_columnconfigure(1, weight=1, uniform='hoh sis')
        self.tab_install.grid_columnconfigure(2, weight=1, uniform='hoh sis')
        self.tab_install.grid_rowconfigure(1, uniform='u')
        self.tab_install.grid_rowconfigure(4, uniform='u')

        self.label_source_zip.grid(row=0, column=0, columnspan=3, padx=(12, 0), pady=(18, 6))
        self.entry_source_zip.grid(row=1, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_source_zip.grid(row=1, column=2, sticky='news', padx=(12, 12))

        self.label_arrow_install.grid(row=2, column=1, padx=(12, 0), pady=(12, 6))

        self.label_missions_dir.grid(row=3, column=0, columnspan=3, padx=(12, 0), pady=(0, 6))
        self.entry_missions_dir.grid(row=4, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_missions_dir.grid(row=4, column=2, sticky='news', padx=(12, 12))

        self.button_install.grid(row=5, column=1, sticky='news', padx=(12, 0), pady=(18, 18))

        self.tab_bundle.grid_columnconfigure(0, weight=1, uniform='hoh sis')
        self.tab_bundle.grid_columnconfigure(1, weight=1, uniform='hoh sis')
        self.tab_bundle.grid_columnconfigure(2, weight=1, uniform='hoh sis')
        self.tab_bundle.grid_rowconfigure(1, uniform='u')
        self.tab_bundle.grid_rowconfigure(4, uniform='u')

        self.label_mission_file.grid(row=0, column=0, columnspan=3, padx=(12, 0), pady=(18, 6))
        self.entry_mission_file.grid(row=1, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_mission_file.grid(row=1, column=2, sticky='news', padx=(12, 12))

        self.label_arrow_bundle.grid(row=2, column=1, padx=(12, 0), pady=(12, 6))

        self.label_dest_dir.grid(row=3, column=0, columnspan=3, padx=(12, 0), pady=(0, 6))
        self.entry_dest_dir.grid(row=4, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_dest_dir.grid(row=4, column=2, sticky='news', padx=(12, 12))

        self.button_bundle.grid(row=5, column=1, sticky='news', padx=(12, 0), pady=(18, 18))

        self.frame_status.grid(row=1, column=1, padx=(6, 12), pady=(12, 12), sticky='news')
        self.frame_status.grid_columnconfigure(0, weight=1)
        self.frame_status.grid_rowconfigure(0, weight=1)
        self.text_status.grid(row=0, column=0, sticky='news')

        self.label_credits.grid(row=2, column=0, columnspan=2, pady=(0, 12))

        self.job = None

    def press_button_source_zip(self):
        zip = tk.filedialog.askopenfilename(title='Select File', filetypes=(('Zip files', '*.zip'),)).replace('\\', '/')
        if zip == '':
            return

        self.entry_source_zip.delete(0, tk.END)
        self.entry_source_zip.insert(0, zip)
        self.entry_source_zip.xview(tk.END)

    def press_button_missions_dir(self):
        directory = tk.filedialog.askdirectory(
            title='Select Directory',
            initialdir=path.platinum(self.entry_missions_dir.get())
        ).replace('\\', '/')
        if directory == '':
            return

        self.entry_missions_dir.delete(0, tk.END)
        self.entry_missions_dir.insert(0, path.relative(directory))
        self.entry_missions_dir.xview(tk.END)

    def press_button_install(self):
        self.job = job.install(
            source_zip=self.entry_source_zip.get(),
            mission_dest_dir=path.platinum(self.entry_missions_dir.get())
        )

        self.text_status.config(state='normal')
        self.text_status.delete('0.0', tk.END)
        self.text_status.config(state='disabled')
        self.update()
    
    def press_button_mission_file(self):
        file = tk.filedialog.askopenfilename(
            title='Select File',
            initialdir=path.platinum('data/missions/custom'),
            filetypes=(('Mission files', '*.mis'),)
        ).replace('\\', '/')
        if file == '':
            return

        self.entry_mission_file.delete(0, tk.END)
        self.entry_mission_file.insert(0, path.relative(file))
        self.entry_mission_file.xview(tk.END)
    
    def press_button_dest_dir(self):
        directory = tk.filedialog.askdirectory(title='Select Directory').replace('\\', '/')
        if directory == '':
            return

        self.entry_dest_dir.delete(0, tk.END)
        self.entry_dest_dir.insert(0, directory)
        self.entry_dest_dir.xview(tk.END)
    
    def press_button_bundle(self):
        self.job = job.bundle(
            mission_file=path.platinum(self.entry_mission_file.get()),
            dest_dir=self.entry_dest_dir.get()
        )

        self.text_status.config(state='normal')
        self.text_status.delete('0.0', tk.END)
        self.text_status.config(state='disabled')
        self.update()

    def update(self):
        if self.job:
            self.text_status.config(state='normal')
            try:
                self.text_status.insert(tk.END, next(self.job))
            except StopIteration:
                self.job = None
            self.text_status.see(tk.END)
            self.text_status.config(state='disabled')

            self.after(10, self.update)
