import sys
# sys.path.remove('/Users/cbaker/Documents/git-chris/reprexpy/reprexpy')
print("\n".join(sys.path))
from reprexpy.reprexpy import _get_statement_chunks, _run_nb, _extract_outputs, \
    _get_code_block_start_stops, _get_cell_txt_outputs, _is_plot_output

import pyimgur
import re
import nbformat
import nbconvert

def read_ex_fi(file):
    with open(file) as fi:
        return fi.read()

code_str = read_ex_fi("tests/test-examples/basic-example.py")
code_chunks = _get_statement_chunks(code_str)
node_out = _run_nb(code_chunks, "python3")

outputs = _extract_outputs(node_out.cells)

tmp_out = _get_cell_txt_outputs(outputs, "#>")


# add text outputs to code inputs
ins_and_outs = [i + j if j else i for i, j in zip(code_chunks, tmp_out)]

# if SO:
ins_and_outs2 = [['    ' + j for j in i] for i in ins_and_outs]

# collapsing each "statement" + output into one string:
outs_appended2 = ['\n'.join(i) for i in ins_and_outs2]

# split statement chunks into code chunks, based on start stops
start_stops = _get_code_block_start_stops(outputs)
chunks = [outs_appended2[i[0]:(i[1] + 1)] for i in start_stops]
chunks2 = ['\n'.join(i) for i in chunks]

# if this is gh, add "```python\n" at start of each chunk and "\n```\n" at end

# for each stop in start_stops, check if that index refers to a list containing a plot output in
# plot_outputs_mkup...if it is, add "\n" + concat of plotouts (markup of them) to txt

    # first need to create plot_outputs_mkup
plot_outputs = [[j for j in i if _is_plot_output(j)] for i in outputs]




data = plot_outputs[3][0]["data"]["image/png"].encode()

client = pyimgur.Imgur("9f3460e67f308f6")

r = client._send_request('https://api.imgur.com/3/image', method='POST', params={'image': data})
r['link']

# ![untitled](https://i.imgur.com/Gip1lad.png)


# first line of so output (keep second comment char)
# # <!-- language-all: lang-py -->



# dev pyperclip work

# import pyperclip
#
# pyperclip.copy('    x = "hi there"\n\n text to be copied to the clipboard.\nhere is more text\tokthen?')
#
# pyperclip.copy("#>   'ok\\nthenhi there'")
# txt = '    ' + chunks[1][1]
# txt = '    ' + chunks[0][0]
# pyperclip.copy(txt)
#
# pyperclip.copy(chunks2[0])
#
# spam = pyperclip.paste()
# x = "some file"
# y = "another file"
#
# ## do i need to handle formating of tables?
#
# pyperclip.copy('    ' + chunks[1][1])
# spam = pyperclip.paste()
# x = "some file"
# y = "another file"