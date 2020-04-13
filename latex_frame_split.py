from collections import namedtuple
import re, os

class Environment(namedtuple('Environment', ['name', 'inner', 'outer'])):
    def __contains__(self, other:'Environment') -> bool:
        return not self.found() or (other.found() and 
            self.inner.begin < other.outer.begin < other.outer.end < self.inner.end
        )
    def found(self) -> bool:
        return self.inner is not None and self.outer is not None

Index = namedtuple('Index', ['begin', 'end'])

def find_comment(text:str) -> int:
    if '%' not in text:
        return -1
    escaped = False
    for i, c in enumerate(text):
        if not escaped:
            if c == '%': 
                return i
            elif c == '\\':
                escaped = True
        else:
            escaped = False
    return -1

def replace_comment_in_line(text:str) -> str:
    comment_index = find_comment(text)
    if comment_index == -1:
        return text
    elif comment_index == 0:
        return (len(text)-comment_index)*' '
    else:
        return text[:comment_index] + (len(text)-comment_index)*' '

def replace_comments(text:str) -> str:
    return '\n'.join(replace_comment_in_line(line) for line in text.split('\n'))

def get_environment(text:str, position:int, name:str) -> Environment:
    begin_token = '\\begin{' + name + '}'
    end_token = '\\end{' + name + '}'
    current_position = position
    begin_outer = None
    while begin_outer is None:
        begin = text.rfind(begin_token, 0, current_position)
        end = text.rfind(end_token, 0, current_position)
        if begin > end or begin == -1:
            begin_outer = begin
        else:
            current_position = begin
    begin_inner = begin_outer + len(begin_token)
    current_position = position
    end_inner = None
    while end_inner is None:
        begin = text.find(begin_token, current_position)
        end = text.find(end_token, current_position)
        if begin > end or begin == -1 or end == -1:
            end_inner = end
        else:
            current_position = end + len(end_token)
    end_outer = end_inner + len(end_token)
    if begin_outer == -1 or end_inner == -1:
        return Environment(name=name, inner=None, outer=None)
    return Environment(name=name, inner=Index(begin_inner, end_inner), 
        outer=Index(begin_outer, end_outer))

def split_frame(buffer:str, position:int) -> tuple:
    r"""
    Splits a LaTeX beamer frame into two frames, each containing
    part of the itemize environment. The split of the itemize 
    environment is around `position` (number of characters from
    beginning of buffer).

    Returns a tuple (frame, frame1, frame2), where frame is an
    Environment with the coordinates of the frame, frame1 and frame2
    are strings with the two frames resulting from the split.

    Usage example:
    >>> buffer = r'''text before frame
    ... \begin{frame}
    ... \begin{itemize}
    ... \item foo
    ... \item bar
    ... \item baz
    ... \end{itemize}
    ... \end{frame}
    ... text after frame
    ... '''
    ... 
    >>> position = 58 # position just before "\item bar"
    >>> frame, frame1, frame2 = split_frame(buffer, position)
    >>> buffer[:frame.outer.begin]
    'text before frame\n'
    >>> buffer[frame.outer.end:]
    '\ntext after frame\n'
    >>> frame1
    '\\begin{frame}\n\\begin{itemize}\n\\item foo\n\\end{itemize}\n\\end{frame}'
    >>> frame2
    '\\begin{frame}\n\\begin{itemize}\n\\item bar\n\\item baz\n\\end{itemize}\n\\end{frame}'
    
    If there is no itemize in the frame, the frame is split at `position`.
    """
    buffer_without_comments = replace_comments(buffer)
    frame = get_environment(buffer_without_comments, position, 'frame')
    if not frame.found():
        raise ValueError(r'Cursor not between \begin{frame} and \end{frame}.')
    itemize = get_environment(buffer_without_comments, position, 'itemize')
    enumerate_ = get_environment(buffer_without_comments, position, 'enumerate')
    if itemize in enumerate_:
        inner_env = itemize
    else:
        inner_env = enumerate_
    if inner_env not in frame:
        frame_options = r'(<.*>)?(\[.*\])?(\{.*\})?(\{.*\})?\s*(\\frametitle\{.*\})?'
        m = re.match(frame_options, buffer_without_comments[frame.inner.begin:frame.inner.end])
        if m is None:
            frame_options_length = 0
        else:
            frame_options_length = m.end()
        if frame.inner.begin + frame_options_length > position:
            raise ValueError('Cursor not in interior of frame, but on frame options.')
        frame_pre1 = buffer[frame.outer.begin:frame.inner.begin + frame_options_length]
        frame_pre2 = frame_pre1
        frame_post = r'\end{frame}'
        first_part = buffer[frame.inner.begin + frame_options_length:position]
        second_part = buffer[position:frame.inner.end]
        if len(first_part) > 0 and first_part[-1] != '\n':
            first_part = first_part + '\n'
        if len(second_part) > 0 and second_part[0] != '\n':
            second_part = '\n' + second_part
    else:
        item1 = buffer_without_comments.find(r'\item', inner_env.inner.begin, inner_env.inner.end)
        if item1 == -1:
            raise ValueError('No item in {}.'.format(inner_env.name))
        split_position = buffer_without_comments.find(r'\item', position-len(r'\item')+1, 
            inner_env.inner.end)
        if split_position == -1:
            raise ValueError('No item after cursor position.')
        frame_pre1 = buffer[frame.outer.begin:item1]
        if inner_env.name == 'enumerate':
            env_before_split = buffer_without_comments[inner_env.inner.begin:split_position]
            counter = len(re.findall(r'\\item', env_before_split))
            enum_level = 'enumi'
            # m = re.search(r'\\setcounter\{(enum[iv]+)\}\{(.*)\}', env_string)
            # if m is not None:
            #     enum_level = m.group(1)
            #     try:
            #         counter += int(m.group(2))
            #     except ValueError:
            #         counter = m.group(2)
            frame_pre2 = buffer[frame.outer.begin:inner_env.inner.begin] + '\n' + \
                r'\setcounter{{{}}}{{{}}}'.format(enum_level, counter) + \
                buffer[inner_env.inner.begin:item1]
        else:
            frame_pre2 = frame_pre1
        frame_post = buffer[inner_env.inner.end:frame.outer.end]
        first_part = buffer[item1:split_position]
        second_part = buffer[split_position:inner_env.inner.end]
    frame1 = frame_pre1 + first_part + frame_post
    frame2 = frame_pre2 + second_part + frame_post
    return frame, frame1, frame2    
