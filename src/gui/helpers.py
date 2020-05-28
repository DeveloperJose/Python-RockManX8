from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor


class SyntaxHighligher(QSyntaxHighlighter):
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent

        symbol_format = QTextCharFormat()
        symbol_format.setForeground(QColor(19, 150, 250))
        symbol_pattern = QRegExp(r"\[[0-9]+\]")
        symbol_pattern.setMinimal(True)

        self.formats = [symbol_format]
        self.patterns = [symbol_pattern]

    def highlightBlock(self, text):
        for frmt, pattern in zip(self.formats, self.patterns):
            idx = pattern.indexIn(text)

            while idx >= 0:
                length = pattern.matchedLength()
                self.setFormat(idx, length, frmt)
                idx = pattern.indexIn(text, idx + length)
        self.setCurrentBlockState(0)