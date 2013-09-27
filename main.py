# -*- coding: utf-8 -*-
# PEP8:NO, LINT:OK, PY3:NO


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Ninja HTML to JS "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 30/10/2013 '
__prj__ = ' '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from BeautifulSoup import BeautifulSoup
from os import linesep
import re
from sets import Set
from datetime import datetime
from getpass import getuser

from PyQt4.QtGui import QIcon, QAction, QInputDialog

from ninja_ide.core import plugin


# constants
js_template = "{}{}{}{}{}{}{}{}{}"
tag_2_ignore = ('head', 'meta', 'noscript', 'script', 'style', 'link', 'no-js',
                'title', 'object', 'col', 'colgroup', 'option', 'param',
                'audio', 'basefont', 'isindex', 'svg', 'area', 'embed', 'br')


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        super(Main, self).initialize(*args, **kwargs)
        self.locator.get_service("menuApp").add_action(QAction(QIcon.fromTheme("edit-select-all"), "HTML to JS", self, triggered=lambda: self.locator.get_service("editor").add_editor(content=self.make_jss(str(self.locator.get_service("editor").get_actual_tab().textCursor().selectedText().encode("utf-8").strip()).lower()), syntax='js')))

    def make_jss(self, html):
        ' make js '
        indnt = ' ' * int(QInputDialog.getInteger(None, __doc__,
                          " JS Indentation Spaces: ", 4, 0, 8, 2)[0])
        scrpt = QInputDialog.getItem(None, __doc__, "Enclosing script Tags ?",
                        ['Use script html tags', 'No script tags'], 0, False)[0]
        p = True if 'Use script html tags' in scrpt else False
        self.soup = self.get_soup(html)
        jss = '<script>{}'.format(linesep) if p is True else ''
        jss += '//{} by {}{}'.format(datetime.now().isoformat().split('.')[0],
                                       getuser(), linesep)
        jss += '$(document).ready(function(){' + linesep
        previously_styled = []
        previously_styled.append(tag_2_ignore)
        jss += '{}//{}{}'.format(linesep, '-' * 76, linesep)
        for part in self.get_ids():
            if part not in previously_styled:
                jss += '{}//{}{}'.format(indnt, '#'.join(part).lower(), linesep)
                jss += js_template.format(indnt, 'var ',
                       re.sub('[^a-z]', '', part[1].lower() if len(part[1]) < 11 else re.sub('[aeiou]', '', part[1].lower())),
                       ' = ', '$("#{}").lenght'.format(part[1]), ';', linesep,
                       linesep, '')
                previously_styled.append(part)
        jss += '//{}{}'.format('-' * 76, linesep)
        for part in self.get_classes():
            if part not in previously_styled:
                jss += '{}//{}{}'.format(indnt, '.'.join(part).lower(), linesep)
                jss += js_template.format(indnt, 'var ',
                       re.sub('[^a-z]', '', part[1].lower() if len(part[1]) < 11 else re.sub('[aeiou]', '', part[1].lower())),
                       ' = ', '$(".{}").lenght'.format(part[1]), ';', linesep,
                       linesep, '')
                previously_styled.append(part)
        jss += '});'
        jss += '{}</script>'.format(linesep) if p is True else ''
        return jss.strip()

    def get_soup(self, html):
        ' get your soup '
        return BeautifulSoup(BeautifulSoup(html).prettify())

    def get_tags(self):
        " get all tags in the html "
        raw_tags, tags = self.soup.findAll(re.compile('')), []
        for tag in raw_tags:
            tags.append((tag.name))
        return list(Set(tags))

    def get_classes(self):
        " get all classes in the html "
        raw_tags = self.soup.findAll(re.compile(''), {'class': re.compile('')})
        tags = []
        for tag in raw_tags:
            attrs_dict = {}
            for attr in tag.attrs:
                attrs_dict[attr[0]] = attr[1]
            tags.append((tag.name, attrs_dict['class']))
        return sorted(list(Set(tags)))

    def get_ids(self):
        " get all ids in the html "
        raw_tags = self.soup.findAll(re.compile(''), {'id': re.compile('')})
        tags = []
        for tag in raw_tags:
            attrs_dict = {}
            for attr in tag.attrs:
                attrs_dict[attr[0]] = attr[1]
            tags.append((tag.name, attrs_dict['id']))
        return sorted(list(Set(tags)))


###############################################################################


if __name__ == "__main__":
    print(__doc__)
