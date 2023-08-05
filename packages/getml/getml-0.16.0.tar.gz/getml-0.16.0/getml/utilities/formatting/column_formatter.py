# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from inspect import cleandoc

from getml.data.helpers import _get_column_content

from ..templates import environment
from .data_frame_formatter import _DataFrameFormatColumn, _DataFrameFormatter

# -----------------------------------------------------------------------------


class _ColumnFormatter(_DataFrameFormatter):

    max_rows = _DataFrameFormatter.max_rows

    template = environment.get_template("column.jinja2")

    # ------------------------------------------------------------

    def __init__(self, col, num_head=max_rows // 2, num_tail=max_rows // 2):
        self.n_rows = len(col)
        self.coltype = type(col).__name__
        if self.coltype.startswith("Virtual"):
            self.name = None
            self.role = None
            self.unit = None
        else:
            self.name = col.name
            self.role = col.role
            self.unit = col.unit

        head = _get_column_content(
            col=col.thisptr,
            coltype=self.coltype.replace("Virtual", ""),
            start=0,
            length=num_head,
        )["data"]
        tail = _get_column_content(
            col=col.thisptr,
            coltype=self.coltype.replace("Virtual", ""),
            start=int(self.n_rows - num_tail),
            length=num_tail,
        )["data"]

        cells = [cell[0] for cell in head + tail]

        header = [self.name or ""]

        if self.role:
            header += [self.role]

        if self.unit:
            header += [self.unit]

        self.data = [
            _DataFrameFormatColumn(
                headers=list(header),
                cells=cells,
                max_cells=self.max_rows,
                n_cells=self.n_rows,
                role=self.role,
            )
        ]

        self._add_index()

        if self.coltype.startswith("Virtual"):
            self.index.header = ""

    # ------------------------------------------------------------

    def _render_footer_lines(self, footer):
        footer_lines = cleandoc(
            f"""
            {footer.n_rows} rows
            type: {footer.type}
            """
        )

        if not self.coltype.startswith("Virtual"):
            footer_lines += f"\nurl: {footer.url}"

        return footer_lines
