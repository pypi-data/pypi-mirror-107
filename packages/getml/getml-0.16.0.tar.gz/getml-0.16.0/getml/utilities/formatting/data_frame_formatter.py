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

"""
Holds the DataFrameFormatter.
"""

from collections import namedtuple
from inspect import cleandoc

import numpy as np

from getml.data.helpers import _get_data_frame_content
from getml.data.roles import join_key, numerical, target, time_stamp, unused_float

from ..templates import environment
from .formatter import _FormatColumn, _Formatter, _IndexColumn, _infer_precision

UNITS = ["D", "h", "m", "s", "ms"]
"""
Numpy datetime units.
"""

UNITS_FORMATS = dict(
    D="{:%Y-%m-%d}",
    h="{:%Y-%m-%d %H}",
    m="{:%Y-%m-%d %H:%M}",
    s="{:%Y-%m-%d %H:%M:%S}",
    ms="{:%Y-%m-%d %H:%M:%S.%f}",
)
"""
A mapping of numpy datetime units to strftime format specifiers.
"""

# --------------------------------------------------------------------


def _infer_resolution(cells):
    cells = np.array(cells, dtype="datetime64")
    deltas = np.unique(cells[1:] - cells[:-1])

    for unit in UNITS:
        normalized_deltas = np.array(
            [np.timedelta64(delta, "ms") for delta in deltas]
        ) / np.timedelta64(1, unit)
        if all(np.mod(normalized_deltas, 1) == 0):
            return unit


# --------------------------------------------------------------------


def _max_digits(cells):
    cells = [cell for cell in cells if "." in cell]
    if len(cells) > 0:
        return max(len(cell.split(".")[1]) for cell in cells)
    return 0


# --------------------------------------------------------------------


