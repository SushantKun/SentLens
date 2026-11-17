import customtkinter as ctk

from ui.ui import SentLensApp


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = SentLensApp()
    app.mainloop()


if __name__ == "__main__":
    main()