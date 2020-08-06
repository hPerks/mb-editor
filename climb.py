import os
import shutil

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog

import sys
import traceback

from mb_editor.interior import Interior
from mb_editor.mission import Mission
from mb_editor.utils import path


def run_import(source_dir, mission_dest_dir):
    os.makedirs(mission_dest_dir, mode=0o777, exist_ok=True)

    mission_source_paths = []
    num_bad_missions = 0
    interiors = []

    for root_dir, _, basenames in os.walk(source_dir):
        for mission_source_basename in basenames:
            if mission_source_basename.endswith('.mis') and not mission_source_basename.startswith('._'):
                mission_source_path = path.join(root_dir, mission_source_basename)
                mission_source_paths.append(mission_source_path)

                if len(mission_source_paths) == 1:
                    yield 'Installed mission(s):\n\n'

                try:
                    mission = Mission.from_file(mission_source_path)
                    yield '"{}" ({})\n'.format(
                        mission.info.name,
                        path.relative(mission_dest_dir, mission_source_basename)
                    )
                except Exception as e:
                    _, _, e_traceback = sys.exc_info()
                    num_bad_missions += 1
                    yield (
                        '\nError parsing mission "{}":\n'.format(mission_source_basename) +
                        '\n'.join(traceback.format_tb(
                            e_traceback)) +
                        '\n{}: {}'.format(
                            e.__class__.__name__, e.args[0]) +
                        '\nSend this text to @hPerks#5581 on Discord for help!\n\n'
                    )
                    continue

                for interior in mission.descendants():
                    if isinstance(interior, Interior) and interior.interiorFile not in [i.interiorFile for i in interiors]:
                        interiors.append(interior)

    if len(mission_source_paths) == 0:
        yield 'No missions found. :(\n'
    yield '\n'

    for mission_source_path in mission_source_paths:
        shutil.copy(mission_source_path, mission_dest_dir)

        if os.path.exists(mission_source_path.replace('.mis', '.png')):
            shutil.copy(mission_source_path.replace('.mis', '.png'), mission_dest_dir)
        if os.path.exists(mission_source_path.replace('.mis', '.jpg')):
            shutil.copy(mission_source_path.replace('.mis', '.jpg'), mission_dest_dir)
        if os.path.exists(mission_source_path.replace('.mis', '.prev.png')):
            shutil.copy(mission_source_path.replace('.mis', '.prev.png'), mission_dest_dir)

    matched_interior_paths = []

    for root_dir, _, basenames in os.walk(source_dir):
        for interior_source_basename in basenames:
            if interior_source_basename.endswith('.dif'):
                interior_source_path = path.join(root_dir, interior_source_basename)

                for interior in interiors:
                    interior_dest_path = path.platinum(interior.interiorFile)
                    interior_dest_dir = os.path.dirname(interior_dest_path)
                    interior_dest_basename = os.path.basename(interior_dest_path)

                    if interior_source_basename == interior_dest_basename:
                        os.makedirs(interior_dest_dir, mode=0o777, exist_ok=True)
                        shutil.copyfile(interior_source_path, interior_dest_path)

                        matched_interior_paths.append(interior_dest_path)
                        if len(matched_interior_paths) == 1:
                            yield 'Interior(s) included:\n\n'

                        yield '{}/{}\n'.format(
                            os.path.dirname(interior.interiorFile),
                            interior_source_basename
                        )
                        break

    if len(matched_interior_paths) == 0:
        yield 'No interiors included.\n'

    num_missing_interiors = 0
    for interior in interiors:
        interior_dest_path = path.platinum(interior.interiorFile)
        if interior_dest_path not in matched_interior_paths:
            if not os.path.exists(interior_dest_path):
                if num_missing_interiors == 0:
                    yield '\nMissing interior(s):\n'
                num_missing_interiors += 1
                yield '{}/{}\n'.format(
                    os.path.dirname(interior.interiorFile),
                    os.path.basename(interior.interiorFile)
                )

    yield '\nSuccessfully installed {} missions'.format(len(mission_source_paths) - num_bad_missions) + (
        ''
        if num_bad_missions == 0
        else ' ({} invalid)'.format(num_bad_missions)
    ) + ' with {} interiors'.format(len(matched_interior_paths)) + (
        ''
        if num_missing_interiors == 0
        else ' ({} missing)'.format(num_missing_interiors)
    )


