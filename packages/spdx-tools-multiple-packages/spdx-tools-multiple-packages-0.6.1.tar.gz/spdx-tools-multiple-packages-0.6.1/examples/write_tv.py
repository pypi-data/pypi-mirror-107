#!/usr/bin/env python

# Writes a new tag/value file from scratch.
# Usage: write_tv <tagvaluefile>
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from spdx.relationship import Relationship, RelationshipOptions

if __name__ == '__main__':
    import sys
    import codecs
    from spdx.writers.tagvalue import write_document, InvalidDocumentError
    from spdx.document import Document, License, LicenseConjunction, ExtractedLicense
    from spdx.version import Version
    from spdx.creationinfo import Person
    from spdx.review import Review
    from spdx.package import Package
    from spdx.file import File, FileType
    from spdx.checksum import Algorithm
    from spdx.utils import SPDXNone, NoAssert, UnKnown

    doc = Document(name="Example", spdx_id="SPDXRef-DOCUMENT", namespace=SPDXNone())
    doc.version = Version(2, 1)
    doc.comment = 'Example Document'
    doc.data_license = License.from_identifier('CC0-1.0')
    doc.creation_info.add_creator(Person('Alice', 'alice@example.com'))
    doc.creation_info.set_created_now()
    review = Review(Person('Joe', None))
    review.set_review_date_now()
    review.comment = 'Joe reviewed this document'
    doc.add_review(review)

    # Package
    package = Package()
    package.spdx_id = "SPDXRef-1"
    package.name = 'TagWriteTest'
    package.version = '1.0'
    package.file_name = 'twt.jar'
    package.download_location = 'http://www.tagwritetest.test/download'
    package.homepage = SPDXNone()
    package.verif_code = '4e3211c67a2d28fced849ee1bb76e7391b93feba'
    license_set = LicenseConjunction(License.from_identifier('Apache-2.0'), License.from_identifier('BSD-2-Clause'))
    package.conc_lics = license_set
    package.license_declared = license_set
    package.add_lics_from_file(License.from_identifier('Apache-2.0'))
    package.add_lics_from_file(License.from_identifier('BSD-2-Clause'))
    package.cr_text = NoAssert()
    package.summary = 'Simple package.'
    package.description = 'Really simple package.'
    doc.add_package(package)

    package2 = Package()
    package2.spdx_id = "SPDXRef-2"
    package2.name = 'TagWriteTest'
    package2.version = '1.0'
    package2.file_name = 'twt.jar'
    package2.download_location = 'http://www.tagwritetest.test/download'
    package2.homepage = SPDXNone()
    package2.verif_code = '4e3211c67a2d28fced849ee1bb76e7391b93feba'
    package2.conc_lics = license_set
    package2.license_declared = license_set
    package2.add_lics_from_file(License.from_identifier('Apache-2.0'))
    package2.add_lics_from_file(License.from_identifier('BSD-2-Clause'))
    package2.cr_text = NoAssert()
    package2.summary = 'Simple package.'
    package2.description = 'Really simple package.'
    package2.add_relationship(Relationship(package2, RelationshipOptions.CONTAINS, package))
    doc.add_package(package2)

    # An extracted license
    lic = ExtractedLicense('LicenseRef-1')
    lic.text = 'Some non legal legal text..'
    doc.add_extr_lic(lic)

    file = sys.argv[1]
    with codecs.open(file, mode='w', encoding='utf-8') as out:
        try:
            write_document(doc, out)
        except InvalidDocumentError:
            print('Document is Invalid')
            messages = []
            doc.validate(messages)
            print('\n'.join(messages))
