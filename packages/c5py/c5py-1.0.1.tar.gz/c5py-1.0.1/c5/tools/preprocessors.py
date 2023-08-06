from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
from nbconvert.preprocessors.execute import CellExecutionError

import nbformat
import nbconvert
from textwrap import dedent

import re
import copy


class PyMarkdownPreprocessor(Preprocessor):
    def replace_variables(self, source, variables):
        """
        Replace {{variablename}} with stored value
        """
        try:
            replaced = re.sub("{{(.*?)}}", lambda m: variables.get(m.group(1), ""), source)
        except TypeError:
            print("ERROR")
            print(source)
            print(variables)
            # raise TypeError
            replaced = source
        return replaced

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess cell

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """
        if cell.cell_type == "markdown":
            # print(cell['metadata'])
            if hasattr(cell["metadata"], "variables"):
                variables = cell["metadata"]["variables"]
                # print(variables)
                if len(variables) > 0:
                    cell.source = self.replace_variables(cell.source, variables)
        return cell, resources

    def preprocess_markdown_cell(self, cell, resources, cell_index):
        # Find and execute snippets of code
        cell["metadata"]["variables"] = {}
        for m in re.finditer("{{(.*?)}}", cell.source):
            # Execute code
            fakecell = nbformat.v4.nbbase.new_code_cell(m.group(1))
            fakecell, _ = self.preprocess_code_cell(fakecell, resources, cell_index, is_fake=True)

            # Output found in cell.outputs
            # Put output in cell['metadata']['variables']
            for output in fakecell.outputs:
                html = self.convert_output_to_html(output)
                if html is not None:
                    cell["metadata"]["variables"][fakecell.source] = html
                    break
        return cell, resources


class ExecuteCodeMarkdownPreprocessor(ExecutePreprocessor):
    def __init__(self, **kwargs):
        self.sections = {"default": True}  # maps section ID to true or false
        self.EmptyCell = nbformat.v4.nbbase.new_raw_cell("")

        return super(ExecuteCodeMarkdownPreprocessor, self).__init__(**kwargs)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Executes a single code cell. See base.py for details.
        To execute all cells see :meth:`preprocess`.
        """

        if cell.cell_type == "code":
            # Do code stuff
            cell, resources = self.preprocess_code_cell(cell, resources, cell_index)

        elif cell.cell_type == "markdown":
            # Do markdown stuff
            cell, resources = self.preprocess_markdown_cell(cell, resources, cell_index)

        return cell, resources

    def preprocess_code_cell(self, cell, resources, cell_index, is_fake=False):
        """ Process code cell. """

        tmp = copy.deepcopy(cell.outputs)
        cell, resources = super(ExecuteCodeMarkdownPreprocessor, self).preprocess_cell(
            cell, resources, cell_index
        )
        if not self.allow_errors:
            for out in cell.outputs:
                if out["output_type"] == "error":
                    pattern = u"""\
                        An error occurred while executing the following cell:
                        ------------------
                        {cell.source}
                        ------------------
                        {out.ename}: {out.evalue}
                        """
                    msg = dedent(pattern).format(out=out, cell=cell)
                    raise CellExecutionError(msg)
        if is_fake is False:
            cell.outputs = tmp
        return cell, resources

    def preprocess_markdown_cell(self, cell, resources, cell_index):
        # Find and execute snippets of code
        cell["metadata"]["variables"] = {}
        for m in re.finditer("{{(.*?)}}", cell.source):
            # Execute code
            fakecell = nbformat.v4.nbbase.new_code_cell(m.group(1))
            fakecell, _ = self.preprocess_code_cell(fakecell, resources, cell_index, is_fake=True)

            # Output found in cell.outputs
            # Put output in cell['metadata']['variables']
            for output in fakecell.outputs:
                html = self.convert_output_to_html(output)
                if html is not None:
                    cell["metadata"]["variables"][fakecell.source] = html
                    break
        return cell, resources

    def convert_output_to_html(self, output):
        """Convert IOpub output to HTML

        See https://github.com/ipython-contrib/IPython-notebook-extensions/blob/master/nbextensions/usability/python-markdown/main.js
        """
        if output["output_type"] == "error":
            text = "**" + output.ename + "**: " + output.evalue
            return text
        elif output["output_type"] == "execute_result" or output["output_type"] == "display_data":
            data = output["data"]
            if "text/latex" in data:
                html = data["text/latex"]
                return html
            elif "image/svg+xml" in data:
                # Not supported
                # var svg = ul['image/svg+xml'];
                # /* embed SVG in an <img> tag, still get eaten by sanitizer... */
                # svg = btoa(svg);
                # html = '<img src="data:image/svg+xml;base64,' + svg + '"/>';
                return None
            elif "image/jpeg" in data:
                jpeg = data["image/jpeg"]
                html = '<img src="data:image/jpeg;base64,' + jpeg + '"/>'
                return html
            elif "image/png" in data:
                png = data["image/png"]
                html = '<img src="data:image/png;base64,' + png + '"/>'
                return html
            elif "text/markdown" in data:
                text = data["text/markdown"]
                return text
            elif "text/html" in data:
                html = data["text/html"]
                return html
            elif "text/plain" in data:
                text = data["text/plain"]
                # Strip <p> and </p> tags
                # Strip quotes
                # html.match(/<p>([\s\S]*?)<\/p>/)[1]
                text = re.sub(r"<p>([\s\S]*?)<\/p>", r"\1", text)
                text = re.sub(r"'([\s\S]*?)'", r"\1", text)
                return text
            else:
                # Some tag we don't support
                return None
        else:
            return None


class PersistentOutputPreprocessor(ExecuteCodeMarkdownPreprocessor):
    def preprocess_code_cell(self, cell, resources, cell_index, is_fake=False):
        return super(PersistentOutputPreprocessor, self).preprocess_code_cell(
            cell, resources, cell_index, is_fake=True
        )

