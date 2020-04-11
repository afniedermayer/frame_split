from collections import namedtuple
import re

Environment = namedtuple('Environment', ['inner', 'outer'])
Index = namedtuple('Index', ['begin', 'end'])

def get_environment(text:str, position:int, begin_token:str, end_token:str) -> Environment:
    current_position = position
    begin_outer = None
    # print('looking for begin')
    while begin_outer is None:
        begin = text.rfind(begin_token, 0, current_position)
        end = text.rfind(end_token, 0, current_position)
        # print('begin: {}'.format(begin))
        # print('end: {}'.format(end))
        if begin > end or begin == -1:
            begin_outer = begin
        else:
            current_position = begin
    begin_inner = begin_outer + len(begin_token)
    current_position = position
    end_inner = None
    # print('looking for begin')
    while end_inner is None:
        begin = text.find(begin_token, current_position)
        end = text.find(end_token, current_position)
        # print('begin: {}'.format(begin))
        # print('end: {}'.format(end))
        if begin > end or begin == -1 or end == -1:
            end_inner = end
        else:
            current_position = end + len(end_token)
    end_outer = end_inner + len(end_token)
    if begin_outer == -1 or end_inner == -1:
        return None
    #     raise ValueError('"{}" missing'.format(begin_token))
    # if end_inner == -1:
    #     raise ValueError('"{}" missing'.format(end_token))        
    return Environment(inner=Index(begin_inner, end_inner), 
        outer=Index(begin_outer, end_outer))

def split_frame(buffer:str, position:int) -> tuple:
    r"""
    Splits a LaTeX beamer frame into two frames, each containing
    part of the itemize environment. The split of the itemize 
    environment is around `position` (number of characters from
    beginning of buffer).
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
    frame = get_environment(buffer, position, r'\begin{frame}', r'\end{frame}')
    if frame is None:
        raise ValueError(r'\begin{frame} or \end{frame} missing')
    itemize = get_environment(buffer, position, r'\begin{itemize}', r'\end{itemize}')
    # if itemize is not None and not (frame.inner.begin < itemize.outer.begin < itemize.outer.end < frame.inner.end):
    #     # raise ValueError('no itemize in current frame')
    #     itemize = None
    if itemize is None or not (frame.inner.begin < itemize.outer.begin < itemize.outer.end < frame.inner.end):
        frame_options = r'(<.*>)?(\[.*\])?(\{.*\})?(\{.*\})?\s*(\\frametitle\{.*\})?'
        m = re.match(frame_options, buffer[frame.inner.begin:frame.inner.end])
        if m is None:
            frame_options_length = 0
        else:
            frame_options_length = m.end()
        if frame.inner.begin + frame_options_length > position:
            raise ValueError('cursor not in interior of frame, but on frame options')
        frame_pre = buffer[frame.outer.begin:frame.inner.begin + frame_options_length]
        # frame_pre = r'\begin{frame}'
        frame_post = r'\end{frame}'
        first_part = buffer[frame.inner.begin + frame_options_length:position]
        second_part = buffer[position:frame.inner.end]
        if len(first_part) > 0 and first_part[-1] != '\n':
            first_part = first_part + '\n'
        if len(second_part) > 0 and second_part[0] != '\n':
            second_part = '\n' + second_part
    else:
        item1 = buffer.find(r'\item', itemize.inner.begin, itemize.inner.end)
        if item1 == -1:
            raise ValueError('no item in itemize')
        split_position = buffer.find(r'\item', position-len(r'\item')+1, itemize.inner.end)
        if split_position == -1:
            raise ValueError('no item after cursor position')
        frame_pre = buffer[frame.outer.begin:item1]
        frame_post = buffer[itemize.inner.end:frame.outer.end]
        first_part = buffer[item1:split_position]
        second_part = buffer[split_position:itemize.inner.end]
    frame1 = frame_pre + first_part + frame_post
    frame2 = frame_pre + second_part + frame_post
    return frame, frame1, frame2    
