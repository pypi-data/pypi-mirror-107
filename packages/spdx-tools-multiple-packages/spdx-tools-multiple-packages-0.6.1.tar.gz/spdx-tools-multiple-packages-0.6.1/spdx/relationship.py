# Copyright (c) 2020 Daniel I Beard
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from spdx.element import Element


class RelationshipOptions:
    """Relationship options"""

    DESCRIBES = "DESCRIBES"
    DESCRIBED_BY = "DESCRIBED_BY"
    CONTAINS = "CONTAINS"
    CONTAINED_BY = "CONTAINED_BY"
    GENERATES = "GENERATES"
    GENERATED_FROM = "GENERATED_FROM"
    ANCESTOR_OF = "ANCESTOR_OF"
    DESCENDANT_OF = "DESCENDANT_OF"
    VARIANT_OF = "VARIANT_OF"
    DISTRIBUTION_ARTIFACT = "DISTRIBUTION_ARTIFACT"
    PATCH_FOR = "PATCH_FOR"
    PATCH_APPLIED = "PATCH_APPLIED"
    COPY_OF = "COPY_OF"
    FILE_ADDED = "FILE_ADDED"
    FILE_DELETED = "FILE_DELETED"
    FILE_MODIFIED = "FILE_MODIFIED"
    EXPANDED_FROM_ARCHIVE = "EXPANDED_FROM_ARCHIVE"
    DYNAMIC_LINK = "DYNAMIC_LINK"
    STATIC_LINK = "STATIC_LINK"
    DATA_FILE_OF = "DATA_FILE_OF"
    TEST_CASE_OF = "TEST_CASE_OF"
    BUILD_TOOL_OF = "BUILD_TOOL_OF"
    DOCUMENTATION_OF = "DOCUMENTATION_OF"
    OPTIONAL_COMPONENT_OF = "OPTIONAL_COMPONENT_OF"
    METAFILE_OF = "METAFILE_OF"
    PACKAGE_OF = "PACKAGE_OF"
    AMENDS = "AMENDS"
    PREREQUISITE_OF = "PREREQUISITE_OF"
    HAS_PREREQUISITE = "HAS_PREREQUISITE"
    OTHER = "OTHER"


class Relationship(object):
    """
    Represents a relationship between multiple SPDX elements
    Fields:
       - source - the source element (first in relationship tag)
       - dest - the dest element (second in relationship tag)
       - relationship  - the relationship between the two
       - comment - a human readable comment for this relationship - Optional
    """

    def __init__(self, source, relationship, dest, comment=""):
        self.source = source
        self.dest = dest
        self.relationship = relationship
        self.comment = comment

    def validate(self, messages):
        if not hasattr(self.source, "spdx_id"):
            messages.append("Source of relationship doesnt have an spdx_id")
        if not hasattr(self.dest, "spdx_id"):
            messages.append("Destination of relationship doesnt have an spdx_id")
        if not hasattr(RelationshipOptions, str(self.relationship)):
            messages.append(str(self.relationship) + " is not a supported relationship")
        return messages