class StyledApp(tk.Tk):
    colors = ['#2f2f2f', '#3f3f3f', '#ddaa00', '#ffdb66', '#dbdbdb', '#2f2f2f']

    class Entry(tk.Entry):
        def __init__(self, parent, **config):
            defaults = dict(
                justify=tk.CENTER,
                relief='flat',
                font=('Roboto', 12),
                background=ImporterApp.colors[1],
                readonlybackground=ImporterApp.colors[1],
                insertbackground=ImporterApp.colors[4],
                foreground=ImporterApp.colors[4],
                highlightthickness=0,
            )
            defaults.update(**config)
            super().__init__(parent, **defaults)

    class Text(tk.Text):
        def __init__(self, parent, **config):
            defaults = dict(
                relief='flat',
                font=('Monaco', 10),
                background=ImporterApp.colors[1],
                foreground=ImporterApp.colors[4],
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
        self.style.map('TButton', background=[('active', self.colors[3])])


class ImporterApp(StyledApp):
    def __init__(self):
        super().__init__()

        self.title('CLIMB v1.0')
        self.configure(background=self.colors[0])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky='news')

        self.label_title = ttk.Label(self.frame, text='CLIMB v1.0', font=('Roboto', 24, 'bold'), foreground='#da0', justify=tk.CENTER)

        self.label_source_dir = ttk.Label(self.frame, text='Install from:', justify=tk.CENTER)
        self.entry_source_dir = self.Entry(self.frame)
        self.button_source_dir = ttk.Button(self.frame, text='Browse', command=self.press_button_source_dir)

        self.label_arrow = ttk.Label(self.frame, text='\u21e9', justify=tk.CENTER, font=('Roboto', 36))

        self.label_missions_dir = ttk.Label(self.frame, text='Missions folder:')
        self.entry_missions_dir = self.Entry(self.frame)
        self.entry_missions_dir.insert(0, '~/data/missions/custom')
        self.entry_missions_dir.xview(tk.END)
        self.button_missions_dir = ttk.Button(self.frame, text='Browse', command=self.press_button_missions_dir)

        self.button_import = ttk.Button(self.frame, text='Install!', command=self.press_button_import)

        self.frame_status = ttk.Frame(self.frame)
        self.scrollbar_status_v = ttk.Scrollbar(self.frame_status, orient='vertical')
        self.text_status = self.Text(self.frame_status, state='disabled', width=0, height=0, yscrollcommand=self.scrollbar_status_v.set)

        self.label_credits = ttk.Label(self.frame, text='made with \u2665 by hPerks, using mb-editor (github.com/omaitzen/mb-editor)', font=('Roboto', 10), foreground='#525252')

        self.frame.grid_columnconfigure(0, weight=1, uniform='joj')
        self.frame.grid_columnconfigure(1, weight=1, uniform='joj')
        self.frame.grid_columnconfigure(2, weight=1, uniform='joj')
        self.frame.grid_columnconfigure(3, weight=3, uniform='joj')

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(3, uniform='u')
        self.frame.grid_rowconfigure(6, uniform='u')
        self.frame.grid_rowconfigure(8, weight=1)

        self.label_title.grid(row=0, column=0, columnspan=4, pady=(18, 12))

        self.label_source_dir.grid(row=2, column=0, columnspan=3, padx=(12, 0), pady=(12, 6))
        self.entry_source_dir.grid(row=3, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_source_dir.grid(row=3, column=2, sticky='news', padx=(12, 0))

        self.label_arrow.grid(row=4, column=1, padx=(12, 0), pady=(12, 6))

        self.label_missions_dir.grid(row=5, column=0, columnspan=3, padx=(12, 0), pady=(0, 6))
        self.entry_missions_dir.grid(row=6, column=0, columnspan=2, sticky='news', padx=(12, 0))
        self.button_missions_dir.grid(row=6, column=2, sticky='news', padx=(12, 0))

        self.button_import.grid(row=7, column=1, sticky='news', padx=(12, 0), pady=(24, 12))

        self.frame_status.grid(row=1, column=3, rowspan=8, padx=(12, 12), pady=(12, 12), sticky='news')
        self.frame_status.grid_columnconfigure(0, weight=1)
        self.frame_status.grid_rowconfigure(0, weight=1)
        self.text_status.grid(row=0, column=0, sticky='news')

        self.label_credits.grid(row=9, column=0, columnspan=4, pady=(0, 12))

        self.import_job = None

    def press_button_source_dir(self):
        directory = tk.filedialog.askdirectory(title='Select Directory').replace('\\', '/')
        if directory == '':
            return

        self.entry_source_dir.delete(0, tk.END)
        self.entry_source_dir.insert(0, directory)
        self.entry_source_dir.xview(tk.END)

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

    def press_button_import(self):
        self.import_job = run_import(
            source_dir=self.entry_source_dir.get(),
            mission_dest_dir=path.platinum(self.entry_missions_dir.get())
        )

        self.text_status.config(state='normal')
        self.text_status.delete('0.0', tk.END)
        self.text_status.config(state='disabled')
        self.update()

    def update(self):
        if self.import_job:
            self.text_status.config(state='normal')
            try:
                self.text_status.insert(tk.END, next(self.import_job))
            except StopIteration:
                self.import_job = None
            self.text_status.see(tk.END)
            self.text_status.config(state='disabled')

            self.after(10, self.update)


if __name__ == '__main__':
    app = ImporterApp()
    app.mainloop()