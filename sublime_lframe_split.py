import sublime
import sublime_plugin 
from .latex_frame_split import get_environment, split_frame

LSPLIT_WARNING = 'lsplit_warning'


class LsplitCommand(sublime_plugin.TextCommand):
    def run(self, edit:sublime.Edit) -> None:
        self.view.erase_phantoms(LSPLIT_WARNING)
        region = self.view.sel()[0]
        position = region.begin() # cursor position
        # create two new frames from splitting frame around
        # the cursor location
        buffer = self.view.substr(sublime.Region(0, self.view.size()))
        try:
            frame, frame1, frame2 = split_frame(buffer, position)
        except ValueError as e:
            self.show_warning('lsplit error: {}'.format(e.args[0]))
            return
        # replace current frame with the two new frames
        new_frame = frame1 + '\n\n' + frame2
        self.view.replace(edit, 
            sublime.Region(frame.outer.begin, frame.outer.end),
            new_frame
        )
        # selected the included frames
        self.view.sel().clear()
        self.view.sel().add(
            sublime.Region(frame.outer.begin, 
                frame.outer.begin + len(new_frame)))

    def show_warning(self, message:str) -> None:
            region = self.view.sel()[0]
            html_message = """
                <body id='{}'>
                  <style>
                    a {{ text-decoration: none; }}
                    div {{ 
                      background-color: red; 
                      border: 3px solid red; 
                      border-radius: 3px; 
                    }}
                  </style>
                  <div>
                    {}&nbsp;<a href='close_warning'>\N{MULTIPLICATION SIGN}</a>
                  </div>
                </body>""".format(LSPLIT_WARNING, message)
            self.view.add_phantom(LSPLIT_WARNING, region, html_message, 
                sublime.LAYOUT_BELOW,
                on_navigate=lambda href: self.view.erase_phantoms(LSPLIT_WARNING)
            )