class _DataFrameFormatter(_Formatter):
    """
    A Formatter for DataFrames.
    """

    max_rows = 10

    template = environment.get_template("data_frame.jinja2")

    # ------------------------------------------------------------

    def __init__(self, df, num_head=max_rows // 2, num_tail=max_rows // 2):
        self.colnames = df.colnames
        self.n_rows = len(df)
        self.name = df.name
        self.memory_usage = df.memory_usage

        units = [df[colname].unit for colname in df.colnames]
        roles = [df[colname].role for colname in df.colnames]

        if all(unit == "" for unit in units):
            units = None

        head = _get_data_frame_content(name=df.name, start=0, length=num_head)["data"]
        tail = _get_data_frame_content(
            name=df.name, start=int(self.n_rows - num_tail), length=num_tail
        )["data"]

        rows = head + tail

        columns = [list(col) for col in zip(*rows)]

        if units:
            headers = zip(self.colnames, roles, units)
        else:
            headers = zip(self.colnames, roles)

        self.data = [
            _DataFrameFormatColumn(
                headers=list(header),
                cells=cells,
                max_cells=self.max_rows,
                n_cells=self.n_rows,
                role=role,
            )
            for header, role, cells in zip(headers, roles, columns)
        ]

        self._add_index()

    # ------------------------------------------------------------

    def __len__(self):
        return self.n_rows

    # ------------------------------------------------------------

    def _render_footer_lines(self, footer):
        return cleandoc(
            f"""
            {footer.n_rows} rows x {footer.n_cols} columns
            memory usage: {footer.memory_usage:.2f} MB
            name: {footer.name}
            type: {footer.type}
            url: {footer.url}
            """
        )

    # ------------------------------------------------------------

    def _add_index(self):
        headers = ["Name"]
        if self.roles:
            headers += ["Role"]
        if self.units:
            headers += ["Units"]
        index_column = _IndexColumn(
            headers=headers,
            n_cells=self.n_rows,
            max_length=self.max_rows,
        )

        self.data = [index_column] + self.data

    # ------------------------------------------------------------

    def _render_html(self, footer=None):
        headers = self._render_head()
        rows = self._render_body(as_html=True)

        precisions = [getattr(column, "precision", None) for column in self.data]

        cell = namedtuple("cell", ["role", "value"])
        headers = [
            [cell(role, header) for role, header in zip(self.roles, headers)]
            for headers in headers
        ]
        rows = [
            [cell(role, value) for role, value in zip(self.roles, row)] for row in rows
        ]

        return self.template.render(
            headers=headers, rows=rows, precisions=precisions, footer=footer
        )

    # ------------------------------------------------------------

    def _render_string(self, footer=None):

        lines = super()._render_string()

        footer_lines = self._render_footer_lines(footer) if footer else ""

        return lines + "\n\n\n" + footer_lines

    # ------------------------------------------------------------

    @property
    def roles(self):
        return [getattr(column, "role", None) for column in self.data]

    # ------------------------------------------------------------

    @property
    def units(self):
        if any(len(column.sub_headers) > 1 for column in self.data):
            return [column.sub_headers[1] for column in self.data]


# --------------------------------------------------------------------


class _DataFrameFormatColumn(_FormatColumn):
    """
    A Formatter for columns of a DataFrame.

    The cell format is set based on the column's role.
    """

    # ------------------------------------------------------------

    def __init__(self, *args, n_cells, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_cells = n_cells
        self.resolution = None
        self.role = role

        # self.parse_cells()
        if self.role in [numerical, target, join_key, unused_float]:
            self.precision = _max_digits(self.data)

        self.cell_template = self.default_cell_template
        self.header_template = self.default_header_template

    # ------------------------------------------------------------

    def __len__(self):
        return len(self.data)

    # ------------------------------------------------------------

    def _format_cells(self):
        """
        A patch to justify time stamps. This is necessary because afaik we are not able
        to specify justification within strftime format strings.
        """
        cells_formatted = super()._format_cells()

        if self.role == "time_stamp":
            cells_formatted.data = [
                cell.ljust(self.width) for cell in cells_formatted.data
            ]

        return cells_formatted

    # ------------------------------------------------------------

    def _clip(self):
        ellipses = "..." + getattr(self, "precision", 0) * " "
        return super()._clip(ellipses=ellipses)

    # ------------------------------------------------------------

    def _parse_cells(self):
        # some fun parsing
        if self.role == time_stamp:
            if all(cell.isdigit() for cell in self.data):
                self.data = np.array(self.data, dtype="float")
                self.data = np.array(self.data, dtype="datetime64[s]").tolist()
            else:
                self.data = np.array(self.data, dtype="datetime64[ms]").tolist()

            resolutions = list(
                set(
                    [
                        _infer_resolution(self.data[: len(self.data) // 2]),
                        _infer_resolution(self.data[len(self.data) // 2 :]),
                    ]
                )
            )

            # sort resolutions in ascending order and pick the smallest one
            self.resolution = sorted(
                resolutions, key=lambda res: UNITS.index(res), reverse=True
            )[0]

        if self.role in [numerical, target, join_key, unused_float]:
            # this logic might be too simplistic, but data comes from the engine
            # in a standardized format anyway, so...¯\_(ツ)_/¯
            if any("." in cell for cell in self.data):
                self.data = [float(cell) for cell in self.data]
                self.precision = _infer_precision(self.data)
            elif all(cell.isdigit() for cell in self.data):
                self.data = [int(cell) for cell in self.data]

    # ------------------------------------------------------------

    @property
    def default_cell_template(self):

        if getattr(self, "role", None) in [
            numerical,
            target,
            join_key,
            unused_float,
        ]:
            if all(cell.isdigit() for cell in self.data):
                return "{:" f">{self.width}" "}"
            return "{:" f" {self.width}.{self.precision}d" "}"

        return super().default_cell_template

    # ------------------------------------------------------------

    @property
    def default_header_template(self):

        if getattr(self, "role", None) in [
            numerical,
            target,
            join_key,
            unused_float,
        ]:
            return "{:" f">{self.width}" "}"

        return super().default_header_template
